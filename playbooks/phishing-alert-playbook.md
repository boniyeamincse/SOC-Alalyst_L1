# Playbook: Phishing Email Response

**PB-0001 | Phishing Alert Investigation**

## Overview

Step-by-step procedures for investigating phishing email alerts.

---

## Steps

### 1. Verify Email Reception (1 min)
- Search email logs for sender/recipient/date
- Confirm user received email
- If not found: Close as FP

### 2. Extract Email Details (1 min)
- Sender address
- Subject line
- Timestamp
- Recipient count
- Attachment (Y/N)
- Links present

### 3. Check Sender Legitimacy (1 min)
- WHOIS domain lookup
- SPF/DKIM/DMARC check
- TI reputation lookup
- Verdict: Authenticated or spoofed?

### 4. Scan Attachment (1 min)
- If no attachment: Skip
- File type, name, size
- Calculate/lookup hash
- VirusTotal scan
- Result: Malware or clean?

### 5. Check URLs (1 min)
- Extract all URLs
- For each: TI reputation lookup
- Check destination legitimacy
- Result: Phishing URLs or safe?

### 6. Check User Actions (1 min)
- Did user click link? (Y/N)
- Did user download? (Y/N)
- Did user enter credentials? (Y/N)
- Document all actions

### 7. Decision (1 min)
- Legitimate: CLOSE (FP)
- Phishing, no action: CLOSE
- Phishing, clicked: ESCALATE
- Phishing, credentials: ESCALATE
- Uncertain: ESCALATE

---

## Time Target: 8-10 minutes

## Version: 1.0