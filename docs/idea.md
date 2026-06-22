# SOC Level 1 Analyst Course Outline

## Beginner to Advanced SOC L1 Training Program

## Course Goal

এই কোর্সের লক্ষ্য হলো একজন beginner learner-কে ধাপে ধাপে SOC Level 1 Analyst হিসেবে তৈরি করা, যাতে সে alert বুঝতে পারে, triage করতে পারে, True Positive ও False Positive আলাদা করতে পারে, report লিখতে পারে, L2 escalation করতে পারে এবং SOC metrics বুঝে নিজের কাজ improve করতে পারে।

---

# Module 1: Introduction to SOC

## 1.1 What is SOC?

SOC এর পূর্ণরূপ Security Operations Center। এটি এমন একটি security team বা department, যারা organisation-এর digital assets protect করে।

SOC-এর মূল লক্ষ্য:

* Confidentiality রক্ষা করা
* Integrity রক্ষা করা
* Availability রক্ষা করা
* Threat detect করা
* Alert triage করা
* Incident response team-কে support করা

## 1.2 Why Organisations Need SOC

SOC দরকার কারণ প্রতিদিন organisation বিভিন্ন cyber threat-এর মুখোমুখি হয়।

উদাহরণ:

* Phishing attack
* Malware infection
* Brute force attack
* Data exfiltration
* Unusual login
* Insider threat
* Ransomware
* Suspicious PowerShell command
* Unauthorized admin privilege

## 1.3 SOC Use Cases in an Organisation

Common SOC use cases:

* User unusual login detection
* Malware detection
* RDP brute force detection
* VPN brute force detection
* Suspicious file download
* Data exfiltration detection
* Privilege escalation detection
* Internal network scanning
* Endpoint compromise detection
* Suspicious email or phishing detection

---

# Module 2: SOC Team Structure and Roles

## 2.1 SOC L1 Analyst

SOC L1 Analyst হলো first-line security analyst।

Main duties:

* Alert review করা
* Alert triage করা
* False Positive এবং True Positive আলাদা করা
* Basic investigation করা
* Evidence collect করা
* Alert report লেখা
* True Positive হলে L2-তে escalate করা

## 2.2 SOC L2 Analyst

SOC L2 Analyst deeper investigation করে।

Main duties:

* L1 থেকে escalated alert receive করা
* Advanced analysis করা
* Remediation plan করা
* Malware বা compromised account investigate করা
* Incident response process শুরু করা

## 2.3 SOC Engineer

SOC Engineer SOC tools, rules, and integrations maintain করে।

Main duties:

* Detection rule তৈরি করা
* SIEM log source configure করা
* Alert field ঠিক রাখা
* Parser issue fix করা
* SOC automation support করা

## 2.4 SOC Manager

SOC Manager SOC operation manage করে।

Main duties:

* SOC team performance monitor করা
* SLA, MTTD, MTTA, MTTR track করা
* Analyst workload manage করা
* Quality of triage ensure করা
* Major incident coordination করা

---

# Module 3: SOC L1 Daily Duties

## 3.1 Daily Responsibilities

SOC L1 Analyst-এর daily কাজ:

* SIEM dashboard monitor করা
* New alerts review করা
* Alert severity অনুযায়ী prioritise করা
* Investigation শুরু করা
* Logs check করা
* User, host, IP enrichment করা
* Verdict দেওয়া
* Report লেখা
* Escalation করা
* Shift handover note তৈরি করা

## 3.2 Role-Based Daily Work

SOC L1-এর কাজ সাধারণত alert queue ভিত্তিক হয়।

Daily flow:

1. Login to SIEM
2. Check assigned alerts
3. Pick high priority alerts first
4. Investigate alert
5. Add comments/evidence
6. Set verdict
7. Close or escalate
8. Update shift report

---

# Module 4: Alert Fundamentals

## 4.1 What is an Alert?

Alert হলো SOC tool বা SIEM থেকে generated warning, যা কোনো suspicious বা abnormal activity detect করলে তৈরি হয়।

Example alert names:

* Unusual Login Location
* Windows RDP Bruteforce
* Email Marked as Phishing
* Potential Data Exfiltration
* Suspicious PowerShell Execution
* VPN Brute Force Attempt

## 4.2 Event vs Alert

Event হলো raw activity বা log.

Alert হলো detection rule দিয়ে important event identify করার পর তৈরি warning।

Example:

Event:

```text
User failed login from IP 103.61.240.174
```

Alert:

```text
Multiple Failed VPN Login Attempts
```

## 4.3 From Events to Alerts

Flow:

```text
User/system activity
↓
Log generated
↓
SIEM receives logs
↓
Detection rule matches suspicious pattern
↓
Alert generated
↓
SOC L1 triage starts
```

---

# Module 5: Alert Properties

## 5.1 Alert Time

Alert Time দেখায় alert কখন তৈরি হয়েছে।

Example:

```text
Event Time: March 21, 15:32
Alert Time: March 21, 15:35
```

## 5.2 Alert Name

Alert Name alert-এর summary দেয়।

Example:

```text
Unusual Login Location
Windows RDP Bruteforce
Potential Data Exfiltration
```

## 5.3 Alert Severity

Severity alert-এর urgency বোঝায়।

Common severity:

* Low / Informational
* Medium / Moderate
* High / Severe
* Critical / Urgent

## 5.4 Alert Status

Alert Status দেখায় alert-এর কাজ কোন অবস্থায় আছে।

Common status:

* New / Unassigned
* In Progress / Pending
* Closed / Resolved

## 5.5 Alert Verdict

Verdict হলো investigation শেষে analyst-এর final decision।

Common verdict:

* True Positive
* False Positive
* Benign
* Suspicious
* Needs Escalation

## 5.6 Alert Assignee

Assignee হলো যে analyst alert investigate করছে।

## 5.7 Alert Description

Alert Description সাধারণত বলে:

* Rule কী detect করেছে
* কেন suspicious
* কীভাবে triage করতে হবে

## 5.8 Alert Fields

Alert Fields-এ থাকে important values।

Example:

* Affected hostname
* Source IP
* Destination IP
* Username
* Command line
* File hash
* URL
* Process name

---

# Module 6: Alert Prioritisation

## 6.1 Picking the Right Alert

SOC L1 analyst সব alert একসাথে investigate করতে পারে না। তাই priority ঠিক করতে হয়।

Prioritisation factors:

* Severity
* Asset criticality
* User privilege
* Threat type
* Business impact
* Alert age
* Number of affected systems

## 6.2 High Priority Alert Examples

High priority alert:

* Critical server malware detection
* Domain admin unusual login
* Data exfiltration alert
* Ransomware behaviour
* VPN compromise
* Internal network scanning

## 6.3 Low Priority Alert Examples

Low priority alert:

* Known system update activity
* Repeated benign software activity
* Informational firewall deny log
* Expected admin login

---

# Module 7: SOC L1 Alert Triage

## 7.1 What is Alert Triage?

Alert triage মানে alert investigate করে বুঝা, এটি real threat নাকি noise।

Triage goal:

```text
Bad activity আলাদা করা
Good/expected activity আলাদা করা
True Positive হলে L2-তে escalate করা
False Positive হলে properly close করা
```

## 7.2 L1 Role in Alert Triage

SOC L1 analyst:

* Alert review করে
* Logs check করে
* User/host/IP context collect করে
* Bad from good আলাদা করে
* True Positive হলে L2 notify করে

## 7.3 Basic Triage Questions

প্রতিটি alert investigate করার সময় প্রশ্ন করুন:

* Who is involved?
* What happened?
* When did it happen?
* Where did it happen?
* Why is it suspicious?
* Is this expected?
* Is this a True Positive?
* Is escalation needed?

---

# Module 8: Alert Verdicts

## 8.1 True Positive

True Positive মানে alert সত্যি malicious বা risky activity detect করেছে।

Example:

```text
VPN brute force successful হয়েছে এবং পরে internal network scanning হয়েছে।
```

## 8.2 False Positive

False Positive মানে alert এসেছে, কিন্তু actual threat ছিল না।

Example:

```text
User unusual location থেকে login করেছে, কিন্তু user official travel-এ ছিল।
```

## 8.3 Benign / Expected

Benign মানে activity normal বা expected।

Example:

```text
IT admin approved maintenance window-তে server access করেছে।
```

## 8.4 Suspicious

Suspicious মানে activity normal না, কিন্তু final proof এখনো পাওয়া যায়নি।

Example:

```text
Unknown IP থেকে login হয়েছে, MFA successful, কিন্তু user location mismatch করছে।
```

## 8.5 Needs Escalation

Needs Escalation মানে L1 analyst final decision নিতে পারছে না বা risk বেশি, তাই L2 support দরকার।

Example:

```text
User বলছে login করেনি, কিন্তু logs successful MFA দেখাচ্ছে।
```

---

# Module 9: Alert Reporting

## 9.1 Why L1 Analysts Write Reports

Alert report দরকার কারণ:

* L2 analyst context পায়
* Future record থাকে
* Investigation quality improve হয়
* Mistake কমে
* Escalation faster হয়

## 9.2 Five Ws Report Format

একটি ভালো alert report-এ Five Ws থাকতে হবে।

### Who

কোন user, host, process, IP involved?

### What

ঠিক কী action হয়েছে?

### When

কখন activity শুরু এবং শেষ হয়েছে?

### Where

কোন device, IP, website, subnet, বা location involved?

### Why

কেন final verdict দেওয়া হলো?

## 9.3 Sample Alert Report Format

```text
Alert Name:
Severity:
Alert Time:
Affected User:
Affected Host:
Source IP:
Destination IP:
Summary:
Investigation Steps:
Evidence:
Verdict:
Reason:
Escalation Required:
Analyst Name:
```

## 9.4 Example Report

```text
Alert Name: Unusual Login Location
Severity: High
Affected User: G.Baker
Source IP: 103.61.240.174
Summary: User logged in from an unusual country not matching HR location.
Investigation: Checked SIEM login logs, identity inventory, and IP reputation.
Evidence: User normally works from UK. Source IP belongs to unknown foreign ISP.
Verdict: Suspicious
Escalation Required: Yes
Reason: Location mismatch and risky IP require L2 validation.
```

---

# Module 10: Alert Escalation

## 10.1 What is Escalation?

Escalation হলো alert L2 analyst বা senior team-এর কাছে পাঠানো, যখন deeper investigation বা action দরকার।

## 10.2 When to Escalate

Escalate করবেন যদি:

* Alert True Positive হয়
* Malware removal দরকার হয়
* Host isolation দরকার হয়
* Password reset দরকার হয়
* User compromise সন্দেহ হয়
* Sensitive asset involved হয়
* Data exfiltration সন্দেহ হয়
* Customer/management communication দরকার হয়
* L1 analyst alert পুরো বুঝতে না পারে

## 10.3 Escalation Steps

General steps:

1. Alert In Progress করুন
2. Investigation complete করুন
3. Report লিখুন
4. Verdict set করুন
5. L2 analyst assign করুন
6. Corporate chat/phone দিয়ে notify করুন
7. Evidence clearly mention করুন

## 10.4 Requesting L2 Support

L1 analyst কোনো alert না বুঝলে blindly close করবে না।

Correct action:

```text
Investigate what you can
Document what you found
Ask L2 for support
```

---

# Module 11: SOC Communication

## 11.1 Communication with L2

যখন urgent alert escalate করবেন:

* Clear summary দিন
* Evidence দিন
* Impact explain করুন
* What action needed বলুন

Example:

```text
Hi, I escalated a High severity VPN compromise alert. Source IP brute forced VPN, got internal IP 10.10.0.53, then scanned Database and Office subnets. Please review urgently.
```

## 11.2 Communication with IT Team

IT team-এর কাছে জানতে হতে পারে:

* Admin privilege granted কি না
* Server maintenance ছিল কি না
* Software installation expected ছিল কি না
* User account change approved ছিল কি না

## 11.3 Communication with HR

HR থেকে জানতে হতে পারে:

* User location
* New employee status
* Terminated employee status
* Department or role

## 11.4 Critical Communication Cases

Case 1: L2 unavailable for critical alert

Action:

```text
Call L2
Call L3
Call SOC Manager
Use emergency contact list
```

Case 2: Chat account compromise

Action:

```text
Breached chat দিয়ে user confirm করবেন না।
Phone বা alternative channel use করুন।
```

Case 3: Too many alerts

Action:

```text
Prioritise critical alerts and inform L2.
```

Case 4: Wrong verdict discovered later

Action:

```text
Immediately inform L2 and explain concern.
```

Case 5: SIEM logs not searchable

Action:

```text
Do not skip alert. Investigate what you can and report to L2/SOC Engineer.
```

---

# Module 12: Identity Inventory

## 12.1 What is Identity Inventory?

Identity Inventory হলো organisation-এর users, service accounts, roles, access, location এবং contact details-এর catalogue।

## 12.2 Why SOC Needs Identity Inventory

Identity inventory দিয়ে analyst বুঝতে পারে:

* User কে?
* User কোন department-এর?
* User-এর normal location কোথায়?
* User-এর role কী?
* User privileged কি না?
* User-এর access expected কি না?

## 12.3 Example Identity Fields

```text
Full Name
Username
Email
Role
Location
Access
Department
Manager
Employment Status
```

## 12.4 Sources of Identity Inventory

Common sources:

* Active Directory
* Entra ID
* Okta
* Google Workspace
* BambooHR
* SAP
* HiBob
* CSV/Excel sheet

## 12.5 Identity Inventory Example

```text
Name: Gregory Baker
Username: G.Baker
Role: Chief Financial Officer
Location: Europe, UK
Access: VPN, HQ, FINANCE
```

SOC meaning:

```text
If G.Baker downloads finance records, it may be expected because he is CFO.
```

---

# Module 13: Asset Inventory

## 13.1 What is Asset Inventory?

Asset Inventory হলো organisation-এর servers, workstations, laptops, IP addresses, OS, owners, and purposes-এর list।

## 13.2 Why SOC Needs Asset Inventory

Asset inventory দিয়ে analyst বুঝতে পারে:

* Hostname কী?
* Device কোথায় located?
* IP address কোন asset-এর?
* Device critical কি না?
* Owner কে?
* Purpose কী?
* Server নাকি workstation?

## 13.3 Asset Inventory Fields

```text
Hostname
Location
IP Address
Operating System
Owner
Purpose
Criticality
Business Unit
```

## 13.4 Sources of Asset Inventory

Common sources:

* Active Directory
* Entra ID
* Elastic
* CrowdStrike
* Microsoft Intune
* Jamf MDM
* CMDB
* CSV/Excel sheets

## 13.5 Asset Inventory Example

```text
Hostname: HQ-FINFS-02
Location: UK Datacenter
IP: 172.16.15.89
OS: Windows Server 2022
Owner: Central IT
Purpose: File server for financial records
```

SOC meaning:

```text
This is a sensitive finance file server, so suspicious access must be prioritised.
```

---

# Module 14: Network Diagrams for SOC Analysts

## 14.1 What is a Network Diagram?

Network diagram হলো organisation-এর network locations, subnets, firewall, servers, VPN, DMZ, and connections-এর visual map।

## 14.2 Why SOC Needs Network Diagrams

Network diagram দিয়ে analyst বুঝতে পারে:

* কোন subnet কী কাজ করে
* কোন IP কোন network-এর
* VPN user কোথা থেকে আসছে
* Firewall কী protect করছে
* কোন traffic suspicious
* Attack path কী হতে পারে

## 14.3 Example Network Scenario

Alert chain:

```text
08:00 - 103.61.240.174 connects to firewall TCP/10443
08:23 - IP translated to internal 10.10.0.53
08:25 - 10.10.0.53 scans 172.16.15.0/24
08:32 - 10.10.0.53 scans 172.16.23.0/24
```

Network diagram meaning:

```text
TCP/10443 = VPN service
10.10.0.0/16 = VPN subnet
172.16.15.0/24 = Database subnet
172.16.23.0/24 = Office subnet
```

## 14.4 Attack Path Reconstruction

Possible attack path:

1. Threat actor from 103.61.240.174 performed VPN brute force
2. VPN login was successful
3. Attacker received internal VPN IP 10.10.0.53
4. Attacker scanned Database subnet
5. Firewall likely blocked Database access
6. Attacker switched to Office subnet scanning
7. Scenario is likely True Positive

---

# Module 15: SOC Workbooks, Playbooks, Runbooks, and Workflows

## 15.1 Playbook

Playbook হলো incident handle করার high-level plan।

Example:

```text
Phishing Playbook
Malware Playbook
Unusual Login Playbook
```

## 15.2 Runbook

Runbook হলো exact technical steps।

Example:

```text
How to disable AD account
How to isolate host in EDR
How to block IP in firewall
```

## 15.3 Workflow

Workflow হলো process sequence।

Example:

```text
Alert Received
↓
Enrichment
↓
Investigation
↓
Verdict
↓
Escalation or Closure
```

## 15.4 Workbook

Workbook হলো analyst-এর step-by-step investigation document/checklist।

SOC L1 analyst workbooks সবচেয়ে বেশি ব্যবহার করে।

## 15.5 Workbook Example: Unusual Login Location

### Phase 1: Enrichment

Use Threat Intelligence and identity inventory to collect information.

Check:

* User role
* User location
* User department
* Login IP
* IP reputation
* Travel status
* Known device

### Phase 2: Investigation

Use SIEM logs and gathered data to decide if login is expected.

Check:

* Login successful or failed
* MFA status
* Previous login history
* Impossible travel
* Same IP targeting multiple users
* Post-login activity

### Phase 3: Escalation

Escalate to L2 or communicate with the user if necessary.

Escalate if:

* User denies login
* IP is malicious
* MFA bypass occurred
* Sensitive system accessed
* Post-login activity suspicious

---

# Module 16: Threat Intelligence and Lookups

## 16.1 What is Threat Intelligence?

Threat Intelligence হলো known malicious IP, domain, URL, hash, malware, campaign, and attacker behaviour সম্পর্কে information।

## 16.2 Common TI Lookups

SOC L1 analyst check করতে পারে:

* IP reputation
* Domain reputation
* URL reputation
* File hash reputation
* ASN
* Geo-location
* WHOIS
* Known malware indicators

## 16.3 Example

Alert:

```text
Login from IP 103.61.240.174
```

TI lookup questions:

* IP malicious কি না?
* VPN/proxy/Tor কি না?
* কোন country?
* আগে brute force activity করেছে কি না?
* Multiple customers report করেছে কি না?

---

# Module 17: SIEM Basics for SOC L1

## 17.1 What is SIEM?

SIEM হলো Security Information and Event Management platform।

SIEM কাজ:

* Logs collect করে
* Logs normalize করে
* Search করার সুযোগ দেয়
* Detection rules চালায়
* Alerts generate করে
* Dashboard/reporting দেয়

## 17.2 Common SIEM Sources

* Firewall logs
* VPN logs
* Active Directory logs
* Windows Event logs
* EDR logs
* Email security logs
* Web proxy logs
* Cloud logs
* DNS logs

## 17.3 Basic SIEM Investigation

L1 analyst should know how to search:

* Username
* Hostname
* Source IP
* Destination IP
* File hash
* Process name
* Command line
* Time range

---

# Module 18: SOC Metrics and Objectives

## 18.1 SOC Objective

SOC-এর objective হলো organisation-এর digital assets protect করা এবং threat দ্রুত detect/respond করা।

## 18.2 Alerts Count

Formula:

```text
AC = Total Count of Alerts Received
```

Measures:

```text
Overall load of SOC analysts
```

Good general range:

```text
5 to 30 alerts per day per L1 analyst
```

Too many alerts:

```text
Analyst overload and real threat may be missed
```

Zero alerts for long time:

```text
May indicate SIEM/log/detection issue
```

## 18.3 False Positive Rate

Formula:

```text
FPR = False Positives / Total Alerts
```

Measures:

```text
Level of noise in alerts
```

Example:

```text
Total alerts = 50
Real threats = 10
False positives = 40
FPR = 40 / 50 = 80%
```

80% or higher is a serious problem.

## 18.4 Alert Escalation Rate

Formula:

```text
AER = Escalated Alerts / Total Alerts
```

Measures:

```text
Experience and independence of L1 analysts
```

Target:

```text
Below 50%, better below 20%
```

## 18.5 Threat Detection Rate

Formula:

```text
TDR = Detected Threats / Total Threats
```

Measures:

```text
Reliability of SOC team
```

Ideal target:

```text
100%
```

A missed threat can cause:

* Ransomware
* Data exfiltration
* Business disruption
* Lateral movement

---

# Module 19: SLA, MTTD, MTTA, and MTTR

## 19.1 SLA

SLA = Service Level Agreement.

It defines how quickly SOC must detect, acknowledge, and respond to alerts.

Example SLA:

```text
SOC Availability: 24/7
MTTD: 5 minutes
MTTA: 10 minutes
MTTR: 60 minutes
```

## 19.2 SOC Team Availability

SOC can work:

* 8/5: Business hours, Monday to Friday
* 24/7: Always available

If team works 8/5 and critical alert comes on Saturday, it may be acknowledged on Monday.

## 19.3 MTTD

MTTD = Mean Time To Detect.

Meaning:

```text
Average time between attack and SOC tool detection
```

Example:

```text
Attack starts: 10:00
Alert received: 10:12
MTTD = 12 minutes
```

## 19.4 MTTA

MTTA = Mean Time To Acknowledge.

Meaning:

```text
Average time for L1 analyst to start triage after alert appears
```

Example:

```text
Alert received: 10:12
L1 moved alert to In Progress: 10:22
MTTA = 10 minutes
```

## 19.5 MTTR

MTTR = Mean Time To Respond.

Meaning:

```text
Average time taken by SOC to stop the breach from spreading
```

Example:

```text
L2 cleanup completed 35 minutes after escalation
Total response time from detection to remediation = 51 minutes
```

---

# Module 20: Improving SOC Metrics as L1 Analyst

## 20.1 Improving False Positive Rate

Problem:

```text
FPR over 80%
```

Recommendations:

* Exclude trusted activities from detection rules
* Tune SIEM/EDR rules
* Add approved system updates to allowlist
* Document common false positive reasons
* Suggest SOAR automation for repeated benign alerts

## 20.2 Improving MTTD

Problem:

```text
MTTD over 30 minutes
```

Recommendations:

* Contact SOC engineers
* Check detection rule schedule
* Ensure logs are collected in real time
* Identify delayed log sources

## 20.3 Improving MTTA

Problem:

```text
MTTA over 30 minutes
```

Recommendations:

* Ensure real-time alert notification
* Distribute alert queue evenly
* Prioritise critical alerts
* Avoid leaving alerts unassigned

## 20.4 Improving MTTR

Problem:

```text
MTTR over 4 hours
```

Recommendations:

* Escalate threats quickly to L2
* Follow documented playbooks
* Provide clear report to L2
* Communicate urgent cases fast
* Ensure attack scenario procedures exist

---

# Module 21: Beginner Practical Labs

## Lab 1: Identify Alert Properties

Given an alert, identify:

* Alert time
* Alert name
* Severity
* Status
* Verdict
* Assignee
* Description
* Fields

## Lab 2: True Positive or False Positive

Given 5 alerts, decide:

* True Positive
* False Positive
* Suspicious
* Needs Escalation

## Lab 3: Basic Report Writing

Write a report using Five Ws:

* Who
* What
* When
* Where
* Why

## Lab 4: Identity Inventory Lookup

Given a username, find:

* Role
* Location
* Access
* Department
* Expected activity

## Lab 5: Asset Inventory Lookup

Given hostname/IP, find:

* Asset owner
* Purpose
* OS
* Location
* Criticality

---

# Module 22: Intermediate Practical Labs

## Lab 6: Unusual Login Investigation

Investigate:

* User location
* Login IP
* IP reputation
* MFA status
* Login history
* Verdict

## Lab 7: VPN Brute Force Investigation

Investigate:

* Source IP
* Failed login count
* Successful login
* Assigned internal IP
* Post-login activity

## Lab 8: Network Scanning Investigation

Investigate:

* Source host
* Destination subnet
* Open ports
* Asset purpose
* Firewall blocks
* Attack path

## Lab 9: Escalation Practice

Prepare:

* Alert report
* Verdict
* Evidence
* L2 escalation message

---

# Module 23: Advanced SOC L1 Skills

## 23.1 Advanced Triage Mindset

Advanced L1 analyst should:

* Think in attack chains
* Correlate multiple alerts
* Use identity, asset, and network context
* Avoid premature False Positive verdicts
* Understand business impact
* Know when to escalate fast

## 23.2 Alert Correlation

Example chain:

```text
VPN brute force
↓
Successful login
↓
Internal IP assigned
↓
Database subnet scanning
↓
Office subnet scanning
```

This is stronger evidence than a single alert.

## 23.3 Attack Path Analysis

L1 should identify:

* Initial access
* Internal access
* Reconnaissance
* Lateral movement possibility
* Sensitive asset targeting

## 23.4 Quality Escalation

A quality escalation includes:

* Short summary
* Clear timeline
* Evidence
* Affected user/host/IP
* Risk explanation
* What L2 should review next

---

# Module 24: Final Capstone Scenario

## Scenario

A user receives an unusual login alert. The source IP is unknown. Threat Intelligence marks the IP as suspicious. Identity inventory shows the user normally works from the UK. SIEM logs show successful MFA, followed by file access to a sensitive finance server. The user does not confirm the activity.

## Student Tasks

1. Perform enrichment
2. Check identity inventory
3. Check asset inventory
4. Review SIEM logs
5. Determine verdict
6. Write report
7. Decide escalation
8. Write L2 escalation message
9. Calculate related metrics if applicable

## Expected Verdict

```text
Needs Escalation / Suspicious / Possible True Positive
```

## Expected Action

```text
Escalate to L2 immediately.
```

---

# Final Learning Outcomes

After completing this course, learners will be able to:

* Explain what SOC is
* Understand SOC L1, L2, SOC Engineer, and SOC Manager roles
* Identify alert properties
* Perform basic and intermediate alert triage
* Distinguish True Positive and False Positive
* Use identity inventory
* Use asset inventory
* Read network diagrams
* Understand attack path from firewall/VPN logs
* Use workbooks/playbooks/runbooks/workflows
* Write proper alert reports
* Escalate alerts to L2 correctly
* Understand SOC metrics like AC, FPR, AER, TDR
* Understand SLA, MTTD, MTTA, MTTR
* Improve SOC performance as an L1 analyst
* Handle communication during critical alerts
* Work as a beginner-to-advanced SOC Level 1 Analyst
