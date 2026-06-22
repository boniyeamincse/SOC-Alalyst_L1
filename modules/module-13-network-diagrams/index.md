# Module 13: Network Diagrams for SOC Analysts

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- Network diagram কি এবং কেন গুরুত্বপূর্ণ
- Network architecture components
- Firewall rules এবং traffic flow
- VPN এবং remote access
- Network subnets এবং segmentation
- DMZ (Demilitarized Zone)
- Office network, database subnet, application subnet
- NAT (Network Address Translation)
- IP translation এবং private vs public IPs
- Network access control এবং trust boundaries
- Using network diagrams in investigations
- Common network misunderstandings

---

## শুরুর আগে: একটি গল্প

নাসিম একজন SOC analyst। Alert আসে: "Traffic from 192.168.1.50 to database 10.0.2.100".

Without network knowledge:
```
09:00 - Alert দেখলো
09:05 - "Some IPs talking"
09:10 - "Don't know network"
09:15 - Escalate to networking team (wasted time)
```

With network knowledge:
```
09:00 - Alert দেখলো
09:02 - Check network diagram:
       └─ 192.168.1.50 = Office workstation
       └─ 10.0.2.100 = Database server
       └─ They're in SAME subnet
       └─ Communication expected
       
09:05 - Additional context:
       └─ Firewall allows traffic (normal)
       └─ Same department (Finance)
       └─ Expected communication
       
09:08 - Verdict: Benign, normal traffic
Close alert (no escalation needed)
```

**Network knowledge = Faster investigation.**

---

## Network Diagram কি?

### Definition:

**Network Diagram = Visual map of organization's network infrastructure.**

```
Shows:
├─ Physical/logical devices
├─ Connections between devices
├─ IP addresses and subnets
├─ Firewall rules
├─ Access controls
├─ Trust boundaries
├─ Data flow paths
└─ External connections
```

### Why Network Diagrams Matter for SOC:

```
Investigation scenario:

Alert: "Suspicious traffic detected"
Raw data: "10.0.1.100 → 192.0.2.50"

Question: Should this traffic exist?
Without diagram:
├─ Don't know network layout
├─ Can't determine if normal
├─ Guess/escalate

With diagram:
├─ 10.0.1.100 = Internal server
├─ 192.0.2.50 = External server
├─ Check: Is this route allowed?
├─ Check: Is this communication normal?
├─ Make confident decision
```

---

## Basic Network Components

### **1. Firewall**

```
What is it:
└─ Security barrier between networks
   ├─ Controls traffic flow
   ├─ Allows approved traffic
   ├─ Blocks unauthorized traffic
   └─ Logs all decisions

How it works:

Traffic arrives:
├─ Source IP?
├─ Destination IP?
├─ Port?
├─ Protocol?
│
Check against rules:
├─ Is this allowed?
├─ Is this blocked?
├─ Is this logged?
│
Decision:
├─ ALLOW → Traffic passes
├─ DROP → Traffic blocked
└─ REJECT → Blocked + response

Firewall placement:

           Internet
              │
              ▼
        ┌──────────────┐
        │  Firewall    │ (Perimeter defense)
        └──────┬───────┘
               │
        ┌──────▼──────────────┐
        │  Organization       │
        │  Network            │
        └─────────────────────┘

Example rules:
├─ ALLOW 0.0.0.0/0:* → 203.0.113.50:443 (web traffic in)
├─ DROP 10.0.0.0/8 → 192.0.2.0/24 (database blocked from office)
├─ ALLOW 10.0.2.0/24 → 192.0.2.0/24 (app servers to database ok)
└─ LOG ALL ATTEMPTS (for audit)
```

### **2. VPN (Virtual Private Network)**

```
What is it:
└─ Encrypted tunnel for remote access
   ├─ Remote employee connects
   ├─ All traffic encrypted
   ├─ Appears as if on office network
   └─ Access to internal systems

How it works:

Employee at home:
├─ Opens VPN client
├─ Authenticates with username/password
├─ MFA? Yes/No (depending on config)
├─ Connects to VPN server
└─ Traffic encrypted

Inside tunnel:
├─ All traffic encrypted
├─ Cannot see payload
├─ But: Can see source/destination IPs
├─ Can see volume/timing
└─ Can see DNS queries

VPN subnet:
└─ Remote VPN users get IPs
   ├─ Example: 10.0.3.0/24 (VPN subnet)
   ├─ User connects: Gets 10.0.3.100
   ├─ User appears: On internal network
   └─ Access: To systems allowed by rules

Investigation implications:

Alert: "User login from external IP"
├─ If VPN subnet: Expected (working remotely)
├─ If not VPN: Unusual (check if approved)
└─ Different risk levels

Firewall rules VPN:
├─ ALLOW VPN subnet → internal systems (yes)
├─ ALLOW VPN → database (check case-by-case)
└─ VPN users can access what's allowed
```

### **3. Network Subnets**

```
What is it:
└─ Logical division of network
   ├─ 10.0.0.0/16 = Full network
   ├─ 10.0.1.0/24 = Office subnet
   ├─ 10.0.2.0/24 = Database subnet
   ├─ 10.0.3.0/24 = VPN subnet
   └─ etc.

Why subnets:
├─ Organization
├─ Security (separate sensitive systems)
├─ Performance (isolate traffic)
├─ Access control (different rules)

Example subnet layout:

┌─────────────────────────────────────┐
│ Organization Network (10.0.0.0/16)  │
├─────────────────────────────────────┤
│                                     │
│ ┌───────────────────────────────┐  │
│ │ Office Subnet (10.0.1.0/24)   │  │
│ │ ├─ Desktop workstations       │  │
│ │ ├─ Laptops                    │  │
│ │ └─ Office printers            │  │
│ └───────────────────────────────┘  │
│                                     │
│ ┌───────────────────────────────┐  │
│ │ App Subnet (10.0.2.0/24)      │  │
│ │ ├─ Web servers                │  │
│ │ ├─ App servers                │  │
│ │ └─ Cache servers              │  │
│ └───────────────────────────────┘  │
│                                     │
│ ┌───────────────────────────────┐  │
│ │ Database Subnet (10.0.3.0/24) │  │
│ │ ├─ Production DB              │  │
│ │ ├─ Backup DB                  │  │
│ │ └─ DB admin tools             │  │
│ └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘

Investigation use:

Alert: "Traffic between two servers"
├─ Check: Are they in same subnet?
│  └─ Yes = Direct communication expected
│  └─ No = Routed through firewall
├─ Check: Firewall rules allow it?
└─ Decision: Expected or suspicious?
```

### **4. DMZ (Demilitarized Zone)**

```
What is it:
└─ Network zone between internet & internal network
   ├─ More exposed than internal
   ├─ Less protected than internal
   ├─ Specific purpose (web servers, mail)
   └─ Filtered access to internal

Architecture:

         Internet
           │
    ┌──────▼──────┐
    │  Firewall   │
    │  (External) │
    └──────┬──────┘
           │
    ┌──────▼──────────────┐
    │  DMZ                │
    │  ├─ Web servers     │
    │  ├─ Mail servers    │
    │  ├─ DNS servers     │
    │  └─ Proxy servers   │
    └──────┬──────────────┘
           │
    ┌──────▼──────┐
    │  Firewall   │
    │  (Internal) │
    └──────┬──────┘
           │
    ┌──────▼──────────────┐
    │  Internal Network   │
    │  ├─ Databases       │
    │  ├─ Office systems  │
    │  └─ File servers    │
    └─────────────────────┘

DMZ traffic rules:

External → DMZ (web server):
├─ ALLOW 0.0.0.0/0:* → DMZ:443 (HTTPS)
└─ ALLOW 0.0.0.0/0:* → DMZ:80 (HTTP)

DMZ → Internal (database):
├─ ALLOW DMZ:web server → Internal:DB (limited)
├─ ALLOW DMZ:app server → Internal:DB (limited)
└─ DROP DMZ:* → Internal:* (default deny)

Internal → DMZ:
├─ Varies by need
└─ Usually restricted

Investigation implications:

Alert: "Web server accessing database"
├─ Expected: DMZ to internal allowed
├─ But: Check if specific access ok
├─ Firewall: May log which DB accessed
└─ Assessment: Depends on rules

Alert: "DMZ server accessing office"
├─ NOT expected (DMZ shouldn't reach office)
├─ Suspicious: Why needs office access?
└─ Escalate: Investigate immediately
```

---

## IP Addressing: Private vs Public

### Public IP Addresses:

```
Used on internet:
├─ Ranges: 1.0.0.0 - 223.255.255.255 (except private)
├─ Unique: Only one per device (on internet)
├─ Routable: Can reach/be reached from internet
├─ Cost: Must be purchased from ISP
└─ Example: 8.8.8.8 (Google DNS)

Organization public IPs:
├─ 203.0.113.50 = Company website (public)
├─ 203.0.113.51 = Email server (public)
├─ 203.0.113.52 = VPN gateway (public)
└─ etc.

Investigation:
└─ If alert shows public IP:
   ├─ It's external or DMZ
   ├─ Internet-facing system
   ├─ Higher risk (exposed)
   └─ Escalate if compromised
```

### Private IP Addresses:

```
Used internally only:
├─ Ranges: 
│  ├─ 10.0.0.0 - 10.255.255.255 (10.0.0.0/8)
│  ├─ 172.16.0.0 - 172.31.255.255 (172.16.0.0/12)
│  └─ 192.168.0.0 - 192.168.255.255 (192.168.0.0/16)
├─ Not routable: Cannot reach internet directly
├─ Can be reused: Same IPs in different organizations
└─ Free: No cost

Example internal IPs:
├─ 10.0.1.100 = Office workstation
├─ 10.0.2.50 = Database server
├─ 10.0.3.200 = VPN user
└─ etc.

Investigation:
└─ If alert shows private IP:
   ├─ It's internal system
   ├─ Cannot directly access from internet
   ├─ Access through firewall/VPN
   └─ Lower external risk (internal threat focus)
```

### NAT (Network Address Translation):

```
What is it:
└─ Translation between private & public IPs
   ├─ Internal: Uses private IPs
   ├─ External: Uses public IPs
   ├─ NAT: Translates between them
   └─ Firewall usually does NAT

How it works:

Internal device (10.0.1.100) sends traffic:
├─ Packet: "From 10.0.1.100 to 8.8.8.8"
├─ Reaches firewall/NAT device
├─ NAT: Changes source IP to public (203.0.113.50)
├─ Packet: "From 203.0.113.50 to 8.8.8.8"
├─ Sent to internet
└─ Response comes back similarly

Investigation implication:

Alert: "Traffic from internal to external"
├─ Raw IP: 203.0.113.50 (public)
├─ But: Actually from 10.0.1.100 (private)
├─ Investigation: Need to find actual source
├─ Logs: Firewall NAT logs show mapping
└─ Action: Trace back through NAT table

NAT table example:
┌──────────────────┬──────────────────┐
│ Internal IP      │ Public IP         │
├──────────────────┼──────────────────┤
│ 10.0.1.100:54321 │ 203.0.113.50:5000 │
│ 10.0.1.101:54322 │ 203.0.113.50:5001 │
│ 10.0.2.50:3306   │ 203.0.113.50:6000 │
└──────────────────┴──────────────────┘
```

---

## Network Segmentation & Trust Zones

### Trust Boundaries:

```
Network divided by trust level:

MOST TRUSTED (Internal):
├─ Office network
├─ Servers trusted
├─ Admin networks
└─ Management network

MEDIUM TRUST:
├─ Application network
├─ Service network
└─ User network

LEAST TRUSTED (DMZ):
├─ Web servers
├─ Mail servers
└─ Public-facing services

UNTRUSTED:
├─ Internet
├─ Public networks
└─ Guest networks

Access rules based on trust:
├─ Office → Internal: ALLOW (trusted)
├─ Office → DMZ: ALLOW (somewhat restricted)
├─ Office → Internet: ALLOW (monitored)
├─ DMZ → Office: DENY (don't trust DMZ)
├─ DMZ → Database: LIMITED (only app servers)
├─ Internet → Office: DENY (untrusted)
└─ Internet → DMZ: ALLOW (specific ports)

Investigation:

Alert: "System X accessing System Y"

Decision tree:
├─ Are they in same trust zone?
│  └─ Yes: Communication normal
├─ Are they in adjacent trust zones?
│  └─ Depends on firewall rules
├─ Are they in opposite trust zones?
│  └─ Unusual, investigate
└─ Is there firewall rule allowing this?
   └─ Yes: Expected, No: Suspicious
```

---

## Real Network Diagram Example

### Complete Organization Network:

```
                        INTERNET
                           │
        ┌──────────────────┴──────────────────┐
        │     EXTERNAL FIREWALL               │
        └──────────────────┬──────────────────┘
                           │
         ┌─────────────────▼─────────────────┐
         │  DMZ (203.0.113.0/24)             │
         │  ┌───────────────────────────┐   │
         │  │ • Web server (443, 80)     │   │
         │  │ • Mail server (25, 587)    │   │
         │  │ • DNS server (53)          │   │
         │  │ • Proxy server (8080)      │   │
         │  └───────────────────────────┘   │
         └──────────────┬────────────────────┘
                        │
        ┌───────────────▼──────────────┐
        │  INTERNAL FIREWALL           │
        └───────────────┬──────────────┘
                        │
        ┌───────────────▼──────────────────────────┐
        │  INTERNAL NETWORK (10.0.0.0/16)         │
        │                                         │
        │  ┌──────────────────────────────────┐  │
        │  │ OFFICE SUBNET (10.0.1.0/24)      │  │
        │  │ • Workstations (10.0.1.x)        │  │
        │  │ • Laptops (DHCP)                 │  │
        │  │ • Printers                       │  │
        │  └──────────────────────────────────┘  │
        │                                         │
        │  ┌──────────────────────────────────┐  │
        │  │ APP SUBNET (10.0.2.0/24)         │  │
        │  │ • Web app servers (10.0.2.x)     │  │
        │  │ • Cache servers                  │  │
        │  │ • Load balancers                 │  │
        │  └──────────────────────────────────┘  │
        │                                         │
        │  ┌──────────────────────────────────┐  │
        │  │ DATABASE SUBNET (10.0.3.0/24)    │  │
        │  │ • Production DB (10.0.3.50)      │  │
        │  │ • Backup DB (10.0.3.51)          │  │
        │  │ • DB admin tools (10.0.3.100)    │  │
        │  └──────────────────────────────────┘  │
        │                                         │
        │  ┌──────────────────────────────────┐  │
        │  │ ADMIN SUBNET (10.0.4.0/24)       │  │
        │  │ • Admin workstations             │  │
        │  │ • Management servers             │  │
        │  │ • Security tools                 │  │
        │  └──────────────────────────────────┘  │
        │                                         │
        │  ┌──────────────────────────────────┐  │
        │  │ VPN SUBNET (10.0.5.0/24)         │  │
        │  │ • Remote users (10.0.5.x)        │  │
        │  │ • Home workers                   │  │
        │  │ • Contractors                    │  │
        │  └──────────────────────────────────┘  │
        │                                         │
        └─────────────────────────────────────────┘

FIREWALL RULES (Summary):

External → DMZ:
├─ :443 (HTTPS) ALLOW
├─ :80 (HTTP) ALLOW
└─ :25 (SMTP) ALLOW

DMZ → Internal:
├─ DMZ web → App servers:443 ALLOW
├─ App servers → DB:3306 ALLOW
└─ * → Office: DENY

Office ↔ App:
├─ Office → App:443 ALLOW
└─ Office → DB: DENY (no direct access)

VPN → Internal:
├─ VPN → Office: ALLOW
├─ VPN → App: ALLOW
└─ VPN → DB: DENY (unless admin)

Investigation example:

Alert: "10.0.3.50 (DB) accessed by 10.0.1.100 (workstation)"
├─ Check diagram: Direct connection?
│  └─ NO (different subnets)
├─ Check firewall rules:
│  └─ Office → DB: DENY rule
├─ Verdict: Traffic BLOCKED by firewall
│  └─ Alert false positive (traffic never reached)
├─ OR: Workstation routed through app server
│  └─ Need to investigate actual path
└─ Action: Check actual network path
```

---

## Using Network Diagrams in Investigations

### Step-by-Step Process:

```
Alert arrives: "Suspicious connection detected"

STEP 1: Identify IPs
├─ Source IP: 10.0.1.100
├─ Destination IP: 10.0.3.50
└─ Port/Protocol: 3306/MySQL

STEP 2: Lookup in diagram
├─ 10.0.1.100: Office subnet (workstation)
├─ 10.0.3.50: Database subnet (production DB)
└─ Connection: Different subnets

STEP 3: Check trust boundaries
├─ Office: Trusted
├─ Database: Sensitive
├─ Path: Through firewall
└─ Risk: HIGH (crossing trust boundary)

STEP 4: Check firewall rules
├─ Rule: Office → Database DENY
├─ Actual traffic: BLOCKED
├─ Verdict: Traffic never reached

STEP 5: Investigate further
├─ Why alert if traffic blocked?
├─ Possible: Firewall logged attempt
├─ Check: What was attempted?
└─ Decision: Log the attempt (no real access)

STEP 6: Document
└─ Finding: Workstation attempted DB access
└─ Firewall: Blocked the connection
└─ Verdict: BENIGN (firewall working as designed)
└─ Action: Log for monitoring, educate user

Confidence: HIGH (clear network path)
```

---

## Common Network Mistakes

### ❌ **Mistake 1: Confusing private IPs**

**সমস्या:**
```
Alert: "10.0.1.100 accessed external server"
Assumption: External IP = internet threat
Reality: Private IP, internal only (cannot access internet)
```

**সمाधান:**
```
Understand IP ranges:
├─ 10.x.x.x = Private (internal only)
├─ 172.16-31.x.x = Private
├─ 192.168.x.x = Private
└─ Others = Public (internet)

Private IPs cannot directly access internet
Need firewall/gateway for outbound
```

---

### ❌ **Mistake 2: Not understanding NAT**

**সमस्या:**
```
Alert shows: External IP 203.0.113.50
Assumption: That IP compromised
Reality: NAT translation (10.0.1.100 actually sending)
```

**সমाধান:**
```
Understand NAT:
├─ Public IP in logs: May be NAT
├─ Check: Firewall NAT table
├─ Find: Actual internal source
└─ Trace: Back through mapping
```

---

### ❌ **Mistake 3: Ignoring firewall rules**

**समस्या:**
```
Alert: "Traffic between systems"
Assumption: Communication happened
Reality: Firewall blocked it
```

**सऴाधान:**
```
Check firewall rules FIRST
└─ Is traffic allowed?
└─ Blocked = Alert is log, not actual access
└─ Allowed = Traffic actually passed
```

---

### ❌ **Mistake 4: Unknown network diagram**

**समस्या:**
```
Alert about traffic
But: Don't know network layout
Action: Guess or escalate
Result: Wrong decisions
```

**सऴाधान:**
```
MUST know your network:
├─ Get network diagram from IT
├─ Understand subnets
├─ Know firewall rules
├─ Ask questions if unclear
```

---

### ❌ **Mistake 5: Confusing DMZ with internal**

**समस्या:**
```
Alert: "DMZ accessing internal database"
Assumption: Normal (both organization's)
Reality: UNUSUAL (DMZ shouldn't reach internal)
```

**सঋাधান:**
```
Remember trust zones:
├─ DMZ < Internal (less trusted)
├─ DMZ → Internal: Usually DENY
├─ Exception: Limited ports for specific services
└─ DMZ accessing DB: RED FLAG
```

---

## Network Investigation Checklist

### **Quick Network Assessment (1-2 minutes)**

- [ ] Identify both IPs from alert
- [ ] Find IPs in network diagram
- [ ] Determine subnets
- [ ] Are they same subnet or different?
- [ ] Check trust zones: Are they crossing boundary?

### **Detailed Network Analysis (3-5 minutes)**

- [ ] Exact IP locations in diagram
- [ ] Firewall rules allow this traffic?
- [ ] Is this communication normal for these systems?
- [ ] NAT involved? (Check if public IP)
- [ ] DMZ involved? (Special rules)
- [ ] VPN involved? (Remote access?)
- [ ] Traffic path: Direct or routed?
- [ ] Port/protocol: What service?

### **Decision Making**

- [ ] Is traffic allowed by firewall?
- [ ] Is communication expected for these systems?
- [ ] Is there legitimate business reason?
- [ ] Any trust boundary violations?
- [ ] Escalate or investigate further?

---

## Mini Quiz: Network Diagrams

### **Question 1: Private IP range কোনটি?**

A) 8.0.0.0 - 8.255.255.255  
B) 10.0.0.0 - 10.255.255.255  
C) 200.0.0.0 - 200.255.255.255  
D) All of above

**Answer:** B) 10.0.0.0 - 10.255.255.255 - এটাই একটি private range (192.168 এবং 172.16-31 ও আছে)

---

### **Question 2: DMZ থেকে internal database access করা সাধারণত?**

A) Normal, both are internal  
B) Expected behavior  
C) UNUSUAL, should be blocked  
D) Always allowed

**Answer:** C) UNUSUAL, should be blocked - DMZ < trusted, shouldn't reach internal

---

### **Question 3: NAT দ্বারা কি করা হয়?**

A) Adds security to traffic  
B) Encrypts network packets  
C) Translates private IPs to public  
D) Routes traffic faster

**Answer:** C) Translates private IPs to public - মূল NAT function

---

### **Question 4: Firewall rules check করা কেন গুরুত্বপূর্ণ?**

A) তা আগ্রহ মূলক তথ্য  
B) Alert এ দেখা traffic allowed নাকি blocked তা জানতে  
C) Firewall টিম কে সাহায্য করতে  
D) শুধু documentation এর জন্য

**Answer:** B) Alert এ দেখা traffic allowed নাকি blocked তা জানতে - Blocked traffic ≠ actual access

---

### **Question 5: সব private IPs একই সাথে reused করা যায়?**

A) না, প্রতিটি unique হতে হবে  
B) হ্যা, different organizations এ same IP ok  
C) শুধু 10.x.x.x range এ  
D) কখনো না, অনুমতি লাগে

**Answer:** B) হ্যা, different organizations এ same IP ok - এটাই private IP point

---

## সহজ ভাষায় সারসংক্ষেপ

**Network Diagram = Map of organization's network**

**Key Components:**
- **Firewall:** Security barrier, allows/blocks traffic
- **VPN:** Remote access, encrypted tunnel
- **Subnets:** Logical network divisions
- **DMZ:** Exposed zone between internet & internal
- **Trust zones:** Different security levels
- **NAT:** Translates private → public IPs

**IP Addresses:**
- **Private:** 10.x, 172.16-31.x, 192.168.x (internal only)
- **Public:** Others (internet-facing)
- **NAT:** Translation between private & public

**Investigation Steps:**
1. Identify both IPs from alert
2. Find in network diagram
3. Check subnets & trust zones
4. Verify firewall rules allow traffic
5. Confirm expected communication
6. Make confident decision

**Red Flags:**
- DMZ → Internal = UNUSUAL
- Crossing trust boundaries = CHECK
- Firewall DENY rule = Traffic blocked
- Unknown network = Ask for diagram

**Remember:**
- Get network diagram first
- Understand firewall rules
- Know trust zones
- Private IPs stay internal
- DMZ is untrusted layer

---

## Resources for Learning

**Network documentation:**
- Network diagram (get from IT)
- Firewall rules documentation
- Subnet allocation list
- VPN configuration
- DMZ description

**Network training:**
- CompTIA Network+
- Cisco CCNA basics
- Your IT team training
- Network fundamentals course

---

**Module 13 Complete! ✅**

এখন আপনি জানেন:
- ✅ Network diagram এবং গুরুত্ব
- ✅ Firewall কিভাবে কাজ করে
- ✅ VPN এবং remote access
- ✅ Network subnets এবং segmentation
- ✅ DMZ architecture
- ✅ Private vs public IPs
- ✅ NAT translation
- ✅ Trust zones এবং boundaries
- ✅ Using network diagrams in investigations
- ✅ Firewall rules impact
- ✅ Common network mistakes
- ✅ Network investigation workflow

Progress: **13 of 28 modules complete (46%)**

