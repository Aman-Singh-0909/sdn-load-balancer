#!/usr/bin/env python3
"""
topology.py
Creates our virtual network:
  - 1 client (h1)
  - 1 switch (s1)
  - 3 servers (h2, h3, h4)
All controlled by Faucet.
"""

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def build_network():

    net = Mininet(
        controller=RemoteController,
        switch=OVSSwitch
    )

    info("=== Adding Controller ===\n")
    net.addController('c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      port=6653)

    info("=== Adding Switch ===\n")
    s1 = net.addSwitch('s1', dpid='0000000000000001')

    info("=== Adding Hosts ===\n")
    client  = net.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
    server1 = net.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
    server2 = net.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03')
    server3 = net.addHost('h4', ip='10.0.0.4/24', mac='00:00:00:00:00:04')

    info("=== Connecting Cables ===\n")
    net.addLink(client,  s1)
    net.addLink(server1, s1)
    net.addLink(server2, s1)
    net.addLink(server3, s1)

    net.start()

    info("=== Setting OpenFlow 1.3 ===\n")
    s1.cmd('ovs-vsctl set bridge s1 protocols=OpenFlow13')

    info("\n=== Network Ready! ===\n")
    info("  h1 = Client  : 10.0.0.1\n")
    info("  h2 = Server1 : 10.0.0.2\n")
    info("  h3 = Server2 : 10.0.0.3\n")
    info("  h4 = Server3 : 10.0.0.4\n")
    info("\nType 'exit' to shut down.\n\n")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    build_network()
