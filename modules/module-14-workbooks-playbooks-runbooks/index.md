# Module 14: SOC Workbooks, Playbooks, Runbooks, and Workflows

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- Workbook কি এবং কিভাবে ব্যবহার করতে হয়
- Playbook কি এবং structure
- Runbook কি এবং practical steps
- Workflow কি এবং automation
- তাদের মধ্যে পার্থক্য
- কিভাবে L1 এই documents use করে
- কিভাবে L1 contribute করে
- খারাপ documentation signs
- Real SOC examples

---

## শুরুর আগে: একটি গল্প

রিনা একজন নতুন SOC L1। প্রথম দিন alert আসে: "Phishing email detected".

Without documentation:
```
09:00 - Alert দেখলো
09:05 - "What do I do?"
09:10 - Random google search
09:20 - Wrong steps নিলো
09:30 - False decision
09:45 - Manager correction needed
```

With documentation (Playbook):
```
09:00 - Alert দেখলো
09:02 - Open playbook: "Phishing Email Response"
09:03 - Follow steps:
       Step 1: Verify email received by user
       Step 2: Check URL reputation
       Step 3: Scan attachment hash
       Step 4: Decision tree...
09:15 - Correct investigation
09:20 - Confident decision
```

**Good documentation = Faster, consistent decisions.**

---

## Workbook, Playbook, Runbook, Workflow: পার্থক্য

### Quick Comparison:

```
┌───────────────┬──────────────────┬─────────────────────┐
│ Document Type │ Purpose          │ Level of Detail     │
├───────────────┼──────────────────┼─────────────────────┤
│ WORKBOOK      │ Investigation    │ High-level process  │
│               │ framework        │ with decision trees │
├───────────────┼──────────────────┼─────────────────────┤
│ PLAYBOOK      │ Response steps   │ Step-by-step        │
│               │ for alerts       │ procedures          │
├───────────────┼──────────────────┼─────────────────────┤
│ RUNBOOK       │ Technical        │ Commands,           │
│               │ execution        │ exact steps         │
├───────────────┼──────────────────┼─────────────────────┤
│ WORKFLOW      │ Automation       │ Automated sequence  │
│               │ sequence         │ (SOAR)              │
└───────────────┴──────────────────┴─────────────────────┘
```

---

## 1. WORKBOOK

### What is it:

**Workbook = Investigation framework for specific alert type.**

```
Contains:
├─ Alert description
├─ Investigation phases
├─ Data enrichment steps
├─ Decision trees
├─ Common findings
├─ Escalation criteria
└─ Documentation template
```

### Purpose:

```
Workbook tells L1:
├─ What is this alert about?
├─ What data should I gather?
├─ What questions should I ask?
├─ How do I make decisions?
├─ When do I escalate?
└─ How do I document findings?
```

### Real Workbook Example:

```
┌─────────────────────────────────────────────────┐
│ WORKBOOK: Brute Force Attack Investigation     │
├─────────────────────────────────────────────────┤
│                                                  │
│ ALERT: Multiple failed login attempts          │
│                                                  │
│ PHASE 1: INITIAL ASSESSMENT (2 min)           │
│ ├─ Alert received: timestamp
│ ├─ Alert properties: user, system, count
│ └─ Severity: assess from count/time
│
│ PHASE 2: USER CONTEXT (2 min)                 │
│ ├─ User legitimate? (Check AD, HR)
│ ├─ User history: previous login attempts?
│ ├─ User on vacation? (Calendar check)
│ ├─ User traveling? (Approved travel?)
│ └─ User profile: access level appropriate?
│
│ PHASE 3: ACTIVITY ANALYSIS (3 min)           │
│ ├─ Source IP reputation: (TI check)
│ │  └─ Malicious? VPN? Residential?
│ ├─ Login pattern: single source or multiple?
│ ├─ Any successful login after failures?
│ │  └─ Yes: Account compromise risk
│ │  └─ No: Still just attack attempt
│ └─ Timeline: cluster or spread out?
│
│ PHASE 4: SYSTEM ASSESSMENT (2 min)           │
│ ├─ Target system: critical or test?
│ ├─ Target: internet-facing or internal?
│ ├─ Data: what sensitive data on system?
│ └─ Current status: any access achieved?
│
│ DECISION TREE:                                 │
│
│ Q1: Successful login after failures?
│ ├─ YES → Q2
│ └─ NO → Q3
│
│ Q2: User on approved travel?
│ ├─ YES → FALSE_POSITIVE (travel expected)
│ └─ NO → TRUE_POSITIVE (account compromise)
│
│ Q3: Source IP malicious?
│ ├─ YES → TRUE_POSITIVE (attack attempt)
│ └─ NO → Q4
│
│ Q4: Internal target?
│ ├─ YES → SUSPICIOUS (investigation deeper)
│ └─ NO → Evaluate criticality → verdict
│
│ ESCALATION CRITERIA:                          │
│ ├─ Confirmed compromise: ESCALATE
│ ├─ Critical system attacked: ESCALATE
│ ├─ Suspicious pattern: ESCALATE
│ └─ Clear false positive: CLOSE
│
│ COMMON FINDINGS:                              │
│ ├─ Backup script old password
│ ├─ User typo'd password multiple times
│ ├─ Unauthorized access attempt
│ ├─ Bot testing common credentials
│ └─ Misconfigured app retrying
│
│ DOCUMENTATION TEMPLATE:                       │
│ ├─ User verified: [Y/N]
│ ├─ Source IP: [safe/suspicious]
│ ├─ Success achieved: [Y/N]
│ ├─ System risk: [high/medium/low]
│ ├─ Investigation time: __ minutes
│ └─ Final verdict: [TP/FP/BENIGN/SUSPICIOUS]
│
└─────────────────────────────────────────────────┘
```

### How L1 Uses Workbook:

```
Alert comes in:
├─ Check: What type of alert?
├─ Find: Matching workbook
├─ Open: Workbook document
├─ Follow: Investigation phases
├─ Answer: Questions in workbook
├─ Use: Decision tree
└─ Reach: Confident verdict
```

---

## 2. PLAYBOOK

### What is it:

**Playbook = Step-by-step response procedure for alert.**

```
Contains:
├─ Alert details
├─ Numbered steps (1, 2, 3...)
├─ Exact procedures
├─ What to check
├─ What tools to use
├─ What to do for each finding
└─ Escalation instructions
```

### Purpose:

```
Playbook tells L1:
├─ Do step 1 first
├─ Then do step 2
├─ If finding X: do action A
├─ If finding Y: do action B
├─ Escalate at this point
└─ Close at this point
```

### Real Playbook Example:

```
┌─────────────────────────────────────────────────┐
│ PLAYBOOK: Phishing Email Response              │
├─────────────────────────────────────────────────┤
│                                                  │
│ STEP 1: Verify Email Reception (1 min)        │
│ ├─ Check: Did user receive email?
│ │  └─ Search email logs for user
│ ├─ If YES: Continue
│ └─ If NO: CLOSE (alert false positive)
│
│ STEP 2: Extract Email Details (1 min)         │
│ ├─ Sender address: _____________
│ ├─ Subject line: _____________
│ ├─ Timestamp: _____________
│ ├─ Recipient count: _____________
│ └─ Attachment: Yes / No
│
│ STEP 3: Check Sender Legitimacy (1 min)       │
│ ├─ Lookup domain: (WHOIS check)
│ ├─ Check: SPF/DKIM/DMARC (TI)
│ ├─ If authenticated: BENIGN (legit email)
│ └─ If NOT authenticated: PHISHING (spoofed)
│
│ STEP 4: Scan Attachment (1 min)               │
│ ├─ If no attachment: Skip to step 5
│ ├─ File type: _____________
│ ├─ File name: _____________
│ ├─ Hash: _____________
│ ├─ VirusTotal lookup:
│ │  ├─ If malware detected: STOP → escalate
│ │  ├─ If clean: Continue
│ │  └─ If unknown: Submit for analysis
│ └─ Document: Result
│
│ STEP 5: Check URL Links (1 min)               │
│ ├─ Extract URLs from email body
│ ├─ For each URL:
│ │  ├─ Check: Destination legitimate?
│ │  ├─ Check: URL TI reputation
│ │  ├─ If malicious: PHISHING → escalate
│ │  └─ If clean: Continue
│ └─ Document: URLs checked
│
│ STEP 6: User Action Assessment (1 min)        │
│ ├─ Question: Did user click link?
│ │  ├─ NO: Risk lower
│ │  └─ YES: Risk higher
│ ├─ Question: Did user download attachment?
│ │  ├─ NO: Risk lower
│ │  └─ YES: ESCALATE (possible infection)
│ ├─ Question: Did user enter credentials?
│ │  ├─ NO: Monitor account
│ │  └─ YES: ESCALATE (credential compromise)
│ └─ Document: User actions
│
│ STEP 7: Decision (1 min)                      │
│ ├─ Legitimate email? → CLOSE
│ ├─ Phishing, no user action? → CLOSE + educate
│ ├─ Phishing, user clicked? → ESCALATE
│ ├─ Phishing, user infected? → ESCALATE
│ └─ Unsure? → ESCALATE to L2
│
│ ESCALATION: If escalating
│ ├─ Document: All findings
│ ├─ Attach: Evidence (URLs, hashes)
│ ├─ Send: To L2/IR with complete context
│ └─ Note: What user may have done
│
│ TOOLS USED:
│ ├─ Email logs: Check user receipt
│ ├─ WHOIS: Domain legitimacy
│ ├─ VirusTotal: URL/attachment reputation
│ ├─ TI platform: Domain/IP reputation
│ └─ EDR: Check user device for malware
│
│ COMMON OUTCOMES:
│ ├─ FP: Legitimate email (looks phishing)
│ ├─ FP: User didn't interact
│ ├─ TP: Phishing caught before user click
│ ├─ TP: User interacted, escalate to IR
│ └─ Unsure: Escalate for L2 judgment
│
│ TIME TARGET: 8-10 minutes per email
│
└─────────────────────────────────────────────────┘
```

### How L1 Uses Playbook:

```
Alert comes in:
├─ Open: Alert playbook
├─ Do: Step 1
├─ Do: Step 2
├─ Answer: Questions
├─ If finding X: Do action A
├─ Continue: Through all steps
├─ Reach: Verdict by end
└─ Close or escalate
```

---

## 3. RUNBOOK

### What is it:

**Runbook = Technical procedures for specific tasks.**

```
Contains:
├─ Exact commands
├─ Tool usage
├─ Copy-paste steps
├─ Screenshots
├─ Expected output
├─ Troubleshooting
└─ Technical details
```

### Purpose:

```
Runbook tells L1/L2/L3:
├─ Use this tool
├─ Type this command
├─ Click this button
├─ Expected result
├─ If error: Do this
└─ Common issues: Fix this way
```

### Real Runbook Example:

```
┌─────────────────────────────────────────────────┐
│ RUNBOOK: Disable AD Account (Incident Response)│
├─────────────────────────────────────────────────┤
│                                                  │
│ PURPOSE: Quickly disable compromised account   │
│                                                  │
│ PREREQUISITES:                                  │
│ ├─ Domain admin credentials
│ ├─ Access to Active Directory
│ ├─ Understanding of account management
│ └─ Confirmation from manager/L2
│
│ STEP 1: Open Active Directory Users & Comp.   │
│ ├─ Windows: Press Windows+R
│ ├─ Type: dsa.msc
│ ├─ Press: Enter
│ └─ Result: Opens AD Users & Computers console
│
│ STEP 2: Locate User Account                   │
│ ├─ In console: Navigate to your OU
│ ├─ OR: Search function (Ctrl+F)
│ ├─ Type: Username to find
│ ├─ Result: Should show 1 user account
│ └─ If multiple: Confirm full name matches
│
│ STEP 3: Disable Account                       │
│ ├─ Right-click: User account
│ ├─ Select: Properties
│ ├─ Go to: Account tab
│ ├─ Check: "Account is disabled" checkbox
│ ├─ Click: Apply
│ ├─ Click: OK
│ └─ Result: Account now disabled
│
│ STEP 4: Verify Disable                        │
│ ├─ In AD console: Account shows ✗ symbol
│ ├─ Verify: User cannot login
│ ├─ Test: Try login (should fail)
│ └─ Confirm: Message "Account disabled"
│
│ STEP 5: Reset Password                        │
│ ├─ Right-click: Disabled account
│ ├─ Select: Reset Password
│ ├─ New password: Generate random
│ ├─ Copy: Temp password
│ ├─ Click: OK
│ └─ Store: In secure location
│
│ STEP 6: Session Logout                        │
│ ├─ Command: quser (list active sessions)
│ ├─ If user logged in: Sessions shown
│ ├─ Command: logoff [session_id] /server:...
│ └─ Force: User offline immediately
│
│ STEP 7: Document Action                       │
│ ├─ Time: Disable timestamp
│ ├─ Reason: Why disabled
│ ├─ Who: Your name
│ ├─ Evidence: Screenshots
│ └─ Ticket: Link to incident
│
│ TROUBLESHOOTING:                               │
│
│ Q: Account won't disable (error)
│ A: ├─ Check: Admin permissions
│    └─ Retry: May need to refresh

│
│ Q: User still logged in after disable
│ A: ├─ Use: logoff command to force
│    └─ Verify: Session actually disconnects
│
│ Q: Can't find account
│ A: ├─ Check: Correct OU
│    ├─ Try: Search by email
│    └─ Confirm: User name spelling

│
│ ROLLBACK PROCEDURE (if accidental):          │
│ ├─ Reopen: AD Users & Computers
│ ├─ Right-click: Account
│ ├─ Uncheck: "Account is disabled"
│ ├─ Click: OK
│ └─ Account: Re-enabled
│
│ RISK: High - Disables user access immediately
│ TIME: 2 minutes
│ APPROVAL: Required before running
│
└─────────────────────────────────────────────────┘
```

### How L1 Uses Runbook:

```
Manager asks: "Disable this account"
├─ Get runbook: "Disable AD Account"
├─ Follow: Step 1, 2, 3...
├─ Type: Exact commands shown
├─ Verify: Expected output
├─ Done: Account disabled
└─ Document: What you did
```

---

## 4. WORKFLOW

### What is it:

**Workflow = Automated sequence (SOAR platform).**

```
Contains:
├─ Trigger: Alert comes in
├─ Automation steps: Automatic actions
├─ Conditional logic: If X then Y
├─ Integration: APIs between tools
├─ No manual steps: All automatic
└─ Result: Enriched alert or action
```

### Purpose:

```
Workflow automates:
├─ Repetitive tasks
├─ Data gathering
├─ Alert enrichment
├─ Escalation routing
├─ Threat hunting
└─ Response actions
```

### Real Workflow Example:

```
WORKFLOW: Phishing Email Auto-Enrichment

TRIGGER: Phishing alert received

STEP 1 (Automatic): Extract email details
├─ Get: Sender, subject, URLs, attachments
└─ Store: In workflow variables

STEP 2 (Automatic): Check sender reputation
├─ Query: Threat Intel API
├─ Get: Sender reputation score
├─ Decision: Known sender or new?

STEP 3 (Automatic): Scan attachment
├─ If attachment exists:
│  ├─ Extract: File hash
│  ├─ Query: VirusTotal API
│  ├─ Get: Vendor detections
│  └─ Decision: Malware or clean?
└─ If no attachment: Skip this step

STEP 4 (Automatic): Check URLs
├─ For each URL:
│  ├─ Extract: Domain
│  ├─ Query: URL reputation
│  └─ Decision: Phishing or clean?

STEP 5 (Automatic): Enrich alert
├─ Add: All findings to alert
├─ Add: Reputation scores
├─ Add: Risk assessment
└─ Update: Alert in SIEM

STEP 6 (Automatic): Route escalation
├─ If malware found: Send to IR (critical)
├─ If phishing confirmed: Send to L2 (high)
├─ If unsure: Send to L2 (medium)
└─ If false positive: Auto-close

RESULT: L1 analyst sees enriched alert with:
├─ Complete reputation data
├─ Automatic risk score
├─ Recommended action
└─ Ready for quick triage

TIME SAVED: 5 minutes per alert
AUTOMATION: 95% of investigation
ANALYST: Just confirms and closes
```

---

## L1 Contribution to Documentation

### How L1 Helps:

```
Workbooks, playbooks, runbooks are LIVING documents.
L1 updates them constantly:

DURING INVESTIGATION:
├─ Find missing step?
│  └─ Note: "Need to add TI lookup here"
├─ Find unclear instruction?
│  └─ Note: "Step 3 unclear, should specify..."
├─ Find common finding?
│  └─ Note: "See this false positive often"
└─ Find better way?
   └─ Note: "Faster if we check X first"

AFTER INVESTIGATION:
├─ Write findings in ticket
├─ L2/Manager reviews
├─ Update: Documentation if needed
└─ Result: Better playbook

EXAMPLES:

Investigation 1:
├─ Followed playbook
├─ Step 5 missing info
├─ Added: "Check EDR logs for process"
└─ Playbook updated

Investigation 2:
├─ Playbook said "Check TI"
├─ But didn't specify which platform
├─ Added: "Use VirusTotal first, then AbuseIPDB"
└─ Playbook improved

Investigation 3:
├─ Found: Alert often false positive (type X)
├─ Added: "Common FP: backup script"
├─ Playbook includes: Common findings now
└─ Future L1: Faster investigation

L1 ROLE in documentation:
├─ Use documents first
├─ Find issues/gaps
├─ Propose improvements
├─ Help team learn from investigations
└─ Make documentation better for next person
```

---

## Quality Signs: Good vs Bad Documentation

### ✅ Good Documentation:

```
├─ Clear steps (numbered, specific)
├─ Decision trees (clear logic)
├─ Examples (real examples included)
├─ Updated (recently reviewed)
├─ Tested (known to work)
├─ Searchable (easy to find)
├─ Screenshots (visual aids)
├─ Troubleshooting (common issues addressed)
└─ Versioning (track changes)
```

### ❌ Bad Documentation:

```
├─ Vague steps ("then investigate")
├─ No decision framework
├─ Generic examples
├─ Outdated (last updated 2021)
├─ Never tested
├─ Hard to search
├─ No visuals
├─ No troubleshooting
└─ No version info
```

---

## Common Mistakes with Documentation

### ❌ **Mistake 1: Not using documentation**

**সমস्या:**
```
Playbook exists
But L1: Doesn't know about it
Result: Inconsistent investigations
```

**সমाधान:**
```
Learn: Where documents stored
Know: What playbooks exist
USE: For every investigation
```

---

### ❌ **Mistake 2: Following outdated playbook**

**समस्या:**
```
Playbook last updated 2021
But tools changed
Instructions now wrong
Result: Wasted time
```

**समाधान:**
```
Check: Last update date
Verify: Steps still valid
Report: If outdated
```

---

### ❌ **Mistake 3: Not updating playbooks**

**समस्या:**
```
Found better way to investigate
But: Don't tell anyone
Result: Others still slow way
```

**समाधান:**
```
Find issue: Document it
Propose fix: Talk to L2
Update: Together
Share: Improve team
```

---

### ❌ **Mistake 4: Over-documenting**

**समस्या:**
```
Playbook: 50 pages long
Nobody reads it
Result: Document unused
```

**सऴाधान:**
```
Keep: Short and focused
Use: Decision trees not paragraphs
Examples: Real, not hypothetical
Trim: Remove outdated sections
```

---

## Documentation Checklist

### **Before Starting Investigation**

- [ ] Alert type identified
- [ ] Workbook exists for this type?
- [ ] Playbook exists for this type?
- [ ] Playbook up-to-date? (check date)
- [ ] Runbook needed for technical steps?

### **During Investigation**

- [ ] Following playbook steps
- [ ] Finding gaps in documentation
- [ ] Noting missing information
- [ ] Tracking time spent
- [ ] Testing runbook if using

### **After Investigation**

- [ ] Documented findings in ticket
- [ ] Found improvements to playbook?
- [ ] Proposed updates to documentation?
- [ ] Time taken: Did playbook estimate match?
- [ ] Would playbook help L1 in future?

### **Documentation Maintenance**

- [ ] Playbooks reviewed quarterly
- [ ] Outdated content removed
- [ ] New patterns added to common findings
- [ ] Screenshots kept current
- [ ] Version history maintained

---

## Mini Quiz: Documentation

### **Question 1: Workbook vs Playbook - মূল পার্থক্য?**

A) একই জিনিস, different names  
B) Workbook: investigation framework, Playbook: step-by-step  
C) Playbook: investigation, Workbook: automation  
D) No difference

**Answer:** B) Workbook: investigation framework, Playbook: step-by-step - উভয় ভিন্ন উদ্দেশ্য

---

### **Question 2: Runbook এর primary purpose কোনটি?**

A) Decision making framework  
B) Alert investigation guide  
C) Technical procedure with exact commands  
D) Automation sequence

**Answer:** C) Technical procedure with exact commands - Runbook copy-paste steps

---

### **Question 3: কিভাবে L1 playbook improve করতে পারে?**

A) নিজে edit করুন  
B) Found issues নোট করুন, L2 সাথে discuss করুন  
C) যেমন আছে তেমন ব্যবহার করুন  
D) Ignore playbooks

**Answer:** B) Found issues নোট করুন, L2 সাথে discuss করুন - L1 observations valuable

---

### **Question 4: Workflow automation করে কি?**

A) Manual investigation steps  
B) Alert escalation decisions  
C) Repetitive data gathering tasks  
D) All of above

**Answer:** D) All of above - SOAR workflows automate multiple things

---

### **Question 5: Outdated playbook use করলে কি হবে?**

A) Still works fine  
B) May have wrong steps, wasted time  
C) Better than no playbook  
D) Check date first

**Answer:** B) May have wrong steps, wasted time - Always verify playbook current

---

## সহজ ভাষায় সারসংক্ষেপ

**4 Types of SOC Documentation:**

- **Workbook:** Investigation framework, decision trees
- **Playbook:** Step-by-step alert response procedures
- **Runbook:** Technical procedures with exact commands
- **Workflow:** Automated sequences (SOAR platform)

**Usage Pattern:**

1. Alert arrives
2. Find matching playbook
3. Follow steps
4. Use runbook for technical tasks
5. Workflow enriches data automatically
6. L1 makes decision
7. Close or escalate

**L1 Role:**

- Use documentation for every investigation
- Find gaps/issues
- Propose improvements
- Help update playbooks
- Make documentation better

**Quality:**

- ✅ Good: Clear, updated, tested, examples
- ❌ Bad: Vague, outdated, untested

**Remember:**

- Documentation is team resource
- Keep it updated
- Use it consistently
- Contribute improvements
- Share knowledge

---

## Resources for Learning

**Documentation platforms:**
- Confluence/Wiki
- GitHub/GitLab
- Google Docs
- Internal documentation system

**Examples:**
- Your company playbooks
- SANS resources
- Public security playbooks
- Industry templates

---

**Module 14 Complete! ✅**

এখন আপনি জানেন:
- ✅ Workbook কি এবং কখন use
- ✅ Playbook step-by-step procedures
- ✅ Runbook technical commands
- ✅ Workflow automation
- ✅ পার্থক্য: Workbook vs Playbook vs Runbook vs Workflow
- ✅ কিভাবে L1 documentation use করে
- ✅ কিভাবে L1 contribute করে
- ✅ Good vs Bad documentation signs
- ✅ Common documentation mistakes
- ✅ Documentation maintenance

Progress: **14 of 28 modules complete (50%)**

🎉 **HALFWAY THERE! 50% COMPLETE! 🎉**

---

<!-- nav-footer -->
## 🧭 Navigation

| | |
|---|---|
| **Previous** | [⬅️ Module 13: Network Diagrams](../module-13-network-diagrams/index.md) |
| **Next** | [Module 15: Enrichment Process ➡️](../module-15-enrichment-process/index.md) |
| **🏠 Course Home** | [STUDY_NOTES.md](../../STUDY_NOTES.md) |
