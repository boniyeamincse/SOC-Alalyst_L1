# Module 9: SOC Investigation Methodology

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- Systematic investigation কি এবং কেন গুরুত্বপূর্ণ
- Investigation phases: Intake → Context → Analysis → Conclusion
- OSINT approach: Open Source Intelligence gathering
- Evidence collection: Where to look, what to gather
- Timeline construction: Event sequencing
- Correlation: Connecting related events
- Root cause analysis: Why did it happen?
- Investigation documentation best practices
- Real SOC investigation workflows
- Common investigation mistakes
- Hypothesis-driven investigation

---

## শুরুর আগে: একটি গল্প

নাজমা একজন experienced SOC L1 analyst। তার নতুন alert আসে: "Unusual database access".

দুটো approach:

**Approach 1: Unstructured (Wrong)**
```
09:00 - Alert see করলো
09:05 - DB log check করলো (nothing)
09:10 - Random user search করলো (no pattern)
09:20 - EDR check করলো (no malware)
09:35 - Confused conclusion: "Probably false positive"
Time: 35 minutes, Low confidence
```

**Approach 2: Structured (Right - নাজমা এর method)**
```
09:00 - Alert intake (30 sec)
09:01 - Context gathering (2 min)
        └─ User: Who? DBA or regular?
        └─ Database: Critical or test?
        └─ Time: Business hours or off?
09:03 - Timeline construction (3 min)
        └─ When exactly?
        └─ Before/after any events?
09:06 - Evidence correlation (5 min)
        └─ DB logs + app logs + network logs
        └─ Do they tell same story?
09:11 - Hypothesis testing (4 min)
        └─ Is it X? Check...
        └─ Is it Y? Check...
09:15 - Conclusion + documentation (2 min)
Time: 15 minutes, HIGH confidence
```

এই module এ systematic investigation শিখব।

---

## Investigation Methodology: Core Principles

### **4 Core Principles:**

```
1. SYSTEMATIC
   ├─ Structured approach
   ├─ Documented steps
   └─ Reproducible process

2. OBJECTIVE
   ├─ Based on evidence, not assumptions
   ├─ Data-driven conclusions
   └─ Avoid bias

3. THOROUGH (but time-bounded)
   ├─ Check all relevant sources
   ├─ Don't miss important evidence
   └─ But stop at 15-20 minutes (escalate if needed)

4. DOCUMENTED
   ├─ Write findings as you go
   ├─ Explain your logic
   └─ Create audit trail
```

---

## Investigation Phases

### **Phase 1: INTAKE & CONTEXT (2-3 minutes)**

```
Goal: Understand what we're investigating

Questions to answer:
┌─────────────────────────────────────────────────┐
│ WHO?                                            │
├─────────────────────────────────────────────────┤
│ ├─ User or account?                            │
│ ├─ Legitimate/known?                           │
│ ├─ History of similar activity?                │
│ └─ Current role/department?                    │
│                                                │
│ WHAT?                                          │
├─────────────────────────────────────────────────┤
│ ├─ What activity triggered alert?              │
│ ├─ Is activity expected?                       │
│ ├─ Baseline normal for this user?              │
│ └─ Severity signals?                           │
│                                                │
│ WHEN?                                          │
├─────────────────────────────────────────────────┤
│ ├─ Exact timestamp?                            │
│ ├─ Business hours or off-hours?                │
│ ├─ Day of week (weekday/weekend)?              │
│ └─ Any scheduled events that time?             │
│                                                │
│ WHERE?                                         │
├─────────────────────────────────────────────────┤
│ ├─ Source IP (internal/external)?              │
│ ├─ Target system (critical/test)?              │
│ ├─ Geographic location?                        │
│ └─ Network segment?                            │
│                                                │
│ WHY?                                           │
├─────────────────────────────────────────────────┤
│ ├─ Business reason for activity?               │
│ ├─ Expected behavior?                          │
│ ├─ Any approvals/tickets?                      │
│ └─ Known automation or process?                │
└─────────────────────────────────────────────────┘
```

### **Example - Phase 1:**

```
Alert: "Database privilege escalation"

Intake questions:
├─ WHO: User "data_analyst"
│  └─ Check: Known employee, data team
│
├─ WHAT: User added to DBA role
│  └─ Check: First time for this user
│
├─ WHEN: 09:30 IST, Monday morning
│  └─ Check: Business hours (expected)
│
├─ WHERE: Database server (production)
│  └─ Check: Critical system
│
└─ WHY: No obvious business event
   └─ Check: IT tickets, calendars

Initial assessment:
└─ Suspicious (unexpected elevation)
└─ But possibly business-related
└─ Continue investigation
```

---

### **Phase 2: EVIDENCE COLLECTION (3-5 minutes)**

```
Goal: Gather all relevant data sources

Where to look for evidence:

LOGS (Different layers):
├─ Source logs (where activity originated)
│  └─ Windows Event: User login, action
│  └─ Syslog: Unix authentication, commands
│
├─ Target logs (system affected)
│  └─ Application log: Database activity
│  └─ Access log: File system changes
│
├─ Network logs
│  └─ Firewall: Traffic allowed/blocked
│  └─ Proxy: Web traffic
│  └─ DNS: Domain queries
│
└─ Security logs
   └─ EDR: Endpoint behavior
   └─ Email: Email metadata
   └─ Authentication: AD changes

WHAT TO COLLECT:

For each evidence source, look for:
├─ Exact timestamp (for timeline)
├─ User/account information
├─ Action taken (what happened)
├─ Status (success/failure)
├─ Details (parameters, files, etc.)
└─ Any related events (before/after)

COLLECTION CHECKLIST:

For CURRENT alert:
- [ ] Alert details (properties we learned)
- [ ] Raw logs that triggered alert
- [ ] Timestamp verification

For CONTEXT:
- [ ] User history (same user, past events)
- [ ] System history (same system, past events)
- [ ] Related events (±10 minutes)

For THREAT INTELLIGENCE:
- [ ] Source IP reputation
- [ ] Domain/URL reputation
- [ ] File hash reputation

For BUSINESS CONTEXT:
- [ ] User calendar (travel, events)
- [ ] IT tickets (planned changes)
- [ ] HR records (employment status)
- [ ] Asset database (system info)
```

### **Example - Phase 2:**

```
Alert: "Database privilege escalation"

Collection:
├─ Alert details
│  └─ User: data_analyst
│  └─ Action: Added to DBA_ROLE
│  └─ Time: 09:30 IST
│  └─ Source: AD PowerShell script
│
├─ Source logs (AD logs)
│  └─ Event ID 4756: Security group member added
│  └─ Change made by: admin account
│  └─ Timestamp: 09:30:15 IST
│
├─ User history
│  └─ data_analyst logins: Normal pattern
│  └─ No privilege escalation before
│  └─ No suspicious activity previous 30 days
│
├─ Related events (±10 min)
│  └─ 09:28: Email from data_analyst
│  │  └─ "Need DBA access for project"
│  └─ 09:29: Email from admin
│  │  └─ "Approved, adding to group"
│
├─ Threat intelligence
│  └─ No malware
│  └─ No suspicious access from new IP
│  └─ User device: Clean (EDR check)
│
└─ Business context
   └─ HR: data_analyst (active)
   └─ Manager: Approves access request
   └─ IT ticket: #12345 (pending DBA access)
   └─ Project: Database migration (known project)

Evidence gathered: COMPLETE
Status: No threat indicators yet
Continue to next phase
```

---

### **Phase 3: TIMELINE CONSTRUCTION (2-3 minutes)**

```
Goal: Create chronological sequence of events

Why timeline matters:
├─ Shows sequence of events
├─ Reveals attack progression
├─ Helps identify root cause
├─ Supports correlation
└─ Essential for incident reconstruction

Timeline construction steps:

1. EXTRACT KEY EVENTS
   └─ List all events with timestamps
   └─ Include: User action, system response, related events

2. SORT CHRONOLOGICALLY
   └─ Earliest first
   └─ Second precision important

3. ADD CONTEXT
   └─ What was normal at each step?
   └─ Any warnings/precursors?

4. IDENTIFY PATTERNS
   └─ Sequence logical?
   └─ Any gaps?
   └─ Any suspicious jumps?

5. MARK ANOMALIES
   └─ Unexpected timing?
   └─ Unusual sequence?
   └─ Indicators of compromise?

TIMELINE FORMAT:

Time       │ Event                      │ Source    │ Status
-----------|----------------------------|-----------|----------
09:28:00   │ Email: DBA access request  │ Email log │ Received
09:29:15   │ Email: Access approved     │ Email log │ Sent
09:30:15   │ User added to DBA role     │ AD log    │ Success
09:30:45   │ User login to database     │ DB log    │ Success
09:31:00   │ Database config accessed   │ DB log    │ Success
09:45:00   │ Normal data queries        │ DB log    │ Success

Analysis:
├─ Sequence logical? YES
├─ Business-driven? YES (email → approval → action)
├─ Any red flags? NO
└─ Looks legitimate
```

### **Example - Phase 3:**

```
Alert: "Database privilege escalation"

Timeline:

09:28:00 | Email request: "Need DBA access"
         └─ Action: Email sent by data_analyst
         └─ To: admin account
         └─ Purpose: Database migration project

09:29:15 | Email approval: "Access granted"
         └─ Action: Email sent by admin
         └─ To: data_analyst, manager
         └─ Approval: Yes, DBA role access

09:30:15 | AD security group change
         └─ Action: Added data_analyst to DBA_ROLE
         └─ By: admin account
         └─ Method: PowerShell script (standard)

09:30:45 | Database login successful
         └─ User: data_analyst (now DBA)
         └─ Action: Connected with new permissions

09:31:00 | Database access pattern
         └─ Activity: Viewing database schemas
         └─ Files: Consistent with DBA role
         └─ No data extraction

Timeline assessment:
├─ Sequence: Email request → approval → implementation
├─ Timing: Logical flow, no gaps
├─ Approval: Manager aware, in email chain
├─ Activity: Consistent with stated purpose
└─ CONCLUSION: Legitimate workflow
```

---

### **Phase 4: CORRELATION & ANALYSIS (3-5 minutes)**

```
Goal: Connect evidence, test hypotheses

HYPOTHESIS-DRIVEN INVESTIGATION:

Step 1: Form initial hypothesis
├─ Based on alert + context
├─ Example: "Legitimate privilege elevation"

Step 2: Gather supporting evidence
├─ Does evidence support hypothesis?
├─ Email approval? Check
├─ User history? Check
├─ Business context? Check

Step 3: Look for contradicting evidence
├─ Any signs this is unauthorized?
├─ Any compromise indicators?
├─ Any data theft signals?

Step 4: Refine or reject hypothesis
├─ If contradictions: Form new hypothesis
├─ If supports: Confidence increases
├─ If uncertain: Mark as SUSPICIOUS (escalate)

Step 5: Draw conclusion
├─ Hypothesis confirmed? TP
├─ Hypothesis rejected? FP
├─ Uncertain? SUSPICIOUS
└─ Complex? ESCALATED
```

### **Correlation Techniques:**

```
CROSS-SOURCE CORRELATION:

Same event, multiple sources:
├─ Event: Login at 14:30:00 IST
├─ Windows log: 14:30:05 (±5 sec OK)
├─ SIEM: 14:30:02 (±5 sec OK)
├─ Proxy log: 14:29:58 (clock skew noticed)
└─ Conclusion: Same event, clock differences acceptable

ACTIVITY CORRELATION:

Related events suggesting pattern:
├─ Event 1: Failed login attempt
├─ Event 2: Password reset 5 min later
├─ Event 3: Successful login
├─ Event 4: File access unusual files
├─ Pattern: Account compromise attempt?
└─ Confidence: HIGH

NEGATIVE CORRELATION:

Absence of expected evidence:
├─ If malware: EDR should detect
├─ But EDR: Clean
├─ Conclusion: No endpoint malware

TEMPORAL CORRELATION:

Events within tight window:
├─ Email arrival: 14:30
├─ User login: 14:31
├─ File access: 14:32
├─ Sequence: Logical? YES
└─ Pattern: Expected workflow
```

### **Example - Phase 4:**

```
Alert: "Database privilege escalation"

Analysis:

HYPOTHESIS 1: "Legitimate business elevation"
Evidence for:
├─ Email request from user ✓
├─ Email approval from admin ✓
├─ User history: No prior issues ✓
├─ Business context: Known project ✓
├─ Activity: Consistent with DBA role ✓
├─ No malware signals ✓
├─ No data theft signals ✓

Evidence against:
└─ None found ✗

Confidence: VERY HIGH

HYPOTHESIS 2: "Account compromise with cover-up"
Evidence for:
└─ Privilege escalation (potential sign) ?

Evidence against:
├─ Emails from account (not suspicious) ✓
├─ Admin approved (trusted person) ✓
├─ No malware on device ✓
├─ No external logins ✓
├─ Normal user behavior ✓

Confidence: VERY LOW

CORRELATION SUMMARY:
├─ Email chain: Authentic
├─ Approval: Proper authorization
├─ Timing: Logical sequence
├─ Activity: Matches business purpose
└─ Indicators: No threat signals

CONCLUSION: Legitimate activity
```

---

## Root Cause Analysis

### What is Root Cause?

```
SYMPTOMS vs ROOT CAUSE:

Symptom: Alert triggered
└─ What we observed

Root Cause: Why did it happen?
└─ Underlying reason

Example:
Symptom: "Failed login 50 times"
Root Causes could be:
├─ User typo'd password
├─ Backup script not updated after password reset
├─ Automated tool misconfigured
├─ User on travel, timezone confusion
├─ Actual brute force attack
└─ Need to identify which one

Why root cause matters:
├─ Determines verdict
├─ Determines action
├─ Prevents future incidents
└─ Improves processes
```

### RCA Process:

```
STEP 1: Identify problem
└─ "What happened?" (event description)

STEP 2: Gather facts
└─ Timeline, context, evidence

STEP 3: Ask "Why?"
└─ Why did this happen?
└─ Multiple levels:
    Level 1: Automation tool failed
    Level 2: Credentials not updated
    Level 3: No process to update tool creds
    Level 4: Tool configuration not automated
    Level 5: No automation governance

STEP 4: Determine root cause
└─ Level 1-2: Technical issue
└─ Level 3-5: Process issue

STEP 5: Recommend fix
├─ Technical: Update credentials
├─ Process: Implement credential change workflow
├─ Preventive: Automate credential rotation
└─ Governance: Add to change management
```

### Example RCA:

```
Problem: "Failed login attempts + successful login"

Level 1 Why: Why failed attempts?
└─ Answer: Wrong password tried

Level 2 Why: Why wrong password?
└─ Answer: User entered old password cached on device

Level 3 Why: Why cached old password?
└─ Answer: User recently reset password at AD
         but browser had cached login

Level 4 Why: Why no refresh?
└─ Answer: Device not rebooted after password change

Level 5 Why: Why not rebooted?
└─ Answer: User didn't know to reboot
         No notification sent about password change

ROOT CAUSE: User awareness + process gap

FIX:
├─ Immediate: Educate user about cache clearing
├─ Short-term: Add password change warning
├─ Long-term: Automate credential sync
└─ Process: Implement change notification workflow
```

---

## Investigation Documentation

### What to Document:

```
As you investigate, write down:

STEP 1: Initial Assessment
├─ Alert received: timestamp
├─ Initial impression: What does it look like?
├─ Initial hypothesis: What's my best guess?
└─ Severity: How urgent?

STEP 2: Context Gathered
├─ User information: Who/department/role
├─ System information: Critical/test/data
├─ Business context: Any known events
└─ Relevant history: Similar alerts before?

STEP 3: Evidence Collected
├─ Data sources checked: SIEM, EDR, AD, etc.
├─ What you found: Details
├─ What you didn't find: Absence of expected evidence
└─ Any anomalies: What stood out?

STEP 4: Timeline
├─ Events in sequence (timestamp)
├─ Any gaps or jumps?
├─ Logical progression?

STEP 5: Analysis
├─ Hypothesis tested
├─ Evidence for/against
├─ Confidence level
├─ Any uncertainties?

STEP 6: Conclusion
├─ Verdict: TP/FP/Benign/Suspicious
├─ Reasoning: Why this verdict?
├─ Actions taken/recommended
└─ Escalation if needed: To whom/why?

TIME SPENT: Start → End time
```

### Documentation Template:

```
┌─────────────────────────────────────────────────────────┐
│ INVESTIGATION REPORT                                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Alert ID: ALERT-0001                                   │
│ Alert Name: Suspicious Database Access                 │
│ Investigator: L1_analyst_1                             │
│ Date/Time: 2024-06-22 14:30 IST                       │
│                                                         │
├─ INITIAL ASSESSMENT                                   │
│ Impression: Unusual activity by database admin        │
│ Hypothesis: Possible compromise or maintenance        │
│ Severity: HIGH (database access)                      │
│                                                         │
├─ CONTEXT GATHERING                                    │
│ User: db_admin (senior DBA, 5 years tenure)          │
│ System: Production database (CRITICAL)                │
│ Business: No scheduled maintenance announced          │
│ History: 3 similar alerts in past month (all FP)      │
│                                                         │
├─ EVIDENCE COLLECTION                                  │
│ ✓ Database logs:                                      │
│   └─ Admin login: 14:30:15 IST                       │
│   └─ Activity: Config table access                    │
│   └─ Duration: 2 minutes                              │
│   └─ Action: Read-only query                          │
│                                                         │
│ ✓ Network logs:                                       │
│   └─ Source: Internal IP (office network)             │
│   └─ Destination: DB server                           │
│   └─ Protocol: Standard DB connection                 │
│   └─ Data volume: Normal                              │
│                                                         │
│ ✓ EDR logs:                                           │
│   └─ Device: db_admin's workstation                   │
│   └─ Process: SSMS (SQL Server Management Studio)     │
│   └─ Behavior: Normal admin tool                      │
│   └─ Malware scan: Clean                              │
│                                                         │
│ ✓ Business context:                                   │
│   └─ IT ticket: #54321 (performance investigation)    │
│   └─ Approval: Manager + DBA lead                     │
│   └─ Time window: Approved 14:00-15:00 IST            │
│                                                         │
├─ TIMELINE                                             │
│ 14:00 │ IT ticket created: "Investigate DB slowness" │
│ 14:05 │ DBA notified of investigation                │
│ 14:25 │ DBA approval received                        │
│ 14:30 │ DBA logged into database                     │
│ 14:30 │ Alert triggered                              │
│ 14:31 │ Config tables queried                        │
│ 14:32 │ Session closed (normal)                      │
│                                                         │
├─ ANALYSIS                                             │
│ Hypothesis: Legitimate performance investigation      │
│                                                         │
│ Supporting evidence:                                  │
│ ✓ IT ticket documents business reason                │
│ ✓ Activity matches typical troubleshooting            │
│ ✓ Admin user (trusted)                                │
│ ✓ Activity within approved time window                │
│ ✓ No data extraction or malicious actions             │
│ ✓ No malware indicators                               │
│                                                         │
│ Contradicting evidence:                               │
│ ✗ None identified                                     │
│                                                         │
│ Confidence: 95%                                       │
│                                                         │
├─ CONCLUSION                                           │
│ Verdict: BENIGN (activity is legitimate)              │
│                                                         │
│ Reasoning:                                            │
│ Alert correctly identified DBA database access.       │
│ However, access is authorized and business-driven.    │
│ Activity within normal admin scope.                   │
│ No threat indicators present.                         │
│                                                         │
├─ ACTIONS TAKEN                                        │
│ ✓ Alert closed as BENIGN                             │
│ ✓ Manager notified (for awareness)                    │
│ ✓ Notes added to db_admin user profile                │
│ ✗ No escalation needed                               │
│                                                         │
├─ RECOMMENDATIONS                                      │
│ ├─ Track similar admin access patterns                │
│ ├─ Consider alert rule tuning (reduce FP rate)        │
│ └─ Monitor performance investigation resolution       │
│                                                         │
└─ INVESTIGATION TIME: 15 minutes (14:30-14:45)        │
```

---

## Real-World Investigation Examples

### **Example 1: Malware → Deep Investigation → Escalate**

```
ALERT: "Ransomware signature detected"
FILE: document.exe
DEVICE: finance-laptop-001

PHASE 1: INTAKE (2 min)
├─ User: finance_analyst (legitimate, not tech-savvy)
├─ Device: Finance laptop (HIGH VALUE)
├─ File: .exe (suspicious, not normal for finance)
└─ Initial: SUSPICIOUS, needs deep dive

PHASE 2: EVIDENCE (4 min)
├─ File source: Email attachment
│  └─ Email: "Invoice from vendor"
│  └─ Sender: spoofed@companyx.com (FAKE)
│
├─ Hash lookup:
│  └─ VirusTotal: 52/71 vendors flag as Emotet
│
├─ EDR behavior:
│  └─ File: Attempting file encryption
│  └─ Network: Connecting to 192.0.2.100 (C2 IP)
│  └─ Actions: Credential dumping attempts
│
└─ Network logs:
   └─ Outbound to known C2: CONFIRMED

PHASE 3: TIMELINE (2 min)
10:15 │ Email received (phishing)
10:16 │ User clicked attachment
10:17 │ File executed
10:18 │ EDR alerts: Suspicious behavior
10:19 │ C2 connection attempt
10:20 │ File encryption starts

PHASE 4: ANALYSIS (3 min)
Hypothesis: Confirmed malware infection
Evidence for:
├─ Hash matches known ransomware ✓
├─ Behavior matches Emotet ✓
├─ C2 communication confirmed ✓
├─ Encryption in progress ✓
└─ Multiple indicators align ✓

Confidence: 99%

CONCLUSION:
Verdict: TRUE_POSITIVE
Action: ESCALATED to Incident Response

ESCALATION:
├─ Device isolated immediately
├─ IR team activated
├─ Finance manager notified
├─ Database backup status checked
└─ Forensics initiated

Time: 12 minutes (under SLA)
```

### **Example 2: False Positive → Pattern Recognition → Close**

```
ALERT: "Multiple failed login attempts"
USER: backup_service
COUNT: 100 failed logins

PHASE 1: INTAKE (1 min)
├─ User: Service account (automated, not human)
├─ Pattern: 100 failures (very high)
├─ Time: 03:00 AM (nightly backup window)
└─ Initial: Might be FP (automation common)

PHASE 2: EVIDENCE (2 min)
├─ SIEM history:
│  └─ Same pattern every single night
│  └─ For past 3 months
│  └─ VERY predictable
│
├─ User details:
│  └─ Created 2022 (backup automation)
│  └─ Never human usage
│  └─ Expected pattern known
│
└─ AD history:
   └─ Password unchanged (but old)
   └─ Account active
   └─ No lockouts

PHASE 3: TIMELINE (1 min)
03:00-03:05 │ 100 failed login attempts
03:05       │ Backup completes successfully (somehow)
03:05       │ No subsequent access

Clear pattern: Automation failure → success pattern

PHASE 4: ANALYSIS (2 min)
Hypothesis: Known false positive from backup automation

Supporting evidence:
├─ Exact same time every night ✓
├─ Exact same count every night ✓
├─ Backup succeeds despite failures ✓
├─ 3-month history confirms ✓
├─ No actual compromise ✓
└─ Non-human account ✓

Confidence: 99%

CONCLUSION:
Verdict: FALSE_POSITIVE
Reason: Backup script using old password credentials

ACTIONS:
├─ Close alert (pattern known)
├─ Document as recurring FP
├─ Note: Update backup script credentials
└─ Recommend: Suppress similar alerts

Time: 6 minutes (EFFICIENT)
```

### **Example 3: Suspicious → Escalate for Context → L2 Contacts User**

```
ALERT: "Large file transfer to external IP"
SIZE: 2 GB
USER: analyst@company.com
DESTINATION: 203.0.113.50

PHASE 1: INTAKE (2 min)
├─ User: Data analyst (legitimate)
├─ Size: 2 GB (large but possible)
├─ Destination: External (concerning)
├─ Time: 22:30 (after hours, odd)
└─ Initial: SUSPICIOUS (needs clarification)

PHASE 2: EVIDENCE (3 min)
├─ File details:
│  └─ Type: CSV (data file, not executable)
│  └─ Source: User's home directory
│
├─ Network logs:
│  └─ Destination: 203.0.113.50
│  └─ IP reputation: Not obviously malicious
│  └─ Port: 22 (SSH, normal)
│
├─ Endpoint:
│  └─ EDR: No malware signals
│  └─ Process: SCP command (legitimate tool)
│
└─ Business context:
   └─ No IT ticket
   └─ No email notification
   └─ No calendar event

PHASE 3: TIMELINE (1 min)
22:25 │ User VPN login
22:30 │ File transfer started
22:35 │ File transfer completed

PHASE 4: ANALYSIS (2 min)
Hypothesis: Could be legitimate collaboration OR unauthorized data transfer

Evidence for legitimate:
├─ User: Legitimate employee
├─ File: Non-executable data
├─ Tool: Standard SCP (legitimate)
├─ Device: No malware
└─ IP: Not known malicious

Evidence for unauthorized:
├─ After hours: Unusual timing
├─ No documentation: No ticket/email
├─ External: Outside organization
├─ 2 GB: Large transfer

Assessment: INSUFFICIENT DATA

CONCLUSION:
Verdict: SUSPICIOUS
Reason: Could be legitimate or unauthorized

ACTION: ESCALATE to L2

ESCALATION NOTE:
├─ Need user confirmation of business reason
├─ Need destination IP context
├─ Need data classification check
└─ Recommend: L2 contacts user/manager

Time: 8 minutes (defer to L2)

L2 FOLLOWUP (Next step):
├─ L2 calls user: "Can you explain file transfer?"
├─ User: "Oh, I'm collaborating with external vendor"
│         "They requested data files"
├─ L2 verifies: Vendor legitimate, data not sensitive
├─ Final verdict: BENIGN (approved collaboration)
└─ Action: Document vendor IP, whitelist
```

---

## Common Investigation Mistakes

### ❌ **Mistake 1: Confirmation bias**

**সমস্যা:**
```
Alert: "Unusual access"
Initial thought: "This looks malicious"
Investigation: Only look for evidence supporting threat
Ignore: Evidence suggesting legitimate use
Result: Wrong verdict
```

**সমাধান:**
```
Always actively look for CONTRADICTING evidence
Ask: "What would prove this is legitimate?"
Check: Can you find that evidence?
If yes → Verdict changes
```

---

### ❌ **Mistake 2: Incomplete timeline**

**সমস্যা:**
```
Alert time: 14:30
Only check logs around 14:30
Miss: What happened 14:15-14:25 (buildup)
Result: Incomplete picture
```

**সমাধান:**
```
Always check ±10 minutes around alert
Look for precursor events
Build complete sequence
```

---

### ❌ **Mistake 3: Not correlating sources**

**সমস্যা:**
```
Check SIEM logs: Suspicious
But don't check: EDR, firewall, network
Result: Miss context from other sources
```

**সমাধান:**
```
Always check multiple sources
SIEM + EDR + Network + Business context
Cross-validate findings
```

---

### ❌ **Mistake 4: Assuming context**

**সমস্যা:**
```
Alert: "Failed login from Singapore"
Assumption: "Must be compromise"
Don't check: User travel status
Result: False positive from business trip
```

**সমাধান:**
```
Never assume
Always verify: Calendar, HR, IT tickets
Get facts, not assumptions
```

---

### ❌ **Mistake 5: Over-investigating**

**সমস্যา:**
```
Investigation time: 45 minutes
Still unclear, kept investigating
Result: Wasted time, queue backlog
```

**সমাধান:**
```
15-20 minutes: Deep investigation
If unclear: ESCALATE to L2 (their job)
Don't force conclusion
```

---

## Practical Investigation Checklist

### **Pre-Investigation Setup (1 min)**

- [ ] Open alert details
- [ ] Note alert properties (who, what, when, where)
- [ ] Acknowledge alert (claim it)
- [ ] Start timer (budget: 15-20 min)

### **Phase 1: Context (2-3 min)**

- [ ] WHO: Is user legitimate? Known? History?
- [ ] WHAT: Is activity expected? Baseline ok?
- [ ] WHEN: Business hours? Day of week? Any events?
- [ ] WHERE: Internal/external? Critical system?
- [ ] WHY: Business reason? Any approvals?

### **Phase 2: Evidence (3-5 min)**

- [ ] SIEM logs: Found raw events? Verified?
- [ ] EDR data: If applicable, checked device?
- [ ] Network logs: Firewall/proxy activity?
- [ ] User history: Any previous incidents?
- [ ] Business context: Tickets/calendar/HR?
- [ ] Threat intel: IP/domain/hash reputation?

### **Phase 3: Timeline (2-3 min)**

- [ ] Sorted events chronologically
- [ ] Added timestamps to each event
- [ ] Identified gaps or anomalies
- [ ] Timeline logical and consistent?

### **Phase 4: Analysis (3-5 min)**

- [ ] Formed initial hypothesis
- [ ] Looked for supporting evidence
- [ ] Looked for contradicting evidence
- [ ] Tested alternative hypotheses
- [ ] Reached confidence level?

### **Phase 5: Documentation (2 min)**

- [ ] Wrote investigation summary
- [ ] Recorded verdict reasoning
- [ ] Noted actions taken
- [ ] Escalation if needed

### **Phase 6: Decision**

- [ ] Verdict: TP/FP/BENIGN/SUSPICIOUS/ESCALATED?
- [ ] Close or escalate?
- [ ] Document final decision
- [ ] Total time: ___ minutes

---

## Mini Quiz: Investigation Methodology

### **Question 1: Investigation phases এর সঠিক order কোনটি?**

A) Analysis → Context → Evidence → Timeline  
B) Context → Evidence → Timeline → Analysis  
C) Evidence → Timeline → Context → Analysis  
D) Timeline → Analysis → Evidence → Context

**Answer:** B) Context → Evidence → Timeline → Analysis - এই order সবচেয়ে logical

---

### **Question 2: Confirmation bias এর বিরুদ্ধে কি করবেন?**

A) একটাই hypothesis গ্রহণ করুন  
B) শুধু supporting evidence দেখুন  
C) Active করে contradicting evidence খুঁজুন  
D) একবার decision নিলে পরিবর্তন করবেন না

**Answer:** C) Active করে contradicting evidence খুঁজুন - এটা bias এর বিরুদ্ধে সবচেয়ে ভাল defense

---

### **Question 3: Investigation এ কত সময় maximum লাগবে?**

A) 5 minutes  
B) 10 minutes  
C) 15-20 minutes  
D) 1 hour if needed

**Answer:** C) 15-20 minutes - এর বেশি হলে escalate করুন L2 কে

---

### **Question 4: Timeline এ কত সময় আগে-পিছে check করবেন?**

A) Same minute only  
B) ±5 minutes  
C) ±10 minutes  
D) ±1 hour

**Answer:** C) ±10 minutes - Precursor events এবং আগে-পিছে context ধরতে

---

### **Question 5: Root cause analysis এ কতবার "Why" ask করবেন?**

A) 1 time  
B) 2-3 times  
C) 5 times (5 Whys method)  
D) যতক্ষণ না fundamental cause পাওয়া যায়

**Answer:** D) যতক্ষণ না fundamental cause পাওয়া যায় - তবে 5 Whys একটা ভাল framework

---

## সহজ ভাষায় সারসংক্ষেপ

**Investigation = Systematic evidence gathering & analysis**

**4 Main Phases:**
1. **Context:** WHO, WHAT, WHEN, WHERE, WHY (2-3 min)
2. **Evidence:** Gather from all sources (3-5 min)
3. **Timeline:** Sequence events chronologically (2-3 min)
4. **Analysis:** Test hypotheses, reach conclusion (3-5 min)

**Key Principles:**
- Systematic (structured approach)
- Objective (evidence-based)
- Thorough but time-bounded (15-20 min max)
- Documented (explain your logic)

**Investigation Tools:**
- Timeline construction
- Hypothesis testing
- Evidence correlation
- Root cause analysis
- Cross-source validation

**Common Mistakes:**
- Confirmation bias (only look for supporting evidence)
- Incomplete timeline (miss context)
- Not correlating sources (miss full picture)
- Assuming context (not verifying)
- Over-investigating (waste time)

**Remember:**
- ±10 minutes around alert time
- Multiple data sources
- Active look for contradicting evidence
- If uncertain → SUSPICIOUS (escalate)
- Document everything

---

## Resources for Learning

**Investigation techniques:**
- SANS Incident Handling
- NIST cybersecurity guide
- Your company playbooks

**Tools & sources:**
- SIEM query training
- EDR documentation
- Threat intel platforms

---

**Module 9 Complete! ✅**

এখন আপনি জানেন:
- ✅ Systematic investigation methodology
- ✅ 5W1H framework (Who, What, When, Where, Why, How)
- ✅ 4-phase investigation process
- ✅ Evidence collection from multiple sources
- ✅ Timeline construction & importance
- ✅ Hypothesis-driven investigation
- ✅ Correlation across evidence sources
- ✅ Root cause analysis (5 Whys method)
- ✅ Investigation documentation standards
- ✅ Real-world investigation examples
- ✅ Common investigation mistakes
- ✅ Practical investigation checklist

Progress: **9 of 28 modules complete (32%)**

---

<!-- nav-footer -->
## 🧭 Navigation

| | |
|---|---|
| **Previous** | [⬅️ Module 08: Alert Verdicts](../module-08-alert-verdicts/index.md) |
| **Next** | [Module 10: Identity Inventory ➡️](../module-10-identity-inventory/index.md) |
| **🏠 Course Home** | [STUDY_NOTES.md](../../STUDY_NOTES.md) |
