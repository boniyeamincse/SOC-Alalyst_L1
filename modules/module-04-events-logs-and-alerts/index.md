# Module 4: Events, Logs, and Alerts

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- Event কি এবং কিভাবে generate হয়
- Log কি এবং বিভিন্ন log types
- Alert কিভাবে logs থেকে create হয়
- Event vs Log vs Alert এর পার্থক্য
- Log parsing এবং normalization
- Windows এবং Linux logs কিভাবে পড়তে হয়
- Alert lifecycle এবং states
- Real SOC দৃষ্টিকোণ থেকে logs

---

## শুরুর আগে: একটি গল্প

রহিম একটি Bangladeshi e-commerce company এ SOC L1 অ্যানালিস্ট। সকালে সে দেখল alert: "Brute Force Attack Detected".

এই alert কোথা থেকে এলো? রহিম trace করল:

**Chain:**
1. **Event:** Employee login attempt failed 3:45 AM
2. **Log:** Windows event log এ recorded: Event ID 4625
3. **Another Event:** 2nd login attempt failed 3:46 AM
4. **Another Log:** Windows log এ recorded again
5. **... 15 failed attempts ...**
6. **Alert Generation:** SIEM rule এ 15 failures detected → Alert generated

এটাই event, log, alert এর journey। এই module এ এটা detail এ শিখব।

---

## Event, Log, Alert: মূল পার্থক্য

### **Event কি?**

**Event = কোন কিছু ঘটা।**

Events happen সব সময়:
- User login করছে
- File opened হয়েছে
- Network connection made হয়েছে
- Process started হয়েছে
- Password changed হয়েছে

**Event = Discrete occurrence।** Automatic generate হয় system এ।

### **Log কি?**

**Log = Event এর record।**

যখন event ঘটে, system record করে। এই records হল logs।

```
Event (happening):    User tries to login
                      └─ Failed

Log (record):         2024-06-21 03:45:32 
                      EventID: 4625
                      User: john.doe
                      Source IP: 192.168.1.100
                      Result: Failed
```

### **Alert কি?**

**Alert = Log থেকে generated warning।**

যখন patterns detect হয়, alert triggered হয়।

```
Logs (5টি failed attempts):
├─ 03:45 - Failed
├─ 03:46 - Failed
├─ 03:47 - Failed
├─ 03:48 - Failed
└─ 03:49 - Failed
       │
       ▼
Rule triggered: "5 failed logins in 5 mins"
       │
       ▼
Alert generated: "BRUTE FORCE ATTACK DETECTED"
```

### Visual: Event → Log → Alert

```
┌──────────────┐
│    Event     │  "User login attempt"
│   (Happens)  │
└──────┬───────┘
       │
       ▼
┌──────────────────────────┐
│        Log               │  "2024-06-21 03:45:32
│  (Recorded in system)    │   EventID: 4625
│                          │   User: john.doe
│                          │   Result: Failed"
└──────┬───────────────────┘
       │
       │ (5টি logs আসলে)
       │
       ▼
┌──────────────────────────┐
│      Alert               │  "BRUTE FORCE ATTACK
│  (Pattern detected)      │   5 failed logins
│                          │   in 5 minutes"
└──────────────────────────┘
       │
       ▼
    Dashboard
      ↓
   L1 Analyst
```

---

## বিভিন্ন Log Types

একটি modern organization এ হাজারো log sources থাকে:

### **1. Windows Event Logs**

**System:**
```
Event ID: 4625 (Failed logon)
Source: Active Directory
Log Name: Security
When: 2024-06-21 03:45:32
User: john.doe
Source IP: 192.168.1.100
Failure Reason: Invalid password
```

**Common Windows Event IDs:**

| Event ID | Meaning | Alert? |
|----------|---------|--------|
| **4624** | Successful login | Maybe |
| **4625** | Failed login | Yes |
| **4720** | User account created | Yes |
| **4722** | User enabled | Yes |
| **4723** | Password changed | Possible |
| **4728** | Member added to group | Yes |
| **4732** | Member added to local group | Yes |
| **4740** | Account locked | Monitor |
| **5140** | Network share accessed | Monitor |

### **2. Linux Syslog**

**Format:**
```
Jun 21 03:45:32 server01 sshd[1234]: 
Failed password for invalid user admin 
from 192.168.1.100 port 54321 ssh2
```

**Common patterns:**
```
Failed password → Brute force attempt
Invalid user → Enumeration attempt
Accepted password → Successful login
Connection closed → Session ended
```

### **3. Application Logs**

**Web Server (Apache/Nginx):**
```
192.168.1.100 - - [21/Jun/2024:03:45:32] 
"GET /admin/login HTTP/1.1" 401 1234
```

Broken down:
- `192.168.1.100` - Source IP
- `GET /admin/login` - What requested
- `401` - Response (Unauthorized)

**Database Logs:**
```
[ERROR] 2024-06-21 03:45:32 
Access denied for user 'admin'@'192.168.1.100'
```

### **4. Firewall Logs**

```
2024-06-21 03:45:32 
Source: 192.168.1.50
Destination: 10.0.0.100:3389
Action: BLOCKED
Reason: Port not allowed
```

### **5. VPN Logs**

```
2024-06-21 03:45:32
User: alice@company.com
Event: Authentication successful
Source IP: 203.0.113.50 (Singapore)
Session Duration: 2 hours
Data: 500 MB
```

### **6. DNS Logs**

```
2024-06-21 03:45:32
Client: 192.168.1.100
Query: suspicious-domain.com
Result: NXDOMAIN (domain doesn't exist)
```

### **7. Email Logs**

```
2024-06-21 03:45:32
From: attacker@evil.com
To: john@company.com
Subject: Urgent: Verify account
Status: QUARANTINED
Reason: Phishing detected
```

---

## Log Formats এবং Parsing

### সমস্যা: বিভিন্ন format

SIEM এ লক্ষ লক্ষ logs আসে। সবাই different format এ।

```
Windows:    "2024-06-21 03:45:32 EventID 4625 User..."
Linux:      "Jun 21 03:45:32 server01 sshd: Failed..."
Firewall:   "1719 03:45:32 SRC 192.168... DST..."
Email:      "[2024-06-21T03:45:32Z] From=..."
```

**কিভাবে SIEM এই সব বুঝে?**

### **Step 1: Parsing**

SIEM এ parsing rules থাকে প্রতিটি log type এর জন্য।

```
Windows Event ID 4625 parsing rule:
Extract:
- Time: [timestamp]
- User: [username]
- Source IP: [IP address]
- Failure Reason: [reason]
```

### **Step 2: Normalization**

সব logs কে common format এ convert করা।

```
Before:
Windows:  "2024-06-21 03:45:32 EventID 4625..."
Linux:    "Jun 21 03:45:32 server01 sshd: Failed..."

After (Normalized):
{
  timestamp: 2024-06-21T03:45:32Z
  event_type: "failed_login"
  user: "john.doe"
  source_ip: "192.168.1.100"
  source_system: "windows" or "linux"
  failure_reason: "invalid_password"
}
```

### **Step 3: Indexing**

Normalized data index করা যাতে search করা যায়।

```
SIEM Database:
timestamp_index ──→ 2024-06-21T03:45:32Z
user_index ──────→ john.doe
ip_index ────────→ 192.168.1.100
event_type_index ─→ failed_login
```

### **Real SOC Query Example:**

```
You search: "failed_login by user john.doe 
            in last 24 hours"

SIEM:
1. Looks in event_type_index for "failed_login"
2. Filters user_index for "john.doe"
3. Filters by timestamp (last 24h)
4. Returns 47 failed login attempts
```

---

## How Alerts Are Generated

### Alert Rules: SIEM এর "Logic"

SIEM তে rules আছে যা patterns detect করে।

### **Rule Example 1: Simple Threshold**

```
Rule: "Multiple failed logins"

Trigger condition:
  IF (failed_login events >= 5)
     AND (time_window = 5 minutes)
  THEN
     Generate alert: "POSSIBLE BRUTE FORCE"
```

### **Real Scenario:**

```
Timeline:
03:45:01 - Attempt 1: FAILED ─┐
03:45:15 - Attempt 2: FAILED  │
03:45:30 - Attempt 3: FAILED  ├─ 5 failures
03:45:45 - Attempt 4: FAILED  │  in 5 mins
03:46:00 - Attempt 5: FAILED ─┘
03:46:15 - Attempt 6: FAILED

SIEM Rule triggers at 03:46:00
Alert generated: "Brute Force Detected"
```

### **Rule Example 2: Composite Rule**

```
Rule: "Possible account compromise"

Trigger condition:
  IF (failed_login >= 10)
     AND (followed_by: successful_login within 2 min)
     AND (different_source_ip: yes)
  THEN
     Generate alert: "ACCOUNT COMPROMISE RISK"
     Severity: HIGH
```

### **Real Scenario:**

```
03:45-03:50 - 12 failed login attempts
             from IP 192.168.1.100
          ↓
03:51:30   - 1 SUCCESSFUL login
          from IP 203.0.113.50 (Singapore!)
          
Rule triggered:
Alert: "Possible compromise - successful login 
        after brute force from different IP"
```

### **Rule Example 3: Behavior Baseline**

```
Rule: "Unusual data access"

Baseline:
  John normally: 
    - Accesses documents folder (5 GB/day)
    - Works 9-5 IST
    - From office network

Unusual if:
  - Accessing database folder (never before)
  - OR accessing at 3 AM (never before)
  - OR from VPN IP (never before)

Alert: "Unusual access pattern detected"
```

---

## Log Lifecycle: From Event to Investigation

```
┌──────────────────────────────────────────────────────┐
│              Event Happens                            │
│         (User login, file access, etc)               │
└────────────────┬─────────────────────────────────────┘
                 │
                 ▼
         ┌─────────────────────┐
         │   Log Generated     │
         │  (Recorded in OS)   │
         └────────┬────────────┘
                  │
                  ▼
         ┌──────────────────────┐
         │ Log Collection       │
         │ (Sent to SIEM)       │
         │ (Usually real-time)  │
         └────────┬─────────────┘
                  │
                  ▼
         ┌──────────────────────┐
         │ Parsing              │
         │ (Extract fields)     │
         └────────┬─────────────┘
                  │
                  ▼
         ┌──────────────────────┐
         │ Normalization        │
         │ (Standard format)    │
         └────────┬─────────────┘
                  │
                  ▼
         ┌──────────────────────┐
         │ Correlation Rules    │
         │ (Pattern matching)   │
         └────────┬─────────────┘
                  │
              ┌───┴───┐
              │       │
           Pattern NO PATTERN
           matched   (OK)
              │       │
              ▼       ▼
         ┌─────┐  │
         │Alert│ IGNORE
         └──┬──┘  │
            │     │
            ▼     ▼
       Dashboard  Stored
            │     (for audit)
            │
            ▼
        L1 Analyst
       Investigates
            │
          ┌─┴─┐
          │   │
      FP  │   │  TP
          │   │
          ▼   ▼
        Close Escalate
```

---

## Alert States: Lifecycle

একটি alert তার lifetime এ different states এ থাকে:

### **Alert States Diagram:**

```
┌─────────────────┐
│  Generated      │  Alert rule triggered
│  (NEW)          │  Waiting for L1 attention
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Assigned       │  L1 picked it up
│  (IN_PROGRESS)  │  Currently investigating
└────────┬────────┘
         │
     ┌───┴──────────┬──────────┐
     │              │          │
     ▼              ▼          ▼
┌─────────────┐ ┌──────────┐ ┌──────────┐
│  Closed     │ │Escalated │ │ Pending  │
│  (FP/OK)    │ │ (L2/IR)  │ │(Awaiting)│
│             │ │          │ │ Info     │
└─────────────┘ └────┬─────┘ └──────────┘
                     │
                     ▼
            ┌──────────────────┐
            │ Incident Created │
            │  (Case opened)   │
            └──────────────────┘
```

### **Alert State Transitions:**

```
NEW → ASSIGNED
  └─ Timestamp: When L1 claimed it
  └─ Assigned_to: L1_analyst_1

ASSIGNED → INVESTIGATING
  └─ Progress: 25% complete
  └─ Current_step: "Checking user history"

INVESTIGATING → ESCALATED
  └─ Escalation_reason: "Needs malware analysis"
  └─ Escalated_to: L2_analyst_2

ESCALATED → INCIDENT
  └─ Incident_ID: INC-2024-001
  └─ Severity: HIGH

OR

INVESTIGATING → CLOSED
  └─ Verdict: FALSE_POSITIVE
  └─ Reason: "User on business trip, travel approved"
```

---

## Common Log Parsing Issues

### Issue 1: Timestamp Confusion

```
Windows log timestamp:
2024-06-21 03:45:32 (Server time, let's say IST)

But SIEM timezone:
UTC conversion: 2024-06-20 22:15:32 UTC

Problem: Timeline এ gap আসে
```

**Solution:**
```
Always normalize to UTC or single timezone
```

---

### Issue 2: Log Format Variation

```
Same Windows Event ID, different formats:

Format 1:
2024-06-21 03:45:32 EventID:4625 User:john.doe

Format 2:
06/21/2024 03:45:32 
Event: Failed login
Username: john.doe

Format 3:
[2024-06-21T03:45:32Z] 4625|john.doe|Failed
```

**Solution:**
```
Regex-based parsing rules
Custom field extraction
```

---

### Issue 3: Missing Fields

```
Some logs missing source IP:
Before:
2024-06-21 03:45:32 
EventID:4625 
User:john.doe
Source: MISSING

After parsing:
source_ip: "unknown"
```

**Solution:**
```
Set default values
Flag incomplete logs
Request more detailed logging
```

---

## L1 Analyst দৃষ্টিকোণ থেকে Logs

### Investigation Workflow:

**Alert আসে: "Suspicious file download"**

```
Step 1: Alert details দেখুন
├─ Time: 14:30
├─ User: alice@company.com
├─ File: invoice.zip
└─ Source: suspicious-domain.net

Step 2: SIEM এ search করুন
├─ Query: "alice@company.com" last 24 hours
├─ Results: 
│  - 14:25 - Email access
│  - 14:28 - Browser download attempt
│  - 14:30 - Download blocked (FW log)
│  - 14:31 - File quarantine (Email security)
└─ Find: Same IP appeared multiple times

Step 3: Cross-check logs
├─ Email log: Phishing email received
├─ Web proxy log: Redirect to malicious site
├─ File hash log: Known ransomware
└─ Conclusion: Confirmed attack attempt

Step 4: Decision
├─ Escalate to L2 with complete log evidence
└─ Timeline + hash + user info প্রদান করুন
```

---

## Real-World Log Scenarios

### **Scenario 1: Brute Force Attack**

```
Windows Security Logs (Event ID 4625 x 50):
Time sequence:
03:45:01 - john.doe - FAILED
03:45:02 - john.doe - FAILED
03:45:03 - john.doe - FAILED
... (repeated) ...
03:46:45 - john.doe - FAILED

Total: 50 failed attempts in 2 minutes
Source IP: 192.168.1.100

Alert: BRUTE FORCE ATTACK
Severity: HIGH
Recommended Action: Lock account, investigate source
```

### **Scenario 2: Privilege Escalation**

```
Sequence of logs:
1. Event 4624 - User alice login (normal)
2. Event 4688 - Process creation: cmd.exe
3. Event 4698 - Scheduled task created (SUSPICIOUS)
4. Event 4720 - New user account created (CRITICAL)
5. Event 4732 - User added to admin group (CRITICAL)

Timeline: 2 minutes (too fast for normal activity)

Alert: PRIVILEGE ESCALATION ATTEMPT
Severity: CRITICAL
Recommended Action: Immediate incident response
```

### **Scenario 3: Data Exfiltration**

```
Log sequence:
1. Firewall log - Large outbound transfer 500MB
2. DNS log - Query to suspicious-c2.net
3. Proxy log - HTTP POST to external server
4. EDR log - Process: cmd.exe → data upload
5. File access log - Reading sensitive database files

Pattern: File access + Encryption + Exfil

Alert: POSSIBLE DATA EXFILTRATION
Severity: CRITICAL
Recommended Action: Isolate endpoint immediately
```

---

## Common Mistakes: Log Analysis

### ❌ **Mistake 1: Ignoring timestamp mismatches**

**সমস্যা:** Event logs এ 10 seconds gap দেখছি কিন্তু ignore করছি

**সমাধান:** Timestamp সবসময় verify করুন, clock skew check করুন

---

### ❌ **Mistake 2: Not understanding log limits**

**সমস্যা:** এক সপ্তাহের logs দেখছি কিন্তু SIEM এ শুধু 48 hours retention

**সমাধান:** জানুন SIEM এর retention policy

---

### ❌ **Mistake 3: Trusting single log source**

**সমস্যা:** শুধু SIEM এ দেখছি, firewall logs check করছি না

**সমাধান:** সবসময় multiple sources cross-check করুন

---

### ❌ **Mistake 4: Not parsing correctly**

**সমস্যা:** "Source IP: 192.168.1.100" কিন্তু আগে-পিছে space থাকায় query miss হচ্ছে

**সমাধান:** Field trimming, regex properly করুন

---

### ❌ **Mistake 5: Ignoring log volume**

**সমস্যা:** 100,000 logs একসাথে দেখে overwhelmed

**সমাধান:** Time window narrow করুন, filter apply করুন

---

## Practical Checklist: Log Investigation

একটি alert investigate করার সময় logs check করার order:

**✅ Initial Alert Review**
- [ ] Alert time দেখুন (timestamp)
- [ ] Alert source identify করুন (কোন rule)
- [ ] Alert severity note করুন

**✅ Get Timeline Context**
- [ ] Event happen করার ±5 minutes আগে-পিছে কি logs আছে?
- [ ] Same user এর other activities কি?
- [ ] Same source IP এর other activities কি?

**✅ Multiple Log Sources**
- [ ] Windows Event logs check
- [ ] Firewall logs check
- [ ] Email security logs check
- [ ] EDR logs check
- [ ] Application logs check

**✅ Pattern Analysis**
- [ ] Events sequential? (A then B then C?)
- [ ] Timeline logical? (Gap আছে কি?)
- [ ] Same field values repeated?

**✅ Verify Parsing**
- [ ] Field values correct?
- [ ] Timestamp timezone consistent?
- [ ] Missing fields আছে কি?

**✅ Decision Making**
- [ ] Data consistent? (সব logs same story বলছে?)
- [ ] Legitimate explanation আছে?
- [ ] Escalation needed?

---

## Mini Quiz: Logs এবং Alerts

### **Question 1: Event, Log, Alert এর মধ্যে কোনটি first happen করে?**

A) Alert  
B) Log  
C) Event  
D) All happen simultaneously

**Answer:** C) Event - Event happen করে প্রথমে, তারপর log record হয়, তারপর alert generate হয়

---

### **Question 2: SIEM এর parsing এর উদ্দেশ্য কি?**

A) Logs delete করা  
B) Logs কে searchable format এ করা  
C) Alerts block করা  
D) User authenticate করা

**Answer:** B) Logs কে searchable format এ করা - Parsing standardize করে logs কে indexed করতে দেয়

---

### **Question 3: Alert rule "5 failed logins in 2 minutes" - এটা কি type এর rule?**

A) Behavioral  
B) Threshold-based  
C) Composite  
D) Machine learning

**Answer:** B) Threshold-based - একটা specific threshold (5) check করছে

---

### **Question 4: কোন Windows Event ID failed login represent করে?**

A) 4624  
B) 4625  
C) 4720  
D) 5140

**Answer:** B) 4625 - এটাই failed logon এর event ID

---

### **Question 5: Logs কোথায় প্রথম recorded হয়?**

A) SIEM database  
B) Operating system  
C) Alert system  
D) Email

**Answer:** B) Operating system - OS/application প্রথমে local এ log করে, তারপর SIEM এ send করে

---

## সহজ ভাষায় সারসংক্ষেপ

**Event → Log → Alert:**

- **Event:** কিছু ঘটা (login attempt, file access)
- **Log:** সেই ঘটা টা record করা (OS এ save হয়)
- **Alert:** Pattern match হওয়া (Multiple failures = brute force)

**Logs come from:**
- Windows (Event ID)
- Linux (syslog format)
- Firewall (traffic rules)
- Email (message security)
- EDR (endpoint activity)
- Application (custom logging)

**L1 Analyst এর কাজ:**
1. Alert এ click করুন
2. Context gather করুন (logs দেখে)
3. Multiple sources cross-check করুন
4. Pattern analyze করুন
5. Decision নিন (FP or TP?)
6. Escalate বা Close করুন

**Remember:**
- Timestamps সবসময় verify করুন
- Single source trust করবেন না
- Logs সবসময় complete নাও হতে পারে
- Parsing errors possible

---

## Resources for Learning

**Log format understanding:**
- Microsoft - Windows Event Log reference
- Linux - syslog RFC 3164/5424
- NIST - Cybersecurity logging guide

**Your company এর documentation:**
- Log retention policy
- SIEM query syntax
- Alert rule library

---

**Module 4 Complete! ✅**

এখন আপনি জানেন:
- ✅ Event কি
- ✅ Log কি (different types)
- ✅ Alert কিভাবে generate হয়
- ✅ Event vs Log vs Alert পার্থক্য
- ✅ Log parsing এবং normalization
- ✅ Alert lifecycle এবং states
- ✅ Real-world log scenarios
- ✅ Log investigation workflow
- ✅ Common log parsing issues

