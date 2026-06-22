# Module 7: SOC L1 Alert Triage Fundamentals

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- Triage কি এবং কেন critical skill
- Systematic triage process
- Alert intake - initial information gathering
- Context enrichment - background research
- Risk assessment - how serious?
- Decision tree - close vs escalate
- Common triage patterns
- False positive identification
- Escalation criteria
- Triage best practices
- Real-world triage workflow

---

## শুরুর আগে: একটি গল্প

সালমান একজন নতুন SOC L1 analyst (1 week এ)। তার first CRITICAL alert আসে:

```
Alert: "Unauthorized database access detected"
Severity: CRITICAL
User: database_admin
```

সালমান nervous ছিল। অবিলম্বে escalate করেছে L2 কে।

L2 দ্রুত investigate করে দেখলো - এটা নিয়মিত backup process ছিল, false alarm।

একসপ্তাহ পর, একই alert আসে। এবার সালমান:

1. Alert click করলো
2. পূর্ববর্তী alerts history দেখলো - 10টি same alert এ
3. সব false positive were
4. Context দেখলো - backup schedule matching
5. দ্রুত close করলো: "FP - backup process"

**এটাই triage সিখা।** Systematic approach দিয়ে দ্রুত decision নেওয়া।

---

## Triage কি?

### Definition:

**Triage = Rapid assessment কতটা serious problem এবং কি action দরকার।**

Term medical field থেকে - emergency room এ patients কে urgent/normal/minor এ sort করা।

### SOC এ Triage:

```
Emergency Alert Queue
        │
        ├─ Patient A: Critical injury → Surgery now
        ├─ Patient B: Medium injury → Doctor soon
        ├─ Patient C: Minor injury → Band-aid OK
        └─ Patient D: Paperwork → Clerk handle
        
SOC Alert Queue
        │
        ├─ Alert A: Active malware → Incident response now
        ├─ Alert B: Suspicious activity → Investigation soon
        ├─ Alert C: Known false positive → Close as pattern
        └─ Alert D: Informational → Archive
```

### Triage Goals:

```
1. SPEED ⚡
   ├─ Decision within 5-15 minutes
   ├─ Not thorough analysis (that's investigation)
   └─ Rapid assessment only

2. ACCURACY ✓
   ├─ Right decision most times
   ├─ Close obvious false positives
   └─ Don't miss actual threats

3. EFFICIENCY 📊
   ├─ Process high alert volume
   ├─ Escalate right cases
   └─ Reduce L2 noise
```

---

## Triage Process: 5-Step Framework

### **Step 1: ALERT INTAKE (30 seconds)**

```
Alert arrives on dashboard

IMMEDIATELY:
├─ Click alert
├─ Read alert name
├─ Note severity + timestamp
├─ Acknowledge receipt (claim alert)
└─ Start timer
```

### **Questions to ask:**
```
✓ What happened? (Alert name)
✓ How serious? (Severity level)
✓ When? (Timestamp - recent or old?)
✓ Did I see similar before?
```

### **Example:**
```
Alert: "Brute Force Attack on SMB"
Severity: HIGH
Timestamp: 2024-06-21 14:30:45 IST
Thought: "Yes, seen this many times"
Action: Continue to Step 2
```

---

### **Step 2: QUICK CONTEXT (2-3 minutes)**

```
Goal: Gather essential context quickly

Key questions to answer:

1. WHO?
   ├─ User legitimate?
   ├─ Known user or suspicious?
   └─ First time or repeat offender?

2. WHERE?
   ├─ Internal or external source?
   ├─ Known location or new?
   └─ Business justified?

3. WHAT SYSTEM?
   ├─ Critical or non-critical?
   ├─ Production or test?
   └─ Sensitive data or not?

4. WHAT HAPPENED?
   ├─ Normal pattern or new?
   ├─ Escalating or declining?
   └─ Related to previous events?
```

### **Quick Lookup Tools:**

```
Use within 1-2 minutes:

├─ Previous alerts same user/IP
│  └─ Query: "user:john.doe last 30 days"
│
├─ User identity verification
│  └─ Look up: HR system, AD info
│
├─ IP reputation
│  └─ Query: TI platform (VirusTotal, AbuseIPDB)
│
├─ Business calendar
│  └─ Check: Any maintenance? Travel approval?
│
└─ Alert rule documentation
   └─ Understand: Why this rule triggers?
```

### **Example Triage Context:**
```
Alert: "Brute Force Attack on SMB"

Context gathering:
├─ User: john.doe (known employee)
│  └─ Search SIEM: 150 other events, normal pattern
│
├─ Source IP: 192.168.1.50
│  └─ Internal network (expected)
│
├─ Time: 14:30 (business hours)
│  └─ Normal time for activity
│
├─ System: File server
│  └─ Critical importance
│
└─ Pattern: Failed password attempts x50
   └─ FIRST TIME for john.doe (suspicious!)

ASSESSMENT: Needs investigation (not obvious FP)
```

---

### **Step 3: RISK ASSESSMENT (2-3 minutes)**

```
Based on context, assess actual risk:

Risk = (Threat_likelihood × Business_impact × Recoverability)

Build a quick assessment:

Threat Likelihood:
├─ HIGH: Known attack pattern, fresh indicators
├─ MEDIUM: Suspicious but could be benign
└─ LOW: Very likely false positive or benign

Business Impact:
├─ HIGH: Critical system, sensitive data
├─ MEDIUM: Important system, normal data
└─ LOW: Test system, non-sensitive

Recoverability:
├─ LOW: Easy to undo/recover from
├─ MEDIUM: Some effort needed
└─ HIGH: Difficult to recover

Final Risk Score:
HIGH threat + HIGH impact + HIGH recovery = CRITICAL risk
MEDIUM threat + MEDIUM impact = MEDIUM risk
LOW threat + ANY = LOW risk
```

### **Example Risk Assessment:**
```
Alert: "Brute Force Attack on SMB"

Threat Likelihood Assessment:
├─ Pattern: 50 failed login = classic brute force ✓
├─ But user: john.doe (legitimate) ❌
├─ Hypothesis: User password reset? Cached password issue?
└─ Likelihood: MEDIUM (could be technical issue)

Business Impact Assessment:
├─ System: File server (CRITICAL)
├─ Data: Employee files (IMPORTANT)
└─ Impact: HIGH

Recoverability Assessment:
├─ If compromised: Password reset + audit logs
├─ Cost: Medium effort
└─ Recoverability: MEDIUM

RISK SCORE:
├─ Threat: MEDIUM
├─ Impact: HIGH
├─ Recovery: MEDIUM
└─ Final: MEDIUM-HIGH RISK → Investigate

DECISION: Cannot close yet, need investigation
```

---

### **Step 4: INITIAL DECISION (1-2 minutes)**

```
Decision tree:

START
  │
  ├─ Obviously FALSE POSITIVE? (Yes)
  │  └─ Close alert
  │     └─ Document reason
  │
  ├─ Needs investigation? (Yes)
  │  └─ Continue to Step 5
  │
  ├─ Escalate immediately? (High risk)
  │  └─ Escalate to L2 with context
  │
  └─ Need more data? (Unclear)
     └─ Make note, continue investigation

Decision categories:

CLOSE (Low risk, high confidence FP):
├─ Reason clear
├─ Pattern known
├─ No action needed
└─ Example: "Known maintenance activity"

INVESTIGATE (Medium risk, uncertain):
├─ Need more details
├─ Context gathering incomplete
├─ Escalate if findings suspicious
└─ Example: "Verify user, check files accessed"

ESCALATE (High risk, needs expertise):
├─ Potential confirmed threat
├─ Incident response needed
├─ Beyond L1 capability
└─ Example: "Active malware detected"
```

### **Example Decision:**
```
Based on Risk Assessment:

Alert: "Brute Force Attack on SMB"
Risk Score: MEDIUM-HIGH

Decision Point:
├─ Close? NO - High risk
├─ Investigate? YES - Need more context
└─ Escalate? MAYBE - Depends on next step

ACTION: Proceed to Step 5 (Investigation)
```

---

### **Step 5: DEEP INVESTIGATION (5-10 minutes max)**

```
Go deeper, but still QUICK

Investigation goals:
├─ Determine if TRUE POSITIVE
├─ Determine if FALSE POSITIVE
├─ Gather evidence for decision
└─ DON'T spend >10 minutes (escalate instead)

Key investigation steps:

1. Verify alert accuracy
   ├─ Are the fields correct?
   ├─ Do raw logs confirm?
   └─ Any parsing errors?

2. Understand user context
   ├─ Is user authenticated in AD?
   ├─ Any recent password changes?
   ├─ Any HR events (travel, leave)?
   └─ Any account modifications?

3. Analyze activity pattern
   ├─ Are failed attempts from single IP?
   ├─ Or distributed (botnet)?
   ├─ Any successful login after failures?
   └─ Any file access or privilege change?

4. Check system state
   ├─ Is system compromised? (Signs?)
   ├─ Any unusual processes?
   ├─ Any suspicious files?
   └─ Any network connections?

5. Cross-reference intelligence
   ├─ Is source IP known malicious?
   ├─ Is pattern matching known attack?
   ├─ Any threat intel hits?
   └─ Any similar incidents this week?
```

### **Example Investigation:**
```
Alert: "Brute Force Attack on SMB"

Deep investigation:

1. Raw log verification
   ├─ Check actual Windows Event logs (Event ID 4625)
   └─ Confirm: 50 failures, same user, same IP

2. User context
   ├─ Check AD: john.doe account active ✓
   ├─ Check: No password reset today ✗
   ├─ Check HR system: john.doe = Present (no travel)
   ├─ Check: No recent account changes
   └─ FINDING: Normal user, no recent changes

3. Activity pattern
   ├─ Failed attempts: All from 192.168.1.50 ✓
   ├─ Distributed or single? Single IP
   ├─ Successful login? 
   │  └─ YES! One success at 14:48
   │  └─ But from SAME IP
   │  └─ Username: john.doe (correct)
   │  └─ This is suspicious! Account compromised?
   └─ File access after? Checking...

4. System state
   ├─ EDR on john's device?
   │  └─ YES - Checking endpoint behavior
   │  └─ No malware detected
   │  └─ No suspicious processes
   └─ FINDING: No endpoint compromise signals

5. Intelligence check
   ├─ Source IP 192.168.1.50 reputation? INTERNAL
   │  └─ Device: meeting-room-laptop
   │  └─ No known issues
   └─ FINDING: Internal device, not malicious

INVESTIGATION RESULT:
└─ Success after failures + internal device + no EP compromise
   = Possible explanation: User entered wrong password 50 times,
     then got it right
   = Could also be: Cached password issue on meeting room laptop
   = Or: Automatic sync tool retrying old password

RISK ASSESSMENT UPDATE:
├─ Success after failures = concerning
├─ But internal device = less concerning
├─ No EP compromise = less concerning
└─ FINAL: MEDIUM risk (needs verification from user)

DECISION: Contact user (or escalate for contact)
```

---

## Common Triage Patterns

### **Pattern 1: False Positive - Known Benign**

```
Characteristics:
├─ Alert fires regularly (daily/hourly)
├─ Always same context
├─ Known legitimate reason
├─ No variation

Examples:
├─ Backup script authentication retries
├─ Monitoring tool health checks
├─ Scheduled maintenance activity
├─ Test alerts from security tools

Triage action:
├─ Recognize pattern immediately (< 1 min)
├─ Close with reason: "FP - Known [reason]"
├─ Update documentation if needed
└─ Note for rule tuning

Time to close: 1 minute
```

### **Pattern 2: Suspicious - Need Context**

```
Characteristics:
├─ Alert structure correct
├─ But context unclear
├─ Could be legitimate or attack
├─ Need user/system verification

Examples:
├─ User unusual location (business trip?)
├─ File access outside hours (admin?)
├─ Large data transfer (backup?)
├─ PowerShell script execution (automation?)

Triage action:
├─ Quick context check (AD, HR, ticket system)
├─ If explanation found: Close with note
├─ If no explanation: Escalate for verification
└─ Document findings

Time to close/escalate: 5-10 minutes
```

### **Pattern 3: Confirmed Threat - Escalate**

```
Characteristics:
├─ Multiple threat indicators
├─ No legitimate explanation
├─ Action already taken (malware, data theft)
├─ Incident-level severity

Examples:
├─ Malware signature confirmed + behavior
├─ Data transfer + C2 communication
├─ Privilege escalation + lateral movement
├─ Account compromise + credential dumping

Triage action:
├─ Immediately escalate to L2/IR
├─ Provide complete context
├─ Document all findings
├─ Follow incident response protocol

Time to escalate: 5 minutes (maximum)
```

### **Pattern 4: Trend/Bulk Alerts**

```
Characteristics:
├─ Same alert type x10+
├─ Similar characteristics
├─ Coordinated or natural?
├─ Possible campaign

Examples:
├─ 50 users get phishing email (campaign)
├─ 100 login failures from one IP (brute force)
├─ 20 hosts file access anomaly (system update)

Triage action:
├─ Investigate root cause (one underlying issue)
├─ If benign: Bulk close all with note
├─ If suspicious: Escalate as coordinated incident
├─ Recommend: Alert rule tuning

Time to assess: 5 minutes
Time to close/escalate: 10-15 minutes total
```

---

## Context Enrichment: Key Sources

### **Internal Sources:**

```
Active Directory (AD)
├─ User status (active/disabled/locked)
├─ Last password change
├─ Department, manager
├─ Group memberships
└─ Use for: User verification

HR System
├─ Employment status
├─ Travel approvals
├─ Leave requests
├─ Department
└─ Use for: Location/time context

Ticketing System
├─ IT tickets for password reset
├─ Access provisioning
├─ Known system maintenance
├─ Incident history
└─ Use for: Activity explanation

CMDB/Asset System
├─ Device owner
├─ Device type
├─ System criticality
├─ Patch status
└─ Use for: Asset context

Previous Incidents
├─ Similar alerts before
├─ How they were resolved
├─ Follow-up actions
└─ Use for: Pattern matching
```

### **External Sources:**

```
Threat Intelligence Platforms
├─ IP reputation
├─ Domain/URL reputation
├─ File hash verdict
├─ File signatures
└─ Use for: Indicator validation

Geographic Data
├─ IP geolocation
├─ Timezone information
├─ Travel patterns
└─ Use for: Impossible travel detection

Public Information
├─ Industry news
├─ Threat advisories
├─ Breach notifications
├─ Security research
└─ Use for: Context/trending
```

---

## Escalation Decision: When to Escalate

### **Escalate to L2 if:**

```
✓ Confirmed or strong suspicion of threat
  └─ Multiple indicators pointing to compromise

✓ Beyond L1 expertise
  └─ Malware analysis, complex forensics needed

✓ Incident response needed
  └─ Containment actions, coordination needed

✓ Investigation taking > 10 minutes
  └─ Too deep for triage, move to investigation

✓ Unclear decision despite good context
  └─ L2 judgment call needed

✓ Business impact unclear
  └─ L2 can engage business stakeholders

✓ Evidence preservation needed
  └─ Complex forensics, chain of custody

DON'T escalate if:
├─ Obviously false positive (waste of L2 time)
├─ Alert is informational only
├─ Problem already well-understood
└─ Just needs routine follow-up
```

---

## False Positive Identification

### **High FP Rate Causes:**

```
1. Alert Rule Too Sensitive
   ├─ Threshold too low
   ├─ Too many conditions met by normal activity
   └─ Fix: Tune rule parameters

2. Legitimate Automation
   ├─ Backup tools
   ├─ Monitoring agents
   ├─ Sync applications
   └─ Fix: Whitelist or suppress

3. Normal Business Activity
   ├─ End of month batch processing
   ├─ Quarter-end reporting
   ├─ Year-end audit activities
   └─ Fix: Calendar-aware rules

4. Known Remediation Attempts
   ├─ Security patches causing access issues
   ├─ Password reset after lockout
   └─ Fix: Temporary rule suppression during change
```

### **Quick FP Checks:**

```
Q1: Same alert repeating?
└─ If daily/hourly with exact pattern → FP candidate

Q2: Known legitimate reason?
└─ Check previous investigations, documentation

Q3: Automation or scheduled task?
└─ Check IT/admin knowledge, asset lists

Q4: Business calendar event?
└─ Check: End of month? Quarter end? Maintenance window?

Q5: System just updated/patched?
└─ Check change management tickets

Q6: User on travel or special project?
└─ Check HR system, email calendar

If 3+ answers = YES → Likely FP
```

---

## Practical Triage Checklist

### **Pre-Triage (Preparation)**

- [ ] Know your alert rules (top 20 rules)
- [ ] Know your organization
- [ ] Know how to access: AD, HR, tickets, SIEM
- [ ] Know escalation contacts
- [ ] Know SLA times

### **Triage Workflow**

**Phase 1: Intake (30 seconds)**
- [ ] Click alert, read alert name
- [ ] Note severity, timestamp
- [ ] Acknowledge alert (claim it)
- [ ] Start your timer

**Phase 2: Quick Context (2-3 minutes)**
- [ ] User: Legitimate? Known?
- [ ] Source: Internal? External?
- [ ] Target: Critical? Sensitive?
- [ ] Pattern: New? Repeated?

**Phase 3: Risk Assessment (2-3 minutes)**
- [ ] Threat likelihood: High/Medium/Low?
- [ ] Business impact: High/Medium/Low?
- [ ] Recoverability: Easy/Medium/Hard?
- [ ] Risk score: What level?

**Phase 4: Initial Decision (1-2 minutes)**
- [ ] Close? (If obvious FP)
- [ ] Investigate? (If uncertain)
- [ ] Escalate? (If high risk)

**Phase 5: Investigation (5-10 minutes max)**
- [ ] Verify alert accuracy (logs)
- [ ] Verify user context (AD, HR)
- [ ] Verify activity pattern (timeline)
- [ ] Verify system state (EDR, firewall)
- [ ] Verify intelligence (TI lookups)

**Phase 6: Final Decision**
- [ ] Close: Write reason + timestamp
- [ ] Escalate: Provide complete context
- [ ] Escalate: Follow escalation procedure

**Total time target: 15 minutes per alert**

### **After Triage**

- [ ] Document findings clearly
- [ ] Update ticket/alert
- [ ] Notify appropriate parties
- [ ] Note any pattern/trend observations
- [ ] Suggest rule improvements if applicable

---

## Real-World Triage Examples

### **Example 1: Brute Force - Resolve in Triage**

```
Alert: "Brute Force - 50 failed logins"
Severity: HIGH
Time: 03:45 AM

STEP 1 - INTAKE (30 sec)
├─ Alert name clear ✓
├─ Timestamp: Off-hours ⚠
└─ Claimed: Ready to investigate

STEP 2 - CONTEXT (2 min)
├─ User: john.doe (legitimate) ✓
├─ Source: 192.168.1.100 (internal) ✓
├─ Pattern: First time for john ❌
└─ Time: Off-hours unusual ⚠

STEP 3 - RISK (2 min)
├─ Threat: MEDIUM (unexpected)
├─ Impact: MEDIUM (internal device)
└─ Risk: MEDIUM → Investigate

STEP 4 - DECISION (1 min)
├─ Close? Not immediately
├─ Investigate? YES
└─ Escalate? Maybe after investigation

STEP 5 - INVESTIGATION (5 min)
├─ Logs: Confirmed 50x failures ✓
├─ User AD: Active, no reset today ✓
├─ File access: After login? CHECKING...
│  └─ YES: Some files accessed
│  └─ But normal employee files only
├─ Endpoint: No malware signals ✓
├─ TI: IP internal, no issues ✓
└─ Context: Why 50 failures?
   └─ Hypothesis: Typo in password? Cached password?

INVESTIGATION RESULT:
├─ Multiple indicators = not obvious FP
├─ But no compromise signals either
└─ RECOMMENDATION: Contact user to verify

STEP 6 - DECISION
├─ Close? NO - Needs verification
├─ Escalate? YES - For user contact
└─ Reason: "Verify cause of failures;
            no compromise signals but 
            activity unusual"

STATUS: ESCALATED to L2 with context
TIME: 12 minutes (within SLA)
```

### **Example 2: Phishing - Close in Triage**

```
Alert: "Phishing Email Detected"
Severity: MEDIUM
Recipients: 47 users

STEP 1 - INTAKE (30 sec)
├─ Alert name clear ✓
├─ Pattern: Bulk email ⚠
└─ Claimed: Ready

STEP 2 - CONTEXT (1 min)
├─ Email source: spoofed@bank.com (FAKE) ❌
├─ Recipients: All employees ✓
├─ Email action: QUARANTINED already ✓
├─ Users affected: Any opened? Checking...
└─ Pattern: Same as yesterday's FP? CHECKING...

PREVIOUS INVESTIGATION NOTE:
└─ Yesterday: Same sender, same pattern, all caught

STEP 3 - RISK (1 min)
├─ Threat: LOW (already caught, FP candidate)
├─ Impact: NONE (quarantined)
└─ Risk: LOW → Likely FP

STEP 4 - DECISION (30 sec)
├─ Close? PROBABLY
├─ Investigate? Brief check
└─ Escalate? Not needed

QUICK CHECK (1 min):
├─ Same sender as yesterday? YES
├─ Same email body? YES (confirmed)
├─ Same pattern? YES
├─ All quarantined? YES
└─ Any user clicked? NO

STEP 5 - DECISION
├─ Verdict: FALSE POSITIVE
└─ Reason: "Duplicate phishing campaign from 
           yesterday; all emails quarantined; 
           no users affected; alert rule 
           triggered redundantly"

RECOMMENDATION: Update rule to recognize pattern
STATUS: CLOSED
TIME: 5 minutes
```

### **Example 3: Malware - Escalate Immediately**

```
Alert: "Malware Detected - Trojan.Emotet"
Severity: CRITICAL
File: invoice.exe
Device: finance-laptop

STEP 1 - INTAKE (30 sec)
├─ Alert name: CRITICAL concern ⚠
├─ Malware family: Known dangerous ❌
└─ Claimed: Ready

STEP 2 - CONTEXT (1 min)
├─ Device: Finance laptop (CRITICAL!)
├─ File: invoice.exe (typical phishing)
├─ Source: User downloaded
└─ Status: PENDING - Not yet isolated

STEP 3 - RISK (1 min)
├─ Threat: CRITICAL (known ransomware family)
├─ Impact: CRITICAL (finance system)
└─ Risk: CRITICAL → IMMEDIATE ACTION

STEP 4 - DECISION (30 sec)
├─ Close? NO - Confirmed malware
├─ Investigate? NO - Clear threat
└─ Escalate? YES - IMMEDIATELY

STEP 5 - ESCALATION
├─ Escalate to: Incident Response
├─ Actions needed:
│  ├─ Isolate device immediately
│  ├─ Preserve evidence
│  ├─ Audit file server access
│  └─ Alert finance manager
├─ Context provided:
│  ├─ Alert timestamp
│  ├─ File hash + signature
│  ├─ Device info + user
│  └─ File location + potential impact

STATUS: ESCALATED to IR - CRITICAL
TIME: 3 minutes (ASAP)
```

---

## Common Triage Mistakes

### ❌ **Mistake 1: Spending too long in triage**

**সমস্যা:** 30 minutes একটা alert investigate করছি

**সমাধান:** 15 min max. যদি unclear থাকে escalate করুন

---

### ❌ **Mistake 2: Not using context sources**

**সমস্যা:** User কে verify করছি না AD এ

**সমাধান:** সবসময় quick context check করুন

---

### ❌ **Mistake 3: Escalating false positives**

**সমস্যা:** Known FP escalate করছি L2 এ

**সমাধান:** Documentation চেক করুন, known patterns চিনুন

---

### ❌ **Mistake 4: Not documenting findings**

**সমস্যা:** Investigation করেছি কিন্তু notes রাখিনি

**সমাধান:** সবসময় findings document করুন

---

### ❌ **Mistake 5: Ignoring trends**

**সমস্যা:** Same alert 10x দেখেছি এটা pattern না বুঝে

**সমাধান:** Bulk assessment করুন, pattern recognize করুন

---

## Mini Quiz: Triage Fundamentals

### **Question 1: Triage এর primary goal কোনটি?**

A) Deep technical investigation  
B) Rapid assessment + decision  
C) Close all false positives  
D) Escalate everything to L2

**Answer:** B) Rapid assessment + decision - Triage speed + accuracy balanced

---

### **Question 2: Triage কত সময় লাগবে একটা alert এ?**

A) 5 minutes maximum  
B) 15 minutes maximum  
C) 30 minutes maximum  
D) 1 hour if needed

**Answer:** B) 15 minutes maximum - এর বেশি হলে escalate করুন

---

### **Question 3: Triage এর কোন step সবচেয়ে গুরুত্বপূর্ণ decision point?**

A) Alert Intake  
B) Quick Context  
C) Risk Assessment  
D) Investigation

**Answer:** C) Risk Assessment - এখানে close vs escalate decide হয়

---

### **Question 4: False Positive identify করার quickest way কোনটি?**

A) Deep investigation (1 hour)  
B) Check alert history + documentation  
C) Escalate সব FP suspect করুন  
D) Run intelligence tools

**Answer:** B) Check alert history + documentation - Known patterns সবচেয়ে দ্রুত

---

### **Question 5: যখন escalate করবেন L2 কে, কোনটা include করবেন?**

A) Just alert ID  
B) Just severity  
C) Complete context + investigation findings  
D) Everything from raw logs

**Answer:** C) Complete context + investigation findings - L2 কে decision এ সাহায্য করতে

---

## সহজ ভাষায় সারসংক্ষেপ

**Triage = দ্রুত assessment, not deep investigation**

**5-Step Triage Process:**
1. **Intake:** Alert read, claim করুন (30 sec)
2. **Quick Context:** User, source, target, pattern (2-3 min)
3. **Risk Assessment:** Threat × Impact = Risk (2-3 min)
4. **Initial Decision:** Close? Investigate? Escalate? (1-2 min)
5. **Investigation:** Deep dive যদি unclear (5-10 min max)

**Decision outcomes:**
- **Close:** FP identified, clear reason
- **Investigate:** Unclear, need more data
- **Escalate:** High risk, L2 expertise needed

**Key triage skills:**
- Quick pattern recognition
- Context gathering (AD, HR, tickets, TI)
- Risk assessment accuracy
- Decision confidence
- Time management (15 min max)

**Common patterns:**
- False Positive: Known benign
- Suspicious: Need context
- Confirmed: Escalate immediately
- Trend: Bulk assessment

**Remember:**
- Triage ≠ Investigation (triage FAST)
- Use context sources efficiently
- Recognize common patterns
- Escalate when uncertain
- Document your findings

---

## Resources for Learning

**Triage training:**
- Your company playbooks
- Alert rule documentation
- Previous investigation examples
- L2 mentor guidance

**Context tools:**
- AD system access
- HR system access
- SIEM query training
- Ticket system tutorials

---

**Module 7 Complete! ✅**

এখন আপনি জানেন:
- ✅ Triage কি এবং কেন critical
- ✅ 5-step triage framework
- ✅ Alert intake process
- ✅ Quick context gathering
- ✅ Risk assessment logic
- ✅ Close vs Investigate vs Escalate decision
- ✅ Investigation depth limits
- ✅ Common triage patterns
- ✅ False positive identification
- ✅ Escalation criteria
- ✅ Real-world triage examples
- ✅ Practical triage checklist

Progress: **7 of 28 modules complete (25%)**

