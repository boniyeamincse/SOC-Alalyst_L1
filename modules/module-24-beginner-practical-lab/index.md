# Module 24: Beginner Practical Lab

## Lab Objective

আপনার জ্ঞান apply করুন real-world scenario তে:
- Alert triage করুন
- Full investigation conduct করুন
- Evidence collect করুন
- Verdict reach করুন
- Properly escalate করুন

---

## Lab Scenario

**Date:** 2024-06-21  
**Your Role:** L1 SOC Analyst - Morning Shift  
**Time:** 09:30 IST

---

## ALERT RECEIVED

```
Alert ID: #2847
Alert Name: Brute Force Attack
Severity: HIGH
Timestamp: 2024-06-21 09:15:32 IST
Target: domain_server_01 (Production)
User attempting: backup_admin@company.com
Source IP: 10.0.1.50
Failed attempts: 47
Time window: 09:00-09:15 (15 minutes)
System: Windows Domain Controller
```

---

## Your Task - Complete Investigation

### STEP 1: TRIAGE (2 minutes)

**Question:** Is this alert legitimate (not false positive)?

```
CHECK ALERT DETAILS:
├─ Alert fired: YES (confirmed in queue)
├─ Time: Recent (15 min ago)
├─ Severity: HIGH
├─ Target: Production domain controller (critical)
└─ Preliminary: Looks legitimate, needs investigation

NEXT: Continue to full investigation
```

---

### STEP 2: GATHER EVIDENCE

**Scenario Data - SIEM Search Results:**

```
Search: source_ip="10.0.1.50" earliest=-1h

Results: 47 failed login attempts
├─ Target account: backup_admin@company.com
├─ Time range: 09:00:32 - 09:14:58 IST
├─ Pattern: ~3 failures per minute
├─ Source: 10.0.1.50 (internal IP)
├─ Destination: DC01 (domain controller)
└─ Authentication: Kerberos failures
```

**Scenario Data - Network Lookup:**

```
IP: 10.0.1.50
Subnet: 10.0.1.0/24 (Office network)
Device Type: Workstation
Hostname: backup_automation_01
Owner: IT Infrastructure team
Status: Active
Last patch: 2024-06-19
EDR Status: Yes, monitored
```

**Scenario Data - User Information:**

```
Account: backup_admin@company.com
Type: Service account (automation)
Department: IT Infrastructure
Status: Active
Created: 2022-01-15
Last login: 2024-06-20 23:00:00
Groups: Domain Admins, Backup Admins
Purpose: Automated backup script
```

**Scenario Data - Process/Logs:**

```
Backup_automation_01 logs:
├─ Scheduled task: "Daily_Backup" 
├─ Schedule: 09:00 IST daily
├─ Last success: 2024-06-20 09:05:00
├─ Password last changed: 2024-06-15
├─ Script: backup_script.ps1
└─ Status: Script still running (seen 09:20)
```

**Scenario Data - Ticket Search:**

```
Query: "backup_admin password"
Results:
├─ Ticket #12847 created 2024-06-15
├─ Title: "Update backup_admin password"
├─ Status: CLOSED
├─ Description: "Updated service account password 
   for security rotation. Script updated with new 
   password. Tested 2024-06-15 14:00."
└─ No issues reported
```

---

### STEP 3: IDENTITY ENRICHMENT (2 minutes)

**Question:** Is backup_admin@company.com legitimate?

```
FINDINGS:
├─ Type: Service account (not human)
├─ Status: ACTIVE in AD
├─ Department: IT Infrastructure
├─ Purpose: Automated backup
├─ Groups: Domain Admins (expected for backup)
└─ Last activity: 2024-06-20 23:00 (yesterday)

ANALYSIS:
├─ Legitimate service account: YES
├─ Being used for expected purpose: YES
├─ Over-privileged? Domain Admin access reasonable 
   for backup operations
└─ Red flag: NO
```

---

### STEP 4: ASSET ENRICHMENT (2 minutes)

**Question:** What's the target system?

```
FINDINGS:
├─ Target: domain_server_01 (Domain Controller)
├─ Criticality: TIER 1 (CRITICAL)
├─ Data: All domain data + passwords
├─ Monitoring: SIEM + EDR coverage
├─ Location: Secure datacenter
└─ Access control: Restricted

ANALYSIS:
├─ High-value target: YES
├─ Properly monitored: YES
├─ Risk if compromise: CRITICAL
└─ But: Service account normal to access DC
```

---

### STEP 5: THREAT INTEL ENRICHMENT (2 minutes)

**Question:** Is source IP malicious?

```
FINDINGS:
├─ IP: 10.0.1.50
├─ Type: INTERNAL office IP
├─ Subnet: 10.0.1.0/24 (office)
├─ Device: backup_automation_01
├─ Reputation: Not in threat intel (internal)
└─ Last known: Own company device

ANALYSIS:
├─ External threat: NO
├─ Known company device: YES
├─ Malicious: Unlikely (internal automation)
└─ Red flag: NO (low threat)
```

---

### STEP 6: BEHAVIORAL ENRICHMENT (2 minutes)

**Question:** Is this normal behavior?

```
FINDINGS:
├─ Service account type: Regular pattern
├─ Scheduled backup: Runs 09:00 daily
├─ Timing: Matches backup schedule
├─ Frequency: First-time failures (check below)
├─ Pattern: ~3 failures/min (consistent with retry)
├─ Device: Automation box (not user workstation)

HISTORICAL CHECK:
├─ Yesterday (2024-06-20): No brute force
├─ Week before: No failures reported
├─ Baseline: Service account doesn't normally fail
└─ Current: 47 failures (deviation)

ANALYSIS:
├─ Pattern consistent with automation: YES
├─ But: Why failures if script was tested?
├─ Possibility 1: Password incorrect (needs update)
├─ Possibility 2: Account lockout (security feature)
└─ Needs investigation
```

---

### STEP 7: CONTEXTUAL ENRICHMENT (1 minute)

**Question:** Is there business reason?

```
FINDINGS:
├─ Ticket #12847: Password updated 2024-06-15
├─ Script updated: 2024-06-15 14:00
├─ Tested: Yes, worked
├─ No escalation issues reported
├─ Backup still running (seen 09:20)
├─ Status: CLOSED (no ongoing issues)

ANALYSIS:
├─ Business reason: Daily backup (expected)
├─ Process followed: Yes (ticket created)
├─ Testing done: Yes (verified working)
├─ Current failures: Unexpected (needs explanation)
└─ Red flag: Password might be wrong again?
```

---

### STEP 8: CORRELATION & DEEPER ANALYSIS

**Question:** Why 47 failures? What's happening?

```
INVESTIGATION:
├─ Check: Account lockout status
│  └─ Status: Account is LOCKED (too many failures)
│  └─ Lockout triggered at: 09:14:32
│  └─ Will unlock: 09:59:32 (30 min default)
│
├─ Check: Script behavior
│  └─ Script stil running: YES (09:20 check)
│  └─ Script keeps retrying: YES (loop behavior)
│  └─ Retries every: ~20 seconds
│
├─ Check: Password status
│  └─ Password changed: 2024-06-15
│  └─ Days since change: 6 days
│  └─ Expiration: Not set
│  └─ Password valid: Seems correct in ticket
│
├─ Check: Recent changes
│  └─ Group Policy changes: None (checked)
│  └─ Domain changes: None (checked)
│  └─ Password policy changes: NONE
│  └─ Account changes: NONE

FINDING: Possible causes
├─ Theory 1: Password changed again, script not updated
│  └─ Unlikely (no ticket for password change)
├─ Theory 2: Account lockout policy tightened
│  └─ Checking... No, policy unchanged
├─ Theory 3: Wrong password in script
│  └─ Possible - how to verify?
├─ Theory 4: Temporary issue (now resolved?)
│  └─ Checking... Account still locked
└─ Most likely: Password issue, script keeps retrying
```

---

### STEP 9: DECISION - VERDICT

**Question:** TP, FP, BENIGN, or SUSPICIOUS?

```
ANALYSIS SUMMARY:
├─ Source: Service account (legitimate)
├─ Target: DC (high value but normal access)
├─ Pattern: Matches scheduled backup
├─ Behavior: Service account normal
├─ Context: Business reason exists
├─ Threat: Low (internal automation)
├─ Cause: Likely password issue
├─ Account locked: Yes (at 09:14)
├─ No successful access: Account lockout prevented
└─ No data compromised: YES

VERDICT: FALSE_POSITIVE

Reason: Service account with known purpose, 
        automated backup process, account lockout 
        prevented successful access, cause likely 
        password mismatch (script vs AD).

Confidence: HIGH (85%)
Risk: LOW (no successful access)
Escalation: NOT NEEDED (unless for remediation)
```

---

### STEP 10: DOCUMENTATION & RECOMMENDATION

**Ticket Summary:**

```
ALERT #2847 - BRUTE FORCE ATTACK

Investigation Complete: FALSE_POSITIVE

Summary:
Alert triggered by service account backup_admin
attempting login 47 times to domain controller.
Investigation reveals expected behavior - automated
backup script with likely password mismatch.
Account lockout feature prevented successful access.

What Happened:
├─ Service account: backup_admin@company.com
├─ Script: Daily backup automation
├─ Failures: 47 in 15 minutes (09:00-09:15)
├─ Cause: Password likely mismatch
├─ Account status: Locked after threshold
├─ Damage: NONE (access denied)

Evidence:
├─ SIEM timeline (screenshot attached)
├─ AD account details (screenshot attached)
├─ Backup script logs (log attached)
├─ Ticket #12847 (password change)
└─ Network device info (backup_automation_01)

Analysis:
├─ Pattern: Matches known backup schedule
├─ Timing: 09:00 daily, expected
├─ Source: Internal automation server
├─ No indicators of compromise
├─ Account lockout prevented access
├─ No sensitive data accessed

Recommendation:
1. Close alert as FALSE_POSITIVE
2. IT team action: Verify backup_admin password
   matches script configuration
3. Update backup_script.ps1 with correct password
4. Test backup process
5. Document in ticket #12847

Playbook Used: "Brute Force Attack" (PB-0012)
Investigation Time: 13 minutes
Status: CLOSED - FALSE_POSITIVE

Next Steps:
[ ] Notify IT team: Check backup script password
[ ] Ensure backup completes successfully
[ ] Monitor for future alerts on same account
[ ] Close ticket once backup verified working
```

---

## WHAT YOU SHOULD HAVE DONE

### Investigation Checklist:

- [✓] Alert triaged (legitimate)
- [✓] Evidence collected (SIEM, AD, logs, tickets)
- [✓] Identity enriched (service account verified)
- [✓] Asset enriched (DC understood)
- [✓] TI checked (IP not malicious)
- [✓] Behavioral analyzed (pattern understood)
- [✓] Context reviewed (business reason found)
- [✓] Correlation done (cause identified)
- [✓] Verdict reached (FP with confidence)
- [✓] Ticket documented completely
- [✓] Recommendation provided
- [✓] No escalation (high confidence)
- [✓] Professional communication

### Time Breakdown:

```
Triage: 2 min
Identity: 2 min
Asset: 2 min
TI: 2 min
Behavioral: 2 min
Context: 1 min
Deeper analysis: 3 min
Verdict: 2 min
Documentation: 3 min
─────────────
Total: 19 minutes (close to 15-min target)
```

---

## Key Learning Points

### ✓ DONE RIGHT:

```
✓ Didn't jump to conclusions
✓ Investigated systematically (Five Ws)
✓ Collected all evidence
✓ Understood service accounts
✓ Recognized known pattern (backup)
✓ Found root cause (password mismatch)
✓ Confident verdict (high confidence)
✓ Provided actionable recommendation
✓ Complete documentation
✓ Time-efficient investigation
```

### ✗ COMMON MISTAKES:

```
✗ Escalate immediately without investigation
  (Would waste L2 time, obvious FP)

✗ Close without understanding cause
  (Might reoccur, no improvement)

✗ Trust SIEM only, ignore business context
  (Business reason obvious if investigated)

✗ Miss the account lockout detail
  (Critical to understanding the situation)

✗ Over-investigate simple case
  (Evidence clear early, don't get stuck)

✗ Poor documentation
  (L2 wouldn't understand)

✗ No recommendation
  (Leaves IT team without guidance)
```

---

## Assessment

### Question 1: Alert verdict?
**A) TRUE_POSITIVE  
B) FALSE_POSITIVE  
C) BENIGN  
D) SUSPICIOUS**

**Answer:** B) FALSE_POSITIVE - Service account, known pattern, no compromise

---

### Question 2: Why did failures happen?
**A) Attacker guessing password  
B) Password mismatch in script  
C) Network problem  
D) Cannot determine**

**Answer:** B) Password mismatch in script - Most likely based on evidence

---

### Question 3: Should you escalate?
**A) YES, definitely  
B) NO, close as FP  
C) Maybe, escalate to manager  
D) Escalate to IR**

**Answer:** B) NO, close as FP - High confidence, no compromise, no escalation needed

---

### Question 4: Investigation time appropriate?
**A) Too slow (>20 min)  
B) Good (13-19 min)  
C) Too fast (<10 min)  
D) Doesn't matter**

**Answer:** B) Good (13-19 min) - Systematic, complete, efficient

---

### Question 5: What should IT team do?
**A) Nothing, false positive  
B) Verify password matches script  
C) Change password immediately  
D) Reboot server**

**Answer:** B) Verify password matches script - Fix root cause, test backup

---

## Summary

**Alert:** Brute force (47 failures)  
**Investigation:** Full Five Ws + correlation  
**Evidence:** Multiple sources (SIEM, AD, logs, tickets)  
**Analysis:** Service account backup, password mismatch  
**Verdict:** FALSE_POSITIVE (high confidence)  
**Action:** Notify IT to fix password, test backup  
**Outcome:** Improved process, no escalation needed

**Key Success:** Systematic investigation → Complete understanding → Right verdict → Helpful recommendation

---

**Module 24 Complete! ✅**

এখন আপনি:
- ✅ Real scenario investigate করেছেন
- ✅ Complete evidence gathering করেছেন
- ✅ Systematic analysis conducted করেছেন
- ✅ Confident verdict reached করেছেন
- ✅ Professional documentation written করেছেন
- ✅ Helpful recommendation provided করেছেন

Progress: **24 of 28 modules complete (86%)**

🎉 **4 MODULES LEFT!** 🎉

---

<!-- nav-footer -->
## 🧭 Navigation

| | |
|---|---|
| **Previous** | [⬅️ Module 23: Professional Skills & Resilience](../module-23-professional-skills-resilience/index.md) |
| **Next** | [Module 25: Intermediate Practical Lab ➡️](../module-25-intermediate-practical-lab/index.md) |
| **🏠 Course Home** | [STUDY_NOTES.md](../../STUDY_NOTES.md) |
