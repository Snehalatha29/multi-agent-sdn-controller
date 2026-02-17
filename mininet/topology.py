from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI

def run_topology():
    net = Mininet(controller=RemoteController)

    c0 = net.addController('c0', ip='127.0.0.1', port=6653)

    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')

    net.addLink(h1, s1)
    net.addLink(h2, s2)
    net.addLink(h3, s3)
    net.addLink(s1, s2)
    net.addLink(s2, s3)

    net.start()
    CLI(net)
    net.stop()

if __name__ == "__main__":
    run_topology()
