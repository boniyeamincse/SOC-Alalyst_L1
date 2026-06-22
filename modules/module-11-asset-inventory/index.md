# Module 11: Asset Inventory for SOC

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- Asset inventory কি এবং কেন critical
- Asset sources: AD, SIEM, EDR, MDM, CMDB, CSV
- Asset types: Servers, workstations, network devices, cloud
- Asset attributes এবং তাদের মানে
- Asset criticality: Critical, high, medium, low
- Asset lifecycle: Provisioning, active, decommission
- Asset owner এবং responsibility
- Using assets in investigations
- Critical asset protection
- Red flags for compromised assets
- Real SOC asset scenarios

---

## শুরুর আগে: একটি গল্প

ফাতিমা একজন SOC L1 analyst। Alert আসে: "Database server accessed unusually".

Approach 1 (Without asset context):
```
09:00 - Alert দেখলো
09:05 - "Database server accessed" → Sounds critical
09:10 - Immediately escalate to IR (alert fatigue)
Reality: Test database, non-critical, false positive
```

Approach 2 (With asset context):
```
09:00 - Alert দেখলো
09:02 - "Database server accessed"
09:03 - Check asset inventory:
       └─ Server name: db-test-01
       └─ Type: Test database
       └─ Criticality: LOW
       └─ Environment: Dev/test (not production)
       └─ Owner: QA team
       
09:05 - Context verified:
       └─ QA team normal testing pattern
       └─ Access appropriate
       └─ Verdict: Benign
       
Close alert (no false escalation)
```

**Asset context = Faster, accurate decisions.**

---

## Asset Inventory কি?

### Definition:

**Asset Inventory = Complete database of all technology resources in organization.**

```
Includes:
├─ Servers (physical, virtual, cloud)
├─ Workstations (desktops, laptops)
├─ Network devices (routers, switches, firewalls)
├─ Mobile devices (phones, tablets)
├─ IoT devices (printers, cameras, sensors)
├─ Cloud infrastructure (VMs, databases, storage)
├─ Applications (software licenses)
└─ Data repositories (file shares, databases)

Information tracked:
├─ Asset identification (name, IP, MAC)
├─ Asset type (server, workstation, etc.)
├─ Owner (department, team, individual)
├─ Location (physical or cloud region)
├─ OS and software version
├─ Criticality level (business importance)
├─ Access level (who can access)
├─ Patch status (security updates)
├─ Status (active, decommissioned, retired)
└─ Last activity timestamp
```

### Why Asset Inventory Matters:

```
Without asset inventory:
├─ Alert: "IP 10.0.1.50 accessed"
├─ Response: Don't know what 10.0.1.50 is
├─ Action: Guess criticality
└─ Result: Over-escalate or miss real threats

With asset inventory:
├─ Alert: "IP 10.0.1.50 accessed"
├─ Lookup: 10.0.1.50 = "finance-db-prod"
├─ Context: Production database (CRITICAL)
├─ Impact: Financial data accessible
└─ Response: Appropriate urgency
```

---

## Asset Sources

### **1. Active Directory (AD)**

```
Contains:
├─ Computer accounts (servers, workstations)
├─ Computer groups
├─ OU structure (organizational units)
├─ Group policies (applied to assets)
└─ Device properties

Information available:
├─ Computer name
├─ DNS name
├─ OS version (registered)
├─ IP address (DHCP registration)
├─ Last logon (device)
├─ Owner (usually user, not always)
├─ Location (OU-based)
├─ Group memberships (determines access)
└─ Last sync time

How L1 uses:
├─ Search computer name
├─ See: Associated user
├─ See: Groups (access rights)
├─ See: Last activity
└─ Verify: Expected device

Limitations:
├─ Only Windows/AD-joined devices
├─ Cloud resources: Not always registered
├─ Older devices: May be stale
└─ BYOD/contractors: May not be registered
```

### **2. SIEM (Security Information Event Management)**

```
SIEM collects logs from all sources, builds asset database.

Contains:
├─ Devices generating logs
├─ IP addresses seen
├─ Hostnames identified
├─ OS types detected
├─ Applications running
└─ Network connections

Information available:
├─ IP address (primary identifier)
├─ Hostname (if detected in logs)
├─ OS (inferred from log format)
├─ Last seen (timestamp of last activity)
├─ Traffic patterns (normal vs anomalous)
└─ Applications (from process logs)

How L1 uses:
├─ Search IP address
├─ See: Associated hostname
├─ See: Activity timeline
├─ See: Last seen when
└─ Check: Is device still active?

Advantages:
├─ Captures ALL devices generating logs
├─ Real-time updates
├─ Activity timeline
├─ Cross-reference with alerts
└─ Behavioral baseline

Limitations:
├─ Devices without logs: Not captured
├─ Lag time: Logs delayed by hours
├─ May have stale data
└─ Device metadata minimal
```

### **3. EDR (Endpoint Detection Response)**

```
EDR agent runs on endpoints, collects detailed device data.

Contains:
├─ Enrolled devices only
├─ Detailed device hardware
├─ OS and patch level
├─ Software inventory
├─ Network connections
├─ User logged in
├─ Security software status
└─ Device health status

Information available:
├─ Device name
├─ IP address (current)
├─ MAC address
├─ OS version and patch level
├─ Installed applications (detailed)
├─ Logged-in user
├─ MFA status
├─ Antivirus/EDR status
├─ Last seen
└─ Risk score

How L1 uses:
├─ Search device name
├─ See: Current user logged in
├─ See: Malware/risk status
├─ See: Patch compliance
├─ See: Last activity
└─ Check: Device compromised?

Advantages:
├─ Very detailed device information
├─ Real-time status
├─ Behavior analysis
├─ Malware/threat detection
└─ Patch status tracking

Limitations:
├─ Only installed devices
├─ May not cover all devices (coverage gaps)
├─ IoT/network devices: Often not covered
└─ Lag time: Data collection delay
```

### **4. MDM (Mobile Device Management)**

```
Manages mobile devices (phones, tablets).

Contains:
├─ Mobile devices enrolled
├─ Device type (iOS, Android)
├─ Device owner (user)
├─ OS version
├─ App inventory
├─ Security status
├─ Location data
└─ Compliance status

Information available:
├─ Device ID
├─ Phone number/IMEI
├─ Device owner
├─ OS and version
├─ Apps installed
├─ JailBreak/root status
├─ Location (if enabled)
├─ Last seen
└─ Compliance: Encryption, password policy

How L1 uses:
├─ Search device owner
├─ See: Devices owned
├─ See: Security status
├─ See: Jailbreak warning
├─ See: App compliance
└─ Check: Unauthorized apps?

Limitations:
├─ Only enrolled devices
├─ Personal devices: Often not enrolled
├─ BYOD: Variable coverage
└─ Non-managed devices: Invisible
```

### **5. CMDB (Configuration Management Database)**

```
IT operations database of all IT assets.

Contains:
├─ Complete asset inventory
├─ Relationships between assets
├─ Configuration items (CI)
├─ Change history
├─ Maintenance history
├─ Ownership structure
└─ Business alignment

Information available:
├─ Asset ID (unique)
├─ Asset name
├─ Asset type (detailed)
├─ Owner (department, team, individual)
├─ Location (physical address or cloud region)
├─ Status (active, retired, planned)
├─ Business service dependent on asset
├─ SLA/criticality level
├─ Maintenance window
├─ Vendor/support info
└─ Cost/budget info

How L1 uses:
├─ Search asset name
├─ See: Ownership (who responsible)
├─ See: Criticality (business importance)
├─ See: Related systems
├─ See: Maintenance windows
└─ Contact: Owner if needed

Advantages:
├─ Most complete inventory
├─ Business context (SLA, owner)
├─ Relationships (dependencies)
├─ Historical tracking
├─ Change management integration

Limitations:
├─ Often outdated (manual updates)
├─ May not reflect current state
├─ Only IT-managed assets
├─ Access: May be restricted
```

### **6. CSV/Excel Spreadsheets**

```
Manual asset tracking (common in small organizations).

Contains:
├─ IP address
├─ Hostname
├─ Asset type
├─ Owner
├─ Location
├─ Criticality
├─ Last update
└─ Notes

Characteristics:
├─ Manual maintenance (error-prone)
├─ Often outdated
├─ Missing fields
├─ Inconsistent format
└─ No real-time updates

How L1 uses:
├─ Search IP or hostname
├─ See: Owner contact
├─ See: Criticality
├─ See: Update date (is it fresh?)
└─ Caveat: May be outdated

Limitations:
├─ VERY unreliable
├─ No automation
├─ Gaps common
├─ Can't query effectively
└─ Often duplicates/errors
```

---

## Asset Types & Criticality

### Asset Classifications:

```
TIER 1: CRITICAL ASSETS (Production business systems)
├─ Production database servers
├─ Email servers
├─ Active Directory domain controllers
├─ Payment processing systems
├─ Web application servers
├─ VoIP systems
├─ Backup systems (also critical)
└─ Firewalls and network core
Impact if compromised: Business stops, revenue loss

TIER 2: HIGH-IMPORTANCE ASSETS (Important but not critical)
├─ File servers
├─ Development database servers
├─ Internal applications
├─ Monitoring systems
├─ Collaboration tools
└─ Corporate network printers
Impact if compromised: Work disrupted, data at risk

TIER 3: MEDIUM-IMPORTANCE ASSETS (Normal work devices)
├─ Developer workstations
├─ Office workstations
├─ Department printers
├─ Meeting room displays
└─ Time tracking devices
Impact if compromised: Individual productivity loss

TIER 4: LOW-IMPORTANCE ASSETS (Minimal business impact)
├─ Test servers
├─ Lab environments
├─ Sandbox systems
├─ Guest WiFi devices
├─ Visitor laptops
└─ Retired systems still online
Impact if compromised: No significant business impact
```

### Asset Attributes:

```
Every asset should have:

IDENTIFICATION:
├─ Asset name (meaningful, unique)
├─ Asset ID (unique identifier)
├─ IP address (or range for cloud)
├─ MAC address (if applicable)
└─ DNS name

CLASSIFICATION:
├─ Asset type (server, workstation, network device)
├─ OS type (Windows, Linux, iOS, Android)
├─ OS version (specific version for patching)
├─ Environment (production, development, test)
└─ Cloud provider (if cloud-based)

OWNERSHIP:
├─ Owner (person responsible)
├─ Team (IT, Finance, Engineering)
├─ Department
├─ Cost center
└─ Manager chain

BUSINESS CONTEXT:
├─ Business criticality (Tier 1-4)
├─ Business service (what does it support?)
├─ Data classification (what data stored?)
├─ SLA (uptime requirement)
├─ Backup status
└─ Disaster recovery plan

SECURITY:
├─ Last patch applied (security updates)
├─ Antivirus status
├─ EDR status
├─ Firewall rules
├─ Encryption status
└─ Compliance (PCI, HIPAA, SOC2, etc.)

LIFECYCLE:
├─ Asset status (active, retired, planned)
├─ Provisioning date
├─ Last update date
├─ Maintenance window
├─ End of life date (planned)
└─ Decommission date (if retired)
```

---

## Asset in Investigation

### Using Assets to Understand Context:

```
Investigation workflow:

STEP 1: Alert mentions asset
Example: "Suspicious access to 192.168.10.50"

STEP 2: Asset lookup
├─ Search: IP 192.168.10.50
├─ Found: finance-db-prod
├─ Type: SQL Server
├─ Criticality: TIER 1 (CRITICAL!)
└─ Owner: Finance team lead

STEP 3: Understand criticality
├─ This is production database
├─ Contains financial data
├─ Business-critical system
├─ Impact of compromise: SEVERE
└─ Investigation priority: IMMEDIATE

STEP 4: Assess impact
├─ If normal: Just access
├─ If suspicious: Data at risk
├─ If compromised: Business could stop
└─ Action: Proportional to criticality

STEP 5: Contact asset owner
├─ Owner: Finance team lead
├─ Question: "Was this access authorized?"
├─ Action: May need immediate containment
└─ Document: Owner notification
```

### Asset Owner Responsibilities:

```
Who owns the asset determines:
├─ Who approves access
├─ Who troubleshoots issues
├─ Who updates/patches
├─ Who receives alerts
└─ Who makes business decisions

When investigating, L1 can:
├─ Contact asset owner
├─ Verify if access expected
├─ Get business context
├─ Escalate if dangerous
└─ Document owner notification
```

### Critical Asset Special Handling:

```
CRITICAL ASSETS (Tier 1) need extra attention:

Alert comes in for critical asset:
├─ Acknowledge immediately (< 1 minute)
├─ Brief triage only (is it real?)
├─ If ANY suspicion: Escalate IMMEDIATELY
├─ Don't waste time investigating
├─ Let L2/IR handle
└─ Containment may be needed

Example:
Alert: "Unusual process on domain controller"
Response:
├─ 09:00 - Alert received
├─ 09:01 - Confirmed it's real domain controller
├─ 09:02 - ESCALATE to IR immediately
├─ 09:03 - IR team decides: Isolate or not?
└─ No deep investigation at L1 level
```

---

## Real-World Asset Scenarios

### **Scenario 1: Test Database Alert**

```
ALERT: "Database server accessed from unusual IP"
SEVERITY: HIGH (alert rule)

Investigation:

Step 1: Asset lookup
├─ IP: 10.0.5.100
├─ Asset: db-test-001
├─ Type: Test database server
├─ Criticality: TIER 4 (LOW)
├─ Owner: QA team
└─ Environment: Testing (not production)

Step 2: Context
├─ Production database: CRITICAL
├─ But this is: TEST database
├─ Impact of compromise: MINIMAL
├─ Testing activity: Expected
└─ Verdict: Different priority than production

Step 3: Access assessment
├─ "Unusual IP" from alert rule
├─ But QA team: Often different IPs
├─ VPN, remote testing: Common
├─ Access appropriate: YES
└─ Expected for test team

VERDICT: BENIGN
REASON: Test database, QA team normal testing
ACTION: Close alert
RECOMMENDATION: Consider lowering severity for test assets
```

### **Scenario 2: Production Server Compromise**

```
ALERT: "Unusual process on web server"
SEVERITY: HIGH

Investigation:

Step 1: Asset lookup
├─ Hostname: web-prod-01
├─ Type: Production web server
├─ Criticality: TIER 1 (CRITICAL!)
├─ Owner: Engineering team
├─ OS: Linux Ubuntu
└─ Data: Customer data, payment processing

Step 2: Asset importance
├─ This is production server
├─ Handles customer traffic
├─ May contain sensitive data
├─ Compromise = Revenue impact
└─ Action: IMMEDIATE handling

Step 3: Process investigation
├─ Process name: unknown_process.bin
├─ EDR behavior: Suspicious
├─ Network activity: Outbound to malicious IP
├─ Files accessed: Payment processing files
└─ Risk: Data theft, system compromise

Step 4: Threat assessment
├─ Multiple threat indicators
├─ Critical asset affected
├─ Clear malicious behavior
└─ Action: MUST escalate

VERDICT: TRUE_POSITIVE
ACTION: ESCALATE to IR immediately
IMMEDIATE ACTIONS (IR will do):
├─ Isolate server from network
├─ Preserve evidence
├─ Audit data access
├─ Notify customer if needed
├─ Coordinate with business leadership
└─ Potential incident declaration
```

### **Scenario 3: Decommissioned Asset Activity**

```
ALERT: "Server access detected"
SEVERITY: MEDIUM

Investigation:

Step 1: Asset lookup
├─ Server: legacy-app-server
├─ Status: RETIRED (decommissioned 6 months ago)
├─ Criticality: TIER 4 (was low)
├─ Current status in inventory: "Decommissioned"
└─ Expected activity: NONE

Step 2: Red flag!
├─ Decommissioned server = should be offline
├─ But activity detected = PROBLEM
├─ Possibilities:
│  ├─ Server not properly shut down
│  ├─ Wrong server in alert (similar name)
│  ├─ Old IP reassigned to new device
│  └─ Security issue (hacked, still online)

Step 3: Verification
├─ Check asset inventory status
│  └─ Status shows: "Decommissioned"
├─ Check physical location
│  └─ Should be: Off, in storage, or destroyed
├─ Check network:
│  └─ Is device reachable? Try ping
├─ Check EDR:
│  └─ Is device still registered?

Step 4: Assessment
├─ If device still powered on = oversight
├─ If activity = security concern
├─ Needs verification from owner
└─ Action: Investigate and shut down

VERDICT: SUSPICIOUS
ACTION: ESCALATE for verification
NEXT STEPS:
├─ Contact IT operations (asset owner)
├─ Verify: Should device be online?
├─ If no: Shut down immediately
├─ If yes: Update inventory (device not really decommissioned)
└─ Audit: Why wasn't it properly decommissioned?
```

---

## Asset Red Flags

### Warning Signs:

```
RED FLAG 1: Asset in inventory but unreachable
├─ Asset: Should be active
├─ But: No response to ping
├─ Implies: Device offline (unplanned)
├─ Action: Verify status, contact owner

RED FLAG 2: Asset active but not in inventory
├─ Device: Detected in SIEM/EDR
├─ But: Not in asset inventory
├─ Implies: Rogue device or new device
├─ Action: Identify device, add to inventory

RED FLAG 3: Asset status mismatch
├─ Inventory says: "Decommissioned"
├─ But: Activity detected
├─ Implies: Inventory not updated OR device still online
├─ Action: Verify status, take action

RED FLAG 4: Unknown asset detected
├─ IP activity: 10.0.1.200
├─ Inventory: No match for IP
├─ Implies: Rogue device on network
├─ Action: Investigate source, block if needed

RED FLAG 5: Critical asset unusual access
├─ Asset: Tier 1 (critical)
├─ Activity: Outside normal pattern
├─ Implies: Possible compromise
├─ Action: ESCALATE immediately

RED FLAG 6: Asset compromised
├─ Malware: Detected on device
├─ Implies: Device infected
├─ Action: Isolate, forensics, clean

RED FLAG 7: Excessive asset access
├─ User accessing: Many systems unusual
├─ Implies: Privilege escalation or lateral movement
├─ Action: Investigate access pattern

RED FLAG 8: Asset beyond end-of-life
├─ OS: Unsupported version
├─ Implies: No security updates, vulnerable
├─ Action: Patch, upgrade, or decommission
```

---

## Asset Investigation Checklist

### **Quick Asset Verification (1 minute)**

- [ ] Search: Asset name/IP/hostname
- [ ] Found in inventory?
- [ ] Check: Asset status (active/retired?)
- [ ] Check: Criticality level (Tier 1-4?)
- [ ] Check: Asset owner/department

### **Deep Asset Context (3-5 minutes)**

- [ ] Asset type: What is this device?
- [ ] OS version: Patch status current?
- [ ] Criticality: Business impact if compromised?
- [ ] Owner: Who responsible?
- [ ] Last activity: When was normal activity?
- [ ] Access rights: Who should access it?
- [ ] Data: What sensitive data on this asset?
- [ ] Backup: Is asset backed up?

### **Threat Assessment for Asset**

- [ ] Asset criticality: High priority?
- [ ] Alert severity appropriate?
- [ ] Activity pattern normal?
- [ ] Access from expected location?
- [ ] User/process expected?
- [ ] Malware/compromise signals?

### **Decision Making**

- [ ] Is activity appropriate for asset type?
- [ ] Is access appropriate for asset criticality?
- [ ] Any red flags from asset data?
- [ ] Critical asset needs escalation?
- [ ] Need owner notification?

---

## Common Asset Mistakes

### ❌ **Mistake 1: Ignoring asset criticality**

**সমস্যা:**
```
Alert about critical asset
But treat same as low-priority alert
Result: Delayed response on critical system
```

**সমাধান:**
```
Always check asset criticality FIRST
Adjust response time accordingly
Critical asset = Escalate faster
```

---

### ❌ **Mistake 2: Alert fatigue from low-criticality**

**সমস্যা:**
```
Many alerts on test systems
Treat with same urgency as production
Result: Alert fatigue, miss real threats
```

**সমাধান:**
```
Filter/suppress alerts on low-criticality assets
Investigate more carefully on critical assets
Different rules for different tiers
```

---

### ❌ **Mistake 3: Not verifying asset exists**

**সমস্যা:**
```
Asset name in alert
But might be typo or old asset name
Investigate wrong asset or ghost asset
```

**সমাধান:**
```
Always verify asset in inventory
Confirm it's current, active device
Not retired or renamed
```

---

### ❌ **Mistake 4: Missing asset relationships**

**সমস্যা:**
```
Alert on server1
But server1 depends on database2
Investigation doesn't check database
Misses related compromise
```

**সমাধान:**
```
Understand asset dependencies
If server1 compromised, check databases
Check related systems
```

---

### ❌ **Mistake 5: Outdated asset inventory**

**সমস्या:**
```
Asset inventory says: "Server offline"
But activity detected today
Trust inventory without verification
Result: Wrong conclusion
```

**সমাধান:**
```
Treat inventory as reference, not truth
Verify with SIEM/EDR if discrepancy
Asset data can be outdated
Always check current status
```

---

## Mini Quiz: Asset Inventory

### **Question 1: Asset inventory র primary purpose কোনটি?**

A) Track all technology costs  
B) Provide context for investigations  
C) Manage software licenses  
D) Monitor network bandwidth

**Answer:** B) Provide context for investigations - Know what asset is = understand criticality & impact

---

### **Question 2: সবচেয়ে reliable asset source কোনটি?**

A) CSV spreadsheet  
B) CMDB (Configuration Database)  
C) Multiple sources combined  
D) Only SIEM

**Answer:** C) Multiple sources combined - No single source perfect, combine for accuracy

---

### **Question 3: Critical asset (Tier 1) এ alert আসলে কি করবেন?**

A) Deep investigation (30 mins)  
B) Escalate immediately after brief triage  
C) Close if looks minor  
D) Wait for next shift

**Answer:** B) Escalate immediately after brief triage - Critical assets need fast escalation, not lengthy investigation

---

### **Question 4: Decommissioned asset এ activity থাকলে?**

A) Ignore, asset is retired  
B) Contact IT to verify status  
C) Escalate as security issue  
D) Close without investigation

**Answer:** B) Contact IT to verify status - Could be oversight OR security issue, needs verification

---

### **Question 5: Asset আছে SIEM এ কিন্তু inventory এ নেই?**

A) False positive alert  
B) Rogue device potentially  
C) Ignore, inventory always right  
D) Just test device

**Answer:** B) Rogue device potentially - Unknown device = RED FLAG, needs investigation

---

## সহজ ভাষায় সারসংক্ষেপ

**Asset Inventory = Database of all technology resources**

**4 Criticality Tiers:**
- **Tier 1:** Critical (production, business stops if down)
- **Tier 2:** High (important but not critical)
- **Tier 3:** Medium (normal work devices)
- **Tier 4:** Low (minimal business impact)

**Key Asset Sources:**
- **AD:** Computer accounts (Windows devices)
- **SIEM:** All devices generating logs
- **EDR:** Enrolled devices (detailed data)
- **MDM:** Mobile devices
- **CMDB:** Complete IT inventory
- **CSV:** Manual tracking (unreliable)

**Asset in Investigation:**
1. Look up asset in inventory
2. Check: Type, criticality, owner
3. Understand: Business impact if compromised
4. Adjust: Response urgency accordingly
5. Contact owner if needed

**Red Flags:**
- Critical asset + unusual activity = ESCALATE
- Decommissioned asset + activity = VERIFY
- Unknown asset detected = INVESTIGATE
- Asset in inventory but offline = CHECK
- Asset data mismatch = VERIFY

**Remember:**
- Criticality determines urgency
- Multiple sources for accuracy
- Asset owner = decision maker
- Critical assets = fast escalation
- Test assets = lower priority

---

## Resources for Learning

**Asset documentation:**
- CMDB access and training
- EDR asset list interface
- SIEM asset queries
- AD computer search

**Your company tools:**
- Asset inventory system
- CMDB access
- Criticality definitions
- Owner contact directory

---

**Module 11 Complete! ✅**

এখন আপনি জানেন:
- ✅ Asset inventory কি এবং কেন important
- ✅ 6টি major asset sources
- ✅ 4টি criticality tiers
- ✅ Asset attributes এবং classification
- ✅ Asset types (servers, workstations, devices)
- ✅ Asset lifecycle management
- ✅ Using assets to understand investigation context
- ✅ Critical asset special handling
- ✅ Asset owner responsibilities
- ✅ 8টি asset red flags
- ✅ Real-world asset scenarios
- ✅ Common asset mistakes
- ✅ Asset investigation checklist

Progress: **11 of 28 modules complete (39%)**

