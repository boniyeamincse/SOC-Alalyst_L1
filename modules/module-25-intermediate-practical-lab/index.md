# Module 25: Intermediate Practical Lab

## Lab Objective

Complex real-world scenario requiring:
- Multi-system investigation
- Difficult verdict decision
- Escalation judgment
- Red flags + FP indicators mixed
- Root cause analysis

---

## Lab Scenario

**Date:** 2024-06-21  
**Your Role:** L1 SOC Analyst - Morning Shift  
**Time:** 11:45 IST

---

## ALERT RECEIVED

```
Alert ID: #3921
Alert Name: Suspicious Process Execution
Severity: MEDIUM
Timestamp: 2024-06-21 11:30:15 IST
System: employee_workstation_42
User: sarah.ali@company.com
Process: powershell.exe
Command: Encoded Base64 string (truncated)
Parent process: explorer.exe
EDR Status: Detected as suspicious
Confidence: 72%
```

---

## Your Task - Complete Investigation

### STEP 1: TRIAGE (2 minutes)

**Question:** Is alert legitimate?

```
INITIAL ASSESSMENT:
├─ Alert type: Suspicious process (medium-high risk)
├─ Detection method: EDR behavioral
├─ Confidence: 72% (moderate)
├─ User impact: Single workstation
├─ Time: Recent (15 min ago)
├─ Verdict so far: Needs investigation

STATUS: Continue investigation
```

---

### STEP 2: GATHER EVIDENCE - Process Details

**SIEM/EDR Data - Process Tree:**

```
Process Chain:
├─ explorer.exe (PID: 4532)
│  └─ Parent: winlogon.exe
│  └─ Started: 2024-06-21 09:00:00 (legitimate)
│
├─ powershell.exe (PID: 7841) ← SUSPICIOUS
│  └─ Parent: explorer.exe (unusual - not svchost)
│  └─ Started: 2024-06-21 11:30:12
│  └─ User context: sarah.ali@company.com
│  └─ Command line: (BASE64 ENCODED - see below)
│  └─ Privileges: User level (not admin)
│
└─ Command executed:
   └─ Base64 decoded: "Get-ChildItem C:\Users\sarah.ali\Documents"
```

**EDR Alert Details:**

```
Alert reason: Encoded PowerShell execution
Behavioral flag: Parent process unusual (explorer not normal)
Risk: Medium (72% confidence)
Previous alerts on system: None in past 30 days
EDR agent status: Active, up-to-date
Execution blocked: NO (monitoring only)
```

---

### STEP 3: GATHER EVIDENCE - User Activity

**SIEM Data - User Activity (last 24 hours):**

```
User: sarah.ali@company.com
├─ Logins:
│  ├─ 2024-06-21 09:00:00 - Office IP (10.0.2.150)
│  ├─ 2024-06-21 09:02:00 - Same location
│  └─ No additional logins
│
├─ File access:
│  ├─ Documents folder: Multiple accesses (normal)
│  ├─ C:\Users\sarah.ali\Documents: READ only
│  └─ Sensitive folders: NO access
│
├─ Network activity:
│  ├─ Outbound: Office DNS queries (normal)
│  ├─ Web: Internal sites only
│  ├─ No external C2: Checked, none found
│  └─ No data transfer: Confirmed
│
└─ Application logs:
   ├─ PowerShell ISE: Opened at 11:28
   ├─ No scripts downloaded
   └─ Local script execution (none detected)
```

---

### STEP 4: IDENTITY ENRICHMENT

**Question:** Who is sarah.ali?

```
AD Information:
├─ Name: Sarah Ali
├─ Department: Finance
├─ Job Title: Senior Financial Analyst
├─ Status: ACTIVE
├─ Employment: Full-time
├─ Email: sarah.ali@company.com
├─ Groups: Finance team, Finance_Reports, Reporting_Access
├─ Admin rights: NO (standard user)
├─ Last password change: 2024-06-01
├─ Account age: 4 years
└─ Previous incidents: NONE

Manager: robert.kim@company.com
HR record: Excellent performance, no flags
Travel: No approved travel (in office expected)
Calendar: Normal working hours
```

---

### STEP 5: ASSET ENRICHMENT

**Question:** What's the target system?

```
System: employee_workstation_42
├─ Type: Standard workstation
├─ User: sarah.ali
├─ OS: Windows 10 (current patch)
├─ Criticality: Low (standard employee)
├─ Data access: Finance reports only
├─ Network: Office subnet (10.0.2.0/24)
├─ Monitoring: EDR + SIEM
├─ Security: Standard baseline
└─ Previous incidents: NONE (clean history)
```

---

### STEP 6: BEHAVIOR ANALYSIS

**Question:** Is PowerShell execution normal?

```
Historical analysis:
├─ PowerShell usage (sarah.ali): Rare
├─ Previous PS execution: 1 time (3 months ago)
│  └─ Context: Script to generate report
│  └─ Legitimate: YES
│
├─ Timing: 11:30 (business hours, normal)
├─ Parent process: explorer.exe (UNUSUAL)
│  └─ Normal: svchost.exe or user-initiated
│  └─ This: User clicked .ps1 or ran from Explorer
│
├─ Command: Get-ChildItem Documents
│  └─ Risk: LOW (just listing files)
│  └─ Legitimate? YES (normal file operation)
│  └─ Encoding: WHY? (unusual)
│
└─ RED FLAG: Why encode simple command?
   └─ Legitimate: Sometimes for escaping characters
   └─ Malicious: Sometimes to hide activity
   └─ Unclear: Needs more investigation
```

---

### STEP 7: THREAT INTEL CHECK

**Question:** Any known malware indicators?

```
Process name: powershell.exe
├─ Reputation: Legitimate system binary
├─ Hash: SHA256: 1234...abcd (standard Windows)
├─ Signature: Microsoft signed
└─ Known malware: NO

Command analysis: "Get-ChildItem C:\Users\sarah.ali\Documents"
├─ Known malicious: NO
├─ Matches known attack: NO
├─ C2 signature: NO
├─ Data exfil pattern: NO
└─ Verdict: Benign command

Encoding: Base64
├─ Indicator of compromise: SOMETIMES
├─ Also legitimate: SOMETIMES (character escaping)
└─ Inconclusive
```

---

### STEP 8: DEEPER INVESTIGATION - Interview

**Scenario Data - Chat with Sarah (11:45 IST):**

```
You: "Hi Sarah, alert triggered for PowerShell 
     on your workstation at 11:30. Can you explain?"

Sarah: "Oh, yeah, I was listing files in my 
        Documents folder. I use PowerShell sometimes 
        for work. Is that a problem?"

You: "You wrote the PowerShell command?"

Sarah: "Actually, no. I had our IT team send me 
        a script last week for reporting. I tried 
        running it today but couldn't get it to 
        work. I was checking if the files it 
        references exist."

You: "Who from IT?"

Sarah: "Robert Kumar from IT. He sent me an 
        email... let me find it. Here's the 
        ticket: #5234."
```

---

### STEP 9: EVIDENCE FOLLOW-UP

**Scenario Data - IT Ticket #5234:**

```
Ticket ID: #5234
Date opened: 2024-06-15
Opened by: sarah.ali
Assigned to: robert.kumar@company.com
Subject: Help with reporting script

Description:
"Need to run monthly financial reports. Robert 
suggested using PowerShell for efficiency. He 
sent me a script. Running it gives encoding 
errors. Need help debugging."

Response (2024-06-16):
"Sarah, I'll send you the corrected script. 
The encoding issue is because the paths have 
special characters. I'll base64 encode it for 
you to avoid escaping issues. Run it to test 
the file references first."

Script received: 2024-06-16
Script: PowerShell script (reporting_v2.ps1)
├─ Purpose: Monthly financial report generation
├─ Uses: Read-only file access
├─ Admin: NOT required
└─ Legitimate: YES

Status: CLOSED (2024-06-20)
Note: "Script working now. Thanks!"
```

---

### STEP 10: VERIFY IT TEAM

**Scenario Data - IT Team Verification:**

```
Contact: robert.kumar@company.com
Title: IT Support Specialist
Department: IT Infrastructure
Employment: Active, 8 years
Legitimate: YES

Ticket verification:
├─ Ticket #5234: EXISTS
├─ Email sent: YES (confirmed in mail logs)
├─ Script attachment: YES
├─ File: reporting_v2.ps1
├─ Purpose documented: YES (finance reports)
└─ No security concerns noted

Script analysis:
├─ File hash: SHA256: 5678...efgh
├─ Virus scan: CLEAN
├─ Signature: Not signed (internal script)
├─ Content: Finance reporting functions only
├─ Malware indicators: NONE
└─ Legitimate: HIGH confidence
```

---

### STEP 11: CORRELATION - Put It Together

**Question:** What's the full story?

```
TIMELINE:
├─ 2024-06-15: Sarah needs reporting help
├─ 2024-06-16: IT sends base64-encoded script
├─ 2024-06-16: Sarah tests script (works)
├─ 2024-06-20: Ticket closed (script working)
├─ 2024-06-21 11:28: Sarah opens PowerShell ISE
├─ 2024-06-21 11:30: Sarah runs file check command
└─ 2024-06-21 11:30: EDR alerts (encoded PS)

FINDINGS:
├─ User: Legitimate (4 year employee, clean)
├─ System: Standard workstation (no criticality)
├─ Process: PowerShell (legitimate system binary)
├─ Command: Get-ChildItem (benign operation)
├─ Encoding: Explained by IT script issue
├─ Business context: Reporting script (legitimate)
├─ IT verification: Confirmed legitimate
├─ No data exfil: CONFIRMED
├─ No compromise: CONFIRMED
├─ No malware: CONFIRMED
└─ No escalation: Not needed

ROOT CAUSE:
Legitimate user running legitimate IT-approved
script with base64 encoding (explained by file
path escaping issue). EDR correctly detected
encoded PowerShell but alert confidence only 72%
(correctly moderate risk). Investigation confirms
no threat.
```

---

### STEP 12: DECISION - VERDICT

**Question:** What's the verdict?

```
ASSESSMENT:
├─ True Positive? NO
├─ False Positive? YES (likely)
├─ Benign? YES
├─ Suspicious? NO (once investigated)

EVIDENCE WEIGHT:
RED FLAGS (innocent explanation):
├─ Encoded PowerShell (due to script fix)
├─ Unusual parent process (user clicked file)
├─ No admin rights (benign command)
└─ All have business explanation

CONFIDENCE FACTORS:
✓ User verified legitimate
✓ IT ticket documented
✓ Script verified clean
✓ Business reason clear
✓ No data exfil
✓ No malware
✓ Historical context matches
✓ All evidence consistent

VERDICT: BENIGN (or FALSE_POSITIVE)

Confidence: HIGH (88%)
Risk: LOW (no threat indicators)
Escalation: NOT REQUIRED
Action: Close and document
```

---

### STEP 13: DOCUMENTATION

**Ticket Response:**

```
ALERT #3921 - SUSPICIOUS PROCESS EXECUTION

Investigation Complete: BENIGN

Summary:
Alert detected encoded PowerShell execution on 
sarah.ali's workstation. Investigation confirms 
legitimate business use - user running IT-approved 
reporting script with base64 encoding to handle 
file path escaping.

What Happened:
├─ User: Sarah Ali (Finance Senior Analyst)
├─ Process: powershell.exe (encoded command)
├─ Command: Get-ChildItem Documents (file check)
├─ Reason: Testing IT-provided reporting script
├─ IT support: Ticket #5234 (documented)
├─ Status: Normal business activity

Evidence Collected:
├─ IT ticket #5234 (reporting script)
├─ Robert Kumar confirmation (IT)
├─ Script verification (clean, no malware)
├─ User interview (confirms legitimate use)
├─ File access logs (documents only, no exfil)
├─ Network logs (no C2, no external comm)
├─ EDR process tree (legitimate binary, user-level)
└─ Historical context (matches expected behavior)

Analysis:
RED FLAGS present (encoded PS, unusual parent):
├─ Explained by: Script base64 encoding
├─ Reason: File path character escaping
├─ Context: IT-recommended approach
├─ Legitimate: Confirmed through ticket #5234

BLUE INDICATORS:
├─ User: 4-year employee, Finance dept, no incidents
├─ System: Standard workstation, no criticality
├─ Command: Get-ChildItem (benign file operation)
├─ Business: Legitimate reporting work
├─ Data: Read-only access, no exfil
├─ Malware: Script scanned clean
└─ No compromise: Any indicators checked

Why Alert Triggered:
EDR correctly detected encoded PowerShell (72% 
confidence - appropriately medium). However, full 
investigation reveals benign business use with 
legitimate IT support context.

Recommendation:
1. CLOSE as BENIGN
2. Document as legitimate reporting process
3. No further action needed
4. EDR tuning: Consider whitelisting approved 
   IT reporting scripts to reduce noise

Playbook: "Suspicious Process Execution" (PB-0045)
Investigation Time: 22 minutes
Confidence: HIGH (88%)
Status: CLOSED - BENIGN
```

---

## What Made This Harder

### Compared to Module 24:

```
Module 24 (Beginner):
├─ Clear root cause (password mismatch)
├─ Service account context obvious
├─ No real red flags
└─ Verdict clear early

Module 25 (Intermediate):
├─ Multiple red flags mixed with legitimate
├─ User context needs verification
├─ Requires interview/follow-up
├─ Needs IT confirmation
├─ More detective work
└─ Verdict less obvious initially
```

---

## Assessment

### Question 1: Initial verdict?
**A) TRUE_POSITIVE - Malware  
B) FALSE_POSITIVE - Benign  
C) SUSPICIOUS - Needs escalation  
D) Cannot determine**

**Answer:** C or D initially reasonable - needs investigation. Final: B (BENIGN)

---

### Question 2: Why was PowerShell encoded?
**A) To hide malicious activity  
B) Character escaping for file paths  
C) Standard obfuscation technique  
D) Unknown**

**Answer:** B) Character escaping for file paths - Explained by IT ticket

---

### Question 3: Should you escalate?
**A) YES - Encoded PowerShell always escalate  
B) NO - Interview and investigation clear it  
C) Maybe - Depends on IT response  
D) Definitely escalate - Too risky**

**Answer:** B) NO - Investigation clears it, no escalation needed

---

### Question 4: How did you verify legitimacy?
**A) Just closed it  
B) Checked IT ticket + script verification  
C) Asked user only  
D) Checked reputation only**

**Answer:** B) Checked IT ticket + script verification - Multiple sources confirm

---

### Question 5: Investigation time appropriate?
**A) Too fast - Should spend more time  
B) Good - Systematic and complete  
C) Too slow - Wasted time  
D) Fine, doesn't matter**

**Answer:** B) Good - Systematic, verified through multiple sources

---

## Key Differences: Beginner vs Intermediate

```
BEGINNER (Module 24):
├─ Obvious root cause
├─ Clear context (backup service account)
├─ Quick resolution
├─ Investigation straightforward

INTERMEDIATE (Module 25):
├─ Mixed signals (red flags + legitimate)
├─ Requires deeper verification
├─ User/IT interview needed
├─ Investigation more complex
├─ Requires judgment calls
├─ Escalation decision needed
└─ Takes longer (20+ min)
```

---

**Module 25 Complete! ✅**

এখন আপনি:
- ✅ Complex scenario investigate করেছেন
- ✅ Mixed signals analyze করেছেন
- ✅ User interview conduct করেছেন
- ✅ IT verification done করেছেন
- ✅ Red flags evaluated করেছেন
- ✅ Confident verdict reached করেছেন
- ✅ Professional escalation decision করেছেন

Progress: **25 of 28 modules complete (89%)**

🎉 **3 MODULES LEFT!** 🎉

---

<!-- nav-footer -->
## 🧭 Navigation

| | |
|---|---|
| **Previous** | [⬅️ Module 24: Beginner Practical Lab](../module-24-beginner-practical-lab/index.md) |
| **Next** | [Module 26: Advanced Practical Lab ➡️](../module-26-advanced-practical-lab/index.md) |
| **🏠 Course Home** | [STUDY_NOTES.md](../../STUDY_NOTES.md) |
