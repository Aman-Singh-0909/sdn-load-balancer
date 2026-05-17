# 🌐 SDN Load Balancer

A fully functional Software-Defined Network (SDN) load balancer built from scratch using **Mininet**, **Faucet**, and **Open vSwitch** on Kali Linux. This project demonstrates core principles of network automation and programmability used in modern data centers.

> Traffic from a client aimed at a single Virtual IP address is automatically distributed across multiple servers using Round Robin load balancing — exactly how Netflix, Google, and Amazon handle millions of requests!

---

## 📸 Project Overview
┌─────────────────┐
                    │  Faucet Controller  │
                    │   (The Brain 🧠)    │
                    │   Python + OpenFlow │
                    └────────┬────────┘
                             │ programs
                             ▼
Client (h1) ──────────→ [ Switch s1 ] ──────→ Server 1 (h2) 10.0.0.2
10.0.0.1                    │                  "SERVER 1 is handling your request!"
│
sends to                     ├──────────────→ Server 2 (h3) 10.0.0.3
Virtual IP                   │                  "SERVER 2 is handling your request!"
10.0.0.10                    │
└──────────────→ Server 3 (h4) 10.0.0.4
"SERVER 3 is handling your request!"The client always talks to ONE address (10.0.0.10). Behind the scenes, the load balancer secretly rotates which real server handles each request!

---

## 🧠 What is SDN?

Traditional networks use dumb switches — they just forward packets based on hardcoded rules you can't easily change.

**Software Defined Networking (SDN)** separates the "brain" from the "muscle":

| Traditional Network | SDN Network |
|---|---|
| Switch decides everything | Controller decides, switch just follows orders |
| Hard to change rules | Rules changed instantly with software |
| One switch at a time | Control thousands of switches from one place |
| Used in old networks | Used in Google, AWS, Microsoft data centers |

---

## 🛠️ Tools Used

| Tool | Version | Purpose |
|---|---|---|
| **Mininet** | 2.3.0 | Creates virtual network (fake computers + cables) |
| **Open vSwitch** | Latest | Virtual switch that forwards traffic |
| **Faucet** | 1.10.12 | SDN controller that programs the switch |
| **OpenFlow** | 1.3 | Protocol (language) used to program the switch |
| **Python** | 3.13 | Programming language for all scripts |
| **Kali Linux** | 2026.1 | Operating system |

---

## 🗺️ Network Layout

| Host | Role | IP Address | MAC Address | Switch Port |
|---|---|---|---|---|
| h1 | Client | 10.0.0.1 | 00:00:00:00:00:01 | Port 1 |
| h2 | Server 1 | 10.0.0.2 | 00:00:00:00:00:02 | Port 2 |
| h3 | Server 2 | 10.0.0.3 | 00:00:00:00:00:03 | Port 3 |
| h4 | Server 3 | 10.0.0.4 | 00:00:00:00:00:04 | Port 4 |
| — | Virtual IP | 10.0.0.10 | 00:00:00:00:00:10 | — |

---

## 📁 Project Files

| File | Purpose |
|---|---|
| `topology.py` | Builds the virtual network using Mininet |
| `load_balancer.py` | Programs the switch with round robin flow rules |
| `faucet.yaml` | Faucet controller configuration file |
| `README.md` | This file! |

---

## ⚙️ Installation

### Prerequisites

- Kali Linux (tested on 2026.1)
- Internet connection
- Basic terminal knowledge

### Step 1 — Install Mininet from source

```bash
git clone https://github.com/mininet/mininet.git
cd mininet
sudo make install
cd ~
```

### Step 2 — Install Open vSwitch

```bash
sudo apt install -y openvswitch-switch
sudo systemctl start openvswitch-switch
sudo systemctl enable openvswitch-switch
```

### Step 3 — Create Python virtual environment

```bash
python3 -m venv ~/sdnenv
source ~/sdnenv/bin/activate
```

### Step 4 — Install Faucet

```bash
pip install faucet
```

### Step 5 — Setup Faucet config

```bash
sudo mkdir -p /etc/faucet
sudo cp faucet.yaml /etc/faucet/faucet.yaml
mkdir -p ~/sdnenv/var/log/faucet
mkdir -p ~/sdnenv/var/run/faucet
```

---

## 🚀 How To Run

You need **3 terminals** open at the same time.

### Terminal 1 — Start Faucet (the brain)

```bash
source ~/sdnenv/bin/activate
faucet --verbose
```

You will see a lot of EVENT messages scrolling — that is normal! Faucet is running and waiting for a switch to connect.

### Terminal 2 — Start the network

```bash
sudo python3 topology.py
```

You should see:=== Adding Controller ===
=== Adding Switch ===
=== Adding Hosts ===
=== Connecting Cables ===
=== Network Ready! ===
h1 = Client  : 10.0.0.1
h2 = Server1 : 10.0.0.2
h3 = Server2 : 10.0.0.3
h4 = Server3 : 10.0.0.4
mininet>
Once you see `mininet>` start the web servers on each server host:
h2 bash -c 'cd /tmp && python3 -m http.server 80 &'
h3 bash -c 'cd /tmp && python3 -m http.server 80 &'
h4 bash -c 'cd /tmp && python3 -m http.server 80 &'
Also add the ARP entry for the Virtual IP:
h1 arp -s 10.0.0.10 00:00:00:00:00:10
### Terminal 3 — Start the load balancer

```bash
sudo python3 load_balancer.py
```

You should see:
==================================================
SDN Load Balancer — TRUE Round Robin
[0] Clearing old rules...
[1] Setting up reverse rules for all servers...
✅ Reverse rule for Server1
✅ Reverse rule for Server2
✅ Reverse rule for Server3
[2] Rotating every 3 seconds... Press Ctrl+C to stop
➡️  Now pointing to Server1 (10.0.0.2)
➡️  Now pointing to Server2 (10.0.0.3)
➡️  Now pointing to Server3 (10.0.0.4)
---

## 🧪 Testing

Go back to **Terminal 2** (mininet prompt) and run:
h1 curl http://10.0.0.10 -s
h1 curl http://10.0.0.10 -s
h1 curl http://10.0.0.10 -s
Expected output — each request goes to a different server:
SERVER 1 is handling your request!
SERVER 2 is handling your request!
SERVER 3 is handling your request!
That proves the round robin load balancing is working! 🎉

---

## 🔍 How It Works — Step by Step
Step 1: Client (h1) sends HTTP request to Virtual IP 10.0.0.10
↓
Step 2: Packet arrives at Switch (s1)
↓
Step 3: Switch checks its flow rules (programmed by load_balancer.py)
↓
Step 4: Flow rule says "change destination to Server X, send to port X"
Switch rewrites the destination IP and MAC address
↓
Step 5: Packet delivered to real Server (h2 or h3 or h4)
↓
Step 6: Server sends reply back to client
↓
Step 7: Switch intercepts reply, rewrites source back to Virtual IP
Client thinks the reply came from 10.0.0.10
↓
Step 8: load_balancer.py rotates to next server after 3 seconds
Next request goes to next server in line!
---

## 💡 Key Concepts Explained Simply

**Virtual IP** — Like a restaurant's main phone number. You call one number but get connected to whichever waiter is free.

**Round Robin** — Taking turns fairly. Request 1 → Server 1, Request 2 → Server 2, Request 3 → Server 3, Request 4 → back to Server 1.

**Flow Rules** — Standing orders programmed into the switch. Like telling a traffic cop "always send red cars left, blue cars right."

**OpenFlow** — The language our Python script uses to talk to the switch and install flow rules.

**SDN Controller** — The manager sitting in an office giving orders to the switch. In our case that's Faucet.

**ARP** — Like asking "who lives at this address?" before sending a letter. We manually told the client who 10.0.0.10 is so it doesn't have to ask.

---

## 🧹 Cleanup

When you are done, clean up properly:

**Terminal 2** (mininet prompt):
exit
Then in any terminal:
```bash
sudo mn -c
```

**Terminal 1** — Press `Ctrl+C` then:
```bash
deactivate
```

**Terminal 3** — Press `Ctrl+C`

---

## 🚧 Challenges Faced

| Challenge | Solution |
|---|---|
| Mininet not in Kali 2026 apt repos | Installed from source via GitHub |
| Ryu controller incompatible with Python 3.13 | Switched to Faucet which supports modern Python |
| Faucet log folder missing | Created folders manually with mkdir |
| Flow rules overwriting each other | Rewrote load balancer to install one rule at a time and rotate |
| Virtual IP not reachable | Added manual ARP entry with `arp -s` |

---

## 📚 What I Learned

- What SDN is and why it matters in modern networking
- How OpenFlow protocol works
- How to use Mininet to simulate real networks
- How to program a virtual switch with flow rules
- How load balancers distribute traffic
- How Virtual IPs hide real server addresses
- How ARP works at the network layer
- How to use Python virtual environments properly

---

## 🔗 References

- [Mininet Official Site](http://mininet.org)
- [Faucet Documentation](https://docs.faucet.nz)
- [OpenFlow Specification](https://opennetworking.org/sdn-resources/openflow/)
- [Open vSwitch Documentation](https://www.openvswitch.org)

---

## 👤 Author

Built as part of a network automation and programmability project on Kali Linux 2026.1

*"This project proves you can control network traffic flow with software, demonstrating the core principles of network automation used in modern data centers."*

