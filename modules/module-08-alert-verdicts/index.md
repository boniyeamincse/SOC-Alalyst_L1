# Module 8: Alert Verdicts and Classifications

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- Verdict কি এবং কেন গুরুত্বপূর্ণ
- Verdict types: True Positive, False Positive, Benign, Suspicious, Escalated
- প্রতিটি verdict এর সংজ্ঞা এবং উদাহরণ
- Verdict framework - কিভাবে classify করবেন
- Decision logic - একটি alert verdict decide করা
- Documentation standards
- Verdict quality metrics
- False Positive vs Benign পার্থক্য
- Real-world verdict examples
- Common verdict mistakes

---

## শুরুর আগে: একটি গল্প

করিম একজন SOC L1 analyst। তিনি একটি alert investigate করেছেন 15 minutes ধরে। এখন findings রয়েছে:

```
Alert: "Large file transfer detected"
Investigation findings:
- User: finance_manager@company.com (legitimate)
- File: monthly_report.xlsx (500 MB)
- Destination: OneDrive (company approved)
- Time: 18:30 (end of workday)
- Context: Month-end report submission (normal)
- No malware, no suspicious destination
```

এখন করিম ticket এ লিখল:
```
Verdict: [What should I write here?]

Options:
A) True Positive
B) False Positive
C) Benign
D) Escalated
E) Other?
```

সঠিক verdict না লিখলে:
- Manager confused হবে (metric wrong হবে)
- Trend analysis ভুল হবে
- Alert rule tuning fail হবে

এই module এ শিখব কীভাবে সঠিক verdict determine করতে হয়।

---

## Verdict কি?

### Definition:

**Verdict = Final determination about alert's true nature।**

সব investigation করার পর, verdict হল সিদ্ধান্ত - এই alert actually কি?

### Verdict vs Status:

```
STATUS: Current position in workflow
├─ NEW
├─ ASSIGNED
├─ IN_PROGRESS
├─ ON_HOLD
├─ INVESTIGATING
├─ CLOSED
└─ REOPENED

VERDICT: Conclusion about alert
├─ TRUE_POSITIVE
├─ FALSE_POSITIVE
├─ BENIGN
├─ SUSPICIOUS
└─ ESCALATED
```

### Key Difference:

```
Status changes multiple times:
NEW → ASSIGNED → IN_PROGRESS → CLOSED

Verdict assigned only ONCE (at end):
When alert is CLOSED
└─ Verdict recorded

Example timeline:
14:30 - Alert NEW (no verdict yet)
14:31 - Alert ASSIGNED (no verdict yet)
14:35 - Alert IN_PROGRESS (no verdict yet)
14:45 - Alert CLOSED (verdict: FALSE_POSITIVE)
```

---

## Five Verdict Types

### **Type 1: TRUE POSITIVE (TP)**

**Definition:** Alert correctly identified real threat/security event.

```
Characteristics:
├─ Alert matched actual security incident
├─ Investigation confirmed threat
├─ Action was justified
├─ Business impact possible
└─ Report as real incident

Real examples:

TP #1: Malware Detection
├─ Alert: "Ransomware signature matched"
├─ Investigation: File hash confirmed malicious
├─ Verdict: TRUE_POSITIVE
├─ Action: Isolate device, restore from backup

TP #2: Account Compromise
├─ Alert: "50 failed logins + 1 success from new IP"
├─ Investigation: Success from attacker IP, 
│  unusual file access detected, credential theft
├─ Verdict: TRUE_POSITIVE
├─ Action: Force password reset, investigate files

TP #3: Data Exfiltration
├─ Alert: "500 GB transfer to external IP"
├─ Investigation: Confirmed C2 communication,
│  sensitive database accessed, transfer confirmed
├─ Verdict: TRUE_POSITIVE
├─ Action: Network isolation, forensics
```

### Documentation Template (TP):

```
Alert ID: ALERT-0001
Alert Name: Ransomware Detected
Investigation Summary:
├─ File detected: invoice.exe
├─ File hash: a1b2c3d4e5f6... (MD5)
├─ Verdict: TRUE_POSITIVE
│
├─ Reasoning:
│ ├─ Hash matched known ransomware (Emotet)
│ ├─ Multiple security vendors flagged
│ ├─ EDR detected suspicious behavior
│ │  └─ File encryption attempts
│ ├─ Network logs: C2 communication
│ └─ Device in use by employee (finance team)
│
├─ Impact Assessment:
│ ├─ Device: finance-laptop (high value)
│ ├─ Potential data: Financial reports, contracts
│ ├─ Risk: High
│ └─ Action: Device isolated, IR activated
│
└─ Recommendations:
  ├─ Restore from last clean backup
  ├─ Reset user credentials
  ├─ Audit file access logs
  └─ Update detection rules

Investigation Time: 8 minutes
Assigned To: L1_analyst_1
Escalated To: Incident Response Team
```

---

### **Type 2: FALSE POSITIVE (FP)**

**Definition:** Alert triggered but there was no actual security issue.

```
Characteristics:
├─ Alert was wrong
├─ No real security event occurred
├─ Activity was benign/normal
├─ No action needed
├─ Should be suppressed from future
└─ Report as FP for metrics

Real examples:

FP #1: Backup Script Retries
├─ Alert: "100 failed login attempts"
├─ Investigation: Backup automation script
│  using old credentials (not changed after reset)
├─ Verdict: FALSE_POSITIVE
├─ Action: Update script credentials, suppress alert

FP #2: Employee Travel
├─ Alert: "Login from impossible location
│  (Tokyo to Singapore in 1 hour)"
├─ Investigation: Employee on business trip,
│  switched hotels, used same VPN connection
├─ Verdict: FALSE_POSITIVE
├─ Action: Review rule, allow travel context

FP #3: Legitimate Large Transfer
├─ Alert: "500 MB data to external IP"
├─ Investigation: Month-end report transfer
│  to approved third-party auditor
├─ Verdict: FALSE_POSITIVE
├─ Action: Whitelist auditor IP, add business context
```

### Documentation Template (FP):

```
Alert ID: ALERT-0002
Alert Name: Brute Force Attack on SMB
Investigation Summary:
├─ Event: Multiple failed logins
├─ Count: 50 attempts in 2 minutes
├─ Verdict: FALSE_POSITIVE
│
├─ Reasoning:
│ ├─ Source: Backup automation script
│ ├─ Script using old credentials
│ │  └─ Credentials changed but script not updated
│ ├─ No successful compromise
│ ├─ No data access attempts
│ └─ Typical retry pattern for automation
│
├─ Root Cause:
│ └─ Credentials changed → Script not updated → Retries
│
├─ Resolution:
│ ├─ Updated script with new credentials
│ ├─ Verified script successful login after fix
│ └─ No further activity
│
├─ Recommendations:
│ ├─ Adjust alert threshold (true brute force
│ │  usually from different source IPs)
│ ├─ Add authentication context to rule
│ └─ Whitelist known internal backup systems
│
└─ Future Prevention:
  ├─ Credential change workflow must include
  │  all dependent systems
  └─ Periodic audit of automation credentials

Investigation Time: 12 minutes
Note: Common FP pattern - similar found yesterday
```

---

### **Type 3: BENIGN**

**Definition:** Alert triggered on legitimate activity with no security implications.

```
⚠️ IMPORTANT: FP vs Benign difference

FALSE POSITIVE:
└─ Alert WRONG - Something happened but not threat

BENIGN:
└─ Alert RIGHT about activity, but activity is SAFE

Example:
Alert: "Unusual file access"
└─ File accessed: YES (alert correct)
└─ Is it malicious? NO
└─ Is it legitimate? YES (regular admin task)
└─ Verdict: BENIGN (not FP)

---

Characteristics (BENIGN):
├─ Activity did occur (alert not wrong)
├─ Activity is legitimate/authorized
├─ No threat indicators
├─ No action needed
└─ But different from FP (happened vs didn't happen)

Real examples:

BENIGN #1: Administrator Maintenance
├─ Alert: "System-level file modifications"
├─ Investigation: Admin patching software
│  (legitimate maintenance)
├─ Activity occurred: YES
├─ Threat: NO
├─ Verdict: BENIGN
├─ Action: None needed

BENIGN #2: Authorized Privilege Escalation
├─ Alert: "User added to admin group"
├─ Investigation: User approved for elevation
│  to admin role (business approved)
├─ Activity occurred: YES
├─ Threat: NO
├─ Verdict: BENIGN
├─ Action: Document approval, close

BENIGN #3: Large Data Transfer
├─ Alert: "1 GB data download"
├─ Investigation: User downloading dataset
│  for analytics project (authorized)
├─ Activity occurred: YES
├─ Threat: NO
├─ Verdict: BENIGN
├─ Action: None needed
```

### Documentation Template (BENIGN):

```
Alert ID: ALERT-0003
Alert Name: Privilege Escalation Detected
Investigation Summary:
├─ Event: User added to admin group
├─ User: data_analyst@company.com
├─ Verdict: BENIGN
│
├─ Reasoning:
│ ├─ Activity did occur (alert correct)
│ ├─ User: Legitimate employee (data team)
│ ├─ Context: New database administration role
│ │  assigned (confirmed with HR/manager)
│ ├─ Approval: IT ticket #12345 shows approval
│ ├─ Business reason: Needs admin access for
│ │  new project
│ └─ No malicious indicators
│
├─ Business Context:
│ └─ User promoted to senior analyst with admin
│    duties (documented in HR system)
│
└─ Notes:
  └─ Alert legitimately triggered on real event
     but activity is authorized and safe

Investigation Time: 5 minutes
Assigned To: L1_analyst_2
```

### FP vs Benign Comparison:

```
                FALSE_POSITIVE    BENIGN
Did activity   
happen?        NO               YES
               Alert wrong      Alert right

Is threat      NO               NO
present?       

Reason         Activity didn't  Activity is
               occur (alert     legitimate
               misfired)        

Example        Backup script    Admin
               using old creds  maintenance
               (doesn't match   (happens &
               actual traffic)  is safe)

Rule fix?      YES - suppress   NO - alert
               or whitelist     working fine
```

---

### **Type 4: SUSPICIOUS**

**Definition:** Alert indicates possible threat but insufficient evidence for confirmation.

```
Characteristics:
├─ Evidence points to possible threat
├─ But not definitive proof
├─ Could be legitimate with context
├─ Needs more investigation/escalation
├─ Cannot close as TRUE/FALSE yet
└─ Usually escalated to L2

Real examples:

SUSPICIOUS #1: Unusual Download
├─ Alert: "Executable downloaded from internet"
├─ Investigation:
│  ├─ File: tool.exe (not recognized)
│  ├─ Source: github.com (legitimate)
│  ├─ User: Developer (reasonable)
│  ├─ But: User doesn't usually download
│  ├─ And: Not in standard tools list
│  └─ File: Not scanned yet
├─ Verdict: SUSPICIOUS (needs more info)
├─ Action: Scan file, check user intent

SUSPICIOUS #2: Unusual File Access Pattern
├─ Alert: "User accessed 100+ files in 1 hour"
├─ Investigation:
│  ├─ User: Legal department
│  ├─ Files: Contract-related (expected area)
│  ├─ But: 100 files unusual quantity
│  ├─ And: Time (late night) unusual
│  ├─ Context: Could be preparing legal case?
│  └─ But: No confirmation
├─ Verdict: SUSPICIOUS (needs verification)
├─ Action: Contact user/manager for context

SUSPICIOUS #3: Failed Login + Password Change
├─ Alert: "3 failed logins → password changed → success"
├─ Investigation:
│  ├─ Timeline: Suspicious sequence
│  ├─ But: Could be user locked out after typo
│  ├─ Or: Actual compromise
│  ├─ No other compromise signals
│  └─ Need to verify with user
├─ Verdict: SUSPICIOUS (needs escalation)
├─ Action: Escalate to L2 for user verification
```

### Documentation Template (SUSPICIOUS):

```
Alert ID: ALERT-0004
Alert Name: Unusual Data Access Pattern
Investigation Summary:
├─ Event: 150 files accessed in 1 hour
├─ User: analyst@company.com
├─ Verdict: SUSPICIOUS
│
├─ Evidence:
│ ├─ Activity level: Unusually high
│ ├─ Time: Late night (01:30 AM)
│ ├─ Files accessed: Database reports (business area OK)
│ ├─ Access method: Standard tools (normal)
│ ├─ Threat signals: None (no malware, no exfil)
│ └─ But: Pattern unusual for this user
│
├─ Possible explanations:
│ ├─ User preparing urgent analysis (legitimate)
│ ├─ User account compromised (threat)
│ └─ Automation script (technical issue)
│
├─ Cannot determine without:
│ ├─ User confirmation of business reason
│ ├─ Endpoint analysis for malware
│ └─ EDR behavior inspection
│
└─ Recommendations:
  ├─ Escalate to L2 for deeper investigation
  ├─ Contact user to verify business context
  └─ Monitor account for further suspicious activity

Investigation Time: 8 minutes
Status: ESCALATED to L2
Reason: Insufficient data to confirm or deny threat
```

---

### **Type 5: ESCALATED**

**Definition:** Alert sent to higher tier for investigation/action.

```
⚠️ IMPORTANT: ESCALATED is NOT final verdict

ESCALATED = Process status
└─ Alert sent to L2/IR for their verdict

Final verdict comes LATER when L2 investigates
└─ L2 will determine: TP, FP, BENIGN, or SUSPICIOUS

Characteristics (ESCALATED):
├─ Investigation started by L1
├─ Complexity beyond L1 scope
├─ High risk signal detected
├─ Needs specialized expertise
├─ Needs immediate response
└─ L1 provides context, L2 investigates

Real examples:

ESCALATED #1: Confirmed Malware
├─ Alert: "Ransomware family detected"
├─ L1 Investigation: Hash confirmed malicious
├─ L1 Verdict: ESCALATED (not L1 decision)
├─ Action: Send to IR team
├─ IR will determine: TP & containment actions

ESCALATED #2: Complex Incident
├─ Alert: "Multiple compromise indicators"
├─ L1 Investigation: Many signals, unclear picture
├─ L1 Verdict: ESCALATED (too complex)
├─ Action: Send to L2 + IR
├─ L2 will do root cause analysis

ESCALATED #3: High-Impact Target
├─ Alert: "C-level executive account accessed unusually"
├─ L1 Investigation: Suspicious but needs business context
├─ L1 Verdict: ESCALATED (executive level)
├─ Action: Send to IR + management notification
└─ IR handles with executive involvement
```

### Documentation Template (ESCALATED):

```
Alert ID: ALERT-0005
Alert Name: Malware Detected - Trojan.Emotet
Investigation Summary:
├─ Event: Malware signature matched
├─ File: invoice.zip
├─ Device: finance-laptop-001
├─ Verdict: ESCALATED
│
├─ L1 Findings:
│ ├─ File hash: a1b2c3d4... (MD5)
│ ├─ Signature: Emotet (known ransomware)
│ ├─ EDR: File quarantined automatically
│ ├─ User: finance_team@company.com
│ ├─ Device: Finance department laptop (HIGH VALUE)
│ └─ Threat level: CRITICAL
│
├─ Escalation Reason:
│ └─ Known malware family detected
│    Device isolation + incident response required
│
├─ Context for L2:
│ ├─ File downloaded from phishing email
│ ├─ Email metadata: [details]
│ ├─ User report: "Opened suspicious email"
│ ├─ EDR agent status: Active, file quarantined
│ └─ Device access before quarantine: [timeline]
│
└─ Recommended Actions:
  ├─ Device isolation (complete network disconnect)
  ├─ Preserve evidence for forensics
  ├─ Audit file server access logs
  ├─ Check for lateral movement
  └─ Notify finance management

Investigation Time: 7 minutes
Status: ESCALATED to Incident Response
Priority: CRITICAL - Immediate IR activation
Next: IR team contacts device user for permission
```

---

## Verdict Framework: Decision Logic

### Decision Tree:

```
START: Investigation Complete

  ├─ Is there actual security incident?
  │
  ├─ YES
  │  │
  │  ├─ Is severity CRITICAL/HIGH?
  │  │  ├─ YES → ESCALATED (to IR/L2)
  │  │  └─ NO → TRUE_POSITIVE (document finding)
  │  │
  │  └─ Is activity unauthorized/malicious?
  │     ├─ YES → TRUE_POSITIVE
  │     └─ NO → BENIGN
  │
  ├─ NO (No incident)
  │  │
  │  ├─ Did activity actually occur?
  │  │  ├─ YES → FALSE_POSITIVE (alert misfired)
  │  │  └─ NO → BENIGN (legitimate, no threat)
  │  │
  │  └─ Unclear after investigation?
  │     └─ SUSPICIOUS (escalate to L2)
  │
  └─ CANNOT DETERMINE
     └─ SUSPICIOUS (escalate)
```

### Practical Decision Matrix:

```
┌─────────────────────────────────────────────────────────┐
│ Verdict Decision Matrix                                  │
├──────────────────┬──────────────┬──────────────────────┤
│ Activity Occurred │ Is Malicious │ Verdict              │
├──────────────────┼──────────────┼──────────────────────┤
│ YES              │ YES          │ TRUE_POSITIVE        │
│ YES              │ NO           │ BENIGN               │
│ NO               │ YES          │ FALSE_POSITIVE       │
│ NO               │ NO           │ FALSE_POSITIVE       │
│ UNCLEAR          │ UNCLEAR      │ SUSPICIOUS           │
│ HIGH RISK        │ ANY          │ ESCALATED            │
└──────────────────┴──────────────┴──────────────────────┘

Quick examples:

Invoice.exe downloaded + malware = TP
  Activity: YES (file downloaded)
  Malicious: YES (ransomware family)
  Verdict: TRUE_POSITIVE

50 login failures from backup script = FP
  Activity: Actually login attempts (logs show it)
  But: From expected source (script)
  Alert trigger: Wrong (rule too sensitive)
  Verdict: FALSE_POSITIVE

Admin file access during maintenance = BENIGN
  Activity: YES (files accessed)
  Legitimate: YES (admin task, authorized)
  Threat: NO
  Verdict: BENIGN

Suspicious download + no context = SUSPICIOUS
  Activity: YES (download occurred)
  Malicious: UNCLEAR (file unknown, need scan)
  Verdict: SUSPICIOUS (escalate for scan)
```

---

## Real-World Verdict Examples

### **Example 1: Malware → TRUE POSITIVE**

```
Alert: "Ransomware Signature Match"
Raw Data:
├─ File: invoice.pdf.exe
├─ Location: C:\Users\john\Downloads
├─ Hash: 5d41402abc4b2a76b9719d911017c592
└─ Signature: Trojan.Emotet

Investigation:
├─ Step 1: Verify hash
│  └─ VirusTotal: 53/71 vendors flagged
│
├─ Step 2: Check EDR
│  └─ Process behavior: Encrypted files, C2 connection
│
├─ Step 3: Verify user
│  └─ User john: Legitimate (but not tech-savvy)
│
├─ Step 4: Check file source
│  └─ Email: Phishing email (spoofed Adobe)
│
├─ Step 5: Check timeline
│  └─ Downloaded 10:30 AM
│  └─ EDR alerts 10:35 AM (5 min delay)
│  └─ File attempts encryption 10:35 AM

Analysis:
├─ Multiple indicators = CONFIRMED threat
├─ Malware family = Ransomware risk
├─ Activity = Encryption and C2 comm
└─ No legitimate explanation

VERDICT: TRUE_POSITIVE
Escalation: IMMEDIATE to IR
Action: Isolate device, restore backup
```

### **Example 2: Admin Access → BENIGN**

```
Alert: "Privilege Escalation - User Added to Admin Group"
Raw Data:
├─ User: alice@company.com
├─ Time: 2024-06-21 09:30 IST
├─ Group: Domain Admins
└─ Source: AD PowerShell script

Investigation:
├─ Step 1: Check user
│  └─ alice: Senior IT staff (legitimate)
│
├─ Step 2: Check AD history
│  └─ Previous: Power User group
│  └─ Change: Deliberate (not unauthorized)
│
├─ Step 3: Check IT tickets
│  └─ IT ticket #5678: "Promote alice to admin"
│  └─ Approval: IT Director + CTO
│  └─ Reason: New infrastructure project
│
├─ Step 4: Check EDR
│  └─ Alice: Using corporate laptop
│  └─ Behavior: Normal admin activities
│
├─ Step 5: Check business context
│  └─ Project: Database migration (confirmed)
│  └─ alice role: Project lead (confirmed)
│  └─ Temporary: Yes (90 days, then rollback)

Analysis:
├─ Activity occurred: YES (elevation real)
├─ Legitimate reason: YES (approved ticket)
├─ Authorization: YES (director approved)
├─ Business context: YES (known project)
└─ Risk: NONE

VERDICT: BENIGN
Action: Close, update access documentation
```

### **Example 3: Backup → FALSE POSITIVE**

```
Alert: "Brute Force Attack - 100 Failed Logins"
Raw Data:
├─ User: sa_backup_service
├─ Count: 100 attempts
├─ Time: 03:00-03:05 AM (nightly)
└─ Source: Backup server

Investigation:
├─ Step 1: Verify events
│  └─ SIEM: 100 Event ID 4625 (failed logon)
│
├─ Step 2: Check user
│  └─ User: Service account (backup automation)
│  └─ Not human user
│
├─ Step 3: Check context
│  └─ Scheduled: Backup runs nightly at 03:00
│  └─ Frequency: Daily (same pattern every day)
│
├─ Step 4: Check AD history
│  └─ Account: Created 2022 for backup system
│  └─ Status: Active
│  └─ Last 30 days: Same failure pattern
│
├─ Step 5: Identify root cause
│  └─ Script issue: Using old password
│  └─ Password changed 2 months ago
│  └─ Script not updated (admin oversight)
│
├─ Step 6: Check infrastructure
│  └─ Backup: Still succeeds somehow
│  └─ Reason: Retries after failures work
│
├─ Step 7: Verify no compromise
│  └─ Account: Never succeeded with new password
│  └─ But: Backup completed (must have alt path)
│  └─ No suspicious activity

Analysis:
├─ Alert triggered: YES
├─ Threat present: NO
├─ Activity dangerous: NO
├─ Legitimate explanation: YES (old password)
├─ Rule issue: YES (should whitelist known services)
└─ Alert misfired: YES

VERDICT: FALSE_POSITIVE
Root Cause: Script credentials not updated after AD password change
Action: Update script, suppress similar alerts, add to whitelist
Recommendation: Implement credential change workflow
```

### **Example 4: Unclear → SUSPICIOUS**

```
Alert: "Unusual File Access Pattern"
Raw Data:
├─ User: developer@company.com
├─ Files: 200+ accessed in 1 hour
├─ Type: Source code repositories
├─ Time: 22:30 (after hours)
└─ Device: Developer laptop

Investigation:
├─ Step 1: Verify activity
│  └─ SIEM: Confirmed (file access logs)
│
├─ Step 2: Check user
│  └─ User: Senior developer (legitimate)
│  └─ Access: Has permissions to these files
│
├─ Step 3: Check pattern
│  └─ Frequency: First time accessing 200+ files/hour
│  └─ Usual: 20-30 files per session
│  └─ Volume: 10x normal
│
├─ Step 4: Check context
│  └─ Business: No announced urgent project
│  └─ Calendar: No late work scheduled
│  └─ Slack: No activity indicating work
│
├─ Step 5: Check file details
│  └─ Files: Mix of source code + config
│  └─ No sensitive files accessed
│  └─ No data files accessed
│
├─ Step 6: Check for malware
│  └─ EDR: No suspicious processes
│  └─ Network: No suspicious connections
│  └─ Files: No encryption attempts
│  └─ Device: No compromise signals
│
Analysis:
├─ Activity: Confirmed, unusual volume
├─ User: Legitimate with access
├─ Files: Code only, not sensitive data
├─ Threat signals: NONE detected
├─ Legitimate explanation: UNKNOWN
│  ├─ Could be: Working on urgent project
│  ├─ Could be: Script accessing files
│  ├─ Could be: Preparation for something
│  └─ Need user confirmation
├─ Malware: No indicators
├─ Compromise: No indicators
└─ Cannot determine: YES

VERDICT: SUSPICIOUS
Reason: Unusual activity with no clear business context
Action: Escalate to L2 for user verification
Next: L2 contacts user to understand business reason
```

---

## Verdict Quality Metrics

### How SOC tracks verdict accuracy:

```
Organization tracks:

FALSE POSITIVE RATE:
└─ Out of 100 closed alerts
   └─ How many were actually FP?
   └─ Target: < 10% (best practice: 5-7%)

TRUE POSITIVE RATE:
└─ Out of 100 TP alerts
   └─ How many were actual threats?
   └─ Target: > 95%

ESCALATION RATE:
└─ Out of 100 alerts
   └─ How many escalated to L2?
   └─ Target: 10-15% (too high = rule issues)

VERDICT AGREEMENT RATE:
└─ When L2 reviews L1 verdicts
   └─ How many agree with L1?
   └─ Target: > 90%

TRIAGE ACCURACY:
└─ Out of 100 closed alerts
   └─ How many correct verdict on first try?
   └─ Target: > 85%
```

### Your Performance Tracked:

```
Personal metrics (L1 analyst):
├─ Alerts handled/day: 40-60
├─ FP rate: __%
├─ Average triage time: __ minutes
├─ Escalation accuracy: __%
├─ L2 agreement rate: __%
└─ Monthly target:
   ├─ Handle: 1000+ alerts
   ├─ FP rate: < 10%
   ├─ Average time: < 15 min
   └─ Accuracy: > 85%

Monthly review:
├─ Manager checks metrics
├─ Trends: Improving? Declining?
├─ Common mistakes: What category?
├─ Training: What areas need work?
└─ Recognition: Best verdicts this month?
```

---

## Common Verdict Mistakes

### ❌ **Mistake 1: Confusing FP and BENIGN**

**সমস্যা:**
```
Alert: "Admin file access"
Investigation: Legitimate admin task
Verdict marked: FALSE_POSITIVE

WRONG! Should be: BENIGN
Reason: Activity occurred (admin really accessed files)
        Alert was right about activity
        But activity is legitimate
```

**সমাধান:**
```
FP = Alert wrong about whether activity happened
BENIGN = Alert right, but activity is legitimate
```

---

### ❌ **Mistake 2: Not escalating SUSPICIOUS**

**সমস্যা:**
```
Alert: Unclear threat
Investigation: Cannot determine if threat
Verdict marked: FALSE_POSITIVE

WRONG! Should be: SUSPICIOUS
Reason: Not enough data to close
        Escalate to L2
```

**সমাধান:**
```
When uncertain → SUSPICIOUS (escalate)
Don't close with guess
```

---

### ❌ **Mistake 3: TP without confirmation**

**সমস্যা:**
```
Alert: Potential malware
Verdict marked: TRUE_POSITIVE
But: No actual verification (too confident)

WRONG! Without verification
```

**সমাধান:**
```
TP needs:
├─ Threat confirmed (hash checked, behavior analyzed)
├─ Context verified (not legitimate use)
└─ Escalation/action taken
```

---

### ❌ **Mistake 4: Poor documentation**

**সমস্যা:**
```
Alert: [some alert]
Verdict: TRUE_POSITIVE
Reason: "Looks bad"

WRONG! No detail
```

**সমাধান:**
```
Always document:
├─ What did you find?
├─ Why is it this verdict?
├─ What evidence?
├─ What action taken?
```

---

### ❌ **Mistake 5: Changing verdict after close**

**সমস্যা:**
```
Alert closed as FALSE_POSITIVE
3 days later: "Actually, it was threat"
└─ Try to reopen + change verdict
```

**সমাধান:**
```
Cannot change closed alert verdict
Must reopen as NEW incident
Prevents metric manipulation
```

---

## Verdict Documentation Standard

### Required Fields:

```
Alert ID: [unique identifier]
Alert Name: [rule name]

Investigation Findings:
├─ What did you discover?
├─ What evidence?
├─ What system/user involved?
└─ Timeline of events

Verdict: [Choose one]
├─ TRUE_POSITIVE
├─ FALSE_POSITIVE
├─ BENIGN
├─ SUSPICIOUS
└─ ESCALATED

Reasoning: [Explain why]
├─ What led to this verdict?
├─ What evidence?
├─ What was ruled out?
└─ Why not other verdict?

Actions Taken:
├─ What did you do?
├─ Close/Escalate?
├─ Notify who?
└─ Recommend what?

Time Spent:
├─ Triage start: HH:MM
├─ Triage end: HH:MM
└─ Total: __ minutes

Assigned To: [Your name]
Escalated To: [If applicable]

Additional Notes:
├─ Similar alerts seen before?
├─ Pattern observations?
├─ Rule improvement suggestions?
└─ Training notes?
```

---

## Mini Quiz: Alert Verdicts

### **Question 1: Alert status এবং verdict এর মধ্যে পার্থক্য কি?**

A) একই জিনিস, different names  
B) Status = workflow position, Verdict = conclusion about threat  
C) Status applied at end, Verdict multiple times  
D) No difference

**Answer:** B) Status = workflow position, Verdict = conclusion about threat - Status changes during investigation, Verdict only at end

---

### **Question 2: FALSE_POSITIVE এবং BENIGN এর মধ্যে পার্থক্য কি?**

A) No difference  
B) FP = activity didn't happen, BENIGN = activity is legitimate  
C) Both mean safe, just different words  
D) BENIGN is serious, FP is not

**Answer:** B) FP = activity didn't happen, BENIGN = activity is legitimate - Key difference: whether activity actually occurred

---

### **Question 3: SUSPICIOUS verdict এর অর্থ কি?**

A) Definitely a threat  
B) Definitely not a threat  
C) Uncertain, needs more investigation  
D) Ready to close

**Answer:** C) Uncertain, needs more investigation - SUSPICIOUS means escalate to L2, not final verdict

---

### **Question 4: কখন ESCALATED verdict ব্যবহার করবেন?**

A) When you're confused  
B) When alert is high risk or needs expertise  
C) When you want to avoid decision  
D) For all alerts

**Answer:** B) When alert is high risk or needs expertise - ESCALATED for IR-level threats or complex cases

---

### **Question 5: একবার alert CLOSED হয়ে গেলে verdict change করতে পারবেন?**

A) Yes, anytime  
B) Yes, with approval  
C) No, cannot change closed alert  
D) Yes, up to 24 hours

**Answer:** C) No, cannot change closed alert - Must reopen as new incident, prevents metric manipulation

---

## সহজ ভাষায় সারসংক্ষেপ

**5 Verdict Types:**

- **TRUE_POSITIVE (TP):** Real threat confirmed
- **FALSE_POSITIVE (FP):** Alert wrong, no actual threat
- **BENIGN:** Activity happened but legitimate
- **SUSPICIOUS:** Uncertain, needs L2 investigation
- **ESCALATED:** High risk or complex, sent to L2/IR

**Key Distinctions:**

- FP ≠ BENIGN (activity occurrence matters)
- SUSPICIOUS ≠ FP (needs escalation, not close)
- ESCALATED ≠ Final verdict (L2 decides)
- TP needs confirmation (not guess)

**Decision Logic:**

1. Did activity happen? (YES/NO)
2. Is activity malicious? (YES/NO/UNCLEAR)
3. Is it authorized? (YES/NO/UNCLEAR)
4. Risk level? (HIGH → escalate, others → verdict)

**Documentation Must Include:**

- What you found
- Why this verdict
- What evidence
- What action taken
- Timestamp

**Remember:**

- Verdict assigned only ONCE (at close)
- Verdicts tracked for metrics/quality
- Cannot change after close
- When uncertain → SUSPICIOUS (escalate)
- Always explain your reasoning

---

## Resources for Learning

**Verdict definitions:**
- Your company alert playbooks
- Alert rule documentation
- Previous investigation examples
- L2 mentor feedback

**Quality tracking:**
- SOC dashboard metrics
- Manager performance reviews
- Industry benchmarks (SANS, CIS)

---

**Module 8 Complete! ✅**

এখন আপনি জানেন:
- ✅ 5 verdict types এবং তাদের সংজ্ঞা
- ✅ TRUE_POSITIVE: Confirmed threat
- ✅ FALSE_POSITIVE: Alert wrong
- ✅ BENIGN: Activity legitimate
- ✅ SUSPICIOUS: Uncertain, escalate
- ✅ ESCALATED: High risk/complex
- ✅ FP vs BENIGN পার্থক্য
- ✅ Verdict decision logic
- ✅ Documentation standards
- ✅ Quality metrics tracking
- ✅ Real-world verdict examples
- ✅ Common mistakes

Progress: **8 of 28 modules complete (29%)**

---

<!-- nav-footer -->
## 🧭 Navigation

| | |
|---|---|
| **Previous** | [⬅️ Module 07: Alert Triage Fundamentals](../module-07-alert-triage-fundamentals/index.md) |
| **Next** | [Module 09: Investigation Methodology ➡️](../module-09-investigation-methodology/index.md) |
| **🏠 Course Home** | [STUDY_NOTES.md](../../STUDY_NOTES.md) |
