#!/usr/bin/env python3
import subprocess
import time

VIRTUAL_IP  = '10.0.0.10'
VIRTUAL_MAC = '00:00:00:00:00:10'
SWITCH      = 's1'
CLIENT_PORT = 1
current_server = 0

SERVERS = [
    {'name': 'Server1', 'ip': '10.0.0.2', 'mac': '00:00:00:00:00:02', 'port': 2},
    {'name': 'Server2', 'ip': '10.0.0.3', 'mac': '00:00:00:00:00:03', 'port': 3},
    {'name': 'Server3', 'ip': '10.0.0.4', 'mac': '00:00:00:00:00:04', 'port': 4},
]

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0

def setup_reverse_rules():
    print("\n[1] Setting up reverse rules for all servers...")
    for server in SERVERS:
        rev = (
            f"sudo ovs-ofctl -O OpenFlow13 add-flow {SWITCH} "
            f"priority=100,ip,"
            f"in_port={server['port']},"
            f"nw_src={server['ip']},"
            f"actions="
            f"mod_nw_src:{VIRTUAL_IP},"
            f"mod_dl_src:{VIRTUAL_MAC},"
            f"output:{CLIENT_PORT}"
        )
        if run(rev):
            print(f"    ✅ Reverse rule for {server['name']}")

def rotate_to_next_server():
    global current_server
    server = SERVERS[current_server]
    print(f"➡️  Now pointing to {server['name']} ({server['ip']})")
    run(
        f"sudo ovs-ofctl -O OpenFlow13 del-flows {SWITCH} "
        f"ip,in_port={CLIENT_PORT},nw_dst={VIRTUAL_IP}"
    )
    run(
        f"sudo ovs-ofctl -O OpenFlow13 add-flow {SWITCH} "
        f"priority=100,ip,"
        f"in_port={CLIENT_PORT},"
        f"nw_dst={VIRTUAL_IP},"
        f"actions="
        f"mod_nw_dst:{server['ip']},"
        f"mod_dl_dst:{server['mac']},"
        f"output:{server['port']}"
    )
    current_server = (current_server + 1) % len(SERVERS)

def main():
    print("=" * 50)
    print("   SDN Load Balancer — TRUE Round Robin")
    print("=" * 50)
    print("\n[0] Clearing old rules...")
    run(f"sudo ovs-ofctl -O OpenFlow13 del-flows {SWITCH}")
    run(f"sudo ovs-ofctl -O OpenFlow13 add-flow {SWITCH} priority=1,actions=normal")
    setup_reverse_rules()
    print("\n[2] Rotating every 3 seconds... Press Ctrl+C to stop\n")
    while True:
        rotate_to_next_server()
        time.sleep(3)

if __name__ == '__main__':
    main()
