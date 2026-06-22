# Module 1: Introduction to SOC

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- SOC (Security Operations Center) কি এবং কেন প্রয়োজন
- Information security এর ভিত্তি (CIA Triad)
- SOC এর মূল কাজ ও দায়িত্ব
- In-house SOC এবং Managed SOC এর পার্থক্য
- SOC team structure এবং বিভিন্ন role
- SOC L1 Analyst হিসেবে আপনার position কোথায়

---

## শুরুর আগে: একটি গল্প

রফি আপনার কোম্পানির সাইবার সিকিউরিটি টিমের একজন L1 Analyst। একদিন সকালে সে office এ এসে দেখল তার dashboard এ লাল alert আছে - "Unusual Login Activity from Unknown Location"। এখন তার কাজ হল:

1. এই alert কি সত্যি threat নাকি false alarm?
2. যদি threat হয় তাহলে কি করতে হবে?
3. কিভাবে তদন্ত করবে?
4. কখন escalate করবে?

এটাই SOC L1 Analyst এর প্রতিদিনের কাজ। আসুন শিখি এটা কিভাবে করতে হয়।

---

## SOC কি? (What is SOC?)

**SOC = Security Operations Center**

SOC হল একটি centralized team যারা 24/7 একটি organization এর security monitor করে, threats detect করে, এবং incidents handle করে।

### সহজ ভাষায় বলতে গেলে:

আপনার বাড়িতে একটি security guard আছে যে দরজা-জানালা পাহারা দেয়। **SOC হল ডিজিটাল বিশ্বের সেই security guard।** এটি:

- সব সময় watch করে
- সন্দেহজনক activity detect করে
- দ্রুত action নেয়
- emergency এ immediate response দেয়

### SOC তিনটি মূল কাজ করে:

1. **Detect (সনাক্তকরণ)** - সন্দেহজনক activity খুঁজে বের করা
2. **Investigate (তদন্ত)** - কি ঘটেছে তা বুঝা
3. **Respond (প্রতিক্রিয়া)** - threat এর বিরুদ্ধে action নেওয়া

---

## CIA Triad: Information Security এর ভিত্তি

সব cybersecurity এর মূল ভিত্তি **CIA Triad**। এটা তিনটি principle:

### 1. **Confidentiality (গোপনীয়তা)**
- শুধুমাত্র authorized people data access পাবে
- কোন unauthorized person data দেখতে পারবে না

**উদাহরণ:**
- Employee database শুধু HR দেখতে পারে
- Customer credit card number কেউ দেখতে পারে না
- Patient medical records শুধু doctor দেখতে পারে

### 2. **Integrity (সততা)**
- Data সঠিক এবং unchanged থাকবে
- কোন unauthorized modification হবে না

**উদাহরণ:**
- Bank transaction এ amount change হতে পারে না
- আপনার salary record কেউ বদলে দিতে পারবে না
- Contract এ কেউ clause add করতে পারবে না

### 3. **Availability (প্রাপ্যতা)**
- Authorized users যখন চায় তখন data/service পাবে
- System downtime minimize করতে হবে

**উদাহরণ:**
- আপনি যখন চান তখন email access পাবেন
- Bank ATM সবসময় কাজ করবে (downtime very rare)
- Company website সবসময় accessible থাকবে

### CIA Triad Visual:

```
        Confidentiality
              /\
             /  \
            /    \
           /      \
          /        \
    Integrity ---- Availability
```

**Real SOC Example:**
একটি ransomware attack এ তিনটাই compromise হয়:
- **Confidentiality ভাঙা:** Attacker data চুরি করেছে
- **Integrity ভাঙা:** Attacker files encrypt করেছে (এখন content পরিবর্তিত)
- **Availability ভাঙা:** Users data access করতে পারছে না

SOC টিম দ্রুত এই তিনটি aspect restore করতে কাজ করে।

---

## In-house SOC vs Managed SOC

### **In-house SOC (নিজস্ব SOC)**

**নিজের টিম আপনার security handle করে।**

**সুবিধা:**
- সম্পূর্ণ control আছে
- Company এর যত্ন নেয় যেন নিজের ব্যবসা
- তাৎক্ষণিক decision নিতে পারে
- Organization context সবসময় জানে

**অসুবিধা:**
- খরচ বেশি (24/7 staff, tools, training)
- talent recruit করা কঠিন
- infrastructure maintain করতে হবে

**কখন সেরা:**
- বড় organization
- High-risk industry (finance, healthcare)
- sensitive data অনেক
- ছোট incident volume নেই

### **Managed SOC (আউটসোর্সড)**

**তৃতীয় পক্ষের service provider handle করে।**

**সুবিধা:**
- সাশ্রয়ী
- 24/7 experts already available
- নিজের staff training করতে হয় না
- Provider নিয়মিত আপডেট দেয়

**অসুবিধা:**
- Less control
- Multiple clients handle করে (দ্রুত response নাও হতে পারে)
- Internal process ঠিকমত বুঝতে নাও পারে
- Data privacy concern থাকতে পারে

**কখন সেরা:**
- ছোট থেকে মাঝারি organization
- Limited budget
- Modern threats এ expose হতে চায় না কিন্তু staff নেই
- Managed service provider transparent ও reliable

### বাংলাদেশে ট্রেন্ড:

বাংলাদেশী স্টার্টআপ এবং ছোট কোম্পানিগুলো বেশিরভাগ **Managed SOC** use করে। কারণ:
- In-house team expensive
- Experts locally limited
- Cost-effective solution চান

---

## SOC Team Structure

একটি SOC তে বিভিন্ন level এর professionals থাকে:

### **1. SOC L1 Analyst (বর্তমানে আপনি)**

**দায়িত্ব:**
- Alerts monitor করা
- Initial triage করা (alert important কিনা)
- False positives filter করা
- Investigation এর প্রথম step
- Data enrich করা
- L2 কে escalate করা যখন প্রয়োজন

**দক্ষতা:**
- Basic networking knowledge
- Log reading ও parsing
- Alert investigation
- Documentation
- Communication

**প্রতিদিনের workflow:**
- 100-500 alerts handle করা
- 5-10 minutes per alert analysis
- 80-90% false positive filter করা
- Critical alerts immediately escalate করা

### **2. SOC L2 Analyst (Senior Analyst)**

**দায়িত্ব:**
- Complex investigations handle করা
- L1 এর escalated alerts investigate করা
- New alert rules create/improve করা
- Threat research করা
- L1 কে guide করা

**দক্ষতা:**
- Advanced networking এবং security
- Malware analysis basic knowledge
- Scripting (Python, bash)
- SIEM deep knowledge

### **3. SOC L3 / SOC Engineer**

**দায়িত্ব:**
- Security tools development
- SIEM tuning এবং optimization
- Automation এবং integration
- Complex incident response
- New tools evaluation

**দক্ষতা:**
- Programming (Python, Java, C++)
- System administration
- Database knowledge
- Advanced threat analysis

### **4. SOC Manager / Team Lead**

**দায়িত্ব:**
- Team manage করা
- KPI track করা
- Budget maintain করা
- Staffing decisions
- Executive reporting

### **5. Incident Response Manager**

**দায়িত্ব:**
- Major incidents handle করা
- Law enforcement এর সাথে communicate করা
- Post-incident review
- Crisis management

### SOC Team Chart:

```
        SOC Manager
            |
    --------|--------
    |       |       |
   IR      L2      L2
  Lead   Lead    Engineer
    |    |  |     |
    |    L1 L1   Tools
    |    L1 L1   Team
 Responders
```

---

## SOC L1 Analyst: আপনার ভূমিকা

### আপনি কিভাবে fit করছেন?

আপনি SOC এর **front-line analyst**। আপনার কাজ:

1. **Volume handle করা** - অনেক alerts দ্রুত process করা
2. **Noise reduce করা** - false positives filter করা
3. **Time save করা** - L2 এর সময় বাঁচানো
4. **Pattern detect করা** - recurring issues spot করা
5. **Documentation** - সব findings properly document করা

### L1 Analyst এর দৈনন্দিন কাজ:

```
09:00 AM - Dashboard open, 250 new alerts
09:15 AM - False positive filter (100 alerts gone)
09:45 AM - 5 alerts investigate (4 benign, 1 suspicious)
10:30 AM - 1 alert escalate to L2
11:00 AM - Documentation update
12:00 PM - Ticket closure
14:00 PM - New alerts batch processing
16:00 PM - Metrics reporting
17:00 PM - Shift end
```

### আপনার সাফল্যের মেট্রিক্স:

- **Alert handling time** - যত তাড়াতাড়ি সম্ভব
- **False positive accuracy** - FP কত% ধরতে পারছেন
- **Escalation rate** - কত% properly escalate করছেন
- **MTTA (Mean Time To Acknowledge)** - কত দ্রুত alert acknowledge করছেন

---

## Key Concepts সারসংক্ষেপ

| Concept | মানে | উদাহরণ |
|---------|------|--------|
| **Threat** | সম্ভাব্য ক্ষতিকর activity | Attacker এর attempt |
| **Vulnerability** | System এর দুর্বলতা | Unpatched software |
| **Risk** | Threat + Vulnerability = ক্ষতির সম্ভাবনা | Attacker + weak password |
| **Alert** | Suspicious activity detection | Unusual login detected |
| **Incident** | Confirmed security event | Confirmed data breach |
| **Detection** | Threat খুঁজে পাওয়া | Alert generated |
| **Investigation** | কি ঘটেছে তা বুঝা | Root cause analysis |
| **Response** | ক্ষতি কমানো | Attacker block করা |

---

## Common Mistakes L1 Analysts করে

### ❌ **Mistake 1: প্রতিটি alert investigate করা**

**সমস্যা:** False positives এ সময় নষ্ট করা

**সমাধান:** Severity এবং context দেখে prioritize করুন

---

### ❌ **Mistake 2: Documentation skip করা**

**সমস্যা:** পরে কেউ context বুঝতে পারে না

**সমাধান:** প্রতিটি alert এ "What", "Why", "Finding" লিখুন

---

### ❌ **Mistake 3: L2 এর সাথে communicate না করা**

**সমস্যা:** অনেক escalation reject হয়

**সমাধান:** প্রমাণ ও context সহ escalate করুন

---

### ❌ **Mistake 4: Alert properties ignore করা**

**সমস্যা:** Important context মিস করা

**সমাধান:** Timestamp, source, destination, user সব check করুন

---

### ❌ **Mistake 5: Same alert বার বার investigate করা**

**সমস্যা:** Time waste

**সমাধান:** Similar alerts এর pattern detect করুন

---

## Practical Checklist: SOC L1 Mindset

আপনি যখন প্রথম দিন SOC তে join করবেন:

**✅ Day 1-3: Learning Phase**
- [ ] Company security policy পড়ুন
- [ ] SIEM dashboard familiarize করুন
- [ ] Alert types বুঝুন
- [ ] Mentor এর সাথে কাজ করুন
- [ ] Previous investigation cases দেখুন

**✅ Week 1: Hands-on Phase**
- [ ] একা simple alerts investigate করুন
- [ ] Documentation practice করুন
- [ ] Escalation decision practice করুন
- [ ] Team members এর সাথে chat করুন
- [ ] Playbooks read করুন

**✅ Week 2-4: Independence Phase**
- [ ] Alert handling volume বাড়ান
- [ ] Decision speed improve করুন
- [ ] FP accuracy track করুন
- [ ] First escalation করুন
- [ ] Process optimization suggest করুন

**✅ Month 2+: Expert Phase**
- [ ] New alert rules suggest করুন
- [ ] Junior analysts mentor করুন
- [ ] Runbooks improve করুন
- [ ] Trending threats identify করুন

---

## Mini Quiz: নিজেকে পরীক্ষা করুন

### **Question 1: CIA Triad এর কোন part যদি compromise হয় যখন attacker password change করে?**

A) Confidentiality  
B) Integrity  
C) Availability  
D) All three

**Answer:** B) Integrity - কারণ data modified হয়েছে (গোপনীয়তা বা প্রাপ্যতা যদিও effect পরতে পারে)

---

### **Question 2: In-house SOC এবং Managed SOC এর মধ্যে কোনটি more control দেয়?**

A) Managed SOC  
B) In-house SOC  
C) Both same  
D) Depends on agreement

**Answer:** B) In-house SOC - কারণ নিজের টিম সম্পূর্ণ control রাখে

---

### **Question 3: L1 Analyst এর প্রধান কাজ কোনটি?**

A) Advanced malware analysis  
B) SIEM development  
C) Alert triage এবং initial investigation  
D) Budget management

**Answer:** C) Alert triage এবং initial investigation - এটাই L1 এর main responsibility

---

### **Question 4: SOC monitoring cycle এর প্রথম step কোনটি?**

A) Investigation  
B) Detection  
C) Response  
D) Reporting

**Answer:** B) Detection - প্রথমে threat detect করতে হবে, তারপর investigate, তারপর respond

---

### **Question 5: False Positive কি?**

A) একটি real threat যা detect হয়েছে  
B) একটি benign activity যা threat মনে হয়েছে  
C) একটি missed threat  
D) একটি incident যা escalate হয়েছে

**Answer:** B) একটি benign activity যা threat মনে হয়েছে - এটাই false positive। L1 এর কাজ এগুলো filter করা।

---

## সহজ ভাষায় সারসংক্ষেপ

**SOC হল একটি security team যারা:**
- 24/7 threats monitor করে
- আপনার company এর data protect করে
- CIA Triad maintain করতে কাজ করে
- In-house হতে পারে বা Managed

**আপনি L1 Analyst হিসেবে:**
- Alert দ্রুত check করবেন
- False positives filter করবেন
- Suspicious activity escalate করবেন
- সবকিছু document করবেন

**আপনার লক্ষ্য:**
- অনেক alerts efficiently handle করা
- High accuracy maintain করা
- L2 কে value add করা
- Gradually advanced become করা

---

## পরবর্তী মডিউল দিকে

আপনি এখন জানেন:
- ✅ SOC কি
- ✅ CIA Triad
- ✅ In-house vs Managed SOC
- ✅ SOC টিম structure
- ✅ আপনার role

**পরবর্তীতে:** Module 2 - "SOC Team Structure এবং Responsibilities" যেখানে আমরা আরো deep dive করব প্রতিটি role এবং তাদের interaction নিয়ে।

---

## Resources for Learning

**Recommended Reading:**
1. SANS SOC Analyst perspective
2. NIST Cybersecurity Framework
3. আপনার company এর security policy documentation
4. SIEM vendor এর training materials

**Online Resources:**
- TryHackMe - SOC Level 1 Path
- Cybrary - Cybersecurity fundamentals
- Professor Messer - Network fundamentals (YouTube)

---

**Module 1 Complete! ✅**

