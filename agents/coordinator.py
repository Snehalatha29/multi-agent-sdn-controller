class Coordinator:
    def decide(self, decisions):
        if "LINK_FAILURE" in decisions:
            return "REROUTE_IMMEDIATELY"
        if "CONGESTED" in decisions:
            return "LOAD_BALANCE"
        if "HIGH_LATENCY" in decisions:
            return "OPTIMIZE_PATH"
        return "NORMAL_OPERATION"
