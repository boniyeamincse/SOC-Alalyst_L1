# Module 26: Advanced Practical Lab

## Lab Objective

Real incident scenario requiring:
- Multi-system correlation
- Actual threat confirmed
- Critical escalation decision
- Complex analysis
- Incident response coordination
- Time-sensitive investigation

---

## Lab Scenario

**Date:** 2024-06-21  
**Your Role:** L1 SOC Analyst - Afternoon Shift  
**Time:** 14:20 IST  
**Status:** CRITICAL - Multiple alerts

---

## ALERTS RECEIVED

```
Alert Set #1 - 14:05 IST
├─ Alert ID: #5401
├─ Alert: "Brute force + Successful login"
├─ User: admin_backup@company.com
├─ Source: External IP 203.0.113.100
├─ Failures: 120+ in 2 hours
├─ Success: 1 successful login at 14:03
└─ System: Citrix gateway (VPN access)

Alert Set #2 - 14:12 IST
├─ Alert ID: #5402
├─ Alert: "Unusual network activity"
├─ System: db_prod_01 (production database)
├─ Activity: Unexpected database backup initiated
├─ Volume: Large (500 MB in 3 minutes)
├─ Destination: Unknown internal IP (10.0.5.100)
└─ Initiated by: admin_backup@company.com

Alert Set #3 - 14:18 IST
├─ Alert ID: #5403
├─ Alert: "Suspicious file access"
├─ System: file_server_prod
├─ User: admin_backup@company.com
├─ Action: Downloaded 50+ sensitive files
├─ Location: Financial_Data, Customer_Data folders
├─ Volume: 2.3 GB in 4 minutes
└─ Destination: Unknown system

Alert Set #4 - 14:20 IST
├─ Alert ID: #5404
├─ Alert: "Network reconnaissance"
├─ Source: 10.0.5.100 (internal)
├─ Activity: Port scanning detected
├─ Targets: Multiple servers (SSH, RDP, DB ports)
└─ Confidence: 95% (high)
```

---

## Your Task - URGENT Investigation

### STEP 1: TRIAGE - ASSESS URGENCY (2 minutes)

**Question:** How urgent?

```
ASSESSMENT:
├─ Multiple alerts (4 separate)
├─ Brute force SUCCESS (not just attempts)
├─ External attacker (external IP)
├─ Compromised critical account (admin_backup)
├─ Active data access (database + files)
├─ Reconnaissance (port scanning)
├─ Timeline: Rapid escalation (15 minutes)
└─ All indicators: ACTIVE INCIDENT

URGENCY LEVEL: CRITICAL/IMMEDIATE

ACTION: Escalate immediately to L2/IR
DO NOT DELAY FOR FULL INVESTIGATION
```

---

### STEP 2: QUICK EVIDENCE COLLECTION (5 minutes)

**Alert #5401 - Brute Force Details:**

```
Source: 203.0.113.100
├─ IP reputation: MALICIOUS (known attacker infrastructure)
├─ First seen: Today (new, targeting today)
├─ ASN: 12345 (datacenter, VPN provider)
├─ Threat intel: Linked to 5+ breaches (TI database)

Target: admin_backup@company.com
├─ Type: Service account (admin backup)
├─ Privileges: HIGH (can access all systems)
├─ Previous activity: Last login 2024-06-19
├─ Password age: 45 days

Attack pattern:
├─ Failures: 120+ attempts in ~2 hours
├─ Success: 1 successful login at 14:03:45
├─ Method: Credential guessing/spray attack
├─ Tools: Likely automated (consistent timing)

Failed to successful:
├─ Failed: 14:00-14:03 (120 attempts)
├─ Success: 14:03:45 (ONE successful)
├─ Pattern: Classic brute force success

POST-LOGIN ACTIVITY:
├─ Time: 14:03:45 to 14:20 (17 minutes active)
├─ Actions: Database dump + file download
├─ Data accessed: Sensitive financial + customer data
└─ Current status: Still connected (14:20)
```

**Alert #5402 - Database Activity:**

```
System: db_prod_01 (TIER 1 CRITICAL)
├─ Contains: Financial records, customer data
├─ Last access: 2024-06-20 (backup only)
├─ Today: Unusual activity by admin_backup

Database dump:
├─ Size: 500 MB
├─ Type: Full backup (unusual for attacker)
├─ Destination: 10.0.5.100 (unknown internal IP)
├─ Time: 14:03-14:06 (3 minutes - fast)
├─ Data: Complete database (worst case)

Access pattern:
├─ User: admin_backup (legitimate service account)
├─ But initiated from: External VPN connection
├─ Normal pattern: No, admin_backup accessed only
  via direct server connection, never remote VPN
└─ Abnormal: CONFIRMED
```

**Alert #5403 - File Download:**

```
System: file_server_prod
├─ Folders accessed:
│  ├─ Financial_Data (customer payment info)
│  ├─ Customer_Data (personal information)
│  └─ Contracts (sensitive business)
├─ Files: 50+ files downloaded
├─ Total: 2.3 GB
├─ Timeframe: 14:06-14:10 (4 minutes)

Destination: Unknown
├─ Internal IP: 10.0.5.100 (same as DB dump)
├─ Not a known company system
├─ Not in asset inventory
├─ Unknown purpose

Data classification:
├─ Financial_Data: HIGHLY SENSITIVE
├─ Customer_Data: PII (privacy regulation)
├─ Contracts: CONFIDENTIAL
└─ Regulatory impact: HIGH (data breach)
```

**Alert #5404 - Reconnaissance:**

```
Source: 10.0.5.100 (internal, unknown)
├─ Port scanning: SSH, RDP, database ports
├─ Targets: 15+ internal systems
├─ Intent: Lateral movement reconnaissance
├─ Confidence: 95% (clear scanning pattern)
├─ Status: Active at 14:18

Analysis:
├─ Purpose: Finding next targets
├─ Lateral movement: Attacker expanding access
├─ Not random: Targeting specific ports (admin access)
└─ Stage: Post-initial-compromise
```

---

### STEP 3: CORRELATION - Connect Alerts

**Question:** Are these connected?

```
TIMELINE RECONSTRUCTION:

14:00 - Brute force starts (203.0.113.100 external)
  └─ Target: admin_backup (high-privilege account)

14:03 - SUCCESS (brute force breaks password)
  └─ Attacker gains VPN access

14:03-14:06 - Database dump initiated
  └─ 500 MB database stolen (db_prod_01)
  └─ Destination: 10.0.5.100 (attacker system)

14:06-14:10 - File download
  └─ 2.3 GB sensitive files
  └─ Customer data + financial data
  └─ Destination: 10.0.5.100 (same attacker system)

14:10+ - Reconnaissance (port scanning)
  └─ Source: 10.0.5.100 (attacker's compromised system)
  └─ Scanning for next targets (lateral movement)

CORRELATION: All connected
├─ All use admin_backup account
├─ Same attacker infrastructure (10.0.5.100)
├─ Timeline sequential (each follows previous)
├─ Progression: Breach → Steal → Expand
└─ Status: ACTIVE INCIDENT (ongoing)
```

---

### STEP 4: THREAT ASSESSMENT

**Question:** What happened?

```
INCIDENT SUMMARY:

ATTACK CHAIN:
├─ Step 1: External attacker (203.0.113.100)
├─ Step 2: Brute force admin_backup account
├─ Step 3: Successful credential compromise
├─ Step 4: VPN access gained
├─ Step 5: Compromise internal system (10.0.5.100)
├─ Step 6: Database dump (500 MB)
├─ Step 7: Sensitive files stolen (2.3 GB)
├─ Step 8: Reconnaissance for lateral movement
└─ Step 9: ONGOING (at 14:20)

DATA BREACH:
├─ Financial data: STOLEN
├─ Customer PII: STOLEN
├─ Business contracts: STOLEN
├─ Volume: 2.8 GB of sensitive data
└─ Regulatory: SERIOUS (privacy violations)

ACTIVE THREAT:
├─ Attacker still connected (14:20)
├─ Port scanning in progress
├─ Preparing lateral movement
├─ Still accessing systems
└─ Threat ongoing, not contained

IMPACT:
├─ Data breach: CONFIRMED
├─ Systems compromised: Multiple
├─ Regulatory impact: HIGH
├─ Customer notification: Required
├─ Immediate containment: NEEDED
└─ Incident response: REQUIRED
```

---

### STEP 5: CRITICAL ACTIONS NEEDED

**Question:** What should happen RIGHT NOW?

```
DO NOT INVESTIGATE FURTHER AS L1
DO IMMEDIATE ESCALATION

IMMEDIATE ACTIONS (NOT L1 responsibility):
├─ [ ] Reset admin_backup password (L2)
├─ [ ] Disable admin_backup account (L2)
├─ [ ] Block external IP 203.0.113.100 (Network)
├─ [ ] Isolate internal system 10.0.5.100 (Network)
├─ [ ] Activate Incident Response team
├─ [ ] Notify CISO
├─ [ ] Preserve evidence
├─ [ ] Begin forensic investigation (L3)
└─ [ ] Legal/Compliance notification (executive)

ESCALATION PATH:
L1 (you) → L2 (immediate)
         → L3 (forensics)
         → IR team (containment)
         → CISO (notification)
         → Legal/HR (notification)
```

---

### STEP 6: ESCALATION TICKET

**Your Action: Create URGENT Escalation Ticket**

```
TICKET TYPE: INCIDENT REPORT
SEVERITY: CRITICAL - DATA BREACH
ESCALATION: IMMEDIATE TO IR TEAM

═══════════════════════════════════════════════════

INCIDENT SUMMARY:

Multi-alert correlation indicates active data 
breach. External attacker compromised high-privilege 
service account via brute force, stealing 2.8 GB 
of sensitive data (financial + customer PII + 
contracts) and establishing internal foothold for 
lateral movement. ACTIVE at time of report.

═══════════════════════════════════════════════════

CRITICAL ALERTS:
├─ Alert #5401: Brute force SUCCESS (external IP)
├─ Alert #5402: Database dump (500 MB stolen)
├─ Alert #5403: File download (2.3 GB stolen)
└─ Alert #5404: Port scanning (lateral movement prep)

ATTACK CHAIN:
1. 14:00 - Brute force attack starts (external IP 203.0.113.100)
2. 14:03 - Successful login (admin_backup account)
3. 14:03-14:06 - Database backup stolen (500 MB)
4. 14:06-14:10 - Sensitive files downloaded (2.3 GB)
5. 14:18+ - Reconnaissance/lateral movement scanning
6. 14:20 - ATTACKER STILL CONNECTED

THREAT INTELLIGENCE:
├─ External IP: 203.0.113.100
├─ Reputation: Known malicious (5+ previous breaches)
├─ ASN: VPN provider/datacenter
├─ Account: admin_backup (high-privilege)
├─ Target: TIER 1 critical database + sensitive files
└─ Timeline: RAPID ESCALATION (15 minutes)

DATA COMPROMISED:
├─ Financial_Data: Complete (500 MB from DB)
├─ Customer_Data: 50+ files (PII exposed)
├─ Contracts: 50+ files (business confidential)
├─ Total: 2.8 GB sensitive data
└─ Regulatory: Privacy breach (requires notification)

INVESTIGATION EVIDENCE:
├─ SIEM brute force log (alert #5401)
├─ Database access logs (alert #5402)
├─ File access logs (alert #5403)
├─ Network reconnaissance (alert #5404)
├─ IP reputation data (threat intel)
├─ Account history (AD records)
└─ Timeline reconstruction (complete)

IMMEDIATE ACTIONS REQUIRED:
├─ [ ] ISOLATE: Internal system 10.0.5.100
├─ [ ] DISABLE: admin_backup account
├─ [ ] BLOCK: External IP 203.0.113.100 at firewall
├─ [ ] RESET: admin_backup account password (new one)
├─ [ ] PRESERVE: All evidence and logs
├─ [ ] NOTIFY: CISO (executive)
├─ [ ] ACTIVATE: Incident Response team
├─ [ ] LEGAL: Prepare breach notification
└─ [ ] FORENSICS: Begin investigation (L3)

CONFIDENCE: VERY HIGH (95%+)

This is confirmed data breach with active attacker. 
Immediate incident response required.

═══════════════════════════════════════════════════

Escalated by: L1_analyst (you)
Time: 2024-06-21 14:20 IST
Escalation path: L2 → IR → CISO
Status: CRITICAL - AWAITING IMMEDIATE ACTION
```

---

## What Made This ADVANCED

### vs Intermediate Lab:

```
Intermediate:
├─ Single system
├─ Uncertain verdict initially
├─ Requires verification
├─ Still BENIGN after investigation
└─ No escalation needed

Advanced:
├─ Multiple systems + alerts
├─ Clear threat indicators
├─ Confirmed compromise
├─ Active attacker (ongoing)
├─ Data breach (regulatory impact)
├─ Immediate escalation needed
├─ Incident response required
├─ Time-sensitive (containment critical)
└─ Executive notification needed
```

---

## Key Skills Demonstrated

### You should have:

```
✓ Recognized alert correlation (4 alerts = 1 incident)
✓ Identified attack chain (brute force → steal → expand)
✓ Understood urgency (immediate escalation)
✓ Recognized active threat (still connected)
✓ Assessed impact (data breach confirmed)
✓ Known NOT to delay (escalate first)
✓ Created proper escalation (complete evidence)
✓ Involved right teams (IR, CISO, Legal)
✓ Followed incident response (preserve evidence)
└─ Professional judgment (L1 role is to escalate)
```

---

## What NOT to Do (Common Mistakes)

```
❌ Wait for full investigation (attacker still active)
❌ Try to trace attacker alone (IR team responsibility)
❌ Attempt containment yourself (might destroy evidence)
❌ Not escalate immediately (critical time wasted)
❌ Close any alerts (part of incident)
❌ Not preserve logs (forensic investigation needs them)
❌ Assume account compromise is limited (widespread)
❌ Not involve CISO (executive notification required)
❌ Delay legal notification (regulatory requirement)
└─ Treat as routine alert (INCIDENT, not alert)
```

---

## Assessment

### Question 1: Initial verdict?
**A) False positive  
B) Benign activity  
C) Confirmed incident - ESCALATE IMMEDIATELY  
D) Needs more investigation**

**Answer:** C) Confirmed incident - ESCALATE IMMEDIATELY

---

### Question 2: What's the primary threat?
**A) Single failed login attempt  
B) Encoded PowerShell  
C) Active data breach with attacker ongoing  
D) Service account misconfiguration**

**Answer:** C) Active data breach with attacker ongoing

---

### Question 3: What should L1 do first?
**A) Investigate fully (get complete picture)  
B) Reset account password  
C) Escalate immediately to IR  
D) Block the IP**

**Answer:** C) Escalate immediately to IR - Don't delay on action items

---

### Question 4: Who needs to be notified?
**A) L2 only  
B) L2, L3, and IR team  
C) L2, L3, IR, CISO, and Legal  
D) External authorities only**

**Answer:** C) L2, L3, IR, CISO, and Legal - Data breach requires executive/legal

---

### Question 5: Investigation time?
**A) 30 minutes (thorough)  
B) 5 minutes (quick escalation)  
C) 1 hour (complete)  
D) No time limit (investigate fully)**

**Answer:** B) 5 minutes (quick escalation) - Every minute matters with active attacker

---

## Real Incident Lessons

```
This lab mirrors real breaches:
├─ Brute force success is catastrophic
├─ High-privilege accounts are critical targets
├─ Attackers act FAST (minutes, not hours)
├─ Data theft happens immediately
├─ Lateral movement starts immediately
├─ Time is the enemy
├─ L1 role: Detect + Escalate (not solve)
├─ IR role: Contain + Investigate + Remediate
└─ Every minute = more data stolen

Key learning:
Recognizing serious incidents and escalating 
immediately is MORE IMPORTANT than deep 
investigation at L1 level.
```

---

**Module 26 Complete! ✅**

এখন আপনি:
- ✅ Real incident scenario handled করেছেন
- ✅ Multi-alert correlation করেছেন
- ✅ Attack chain identified করেছেন
- ✅ Active threat recognized করেছেন
- ✅ Data breach assessed করেছেন
- ✅ Critical escalation decision করেছেন
- ✅ Proper incident reporting written করেছেন
- ✅ Executive notification planned করেছেন

Progress: **26 of 28 modules complete (93%)**

🎉 **2 MODULES LEFT - CAPSTONE & FINAL EXAM!** 🎉

