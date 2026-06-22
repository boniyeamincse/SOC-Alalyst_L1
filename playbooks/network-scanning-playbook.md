# Playbook: Network Scanning Response

**PB-0006 | Network Scanning Investigation**

## Overview

Step-by-step procedures for investigating network reconnaissance/port scanning alerts.

---

## Steps

### 1. Verify Scanning Pattern (1 min)
- Source IP
- Target IPs/systems
- Ports being scanned
- Scanning method/protocol
- Time window
- Volume

### 2. Identify Source (1 min)
- Source IP address
- Reputation (TI lookup)
- Internal or external?
- Datacenter/VPN/Residential?
- Known company system?

### 3. Identify Targets (1 min)
- Which systems being scanned?
- Criticality of targets
- Data on targets
- Network segmentation
- Firewall protection

### 4. Check Business Purpose (1 min)
- Authorized network scan?
- Vulnerability assessment scheduled?
- Ticketed IT work?
- Maintenance window?
- Expected activity?

### 5. Assess Reconnaissance Pattern (1 min)
- Random scanning or targeted?
- Specific ports or broad?
- Research phase or attack prep?
- Known attack pattern?
- Lateral movement phase?

### 6. Check System Status (1 min)
- Alert triggered by: IDS/Firewall
- Scans successful or blocked?
- Were vulnerabilities found?
- Is system exploitable?
- Was access gained?

### 7. Decision (1 min)
- Authorized vulnerability scan: CLOSE
- External, blocked, no follow-up: MONITOR
- Targeted internal scanning: ESCALATE
- After compromise detected: ESCALATE
- Unusual pattern: ESCALATE
- Uncertain: Escalate to L2

---

## Time Target: 8-10 minutes

## Version: 1.0
