# Module 16: SIEM Investigation for SOC L1

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- SIEM কীভাবে কাজ করে investigation এর জন্য
- SIEM interface navigation
- Basic search এবং query fundamentals
- Timeline visualization
- Log correlation এবং pivoting
- Saved searches এবং dashboards
- Common SIEM queries
- Timeline construction in SIEM
- Multi-source correlation
- SIEM limitations এবং gaps
- Real investigation workflows
- Common SIEM mistakes

---

## শুরুর আগে: একটি গল্প

করিম একজন SOC analyst। Alert: "Suspicious file downloaded".

Without SIEM knowledge:
```
09:00 - Alert পেলো
09:05 - "Don't know how to investigate"
09:10 - Escalate immediately (no investigation)
```

With SIEM knowledge:
```
09:00 - Alert পেলো
09:02 - SIEM search: "user john.doe"
       └─ See: All john's activity
09:04 - Timeline view:
       └─ 09:00: Email received
       └─ 09:01: File downloaded
       └─ 09:02: File executed
09:06 - Correlation:
       └─ File hash + TI lookup in SIEM
09:08 - Verdict: Malware confirmed
09:10 - Escalate with full context
```

**SIEM skills = Faster, complete investigation.**

---

## SIEM কীভাবে কাজ করে

### SIEM Architecture Quick Review:

```
Multiple data sources:
├─ Windows Event Logs
├─ Linux Syslog
├─ Firewall logs
├─ Network traffic
├─ Application logs
└─ etc.

        │
        ▼
    SIEM Ingestion
    (Collect + Parse + Normalize)
        │
        ▼
    SIEM Database
    (Indexed for search)
        │
        ▼
    SIEM Interface
    ├─ Search interface
    ├─ Dashboards
    ├─ Alerts
    └─ Reports

L1 interaction:
└─ Use search interface
└─ Query indexed data
└─ Build timeline
└─ Make decisions
```

### Why SIEM for Investigation:

```
Without SIEM:
├─ Logs on individual devices
├─ Hard to search
├─ No correlation
├─ Manual timeline building
├─ Time-consuming

With SIEM:
├─ All logs central location
├─ Fast search (indexed)
├─ Automatic correlation
├─ Timeline visualization
├─ Efficiency multiplied
```

---

## SIEM Search Basics

### Search Types:

```
SIMPLE SEARCH:
└─ Find all events matching criteria
   Example: username="john.doe"
   Result: All john's activity
   Time: Seconds

STRUCTURED QUERY:
└─ Use specific syntax (Lucene, SPL, KQL)
   Example: username=john.doe AND action=login
   Result: John's logins only
   Time: Seconds

TIME-RANGE QUERY:
└─ Add time constraint
   Example: username=john.doe earliest=-24h
   Result: John's activity last 24 hours
   Time: Minutes

COMPLEX CORRELATION:
└─ Multi-condition query
   Example: 
   ├─ action=failed_login
   ├─ username=john.doe
   ├─ earliest=-1h
   ├─ count > 10
   Result: John with 10+ failures last hour
   Time: Minutes
```

### Basic SIEM Query Syntax:

```
Most SIEM platforms (Splunk, ELK, etc.) use similar:

Basic pattern:
└─ field = value

Examples:
├─ username = "john.doe"
├─ source_ip = "192.168.1.100"
├─ action = "login"
├─ severity = "high"
└─ hostname = "database-server"

Combining conditions:
├─ AND: All must match
│  └─ username="john" AND action="login"
├─ OR: Any can match
│  └─ username="john" OR username="alice"
├─ NOT: Exclude
│  └─ action="login" NOT username="admin"

Time range:
├─ earliest=-24h (last 24 hours)
├─ latest=-1h (last hour to now)
├─ earliest="2024-06-21 09:00" (specific time)
└─ latest="2024-06-21 10:00"

Wildcards:
├─ username="john*" (john, john.doe, johnny)
├─ username="*admin" (*admin, joh_admin)
└─ hostname="web*" (web-01, web-02, web-prod)

Operators:
├─ = (equals)
├─ != (not equals)
├─ > (greater than)
├─ < (less than)
├─ >= / <=
└─ IN (value in list)
```

---

## Common Investigation Queries

### **Query 1: User Activity Timeline**

```
Purpose: See all activity by specific user

Query:
username="john.doe" earliest=-24h

Results show:
├─ All events john generated
├─ All actions john took
├─ All systems john accessed
└─ Complete 24-hour timeline

Analysis:
├─ Group by time: See sequence
├─ Group by host: See systems accessed
├─ Group by action: See types of activity
└─ Count: See volume of activity
```

### **Query 2: Failed Login Attempts**

```
Purpose: Find brute force patterns

Query:
EventCode=4625 earliest=-1h

Results show:
├─ All failed login events
├─ User attempting: ___
├─ Source IP: ___
├─ Target: ___
├─ Count: ___

Pivot options:
├─ Stats by username (who failed most?)
├─ Stats by source_ip (which IP attempted?)
├─ Stats by target_host (which system targeted?)
└─ Timeline (when did attempts occur?)

Decision:
├─ 1-2 failures: Typo (normal)
├─ 5+ failures: Brute force (suspicious)
├─ 50+ failures: Confirmed attack
└─ Distributed IPs: Botnet
```

### **Query 3: System Access Pattern**

```
Purpose: Find unusual system access

Query:
hostname="database-server" AND action="access"
earliest=-7d

Results show:
├─ Who accessed: ___
├─ When: ___
├─ What: ___
├─ How often: ___

Analysis:
├─ Users normally accessing: Expected
├─ New users accessing: Red flag?
├─ Time pattern: Business hours or off-hours?
├─ Frequency: Spike detection?

Investigation:
├─ If unexpected user: RED FLAG
├─ If unexpected time: RED FLAG
├─ If spike in volume: RED FLAG
└─ Otherwise: Normal
```

### **Query 4: File Activity**

```
Purpose: Find file creation/modification

Query:
file_name="malware.exe" OR file_hash="a1b2c3..."

Results show:
├─ When created: ___
├─ By whom: ___
├─ On which system: ___
├─ Size/type: ___
└─ Subsequent activity: ___

Analysis:
├─ First seen: When appeared?
├─ Spread: How many systems?
├─ Access: Who accessed file?
├─ Execution: Was it run?
└─ Deletion: Was it removed?

Investigation:
├─ Single system: Isolated incident
├─ Multiple systems: Widespread malware
├─ Execution detected: Active infection
└─ Recent creation: New malware
```

### **Query 5: Network Connection Pattern**

```
Purpose: Find unusual network connections

Query:
dest_port=3389 AND source_ip="10.0.1.*"
earliest=-24h

Results show:
├─ Source: Which IPs attempting?
├─ Destination: RDP servers?
├─ Port: 3389 (RDP)
├─ Success/failure: Connected or blocked?
├─ Count: How many attempts?

Analysis:
├─ From office subnet: Expected
├─ From external: Red flag
├─ Port 3389: RDP (remote access)
├─ Rapid connections: Brute force
├─ Allowed connections: Check authorized

Investigation:
├─ Internal RDP: Often normal
├─ External RDP: Usually suspicious
├─ Multiple attempts: Brute force
├─ Success after failures: Compromise
```

---

## Timeline Construction in SIEM

### Building Timeline:

```
SIEM search gives events, but unordered initially.

Step 1: Search all related events
└─ Query: username="john.doe" earliest=-24h

Step 2: Sort by timestamp
└─ Results: Chronologically ordered

Step 3: Extract key events
└─ Filter: Show important events only

Step 4: Build narrative
└─ Timeline: Event A → Event B → Event C

Example timeline:

Time       │ Event                    │ Source
-----------|--------------------------|----------
09:00:00   │ Login attempt (failed)   │ Windows log
09:00:15   │ Login attempt (failed)   │ Windows log
09:00:30   │ Login attempt (failed)   │ Windows log
09:01:00   │ Login successful         │ Windows log
09:01:30   │ File accessed: admin.txt │ Fileserver log
09:02:00   │ Email: unusual send      │ Email log
09:03:00   │ Network: outbound traffic│ Firewall log

Analysis:
├─ Failures then success: Compromise attempt
├─ File access after: Unauthorized access
├─ Email unusual send: Possible escalation
├─ Outbound traffic: Data exfiltration?
└─ Verdict: Account compromised
```

---

## SIEM Pivoting

### Pivot Technique:

```
Finding in one query → Pivot to related data

Example pivot:

Initial finding:
└─ Alert: Malicious file on workstation
└─ File hash: abc123...

Pivot 1: Find other systems with same file
└─ Query: file_hash="abc123..."
└─ Results: 5 other systems have this file
└─ Action: Identify compromised systems

Pivot 2: Find who accessed these files
└─ Query: file_hash="abc123..." | stats by user
└─ Results: 3 users accessed file
└─ Action: Check if users compromised

Pivot 3: Find network activity by these users
└─ Query: user="alice" OR user="bob" OR user="charlie"
└─ Results: Unusual outbound connections
└─ Action: Escalate as potential spread

Pivot 4: Find earlier activity
└─ Query: same users earliest=-7d
└─ Results: Activity started 3 days ago
└─ Action: Check for other infections

Result: Initial one alert → Widespread incident discovered
```

### Pivot Decision Tree:

```
Start: Alert or finding

       │
       ▼
   Ask: What's related?
   
   Answer options:
   ├─ Same user: Pivot by username
   ├─ Same system: Pivot by hostname
   ├─ Same file: Pivot by file_hash
   ├─ Same IP: Pivot by source_ip
   ├─ Same pattern: Pivot by signature
   └─ Same time: Pivot by time window
   
       │
       ▼
   Execute pivot query
   
       │
       ▼
   Results show correlation
   
       │
       ▼
   New pivot opportunities?
   
   ├─ Yes: Continue pivoting
   └─ No: Investigation complete
```

---

## SIEM Dashboards & Saved Searches

### Pre-built Dashboards:

```
Organization has pre-built dashboards:

Security Dashboard:
├─ Alert count last 24h
├─ Top alerts by type
├─ Failed login attempts
├─ Critical system access
└─ Malware detections

User Activity Dashboard:
├─ New users logged in
├─ Users accessing critical systems
├─ Unusual data transfers
├─ Off-hours activity
└─ Geographic anomalies

System Health Dashboard:
├─ System patch status
├─ Antivirus status
├─ Disk space warnings
├─ Performance metrics
└─ Connectivity issues

L1 usage:
└─ Browse dashboard
└─ Find specific metric
└─ Drill down if needed
└─ Pivot to detailed search
```

### Saved Searches:

```
Pre-written queries for common investigations:

Examples:
├─ "Brute Force Detection"
├─ "Privilege Escalation"
├─ "Data Exfiltration"
├─ "Malware Activity"
├─ "Phishing Activity"
├─ "Failed Logins"
├─ "Admin Activity"
└─ "VPN Activity"

L1 usage:
├─ Open saved search
├─ Run for specific user/system
├─ Results appear immediately
├─ Modify timeframe if needed
└─ No need to write query from scratch

Advantage:
└─ Tested queries
└─ Known to work
└─ Consistent format
└─ Fast execution
```

---

## SIEM Investigation Workflow

### Complete Investigation in SIEM:

```
STEP 1: Initial Alert Search (2 min)
├─ Alert: IP 10.0.1.100 accessed database
├─ Query: source_ip="10.0.1.100" earliest=-1h
├─ Results: Found 3 accesses to database

STEP 2: Identify Source (1 min)
├─ Pivot: Hostname of 10.0.1.100
├─ Query: src_ip="10.0.1.100" | stats by hostname
├─ Results: admin_workstation

STEP 3: Identify User (1 min)
├─ Pivot: Who's using admin_workstation?
├─ Query: hostname="admin_workstation" AND action="login"
├─ Results: User john.doe

STEP 4: Build Timeline (2 min)
├─ Query: username="john.doe" earliest=-4h
├─ Results: 
│  ├─ 08:00: Logged in (office IP)
│  ├─ 08:30: File accessed (expected)
│  ├─ 14:00: Database accessed (unexpected)
│  └─ 14:05: Another database access

STEP 5: Correlation (2 min)
├─ Pivot: Database access pattern
├─ Query: hostname="database-server" earliest=-24h
│         stats by username
├─ Results: john.doe rarely accesses database
│          This pattern unusual

STEP 6: Enrichment Lookup (1 min)
├─ Check: Why would john access database?
├─ Search: IT tickets for john + database
├─ Results: No approval ticket found

STEP 7: Decision (1 min)
├─ Findings:
│  ├─ Legitimate user: YES
│  ├─ Normal system: YES
│  ├─ Unusual access: YES
│  ├─ No business reason: YES
│  └─ First time database access: YES
└─ Verdict: SUSPICIOUS → Escalate

Total time: 10 minutes
Complete investigation in SIEM
All evidence documented
Ready to escalate to L2
```

---

## SIEM Limitations & Gaps

### What SIEM Cannot See:

```
Encrypted traffic:
└─ HTTPS: Cannot see payload
└─ Can see: IP, port, volume, timing
└─ Cannot see: Content, URLs, commands

Devices without logging:
└─ IoT devices: Often no logs
└─ Personal devices: Not monitored
└─ BYOD: May not have agents
└─ Result: Blind spots

Off-network activity:
└─ Home WiFi: Not visible
└─ Public WiFi: Not visible
└─ Result: No logs during remote activity

Deleted logs:
└─ Attacker: May delete logs
└─ SIEM: Cannot see deleted data
└─ Result: Evidence gap

Local activity:
└─ Offline: No network logs
└─ Local files: Only if monitored
└─ Result: Incomplete picture

Timing issues:
└─ Delay: Logs may lag 1-24 hours
└─ Real-time: Not always real-time
└─ Result: Investigation lag
```

### Handling Limitations:

```
When SIEM data missing:
├─ Check: EDR logs (if available)
├─ Check: Firewall logs (might have data)
├─ Check: Application logs (may complement)
├─ Check: Manual logs (if accessible)
└─ Result: Piece together from multiple sources

When gaps appear:
├─ Note: Gap in evidence
├─ Don't: Assume or guess
├─ Do: Escalate for L2 investigation
└─ Action: May need forensics
```

---

## Common SIEM Mistakes

### ❌ **Mistake 1: Wrong time range**

**সমস्या:**
```
Query: username="john" earliest=-1h
Alert happened 2 hours ago
Results: Nothing found
```

**সমाधান:**
```
Expand time range:
├─ Start wider: earliest=-24h
├─ Refine if needed
└─ Never miss data due to time
```

---

### ❌ **Mistake 2: Wrong field names**

**समس्या:**
```
Query: user="john" (field doesn't exist)
Results: No data found
Correct field: username="john"
```

**समाधान:**
```
Know field names:
├─ username or user?
├─ source_ip or src?
├─ hostname or host?
└─ Ask L2 or check docs
```

---

### ❌ **Mistake 3: Trusting SIEM completeness**

**समस्या:**
```
SIEM search shows: No activity
Assumption: Clean
Reality: Device not logging
```

**समाधान:**
```
Verify logging:
├─ Is device monitored?
├─ Are logs actually flowing?
├─ Check data source status
└─ May have gaps
```

---

### ❌ **Mistake 4: Not pivoting enough**

**समस्या:**
```
Find one event
Report finding
Miss: Correlated events
```

**समाधान:**
```
Always pivot:
├─ Same user: Other activity?
├─ Same system: Other access?
├─ Same pattern: Wider scope?
└─ Correlation = Bigger picture
```

---

### ❌ **Mistake 5: Inefficient queries**

**समस्या:**
```
Query: * (all events)
Results: Billions of events
System: Overwhelmed
```

**समाधान:**
```
Focused queries:
├─ Add filter: earliest/latest
├─ Add field: username/hostname
├─ Add condition: action/status
└─ Result: Manageable set
```

---

## SIEM Investigation Checklist

### **Before Querying**

- [ ] Alert details: What am I looking for?
- [ ] Time frame: When did it happen?
- [ ] Relevant fields: What to search on?
- [ ] Expected data: Should SIEM have it?

### **Query Development**

- [ ] Simple query first: Test syntax
- [ ] Add filters: Time, field, value
- [ ] Results make sense? (sanity check)
- [ ] Too many results? (narrow query)
- [ ] Too few results? (expand query)

### **Timeline Analysis**

- [ ] Events ordered: Chronological?
- [ ] Gaps: Any missing data?
- [ ] Sequence: Does story make sense?
- [ ] Related events: Correlated?

### **Pivoting**

- [ ] Same user: Other activity?
- [ ] Same system: Other access?
- [ ] Same IP: Other connections?
- [ ] Same file/hash: Other matches?
- [ ] Time window: Other related events?

### **Documentation**

- [ ] Query used: Documented
- [ ] Results: Screenshot or export
- [ ] Timeline: Screenshot
- [ ] Pivots: All documented
- [ ] Evidence: Ready to share

### **Decision**

- [ ] All evidence reviewed?
- [ ] Correlation complete?
- [ ] Confident verdict?
- [ ] Ready to escalate?

---

## Mini Quiz: SIEM Investigation

### **Question 1: SIEM এর primary benefit কোনটি?**

A) Encrypt all traffic  
B) Centralize logs for fast search  
C) Prevent all attacks  
D) Make backdoors

**Answer:** B) Centralize logs for fast search - SIEM aggregates for correlation

---

### **Question 2: Basic SIEM query field operator কোনটি?**

A) ||  
B) >>  
C) =  
D) &&

**Answer:** C) = - Most SIEM use field=value syntax

---

### **Question 3: "Pivoting" মানে কি?**

A) Rotating dashboard  
B) Finding related data from initial finding  
C) Changing search time  
D) Closing investigation

**Answer:** B) Finding related data from initial finding - Pivot to expand investigation

---

### **Question 4: SIEM এ encrypted traffic এ কি দেখা যায়?**

A) Content/payload  
B) Source/dest IP, volume, timing  
C) Commands/URLs  
D) All details

**Answer:** B) Source/dest IP, volume, timing - HTTPS payload encrypted

---

### **Question 5: যখন SIEM কোন result দেয় না?**

A) Always means clean  
B) Check: Time range, field names, logging active  
C) Restart SIEM  
D) Assume no activity

**Answer:** B) Check: Time range, field names, logging active - No results ≠ No activity

---

## সহজ ভাষায় সারসংক্ষেপ

**SIEM = Centralized log search platform**

**Core Skills:**
- Basic query: field="value"
- Time range: earliest=-24h
- Combine conditions: AND, OR, NOT
- Wildcards: john*, *admin

**Investigation Steps:**
1. Search initial events
2. Identify user/system
3. Build timeline
4. Pivot for correlation
5. Document evidence
6. Make verdict

**Pivoting:**
Same user → other activity?
Same system → other access?
Same IP → other connections?
Same file → other matches?

**Timeline:**
Order events chronologically
Find sequence/gaps
Build narrative
Correlation = bigger picture

**SIEM Limitations:**
- Encrypted traffic: Only headers
- No logging devices: Blind spots
- Timing: May lag hours
- Gaps: Don't assume

**Queries Used:**
- User activity: username="john"
- Brute force: EventCode=4625
- File activity: file_name="..."
- Network: dest_port=3389
- Access patterns: hostname="db"

**Remember:**
- Right time range (don't miss data)
- Right field names (correct syntax)
- Pivot enough (wider picture)
- Check data exists (not gaps)
- Document everything

---

## Resources for Learning

**SIEM vendor documentation:**
- Splunk SPL (Search Processing Language)
- ELK Lucene query syntax
- QRadar AQL
- Your specific SIEM vendor docs

**Your company:**
- SIEM admin guides
- Query examples/templates
- Field dictionary
- Training materials

---

**Module 16 Complete! ✅**

এখন আপনি জানেন:
- ✅ SIEM কীভাবে কাজ করে investigation এ
- ✅ Basic search এবং query syntax
- ✅ Time range filtering
- ✅ Combining conditions (AND, OR, NOT)
- ✅ Common investigation queries
- ✅ Timeline construction in SIEM
- ✅ Pivoting techniques
- ✅ Dashboards এবং saved searches
- ✅ Complete investigation workflow
- ✅ SIEM limitations এবং gaps
- ✅ Common SIEM mistakes
- ✅ Investigation checklist

Progress: **16 of 28 modules complete (57%)**

