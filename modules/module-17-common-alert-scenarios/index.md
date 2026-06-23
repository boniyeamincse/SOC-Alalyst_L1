# Module 17: Common SOC L1 Alert Scenarios

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- 10টি সাধারণ alert type যা L1 দেখে
- প্রতিটি scenario এ investigate করা
- Common findings এবং verdict patterns
- কিভাবে distinguish করা: FP vs TP
- Investigation examples real data সাথে
- Quick decision frameworks
- Red flags for each scenario
- Playbook recommendations

---

## শুরুর আগে: একটি গল্প

নাফিস তার প্রথম সপ্তাহ SOC তে। Alert types এর pattern দেখছে:

**Week 1:**
```
Monday: Brute force alert
Tuesday: Unusual login location
Wednesday: Phishing email
Thursday: Malware detected
Friday: Data transfer alert
```

এই module এ তিনি শিখবে: প্রতিটি scenario মানে কি, কীভাবে investigate, কখন escalate।

---

## 10 Common Alert Scenarios

### **Scenario 1: Brute Force Attack (Login Attempts)**

**Alert trigger:**
```
Multiple failed login attempts in short time window
Threshold: 5+ failures in 5 minutes
```

**Investigation steps:**

```
Step 1: Verify alert accuracy
├─ Count: How many failures?
├─ Time: How fast (1 minute? 10 minutes?)
├─ Target: Which system/account?
└─ Source: Single IP or multiple?

Step 2: Identify source
├─ Source IP: Internal or external?
├─ VPN: Is it VPN IP?
├─ Reputation: Known malicious?
└─ Pattern: Distributed or single?

Step 3: Identify target
├─ Account: Real account?
├─ User: Legitimate or service?
├─ Access level: Admin or regular?
└─ History: Ever been attacked?

Step 4: Check for success
├─ Successful login? After failures?
├─ Timing: How soon after?
├─ From same IP: Yes or different?
└─ This is CRITICAL
```

**Common findings & verdicts:**

```
Finding: Service account, nightly schedule
Verdict: FALSE_POSITIVE (backup script retry)

Finding: External IP, 50 failures, 1 success after
Verdict: TRUE_POSITIVE (account compromised)

Finding: Internal user, 3 failures, typo password
Verdict: FALSE_POSITIVE (user error)

Finding: Distributed IPs, 1000+ failures per IP
Verdict: TRUE_POSITIVE (DDoS/bot attack)
```

**Red flags:**

```
❌ Successful login after failures
❌ From unexpected location
❌ High-privilege account targeted
❌ Distributed from many IPs
❌ Account disabled but still attempts
```

**Quick decision:**

```
Decision tree:
├─ Success after failures? → Escalate (compromise)
├─ From known VPN? → Probably FP (working remote)
├─ Service account + schedule? → FP (automation)
├─ External + high-privilege? → Escalate
├─ Distributed IPs? → Escalate
└─ Single internal IP + typo? → Close (user error)
```

---

### **Scenario 2: Unusual Login Location (Impossible Travel)**

**Alert trigger:**
```
User login from geographically impossible location
Example: Login from India at 10:00, then Singapore at 10:05
```

**Investigation steps:**

```
Step 1: Verify locations
├─ Location 1: Where is it?
├─ Location 2: Where is it?
├─ Distance: How far apart?
├─ Time: How much time between?
└─ Travel time: Is it possible?

Step 2: Check business context
├─ Business travel approved? (Calendar)
├─ Employee location: Where should they be?
├─ Time zone: Different TZ = different hours?
└─ VPN: Are they on company VPN?

Step 3: Verify with user
├─ Contact: Ask about travel
├─ Approval: Was it approved?
├─ Dates: When were they traveling?
└─ Details: Do dates match logins?

Step 4: Check account activity
├─ Typical access: What's normal?
├─ Session duration: How long logged in?
├─ Data access: What did they access?
└─ Devices: Any new devices?
```

**Common findings & verdicts:**

```
Finding: Business trip approved, calendar shows travel
Verdict: FALSE_POSITIVE (expected travel)

Finding: VPN from Singapore after India, 30 min apart
Verdict: FALSE_POSITIVE (VPN makes location unclear)

Finding: Impossible travel (physical travel impossible)
Verdict: TRUE_POSITIVE (account compromise/spoofing)

Finding: First time overseas, no approval
Verdict: SUSPICIOUS (investigate more)
```

**Red flags:**

```
❌ No travel approved
❌ Impossible travel time (1000 km in 5 min)
❌ Multiple countries in one day (unusual)
❌ New unusual location (employee never there)
❌ Coincides with data access
```

**Quick decision:**

```
├─ Travel approved + calendar matches? → Close
├─ On VPN? → Probably close (VPN obscures location)
├─ Physically impossible? → Escalate
├─ New location + no approval? → Escalate
├─ Timezone difference explains? → Close
└─ Uncertain? → Contact manager
```

---

### **Scenario 3: Successful Login After Brute Force**

**Alert trigger:**
```
Sequence: Multiple failed logins THEN one successful login
```

**Investigation steps:**

```
CRITICAL: This is strong compromise indicator

Step 1: Verify sequence
├─ Failures first: Confirmed?
├─ Success after: From same source?
├─ Timing: How long between?
└─ Username: Same account?

Step 2: Analyze source
├─ IP: External or internal?
├─ Reputation: Known malicious?
├─ ASN: What ISP/datacenter?
├─ VPN: Is it VPN IP?

Step 3: Check post-login activity
├─ What did attacker do?
├─ Systems accessed: Which?
├─ Files: What data touched?
├─ Escalation: Any admin actions?
└─ This indicates damage extent
```

**Common findings & verdicts:**

```
Finding: 50 failures, 1 success, then suspicious file access
Verdict: TRUE_POSITIVE (confirmed compromise)

Finding: Failures from script, success also script (nightly)
Verdict: FALSE_POSITIVE (script with wrong password)

Finding: Failures external, success internal (different IPs)
Verdict: NEED INVESTIGATION (complicated)
```

**Red flags:**

```
❌ Multiple sources failing, one succeeding
❌ Success followed by:
  ├─ Data access unusual
  ├─ Privilege escalation
  ├─ File download/exfil
  └─ Account creation
❌ Rapid subsequent activity
```

**Decision:**

```
This pattern = Almost always escalate
├─ Even if "looks normal"
├─ Sequence of failures+success = Attack pattern
└─ Escalate to L2/IR immediately
```

---

### **Scenario 4: Phishing Email**

**Alert trigger:**
```
Email detected as phishing
Usually by content scan + URL/domain reputation
```

**Investigation steps:**

```
Step 1: Verify phishing indicators
├─ Sender: Spoofed? Check SPF/DKIM
├─ Links: Point to phishing site?
├─ Attachment: Malware?
├─ Content: Looks legitimate but fake?

Step 2: Check user action
├─ Did user receive: Yes?
├─ Did user click: Yes/No? (CRITICAL)
├─ Did user download: Yes/No?
├─ Did user enter creds: Yes/No? (CRITICAL)

Step 3: Assess damage
├─ If no action: Low risk
├─ If clicked: Possible infection (check endpoint)
├─ If downloaded: Possible malware (check hash)
├─ If entered credentials: Possible account compromise
```

**Common findings & verdicts:**

```
Finding: Phishing email, user didn't interact
Verdict: FALSE_POSITIVE (caught by filter)

Finding: Phishing, 50 users received, 1 clicked link
Verdict: ESCALATE (possible infection)

Finding: Phishing, user entered credentials
Verdict: ESCALATE (credential compromise + password reset)

Finding: Looks like phishing but actually legitimate
Verdict: FALSE_POSITIVE (update filters)
```

**Red flags:**

```
❌ Widespread: Many recipients
❌ User interacted: Clicked, downloaded, entered info
❌ Known phishing campaign: Same pattern before
❌ Targets executives/finance
❌ Attachment is executable
```

**Decision:**

```
├─ Phishing + user interacted? → Escalate
├─ Phishing + no interaction? → Close + educate
├─ Attachment malware? → Escalate
├─ Credentials entered? → Escalate
└─ Widespread campaign? → Escalate as incident
```

---

### **Scenario 5: Suspicious PowerShell**

**Alert trigger:**
```
PowerShell execution with suspicious commands
Patterns: Encoding, obfuscation, system modification
```

**Investigation steps:**

```
Step 1: Get command details
├─ Command: What was executed?
├─ Encoding: Obfuscated or plain?
├─ Purpose: What does command do?
└─ Risk: Admin? Data access? Network?

Step 2: Identify source
├─ User: Who ran it?
├─ Device: Which computer?
├─ Context: Admin or regular user?
├─ Permission: Had permission?

Step 3: Check legitimacy
├─ Admin task: Expected?
├─ Management tool: Legitimate tool?
├─ Script: Legitimate script?
├─ Documentation: Is there ticket?

Step 4: Check for impact
├─ Files: Modified?
├─ Registry: Changed?
├─ Network: Connections made?
├─ Escalation: Privileges gained?
```

**Common findings & verdicts:**

```
Finding: Admin running encoded script during maintenance
Verdict: FALSE_POSITIVE (admin task)

Finding: Regular user, Base64 encoded command, C2 connection
Verdict: TRUE_POSITIVE (malware execution)

Finding: Management tool (Puppet, Chef), legitimate
Verdict: FALSE_POSITIVE (automation tool)

Finding: System admin running update script
Verdict: DEPENDS (verify script + timing)
```

**Red flags:**

```
❌ Encoded/obfuscated commands (why hide?)
❌ Non-admin user running PowerShell
❌ Network connections after execution
❌ File/registry modifications suspicious
❌ Downloaded script then executed
❌ Scheduled task creation
```

**Decision:**

```
├─ Admin running known script? → Probably OK
├─ Regular user + encoded command? → Escalate
├─ Network connection suspicious? → Escalate
├─ User not expected to run PS? → Escalate
└─ Can't determine legitimacy? → Escalate
```

---

### **Scenario 6: Malware Detection**

**Alert trigger:**
```
Malware signature match or behavior detection
Antivirus/EDR flagged file as malicious
```

**Investigation steps:**

```
Step 1: Verify detection
├─ File: Hash, name, path
├─ Signature: What malware detected?
├─ Confidence: Vendor consensus?
├─ False positive rate: Known bad vendors?

Step 2: Identify source
├─ Where found: Disk, memory, network?
├─ How arrived: Downloaded? Email? USB?
├─ User: Who accessed?
├─ When: How old file?

Step 3: Assess impact
├─ Executed: Running?
├─ Spread: Multiple systems?
├─ Persistence: Installed for long term?
├─ C2: Calling home? Network activity?

Step 4: Determine action
├─ Isolation: Isolate device?
├─ Cleanup: Malware removed?
├─ Forensics: Needed?
└─ Escalation: Incident level?
```

**Common findings & verdicts:**

```
Finding: Known malware, quarantined, no execution
Verdict: BENIGN (caught + contained)

Finding: Malware hash, 50 vendors detect, C2 connection
Verdict: TRUE_POSITIVE (confirmed infection)

Finding: PUP (possibly unwanted), single vendor flags
Verdict: FALSE_POSITIVE (likely adware, not critical)

Finding: File in quarantine, never executed
Verdict: BENIGN (security working)
```

**Red flags:**

```
❌ Multiple vendors detect (consensus)
❌ C2 network connections
❌ Execution confirmed
❌ Spread to multiple devices
❌ Persistence mechanisms
❌ Running with high privileges
```

**Decision:**

```
├─ Quarantined + not executed? → Close
├─ Multiple vendors + execution? → Escalate
├─ Known ransomware family? → Escalate immediately
├─ Spreading to other systems? → Escalate
└─ Uncertain? → Isolate + Escalate
```

---

### **Scenario 7: Data Exfiltration**

**Alert trigger:**
```
Large data transfer to external IP/location
Unusual volume or suspicious destination
```

**Investigation steps:**

```
Step 1: Verify transfer
├─ Volume: How much data?
├─ Destination: Where is it going?
├─ Protocol: What method? (FTP, SFTP, S3, etc)
├─ Timing: Normal business hours or off-hours?

Step 2: Identify source
├─ User: Who initiated?
├─ Device: Which system?
├─ Access: Do they normally download data?
└─ Context: Business reason?

Step 3: Analyze destination
├─ IP reputation: Known malicious?
├─ ASN: What organization?
├─ DNS: What domain?
├─ Previous: Contacted before?

Step 4: Assess business context
├─ Approved transfer? (Ticket)
├─ Business partner? (Known relationship)
├─ Backup: Is it backup activity?
└─ Regular: Does user do this?
```

**Common findings & verdicts:**

```
Finding: Backup software, scheduled transfer, known destination
Verdict: FALSE_POSITIVE (normal backup)

Finding: 500 MB to unknown IP, off-hours, C2 IP
Verdict: TRUE_POSITIVE (data exfiltration)

Finding: Monthly report to auditor, approved, business partner
Verdict: FALSE_POSITIVE (legitimate business)

Finding: User downloads 1 GB after accessing database
Verdict: SUSPICIOUS (needs investigation)
```

**Red flags:**

```
❌ Unusual volume (10x normal)
❌ Off-hours transfer
❌ External IP known malicious
❌ Sensitive data (database, financial)
❌ Compressed files (harder to detect)
❌ Encrypted tunnel
```

**Decision:**

```
├─ Approved business transfer? → Close
├─ Backup to known location? → Close
├─ Unknown destination + large volume? → Escalate
├─ Off-hours + sensitive data? → Escalate
├─ C2 destination? → Escalate immediately
└─ Uncertain? → Escalate
```

---

## Alert Verdict Quick Reference

**Scenarios by Common Verdict:**

```
Usually FALSE_POSITIVE:
├─ Backup script retrying
├─ Admin maintenance activity
├─ Approved business transfer
├─ VPN login from travel
├─ Email caught by filter (not opened)
├─ Test/lab activity
└─ User typo (few failed attempts)

Usually TRUE_POSITIVE:
├─ Successful login after brute force
├─ Malware with multiple vendor consensus
├─ C2 network connections
├─ Distributed brute force
├─ Phishing + user interacted
├─ Suspicious escalation + access
└─ Known malware family

Usually SUSPICIOUS (escalate):
├─ Unusual location, no travel approved
├─ Behavioral anomaly (new pattern)
├─ Missing business context
├─ Impossible travel
├─ Data access anomaly
└─ Unclear legitimacy

Usually BENIGN:
├─ Expected admin activity
├─ Approved travel + location match
├─ Known automation pattern
├─ Quarantined malware (not executed)
└─ Test/intentional activity
```

---

## Investigation Workflow for L1

**Generic workflow (works for all scenarios):**

```
ALERT RECEIVED
    │
    ▼
1. TRIAGE (5 min)
   ├─ What alert type?
   ├─ Severity appropriate?
   └─ Continue or escalate immediately?

2. INITIAL INVESTIGATION (5 min)
   ├─ Verify alert is accurate
   ├─ Get basic context
   └─ Any immediate red flags?

3. IDENTITY ENRICHMENT (2 min)
   ├─ User: Legitimate?
   ├─ Status: Active/disabled?
   └─ Normal behavior?

4. ASSET ENRICHMENT (2 min)
   ├─ System: What is it?
   ├─ Criticality: How important?
   └─ Data: Sensitive?

5. THREAT INTEL (2 min)
   ├─ IP/Domain reputation?
   ├─ File hash verdict?
   └─ Known threat?

6. BEHAVIOR ANALYSIS (2 min)
   ├─ Pattern: Expected?
   ├─ Timeline: Sequence makes sense?
   └─ Correlated events?

7. CONTEXT (1 min)
   ├─ Business reason?
   ├─ Ticket/approval?
   └─ Previous similar?

8. VERDICT (1 min)
   ├─ Close? (FP or BENIGN)
   ├─ Escalate? (TP or SUSPICIOUS)
   └─ Need more info? (Escalate with questions)

TOTAL TIME: 15-20 minutes
```

---

## Common Mistakes by Scenario

```
❌ Brute Force:
   └─ Not checking for successful login after
   
❌ Impossible Travel:
   └─ Not considering VPN (obscures location)
   
❌ Phishing:
   └─ Not checking if user actually clicked
   
❌ PowerShell:
   └─ Closing immediately (admin context needed)
   
❌ Malware:
   └─ Over-reacting to single vendor detection
   
❌ Data Transfer:
   └─ Not checking backup software
   
❌ All scenarios:
   └─ Not checking business context/tickets
   └─ Not enriching fully
   └─ Not escalating uncertain
   └─ Not documenting findings
```

---

## Mini Quiz: Scenarios

### **Question 1: Successful login after 50 failed attempts?**

A) False positive (typo)  
B) Benign (user error)  
C) True positive (account compromise)  
D) Needs more data

**Answer:** C) True positive (account compromise) - This pattern = attack success

---

### **Question 2: Login from Singapore, then India 30 min later?**

A) Impossible travel (escalate)  
B) False positive if approved travel  
C) Check if VPN (may be on VPN)  
D) All above

**Answer:** D) All above - Context determines verdict

---

### **Question 3: Malware detected by 1 vendor, quarantined?**

A) Definitely malware (escalate)  
B) Definitely false positive  
C) Assess: vendor reliability + execution  
D) Always escalate malware

**Answer:** C) Assess: vendor reliability + execution - Single vendor = check quality + confirm execution

---

### **Question 4: PowerShell by IT admin during maintenance?**

A) Always suspicious (escalate)  
B) Probably legitimate (verify script + ticket)  
C) Close immediately (admin work)  
D) Never investigate admin

**Answer:** B) Probably legitimate (verify script + ticket) - Context = admin task probably ok

---

### **Question 5: 500 MB data transfer to known auditor?**

A) Suspicious (escalate)  
B) False positive if approved + business partner  
C) Always escalate large transfers  
D) Close without context

**Answer:** B) False positive if approved + business partner - Business context = legitimate

---

## সহজ ভাষায় সারসংক্ষেপ

**7 Common Scenarios:**

1. **Brute Force:** Multiple failures → check for success after
2. **Impossible Travel:** Different locations → check travel approval
3. **Success After Failures:** Attack pattern → usually escalate
4. **Phishing:** Email detected → check if user clicked
5. **PowerShell:** Suspicious command → verify context/ticket
6. **Malware:** Signature match → check execution + consensus
7. **Data Exfiltration:** Large transfer → verify business reason

**Investigation Pattern:**
1. Triage (alert accurate?)
2. Identity (user legitimate?)
3. Asset (system type?)
4. TI (reputation?)
5. Behavior (expected?)
6. Context (business reason?)
7. Verdict (close or escalate?)

**Quick Rules:**
- Brute force + success → Escalate
- Impossible travel + no approval → Escalate
- Phishing + user clicked → Escalate
- PowerShell + encoded → Escalate
- Malware + execution → Escalate
- Data transfer + no ticket → Escalate
- Uncertain → Escalate

**Common Verdict:**
- FP: Backup, automation, approved transfer, test
- TP: Compromise, malware consensus, C2, escalation
- BENIGN: Admin work, expected pattern, caught before execution
- SUSPICIOUS: Unclear context, missing approval, anomaly

---

## Resources for Learning

**Your company playbooks:**
- Brute force playbook
- Phishing playbook
- Malware playbook
- Data exfiltration playbook

**Learning resources:**
- SANS resources
- Cybrary scenarios
- TryHackMe SOC labs
- Your L2 mentor

---

**Module 17 Complete! ✅**

এখন আপনি জানেন:
- ✅ 7টি common alert scenarios
- ✅ প্রতিটি scenario investigation steps
- ✅ Common findings এবং verdicts
- ✅ Red flags for each scenario
- ✅ Quick decision frameworks
- ✅ Real-world patterns
- ✅ Generic L1 investigation workflow
- ✅ Common mistakes by scenario
- ✅ Verdict prediction patterns

Progress: **17 of 28 modules complete (61%)**

---

<!-- nav-footer -->
## 🧭 Navigation

| | |
|---|---|
| **Previous** | [⬅️ Module 16: SIEM Investigation](../module-16-siem-investigation/index.md) |
| **Next** | [Module 18: Alert Reporting ➡️](../module-18-alert-reporting/index.md) |
| **🏠 Course Home** | [STUDY_NOTES.md](../../STUDY_NOTES.md) |
