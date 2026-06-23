# Module 5: Alert Properties

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- Alert properties কি এবং কেন গুরুত্বপূর্ণ
- Alert details সঠিকভাবে পড়তে হয়
- Time, Name, Severity, Status, Verdict - প্রতিটির মানে
- Alert fields কি information provide করে
- যে properties সবচেয়ে গুরুত্বপূর্ণ investigation এ
- Alert metadata analyze করা
- Incomplete alert data handle করা
- Real SOC alert examples

---

## শুরুর আগে: একটি গল্প

নাজমা একজন senior SOC L1 analyst। তার dashboard এ নতুন alert আসলো। সে দ্রুত click করে alert details দেখলো:

```
Alert Name: Suspicious PowerShell Execution
Severity: HIGH
Status: NEW
Timestamp: 2024-06-21 14:30:45 IST
User: admin@company.com
Source IP: 192.168.1.50
Command: Get-ChildItem -Recurse C:\Windows\System32
```

এখন নাজমা প্রতিটি property বিশ্লেষণ করল:
- **Name:** কি type এর threat?
- **Severity:** কত urgent?
- **Timestamp:** কখন happen করেছে?
- **User:** কার account use হচ্ছে?
- **Source IP:** কোথা থেকে?

এই module এ আমরা শিখব কিভাবে প্রতিটি alert property কে systematically analyze করতে হয়।

---

## Alert Properties: Complete Reference

একটি typical alert এ এই properties থাকে:

### **Core Properties:**

```
┌────────────────────────────────────────────┐
│ Alert Properties                           │
├────────────────────────────────────────────┤
│ • Alert ID / Name                          │
│ • Timestamp (When)                         │
│ • Severity (How serious)                   │
│ • Status (Current state)                   │
│ • Verdict (True/False positive decision)   │
│ • Assigned To (Which analyst)              │
│ • Description (Summary)                    │
│ • Detection Source (Which tool)            │
│ • Rule Name (Which rule triggered)         │
│ • Custom Fields (Context-specific)         │
└────────────────────────────────────────────┘
```

---

## 1. Alert ID / Alert Name

### Alert ID:
```
Unique identifier: INC-2024-000145
OR
ALERT-0001-2024-06-21

Usage:
- Tracking
- Cross-reference
- Escalation
```

### Alert Name:

Alert name সংক্ষিপ্তভাবে বলে কি ঘটেছে:

```
Examples:
- "Brute Force Attack on SMB"
- "Suspicious PowerShell Command"
- "Phishing Email Detected"
- "Ransomware Signature Match"
- "Unusual Data Access"
- "VPN Login from Impossible Location"
```

**Alert name analyze করার সময়:**
- কি type threat? (Malware, phishing, brute force)
- কোথায় detected? (Endpoint, network, email)
- কতটা serious শোনাচ্ছে?

---

## 2. Timestamp

### কেন critical?

Timestamp tell করে **exactly কখন event ঘটেছে।** এটা timeline create করতে help করে।

### Timestamp Format Issues:

```
Different formats, same moment:
- 2024-06-21 14:30:45 (ISO format, readable)
- 1719 14:30:45 (Unix epoch)
- 21/06/2024 2:30:45 PM (Regional)
- 06/21/2024 14:30:45 IST (With timezone)

IMPORTANT: Timezone সবসময় note করুন!
```

### Timestamp Verification:

```
Alert says: 14:30:45
But correlation check করলে:
- File access log: 14:30:50
- Network log: 14:29:40

PROBLEM: 70 second gap!

Investigation:
├─ Clock skew? (System time sync issue)
├─ Logging delay? (Process time to log time)
├─ Multiple events? (Different systems)
└─ Sequence matter করে? (এটা first event?)
```

### L1 Checklist: Timestamp

```
✅ Timestamp note করুন
✅ Timezone confirm করুন
✅ Before/after ±10 minutes logs check করুন
✅ Same device এর other logs সাথে match করুন
✅ Timeline logical আছে কিনা verify করুন
```

---

## 3. Severity

### Severity Levels:

```
Critical / P1 / Red
├─ Immediate threat
├─ Business impact high
├─ Active incident likely
└─ IMMEDIATE ACTION NEEDED

High / P2 / Orange
├─ Significant threat
├─ Potential incident
├─ Escalate to L2
└─ URGENT

Medium / P3 / Yellow
├─ Suspicious activity
├─ Needs investigation
├─ Context dependent
└─ INVESTIGATE SOON

Low / P4 / Blue
├─ Possible FP
├─ Monitor status
├─ Non-urgent
└─ CHECK WHEN TIME
```

### Severity কিভাবে decide হয়?

```
Formula: (Threat_likelihood × Business_impact)

Brute Force Attack:
├─ Threat: HIGH (Known attack)
├─ Impact: MEDIUM (Account compromise)
└─ Severity: HIGH (P2)

Geo-Inconsistent Login:
├─ Threat: MEDIUM (Could be travel)
├─ Impact: LOW (Need verification)
└─ Severity: LOW (P4)

Data Exfiltration:
├─ Threat: CRITICAL (Active data theft)
├─ Impact: CRITICAL (Data loss)
└─ Severity: CRITICAL (P1)
```

### ⚠️ Important:

```
Alert severity ≠ Actual severity

A "LOW" severity alert could be FALSE POSITIVE
OR could be FIRST STEP of multi-stage attack

Example:
Alert: "Unusual login location" (LOW)
Reality: Compromised account + malware deployed next

L1 Job: Context দেখে real severity assess করা
```

---

## 4. Status

### Alert Status States:

```
NEW
├─ Alert just generated
├─ Waiting for L1 attention
├─ MUST ACK within 15 minutes

ASSIGNED
├─ L1 claimed the alert
├─ Currently investigating
├─ Shows: assigned_to, assigned_at

IN_PROGRESS
├─ Active investigation
├─ Awaiting more data
├─ Shows: last_updated_at

ON_HOLD
├─ Waiting for additional info
├─ Waiting for user confirmation
├─ Shows: hold_reason

INVESTIGATING
├─ L2 taking over
├─ Complex analysis
├─ Shows: escalated_to

CLOSED
├─ Investigation complete
├─ Shows: verdict + reason
└─ Final status

REOPENED
├─ New information discovered
├─ Previous closure reviewed
└─ Re-investigation needed
```

### Status Timeline Example:

```
Time        Status          Actor
14:30:00    NEW             SIEM (auto)
14:31:15    ASSIGNED        L1_analyst_1
14:35:00    IN_PROGRESS     L1_analyst_1
14:45:00    ON_HOLD         L1_analyst_1
            (Waiting user confirmation)
15:00:00    INVESTIGATING   L2_analyst_2
            (Escalated as suspicious)
16:30:00    CLOSED          L2_analyst_2
            Verdict: TRUE_POSITIVE
            Reason: "Confirmed compromise"
```

---

## 5. Verdict

### Alert Verdict কি?

**Verdict = Final determination about alert।**

আপনার (বা L2 এর) investigation এর result।

### Verdict Types:

```
TRUE_POSITIVE (TP)
├─ Alert এ লেখা threat real
├─ Actual security event ঘটেছে
├─ Action নেওয়া হবে
└─ Example: "Malware confirmed, isolate device"

FALSE_POSITIVE (FP)
├─ Alert wrong ছিল
├─ No actual threat
├─ Normal activity
└─ Example: "User on approved business trip"

SUSPICIOUS
├─ Investigation incomplete
├─ Could be threat, could be benign
├─ Needs more evidence
└─ Example: "Unusual command, but could be admin"

ESCALATED
├─ Too complex for L1
├─ Needs L2/L3 expertise
├─ Not final verdict yet
└─ Example: "Possible APT activity"

INCONCLUSIVE
├─ Insufficient data
├─ Cannot determine
├─ Recommend: More monitoring
└─ Example: "No corroborating logs found"
```

### Verdict Decision Process:

```
Alert: "Multiple failed logins"

Investigation:
├─ User: john.doe (legitimate employee)
├─ Time: 03:45 AM (off-hours)
├─ Location: Singapore (unusual)
├─ Pattern: 50 failed in 2 minutes (suspicious)
├─ Action taken: Password reset 3 hours later
├─ Activity after: Normal work (email, files)
└─ Find: User called IT at 03:50 about locked account

Decision Matrix:
┌─────────────────────────┬──────────────┐
│ Factor                  │ Result       │
├─────────────────────────┼──────────────┤
│ Legitimate user?        │ YES          │
│ Business reason?        │ YES (travel) │
│ Malicious behavior?     │ NO           │
│ Account compromise?     │ NO           │
└─────────────────────────┴──────────────┘

Verdict: FALSE_POSITIVE
Reason: "Legitimate user on business trip,
         incorrect password attempts during
         timezone adjustment."
```

---

## 6. Assignee

### কে investigate করবে?

```
Alert properties:
├─ assigned_to: L1_analyst_2
├─ assigned_at: 2024-06-21 14:31:15
├─ queue: "High Priority"
└─ escalated_to: L2_analyst_1 (if applicable)
```

### Assignee Routing:

```
Alert comes in
       │
       ▼
Round-robin assignment
OR
Skill-based assignment
OR
Load-based assignment
       │
    ┌──┴──┬──────┬──────┐
    │     │      │      │
L1_1  L1_2   L1_3   L1_4
(2)   (5)    (8)    (1)  ← Current load

Assign to: L1_4 (least busy)
```

### Un-assigned Alerts:

```
Alert sitting NEW for 15+ minutes
└─ Management escalation: "Queue backlog"

Alert stuck IN_PROGRESS for 2+ hours
└─ Manager check: "Analyst stuck? Reassign?"

Alert reassigned:
├─ Old assignee: L1_analyst_1
├─ New assignee: L1_analyst_2
├─ Reason: "L1_analyst_1 on break"
└─ Handover: Context shared
```

---

## 7. Description / Summary

### কি থাকে description এ?

```
Alert details এর natural language summary:

"Multiple failed login attempts detected for user
john.doe from IP 192.168.1.100. Total 50 attempts
in 2 minutes (03:45-03:47 IST). After failed
attempts, one successful login detected at
03:48 IST from same IP. User account may be
compromised."

Contains:
├─ What happened (failed logins)
├─ Who (user: john.doe)
├─ When (timestamp)
├─ Where (source IP)
├─ How many (50 attempts)
├─ Severity implication
└─ Recommended action
```

### Description Length:

```
Too short:
"Bad login"
├─ Not enough context
├─ Analyst confused

Too long:
"User john.doe@company.com (emp ID 12345,
department: Finance, manager: ...) tried to login
12 times with wrong password on server
192.168.1.100 (Ubuntu 20.04, ...) at..."
├─ Overwhelming detail
├─ Hard to parse

Right length:
"Failed login x50 by john.doe from 192.168.1.100
in 2 minutes; 1 successful after. Check account."
├─ Complete
├─ Actionable
├─ Concise
```

---

## 8. Detection Source / Tool

### কোন tool detect করেছে?

```
Detection Source can be:
├─ SIEM (Log correlation)
├─ EDR (Endpoint behavior)
├─ Firewall (Network rule)
├─ Email Security (Phishing detection)
├─ IDS/IPS (Intrusion detection)
├─ Proxy (Web activity)
├─ DNS (Domain query)
└─ Manual (Human discovered)

Alert properties show:
detection_source: "SIEM"
detection_tool: "Splunk"
rule_name: "Brute_Force_Detection_v2"
```

### Source Credibility:

```
Some sources more reliable:

Firewall ✅ HIGH
├─ Network rules clear
├─ Low false positive

EDR ✅ HIGH
├─ Endpoint level detail
├─ Behavioral analysis

Email Security ✅ HIGH
├─ Signature + behavior
├─ Sandbox analysis

SIEM ⚠️  MEDIUM
├─ Depends on rule quality
├─ Can have FP

IDS/IPS ⚠️  MEDIUM
├─ Signature-based
├─ Evasion possible

DNS ⚠️  MEDIUM
├─ Query log only
├─ Not always malicious
```

---

## 9. Alert Fields / Raw Data

### কি fields থাকে alert এ?

```
Common alert fields:

┌─────────────────────────────────────────┐
│ Identity Fields                         │
├─────────────────────────────────────────┤
│ user_id / username                      │
│ email_address                           │
│ domain \ user_account                   │
├─────────────────────────────────────────┤
│ Source Fields (Where from)              │
├─────────────────────────────────────────┤
│ source_ip                               │
│ source_port                             │
│ source_hostname                         │
│ source_application                      │
├─────────────────────────────────────────┤
│ Destination Fields (Where to)           │
├─────────────────────────────────────────┤
│ destination_ip                          │
│ destination_port                        │
│ destination_hostname                    │
│ destination_application                 │
├─────────────────────────────────────────┤
│ Action Fields                           │
├─────────────────────────────────────────┤
│ action_type (login, file_access, etc)   │
│ action_status (success, failed)         │
│ action_result (allowed, blocked)        │
├─────────────────────────────────────────┤
│ Security Indicators                     │
├─────────────────────────────────────────┤
│ malware_name                            │
│ file_hash (MD5, SHA256)                 │
│ file_path                               │
│ process_name                            │
│ command_line                            │
│ url / domain                            │
├─────────────────────────────────────────┤
│ Context Fields                          │
├─────────────────────────────────────────┤
│ device_name                             │
│ device_type                             │
│ os_version                              │
│ geographic_location                     │
│ asn (ISP info)                          │
└─────────────────────────────────────────┘
```

### Field Analysis Example:

```
Alert: "Suspicious PowerShell"

Fields:
source_ip: 192.168.1.50
    ├─ Investigation: Internal IP ✓
    └─ But office closed at this time ❌

user: admin@company.com
    ├─ High privilege account ❌
    └─ Should not run random commands

command: Get-ChildItem -Recurse C:\Windows\System32
    ├─ Reconnaissance pattern ❌
    └─ Listing system directories

timestamp: 03:45 AM
    ├─ Off-hours ❌
    └─ Unusual for admin work

process_parent: explorer.exe
    ├─ Normal ✓
    └─ PowerShell launched from Explorer

SCORE: 4/5 suspicious signals → ESCALATE
```

---

## 10. Custom Fields

### Organization-specific Fields

Different organizations add custom fields:

```
Banking sector:
├─ account_number
├─ transaction_amount
├─ branch_code
└─ compliance_flag

Healthcare:
├─ patient_id
├─ medical_record_id
├─ department
└─ hipaa_violation_flag

E-commerce:
├─ customer_id
├─ order_id
├─ payment_method
└─ fraud_score
```

### Custom Field Usage:

```
Alert with custom fields:
customer_id: "CUST_12345"
    └─ Query: All alerts for this customer?
       
fraud_score: 92/100
    └─ Query: High-risk activity?
    
transaction_amount: 500,000 BDT
    └─ Decision: Escalate (large amount)
```

---

## Alert Properties in Real Investigation

### Complete Alert Example:

```
┌──────────────────────────────────────────────────┐
│ ALERT DETAILS                                    │
├──────────────────────────────────────────────────┤
│                                                  │
│ Alert ID:        ALERT-0145-2024-06-21          │
│ Alert Name:      Brute Force Attack on SMB       │
│                                                  │
│ Timestamp:       2024-06-21 14:30:45 IST         │
│ Severity:        HIGH                           │
│ Status:          ASSIGNED                       │
│                                                  │
│ Assigned To:     L1_analyst_2                    │
│ Assigned At:     2024-06-21 14:31:15 IST         │
│                                                  │
│ Detection:                                      │
│ ├─ Source: SIEM (Splunk)                        │
│ ├─ Rule: Windows_Brute_Force_v3                 │
│ └─ Rule Trigger: ≥5 failed logins in 5 min      │
│                                                  │
│ Key Fields:                                      │
│ ├─ User: admin@company.com                      │
│ ├─ Source IP: 192.168.1.100                     │
│ ├─ Target: File server (\\fs01)                │
│ ├─ Attempt Count: 50                            │
│ ├─ Success Count: 0                             │
│ └─ Status: No successful login                  │
│                                                  │
│ Raw Event Count: 50 Windows Event ID 4625        │
│ Description:                                     │
│ "Multiple failed SMB login attempts from         │
│  192.168.1.100 to admin account on file server. │
│  50 attempts in 2 minutes, no successful login." │
│                                                  │
│ Verdict:        [Pending - Under investigation] │
│ Reason:         ---                             │
│                                                  │
└──────────────────────────────────────────────────┘

L1 Investigation:

Step 1: Check timestamp
├─ 14:30:45 IST, June 21, 2024 ✓
├─ Timezone: India Standard Time ✓
└─ Cross-check with other events in range

Step 2: Analyze fields
├─ User: admin - High privilege account
├─ Source: 192.168.1.100 - Internal IP
├─ Pattern: 50 failures - Brute force signature
└─ Duration: 2 minutes - Rapid-fire attempts

Step 3: Context gathering
├─ Search: admin account login history
├─ Search: 192.168.1.100 activity
├─ Check: Is admin on-site today?
└─ Check: File server access logs

Step 4: Decision
IF all context normal:
  └─ Verdict: FALSE_POSITIVE
     Reason: "Possible misconfigured script"
     
IF suspicious signals found:
  └─ Verdict: ESCALATED
     Action: "Escalate to L2 for deep dive"
     Reason: "Possible account compromise attempt"
```

---

## Incomplete/Missing Alert Properties

### কখন data missing থাকে?

```
Scenario 1: EDR agent not installed
Alert says: "Suspicious file download"
But missing: process_name, file_path, hash
Problem: Cannot verify malware

Scenario 2: Timestamp mismatch
Alert time: 14:30:45
But logs show: 14:30:50
Gap: 5 seconds (normal for processing delay)

Scenario 3: Redaction for privacy
Alert says: File accessed
But missing: File path (redacted for privacy)
Impact: Hard to assess if sensitive data

Scenario 4: Unknown source IP geolocation
Alert has: source_ip = 192.0.2.100
But missing: geographic_location
Impact: Cannot determine if "impossible travel"
```

### Handle Missing Data:

```
✅ DO:
├─ Note missing data
├─ Investigate alternative sources
├─ Ask L2 for help
├─ Document the gap
└─ Request better logging if possible

❌ DON'T:
├─ Assume/guess missing data
├─ Ignore the gap
├─ Make conclusions without data
├─ Close alert prematurely
└─ Escalate vague alerts
```

---

## Common Mistakes: Alert Properties

### ❌ **Mistake 1: Ignoring severity**

**সমস্যা:** CRITICAL alert কিন্তু casual approach

**সমাধান:** Severity অনুযায়ী response time adjust করুন

---

### ❌ **Mistake 2: Trusting timestamp blindly**

**সমস্যা:** Alert says 14:30 কিন্তু clock skew আছে

**সমাধান:** সবসময় cross-check করুন অন্য sources এ

---

### ❌ **Mistake 3: Missing key fields ignore করা**

**সমস্যা:** source_ip নেই কিন্ত investigation continue করছি

**সমাধান:** Key fields miss হলে escalate করুন বা investigate করুন alternate sources থেকে

---

### ❌ **Mistake 4: Alert name এ trust করা**

**সমস্যা:** Alert says "Malware" কিন্তু actually false positive

**সমাধান:** Alert name শুধু starting point। Raw data investigate করুন

---

### ❌ **Mistake 5: Too long investigation without escalation**

**সমস্যা:** 2 hours investigate করেছি কিন্তু আরো info দরকার

**সমাধান:** যখন stuck হন, L2 কে escalate করুন

---

## Practical Checklist: Alert Properties Analysis

নতুন alert পেলে এই order এ check করুন:

**✅ Immediate Context (30 seconds)**
- [ ] Alert Name পড়ুন
- [ ] Severity identify করুন
- [ ] Timestamp note করুন

**✅ Status Check (1 minute)**
- [ ] Status কি? (NEW, ASSIGNED?)
- [ ] আপনি claim করবেন এটা?
- [ ] ACK করুন (acknowledge)

**✅ Key Fields Review (2 minutes)**
- [ ] User কে? (Legitimate employee?)
- [ ] Source কোথা? (Internal/external?)
- [ ] Target কী? (Important system?)
- [ ] What happened? (Process, file, network?)

**✅ Severity Validation (2 minutes)**
- [ ] Alert severity correct কিনা?
- [ ] কোন factors suggest different severity?
- [ ] Business impact কত?

**✅ Field Completeness (1 minute)**
- [ ] Key fields আছে কিনা?
- [ ] কোন important fields missing?
- [ ] Redacted data আছে কিনা?

**✅ Detection Source Credibility (1 minute)**
- [ ] কোন tool detect করেছে?
- [ ] এই tool reliable?
- [ ] False positive rate এ জানা আছে?

**✅ Timeline Verification (2 minutes)**
- [ ] Timestamp সব logs এ consistent?
- [ ] Before/after logs সাথে match?
- [ ] Sequence logical?

**✅ Decision Point (5 minutes)**
- [ ] এখনে investigation complete হয়েছে?
- [ ] এই properties দিয়ে verdict দিতে পারবেন?
- [ ] Need escalation? OR can close?

**Total time: ~15 minutes per alert**

---

## Mini Quiz: Alert Properties

### **Question 1: Alert verdict কি represent করে?**

A) Alert generate হওয়ার কারণ  
B) Investigation result - True/False positive  
C) Alert এ কত events আছে  
D) Who detected the alert

**Answer:** B) Investigation result - True/False positive - Verdict হল final determination

---

### **Question 2: Critical severity alert এ response time কত?**

A) 1 hour  
B) 15 minutes  
C) Within 5 minutes  
D) End of shift

**Answer:** C) Within 5 minutes - Critical alerts need immediate attention

---

### **Question 3: Missing alert properties থাকলে কি করবেন?**

A) Guess করে investigation করুন  
B) Ignore করুন, conclude করুন  
C) Note করুন, alternate sources থেকে investigate করুন  
D) Alert close করে দিন

**Answer:** C) Note করুন, alternate sources থেকে investigate করুন - Missing data সবসময় escalate বা investigate করা উচিত

---

### **Question 4: Timestamp একটি alert এ কখন modify হয়?**

A) কখনো না - Fixed  
B) Alert close হলে  
C) Investigation শেষে  
D) False positive determine হলে

**Answer:** A) কখনো না - Fixed - Timestamp creation এর সময় set হয়, পরে change হয় না

---

### **Question 5: Alert severity kম/বেশি হওয়া সম্ভব reality থেকে?**

A) কখনো না - Always accurate  
B) হ্যা - Alert rule wrong হতে পারে  
C) শুধু HIGH severity এর ক্ষেত্রে  
D) শুধু LOW severity এর ক্ষেত্রে

**Answer:** B) হ্যা - Alert rule wrong হতে পারে - Alert severity ≠ Actual severity; L1 এ context যোগ করে assess করতে হয়

---

## সহজ ভাষায় সারসংক্ষেপ

**Alert Properties = Alert এর "Fingerprint"**

প্রতিটি property গুরুত্বপূর্ণ:

- **Alert Name:** কি ঘটেছে (malware, phishing, brute force)
- **Timestamp:** কখন ঘটেছে
- **Severity:** কত urgent
- **Status:** কোন stage এ
- **Verdict:** TP নাকি FP (final decision)
- **Assignee:** কে investigate করছে
- **Fields:** Details (user, IP, target, action)
- **Source:** কোন tool detected করেছে

**Investigation order:**
1. Alert name + severity
2. Timestamp verify
3. Key fields check
4. Completeness verify
5. Escalate or close

**Remember:**
- Alert severity ≠ Real severity (context দরকার)
- Timestamp সবসময় verify করুন
- Missing fields escalate করুন
- Raw data trust করুন, alert name নয়

---

## Resources for Learning

**Alert Properties documentation:**
- SIEM vendor guide
- আপনার company এর alert schema
- Detection rules documentation

**Field reference:**
- Common Information Model (CIM) - Splunk
- ECS (Elastic Common Schema)
- CEF (Common Event Format)

---

**Module 5 Complete! ✅**

এখন আপনি জানেন:
- ✅ 10টি core alert properties
- ✅ প্রতিটি property কিভাবে analyze করতে হয়
- ✅ Severity কিভাবে determine হয়
- ✅ Verdict types এবং decision process
- ✅ Alert fields কি information দেয়
- ✅ Missing/incomplete data handle করা
- ✅ Alert properties এ common mistakes
- ✅ Properties-based investigation checklist
- ✅ Real-world alert examples

---

<!-- nav-footer -->
## 🧭 Navigation

| | |
|---|---|
| **Previous** | [⬅️ Module 04: Events, Logs & Alerts](../module-04-events-logs-and-alerts/index.md) |
| **Next** | [Module 06: Alert Prioritisation ➡️](../module-06-alert-prioritisation/index.md) |
| **🏠 Course Home** | [STUDY_NOTES.md](../../STUDY_NOTES.md) |
