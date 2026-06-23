# Module 20: SOC Communication

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- Communication key stakeholders: L2, managers, IT, HR, users
- Email communication best practices
- Slack/messaging communication
- Escalation communication (already started in Module 19)
- Status update communication
- Incident notification communication
- Difficult conversations handling
- Cross-functional communication
- Real communication examples
- Common communication mistakes

---

## শুরুর আগে: একটি গল্প

রাজিব একজন L1 analyst তার দ্বিতীয় সপ্তাহে। Alert investigate করে escalate করবে L2 কে।

Poor communication:
```
Slack: "yo L2, check alert 456, 
        looks bad lol"
L2: "What alert? What's bad? 
     Be professional"
```

Good communication:
```
Email to L2_analyst_2:
Subject: ESCALATION - Alert #456 - 
         Suspicious DB Access

Escalating alert #456 for your investigation.

Summary: User john.doe accessed 
production_database without approval.
First-time access, no business justification.

Evidence: [Attached]
Recommendation: Verify with manager

Ticket: #456

Thanks,
L1_analyst_1
```

**Professional communication = Credibility + efficiency.**

---

## Communication Stakeholders

### Who You Communicate With:

```
TECHNICAL:
├─ L2 Analysts (escalations, questions)
├─ L3 Engineers (tool issues, complex cases)
├─ SOC Manager (reporting, issues)
└─ Other L1 Analysts (knowledge sharing)

OPERATIONAL:
├─ IT Operations (system issues, credentials)
├─ Network Team (traffic issues, firewall)
├─ Endpoint Team (EDR issues, deployment)
└─ Database Team (DB access, queries)

BUSINESS:
├─ User/Employee (incident notification)
├─ Manager/Supervisor (compliance, approvals)
├─ HR (employment verification)
├─ Business units (incident impact)
└─ Executive (major incidents)

EXTERNAL:
├─ Law Enforcement (if breach)
├─ Vendors (tool support)
└─ Auditors (compliance)
```

---

## Communication Channels

### When to Use Which Channel:

```
EMAIL:
├─ Formal escalations
├─ Documentation needed
├─ Urgent matters
├─ Multiple recipients
├─ Record keeping required

SLACK/MESSAGING:
├─ Quick questions
├─ Status updates (peer)
├─ Casual coordination
├─ Fast response needed
├─ Low-sensitivity info

TICKET/COMMENT:
├─ Alert investigation
├─ Progress updates
├─ Case documentation
├─ Team visibility
├─ Audit trail

IN-PERSON:
├─ Complex discussions
├─ Difficult messages
├─ Crisis situations
├─ Immediate response
├─ Relationship building

PHONE:
├─ Critical urgency
├─ Immediate action
├─ Difficult/sensitive
├─ No written needed
├─ Verbal confirmation
```

---

## Communication by Stakeholder

### **1. Communication with L2 Analyst**

**When:** Escalating, asking technical questions, providing updates

**Tone:** Professional, technical, brief

**Content:**
```
✓ Specific details (alert ID, findings)
✓ Evidence attached
✓ Your verdict/recommendation
✓ What you've already checked
✓ What L2 needs to determine
✗ Vague descriptions
✗ No evidence
✗ Rambling explanations
```

**Email example:**
```
Subject: Escalation - Alert #456 - Suspicious 
         Database Access

Hi L2_analyst_2,

Escalating alert #456 for your investigation.

SUMMARY:
User john.doe accessed production_database 
without prior access history or approval ticket.

FINDINGS:
- First-time database access (checked SIEM 6-month history)
- No approval ticket in Jira
- No business context found
- User is Finance analyst (doesn't normally query DB)

EVIDENCE ATTACHED:
- SIEM timeline (screenshot)
- User AD record (screenshot)
- Jira search results

RECOMMENDATION:
Verify with john's manager whether this access 
was authorized.

Please let me know if you need any additional 
information.

Thanks,
L1_analyst_1

---
Ticket: #456
Time escalated: 14:30 IST
```

**Slack example (quick question):**
```
@L2_analyst_2 Quick question on alert #123 - 
it shows user accessed file but no data transfer. 
Should I escalate or does access alone not worry you?
```

---

### **2. Communication with SOC Manager**

**When:** Reporting metrics, issues, requesting help, status updates

**Tone:** Professional, business-focused, concise

**Content:**
```
✓ Business impact
✓ Metrics/numbers
✓ Clear issue/problem
✓ Recommendation
✓ Context
✗ Too technical jargon
✗ Overly detailed
✗ Emotional tone
```

**Email example:**
```
Subject: Daily Metrics Report - 2024-06-21

Hi Manager,

Daily metrics for shift:
- Alerts processed: 285
- False positive rate: 8.5%
- Escalations: 5 (2 confirmed threats)
- Average triage time: 12 minutes

Issues:
- SIEM slow this afternoon (2-3 min queries)
  (Contacted L3 Engineer - investigating)

Wins:
- Caught phishing campaign (50 users)
- Prevented malware spread (isolated 1 system)

Requests:
- Need access to HR system for user verification

Please let me know if you need any clarification.

Thanks,
L1_analyst_1
```

---

### **3. Communication with IT Operations**

**When:** Requesting credentials, system access, technical support

**Tone:** Professional, specific, service-oriented

**Content:**
```
✓ Clear request
✓ Business justification
✓ Specific details
✓ Timeline
✗ Vague requests
✗ No justification
✗ Demanding tone
```

**Ticket example:**
```
Subject: Request - User Credential Verification

Team,

Investigation alert #456 requires verification 
of user john.doe's recent password changes.

Can you provide:
1. Last password change date for john.doe
2. Number of failed logins past 24 hours
3. Current account status

For ticket: #456
By: This morning if possible (ongoing investigation)

Thanks,
L1_analyst_1
```

---

### **4. Communication with HR**

**When:** Verifying employment status, contractor info

**Tone:** Professional, respectful, compliant

**Content:**
```
✓ Specific request
✓ Privacy-aware
✓ Legitimate security reason
✓ Timeline
✗ Over-reaching requests
✗ No justification
✗ Casual tone
```

**Email example:**
```
Subject: Security - Employment Verification

Hi HR Team,

For security investigation, need verification:

Employee: john.doe
Question: Is john currently employed and 
          on-site 2024-06-21?

Background: Alert investigation requires 
           confirmation of user activity.

Please confirm at your earliest convenience.

Thanks,
L1_analyst_1
Security Operations Team
```

---

### **5. Communication with User (Incident)**

**When:** Notifying about incident, requesting information

**Tone:** Professional, calm, helpful, non-accusatory

**Content:**
```
✓ Factual (what happened)
✓ What we're doing
✓ What they should do
✓ Support contact
✗ Accusatory tone
✗ Technical jargon
✗ Fear-mongering
✗ Blame
```

**Email example:**
```
Subject: Security Alert - Action Required

Hi john,

Our security team detected unusual activity on 
your account today at 14:30 IST.

WHAT HAPPENED:
Your account was accessed from an unusual 
location. We detected this and took immediate 
protective actions.

WHAT WE'RE DOING:
- Investigating the activity
- Reviewing what data was accessed
- Securing your account

WHAT YOU SHOULD DO:
1. Reset your password immediately
2. Review your recent account activity
3. Contact security if you see anything unusual

SUPPORT:
If you have questions, please contact:
- Security team: security@company.com
- Direct: +91-XXXX-XXXX-XXXX

We're here to help and protect your account.

Thanks,
Security Operations Team
```

---

### **6. Communication with Executive (Major Incident)**

**When:** Reporting major incidents, breaches, critical findings

**Tone:** Professional, executive-focused, impact-clear, calm

**Content:**
```
✓ Business impact (clear language)
✓ Current status
✓ Actions taken
✓ Next steps
✓ No technical jargon
✗ Alarmist language
✗ Technical details
✗ Uncertainty
✗ Multiple options
```

**Email example:**
```
Subject: SECURITY INCIDENT - Status Update

Dear [Executive],

Our security team has identified and is responding 
to a security incident.

SITUATION:
Unauthorized access to employee account detected.
Scope: 1 user, active monitoring underway.

CURRENT STATUS:
- Account secured
- Investigation active
- No data confirmed compromised (yet)
- No business impact to services

ACTIONS TAKEN:
- Account isolation
- Credential reset
- Forensic investigation initiated
- Incident response team activated

NEXT STEPS:
- Complete investigation (24-48 hours)
- Determine extent of access
- Implement additional protections
- Executive brief with findings

We will update you every 4 hours or immediately 
if critical changes.

Security Team
```

---

## Professional Communication Standards

### Email Best Practices:

```
SUBJECT LINE:
├─ Specific, not vague
├─ Alert type if relevant
├─ Urgency if needed
├─ Example: "ESCALATION - Alert #456 - 
           Suspicious DB Access"

GREETING:
├─ Professional
├─ Name if known
├─ Example: "Hi L2_analyst_2,"

BODY:
├─ Clear, concise summary first
├─ Then supporting details
├─ Evidence attached/referenced
├─ Specific requests/questions

TONE:
├─ Professional
├─ No slang/emojis
├─ Respectful
├─ Helpful

CLOSING:
├─ Professional sign-off
├─ Contact info if needed
├─ Thank you

SIGNATURE:
├─ Full name
├─ Title (L1 SOC Analyst)
├─ Contact info
└─ Company
```

### Slack Best Practices:

```
QUICK MESSAGES:
├─ Use for: Quick questions, status
├─ Tone: Can be casual but professional
├─ Length: 1-3 messages
├─ Example: "@L2 quick q on alert #123..."

THREADS:
├─ Keep discussion in thread (don't spam channel)
├─ Use for: Ongoing discussion
├─ Tag: Specific people

CHANNEL vs DM:
├─ Channel: General info, visibility
├─ DM: Sensitive, specific person

PROFESSIONALISM:
├─ No excessive emojis
├─ Proper grammar
├─ Respectful tone
├─ No personal drama
```

---

## Difficult Communications

### How to Handle Difficult Messages:

```
TELLING SOMEONE THEY WERE WRONG:
❌ "That was dumb"
✅ "I found something different in my 
   investigation. Can we discuss?"

ASKING FOR HELP:
❌ "I can't figure this out"
✅ "I've hit a blocker - I've checked X and Y,
   but need your expertise on Z"

DENYING REQUEST:
❌ "No, can't do that"
✅ "That's outside my scope, but let me 
   connect you with the right team"

ESCALATING MISTAKE:
❌ "This was missed by L2"
✅ "Additional findings in this case that 
   need further investigation"

DISAGREEMENT:
❌ "You're wrong"
✅ "I interpreted that differently. 
   Can we discuss?"
```

---

## Real Communication Examples

### **Example 1: Status Update**

```
Slack to L2_analyst_2:
"Alert #456 update: Investigated unusual DB access 
by john.doe. First-time access, no approval ticket. 
Escalating to you now - need manager verification 
on whether this was authorized. Ticket ready for 
your review."
```

### **Example 2: Difficult Question**

```
Slack to Manager:
"Hey, I escalated alert #456 to L2 yesterday. 
Just checking - is there a standard 
process for following up on escalations? 
Want to make sure I'm supporting L2 properly."

Manager response:
"Good question. L2 will update ticket status. 
If no update in 4 hours, follow up via Slack. 
Thanks for asking!"
```

### **Example 3: Asking for Help**

```
Slack to L3_engineer:
"I'm investigating a PowerShell alert and hit 
a technical block. The command is encoded in 
Base64. Should I decode it locally or is there 
a safe way through the SIEM? Don't want to 
accidentally execute anything. Your guidance?"
```

### **Example 4: Critical Incident**

```
Email to Security Manager:
Subject: CRITICAL - Active Incident #789

Immediate escalation: Confirmed malware execution 
on 3 systems, C2 communication detected, possible 
lateral movement.

Current: Containing systems, investigation ongoing
Action: Need IR team activation for full response
Timeline: Situation developing, hourly updates

Incident Response team cc'd for immediate activation.

Will follow up within 1 hour with more details.
```

---

## Common Communication Mistakes

### ❌ **Mistake 1: Too technical, no context**

**সমস्या:**
```
"EventID 4625 x50, source 10.0.1.100, 
 destination admin account, protocol NTLM"
L2: "What alert? What's the risk?"
```

**সমাধান:**
```
"Brute force attack on admin account detected.
 50 failed login attempts from internal IP,
 suggesting either attacker or misconfigured script.
 Need investigation to determine which."
```

---

### ❌ **Mistake 2: Vague/unprofessional**

**समस्या:**
```
Slack: "yo there's some weird stuff on alert 123
       lol might be bad?"
```

**समाधान:**
```
Email: "Alert #123: Suspicious file execution 
        detected. Needs investigation. Escalating 
        with evidence. Ticket #123."
```

---

### ❌ **Mistake 3: Accusatory tone**

**समस्या:**
```
"Your password is weak and got hacked because 
 you're not careful"
```

**समाधान:**
```
"We detected unusual activity on your account.
 As a precaution, please reset your password 
 and review recent activity. We're investigating."
```

---

### ❌ **Mistake 4: No supporting evidence**

**समस्या:**
```
Email: "Alert looks bad, should escalate"
L2: "What did you find? Show me the data."
```

**समाधान:**
```
Email: "Alert #456 escalation. First-time DB 
       access by john.doe, no approval ticket.
       Evidence attached (SIEM screenshot, 
       AD record, Jira search)."
```

---

### ❌ **Mistake 5: Wrong tone for audience**

**समस्या:**
```
To Executive: "Technical jargon overload, 
              no clear impact"
```

**समाधान:**
```
To Executive: "Unauthorized access detected 
             on one account. Investigating now.
             Will update in 4 hours."
```

---

## Communication Checklist

### **Before Sending Message**

- [ ] Audience appropriate (email vs slack)?
- [ ] Tone professional?
- [ ] Content clear and specific?
- [ ] Evidence/attachments ready?
- [ ] No jargon/acronyms without explanation?
- [ ] Specific request/question stated?
- [ ] Timeline clear?

### **Email Specifically**

- [ ] Subject line descriptive?
- [ ] Summary in first paragraph?
- [ ] Supporting details after?
- [ ] Professional greeting/closing?
- [ ] Signature included?
- [ ] Evidence attached?
- [ ] No urgent tone if not urgent?

### **Slack Specifically**

- [ ] Specific person tagged if needed?
- [ ] Using thread if continuation?
- [ ] Not spamming channel?
- [ ] Professional tone?
- [ ] Correct channel/DM?

### **User/Executive Communication**

- [ ] Non-technical language?
- [ ] Clear impact/next steps?
- [ ] No blame/accusatory?
- [ ] Reassuring tone?
- [ ] Support contact clear?

---

## Mini Quiz: Communication

### **Question 1: L2 কে escalate করার সময় কোনটা সবচেয়ে important?**

A) হাই-লেভেল summary  
B) Complete evidence এবং findings  
C) Technical jargon  
D) Your opinion on severity

**Answer:** B) Complete evidence এবং findings - L2 এর investigation based on your evidence

---

### **Question 2: User কে incident notify করার সময় টোন কেমন হওয়া উচিত?**

A) Accusatory (blame user)  
B) Alarmist (create fear)  
C) Professional, calm, helpful  
D) Overly technical

**Answer:** C) Professional, calm, helpful - সঠিক টোন user trust maintain করে

---

### **Question 3: কোনটা ভাল email subject line?**

A) "Alert"  
B) "ESCALATION - Alert #456 - Suspicious DB Access"  
C) "Check this"  
D) "FYI"

**Answer:** B) "ESCALATION - Alert #456 - Suspicious DB Access" - Specific, urgent level clear, easy to search

---

### **Question 4: Executive কে incident report করার সময় include করবেন?**

A) All technical details  
B) Complex jargon  
C) Business impact, current status, next steps  
D) Your personal concerns

**Answer:** C) Business impact, current status, next steps - Executives care about "What does this mean for business?"

---

### **Question 5: Slack ব্যবহার করবেন কখন?**

A) সব communication এর জন্য  
B) Quick questions, fast response needed  
C) Formal escalations  
D) Reporting to executive

**Answer:** B) Quick questions, fast response needed - Slack for speed, Email for documentation

---

## সহজ ভাষায় সারসংক্ষেপ

**Communication = Critical SOC skill**

**Stakeholders:**
- **L2/L3:** Technical, specific, evidence
- **Manager:** Business impact, metrics
- **IT:** Clear request, justification
- **HR:** Specific, privacy-aware
- **User:** Non-technical, reassuring
- **Executive:** Impact, status, next steps

**Channels:**
- **Email:** Formal, documentation, urgent
- **Slack:** Quick, status, casual questions
- **Ticket:** Investigation, team visibility
- **In-person:** Complex, difficult, crisis
- **Phone:** Critical urgency

**Professional Standards:**
✓ Clear subject line
✓ Professional tone
✓ Specific content
✓ Evidence/attachments
✓ Clear request/question
✓ Right audience
✗ No jargon (explain or avoid)
✗ No accusatory tone
✗ No vague descriptions

**Common Mistakes:**
- Over-technical/no context
- Vague/unprofessional
- Accusatory tone
- No supporting evidence
- Wrong tone for audience

**Email Best Practice:**
1. Subject line (specific)
2. Summary (first paragraph)
3. Details (supporting)
4. Evidence (attached)
5. Request (clear)
6. Professional closing

**Remember:**
- Match tone to audience
- Include evidence always
- Be specific, not vague
- Professional always
- Non-technical for users/execs
- Clear requests

---

## Resources for Learning

**Communication templates:**
- Email templates (your company)
- Escalation format
- User notification template
- Executive summary format

**Feedback:**
- Ask manager for feedback
- Learn from L2 responses
- Ask if communication was clear

---

**Module 20 Complete! ✅**

এখন আপনি জানেন:
- ✅ Communication stakeholders
- ✅ Communication channels
- ✅ Professional email format
- ✅ Slack best practices
- ✅ Communication by stakeholder type
- ✅ Difficult communication handling
- ✅ Executive communication
- ✅ Real communication examples
- ✅ Common communication mistakes
- ✅ Communication checklist

Progress: **20 of 28 modules complete (71%)**

---

<!-- nav-footer -->
## 🧭 Navigation

| | |
|---|---|
| **Previous** | [⬅️ Module 19: Alert Escalation](../module-19-alert-escalation/index.md) |
| **Next** | [Module 21: SOC Metrics & Objectives ➡️](../module-21-soc-metrics-objectives/index.md) |
| **🏠 Course Home** | [STUDY_NOTES.md](../../STUDY_NOTES.md) |
