# Module 3: SOC Tools and Environment

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- SIEM (Security Information and Event Management) কি এবং কিভাবে কাজ করে
- EDR (Endpoint Detection and Response) tool কেন গুরুত্বপূর্ণ
- SOAR (Security Orchestration, Automation and Response) automation এ সাহায্য করে
- Firewall এবং VPN logs কীভাবে security monitoring এর জন্য ব্যবহার করা হয়
- Email security tools কেন phishing detect করতে critical
- Threat Intelligence platforms কিভাবে reputation data প্রদান করে
- SOC environment setup এবং access control

---

## শুরুর আগে: একটি গল্প

সোফিয়া একটি Bangladeshi bank এ SOC L1 Analyst হিসেবে কাজ করছে। তার সকালের টাস্ক হল একটি alert investigate করা: "Suspicious login from India". 

সে multiple tools open করে:
1. **SIEM Dashboard** - সব logs একই জায়গায় দেখে
2. **EDR Console** - employee এর laptop এ কি happen করেছে তা দেখে
3. **Threat Intel Platform** - IP এর reputation check করে
4. **Email System** - user এর email activity audit করে
5. **Firewall Logs** - network traffic pattern দেখে

এক ঘণ্টার investigation এ তার সব tools এর data একসাথে ব্যবহার করে সে discover করল - এটা legitimate business trip ছিল, false alarm।

এই module এ আমরা শিখব কিভাবে প্রতিটি tool কাজ করে এবং কখন কোনটা ব্যবহার করতে হয়।

---

## Core SOC Tools: The Stack

একটি modern SOC এ সাধারণত এই tools থাকে:

```
┌─────────────────────────────────────┐
│   Detection Layer (Where data in)   │
│  Firewall, EDR, Email, Web, DNS     │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│  Collection & Processing Layer      │
│   SIEM (Aggregates all logs)       │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│   Correlation & Analysis Layer      │
│  Rules, Alerts, Aggregation        │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│   Investigation & Response Layer    │
│  SOAR, TI Platforms, Manual Inv     │
└─────────────────────────────────────┘
```

---

## 1. SIEM: Security Information and Event Management

### SIEM কি?

**SIEM হল SOC এর central nervous system।** এটি সব থেকে logs collect করে, একত্রিত করে, এবং security alerts generate করে।

### কিভাবে কাজ করে:

```
Data Sources ─┬─ Windows Event Logs
              ├─ Linux Syslogs
              ├─ Firewall Logs
              ├─ VPN Logs
              ├─ Web Server Logs
              ├─ Application Logs
              └─ Database Logs
                       │
                       ▼
              ┌─────────────────────┐
              │  SIEM Aggregation   │
              │  (Normalize data)   │
              └────────┬────────────┘
                       │
                       ▼
              ┌─────────────────────┐
              │  Parsing & Indexing │
              │  (Make searchable)  │
              └────────┬────────────┘
                       │
                       ▼
              ┌─────────────────────┐
              │  Correlation Rules  │
              │  (Pattern matching) │
              └────────┬────────────┘
                       │
                       ▼
              ┌─────────────────────┐
              │  Alert Generation   │
              │  (Your dashboard)   │
              └─────────────────────┘
```

### SIEM এর দায়িত্ব:

**Data Collection:**
- হাজারো সিস্টেম থেকে logs সংগ্রহ করা
- Real-time ও historical data রাখা

**Log Normalization:**
- Different format এর logs কে standard format এ convert করা
- Example: Windows logs ≠ Linux logs, কিন্তু SIEM দুটোকেই বুঝতে পারে

**Correlation:**
- Pattern detect করা
- যেমন: 5টি failed logins → 1টি successful login = suspicious

**Alerting:**
- Rules follow করে alerts generate করা

**Search Capability:**
- আপনি যেকোনো data query করে search করতে পারেন
- Example: "Show all login attempts from IP 192.168.1.100 last 7 days"

### L1 Analyst এর SIEM সাথে কাজ:

```
09:00 - Dashboard open
        └─ "You have 350 alerts"
        
09:15 - Click alert: "Suspicious PowerShell"
        └─ SIEM shows:
           User: admin@company.com
           Time: 03:45 AM
           Command: Get-ChildItem C:\
           Source: 192.168.1.50
           
09:20 - Investigate:
        └─ Search: "admin@company.com" last 24 hours
        └─ Find: 15 other PowerShell commands
        └─ Decision: Pattern analysis
        
09:25 - Escalate to L2 with findings
```

### Popular SIEM Platforms:

| Platform | Known For | Cost |
|----------|-----------|------|
| **Splunk** | Industry leader, powerful | Very High |
| **ELK Stack** | Open source, flexible | Low |
| **IBM QRadar** | Large enterprises | High |
| **ArcSight** | Enterprises | High |
| **Sumo Logic** | Cloud-native | Medium |
| **Fortinet FortiSIEM** | Mid-market | Medium |

---

## 2. EDR: Endpoint Detection and Response

### EDR কি?

**EDR হল প্রতিটি computer এর উপর একটি "detective"।** এটি device level এ suspicious activity monitor করে এবং detect করে।

### কেন EDR প্রয়োজনীয়?

SIEM সব network logs দেখে, কিন্তু **মানুষের computer এর ভিতরে কি হচ্ছে তা দেখতে পারে না।**

EDR এটা solve করে:

```
Network Level (SIEM):        Endpoint Level (EDR):
└─ Login attempt            └─ File executed
└─ Network connection       └─ Process created
└─ Data transfer            └─ Registry changed
                            └─ Memory injection
                            └─ Malware detected
```

### EDR কিভাবে কাজ করে:

```
┌─────────────────────────────┐
│  Agent installed on device  │
│  (Windows, Mac, Linux)      │
└────────────┬────────────────┘
             │
   Continuously monitors:
   ├─ Processes started
   ├─ Network connections
   ├─ File modifications
   ├─ Registry changes
   ├─ Memory activities
   └─ System calls
             │
             ▼
┌─────────────────────────────┐
│  Behavioral Analysis        │
│  (Is this normal?)          │
└────────────┬────────────────┘
             │
    If suspicious:
    ├─ Alert generated
    ├─ Threat score calculated
    ├─ Evidence collected
    └─ Optionally auto-remediate
             │
             ▼
┌─────────────────────────────┐
│  EDR Console (L1 visibility)│
│  Analyst sees details       │
└─────────────────────────────┘
```

### L1 Analyst দৃষ্টিকোণ থেকে EDR:

**Scenario: Alert আসে "Suspicious Process"**

EDR console এ আপনি দেখেন:
```
Device: john-laptop (John's computer)
User: john.doe@company.com
Time: 14:30 IST
Alert: Ransomware behavior detected

Details:
- Process: notepad.exe started
- Child Process: cmd.exe (unusual)
- Files Modified: 500+ on C:\Users\Documents
- Encryption: AES encryption detected
- Network: Connection to 192.0.2.10 (external)
- Risk Score: 95/100 (CRITICAL)

EDR Actions:
- [ ] Quarantine device
- [ ] Isolate network
- [ ] Terminate process
- [ ] Block user
```

### L1 এর পরবর্তী step:

1. **Immediate:** Device isolate করার recommendation করুন
2. **Investigation:** 
   - File pattern কি?
   - আগে এই IP connect হয়েছে?
   - User এর action কি?
3. **Escalation:** L2 কে escalate করুন সম্পূর্ণ context সহ

### Popular EDR Solutions:

| Solution | Known For |
|----------|-----------|
| **CrowdStrike Falcon** | Fast, lightweight |
| **Microsoft Defender for Endpoint** | Integration with Windows |
| **SentinelOne** | Autonomous response |
| **Palo Alto Networks Cortex** | Threat correlation |
| **FireEye Endpoint** | Malware expertise |

---

## 3. SOAR: Security Orchestration, Automation and Response

### SOAR কি?

**SOAR হল SOC এর "automation engine"।** এটি repetitive tasks automatically করে এবং workflow orchestrate করে।

### SOAR এর কাজ:

**তিনটি P:**

1. **Parse:** Data automatically extract করা
2. **Process:** Rules follow করে automatically action নেওয়া
3. **Perform:** রিপোর্ট তৈরি করা, escalation করা, টিকেট close করা

### উদাহরণ: Malware Alert Workflow

```
Alert: "Malware detected on endpoint"

SOAR automatically:
1. Parse:
   └─ Extract device ID, user, file hash
   
2. Process:
   └─ Check threat intel (is this hash known?)
   └─ Check user history (repeat offender?)
   └─ Check device risk (already compromised?)
   
3. Perform:
   ├─ If HIGH_RISK: 
   │  └─ Auto-isolate device
   │  └─ Auto-notify user & manager
   │  └─ Auto-create incident ticket
   │
   ├─ If MEDIUM_RISK:
   │  └─ Auto-quarantine file
   │  └─ Escalate to L2 with context
   │
   └─ If LOW_RISK:
      └─ Auto-close as false positive
      └─ Auto-update SIEM rule
```

### L1 Analyst দৃষ্টিকোণ থেকে SOAR:

```
Before SOAR (Manual):
├─ Alert check করো
├─ Context manually search করো
├─ Manual decision নাও
├─ Manual action নাও
├─ Manual ticket create করো
└─ Time: 30+ minutes

With SOAR (Automated):
├─ Alert arrives
├─ SOAR: Auto-enriches with 10 data points
├─ SOAR: Auto-makes decision
├─ SOAR: Auto-takes action
├─ SOAR: Auto-notifies stakeholders
└─ Time: 30 seconds
└─ L1: Reviews SOAR recommendation
└─ L1: Confirms or corrects
└─ Time: 2 minutes total
```

### SOAR এর সুবিধা L1 এর জন্য:

- **Speed:** 10-15x faster response
- **Accuracy:** Consistent rule-based decisions
- **Volume:** 100x more alerts handle করা যায়
- **Focus:** Complex investigation এ focus করতে পারেন

### Popular SOAR Platforms:

| Platform | Known For |
|----------|-----------|
| **Splunk Phantom** | Easy integration |
| **Palo Alto Networks XSOAR** | Powerful automation |
| **IBM Resilient** | Large enterprises |
| **ServiceNow Security Operations** | IT-security bridge |

---

## 4. Firewall & VPN Logs

### কেন গুরুত্বপূর্ণ?

**Firewall = Network এর bouncer।** এটি সব incoming/outgoing traffic monitor করে।

### Firewall logs কী দেখায়:

```
Log Entry:
Time: 14:23:45
Source IP: 192.168.1.105 (Internal)
Destination IP: 10.0.0.50 (External)
Source Port: 54321
Destination Port: 3389 (RDP)
Protocol: TCP
Action: DENY
Reason: Unapproved destination
```

### Common Firewall Alerts:

| Alert | Meaning | Action |
|-------|---------|--------|
| **Port scan** | Someone scanning ports | Investigate source |
| **Blocked connection** | Firewall denied traffic | Was it supposed to be allowed? |
| **Large data transfer** | Unusual outgoing volume | Data exfiltration check? |
| **Blacklist hit** | Connection to known bad IP | Compromised endpoint? |
| **Unusual protocol** | Traffic on wrong port | Evasion attempt? |

### VPN Logs:

**VPN = Remote employees connect করার gate।**

VPN logs important কারণ:
```
VPN Login Logs:
├─ Who connected (user ID)
├─ When (timestamp)
├─ From where (external IP)
├─ Which location (geographic)
├─ Session duration
└─ Data transferred
```

### L1 Alert Investigation উদাহরণ:

**Alert: "VPN login from unusual location"**

```
Investigation:
1. Check firewall/VPN logs:
   └─ User: alice@company.com
   └─ Time: 02:00 AM (unusual)
   └─ Location: Singapore
   └─ Last login: India

2. Context questions:
   ├─ Is Alice traveling? (Check email/calendar)
   ├─ Has Alice been here before?
   ├─ Is 02:00 AM normal for her?
   ├─ Any failed attempts before success?

3. Decision:
   ├─ If YES to all: Likely legitimate
   ├─ If NO to most: Possible compromise
```

---

## 5. Email Security Tools

### কেন Email Security critical?

**Phishing = সবচেয়ে common attack।** 90%+ breaches phishing দিয়ে শুরু হয়।

### Email Security Tools কী করে:

```
Incoming Email
      │
      ▼
┌─────────────────────────────────┐
│  Malware Scanning               │
│  (Is attachment malicious?)     │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Phishing Detection              │
│  (Is sender spoofed?)           │
│  (Is content malicious?)        │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  URL Reputation Checking        │
│  (Does email have malicious     │
│   links?)                       │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  SPF/DKIM/DMARC Verification   │
│  (Is email from real sender?)   │
└────────────┬────────────────────┘
             │
       SAFE or QUARANTINE
```

### Email Alert Example:

**Alert: "Phishing email detected"**

```
Email Details:
From: amazon-verify@amazonx.com (SPOOFED)
To: john@company.com
Subject: "Confirm your account - urgent action needed"
Attachment: invoice.exe (MALWARE)

Email Security finding:
- ❌ SPF: FAILED
- ❌ DKIM: FAILED
- ❌ Attachment: Trojan.Generic
- ❌ Links: Redirect to phishing site

Action taken:
✓ Email quarantined
✓ User not received
✓ Alert sent to L1
✓ Incident logged
```

### L1 এর Email Investigation:

```
1. Check email metadata:
   - Is really from Amazon?
   - SPF/DKIM authenticated?
   
2. Check recipient:
   - How many users got it?
   - Did anyone click?
   
3. Check payload:
   - Attachment malicious?
   - Links to malicious site?
   
4. Action:
   - Permanently delete from recipients?
   - User security training?
   - Block sender?
```

---

## 6. Threat Intelligence Platforms

### Threat Intelligence কি?

**TI = "আগাম warning সিস্টেম"।** এটি জানা malicious IPs, domains, file hashes রাখে।

### কিভাবে কাজ করে:

```
You find: suspicious IP 185.220.101.50

Query Threat Intelligence Platform:
         │
         ▼
    Database search
         │
    ┌────┴─────┐
    │           │
    ▼           ▼
  "Known    "Not yet
  C2 server known"
  (Malware
  control)
```

### Common TI Lookups:

| Query | Purpose | Data |
|-------|---------|------|
| **IP Reputation** | Is this IP malicious? | ASN, Country, C2 status |
| **Domain Lookup** | Is this domain phishing? | Registration, hosting, DNS |
| **File Hash (MD5/SHA256)** | Is this malware? | Malware name, family, detection |
| **URL Check** | Does this link lead to malware? | Phishing status, redirect |
| **Email Domain** | Is sender legitimate? | MX records, reputation |

### Real SOC Example:

**Alert: "Suspicious download from external URL"**

```
File downloaded:
└─ File name: invoice.zip
└─ URL: http://suspicious-domain.net/files/invoice.zip
└─ SHA256: a1b2c3d4e5f6...

L1 Investigation:
1. Query hash against VirusTotal/AbuseIPDB
   └─ ✓ 45 antivirus detected as malware
   └─ ✓ Known as Trojan.Emotet
   
2. Query domain
   └─ ✗ Registered today
   └─ ✗ Registered with privacy
   └─ ✗ Hosted on free hosting
   
3. Query IP
   └─ ✗ Known C2 infrastructure
   └─ ✗ Reported 1000+ times

Conclusion: CONFIRMED MALWARE
Action: Isolate user, escalate to incident response
```

### Popular TI Platforms:

| Platform | Focus | Cost |
|----------|-------|------|
| **VirusTotal** | File & URL analysis | Free tier |
| **AlienVault OTX** | Community intel | Free |
| **Shodan** | Internet devices | Free/Paid |
| **Censys** | Internet-wide scan | Free/Paid |
| **Recorded Future** | Advanced intel | Paid |
| **ThreatStream** | Enterprise intel | Paid |

---

## SOC Environment: Physical Setup

### Network Architecture:

```
┌─────────────────────────────────────────┐
│        Management Network               │
│   (Segregated, secure access only)     │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
    ┌────────┐ ┌────────┐ ┌────────┐
    │ SIEM   │ │ SOAR   │ │ EDR    │
    │Server  │ │Server  │ │Server  │
    └─┬──────┘ └──┬─────┘ └─┬──────┘
      │           │         │
      └───────────┼─────────┘
                  │
         (Internal network,
          no direct internet)
                  │
      ┌───────────┼──────────┐
      │           │          │
      ▼           ▼          ▼
  ┌────────┐ ┌────────┐ ┌──────────┐
  │Windows │ │Linux   │ │Firewall  │
  │Domain  │ │Servers │ │Logs      │
  │(AD)    │ │        │ │          │
  └────────┘ └────────┘ └──────────┘
      │           │          │
      └───────────┴──────────┘
             │
         (Production Network)
```

### SOC Physical Environment:

**Option 1: Centralized SOC (Large org)**
```
SOC Room:
├─ Rows of desks
├─ Each desk: 2-3 monitors
├─ One large dashboard screen
├─ Meeting room nearby
├─ 24/7 staffed
├─ Access card controlled
├─ No phones/recording allowed
└─ "Secure area"
```

**Option 2: Distributed SOC (Managed/Remote)**
```
Analysts work from:
├─ Home office
├─ Client office
├─ Distributed locations
├─ VPN access required
├─ MFA authentication
├─ Encrypted endpoints
└─ Remote monitoring
```

### Access Control:

**L1 Analyst এর কাছে থাকবে:**
- ✓ Read access to SIEM
- ✓ Read access to EDR
- ✓ Read access to email system
- ✓ Read access to firewall logs
- ✓ Query capability limited to "need-to-know"
- ✓ No direct system access
- ✓ No credential reset authority
- ✗ No delete capability
- ✗ No rule change authority

**Access Log Example:**
```
2024-06-21 09:00 L1_analyst1 logged in - OK
2024-06-21 09:05 Query: "Failed logins last 24h" - OK
2024-06-21 09:15 Try to access L2_credentials - BLOCKED (audit logged)
2024-06-21 09:45 Download: investigation_report.csv - MONITORED
2024-06-21 10:30 L1_analyst1 logged out
```

---

## SOC Dashboard: What You'll See

### Typical Dashboard Layout:

```
┌────────────────────────────────────────────────────────┐
│  SOC Dashboard - Real-time Monitoring                   │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Alerts (Last 24h):  842    │  Critical: 12            │
│  Incidents:          3      │  Open Cases: 8           │
│  Users online:       450    │  Avg Response: 4 mins    │
│                                                         │
├────────────────────────────────────────────────────────┤
│  Top Threats (Last 24h)        │  Alerts by Severity   │
│  ├─ Phishing: 340              │  ├─ Critical: 3%      │
│  ├─ Malware: 215               │  ├─ High: 12%         │
│  ├─ Brute force: 185           │  └─ Medium: 85%       │
│  └─ Data access: 102           │                        │
│                                                         │
├────────────────────────────────────────────────────────┤
│  Pending Alerts (Awaiting triage)                       │
│  ├─ [HIGH] Suspicious PowerShell - 10 mins ago        │
│  ├─ [MED] Failed login 5x - 8 mins ago                │
│  ├─ [LOW] Geo-inconsistent login - 5 mins ago         │
│  └─ [MED] Large file transfer - 2 mins ago            │
│                                                         │
├────────────────────────────────────────────────────────┤
│  Your Queue: 15 alerts assigned to you                 │
│  [Claim Alert]  [My Workload] [Team Status]           │
└────────────────────────────────────────────────────────┘
```

---

## Common Mistakes: Tool Usage

### ❌ **Mistake 1: Only checking SIEM**

**সমস্যা:** Network layer logs দেখছি কিন্তু endpoint এ কি হয়েছে জানি না

**সমাধান:** Always cross-check SIEM + EDR + Email security

---

### ❌ **Mistake 2: Ignoring TI lookups**

**সমস্যা:** Suspicious IP পেয়েছি কিন্তু reputation check করিনি

**সমাধান:** প্রতিটি new IP/domain/hash query করুন TI platform এ

---

### ❌ **Mistake 3: Not understanding tool limitations**

**সমস্যা:** "EDR agent installed নেই যে system এ" - তাই blind spot

**সমাধান:** জানুন কোন device এ agent আছে, কোথায় নেই

---

### ❌ **Mistake 4: Over-relying on automation (SOAR)**

**সমস্যা:** SOAR এ auto-close হয়েছে কিন্তু false positive ছিল

**সমাধান:** SOAR recommendation review করুন, blindly trust করবেন না

---

### ❌ **Mistake 5: Not correlating across tools**

**সমস্যা:** EDR দেখাচ্ছে malware কিন্তু firewall দেখাচ্ছে outbound blocked

**সমাধান:** সব tool এর data একসাথে look করুন complete picture এর জন্য

---

## Practical Checklist: Tool Investigation

যখন কোন alert আসে, এই order এ check করুন:

**✅ Step 1: SIEM Dashboard**
- [ ] Alert details পড়ুন
- [ ] Alert source identify করুন (কোন rule generate করেছে)
- [ ] Immediate context দেখুন

**✅ Step 2: Source Enrichment**
- [ ] Source IP query করুন:
  - [ ] SIEM এ historical আছে?
  - [ ] TI platform এ malicious?
- [ ] Source user query করুন:
  - [ ] New user?
  - [ ] Previous incidents?

**✅ Step 3: Target/Destination**
- [ ] কোন resource access হয়েছে?
- [ ] Server normal কি?
- [ ] Data sensitive কি?

**✅ Step 4: EDR Evidence**
- [ ] Target device এ EDR agent আছে?
- [ ] যদি আছে - endpoint এ কি activity?
- [ ] Process, file, network সব check করুন

**✅ Step 5: Correlate**
- [ ] Timeline match করছে?
- [ ] Multiple sources same story বলছে?
- [ ] কোন gaps?

**✅ Step 6: TI Validation**
- [ ] Suspicious file hash lookup করেছেন?
- [ ] URL/domain reputation check করেছেন?

**✅ Step 7: Make Decision**
- [ ] True positive? → Escalate
- [ ] False positive? → Close with reasoning
- [ ] Need more data? → Gather + escalate

---

## Mini Quiz: Tool Knowledge

### **Question 1: SIEM এর primary কাজ কোনটি?**

A) Endpoint এ malware detect করা  
B) Multiple sources থেকে logs aggregate করা  
C) Automated response নেওয়া  
D) Firewall rules manage করা

**Answer:** B) Multiple sources থেকে logs aggregate করা - এটাই SIEM এর মূল কাজ

---

### **Question 2: EDR agent missing থাকলে, এটা কেন problem?**

A) SIEM কাজ করবে না  
B) Endpoint level activities invisible হবে  
C) Email security fail হবে  
D) Firewall down হবে

**Answer:** B) Endpoint level activities invisible হবে - EDR ছাড়া device monitoring impossible

---

### **Question 3: Threat Intelligence platform এ কী query করতে পারেন?**

A) SIEM rules modify করা  
B) File hashes, IPs, domains এর reputation  
C) Employee পার্সোনাল data  
D) Firewall configuration

**Answer:** B) File hashes, IPs, domains এর reputation - এটাই TI এর purpose

---

### **Question 4: SOAR এর সবচেয়ে বড় সুবিধা কোনটি?**

A) More accurate than SIEM  
B) Automatically repetitive tasks execute করা  
C) Better malware detection  
D) Cheaper than EDR

**Answer:** B) Automatically repetitive tasks execute করা - SOAR এ automation key benefit

---

### **Question 5: Phishing email detect করতে কোন tool সবচেয়ে important?**

A) SIEM  
B) EDR  
C) Email Security Gateway  
D) Firewall

**Answer:** C) Email Security Gateway - Email security tools phishing detection এ specialize করে

---

## সহজ ভাষায় সারসংক্ষেপ

**SOC Toolkit:**

- **SIEM:** "সব logs এর হাব" - সবকিছু এক জায়গায় দেখুন
- **EDR:** "প্রতিটি computer এর bodyguard" - endpoint activity monitor করে
- **SOAR:** "Automation engine" - repetitive tasks automatic করে
- **Firewall/VPN:** "Network এর door" - কে আসছে/যাচ্ছে তা দেখে
- **Email Security:** "Phishing blocker" - malicious email থামায়
- **Threat Intel:** "reputation database" - bad actors এর list রাখে

**Tool Integration:**

```
1 Alert আসে
2 SIEM এ investigation করুন
3 EDR এ endpoint check করুন
4 TI এ reputation verify করুন
5 সব data একসাথে অ্যানালাইজ করুন
6 Decision নিন + escalate
```

---

## Resources for Learning

**Tool-specific Training:**
- আপনার company এর tool documentation
- Vendor-provided training programs
- YouTube tool demos

**General SOC tools:**
- SANS Institute - SOC tools overview
- Cybersecurity frameworks
- Tool comparison articles

---

**Module 3 Complete! ✅**

এখন আপনি জানেন:
- ✅ SIEM কিভাবে logs aggregate করে
- ✅ EDR এন্ডপয়েন্ট monitoring করে
- ✅ SOAR কিভাবে automation করে
- ✅ Firewall/VPN logs এর value
- ✅ Email security phishing রোকায়
- ✅ Threat Intel reputation check করে
- ✅ Tools কিভাবে একসাথে কাজ করে

---

<!-- nav-footer -->
## 🧭 Navigation

| | |
|---|---|
| **Previous** | [⬅️ Module 02: SOC Team Structure](../module-02-soc-team-structure/index.md) |
| **Next** | [Module 04: Events, Logs & Alerts ➡️](../module-04-events-logs-and-alerts/index.md) |
| **🏠 Course Home** | [STUDY_NOTES.md](../../STUDY_NOTES.md) |
