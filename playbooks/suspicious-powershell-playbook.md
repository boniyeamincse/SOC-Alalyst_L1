# Playbook: Suspicious PowerShell Response

**PB-0005 | Suspicious PowerShell Investigation**

## Overview

Step-by-step procedures for investigating suspicious PowerShell execution.

---

## Steps

### 1. Get Command Details (1 min)
- Full command executed
- Encoded or plain text?
- What does command do?
- Parent process
- User context

### 2. Decode if Necessary (1 min)
- If Base64 encoded: Decode
- If obfuscated: De-obfuscate
- Understand actual command purpose

### 3. Identify Source (1 min)
- User: Who executed?
- Device: Which system?
- Admin rights: Yes or no?
- Expected to run PS: Yes or no?

### 4. Check Business Context (1 min)
- IT ticketed script?
- Admin task scheduled?
- Legitimate tool (Management)?
- Expected for this user?

### 5. Assess Risk (1 min)
- Encoding purpose (escaping vs hiding)?
- Network connections attempted?
- File/registry modifications?
- Credential access attempted?

### 6. Verify Legitimacy (1 min)
- Contact user: Did you run this?
- Check IT: Is this known script?
- Search tickets: Any approval?
- Check history: Ever run before?

### 7. Decision (1 min)
- Legitimate admin task: CLOSE
- Known management tool: CLOSE
- Encoding unexplained: ESCALATE
- Suspicious behavior: ESCALATE
- Malicious indicators: ESCALATE IMMEDIATELY
- Uncertain: Escalate to L2

---

## Time Target: 10-12 minutes

## Version: 1.0
