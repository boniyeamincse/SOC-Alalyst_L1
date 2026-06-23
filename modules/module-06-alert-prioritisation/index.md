# Module 6: Alert Severity and Prioritisation

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- Severity কি এবং কিভাবে determine হয়
- Priority এবং Severity এর পার্থক্য
- Severity levels: Critical, High, Medium, Low
- Alert prioritisation strategy
- Triage queue management
- SLA (Service Level Agreement) এবং response time
- কখন severity override করবেন
- Business context অনুযায়ী prioritisation
- Real SOC prioritisation scenarios
- Queue management best practices

---

## শুরুর আগে: একটি গল্প

সকাল ৯টায় রহিম তার SOC shift শুরু করলো। Dashboard এ 350টি alerts waiting:

```
Critical:  5 alerts
High:     45 alerts
Medium:  200 alerts
Low:     100 alerts
```

এখন প্রশ্ন: কোন alerts প্রথমে handle করবে? 

রহিম শুধু Critical 5টা দেখলো না। সে দেখলো:
- সেগুলোর মধ্যে 2টা false positive
- Medium severity এর মধ্যে 1টা একটা important customer এর database access (আসলে Critical হওয়া উচিত)
- Low severity এ একটা suspicious pattern যা ৫টি similar alerts এর সাথে মিলছে (trend আছে)

এটাই **Alert Prioritisation** - শুধু severity দেখা নয়, context দেখে priority decide করা।

এই module এ শিখব কিভাবে efficiently prioritise করতে হয়।

---

## Severity vs Priority: মূল পার্থক্য

### **Severity:**

Severity = **এই alert কতটা serious?**

Alert rule define করে severity automatic।

```
Fixed দ্বারা:
├─ Threat type
├─ Impact area
├─ Known threat signature
└─ Rule configuration

Examples:
├─ Ransomware detected = CRITICAL
├─ Phishing email = HIGH
├─ Failed login = LOW
```

### **Priority:**

Priority = **আমাদের এখন কোনটা handle করবো?**

Priority decide করে human (L1/Manager) context এবং business situation দেখে।

```
Depends on:
├─ Severity (inherent threat level)
├─ Business impact (which system affected)
├─ Queue length (backlog কত?)
├─ SLA (response time requirement)
├─ Context (legitimate user? known pattern?)
└─ Business time (peak hours vs off-hours)
```

### Visual: Severity vs Priority

```
Same severity, different priority:

Alert 1: "Malware on laptop" 
├─ Severity: CRITICAL
├─ Device: Non-critical workstation
├─ User: Intern
└─ Priority: 2nd (Important, not urgent)

Alert 2: "Malware on database server"
├─ Severity: CRITICAL
├─ Device: Critical infrastructure
├─ Impact: Business halted
└─ Priority: 1st (IMMEDIATE)

Same alert, changing priority:

08:00 AM: "Medium severity - unusual login"
├─ Queue: 50 alerts
├─ Priority: Handle after critical alerts
├─ Time to investigate: 2 hours

02:00 AM: "Medium severity - unusual login"
├─ Queue: 2 alerts
├─ Priority: Handle immediately
├─ Time to investigate: 5 minutes
└─ Why? Off-hours, more suspicious
```

---

## Severity Levels Explained

### **Level 1: CRITICAL (P0 / Red)**

```
Severity Signals:
├─ Known malware/ransomware
├─ Active data exfiltration
├─ Critical system compromised
├─ Breach in progress
├─ Large-scale attack
└─ Immediate business impact

Response Time SLA: < 5 minutes
Investigation: IMMEDIATE

Examples:
├─ "Ransomware detected on production server"
├─ "500 GB data transfer to external IP"
├─ "Multiple admin accounts created"
├─ "C2 communication detected"
└─ "Financial database accessed externally"

Action:
├─ Immediate escalation
├─ Incident Response team activation
├─ Executive notification
├─ Possible business shutdown decision
```

### **Level 2: HIGH (P1 / Orange)**

```
Severity Signals:
├─ Brute force attack
├─ Privilege escalation attempt
├─ Suspected account compromise
├─ Suspicious PowerShell/script
├─ Data access anomaly
└─ Potential incident indicators

Response Time SLA: < 15 minutes
Investigation: URGENT

Examples:
├─ "50 failed logins followed by 1 success"
├─ "User added to admin group"
├─ "Suspicious process execution"
├─ "Phishing email to C-level executive"
└─ "VPN login from 5 countries in 1 hour"

Action:
├─ L1 investigate ASAP
├─ Escalate to L2 if complex
├─ Possible containment actions
├─ Monitor closely
```

### **Level 3: MEDIUM (P2 / Yellow)**

```
Severity Signals:
├─ Unusual activity patterns
├─ Failed authentication attempts
├─ File access anomalies
├─ Network connection to suspicious domain
├─ Geo-inconsistent activity
├─ Could be legitimate or suspicious

Response Time SLA: < 1 hour
Investigation: INVESTIGATE WITHIN SHIFT

Examples:
├─ "User login from unusual location"
├─ "Multiple file access in short time"
├─ "Large email attachment detected"
├─ "DNS query to new domain"
└─ "USB device access attempt"

Action:
├─ Normal investigation
├─ Context gathering
├─ User/manager confirmation if needed
├─ Close if benign, escalate if suspicious
```

### **Level 4: LOW (P3 / Blue)**

```
Severity Signals:
├─ Informational only
├─ Known benign patterns
├─ High false positive probability
├─ Non-critical system
├─ Trend monitoring only
└─ No immediate threat

Response Time SLA: < 4 hours
Investigation: WHEN TIME PERMITS

Examples:
├─ "Failed login (old password)"
├─ "File access outside normal hours"
├─ "Software update detected"
├─ "Password expiry warning"
└─ "Test alert from monitoring"

Action:
├─ Low priority investigation
├─ Bulk close if pattern known
├─ Document findings
├─ Ignore if FP rate > 80%
```

---

## Severity Determination: How Rules Decide

### **Automatic Severity Setting:**

SIEM rules severity assign করে based on threat signature:

```
Detection Rule: "Ransomware File Behavior"

Input factors:
├─ File encryption detected: YES → +40
├─ File extension changes: YES → +30
├─ Master boot record access: YES → +20
├─ Network communication to C2: YES → +30
└─ Total score: 120/100

Output: CRITICAL severity

---

Detection Rule: "Failed Login"

Input factors:
├─ Failed authentication: YES → +10
├─ Repeated attempts: NO → +0
├─ From known location: YES → -5
├─ Known user: YES → -5
└─ Total score: 0/100

Output: LOW severity
```

### **Manual Severity Override:**

কখনো কখনো L2/Manager override করে severity:

```
Original: "Medium severity - file access"
Scenario: Small engineering firm, 1 database

Normal Context:
├─ Database access: Routine
├─ Medium severity: Appropriate
└─ Handle when time permits

Override Context:
├─ Ransomware attack in progress (news)
├─ Same file patterns detected
├─ Similar firm attacked yesterday
└─ Change to CRITICAL

Decision: "Override to CRITICAL given context"
Reason: "Targeted ransomware attack pattern"
```

---

## Priority Levels: Tactical Decisions

### **How L1 Prioritises Queue:**

```
Alert Queue Management:

09:00 AM: 350 alerts waiting

Priority Matrix:
┌──────────────┬─────────────────┬──────────────────────┐
│ Severity     │ Business Impact │ Priority             │
├──────────────┼─────────────────┼──────────────────────┤
│ CRITICAL     │ HIGH            │ NOW (< 5 min)        │
│ CRITICAL     │ LOW             │ VERY SOON (< 15 min) │
│ HIGH         │ HIGH            │ SOON (< 30 min)      │
│ HIGH         │ LOW             │ NORMAL (< 1 hour)    │
│ MEDIUM       │ HIGH            │ NORMAL (< 1 hour)    │
│ MEDIUM       │ LOW             │ BATCH (< 4 hours)    │
│ LOW          │ ANY             │ BATCH (< 4 hours)    │
└──────────────┴─────────────────┴──────────────────────┘

Execution order:
1. CRITICAL + HIGH_impact (2 alerts) - START
2. CRITICAL + LOW_impact (3 alerts) - WAIT
3. HIGH + HIGH_impact (5 alerts) - WAIT
4. HIGH + LOW_impact (10 alerts) - WAIT
5. MEDIUM + HIGH_impact (8 alerts) - WAIT
6. MEDIUM + LOW_impact (50 alerts) - BATCH
7. LOW (100 alerts) - BATCH
```

---

## Business Context: Impact-Based Prioritisation

### **System Criticality:**

```
Business Impact Assessment:

Tier 1 (CRITICAL):
├─ Production database
├─ Payment processing
├─ Customer-facing services
├─ Security infrastructure
└─ Employee authentication

Tier 2 (HIGH):
├─ Development environments
├─ Internal dashboards
├─ Email systems
├─ File servers
└─ Time tracking systems

Tier 3 (MEDIUM):
├─ Test environments
├─ Non-critical workstations
├─ Archive systems
├─ Legacy applications
└─ Developer machines

Tier 4 (LOW):
├─ Laptops (non-critical staff)
├─ Guest WiFi
├─ Lab systems
└─ Sandbox machines
```

### **Same Alert, Different Priority:**

```
Alert: "Unusual file access pattern"

Scenario A: HR workstation
├─ System: Medium criticality
├─ Data: Employee records (sensitive)
├─ Impact: Medium
├─ Priority: Handle within 1 hour

Scenario B: Test server
├─ System: Low criticality
├─ Data: Test data only
├─ Impact: Low
├─ Priority: Handle when convenient

Scenario C: Finance database
├─ System: Critical
├─ Data: Financial records (very sensitive)
├─ Impact: High (compliance, reporting)
├─ Priority: IMMEDIATE
```

---

## SLA (Service Level Agreement): Response Times

### **What is SLA?**

SLA = Commitment কত দ্রুত সমস্যার সমাধান করবো।

```
Alert Severity → SLA Response Time → SLA Escalation

CRITICAL:
├─ Acknowledge: < 5 minutes
├─ Investigation start: < 5 minutes
├─ Update provided: Every 15 minutes
└─ Manager escalation if: > 30 minutes unresolved

HIGH:
├─ Acknowledge: < 15 minutes
├─ Investigation start: < 15 minutes
├─ Update provided: Every 1 hour
└─ Manager escalation if: > 2 hours unresolved

MEDIUM:
├─ Acknowledge: < 1 hour
├─ Investigation start: < 1 hour
├─ Update provided: Daily
└─ Manager escalation if: > 8 hours unresolved

LOW:
├─ Acknowledge: < 4 hours
├─ Investigation start: < 4 hours
├─ Update provided: Weekly
└─ Manager escalation if: > 24 hours unresolved
```

### **SLA Tracking:**

```
Alert Properties:
├─ received_at: 2024-06-21 14:30:00
├─ severity: CRITICAL
├─ sla_response_time: 5 minutes
├─ sla_deadline: 2024-06-21 14:35:00
├─ acknowledged_at: 2024-06-21 14:33:15 ✓ (within 5 min)
├─ investigation_start: 2024-06-21 14:33:45 ✓
├─ status_update_sent: 2024-06-21 14:45:00 ✓
└─ currently_elapsed: 15 minutes (50% of SLA)

Dashboard SLA Status:
┌─────────────────────────────────────────────┐
│ Alert ALERT-0001 SLA Status                 │
├─────────────────────────────────────────────┤
│ ████████░░░░░░░░░░░░░░░░ 50% elapsed       │
│ Deadline: 14:35:00                          │
│ Current: 14:45:00 - WITHIN SLA ✓            │
│ Estimated resolution: 16:30:00              │
└─────────────────────────────────────────────┘
```

### **SLA Breach:**

```
Critical alert not acknowledged in 5 minutes
        │
        ▼
Manager notification: "ALERT SLA BREACH"
        │
    ┌───┴─────┐
    │         │
Assigned  Escalate
to new    to L2
analyst   immediately

Dashboard shows:
🔴 ALERT-0001 [SLA BREACH - 5 min overdue]
```

---

## Triage Queue Management

### **Daily Workflow:**

```
09:00 AM - Shift Start
├─ Dashboard check: 350 alerts
├─ Sort by priority
├─ Identify SLA breaches
└─ Create work plan

09:15 AM - Handle Critical
├─ 5 CRITICAL alerts
├─ Avg time: 10 min each
├─ Complete: 09:50 AM

09:50 AM - Handle HIGH
├─ 45 HIGH alerts
├─ Avg time: 5 min each (some are FP)
├─ Complete: 12:40 PM (with break)

12:40 PM - Lunch break

13:00 PM - Handle MEDIUM + LOW
├─ 300 MEDIUM + LOW alerts
├─ Bulk process (many similar)
├─ Batch close obvious FP
├─ Complete: 17:00 PM

17:00 PM - Shift End
├─ Handover to evening shift
├─ Status: 95% alerts processed
└─ 15 escalated to L2
```

### **Queue Backlog Scenario:**

```
Normal day:
Alerts coming: 150/hour
Alerts processed: 150/hour
Queue: Stable (350 alerts)

High activity day:
Alerts coming: 500/hour
Alerts processed: 150/hour
Queue: Growing (850+ alerts)

Response:
├─ Manager alerted at 600 queue
├─ LOW severity alerts auto-closed
├─ Batch processing initiated
├─ Additional L1 called in
└─ New rule tuning (reduce FP)
```

---

## Real-World Prioritisation Scenarios

### **Scenario 1: Multiple Critical Alerts**

```
09:00 AM - 4 CRITICAL alerts arrive simultaneously:

Alert A: "Ransomware on server"
├─ Severity: CRITICAL
├─ System: Database server
├─ Impact: CRITICAL
└─ Priority: #1 - IMMEDIATE

Alert B: "Failed login retry 100x"
├─ Severity: CRITICAL
├─ System: Mail server
├─ Impact: MEDIUM (retry still active, not breached)
└─ Priority: #2 - AFTER A

Alert C: "Suspicious PowerShell"
├─ Severity: CRITICAL
├─ System: Admin workstation
├─ Impact: MEDIUM (isolated, non-critical)
└─ Priority: #3 - AFTER B

Alert D: "Data transfer 1TB to external"
├─ Severity: CRITICAL
├─ System: File server
├─ Impact: CRITICAL
└─ Priority: #2 TIE WITH B (both critical impact)
    Check timestamp - Alert D earlier → #2

Final order: A → D/B → C
Reasoning: Impact CRITICAL > MEDIUM
           Among MEDIUM: First come first serve
```

### **Scenario 2: False Positive Detection Opportunity**

```
Alerts in queue:
├─ 15 "User login from unusual location"
├─ 12 "Failed authentication attempts"
└─ 8 "Large file download"

Pattern Recognition:
"User login from unusual location" - all same IP
(203.0.113.100 - Singapore)

Investigation of first 3:
├─ Alert 1: john.doe from Singapore ← Check...
│  └─ FOUND: john.doe travel approval (June 20-25)
│  └─ Verdict: FALSE POSITIVE
│
├─ Alert 2: alice@company.com from Singapore ← Check...
│  └─ FOUND: Same delegation, company event Singapore
│  └─ Verdict: FALSE POSITIVE
│
├─ Alert 3: admin@company.com from Singapore
│  └─ FOUND: Same event, all team on trip
│  └─ Verdict: FALSE POSITIVE

Decision: Check remaining 12 - likely all FP
└─ Bulk close: "All same business trip - expected"
└─ Time saved: 12 × 10 min = 120 minutes
└─ Communicate pattern to L2: Update alert rule
```

### **Scenario 3: Context Changes Priority**

```
Morning 08:00:
Alert: "Failed login 5 times on trading account"
├─ Severity: MEDIUM (normal business day)
├─ Impact: MEDIUM
├─ Priority: Handle in 1 hour
└─ Analyst: Queued for later

Afternoon 14:30:
News: "Major financial fraud case in industry"
└─ Several firms targeted with same pattern

Re-evaluation:
Alert (same alert): "Failed login 5 times on trading"
├─ Severity: Still MEDIUM (rule didn't change)
├─ But context: CRITICAL (known targeted attack)
├─ Priority: UPGRADE to #1 - IMMEDIATE
├─ Action: Escalate to incident response
└─ Reason: Coordinated attack pattern
```

---

## Prioritisation Mistakes: What NOT to Do

### ❌ **Mistake 1: Only following alert severity**

**সমস্যা:** CRITICAL alert handling করছি কিন্তু LOW severity এ active breach আছে

**সমাধান:** Severity + business context উভয়ো দেখুন

---

### ❌ **Mistake 2: Ignoring SLA**

**সমস্যা:** Alert SLA breach হয়েছে কিন্তু investigating continue করছি casual mode এ

**সমাধান:** SLA dashboard সবসময় monitor করুন

---

### ❌ **Mistake 3: Queue backlog ignore করা**

**সমস্যা:** 500 alerts queue তে আছে কিন্তু manager কে report করছি না

**সমাধান:** Queue > 200 হলে escalate করুন

---

### ❌ **Mistake 4: Pattern miss করা**

**সমস্যা:** 50টি same type alert আলাদাভাবে investigate করছি

**সমাধান:** Bulk processing করুন similar alerts এর জন্য

---

### ❌ **Mistake 5: Context ignore করা**

**সমস্যা:** Alert rule বলছে MEDIUM কিন্তু it's CEO এর account compromise

**সমাধান:** যদি business impact HIGH হয়, severity override করুন

---

## Practical Checklist: Daily Prioritisation

শিফটের শুরুতে:

**✅ Dashboard Assessment (5 min)**
- [ ] Total alerts count note করুন
- [ ] CRITICAL count: কত?
- [ ] HIGH count: কত?
- [ ] SLA breaches check করুন

**✅ SLA Breach Management**
- [ ] কোন alerts SLA breach করেছে?
- [ ] সেগুলো escalate করুন immediate
- [ ] Manager কে notify করুন

**✅ Create Priority Matrix**
- [ ] CRITICAL + HIGH_business → Priority 1 (Now)
- [ ] CRITICAL + LOW_business → Priority 2 (Soon)
- [ ] HIGH + HIGH_business → Priority 3 (Soon)
- [ ] Rest → Priority 4 (Batch process)

**✅ Pattern Detection**
- [ ] Similar alerts grouped?
- [ ] Bulk close opportunities?
- [ ] Trend alerts?

**✅ Capacity Planning**
- [ ] Queue > 300? Activate backup
- [ ] Queue > 500? Escalate to manager
- [ ] Alert rate increasing? Note for L2

**✅ Work Allocation**
- [ ] Priority 1: Start now
- [ ] Priority 2: Parallel processing
- [ ] Priority 3-4: As time permits
- [ ] Recheck SLA every 30 minutes

**✅ During Shift**
- [ ] Update SLA progress
- [ ] Any emergencies? Reorder queue
- [ ] Communicate blockers

**✅ Shift End**
- [ ] Queue status: Handover notes
- [ ] Escalated items: Context document
- [ ] Trends: What changed today?

---

## Severity Override: When and How

### **When to Override Severity:**

```
Original: MEDIUM
Condition 1: Business context critical
├─ CEO account (even if medium alert)
├─ Legal case related (even if medium alert)
├─ Regulatory requirement
└─ Override to: HIGH or CRITICAL

Original: LOW
Condition 2: Attack pattern detected
├─ Same alert x100 from different users
├─ Coordinated attack signatures
├─ Industry-wide campaign
└─ Override to: CRITICAL

Original: CRITICAL
Condition 3: Known false positive
├─ Same pattern as yesterday's FP
├─ Alert rule known broken
├─ Rate limit exceeded
└─ Override to: LOW (suppress, fix rule later)
```

### **How to Override:**

```
1. Document reason clearly
├─ What are you overriding?
├─ From what to what?
├─ Why? (business context, pattern, etc.)

2. Notify management
├─ Severity changes logged
├─ Manager approval required (org dependent)

3. Update rule (if pattern-based)
├─ Communicate to L2
├─ Rule needs tuning
├─ Prevent future false overrides

Example override:
┌──────────────────────────────────────────┐
│ Severity Override                        │
├──────────────────────────────────────────┤
│ Alert ID: ALERT-0001                     │
│ Original Severity: LOW                   │
│ New Severity: CRITICAL                   │
│                                          │
│ Reason:                                  │
│ "Coordinated attack pattern - 47 users   │
│  targeted simultaneously with same       │
│  phishing campaign. Industry alert       │
│  issued. Escalating to incident response"│
│                                          │
│ Approved By: SOC_Manager                 │
│ Time: 09:15 IST                          │
│ Effective: Immediately                   │
└──────────────────────────────────────────┘
```

---

## Alert Volume Impact on Prioritisation

### **Low Volume Days (< 100 alerts):**

```
Approach: Thorough investigation
├─ Each alert: 15-20 min investigation
├─ Deep dive into context
├─ Escalate when needed
└─ Quality > Speed
```

### **Normal Days (100-400 alerts):**

```
Approach: Balanced
├─ CRITICAL: Deep investigation
├─ HIGH: Normal investigation
├─ MEDIUM: Quick check
├─ LOW: Batch/close
└─ Balance quality + speed
```

### **High Volume Days (> 400 alerts):**

```
Approach: Triage-focused
├─ CRITICAL: Immediate
├─ HIGH: Escalate generously (L2 handles)
├─ MEDIUM: Bulk process + close obvious
├─ LOW: Auto-close or close with group
└─ Speed > Deep analysis

Actions:
├─ Alert fatigue risk: Keep high
├─ Quality risk: Higher
├─ Manager call: Additional L1?
├─ Ask: Rule tuning needed?
```

---

## Mini Quiz: Prioritisation

### **Question 1: Priority এবং Severity এর মধ্যে main পার্থক্য কি?**

A) Priority automatic, Severity manual  
B) Severity rule-based, Priority context-based  
C) একই জিনিস, different names  
D) Priority only for CRITICAL

**Answer:** B) Severity rule-based, Priority context-based - Severity algorithm decide করে, Priority human decide করে context দেখে

---

### **Question 2: CRITICAL severity alert এর SLA response time কত?**

A) 15 minutes  
B) 5 minutes  
C) 1 hour  
D) End of shift

**Answer:** B) 5 minutes - CRITICAL এ immediate response required

---

### **Question 3: কোন scenario এ severity override করবেন?**

A) কখনো না - Rule এর decision সবসময় সঠিক  
B) Business impact critical হলে  
C) Pattern detected হলে  
D) Both B এবং C

**Answer:** D) Both B এবং C - Business context এবং attack patterns উভয়োই severity change করতে পারে

---

### **Question 4: Alert queue 400+ হলে কি করবেন?**

A) সব alerts handle না হওয়া পর্যন্ত শান্ত থাকুন  
B) Manager কে escalate করুন  
C) LOW severity alerts auto-close করুন  
D) Both B এবং C

**Answer:** D) Both B এবং C - Manager inform করুন এবং backlog reduce করার তাৎক্ষণিক action নিন

---

### **Question 5: একই MEDIUM severity alert, কিন্তু different systems তে - priority সবসময় same?**

A) হ্যা - Severity determine করে priority  
B) না - System criticality affect করে priority  
C) Depends on time of day  
D) Depends on analyst skill

**Answer:** B) না - System criticality affect করে priority - Same alert, different impact = different priority

---

## সহজ ভাষায় সারসংক্ষেপ

**Severity = Rule-based threat level**
- CRITICAL: Active threat
- HIGH: Suspicious activity
- MEDIUM: Could be threat
- LOW: Informational

**Priority = Human decision (context)**
- Not just severity
- Business impact important
- System criticality important
- Current queue status important

**Prioritisation strategy:**
1. Check SLA breaches (escalate immediately)
2. Handle CRITICAL first
3. Consider business impact
4. Batch similar LOW severity
5. Monitor queue health
6. Escalate when backlogged

**SLA = Response time commitment**
- CRITICAL: < 5 min
- HIGH: < 15 min
- MEDIUM: < 1 hour
- LOW: < 4 hours

**Remember:**
- Severity ≠ Priority
- Context matters
- Pattern detection saves time
- SLA must be tracked
- Escalate when overwhelmed

---

## Resources for Learning

**Prioritisation framework:**
- NIST cybersecurity maturity
- Your company SLA policy
- Industry standards (SANS, CIS)

**Alert tuning:**
- False positive rate tracking
- Rule effectiveness metrics
- Your SIEM vendor docs

---

**Module 6 Complete! ✅**

এখন আপনি জানেন:
- ✅ Severity vs Priority পার্থক্য
- ✅ 4টি severity levels এবং response times
- ✅ কিভাবে severity determine হয়
- ✅ Business context prioritisation
- ✅ SLA tracking এবং breaches
- ✅ Queue management strategies
- ✅ Pattern-based bulk processing
- ✅ Severity override যখন প্রয়োজন
- ✅ Real-world prioritisation scenarios
- ✅ Daily prioritisation workflow

---

<!-- nav-footer -->
## 🧭 Navigation

| | |
|---|---|
| **Previous** | [⬅️ Module 05: Alert Properties](../module-05-alert-properties/index.md) |
| **Next** | [Module 07: Alert Triage Fundamentals ➡️](../module-07-alert-triage-fundamentals/index.md) |
| **🏠 Course Home** | [STUDY_NOTES.md](../../STUDY_NOTES.md) |
