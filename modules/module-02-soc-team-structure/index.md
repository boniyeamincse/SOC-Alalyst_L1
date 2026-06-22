# Module 2: SOC Team Structure and Responsibilities

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- SOC team এর comprehensive structure
- প্রতিটি role এর specific responsibilities
- L1, L2, L3, এবং Manager এর মধ্যে interaction
- Different SOC models (24x7, follow-the-sun, hybrid)
- Career progression path: L1 → L2 → L3
- Shift structure এবং on-call system
- How escalation works in reality

---

## SOC Team: Complete Picture

একটি পূর্ণ-বিকশিত SOC এ বিভিন্ন টিম থাকে যারা একসাথে কাজ করে:

```
┌─────────────────────────────────────────────────────────┐
│         SOC Director / Chief Security Officer            │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
    ┌───▼────┐      ┌──────▼────┐    ┌────▼──────┐
    │ SOC     │      │  Incident │    │ Threat    │
    │Manager  │      │ Response  │    │ Intel     │
    │(Mon-    │      │ Manager   │    │ Team      │
    │ Fri)    │      │           │    │           │
    └───┬────┘      └──────┬────┘    └────┬──────┘
        │                  │               │
    ┌───▴────────┐    ┌────▴────┐   ┌─────▴──────┐
    │             │    │         │   │            │
┌──▼──┐  ┌──▼──┐│ ┌─▼──┐ ┌──▼─┐│ ┌┴──┐ ┌───┐
│ L2  │  │ L2  ││ │IR  │ │IR  ││ │TI │ │TI │
│Lead │  │Eng  ││ │Lead│ │Team││ │Eng│ │Ana│
└──┬──┘  └──┬──┘│ └──┬─┘ └──┬─┘│ └┬──┘ └──┬┘
   │         │  │    │      │  │  │        │
  ┌┴─────────┴──┴┐   │      │  │  └────┬───┘
  │              │   │      │  │       │
┌─▼──┐ ┌──┐ ┌──▼─┐  │      │  │       │
│ L1 │ │L1│ │ L1 │  │      │  │       │
│    │ │  │ │    │  │      │  │       │
└────┘ └──┘ └────┘  │      │  │       │
                     └──────┘  └───────┘
                                (24/7)
```

---

## প্রতিটি Role: Deep Dive

### **1. SOC L1 Analyst - আপনার বর্তমান Position**

#### দায়িত্ব:

**Alert Management:**
- 100-500+ alerts daily handle করা
- 5-10 minutes per alert analysis
- Alert properties review (source, destination, user, time)
- Immediate action যা required

**Initial Triage:**
- এই alert real threat কিনা decision করা
- False positives filter করা (noise reduction)
- Benign activity identify করা
- Severity verify করা

**Data Enrichment:**
- IP reputation check করা
- Domain information lookup করা
- User activity history দেখা
- Previous similar alerts check করা

**Investigation:**
- Initial root cause analysis
- Context gathering
- Timeline creation
- Evidence collection

**Documentation:**
- Alert ticket এ findings লিখা
- Investigation steps document করা
- Decision reasoning explain করা
- Follow-up actions note করা

**Escalation:**
- Which alerts escalate করবে L2 কে decide করা
- Complete context সহ escalate করা
- এবং L2 কে what-why-how explain করা

**Communication:**
- Team মাসিক update তে findings share করা
- L2 সাথে collaboration
- Manager কে metrics report করা

#### কাজের উদাহরণ:

**Scenario: Unusual login alert**

```
সকাল 9:30 AM: Alert আসে
"User john.doe logged in from Singapore at 3:00 AM"

L1 এর investigation:

1. User জানি কিনা?
   ✓ john.doe - Finance department এ work করে
   
2. Normal location?
   ✗ Singapore - এখানে কখনো login করেনি
   
3. Time normal?
   ✗ 3:00 AM - এটা sleep time
   
4. VPN use করেছে?
   ✗ No VPN detected
   
5. Previous similar activity?
   ✗ Last month এও এক সপ্তাহ Singapore travel করেছিল
   
6. Account compromise signals?
   ✓ Password reset same day?
   ✓ New device?
   ✓ Email forwarding?
   
Decision: "Needs Investigation by L2 - possible compromised account"
Escalation: YES
```

#### দৈনিক শিডিউল:

```
09:00 - Dashboard open, prioritize 300 alerts
09:15 - Batch process low-severity benign alerts (50)
10:00 - 5টি complex alert investigate
10:45 - Documentation update
11:15 - L2 meeting - escalations discuss করুন
12:00 - Lunch break
13:00 - Alert backlog continue
15:00 - Playbook update (new patterns found)
16:00 - Metrics calculate
16:30 - Handover notes L2 এর জন্য
17:00 - Shift end
```

#### প্রত্যাশিত Performance Metrics:

- **Alert Handling Rate:** ৩০-৪০ alerts/hour
- **False Positive Accuracy:** ৮৫-৯০%
- **Mean Time to Triage (MTTR):** < ৫ minutes
- **Escalation Accuracy:** > ৯০%
- **Ticket Closure Rate:** ২০০+ per shift

---

### **2. SOC L2 Analyst - Senior Investigator**

#### দায়িত্ব:

**Complex Investigation:**
- L1 থেকে escalated alerts investigate করা
- Deep-dive analysis করা
- Malware basic analysis
- Advanced SIEM queries লেখা
- Threat correlation করা

**Alert Rule Tuning:**
- False positive generating rules identify করা
- New rules create করা
- Existing rules improve করা
- Threshold adjust করা

**Threat Research:**
- New threat intelligence analyze করা
- Emerging attack patterns study করা
- Industry trends follow করা
- Detection capability improve করা

**L1 Training & Mentoring:**
- Junior analysts guide করা
- Playbooks improve করা
- Best practices share করা
- Knowledge transfer করা

**Incident Escalation:**
- Incidents কে Incident Response team কে escalate করা
- Context provide করা
- Initial assessment করা

#### কাজের উদাহরণ:

**Scenario: L1 থেকে escalated investigation**

```
L1 escalation: "Possible compromised account - john.doe"

L2 deeper investigation:

1. Account Activity Timeline:
   2:50 AM - Password changed (email request)
   3:00 AM - Singapore login
   3:15 AM - Email forwarding rule added (suspicious)
   3:30 AM - Access to Finance shared drive
   
2. Email Monitoring:
   ✗ Email forwarding to external: attacker@evil.com
   
3. Data Access Pattern:
   ✗ John usually: 9 AM-5 PM, India IP
   ✗ Now: 24/7 access, multiple countries
   
4. File Downloads:
   ✗ 500 MB sensitive documents downloaded
   ✗ Unusual for john (normally read-only)
   
Conclusion: "Confirmed Account Compromise - Data Exfiltration Risk"
Escalate to: Incident Response Team
Recommended Actions:
  - Account immediate lock
  - Email forwarding remove
  - Data access audit
  - Forensics on john's device
```

#### দায়িত্বের হায়ারার্কি:

```
L1 says: "This looks suspicious"
L2 says: "Here's what really happened"
L2 says: "This is a confirmed incident"
```

---

### **3. SOC L3 / SOC Engineer**

#### দায়িত্ব:

**Tool Development & Integration:**
- Custom detection scripts লেখা
- SIEM integration build করা
- Automation develop করা
- API integration করা

**SIEM Optimization:**
- Performance tuning করা
- Data pipeline optimize করা
- Alert correlation rules improve করা
- Correlation engine optimize করা

**Advanced Threat Analysis:**
- Malware detailed analysis
- Reverse engineering (basic)
- Threat actor TTPs research
- Custom detection logic develop করা

**Architecture & Design:**
- SOC architecture plan করা
- Tool selection recommend করা
- Scalability design করা
- New tech evaluation করা

**Documentation:**
- Technical documentation maintain করা
- Playbook automation part handle করা
- Runbook technical section write করা

#### কাজের উদাহরণ:

**Scenario: নতুন threat detection develop করা**

```
Background: L2 notice করলো একটি trend
"Multiple phishing emails + credential theft + 
internal network scanning"

L3 এর কাজ:

1. Pattern Analysis:
   - Timeline এর correlation
   - Attacker methodology identify
   - Attack chain visualization
   
2. Custom Detection:
   - SIEM correlation rule write করা
   - Python script develop করা
   - Detection accuracy test করা
   
3. Integration:
   - Detection system integrate করা
   - Automation pipeline build করা
   - Alert generation test করা
   
4. Deployment:
   - Testing phase
   - Production rollout
   - L1/L2 কে training দেওয়া
   
Result: নতুন attack pattern automatically detect হয় এখন
```

---

### **4. Incident Response Manager**

#### দায়িত্ব:

**Major Incident Handling:**
- Confirmed incidents manage করা
- Response team coordinate করা
- Escalation path decide করা
- Communication centralize করা

**Crisis Communication:**
- Executive management কে update দেওয়া
- Incident severity communicate করা
- Timeline maintain করা
- Status updates regular দেওয়া

**Post-Incident Analysis:**
- Root cause analysis (post-incident)
- Lessons learned documentation
- Prevention recommendations দেওয়া
- Process improvement identify করা

**Stakeholder Management:**
- Business team notify করা
- IT operations coordinate করা
- Legal inform করা (যদি প্রয়োজন)
- Customer communication (যদি প্রয়োজন)

#### Incident Classification:

```
Low (Green):
- Single user affected
- Data not exposed
- No business impact
- L2 + Incident Manager handle করে

Medium (Yellow):
- Multiple users affected
- Potential data exposure
- Limited business impact
- Incident Response team activate

High (Red):
- Multiple departments affected
- Data confirmed exposed
- Major business impact
- Full incident response team
- Executive notification

Critical (Black):
- Entire organization affected
- Major data breach
- Severe business impact
- External communication may needed
- Law enforcement involvement possible
```

---

### **5. SOC Manager / Team Lead**

#### দায়িত্ব:

**Team Management:**
- L1, L2 analysts coordinate করা
- Shift planning করা
- Performance review করা
- Hiring decisions take করা
- Training programs organize করা

**KPI Monitoring:**
- Alert metrics track করা
- FP rate monitor করা
- MTTR improve করা
- Team efficiency measure করা

**Escalation Authority:**
- কোন alert escalate করবে সেটা decide করা
- New alert rules approve করা
- Process changes approve করা

**Executive Reporting:**
- Monthly metrics report তৈরি করা
- Trending threats communicate করা
- Resource needs request করা
- Budget management করা

**Process Improvement:**
- Playbooks improve করা
- Workflows optimize করা
- New tools evaluate করা
- Best practices implement করা

---

## Escalation Flow: Real Example

একটি alert এর journey দেখি escalation chain এ:

### **Alert Journey: Malware Detection**

```
Stage 1: ALERT GENERATION (SIEM)
└─ File "invoice.exe" download হয়েছে suspicious source থেকে
   └─ Alert: "Malware - Trojan.Generic.A detected"

Stage 2: L1 TRIAGE (5-10 mins)
└─ L1 Analyst checks:
   ✓ File hash database এ আছে? YES - Known malware
   ✓ User action? Clicked email link
   ✓ File executed? NO - Still in downloads folder
   ✓ System compromised signals? NO
   ✓ Decision: "Suspicious but contained"
   └─ Escalate to L2: "User clicked malware link, 
                       file not executed, recommend 
                       user education"

Stage 3: L2 INVESTIGATION (15-30 mins)
└─ L2 checks:
   ✓ Email source legitimate? NO - Spoofed
   ✓ Similar emails other users? YES - 50+ users
   ✓ Anyone executed it? Checking endpoints...
   ✓ Findings: Coordinated phishing campaign
   └─ Escalate to Incident Response:
      "Phishing campaign - 50 users targeted,
       1 execution confirmed, full IR needed"

Stage 4: INCIDENT RESPONSE (ongoing)
└─ IR Manager activates team:
   ✓ Contain affected endpoints
   ✓ Email security block sender
   ✓ User education send
   ✓ Forensics on executed endpoint
   └─ Update Management:
      "Security incident detected - phishing campaign,
       1 system potentially affected, containment 
       underway, no data loss yet"

Stage 5: POST-INCIDENT (1-7 days)
└─ Lessons learned:
   ✓ New email filter rule add
   ✓ Detection rule improve
   ✓ User training update
   ✓ Process documentation update
```

---

## Different SOC Models

বিভিন্ন organization বিভিন্ন model use করে:

### **Model 1: 24x7 SOC (Round-the-clock)**

**কিভাবে কাজ করে:**
- 3টি shift: Morning (9-5), Evening (5-1), Night (1-9)
- প্রতিটি shift এ পূর্ণ team
- Incident যেকোনো সময় handle করা যায়

**সুবিধা:**
- Real-time response
- No blind spots
- Better incident detection

**অসুবিধা:**
- সবচেয়ে expensive
- Staff recruitment challenge

**ব্যবহার করে:**
- Large enterprises
- Financial institutions
- Healthcare organizations

```
Manager: Mon-Fri 9-5
L2 Team:  [====][====][====] (3 shifts)
L1 Team:  [========][========][========] (3 shifts)
IR Team:  24/7 on-call
```

---

### **Model 2: Business Hours SOC (9-5)**

**কিভাবে কাজ করে:**
- শুধু office hours কাজ করা
- Off-hours এ on-call team থাকে
- ছোট team higher volume handle করে

**সুবিধা:**
- Cost effective
- Management easier
- Work-life balance better

**অসুবিধা:**
- Delayed response off-hours
- Alert backlog morning এ

**ব্যবহার করে:**
- Medium organizations
- স্থানীয় businesses
- Non-critical services

```
Manager: Mon-Fri 9-5
L2 Team:  [=======] 9-5 + on-call nights
L1 Team:  [=======] 9-5 + on-call nights
IR Team:  On-call 24/7
```

---

### **Model 3: Follow-the-Sun SOC**

**কিভাবে কাজ করে:**
- Multiple offices different time zones এ
- একটি team শেষ হলে পরেরটা শুরু করে
- 24/7 coverage কিন্তু distributed

**সুবিধা:**
- 24/7 coverage cost-effective
- Different geographic expertise
- Scalable

**অসুবিধা:**
- Handover complexity
- Time zone communication challenge

**ব্যবহার করে:**
- Global organizations
- Multinational companies
- Distributed teams

```
Timezone A (India):     [========] 9-5 IST
Timezone B (Middle East):[====][====] shifts
Timezone C (Europe):    [======] 9-5 CET
Timezone D (US):        [======] 9-5 EST

24/7 coverage maintained through handover
```

---

## Career Progression: L1 → L2 → L3

আপনি কিভাবে এগিয়ে যাবেন:

### **L1 থেকে L2: 18-24 months**

**প্রয়োজনীয় দক্ষতা:**
- ✓ Alert triage এ mastery (95%+ accuracy)
- ✓ Network fundamentals প্রকাশ্যে demonstrate
- ✓ Basic scripting (Python/bash)
- ✓ Complex investigations independently handle করতে পারা
- ✓ Leadership potential দেখানো

**প্রয়োজনীয় সার্টিফিকেশন:**
- CompTIA Security+
- GCIH (GIAC Certified Incident Handler) optional
- SIEM vendor certification

**পরীক্ষিত দক্ষতা:**
- 500+ alerts investigate করা
- Complex incident handle করা
- Playbook contribute করা
- Junior analyst mentor করা

### **L2 থেকে L3: 24-36 months**

**প্রয়োজনীয় দক্ষতা:**
- ✓ Advanced threat analysis capability
- ✓ Scripting proficiency (Python, bash, PowerShell)
- ✓ SIEM architecture understanding
- ✓ Detection engineering experience
- ✓ New tools evaluate করতে পারা

**প্রয়োজনীয় সার্টিফিকেশন:**
- GIAC Certified Enterprise Defender (GCED)
- OSCP (Offensive Security Certified Professional)
- Advanced scripting course

**পরীক্ষিত দক্ষতা:**
- Detection rules create করা
- Custom automation develop করা
- Advanced incident response
- Tool integration successful

---

## On-Call System: পরে দায়িত্ব

অফিস সময়ের বাইরে serious incident এ কে respond করবে?

### **On-Call Rotation:**

```
Week 1: Analyst A primary, Analyst B backup
Week 2: Analyst B primary, Analyst C backup
Week 3: Analyst C primary, Analyst D backup
Week 4: Analyst D primary, Analyst A backup

On-Call Duty:
- 24 hours respond করতে ready থাকা
- Average: 2-4 incident calls per month
- Response time: < 15 minutes
- Compensation: On-call stipend + overtime
```

### **On-Call Protocol:**

```
Alert triggered at 2:00 AM (off-hours)

STEP 1: SIEM alert
└─ Auto-escalation to on-call analyst

STEP 2: Notification
└─ Phone call + SMS + Email

STEP 3: Acknowledgment
└─ On-call analyst: "Investigating"

STEP 4: Initial Assessment
└─ Critical? → Full activation
    Medium? → Assessment only
    Low? → Queue for morning

STEP 5: Communication
└─ Manager inform করা
    Team notify করা
    If critical: Additional resources activate
```

---

## SOC Team Interaction Workflow

একটি দিন এর মধ্যে কিভাবে team interact করে:

### **Morning Standup (9:00 AM)**

```
Attendees: Manager, all L1s, L2 Lead

L1 Updates:
- "200 alerts processed, 180 FP, 20 escalated"
- "New phishing campaign detected"
- "User joe@company.com compromised yesterday"

L2 Updates:
- "3 escalations investigated"
- "2 confirmed incidents"
- "New alert rule needed for phishing pattern"

Decisions:
- New alert rule create করবে L3
- Phishing playbook update করবে L2
- User joe notification করবে IT
```

---

### **Throughout the Day**

```
09:15 - New complex alert আসে
└─ L1 initial triage
    └─ L2 কে escalate করে প্রমাণ সহ
        └─ L2 investigate করে
            └─ "Incident confirmed"
                └─ IR Manager activate করে

13:00 - L2 এবং L3 coordination meeting
└─ New detection rules review
    └─ False positive patterns discuss
        └─ New SIEM queries test করা

15:00 - L1 এবং L2 collaboration
└─ Complex case discuss করা
    └─ Investigation technique শেয়ার করা
        └─ L1 learning করছে
```

---

### **End of Shift (5:00 PM)**

```
L1 Handover to Evening L1:
- "50 alerts in queue"
- "High-priority: alert #123 needs follow-up"
- "New escalation: user compromise case"

L2 Handover:
- "Case #456 still investigating"
- "Alert rule #789 needs tuning"
- "Incident #012 may need escalation tonight"

Manager Sign-off:
- ✓ All critical alerts acknowledged
- ✓ No major incidents pending
- ✓ Team ready for evening shift
```

---

## Key Concepts: Role Mapping

| Decision Type | Authority | Process |
|---------------|-----------|---------|
| **False Positive** | L1 | 5-10 min analysis, close ticket |
| **Needs Investigation** | L1→L2 | Escalate with context |
| **Confirmed Incident** | L2→IR | Activate response team |
| **New Alert Rule** | L2+L3 | Design, test, deploy |
| **Staffing Decision** | Manager | Budget + hiring |
| **Process Change** | Manager+L2 | Review, implement, document |
| **Tool Evaluation** | L3+Manager | Technical + business case |
| **Performance Review** | Manager | Quarterly or annual |

---

## Common Mistakes: Role Confusion

### ❌ **Mistake 1: L1 trying L3 work**

**সমস্যা:** Alert investigate করতে গিয়ে scripting করতে যাওয়া

**সমাধান:** আপনার role focus করুন। L3 এর কাজ L2 এর সাথে discuss করুন।

---

### ❌ **Mistake 2: L2 ignoring L1 input**

**সমস্যা:** L1 এর escalation এর context read না করা

**সমাধান:** L1 এর investigation valuable input। তাদের findings seriously নিন।

---

### ❌ **Mistake 3: Manager micro-managing L1**

**সমস্যা:** প্রতিটি decision Manager এ question করা

**সমাধান:** L1 trust করুন, guidance দিন, empower করুন।

---

### ❌ **Mistake 4: Alert stalling যখন responsibility unclear**

**সমস্যা:** "এটা L2 এর কাজ" বলে L1 করছে না, L2 কেউ নেই

**সমাধান:** Clear escalation path define করুন। যখন unclear তখন higher level inform করুন।

---

### ❌ **Mistake 5: No handover documentation**

**সমস্যা:** Evening shift কোন context পাচ্ছে না

**সমাধান:** Shift handover always document করুন। Key alerts সব info সহ pass করুন।

---

## Practical Checklist: Team Communication

আপনি L1 হিসেবে কিভাবে professionally team এর সাথে কাজ করবেন:

**✅ L2 এর সাথে escalation**
- [ ] Complete context provide করুন
- [ ] Your investigation step include করুন
- [ ] কেন escalate করছেন explain করুন
- [ ] Next step suggest করুন

**Example escalation message:**
```
Alert: Suspicious PowerShell Activity
User: admin@company.com
Time: 14:30 IST
Status: ESCALATE

Investigation:
- User: Senior admin (legitimate)
- Command: Get-ChildItem -Recurse (common)
- Target: C:\ProgramData (system directory)
- Time: Off-hours (unusual)
- Context: User on vacation today

Finding: Likely automated script or policy compliance 
scan, but admin on vacation makes it suspicious.

Question for L2: Should we contact admin to verify?
```

**✅ Manager এর সাথে reporting**
- [ ] Numbers exact করুন
- [ ] Trending দেখান
- [ ] Resource needs identify করুন
- [ ] Wins celebrate করুন

**✅ Team knowledge sharing**
- [ ] New pattern discover করলে team inform করুন
- [ ] New playbook need হলে suggest করুন
- [ ] Questions ask করুন - learning যায় বেড়ে

---

## Mini Quiz: Team Structure

### **Question 1: একটি complex phishing campaign এ, কার দায়িত্ব comprehensive detection rule create করা?**

A) L1 Analyst  
B) L2 Analyst  
C) L3 Engineer  
D) Incident Response Manager

**Answer:** C) L3 Engineer - কারণ advanced detection logic এবং automation engineer এর কাজ

---

### **Question 2: On-call এ কে থাকে 24/7 এমনকি business hours ছাড়াও?**

A) L1 Analyst  
B) L2 Analyst  
C) Only Incident Response Manager  
D) All senior staff এ rotation

**Answer:** D) All senior staff এ rotation - specific organization policy অনুযায়ী

---

### **Question 3: L1 এ escalation করার সময় কোনটি সবচেয়ে গুরুত্বপূর্ণ?**

A) Alert severity নিয়ে discuss করা  
B) আপনার investigation findings + why escalation needed  
C) L2 কে alert rule change করতে বলা  
D) Manager কে inform করা

**Answer:** B) আপনার investigation findings + why escalation needed - Context ছাড়া escalation useless

---

### **Question 4: কার responsible new alert rule create এবং test করা?**

A) L1 + L2  
B) L2 + L3  
C) L3 + Manager  
D) Manager only

**Answer:** B) L2 + L3 - L2 requirement define করে, L3 technically implement করে

---

### **Question 5: একটি critical incident এ, যে সবসময় executive এর কাছে update রিপোর্ট করবে?**

A) L1 Analyst  
B) L2 Analyst  
C) Incident Response Manager  
D) SOC Manager

**Answer:** C) Incident Response Manager - crisis communication তাদের responsibility

---

## SOC Team Interaction Matrix

কে কার সাথে, কখন, কীভাবে interact করে:

```
┌─────────────────────────────────────────────────────────────────┐
│ From\To │  L1    │  L2    │  L3    │   IR   │  Manager │ Ext   │
├─────────────────────────────────────────────────────────────────┤
│   L1    │ Daily  │ Alert  │  Tool  │ None   │ Monthly │ None  │
│         │ Collab │Escalate│Request │        │ Metrics │       │
├─────────────────────────────────────────────────────────────────┤
│   L2    │ Guide  │ Daily  │ Query  │ Incident│ Issue  │ Threat │
│         │ Mentor │ Standup│ Design │ Escal.  │ Report │ Intel  │
├─────────────────────────────────────────────────────────────────┤
│   L3    │ Train  │ Tech   │ Daily  │ Tech   │ Budget │ Tools  │
│         │ Forum  │ Review │ Standup│ Review │ Request│ Info   │
├─────────────────────────────────────────────────────────────────┤
│   IR    │ Alert  │ Active │ Foren  │ Daily  │ Status │ Law Enf│
│         │ Inform │ Coll   │ Tools  │ Coord  │ Updates│ Notify │
├─────────────────────────────────────────────────────────────────┤
│Manager  │  1on1  │ 1on1   │ 1on1   │ Incident│ Weekly │Executive
│         │ Perf   │ Goals  │ Goals  │ Review │ Meeting│ Report │
└─────────────────────────────────────────────────────────────────┘

Frequency: Daily, Weekly, Monthly, As-needed, or Project-based
```

---

## সহজ ভাষায় সারসংক্ষেপ

**SOC টিম এর স্তর:**

- **L1:** আপনি এখন - Alert volume handle করো, false positive filter করো
- **L2:** Advanced investigation - Complex cases handle করে, L1 mentor করে
- **L3:** Engineer - Detection rules create করে, automation develop করে
- **Manager:** Team lead - Staffing, KPI, decisions
- **IR Manager:** Major incidents - Crisis management, escalation

**কে কি করে:**
- L1: Triage + initial investigation
- L2: Deep investigation + rule tuning
- L3: Detection development + automation
- IR: Incident response + stakeholder management

**Escalation মানে:**
- আমি investigate করেছি
- এটা complex/serious
- You এর expertise দরকার
- এখানে আমার findings

**On-call মানে:**
- Office বন্ধ সময়ে যেকোনো incident handle করতে ready
- 15 minutes response time
- প্রয়োজনে team activate করো

---

## Resources for Learning

**Team collaboration best practices:**
- Atlassian - Communication tips
- Harvard Business Review - Cross-functional teams
- Your company এর training program

**Incident escalation procedures:**
- আপনার company playbook
- NIST Incident Response guide
- Your manager থেকে direct training

---

**Module 2 Complete! ✅**

এখন আপনি জানেন:
- ✅ SOC টিমের পূর্ণ structure
- ✅ প্রতিটি role এর responsibility
- ✅ কিভাবে escalation কাজ করে
- ✅ Different SOC models
- ✅ Career progression path
- ✅ Team interaction workflows

