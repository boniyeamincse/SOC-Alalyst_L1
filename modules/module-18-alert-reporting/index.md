# Module 18: Alert Reporting

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- Alert reporting কেন critical
- Five Ws framework (Who, What, When, Where, Why)
- Alert ticket structure
- Evidence collection এবং documentation
- Clear finding summary
- Playbook references
- Escalation communication
- Real reporting examples
- Common reporting mistakes

---

## শুরুর আগে: একটি গল্প

করিম একটি alert investigate করলো এবং verdict পেলো। এখন escalate করবে L2 কে।

Poor reporting:
```
Ticket: "Alert #123 - Suspicious"
Comment: "Checked stuff, looks bad"
Escalated to: L2_analyst

L2 response: "What did you check? What evidence? 
             What makes you think it's bad?"
Result: Time wasted, rework needed
```

Good reporting:
```
Ticket: "Alert #123 - Suspicious database access"
Summary:
├─ User: john.doe (Finance, not IT)
├─ Target: production_database (Tier 1)
├─ Action: SELECT on financial tables
├─ Finding: First time john accessed database
├─ Evidence: AD confirms no DB access before
├─ Risk: User not authorized, sensitive data

Evidence attached:
├─ SIEM timeline (screenshot)
├─ User AD record (screenshot)
├─ Database access logs (export)
├─ Playbook used: "Unauthorized DB Access"

Recommendation: Verify with john's manager
Escalated to: L2_analyst

L2 response: "Clear findings, good context.
            Following up with manager now."
Result: Smooth handoff, proper escalation
```

**Good reporting = Smooth escalation, no rework.**

---

## Alert Reporting কেন Critical

### Impact of Good Reporting:

```
Good report:
├─ L2 understands immediately
├─ No "what do you mean?" questions
├─ Can escalate further if needed
├─ Documents investigation
├─ Helps future analysts
└─ Metrics tracking works

Poor report:
├─ L2 confused
├─ Asks for clarification
├─ More back-and-forth
├─ Wastes time
├─ No documentation value
└─ Metrics unclear
```

### Reporting Requirements:

```
Every alert report needs:
├─ WHAT happened (alert summary)
├─ WHO was involved (user/system/IP)
├─ WHEN it occurred (timestamp)
├─ WHERE it happened (system/location)
├─ WHY you think so (evidence)
├─ VERDICT (TP/FP/Benign/Suspicious)
└─ RECOMMENDATION (close/escalate/investigate)
```

---

## Five Ws Framework

### **WHO - Identity**

```
Answer: Who was involved in this alert?

Include:
├─ Username: john.doe
├─ Full name: John Doe
├─ Department: Finance
├─ Job title: Senior Analyst
├─ Type: Human or service account?
├─ Status: Active or disabled?
├─ Role: Normal access level?

Example report:
"User: john.doe (Finance department, 
 Senior Analyst, active account, no admin rights)"
```

### **WHAT - Activity**

```
Answer: What activity triggered alert?

Include:
├─ Alert name: "Unusual database access"
├─ Action: Database login attempt
├─ Target: production_database
├─ Result: Successful access
├─ Data accessed: Financial tables
├─ Volume: How much accessed?

Example report:
"Activity: User successfully accessed
 production_database and queried
 financial transaction tables (SELECT
 on sales_transactions table, ~50k rows returned)"
```

### **WHEN - Timestamp**

```
Answer: When did this happen?

Include:
├─ Date: 2024-06-21
├─ Time: 14:30:45 IST
├─ Duration: How long? (5 minutes)
├─ Timezone: IST (specify for clarity)
├─ Time pattern: Business hours? Off-hours?
├─ Frequency: First time? Regular pattern?

Example report:
"Timestamp: 2024-06-21 14:30:45 IST
 Duration: Activity lasted 5 minutes
 Pattern: First time john accessed database
           (checked AD: no prior access)"
```

### **WHERE - Location**

```
Answer: Where did this happen?

Include:
├─ System: Which server/device?
├─ Network: Which subnet?
├─ IP address: Source and destination
├─ Geographic: Physical location
├─ VPN: On VPN or direct?

Example report:
"Location: Database server in US-East datacenter
 Source IP: 10.0.1.100 (office subnet)
 Device: john's workstation
 Connection: Direct office network
 (not on VPN)"
```

### **WHY - Evidence & Analysis**

```
Answer: Why do you think this happened/is suspicious?

Include:
├─ Evidence: What data supports this?
├─ Analysis: What does it mean?
├─ Context: Any business reason?
├─ Baseline: How does this compare to normal?
├─ Red flags: Any concerns?

Example report:
"Evidence & Analysis:
 1. john.doe never accessed DB before
    (checked SIEM 6 months back: 0 DB logins)
 2. No ticket requesting DB access
    (searched Jira, ServiceNow: nothing)
 3. Unusual for Finance role
    (Finance typically read reports, not query DB)
 4. Target is financial_transactions table
    (sensitive data - sales, revenue)
 5. Timing: During business hours (normal)
    
 Red flags:
 ✗ No business justification
 ✗ First-time database access
 ✗ Unauthorized user role
 ✓ Normal time (not suspicious)
 ✓ From office network (expected)"
```

---

## Alert Ticket Structure

### Standard Ticket Format:

```
┌─────────────────────────────────────────┐
│ ALERT TICKET TEMPLATE                   │
├─────────────────────────────────────────┤
│                                         │
│ TICKET ID: INC-2024-001                │
│ ALERT NAME: Unusual Database Access    │
│ TIMESTAMP: 2024-06-21 14:30:45 IST     │
│ REPORTER: L1_analyst_1                 │
│                                         │
│ ─ SUMMARY ─                            │
│ User john.doe (Finance) accessed      │
│ production_database and queried        │
│ financial data. First-time access,    │
│ no business justification found.       │
│                                         │
│ ─ FIVE Ws ─                           │
│ WHO: john.doe (Finance, Senior)        │
│ WHAT: DB login + SELECT query          │
│ WHEN: 14:30:45 IST (business hours)   │
│ WHERE: Office network, DB server       │
│ WHY: First access, no ticket, no auth │
│                                         │
│ ─ VERDICT ─                           │
│ SUSPICIOUS                             │
│ (Needs manager verification)           │
│                                         │
│ ─ EVIDENCE ─                          │
│ 1. SIEM query: john's DB access hist │
│    Result: Only today's access        │
│    (Screenshot attached: evidence-1)  │
│                                         │
│ 2. AD record check: john's groups     │
│    Result: No DB_access group         │
│    (Screenshot attached: evidence-2)  │
│                                         │
│ 3. Ticket search: "john db access"    │
│    Result: No approval ticket found   │
│    (Jira search: evidence-3)          │
│                                         │
│ 4. Email to manager:                  │
│    "Did you approve DB access for     │
│    john today?"                        │
│    Status: Awaiting response          │
│                                         │
│ ─ ANALYSIS ─                          │
│ Normal: Business hours, office IP     │
│ Unusual: First database access        │
│ Risky: Accessing sensitive tables     │
│ Concerning: No authorization found    │
│                                         │
│ ─ RECOMMENDATION ─                    │
│ 1. Contact john's manager             │
│    Question: Was this access approved?│
│                                         │
│ 2. If YES (approved):                 │
│    - Close ticket (BENIGN)           │
│    - Create access request (for docs) │
│    - Add john to DB_access group      │
│                                         │
│ 3. If NO (not approved):              │
│    - ESCALATE to L2 (potential breach)│
│    - Flag: Unauthorized data access  │
│    - Check: What data was queried?    │
│                                         │
│ ─ PLAYBOOK USED ─                    │
│ Playbook: "Unauthorized DB Access"    │
│ Reference: PB-0045                     │
│                                         │
│ ─ NEXT STEPS ─                       │
│ [ ] Awaiting manager response         │
│ [ ] If approved: Close with docs      │
│ [ ] If denied: Escalate to L2        │
│                                         │
│ ─ ATTACHMENTS ─                      │
│ 1. SIEM-timeline.png (DB access log) │
│ 2. AD-record.png (john's groups)      │
│ 3. Jira-search.txt (no tickets found) │
│ 4. Email-to-manager.txt (pending)    │
│                                         │
└─────────────────────────────────────────┘
```

---

## Evidence Collection

### What Evidence to Attach:

```
Screenshots:
├─ SIEM timeline (with alert details)
├─ User AD/identity record
├─ System information
├─ Previous activity (showing baseline)
└─ Any unusual patterns

Log exports:
├─ Raw event data (CSV/JSON)
├─ Timeline data
├─ Query results
└─ Correlation data

Documentation:
├─ Ticket search results (no approval)
├─ Email conversations
├─ Calendar information
├─ HR/employment data

External lookups:
├─ TI reputation (VirusTotal, etc)
├─ IP geolocation
├─ Domain information
└─ Hash analysis

Naming convention:
├─ evidence-1-siem-timeline.png
├─ evidence-2-ad-record.png
├─ evidence-3-ti-lookup.txt
└─ Clear, sequential naming
```

### Screenshot Best Practices:

```
DO:
├─ Include timestamp/date visible
├─ Show relevant data (not whole screen)
├─ Highlight key information
├─ Clear, readable (good resolution)
├─ Include data source (SIEM, AD, etc)

DON'T:
├─ Include irrelevant information
├─ Leave out context
├─ Blur important data
├─ Take screenshots of entire screen
├─ Forget to name/label them
```

---

## Summary Writing

### Clear vs Unclear Summaries:

```
UNCLEAR:
"Suspicious alert detected. Possible threat.
 Need investigation."

Problem: Doesn't say WHAT is suspicious
         Doesn't explain WHY
         No specifics

CLEAR:
"User john.doe (Finance department) accessed
 production_database and queried financial_transactions
 table. First-time database access with no approval
 ticket found. Requires manager verification to
 determine if legitimate or unauthorized."

Better: Specific what happened
        Explains why concerning
        Clear action needed

EVEN BETTER:
"SUSPICIOUS: Unauthorized DB Access

Alert: User john.doe accessed production_database
Action: Queried financial_transactions (SELECT, ~50k rows)
Timing: 14:30 IST (business hours)
Issue: First-time access, no approval ticket, Finance role
       doesn't typically require DB access
Evidence: SIEM shows 0 prior DB access, AD shows no DB
          permission group, Jira has no access request

Verdict: SUSPICIOUS (needs manager verification)
Next: Contact manager; if approved → BENIGN, 
      if denied → ESCALATE as potential breach"

Best: Concise but complete
      All key info in first paragraph
      Verdict clear
      Action clear
```

---

## Real Reporting Examples

### **Example 1: Close Report (False Positive)**

```
Alert: "Brute Force Attack"

Ticket Report:
─────────────
ALERT: brute_force_50_failures_5min

SUMMARY:
Service account backup_automation attempted
database login 50 times in 5 minutes. Pattern
typical of automation retry behavior.

WHO: backup_automation (service account, infrastructure team)
WHAT: Failed login attempts (password auth)
WHEN: 03:00-03:05 IST (scheduled backup window)
WHERE: Database server, internal network
WHY: Service account using old credentials after
     password policy reset. Script not updated.

VERDICT: FALSE_POSITIVE

EVIDENCE:
1. Account type: Service account (not human)
   Evidence-1: AD-service-account.png
   
2. Pattern timing: Every night at 03:00
   Evidence-2: SIEM-6-month-history.png
   
3. Known process: Backup job scheduled
   Evidence-3: IT-ticket-12345-backup-schedule.txt
   
4. Success despite failures: Backup completes
   Evidence-4: Backup-completion-log.png

ANALYSIS:
- Automation pattern: 50 failures then process continues
- Timing: Consistent schedule for 6 months
- No security risk: Service account, no data access attempts
- No escalation: Legitimate operational process

RECOMMENDATION:
1. Close ticket as FALSE_POSITIVE
2. Document as known FP (update alert rule)
3. Note for L2: Consider suppressing similar alerts
4. Action: Script needs credential update
   (not security emergency, routine maintenance)

PLAYBOOK: "Failed Login Attempts" (PB-0012)
REFERENCE: False Positive - Service Account Retry
STATUS: CLOSED - FP

Time spent: 10 minutes
─────────────
```

### **Example 2: Escalation Report (True Positive)**

```
Alert: "Successful login after brute force"

Ticket Report:
─────────────
ALERT: brute_force_with_success

SUMMARY:
External IP attempted login 50+ times, 
followed by successful login. Account is
high-privilege admin account. Clear attack
pattern indicating possible account compromise.

WHO: admin@company.com (IT admin, privilege level: ADMIN)
WHAT: 50 failed + 1 successful login
WHEN: 09:30-09:45 IST (business hours, unexpected for admin)
WHERE: External IP 203.0.113.50, targeting domain controller
WHY: Pattern matches credential attack. Success after
     distributed attempts indicates credential guessing
     success or leaked credentials.

VERDICT: TRUE_POSITIVE (ESCALATE IMMEDIATELY)

EVIDENCE:
1. Failed login sequence
   Evidence-1: SIEM-brute-force-timeline.png
   Count: 52 failures in 15 minutes
   
2. Successful login after
   Evidence-2: SIEM-successful-login-event.png
   Time: 09:45:23 IST (after failures)
   
3. Source IP reputation
   Evidence-3: VirusTotal-IP-lookup.txt
   Verdict: Known attacker infrastructure
   
4. Admin account privileges
   Evidence-4: AD-admin-account.png
   Groups: Domain Admin, Enterprise Admin
   Impact: CRITICAL if compromised

5. Post-login activity
   Evidence-5: SIEM-admin-activity-after.png
   Actions: File access, group modifications
   Risk: Possible escalation/lateral movement

ANALYSIS:
- Attack pattern: Classic brute force then success
- Threat level: CRITICAL (admin account)
- Compromise confirmed: Yes (successful login from external)
- Post-compromise actions: Suspicious activity detected
- Impact: Full domain admin access possible

IMMEDIATE ACTIONS TAKEN:
- None (escalation only)

RECOMMENDATION FOR L2/IR:
1. IMMEDIATE: Reset admin@company.com password
2. URGENT: Audit admin account activity since 09:45
3. URGENT: Check for data access/exfiltration
4. CRITICAL: Investigate group/permission changes
5. Monitor: For lateral movement indicators
6. Contact: Admin user to verify legitimate access

PLAYBOOK: "Brute Force Success" (PB-0008)
REFERENCE: Possible Admin Account Compromise
STATUS: ESCALATED to L2_analyst_2 + IR_team

Confidence: HIGH (multiple indicators)
Time spent: 12 minutes
Action: IMMEDIATE ESCALATION REQUIRED
─────────────
```

---

## Communication Tips

### Escalation Email:

```
TO: L2_analyst_2, ir_team@company.com
SUBJECT: ESCALATION - Alert #456 - Admin Account 
         Possible Compromise

Hi team,

Escalating alert #456 with HIGH CONFIDENCE for 
immediate investigation and action.

SUMMARY:
Admin account (admin@company.com) compromised via 
brute force attack from external IP. Successful login 
detected after 50+ failed attempts. Post-login activity 
shows suspicious group modifications.

IMMEDIATE RISK:
- Full domain admin access possible
- Data access: Unknown extent
- Lateral movement: Possible

RECOMMENDED IMMEDIATE ACTIONS:
1. Reset admin password NOW
2. Audit recent activity on admin account
3. Check for data access/exfiltration
4. Investigate permission/group changes

EVIDENCE ATTACHED:
- Alert ticket #456 (see below)
- SIEM timeline (screenshot)
- IP reputation lookup
- Post-login activity log

TICKET: #456
TIME ESCALATED: 14:35 IST
L1 ANALYST: L1_analyst_1

Please see ticket for full details and evidence.

Thanks,
L1_analyst_1

═══════════════════════════════════════════════
TICKET DETAILS:
[Full ticket content here...]
═══════════════════════════════════════════════
```

---

## Common Reporting Mistakes

### ❌ **Mistake 1: Vague summary**

**সমস्या:**
```
Summary: "Alert triggered. Suspicious activity detected."
L2: "What alert? What activity? Be specific."
```

**সমाधان:**
```
Summary: "User john.doe accessed production_database
         for first time without approval. SUSPICIOUS."
```

---

### ❌ **Mistake 2: Missing evidence**

**समस्या:**
```
Ticket: "This looks like brute force."
No attachments, no SIEM output, no data.
L2: "How do you know? Where's the data?"
```

**समाधान:**
```
Attach: SIEM timeline showing 50 failures
        Screenshot of brute force pattern
        IP reputation lookup
        Activity summary
```

---

### ❌ **Mistake 3: No verdict**

**समस्या:**
```
Ticket: "Investigated alert. Possible threat."
No conclusion. L2: "Is it TP or FP? What's the verdict?"
```

**समाधान:**
```
VERDICT: FALSE_POSITIVE - Service account retry
         (or)
VERDICT: TRUE_POSITIVE - Escalate to IR immediately
```

---

### ❌ **Mistake 4: No recommendation**

**समस्या:**
```
Ticket: "Found something suspicious."
No action stated. L2: "Now what? What should I do?"
```

**समाधान:**
```
RECOMMENDATION:
1. Contact manager to verify
2. If denied: Escalate as breach
3. If approved: Update access group
```

---

### ❌ **Mistake 5: Rambling/unclear**

**समस्या:**
```
Ticket: [Long paragraph with mixed information,
         unclear conclusion, hard to parse]
```

**समाधान:**
```
Use Five Ws framework
Clear verdict first
Then supporting details
Structured bullet points
```

---

## Reporting Checklist

### **Every Alert Report Needs:**

- [ ] **WHO:** User/system identity with context
- [ ] **WHAT:** Specific alert and activity
- [ ] **WHEN:** Timestamp and time pattern
- [ ] **WHERE:** Location/network/system
- [ ] **WHY:** Evidence and analysis

### **Ticket Components:**

- [ ] Alert ID/name clear
- [ ] Summary concise but complete
- [ ] Verdict stated (TP/FP/Benign/Suspicious)
- [ ] Evidence attached (screenshots/logs)
- [ ] Analysis: Why you think so
- [ ] Recommendation: Next steps
- [ ] Playbook referenced
- [ ] Status: Open/Closed/Escalated

### **Quality Check:**

- [ ] Would L2 understand immediately?
- [ ] All evidence included?
- [ ] Verdict clear?
- [ ] Action clear?
- [ ] Professional tone?
- [ ] No typos/errors?
- [ ] Properly formatted?
- [ ] Timestamp accurate?

---

## Mini Quiz: Reporting

### **Question 1: Five Ws framework এর purpose কোনটি?**

A) Make report longer  
B) Ensure complete investigation documentation  
C) Impress management  
D) Follow company template

**Answer:** B) Ensure complete investigation documentation - WHO/WHAT/WHEN/WHERE/WHY = complete picture

---

### **Question 2: Alert summary এ কি থাকবে প্রথম line এ?**

A) All details mixed together  
B) Key facts: user, action, concern (concise)  
C) Your opinion on threat level  
D) Request for escalation

**Answer:** B) Key facts: user, action, concern (concise) - Summary = executive overview

---

### **Question 3: Evidence attach না করলে কি হয়?**

A) Nothing, L2 trust করবে  
B) L2 ask করবে "প্রমাণ কোথায়?"  
C) Ticket auto-close হয়  
D) No problem

**Answer:** B) L2 ask করবে "প্রমাণ কোথায়?" - Evidence essential for L2 verification

---

### **Question 4: Escalation এ verdict clear করা কেন important?**

A) Just decoration  
B) L2 জানতে পারে action urgent কিনা  
C) Mandatory form field  
D) No special reason

**Answer:** B) L2 জানতে পারে action urgent কিনা - Verdict = priority indicator

---

### **Question 5: Vague summary এর impact কোনটি?**

A) L1 সময় বাঁচায়  
B) L2 confused, back-and-forth needed, waste  
C) Better documentation  
D) No impact

**Answer:** B) L2 confused, back-and-forth needed, waste - Bad summary = rework

---

## সহজ ভাষায় সারসংক্ষেপ

**Alert Reporting = Documentation + Communication**

**Five Ws:**
- **WHO:** User/system identity with context
- **WHAT:** Alert and activity specifically
- **WHEN:** Timestamp and pattern
- **WHERE:** Location/network/system
- **WHY:** Evidence and analysis

**Ticket Structure:**
1. Summary (concise, key facts)
2. Five Ws breakdown
3. Verdict (TP/FP/Benign/Suspicious)
4. Evidence (attached)
5. Analysis (why you think so)
6. Recommendation (next steps)

**Evidence:**
- Screenshots (SIEM, AD, etc)
- Log exports
- Search results
- Clear naming/labeling

**Writing:**
- Specific not vague
- Complete not scattered
- Professional tone
- Structured format
- Clear verdict
- Clear action

**Mistakes to avoid:**
- Vague summary
- Missing evidence
- No verdict
- No recommendation
- Rambling/unclear writing

**Remember:**
- L2 reads dozens daily
- Make it easy to understand
- Clear verdict = fast action
- Good reporting = no rework

---

## Resources for Learning

**Your company:**
- Ticket template
- Reporting standards
- Escalation procedures
- Email templates

**Examples:**
- Previous tickets (anonymized)
- L2 feedback
- Manager guidance

---

**Module 18 Complete! ✅**

এখন আপনি জানেন:
- ✅ Alert reporting কেন critical
- ✅ Five Ws framework
- ✅ Alert ticket structure
- ✅ Evidence collection
- ✅ Summary writing
- ✅ Playbook references
- ✅ Escalation communication
- ✅ Real reporting examples
- ✅ Common reporting mistakes
- ✅ Reporting checklist

Progress: **18 of 28 modules complete (64%)**

---

<!-- nav-footer -->
## 🧭 Navigation

| | |
|---|---|
| **Previous** | [⬅️ Module 17: Common Alert Scenarios](../module-17-common-alert-scenarios/index.md) |
| **Next** | [Module 19: Alert Escalation ➡️](../module-19-alert-escalation/index.md) |
| **🏠 Course Home** | [STUDY_NOTES.md](../../STUDY_NOTES.md) |
