# Playbook: Unusual Login Response

**PB-0004 | Unusual Login Investigation**

## Overview

Step-by-step procedures for investigating unusual login alerts.

---

## Steps

### 1. Verify Login Details (1 min)
- User account name
- Timestamp of login
- Source IP/location
- Target system/service
- Login method (password/MFA/etc)

### 2. Verify User Legitimacy (1 min)
- User account active?
- User employed/contractor status
- Employment end date (if contractor)
- Normal user or service account?

### 3. Check Geographic Anomaly (1 min)
- Previous login location
- Current login location
- Distance between locations
- Time between logins
- Physically possible?

### 4. Business Context (1 min)
- User approved for travel?
- Calendar shows travel?
- VPN usage? (obscures location)
- On company trip?
- Working from different location?

### 5. Compare to Baseline (1 min)
- Expected login time?
- Expected location?
- Expected device/method?
- Any deviations from pattern?

### 6. Check Account Security (1 min)
- Password recently changed?
- MFA enabled/working?
- Recent suspicious activity?
- Account compromise indicators?

### 7. Decision (1 min)
- Travel approved + context matches: CLOSE
- Impossible travel: ESCALATE
- No travel approved: ESCALATE
- Baseline anomaly: ESCALATE
- Uncertain: Contact manager or escalate

---

## Time Target: 8-10 minutes

## Version: 1.0
