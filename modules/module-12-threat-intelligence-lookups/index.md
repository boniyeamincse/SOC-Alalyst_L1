# Module 12: Threat Intelligence and Lookups

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- Threat Intelligence (TI) কি এবং কিভাবে use করতে হয়
- TI platforms: VirusTotal, AbuseIPDB, Shodan, Censys, Recorded Future
- IP reputation lookup এবং কি মানে
- Domain/URL reputation checking
- File hash lookup (MD5, SHA256)
- Email domain validation
- GeoIP এবং location analysis
- ASN (Autonomous System Number) information
- VPN/Proxy/Tor detection
- TI false positives এবং limitations
- Real SOC TI scenarios
- Common TI mistakes

---

## শুরুর আগে: একটি গল্প

করিম একটি suspicious alert investigate করছে। Alert says: "Unusual connection to 192.0.2.100".

Without TI (Wrong):
```
09:00 - Alert দেখলো
09:05 - IP check করলো (it's just an IP)
09:10 - "Not sure if malicious"
09:15 - Escalate to L2 (uncertain)
Result: False escalation
```

With TI (Right):
```
09:00 - Alert দেখলো
09:02 - IP lookup: VirusTotal
       └─ 192.0.2.100
       └─ Known C2 server
       └─ 47 vendors flagged
       └─ Malware family: Emotet
       
09:05 - Additional check: AbuseIPDB
       └─ Same IP
       └─ High reputation score
       └─ Hundreds of reports
       
09:08 - Verdict: CONFIRMED threat
09:10 - Escalate with TI data
Result: Confident escalation with evidence
```

**TI = Instant threat validation.**

---

## Threat Intelligence কি?

### Definition:

**Threat Intelligence = Data about known threats, malicious indicators, attacker infrastructure.**

```
TI provides:
├─ Known malicious IPs
├─ Known malicious domains
├─ Malware file hashes
├─ Phishing URLs
├─ Botnet command & control (C2) servers
├─ Compromised credentials
├─ Attacker techniques
├─ Vulnerability information
├─ Threat actor profiles
└─ Industry-specific threat data
```

### Why TI Matters:

```
During investigation:

Find suspicious indicator:
├─ IP address: 192.0.2.50
├─ Question: Is this malicious?
│
├─ Without TI:
│  └─ Guess based on context
│  └─ Might be wrong
│  └─ False positive risk
│
└─ With TI:
   └─ Query TI database
   └─ Get: 50+ vendors flagged
   └─ Get: Known malware family
   └─ Get: Historical reports
   └─ Know: Definitely malicious
```

---

## TI Platforms

### **1. VirusTotal**

```
Most used TI platform for malware/file analysis.

What it does:
├─ Analyzes files (executables, documents, zips)
├─ Analyzes URLs
├─ Analyzes IPs
├─ Analyzes domains
├─ Runs files in 70+ sandbox engines
└─ Aggregates data from 90+ antivirus vendors

Information provided:

FILE HASH LOOKUP:
├─ Hash: MD5, SHA256, SHA1
├─ Verdict: Malware/clean/suspicious
├─ Vendors detecting: Count (e.g., 45/71)
├─ Malware family: Name
├─ First seen: When detected
├─ Last seen: Recent activity?
├─ File type: What is it?
└─ Size: File size

IP LOOKUP:
├─ Country: Geographic location
├─ ASN: Internet provider
├─ Domains: Hosted on IP
├─ URLs: Hosted on IP
├─ Resolutions: Historic IPs for domain
└─ Community score: Reputation

DOMAIN/URL LOOKUP:
├─ Registrar: Who registered?
├─ Registration date: When?
├─ Last updated: Recent change?
├─ Nameservers: DNS servers
├─ Hosting provider: Where hosted?
├─ Phishing/malware: Flagged?
├─ Community reports: User reports
└─ HTTP response: Live check

How to use:
├─ Search: Hash, IP, domain, URL
├─ See: Detection status
├─ See: Vendor reports
├─ See: Behavior analysis
└─ Make decision: Malicious or not?

Pricing:
├─ Free tier: Limited queries
├─ Paid API: Unlimited
└─ Cost: ~$500/month for API

Use when:
├─ File hash found in alert
├─ Unknown URL/domain
├─ Unknown IP
├─ Need vendor consensus
└─ Need malware family
```

### **2. AbuseIPDB**

```
Specialized for IP reputation.

What it does:
├─ Tracks abuse reports for IPs
├─ Aggregates malicious activity
├─ Tracks attack vectors
├─ Geographic blocking lists
└─ Real-time updates

Information provided:

├─ Abuse score: 0-100 (higher = more malicious)
├─ Number of reports: How many users reported?
├─ Attack types: What did it do?
│  ├─ Brute force
│  ├─ Phishing
│  ├─ Spam
│  ├─ DDoS
│  ├─ Malware
│  └─ Other
├─ Reporting users: Community input
├─ ISP/Hosting: Who owns IP?
├─ Usage type: Data center, residential, VPN?
└─ Last report date: Recent activity?

How to use:
├─ Search: IP address
├─ See: Abuse score
├─ See: Attack types
├─ See: Recent reports
└─ Make decision: Trust this IP?

Pricing:
├─ Free tier: 1000 queries/day
├─ Paid: $30-100/month
└─ Cost effective

Use when:
├─ Need IP reputation
├─ Checking source IP
├─ Checking C2 server
├─ Looking for spam/phishing
└─ Need historical data
```

### **3. Shodan**

```
Search engine for internet-connected devices.

What it does:
├─ Indexes internet-connected devices
├─ Maps services running on IPs
├─ Finds exposed services
├─ Historical data available
└─ Deep protocol analysis

Information provided:

├─ Services running: Ports/protocols
├─ Banners: Service identification
├─ Operating systems: What OS?
├─ Vulnerabilities: Known issues?
├─ Hostnames: Domain names
├─ Geographic location: Where?
├─ ISP information: Who owns?
└─ Screenshots: Visual service info

How to use:
├─ Search: IP address
├─ See: Services exposed
├─ See: Open ports
├─ See: OS version
├─ Make decision: Is this exposed device normal?

Pricing:
├─ Free tier: Limited
├─ Paid: $200-2000+/month
└─ Expensive

Use when:
├─ Want to know: What services on IP?
├─ Want to know: OS version
├─ Want to know: Exposed ports
├─ Want to know: What vulnerabilities possible?
├─ Infrastructure reconnaissance
└─ Need historical snapshots
```

### **4. AlienVault OTX (Open Threat Exchange)**

```
Community-driven threat intelligence.

What it does:
├─ Aggregates threat data from users
├─ Provides indicators of compromise
├─ Maps attack campaigns
├─ Tracks threat actor profiles
└─ Free community data

Information provided:

├─ Pulses: Threat campaigns
├─ Indicators: IPs, domains, hashes
├─ Malware samples: Details
├─ Attack patterns: ATT&CK framework
├─ Community subscriptions: Expert intel
└─ Automated indicators: Feeds

How to use:
├─ Search: IP, domain, hash
├─ See: Community reports
├─ See: Related indicators
├─ See: Pulses (campaigns)
└─ Make decision: Part of known campaign?

Pricing:
├─ Free: Community data
├─ Paid: Advanced feeds
└─ Cost: ~$300+/month

Use when:
├─ Community input valuable
├─ Looking for campaign indicators
├─ Want free TI data
├─ Need indicator feeds
└─ Correlation analysis
```

### **5. Recorded Future**

```
Enterprise threat intelligence platform.

What it does:
├─ Advanced threat research
├─ Dark web monitoring
├─ Vulnerability intelligence
├─ Ransomware tracking
├─ Managed hunting
└─ Industry-specific intelligence

Information provided:

├─ Risk scores: For indicators
├─ Threat reports: Detailed analysis
├─ Dark web data: Underground sources
├─ CVE intelligence: Vulnerabilities
├─ Malware tracking: Active malware
├─ Phishing detection: URL reputation
└─ Custom reporting: Tailored intel

Pricing:
├─ Enterprise only
├─ $10000+/year
└─ Very expensive

Use when:
├─ Have budget for enterprise TI
├─ Need comprehensive intelligence
├─ Dark web visibility needed
├─ Industry-specific threats
├─ Executive reporting
└─ Strategic threat monitoring
```

---

## Common Lookups & What They Mean

### **IP Reputation Lookup**

```
Query: 192.0.2.100

Possible results:

RESULT 1: "Known malicious IP"
├─ Verdict: MALICIOUS
├─ Implies: C2 server or attacker infrastructure
├─ Action: High alert, escalate
├─ Example: Known botnet C2

RESULT 2: "High abuse score"
├─ Verdict: SUSPICIOUS
├─ Implies: History of malicious activity
├─ Action: Investigate context
├─ Example: Previous brute force attacks

RESULT 3: "VPN/Proxy detected"
├─ Verdict: CONTEXT-DEPENDENT
├─ Implies: Traffic anonymized
├─ Action: Check if approved VPN
├─ Example: Employee on VPN (ok) vs attacker hiding

RESULT 4: "Data center IP"
├─ Verdict: CONTEXT-DEPENDENT
├─ Implies: Cloud provider or hosting
├─ Action: Check if legitimate cloud service
├─ Example: AWS IP ok, but malware hosted there?

RESULT 5: "Residential IP"
├─ Verdict: LOW RISK typically
├─ Implies: Home internet
├─ Action: Normal traffic expected
├─ Example: Employee from home

RESULT 6: "Clean / No reports"
├─ Verdict: NOT KNOWN TO BE MALICIOUS
├─ Implies: No history of abuse
├─ Action: Likely benign
├─ Caveat: Doesn't mean 100% safe (new attacker)
```

### **Domain/URL Reputation**

```
Query: suspicious-domain.net

Possible results:

RESULT 1: "Known phishing domain"
├─ Verdict: MALICIOUS
├─ Implies: Phishing site
├─ Action: Block, escalate
├─ Users compromised if visited

RESULT 2: "Malware distribution site"
├─ Verdict: MALICIOUS
├─ Implies: Serves malware
├─ Action: Block, escalate
├─ Users infected if downloaded

RESULT 3: "Newly registered"
├─ Verdict: SUSPICIOUS
├─ Implies: Brand new domain
├─ Action: Investigate further
├─ Caveat: Can be legitimate or attacker-created

RESULT 4: "Legitimate domain but compromised"
├─ Verdict: COMPROMISED
├─ Implies: Hacked website
├─ Action: Notify owner, avoid
├─ Users clicking = malware risk

RESULT 5: "Low reputation score"
├─ Verdict: SUSPICIOUS
├─ Implies: Mixed community reports
├─ Action: Check why
├─ Example: Spam reports vs malware

RESULT 6: "Clean / No records"
├─ Verdict: NOT KNOWN TO BE MALICIOUS
├─ Implies: No history
├─ Action: Likely ok
├─ Caveat: Brand new (legitimate or attacker)
```

### **File Hash Lookup**

```
Query: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6 (SHA256)

Possible results:

RESULT 1: "Known malware"
├─ Verdict: MALICIOUS
├─ Implies: Exact hash matches known malware
├─ Action: Delete file, escalate
├─ Confidence: VERY HIGH (exact match)
├─ Example: Hash = 45/71 vendors detect

RESULT 2: "PUP (Potentially Unwanted Program)"
├─ Verdict: SUSPICIOUS
├─ Implies: Legitimate software but unwanted
├─ Action: Verify if intentionally installed
├─ Example: Adware, toolbar, scareware

RESULT 3: "Unknown file"
├─ Verdict: CANNOT DETERMINE
├─ Implies: Not seen before in databases
├─ Action: Cannot rely on reputation
├─ Caveat: New malware = unknown hash
├─ Option: Submit to sandbox for analysis

RESULT 4: "Legitimate software"
├─ Verdict: CLEAN
├─ Implies: Known legitimate file
├─ Action: Safe to proceed
├─ Example: Windows DLL, Adobe reader

RESULT 5: "Hash not found"
├─ Verdict: UNKNOWN
├─ Implies: Never submitted/analyzed
├─ Action: Unknown behavior
├─ Risky: Could be custom malware
├─ Option: Submit for analysis (if safe)
```

---

## Special Lookups

### **GeoIP & Location**

```
Query: What location is this IP?

Purpose:
├─ Understand user/attacker location
├─ Detect impossible travel
├─ Assess geographic anomalies

Information:
├─ Country
├─ City
├─ Latitude/Longitude
├─ ISP/Organization
├─ ASN (network owner)
├─ Connection type (residential, data center)
└─ Timezone

Use cases:

User login from Singapore but was:
├─ In India 30 minutes ago?
├─ = Impossible travel = SUSPICIOUS
└─ Action: Investigate account

Employee on approved travel:
├─ Accessing from expected country?
├─ = Expected location = OK
└─ Action: Normal activity
```

### **ASN (Autonomous System Number)**

```
What is ASN?
└─ Unique number for network ownership

Query: What ASN owns this IP?

Information:
├─ Organization: Who owns?
├─ Network type: ISP, datacenter, etc.
├─ IP range: Full network range
├─ Reputation: Known for hosting malware?
└─ Other IPs in range: Related services

Use cases:

IP detected: 192.0.2.50
└─ Check ASN:
   ├─ ASN: AS1234
   ├─ Owner: "Evil Hosting Company"
   ├─ Reputation: Known for malware hosting
   └─ Decision: BLOCK this ASN
   
Alternative:
└─ ASN: AS5678
├─ Owner: "AWS Amazon"
├─ Reputation: Legitimate cloud
└─ Decision: OK, but check what service
```

### **VPN/Proxy/Tor Detection**

```
Query: Is this IP a VPN/Proxy/Tor exit node?

Importance:
└─ Indicates traffic anonymization
   ├─ Can be legitimate (privacy-conscious user)
   ├─ Or malicious (attacker hiding)
   └─ Context matters

Results:

Result 1: "VPN detected"
├─ Verdict: ANONYMIZED
├─ Check: Is this approved VPN?
│  ├─ If company VPN: OK
│  ├─ If consumer VPN: Why using?
│  └─ If suspicious: RED FLAG
└─ Action: Verify legitimacy

Result 2: "Tor exit node"
├─ Verdict: HIGHLY ANONYMIZED
├─ Implies: Deep anonymization
├─ Risk: Usually indicates malicious
├─ Action: Investigate
└─ Example: Attacker hiding, ransomware C2

Result 3: "Proxy detected"
├─ Verdict: TRAFFIC PROXIED
├─ Check: Why proxied?
│  ├─ Corporate proxy: OK
│  ├─ Anonymous proxy: Suspicious
│  └─ Bypass proxy: RED FLAG
└─ Action: Investigate

Result 4: "Residential proxy"
├─ Verdict: SUSPICIOUS
├─ Implies: Using residential IP as proxy
├─ Risk: Usually malicious
├─ Action: Escalate
└─ Example: Bot using residential IP to hide
```

---

## TI False Positives & Limitations

### False Positives:

```
SITUATION 1: Old reputation data
├─ Domain: Was malicious 2 years ago
├─ Now: Legitimate domain, cleaned up
├─ TI: Still shows malicious (stale data)
└─ Action: Verify with current info

SITUATION 2: Legitimate but flagged
├─ File: Legitimate tool flagged by 1 vendor
├─ But: 69 vendors say clean
├─ Decision: Check which vendor (sometimes wrong)
└─ Action: Use consensus, not single vendor

SITUATION 3: VPN/Proxy misidentification
├─ User: On legitimate VPN
├─ TI: Shows as malicious (VPN abuse history)
├─ Reality: Different user now on same VPN
└─ Action: Check context, not just VPN flag

SITUATION 4: Clean up & re-infection
├─ Website: Was malicious, cleaned
├─ Now: Re-infected with new malware
├─ TI: Mixed signals (old + new data)
└─ Action: Check latest reports
```

### Limitations:

```
LIMITATION 1: Zero-day threats
├─ New malware: No hash signatures yet
├─ New domain: Just created
├─ TI: Nothing in database
└─ Solution: Behavioral analysis, sandboxing

LIMITATION 2: Encrypted traffic
├─ HTTPS: Content encrypted
├─ TI: Can see IP/domain but not payload
├─ Action: Trust domain/IP reputation only

LIMITATION 3: Dynamic infrastructure
├─ Attacker: Moves C2 servers frequently
├─ TI: Data lags behind
└─ Solution: Monitor patterns, not just IPs

LIMITATION 4: False flags
├─ Vendor bugs: Sometimes trigger incorrectly
├─ Community reports: Sometimes wrong
├─ TI: May have incorrect data
└─ Solution: Cross-reference multiple sources

LIMITATION 5: Context matters
├─ IP malicious: But used by legitimate business
├─ Example: Hosting company IP with mixed reputation
└─ Solution: Don't rely on TI alone
```

---

## Real-World TI Scenarios

### **Scenario 1: Confirmed Malware via Hash**

```
ALERT: "Malware detected - invoice.exe"

Investigation:

Step 1: Extract hash
├─ File: invoice.exe
├─ SHA256: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6

Step 2: TI Lookup - VirusTotal
├─ Search: Hash
├─ Result: FOUND
├─ Vendors: 48/71 detect
├─ Family: Emotet (ransomware)
├─ First seen: 3 months ago
├─ Last seen: Today

Step 3: Additional TI - AbuseIPDB
├─ Search: Known C2 for Emotet
├─ Result: Found 5 C2 IPs
├─ Abuse score: 98/100
├─ Reports: 1000+ users

VERDICT: TRUE_POSITIVE - CONFIRMED MALWARE
ACTION: ESCALATE immediately
├─ Isolate device
├─ Preserve evidence
├─ Audit data access
└─ Incident response activated

Confidence: 99% (multiple TI sources)
```

### **Scenario 2: Suspicious URL - TI Unclear**

```
ALERT: "User clicked suspicious URL"

Investigation:

Step 1: Extract URL
├─ URL: http://totally-legitimate-bank.net/login
├─ Domain: totally-legitimate-bank.net

Step 2: TI Lookup - VirusTotal
├─ Search: Domain
├─ Result: Mixed signals
├─ Vendors: 3/71 flag as phishing
├─ Community: Some reports of phishing
├─ But: Some say legitimate
├─ Domain age: 2 days old (NEW!)

Step 3: Additional checks - Shodan
├─ IP: 192.0.2.200
├─ Hosting: Free hosting service
├─ OS: Windows Server
├─ Services: Only HTTP

Step 4: Context analysis
├─ Domain: "totally-legitimate-bank"
├─ But: Real bank is "legitimateb ank.net" (spelling off)
├─ Verdict: Phishing attempt (typosquatting)

VERDICT: SUSPICIOUS/TRUE_POSITIVE
ACTION: 
├─ Block URL
├─ Isolate user device
├─ Check if credentials entered
├─ Investigate user
└─ Escalate to incident response

Confidence: 85% (phishing indicators strong)
```

### **Scenario 3: VPN Not Malicious**

```
ALERT: "Login from VPN IP"

Investigation:

Step 1: Alert details
├─ User: alice@company.com
├─ IP: 203.0.113.50
├─ Alert: VPN IP = unusual

Step 2: TI Lookup - AbuseIPDB
├─ Search: 203.0.113.50
├─ Result: VPN provider IP
├─ Reports: Abuse score 45/100 (medium)
└─ Reason: VPN abuse complaints

Step 3: Additional context
├─ Calendar: Alice approved for travel
├─ Travel: Singapore Jun 20-25
├─ Current time: Jun 22 (during travel)
├─ IP location: Singapore
├─ Expected: Alice in Singapore

Step 4: Verification
├─ VPN provider: Known commercial VPN
├─ Legitimate: Many users, legitimate business
├─ User behavior: Normal for alice during travel
└─ No compromise signals

VERDICT: BENIGN
ACTION: Close alert
REASON: Expected VPN usage during approved travel
Confidence: 95%
```

---

## TI Investigation Checklist

### **Quick TI Check (1-2 minutes)**

- [ ] Identify indicators: IP? Domain? Hash? Email?
- [ ] Choose TI platform (VirusTotal primary)
- [ ] Search indicator
- [ ] Get verdict: Malicious/suspicious/clean?
- [ ] Make decision: Escalate or continue investigating

### **Deep TI Analysis (3-5 minutes)**

- [ ] Multiple TI platforms: Cross-reference
- [ ] Check: Vendor consensus (if file hash)
- [ ] Check: Abuse reports (if IP)
- [ ] Check: Domain registration age
- [ ] Check: ASN and hosting provider
- [ ] Check: VPN/Proxy/Tor status
- [ ] Check: Community reports
- [ ] Check: Timeline (when seen first/last)
- [ ] Note: Any TI contradictions?

### **Decision Making**

- [ ] TI says malicious: Evidence strong?
- [ ] TI says clean: Any context contradicting?
- [ ] TI says unknown: How to proceed?
- [ ] Any false positive signals?
- [ ] Should escalate or investigate more?

---

## Common TI Mistakes

### ❌ **Mistake 1: Trusting single TI source**

**সমস্যা:**
```
One vendor says malware
Assume: Definitely malware
Reality: Could be false positive
```

**সমাধান:**
```
Cross-reference multiple TI sources
VirusTotal + AbuseIPDB + community checks
Consensus > single source
```

---

### ❌ **Mistake 2: Not checking TI data age**

**সমস্যা:**
```
TI says malicious from 1 year ago
Action: Block domain
Reality: Domain cleaned, now legitimate
```

**সমাধান:**
```
Check: Last seen date
Check: Recent reports
Older data = verify with current info
```

---

### ❌ **Mistake 3: Over-relying on TI**

**সমস्या:**
```
TI says clean
Assume: Definitely safe
Reality: Could be new attacker, zero-day
```

**সمाधान:**
```
TI is one input, not conclusive
Consider: Behavior, context, other indicators
Especially for unknown/new indicators
```

---

### ❌ **Mistake 4: Confusing VPN with malicious**

**সમস्या:**
```
TI shows VPN detected
Assume: Attacker using VPN
Reality: Legitimate employee on approved VPN
```

**সমाধান:**
```
VPN ≠ automatically malicious
Check: Approved VPN?
Check: Expected user behavior?
Check: Travel/work-from-home?
```

---

### ❌ **Mistake 5: Not noting TI results**

**समस्या:**
```
Did TI lookup verbally
Didn't document
Later: Can't remember findings
```

**समाधान:**
```
Always document TI findings
Record: What you searched
Record: What you found
Record: Confidence level
```

---

## Mini Quiz: Threat Intelligence

### **Question 1: VirusTotal hash lookup এ 45/71 vendor detection মানে?**

A) 45% sure it's malware  
B) 45 out of 71 vendors detect it as malware  
C) Only 45 true positives  
D) Not malware (majority clean)

**Answer:** B) 45 out of 71 vendors detect it as malware - Strong indication of malware

---

### **Question 2: Unknown file hash TI lookup এ কি করবেন?**

A) Assume clean (if TI doesn't have it)  
B) Cannot rely on TI, need behavioral analysis  
C) Definitely malware (new attacker)  
D) Close alert

**Answer:** B) Cannot rely on TI, need behavioral analysis - Unknown ≠ safe

---

### **Question 3: VPN IP detected এ সবসময় suspicious?**

A) হ্যা, VPN = attacker  
B) না, depends on context  
C) Only if external VPN  
D) Yes, block all VPN

**Answer:** B) না, depends on context - Check if approved, expected usage, employee travel

---

### **Question 4: Domain newly registered কে তাৎক্ষণিক block করবেন?**

A) হ্যা, new = suspicious  
B) না, could be legitimate  
C) Yes, always new = attacker  
D) Only if flagged by vendors

**Answer:** B) না, could be legitimate - New domain suspicious but not conclusive, investigate further

---

### **Question 5: TI platform কোনটি IP reputation এ সবচেয়ে specialised?**

A) VirusTotal  
B) Shodan  
C) AbuseIPDB  
D) Recorded Future

**Answer:** C) AbuseIPDB - IP abuse tracking specialised

---

## সহজ ভাষায় সারসংক্ষেপ

**Threat Intelligence = Known threat data**

**5 Major TI Platforms:**
- **VirusTotal:** File/IP/URL/domain analysis (90+ vendors)
- **AbuseIPDB:** IP reputation & abuse reports
- **Shodan:** Internet device discovery
- **AlienVault OTX:** Community threat data
- **Recorded Future:** Enterprise threat intelligence

**Common Lookups:**
- **IP reputation:** Malicious? History? Location?
- **Domain/URL:** Phishing? Malware? Clean?
- **File hash:** Malware family? Verdict? Vendors?
- **Email domain:** Legitimate? Spoofed?
- **GeoIP:** Location validation, impossible travel
- **ASN:** Network owner, reputation
- **VPN/Proxy/Tor:** Anonymization detection

**Interpretation:**
- **Malicious TI:** High confidence threat
- **Suspicious TI:** Medium risk, investigate more
- **Clean TI:** Likely safe, but not 100%
- **Unknown TI:** Cannot rely on reputation, behavioral analysis needed
- **Mixed TI:** Cross-reference, check recency

**Limitations:**
- Zero-day threats: No TI data
- False positives: Outdated or wrong data
- Context matters: TI ≠ verdict alone
- VPN ≠ automatically malicious
- New domains: Could be legitimate

**Remember:**
- Cross-reference multiple sources
- Check data age (recent vs stale)
- Context is crucial (VPN, travel, etc.)
- Document findings always
- TI one input, not conclusive
- Unknown ≠ Safe

---

## Resources for Learning

**TI platform access:**
- VirusTotal free account setup
- AbuseIPDB free access
- Shodan basics
- OTX community

**Integration:**
- SIEM TI integration
- EDR TI feeds
- Alert enrichment
- Automation with TI APIs

---

**Module 12 Complete! ✅**

এখন আপনি জানেন:
- ✅ Threat Intelligence কি এবং গুরুত্ব
- ✅ 5টি major TI platforms
- ✅ IP reputation lookups
- ✅ Domain/URL reputation checking
- ✅ File hash malware detection
- ✅ GeoIP এবং location analysis
- ✅ ASN information
- ✅ VPN/Proxy/Tor detection
- ✅ TI false positives
- ✅ TI limitations (zero-day, encrypted, etc.)
- ✅ Real-world TI scenarios
- ✅ Common TI mistakes

Progress: **12 of 28 modules complete (43%)**

---

<!-- nav-footer -->
## 🧭 Navigation

| | |
|---|---|
| **Previous** | [⬅️ Module 11: Asset Inventory](../module-11-asset-inventory/index.md) |
| **Next** | [Module 13: Network Diagrams ➡️](../module-13-network-diagrams/index.md) |
| **🏠 Course Home** | [STUDY_NOTES.md](../../STUDY_NOTES.md) |
