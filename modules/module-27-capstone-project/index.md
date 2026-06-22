# Module 27: Capstone Project

## Capstone Objective

Simulate complete L1 shift using ALL skills learned:
- Alert triage
- Investigation methodology
- Multiple skill levels (beginner → intermediate → advanced)
- Time management
- Metrics tracking
- Professional communication
- Escalation decisions
- Incident handling
- Real-world pressures

---

## Full Shift Simulation

**Date:** 2024-06-22  
**Your Role:** L1 SOC Analyst - Morning Shift (09:00-17:00)  
**Shift Goal:** Handle queue, maintain quality, proper escalations

---

## SHIFT START: 09:00 IST

### Pre-Shift Review

```
QUEUE STATUS:
├─ Alerts pending: 42
├─ Average severity: MEDIUM
├─ Escalations awaiting: 3
├─ SLA target: 95% < 20 min

METRICS TARGET (today):
├─ Alerts to handle: 40-60
├─ Avg investigation: < 15 min
├─ FP rate target: < 10%
├─ Escalation accuracy: > 90%
└─ SLA compliance: > 95%

YOUR GOALS:
✓ Process queue methodically
✓ Maintain quality
✓ Hit time targets
✓ Escalate appropriately
✓ Document completely
```

---

## ALERT 1: 09:05 IST - Failed Login (EASY)

```
Alert: Failed login attempt
User: john.smith@company.com
System: mail_server
Failures: 3 in 5 minutes
Time: 09:00-09:05

QUICK TRIAGE:
├─ Pattern: 3 failures (low, typical user error)
├─ Time: 5 minutes (normal)
├─ User: Regular employee (not admin)
└─ Risk: LOW

DECISION: Close as user error
Time spent: 5 minutes
Verdict: FALSE_POSITIVE
```

---

## ALERT 2: 09:15 IST - Unusual Login Location (MEDIUM)

```
Alert: User login from unusual location
User: alice.johnson@company.com
Location: Singapore (from India previous day)
Time: 09:10 IST
Previous login: India, 2024-06-21 17:00

INVESTIGATION:
├─ Distance: 3000+ km
├─ Time: 16 hours between logins
└─ Travel: POSSIBLE but tight

ENRICHMENT:
├─ User calendar: No travel mentioned
├─ Manager: Reached out "No approval"
├─ VPN: Not using VPN (direct login)

VERDICT: SUSPICIOUS - Possible compromise
Escalate: YES to L2 (manager to verify)
Time spent: 12 minutes
```

---

## ALERT 3: 09:35 IST - File Download Alert (BEGINNER LAB TYPE)

```
Alert: Large file downloaded
User: bob.wilson@company.com
File: Customer_data_backup.csv (45 MB)
Destination: USB drive
Time: 09:30

INVESTIGATION:
├─ User: IT admin (access normal)
├─ File: Legitimate backup file
├─ Destination: USB (standard procedure)
├─ Ticket: #8234 (backup authorization)

TICKET CHECK: Yes, documented
Manager approval: Yes, confirmed
Purpose: Offsite backup (legitimate)

VERDICT: FALSE_POSITIVE - Authorized activity
Time spent: 8 minutes
```

---

## ALERT 4: 10:05 IST - Malware Detection (COMPLEX)

```
Alert: File detected as malware
System: test_workstation_05
File: document.exe
Vendor: 3 of 50 vendors detect
Confidence: 60%
EDR: No execution detected

INVESTIGATION:
├─ File type: .exe (executable)
├─ Context: Downloaded from email
├─ Vendor consensus: LOW (3/50)
├─ Execution: NO (quarantined)
├─ System: Test lab (isolated)

RESEARCH:
├─ File hash: Known PUP (adware, not malware)
├─ Infection risk: LOW (not executed)
├─ Damage: NONE (caught early)

DECISION: Monitor or escalate?
├─ Confidence: 60% (not high)
├─ Risk: LOW (quarantined, not executed)
└─ Escalate: YES to L2 (for context + possible user education)

Time spent: 16 minutes
```

---

## ALERT 5: 10:30 IST - Multiple Brute Force (ADVANCED TYPE)

```
Alert Set:
├─ User: admin_prod@company.com
├─ Failures: 85 in 10 minutes
├─ Sources: Multiple IPs (distributed)
├─ Success: YES (1 successful login)
├─ Source of success: Same IP as failures
├─ System: Production server

RED FLAGS:
├─ Brute force success (compromise indicators)
├─ Admin account (high-privilege)
├─ Distributed attack (bot network)
├─ Still active: YES (14:30)
├─ Production system (critical)

IMMEDIATE ASSESSMENT:
├─ This is actual compromise
├─ Requires immediate escalation
├─ Do not wait for full investigation
└─ Alert L2/IR NOW

ESCALATION TICKET:
Status: CRITICAL - ESCALATE IMMEDIATELY
Do not investigate further as L1
Attach all alert evidence
Alert: L2 analyst + IR team

Time spent: 8 minutes (quick escalation)
```

---

## ALERT 6: 11:00 IST - Phishing Email (EASY)

```
Alert: Phishing email detected
Sender: Looks like bank (fake domain)
Subject: "Urgent: Verify Your Account"
Recipients: 25 users
User action: Not opened (caught by filter)

QUICK CHECK:
├─ Email: Caught by filter (good)
├─ Users: Did not click (safe)
├─ Damage: NONE (prevented)
├─ Action needed: Educate users

DECISION: Close as caught
Note: Mention in team briefing
Time spent: 3 minutes
```

---

## ALERT 7: 11:30 IST - Suspicious PowerShell (INTERMEDIATE TYPE)

```
Alert: Encoded PowerShell execution
User: carol.smith@company.com
System: finance_workstation_08
Command: Base64 encoded

INITIAL CHECK:
├─ Encoding: SUSPICIOUS
├─ User: Finance dept (rare PS)
├─ Context: Unknown

INVESTIGATION:
├─ IT ticket: None found
├─ Previous: No PowerShell history
├─ Business: Not finance function

DEEPER INVESTIGATION:
├─ Contact user: No, not with user
├─ Escalate to L2: YES (unusual, no context)

DECISION: ESCALATE (similar to Module 25)
Time spent: 14 minutes

Note: Let L2 verify user/IT ticket
```

---

## BREAK: 12:00 IST (1 hour)

```
Lunch break (12:00-13:00)
Completed alerts: 7
Time so far: 3 hours
Pace: On track (need 40-60 for shift)
Quality: Good (mix of FP and escalations)

STATS SO FAR:
├─ Alerts handled: 7
├─ Closed: 5 (FP + benign)
├─ Escalated: 2 (suspicious + critical)
├─ Average time: 10.7 min
└─ SLA: On target
```

---

## AFTERNOON SESSION: 13:00-17:00

### ALERT 8-12: Routine Alerts (Various types)

```
Alert 8 (13:15): Failed login, admin account
├─ Investigation: Service account retry
└─ Decision: Close as FP

Alert 9 (13:35): Network anomaly
├─ Investigation: Backup process
└─ Decision: Close as benign

Alert 10 (14:05): Unusual data access
├─ Investigation: Authorized user, project access
└─ Decision: Close as benign

Alert 11 (14:40): Account lockout
├─ Investigation: Failed password (user knows reason)
└─ Decision: Close as benign

Alert 12 (15:15): System scan detected
├─ Investigation: Routine antivirus scan
└─ Decision: Close as benign

PATTERN: Afternoon quieter, routine alerts
Pace: Good (handling efficiently)
```

---

### ALERT 13: 15:50 IST - Escalation Follow-up

```
Alert #2 (Unusual login) Follow-up:
├─ L2 responds: "Manager confirms no approval"
├─ Status: Suspicious travel confirmed
├─ Action: Password reset recommended
├─ Your role: Document follow-up

NOTE: Shows escalation working through chain
Users want to see coordination working
```

---

## SHIFT END: 17:00 IST

### Daily Summary

```
ALERTS PROCESSED:
├─ Total handled: 42 alerts
├─ Closed: 35 (83%)
├─ Escalated: 7 (17%)
└─ Average time: 11.8 minutes

QUALITY METRICS:
├─ FP rate: 8.2% (target <10%) ✓
├─ Escalation accuracy: 95% (target >90%) ✓
├─ SLA compliance: 96% (target >95%) ✓
├─ Documentation: 100% complete ✓

INCIDENT SUMMARY:
├─ 1 Critical incident escalated (#5)
├─ 2 Suspicious escalated for L2 (#2, #7)
├─ 35 Routine closed appropriately
└─ No missed threats

PROFESSIONAL:
├─ Communication: All tickets documented
├─ Time management: Efficient workflow
├─ Quality maintained: Good mix of decisions
└─ Team coordination: Escalations clear

LEARNING ACHIEVED:
✓ Triage skills (quick assessment)
✓ Investigation (systematic analysis)
✓ Time management (efficient pace)
✓ Escalation judgment (when to escalate)
✓ Documentation (complete and clear)
✓ Communication (professional)
✓ Quality vs speed balance (maintained)
└─ Real-world L1 experience (simulated)
```

---

## Key Takeaways from Capstone

### Skills Integration:

```
Triage (Module 6-7):
├─ Quick alert assessment
├─ Severity matching
├─ Resource planning
└─ Queue management

Investigation (Module 9):
├─ Systematic approach
├─ Evidence gathering
├─ Analysis
└─ Correlation

Enrichment (Module 15):
├─ Identity context
├─ Asset context
├─ Threat intelligence
├─ Behavioral analysis

Communication (Module 20):
├─ Professional tickets
├─ Clear escalations
├─ Status updates
├─ Team coordination

Metrics (Module 21):
├─ Time tracking
├─ Quality monitoring
├─ SLA compliance
└─ Performance assessment

Improvement (Module 22):
├─ Learn from investigations
├─ Document findings
├─ Identify patterns
└─ Suggest improvements

Resilience (Module 23):
├─ Stress management
├─ Time boundaries
├─ Professional standards
└─ Confidence building
```

---

## Assessment: Capstone Reflection

### Question 1: What made today successful?

**Options:**
A) Handled maximum alerts  
B) Balanced speed + quality + right escalations  
C) No escalations at all  
D) Investigated everything deeply

**Answer:** B) Balanced speed + quality + right escalations - L1 success = efficiency + accuracy

---

### Question 2: Alert #5 (brute force success) - right decision?

**A) Should have investigated fully  
B) Should have closed as routine  
C) Escalated immediately - correct  
D) Could have done either**

**Answer:** C) Escalated immediately - correct - Active incident requires urgent escalation

---

### Question 3: Your FP rate was 8.2%. Is that good?

**A) Too high (should be <5%)  
B) Good (target <10%)  
C) Too low (should be higher)  
D) Doesn't matter**

**Answer:** B) Good (target <10%) - 8.2% is healthy, shows good judgment

---

### Question 4: Time management - 11.8 min average. Evaluate:

**A) Too slow (target <10 min)  
B) Good (target 15 min, you better)  
C) Too fast (missed details)  
D) Can't evaluate**

**Answer:** B) Good (target 15 min, you better) - Faster than target without sacrificing quality

---

### Question 5: Most important lesson from capstone?

**A) Close as many as possible  
B) Escalate everything uncertain  
C) Balance efficiency + accuracy + right decisions  
D) Speed only matters**

**Answer:** C) Balance efficiency + accuracy + right decisions - Real L1 work

---

## Your First Day as L1 (Simulated)

### What you accomplished:

```
✓ Processed 42 alerts methodically
✓ Made correct verdicts (FP vs TP/Suspicious)
✓ Escalated 7 appropriately (17% rate)
✓ Caught 1 critical incident (brute force success)
✓ Maintained <12 min average
✓ Hit all quality metrics
✓ Documented professionally
✓ Communicated clearly
✓ Managed time well
✓ Maintained composure under pressure
```

### What L1 analysts really do:

```
NOT: Deep technical forensics (that's L3)
NOT: Design detection rules (that's engineering)
NOT: Executive decisions (that's management)

YES: Triage alerts quickly
YES: Investigate systematically
YES: Escalate appropriately
YES: Document clearly
YES: Communicate professionally
YES: Maintain quality
YES: Hit time targets
YES: Know your limits
YES: Ask for help when needed
└─ REPEAT daily
```

---

## Congratulations!

```
You have completed:

✓ 27 modules of SOC L1 training
✓ Theoretical knowledge (1-23)
✓ Practical labs (24-26)
✓ Capstone simulation (27)
✓ Real-world skills demonstrated

Ready for Module 28: Final Assessment
```

---

**Module 27 Complete! ✅**

Capstone Project covering:
- Full shift simulation (8 hours, 42 alerts)
- Alert 1: Routine FP (user error)
- Alert 2: Investigation required (unusual location) → Escalate
- Alert 3: Beginner lab type (authorized file download) → Close
- Alert 4: Complex decision (low confidence malware) → Escalate
- Alert 5: Critical incident (brute force success) → Immediate escalation
- Alert 6: Caught by filter (phishing) → Close
- Alert 7: Intermediate type (PowerShell context) → Escalate
- Alert 8-12: Routine mix → Close appropriately
- Shift metrics: 42 handled, 35 closed (83%), 7 escalated (17%), 11.8 min avg
- Quality: 8.2% FP rate (target <10%), 95% escalation accuracy, 96% SLA compliance
- Skills integration: Triage, investigation, enrichment, communication, metrics, improvement, resilience
- Key learning: Balance efficiency + accuracy + right escalation decisions
- Assessment: 5 reflection questions

Progress: **27 of 28 modules complete (96%)**

🎉 **1 MODULE LEFT - FINAL ASSESSMENT!** 🎉

Continue to **Module 28: Final Assessment & Course Completion**?