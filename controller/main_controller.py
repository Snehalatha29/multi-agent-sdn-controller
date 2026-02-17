from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3

from ryu.lib.packet import packet, ethernet
from ryu.lib.packet import ether_types

import random

# --- Multi-Agent Imports ---
from agents.latency_agent import LatencyAgent
from agents.bandwidth_agent import BandwidthAgent
from agents.fault_agent import FaultAgent
from agents.coordinator import Coordinator

# --- Database ---
from database.db_manager import init_db, log_decision


class MultiAgentController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MultiAgentController, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

        # Initialize Agents
        self.latency_agent = LatencyAgent()
        self.bandwidth_agent = BandwidthAgent()
        self.fault_agent = FaultAgent()
        self.coordinator = Coordinator()

        # Initialize Database
        init_db()

        self.logger.info("🚀 Multi-Agent SDN Controller Started")

    # Install default flow rule
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                         ofproto.OFPCML_NO_BUFFER)]

        self.add_flow(datapath, 0, match, actions)

    # Add flow helper
    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(
            ofproto.OFPIT_APPLY_ACTIONS, actions)]

        mod = parser.OFPFlowMod(datapath=datapath,
                               priority=priority,
                               match=match,
                               instructions=inst)

        datapath.send_msg(mod)

    # Packet handler
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        dpid = datapath.id

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        # Ignore LLDP
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return

        dst = eth.dst
        src = eth.src

        self.mac_to_port.setdefault(dpid, {})

        in_port = msg.match['in_port']
        self.mac_to_port[dpid][src] = in_port

        # Decide output port
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # Install flow if known destination
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)

        # Send packet
        data = msg.data
        out = parser.OFPPacketOut(datapath=datapath,
                                 buffer_id=ofproto.OFP_NO_BUFFER,
                                 in_port=in_port,
                                 actions=actions,
                                 data=data)
        datapath.send_msg(out)

        # ---------------------------
        # 🧠 MULTI-AGENT LOGIC
        # ---------------------------
        latency = random.randint(50, 150)
        bandwidth = random.randint(30, 100)
        link_status = random.choice([True, True, True, False])

        latency_decision = self.latency_agent.analyze(latency)
        bandwidth_decision = self.bandwidth_agent.analyze(bandwidth)
        fault_decision = self.fault_agent.analyze(link_status)

        decisions = [latency_decision, bandwidth_decision, fault_decision]
        final_decision = self.coordinator.decide(decisions)

        # Log to console
        self.logger.info(
            f"Agents → Latency:{latency_decision}, "
            f"BW:{bandwidth_decision}, "
            f"Fault:{fault_decision} => Final:{final_decision}"
        )

        # Log to database
        log_decision(latency, bandwidth, fault_decision, final_decision)
