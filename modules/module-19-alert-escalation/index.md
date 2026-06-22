# Module 19: Alert Escalation

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- Escalation কি এবং কেন critical
- Escalation levels: L1 → L2, L2 → L3, L2 → IR
- Escalation criteria এবং decision tree
- When to escalate vs close alert
- Escalation procedures এবং protocols
- Information to include when escalating
- Red flags that force immediate escalation
- Real escalation scenarios
- Common escalation mistakes

---

## শুরুর আগে: একটি গল্প

নাজমা একজন L1 analyst। Alert investigate করেছে এবং এখন decision: close নাকি escalate?

Wrong escalation:
```
Alert: "Failed login attempt"
Decision: "Escalate to L2"
Result: L2 annoyed "This is obviously FP, 
        should've closed. Wasting my time."
```

Right escalation:
```
Alert: "Brute force + successful login"
Decision: "Escalate to L2"
Context: "50 failures then success, admin account,
         external IP, no approval ticket"
Result: L2 grateful "Good catch. Investigating now."
```

**Good escalation = Right cases at right time.**

---

## Escalation Overview

### What is Escalation?

```
Escalation = Sending alert + findings to higher expertise level

Levels:
├─ L1: Initial triage
├─ L2: Complex investigation
├─ L3: Advanced forensics/engineering
└─ IR: Incident response team

Escalation path:
└─ L1 → L2 (most common)
└─ L2 → L3 (complex technical)
└─ L2 → IR (incident confirmed)
```

### Why Escalate?

```
Escalate when:
├─ Confirmed threat detected
├─ Complex investigation needed
├─ Beyond L1 expertise
├─ Business impact possible
├─ Incident response needed
└─ Uncertain verdict (let L2 decide)

Don't escalate when:
├─ Obvious false positive
├─ Clear benign activity
├─ Legitimate authorization
├─ No red flags
└─ L1 can confidently close
```

---

## Escalation Decision Tree

### Should You Escalate?

```
START: Alert investigated

│
├─ CERTAIN it's false positive?
│  └─ NO → Continue
│  └─ YES → CLOSE (don't escalate)

├─ CERTAIN it's benign?
│  └─ NO → Continue
│  └─ YES → CLOSE (don't escalate)

├─ ANY red flags found?
│  └─ YES → ESCALATE (even if uncertain)
│  └─ NO → Continue

├─ Can you confidently determine verdict?
│  └─ YES → Close if FP/BENIGN
│  └─ NO → ESCALATE (let L2 decide)

├─ Business impact risk?
│  └─ HIGH → ESCALATE
│  └─ LOW → Continue to next check

├─ Critical system involved?
│  └─ YES → ESCALATE
│  └─ NO → Continue

└─ Beyond your expertise?
   └─ YES → ESCALATE
   └─ NO → Close if confident

RESULT:
├─ ESCALATE → Send to L2 with context
├─ CLOSE → Document and move on
└─ UNSURE → ESCALATE (better safe)
```

---

## Escalation Criteria

### Clear Escalation Cases

```
ALWAYS ESCALATE (No question):

❌ Confirmed malware
   └─ Hash consensus + execution

❌ Active data exfiltration
   └─ Sensitive data + external destination

❌ Successful compromise indicators
   └─ Brute force success + suspicious activity

❌ Privilege escalation
   └─ User gained unauthorized admin

❌ C2 communication
   └─ Known command & control connection

❌ Ransomware patterns
   └─ File encryption + C2 signals

❌ Critical system compromise
   └─ Any threat on Tier 1 system

❌ Incident response needed
   └─ Multiple systems affected

❌ Legal/compliance implications
   └─ Data breach, regulated data access

❌ Impossible to investigate at L1
   └─ Too complex or specialized
```

### Grey Area Cases

```
PROBABLY ESCALATE (Most cases):

⚠️ Suspicious but unclear
   └─ Has red flags, uncertain verdict

⚠️ Behavioral anomaly
   └─ Unusual pattern, no explanation

⚠️ Missing business context
   └─ No approval found, no ticket

⚠️ High-privilege account unusual activity
   └─ Admin with weird activity

⚠️ External access unusual target
   └─ External IP accessing sensitive system

⚠️ Multiple related events
   └─ Correlation suggests incident

⚠️ Known attack pattern
   └─ Matches documented threat

⚠️ User/system new or problematic
   └─ Contractor, contractor, or flag
```

### Don't Escalate (Obvious Cases)

```
✅ Obvious false positive
   └─ Backup script, automation, known pattern

✅ Approved activity with ticket
   └─ User requested, manager approved

✅ Expected operational activity
   └─ Scheduled maintenance, expected access

✅ User error (single attempt)
   └─ Wrong password, single click

✅ Benign with clear explanation
   └─ Travel approved, timezone difference

✅ Test/development activity
   └─ Lab environment, test data

✅ Known exceptions
   └─ Documented false positive
```

---

## Escalation Procedures

### What to Include When Escalating

```
ESCALATION PACKAGE MUST HAVE:

1. SUMMARY (2-3 sentences)
   └─ Key facts, risk level, recommendation

2. FULL FINDINGS
   └─ All investigation results

3. EVIDENCE
   └─ Screenshots, logs, exports

4. VERDICT & REASONING
   └─ Why you think it's TP/SUSPICIOUS

5. WHAT YOU CHECKED
   └─ What investigation steps taken

6. WHAT YOU COULDN'T DETERMINE
   └─ What L2 needs to find out

7. RECOMMENDED ACTIONS
   └─ What should L2 do next

8. URGENCY LEVEL
   └─ IMMEDIATE, URGENT, NORMAL
```

### Escalation Protocol

```
STEP 1: Prepare complete ticket
├─ All Five Ws documented
├─ Evidence attached
├─ Verdict stated
└─ Recommendation clear

STEP 2: Assign to appropriate person
├─ Critical case → On-call L2 or IR
├─ Complex case → Subject-matter expert
├─ Standard case → Next available L2

STEP 3: Set escalation priority
├─ IMMEDIATE: Confirmed active threat
├─ URGENT: High-risk, needs quick action
├─ NORMAL: Needs investigation, less urgent

STEP 4: Send escalation notification
├─ Email with ticket link
├─ Highlight urgency
├─ Summarize key points
├─ Attach evidence

STEP 5: Update ticket status
├─ Mark: ESCALATED
├─ Set: Escalated_to field
├─ Set: Escalation_time timestamp
└─ Set: Priority level

STEP 6: Monitor escalation
├─ Check if L2 acknowledged
├─ If not acknowledged in SLA → Follow up
└─ Document follow-up attempts
```

---

## Escalation Levels

### **L1 → L2 Escalation**

```
When: Most escalations
Who: L1 escalates to L2

Triggers:
├─ Suspicious but uncertain
├─ Complex investigation needed
├─ Possible true positive
├─ Multiple red flags
├─ High-risk system involved
├─ Beyond L1 expertise

L2 will do:
├─ Deeper investigation
├─ Make final verdict
├─ Decide if incident
├─ Close or escalate further

Example:
└─ L1: "Unusual database access, 
         first time, no ticket"
└─ L2: Contacts manager, gets approval,
       closes as BENIGN
```

### **L2 → L3 Escalation**

```
When: Complex technical issues
Who: L2 escalates to L3/Engineer

Triggers:
├─ Malware analysis needed
├─ Forensics needed
├─ Tool/system expertise needed
├─ Automation/scripting required
├─ Detection rule development

L3 will do:
├─ Deep technical analysis
├─ Develop detection rules
├─ Malware reverse engineering
├─ System forensics
├─ Tool customization

Example:
└─ L2: "Malware variant unknown, 
        need behavior analysis"
└─ L3: Sandbox analysis, reverse
       engineering, detection rule
```

### **L2 → Incident Response**

```
When: Confirmed incident
Who: L2 escalates to IR team

Triggers:
├─ Confirmed compromise
├─ Active threat indicators
├─ Data breach suspected
├─ Malware execution confirmed
├─ Multiple systems affected
├─ Immediate containment needed

IR will do:
├─ Contain threat
├─ Preserve evidence
├─ Forensic investigation
├─ Eradication
├─ Communication/notification
├─ Post-incident analysis

Example:
└─ L2: "Admin account compromised,
        C2 connections, data access"
└─ IR: Full incident response,
       system isolation, forensics
```

---

## Red Flags for Immediate Escalation

### No-Question Escalation Signals

```
🚨 IMMEDIATE ESCALATION (Don't wait):

1. Confirmed malware execution
   └─ Hash match + behavior confirmation

2. C2 communication detected
   └─ Known C2 IP/domain connection

3. Data exfiltration in progress
   └─ Large transfer to external

4. Privilege escalation successful
   └─ User gained admin rights

5. Critical system compromise
   └─ Tier 1 system access by attacker

6. Ransomware indicators
   └─ File encryption + C2 + network scan

7. Credential compromise
   └─ User entered creds to phishing
   └─ Or admin account brute force success

8. Multiple attack indicators
   └─ Brute force + malware + exfil together

9. Business impact imminent
   └─ Active threat to critical operation

10. Impossible to safely investigate
    └─ Risk of triggering malware
    └─ Risk of evidence destruction
```

---

## Real Escalation Scenarios

### **Scenario 1: Uncertain, Better Safe**

```
L1 Investigation:
├─ Alert: "User accessing admin files"
├─ Finding: Not in admin group
├─ But: Could be delegated access
├─ Uncertain: Can't confirm legitimate

Decision: ESCALATE
Reason: Gray area, not obvious FP
        L2 can contact manager
        Better to escalate uncertain

Escalation:
"User john.doe accessed admin_files.
 User is not in admin group. Cannot find
 approval ticket. Unclear if delegated
 access. Escalating for verification."

L2 follows up:
"Manager says yes, delegated for this
 project. CLOSE as BENIGN."
```

### **Scenario 2: Red Flag, Immediate**

```
L1 Investigation:
├─ Alert: "Brute force + success"
├─ Finding: 50 failures, 1 success
├─ From: External IP
├─ Target: Admin account
├─ Post-activity: Suspicious file access

Decision: ESCALATE IMMEDIATELY
Reason: Confirmed attack pattern
        Admin account compromised
        Active threat

Escalation:
"URGENT ESCALATION - Account Compromise

Brute force attack succeeded on admin account.
External IP, 50 failures + 1 success.
Post-login: Suspicious file access detected.

IMMEDIATE ACTIONS NEEDED:
1. Reset admin password NOW
2. Audit account activity
3. Check data access extent
4. Investigate file modifications"

L2/IR follows up:
"Activated incident response.
 Isolating systems. Full forensics."
```

### **Scenario 3: Obvious FP, Don't Escalate**

```
L1 Investigation:
├─ Alert: "Failed login attempts"
├─ Finding: Service account, nightly
├─ Pattern: 50 failures every night for 6 months
├─ Context: Backup script known
├─ Ticket: IT-12345 "Backup automation"

Decision: CLOSE (don't escalate)
Reason: Obvious false positive
        Known automation
        No security risk
        Escalating would waste L2 time

Ticket:
"FALSE_POSITIVE - Service Account Retry

Service account backup_automation
attempting login 50x nightly. Known
pattern, automation scheduled, no
security risk. Closing as FP.

Note for team: Consider suppressing
similar alerts in future."

Result: Clean close, no unnecessary escalation
```

---

## Common Escalation Mistakes

### ❌ **Mistake 1: Over-escalating**

**সমস्या:**
```
Alert: "Failed login (user typo)"
Escalation: "URGENT - Possible brute force"
L2: "This is obvious FP, stop wasting time"
Result: L2 frustrated, L1 loses credibility
```

**সমाधान:**
```
Only escalate if:
├─ Red flags present
├─ Uncertain verdict
├─ Complex investigation needed
├─ NOT obvious FP/benign
```

---

### ❌ **Mistake 2: Under-escalating**

**समस्या:**
```
Alert: "Malware detected"
L1 decision: "Probably FP, closing"
Reality: Confirmed malware, spread to 10 systems
Result: Incident missed, damage spreads
```

**समाधान:**
```
Escalate when uncertain
Don't close malware/compromise
If doubt → escalate
```

---

### ❌ **Mistake 3: Incomplete escalation**

**समस्या:**
```
Escalation: "Check this alert #456"
No context, no evidence, no findings
L2: "What did you find? Where's the evidence?"
Result: Back-and-forth delay
```

**समाधान:**
```
Always include:
├─ Complete findings
├─ Evidence attached
├─ Verdict & reasoning
├─ Recommended actions
```

---

### ❌ **Mistake 4: Wrong urgency level**

**समस्या:**
```
Escalation: "Possible account compromise"
Priority: NORMAL (low priority)
Reality: Active data theft happening NOW
Result: Delayed response, more damage
```

**समाधान:**
```
Match urgency to threat:
├─ IMMEDIATE: Active threat
├─ URGENT: High-risk, needs fast action
├─ NORMAL: Can wait for next person
```

---

### ❌ **Mistake 5: No follow-up**

**समस्या:**
```
Escalate alert to L2
Never check if acknowledged
Days pass, no response
Alert forgotten
```

**समाधान:**
```
After escalation:
├─ Check acknowledgment
├─ Follow up if no response (SLA)
├─ Document follow-up
```

---

## Escalation Checklist

### **Before Escalating**

- [ ] Investigation complete (or L2 needs to finish)
- [ ] Verdict clear (or uncertain, needs escalation)
- [ ] Evidence collected
- [ ] Five Ws documented
- [ ] Recommendations clear

### **Escalation Package**

- [ ] Ticket summary (2-3 sentences)
- [ ] Full investigation findings
- [ ] Evidence attached (screenshots, logs)
- [ ] Verdict clearly stated
- [ ] Reasoning explained
- [ ] Recommended actions
- [ ] Urgency level set
- [ ] Assigned to right person

### **Escalation Notification**

- [ ] Email sent with ticket link
- [ ] Urgency highlighted
- [ ] Key points summarized
- [ ] Evidence highlighted

### **Follow-up**

- [ ] Check L2 acknowledged
- [ ] If not acknowledged in SLA: Follow up
- [ ] Monitor escalation progress
- [ ] Document any issues

### **When NOT to Escalate**

- [ ] Obvious false positive
- [ ] Clear benign activity
- [ ] Legitimate approved access
- [ ] You're confident in verdict
- [ ] No red flags present

---

## Mini Quiz: Escalation

### **Question 1: Escalation primary reason কোনটি?**

A) Get more people involved  
B) Send alert to someone else  
C) Complex cases need higher expertise  
D) Always escalate everything

**Answer:** C) Complex cases need higher expertise - Escalation = expertise match

---

### **Question 2: কখন NOT escalate করবেন?**

A) উদ্বিগ্ন থাকলে  
B) Obvious false positive + confident  
C) কিছু uncertain থাকলে  
D) সবসময় escalate করুন

**Answer:** B) Obvious false positive + confident - Don't waste L2 time on clear FP

---

### **Question 3: Escalation package এ কি NOT প্রয়োজন?**

A) Findings এবং evidence  
B) Your detailed technical analysis notes  
C) Verdict এবং reasoning  
D) Recommended actions

**Answer:** B) Your detailed technical analysis notes - Summary enough, not raw notes

---

### **Question 4: IMMEDIATE escalation কখন?**

A) সব escalation immediate  
B) Complex cases  
C) Confirmed active threat  
D) Uncertain cases

**Answer:** C) Confirmed active threat - IMMEDIATE = threat ongoing NOW

---

### **Question 5: Escalation after, কি করবেন?**

A) Nothing, alert done  
B) Monitor acknowledgment, follow up if needed  
C) Close ticket  
D) Escalate again

**Answer:** B) Monitor acknowledgment, follow up if needed - Ensure proper handoff

---

## সহজ ভাষায় সারসংক্ষেপ

**Escalation = Sending to higher expertise**

**Levels:**
- L1 → L2: Complex investigation
- L2 → L3: Technical expertise needed
- L2 → IR: Incident confirmed

**Escalate When:**
✅ Red flags found
✅ Uncertain verdict
✅ Complex case
✅ Critical system
✅ Possible incident

**Don't Escalate:**
❌ Obvious false positive
❌ Clear benign
❌ Legitimate approved
❌ You confident

**Escalation Package:**
- Summary (2-3 sentences)
- Findings (complete)
- Evidence (attached)
- Verdict (clear)
- Reasoning (why you think so)
- Actions (what L2 should do)

**Red Flags = Immediate:**
- Malware confirmed
- C2 communication
- Data exfiltration
- Compromise successful
- Privilege escalation

**Common Mistakes:**
- Over-escalate (waste L2)
- Under-escalate (miss threat)
- Incomplete escalation (confusion)
- Wrong urgency (slow response)
- No follow-up (forgotten)

**Remember:**
- Right case + right level = smooth handoff
- Uncertain = escalate (better safe)
- Clear FP = don't escalate
- Always include evidence
- Follow up on acknowledgment

---

## Resources for Learning

**Your company:**
- Escalation procedures
- Who to escalate to
- L2 contact list
- IR activation process
- SLA response times

**Guidelines:**
- Escalation criteria docs
- Red flags checklist
- Playbook escalation sections

---

**Module 19 Complete! ✅**

এখন আপনি জানেন:
- ✅ Escalation কি এবং কেন
- ✅ Escalation levels (L1→L2, L2→L3, L2→IR)
- ✅ Decision tree (escalate vs close)
- ✅ Escalation criteria
- ✅ What to include when escalating
- ✅ Escalation procedures
- ✅ Red flags requiring immediate escalation
- ✅ Real escalation scenarios
- ✅ Common escalation mistakes
- ✅ Escalation checklist

Progress: **19 of 28 modules complete (68%)**

🎉 **Over 2/3 through the course!** 🎉

