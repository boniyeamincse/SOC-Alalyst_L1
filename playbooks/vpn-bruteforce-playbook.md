# Playbook: VPN Brute Force Response

**PB-0003 | VPN Brute Force Investigation**

## Overview

Step-by-step procedures for investigating VPN brute force alerts.

---

## Steps

### 1. Verify Attack Pattern (1 min)
- Failed login count
- Time window
- Source IP(s)
- Target account
- Attack distributed or single IP?

### 2. Identify Source (1 min)
- Source IP address
- Reputation lookup (TI)
- Geographic location
- ASN/datacenter
- Known attacker infrastructure?

### 3. Identify Target (1 min)
- Account name
- Account type: User or service account?
- Privilege level: Admin or regular?
- Password age
- Account history

### 4. Check for Success (1 min)
- Successful login after failures? (CRITICAL)
- If YES:
  - When did success occur?
  - What did attacker do after?
  - Escalate immediately
- If NO:
  - Attack contained
  - Continue investigation

### 5. Check Account Status (1 min)
- Account locked out?
- Account disabled?
- Recent activity logged?
- Unusual access patterns?

### 6. Assess Business Context (1 min)
- Approved remote access?
- User on travel?
- Script/automation activity?
- Legitimate VPN usage expected?

### 7. Decision (1 min)
- Success + suspicious activity: ESCALATE IMMEDIATELY
- Failures only: MONITOR
- Service account + known pattern: Close (FP)
- Uncertain: Escalate

---

## Time Target: 10-12 minutes

## Version: 1.0
