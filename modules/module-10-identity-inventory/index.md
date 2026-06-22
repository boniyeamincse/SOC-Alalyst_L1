# Module 10: Identity Inventory for SOC

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- Identity inventory কি এবং কেন critical
- Identity sources: AD, Entra ID, Okta, Google Workspace
- HR systems: BambooHR, SAP, HiBob integration
- User attributes এবং তাদের মানে
- Service accounts vs Regular users
- User lifecycle: onboard, offboard, transfers
- User access rights এবং permissions
- Identity verification during investigations
- Red flags for compromised accounts
- Real SOC identity scenarios
- Common identity-related mistakes

---

## শুরুর আগে: একটি গল্প

সালিম একজন SOC L1 analyst। Alert আসে: "admin account accessed from unusual IP".

Approach 1 (Wrong):
```
09:00 - Alert দেখলো
09:05 - Investigate করলো log
09:10 - "Probably attacker" conclude করলো
09:15 - Escalate করলো IR কে (false alarm)
```

Approach 2 (Right - experienced analyst):
```
09:00 - Alert দেখলো
09:02 - "admin account" verify করলো
       └─ SIEM search: "admin" matched 200+ accounts
       └─ Which admin?
       
09:04 - Identity lookup:
       └─ Check AD
       └─ Found: admin_backup (service account)
       └─ vs admin_user_1 (human account)
       └─ vs admin_contractor (temp access)
       
09:06 - Context check:
       └─ admin_backup: Nightly backup process (expected)
       └─ admin_user_1: On vacation (vacation marked in AD)
       └─ admin_contractor: Contract ended yesterday (disabled)
       
09:08 - Verdict:
       └─ Service account, expected activity
       └─ False positive
       └─ Close alert (no escalation needed)

Time: 8 minutes, HIGH confidence, NO false escalation
```

**Difference?** Strong identity inventory knowledge.

---

## Identity Inventory কি?

### Definition:

**Identity Inventory = Complete database of who is who in organization.**

```
Basic info:
├─ User ID / Username
├─ Full name
├─ Email address
├─ Department
├─ Job title
├─ Manager
└─ Employee ID

System info:
├─ AD account status (active/disabled/locked)
├─ Last login
├─ Account creation date
├─ Recent password change
├─ Group memberships
└─ Account type (human/service/contractor)

Access info:
├─ Systems accessed
├─ Permissions level
├─ Application licenses
├─ MFA status
└─ Last access per system

Employment info:
├─ Start date
├─ End date (if offboarded)
├─ Employment type (employee/contractor)
├─ Location
├─ Cost center
└─ Approval chain (manager, department)
```

### Why Identity Inventory Matters:

```
Investigation scenario:

Alert: "Unusual database access"
Raw data: "User: db_admin accessed database"

WITHOUT identity inventory:
├─ "db_admin" → Is it legitimate user?
├─ No context
├─ Escalate to L2 (uncertain)

WITH identity inventory:
├─ "db_admin" → Check AD
├─ Found: db_admin (active, last login today)
├─ Department: Database team
├─ Manager: John (approves DB access)
├─ Group: DBA_ROLE (has DB access)
├─ Status: Expected access
├─ Close immediately (confident)
```

---

## Identity Sources

### **1. Active Directory (AD) - Windows Core**

```
The most important identity source for most organizations.

Contains:
├─ User accounts (human, service, shared)
├─ Group memberships
├─ Computer accounts
├─ Organizational units (departments)
└─ Security groups

Information available:
├─ Username
├─ Display name
├─ Email
├─ Department
├─ Manager
├─ Phone number
├─ Office location
├─ Job title
├─ Account status (active/disabled/locked)
├─ Last logon
├─ Password age
├─ Group memberships
└─ Custom attributes

How L1 uses AD:

QUICK LOOKUP:
└─ Search: username
   └─ See: User details
   └─ See: Groups (what access?)
   └─ See: Status (active/disabled?)
   └─ See: Department (internal/external?)

IMPORTANT FIELDS:

admin@company.com vs admin_backup:
├─ admin@company.com
│  └─ Display name: "Admin User 1"
│  └─ Department: "IT Operations"
│  └─ Type: Human user
│  └─ Groups: Domain Admins, Security Team
│
└─ admin_backup
   └─ Display name: "Backup Automation"
   └─ Department: "Infrastructure"
   └─ Type: Service account
   └─ Groups: Domain Admins (for backup rights)
   └─ Last logon: Always recent (automation)

The difference matters!
```

### **2. Entra ID (Azure AD) - Cloud Identity**

```
Microsoft cloud identity service.
Modern organizations use this + on-prem AD.

Contains:
├─ Cloud user accounts
├─ Cloud groups
├─ External user access
├─ Device registration
├─ Conditional access policies
└─ MFA settings

Entra-specific info:
├─ Cloud-only users
├─ Guest users (contractors, partners)
├─ MFA enrollment status
├─ Conditional access policies (location, device)
├─ Last sign-in (cloud services)
└─ Device compliance status

Why matters for SOC:
├─ Cloud apps only in Entra (not AD)
├─ Remote workers: Entra is source of truth
├─ Guest users: Special attention
├─ MFA: Security posture check
└─ External partners: Track access
```

### **3. Okta - Identity & Access Management**

```
Enterprise SSO (Single Sign-On) platform.

Contains:
├─ User identity
├─ Application assignments
├─ Group memberships
├─ MFA enrollment
├─ Session information
└─ API token status

Okta-specific info:
├─ Which apps user has access to
├─ Active sessions (who logged in where)
├─ Last activity per app
├─ API tokens (for automation)
├─ Password policy compliance
└─ MFA methods enrolled

Why matters for SOC:
├─ Tracks who has app access
├─ Session data for timeline
├─ API tokens often leaked (monitor)
├─ Can revoke access/sessions
└─ Central auth log source
```

### **4. Google Workspace - Cloud Office Suite**

```
Google's email, docs, drive platform.

Contains:
├─ User accounts
├─ Organization hierarchy
├─ Group memberships
├─ Device enrollment
├─ Access control settings
└─ Shared drive permissions

Google Workspace info:
├─ Email address
├─ Organization unit
├─ Manager
├─ Department
├─ Shared drive access
├─ Document sharing
├─ Mobile device enrollment
└─ Last activity

Why matters for SOC:
├─ Email access patterns
├─ Document sharing anomalies
├─ Drive data access
├─ External sharing risks
└─ Mobile device management
```

### **5. HR Systems - BambooHR, SAP, HiBob**

```
Where employment data lives.

BambooHR:
├─ Employee directory
├─ Org chart
├─ Onboard/offboard tracking
├─ Time off requests
├─ Performance reviews
└─ Personal information

SAP:
├─ Employee master data
├─ Cost center assignments
├─ Payroll information
├─ Leave approvals
├─ Approval chain
└─ Headcount data

HiBob:
├─ Employee profiles
├─ Holiday calendar
├─ Onboarding workflows
├─ Offboarding checklists
├─ Team structure
└─ Direct reports

Why HR systems matter:
├─ Verify employment status
├─ Check travel/leave (for location anomalies)
├─ Identify contractors (temp access)
├─ Track onboards/offboards (new/old accounts)
├─ Confirm manager relationship
├─ Understand org structure
└─ Verify employment dates
```

---

## User Attributes: What They Mean

### User Classification:

```
HUMAN USERS:
├─ Regular employees
│  └─ Standard access
│  └─ Business applications
│  └─ Email, files, normal work
│
├─ Administrators
│  └─ Elevated access
│  └─ System configuration rights
│  └─ Usually fewer in count
│
├─ Contractors/Temporary
│  └─ Limited-time access
│  └─ Often external accounts
│  └─ Should be offboarded on end date
│
└─ Contractors/Partners
   └─ External access
   └─ Guest accounts
   └─ Limited to specific systems

SERVICE ACCOUNTS:
├─ Backup automation
│  └─ Always active
│  └─ High access (for backups)
│  └─ No human interaction
│
├─ Application service accounts
│  └─ App authentication
│  └─ Database connections
│  └─ API calls
│
├─ Monitoring/Security tools
│  └─ EDR agents
│  └─ SIEM collectors
│  └─ Antivirus services
│
└─ Scheduled tasks
   └─ Nightly jobs
   └─ Batch processing
   └─ Report generation

How to identify:
├─ Service account names: Service-like (backup_svc, app_sa)
├─ Activity pattern: Always regular (not human)
├─ Last logon: Recent (if automated)
├─ Groups: Service-specific groups
└─ No manager: Service accounts usually have none
```

### Critical User Attributes:

```
For each user, know:

IDENTIFICATION:
├─ Username (critical for investigation)
├─ Full name
├─ Email
├─ Employee ID
└─ Alternative accounts

STATUS:
├─ Active / Disabled / Locked
├─ On leave / Vacation / Sick
├─ On travel
├─ Onboarding / Offboarding
└─ Contractor expiry date

EMPLOYMENT:
├─ Department
├─ Job title
├─ Manager
├─ Cost center
├─ Start date
├─ End date (if known)
└─ Employment type (employee/contractor)

ACCESS RIGHTS:
├─ Group memberships
├─ System access
├─ Application licenses
├─ Database permissions
├─ Elevated access (admin?)
└─ API token access

SECURITY:
├─ MFA enrolled?
├─ Last password change
├─ Account age
├─ Privileged accounts
└─ Known high-risk
```

---

## User Lifecycle: Timeline Matters

### Onboarding:

```
Timeline (typically):
Day 0: Offer acceptance
Day -5: HR starts onboarding
Day 0: First day
├─ AD account created
├─ Email provisioned
├─ System access granted
├─ Device provisioned
└─ Groups added

Investigation implications:
├─ New account (< 1 month) might lack context
├─ First-time access anomalies normal
├─ Unusual system access might be training
├─ Check onboarding ticket/manager approval
└─ Service account pattern different (no training)

Red flags:
├─ Account created but no HR record
├─ Access granted beyond job scope
├─ Privileged access on day 1 (investigate)
└─ Multiple accounts for same person
```

### Normal Operation:

```
Active employee timeline:
├─ Regular login patterns (establish baseline)
├─ Typical access patterns
├─ Vacation/sick days (in calendar)
├─ Business trips (may change location)
├─ Role changes (access may change)
└─ Training events

Investigation implications:
├─ Compare against baseline
├─ Check calendar for off-hours access explanation
├─ Verify access is appropriate for role
├─ Monitor for privilege escalation
└─ Track access pattern changes
```

### Offboarding:

```
Timeline when employee leaves:
Day N: Notice given (usually 2 weeks)
├─ HR records: Last day marked
├─ Access revocation: Scheduled
├─ Equipment: Collected
└─ Accounts: Disabled after last day

Day N+1 onwards: Account status
├─ Account disabled (not deleted)
├─ Still exists (for audit)
├─ Cannot login
├─ But group memberships may persist
└─ Data access: Usually restricted

Investigation implications:
├─ If offboarded user has activity = ALERT!
├─ Could indicate: Credentials stolen before leaving
├─ Check: Offboarding completed properly?
├─ Check: All access revoked?
├─ Red flag: Disabled account with recent login
```

---

## Service Accounts vs Human Accounts

### How to Distinguish:

```
HUMAN ACCOUNTS:
├─ Activity pattern: Varies by day/time
├─ Work hours: 9-5 (mostly)
├─ Login locations: Office, sometimes home
├─ Weekends: Rare (except on-call)
├─ Activity: Irregular, contextual
├─ Manager: Always assigned
├─ Password: Changed regularly (policy)
├─ Reason for access: Role-based
└─ Failed logins: Occasional (user error)

SERVICE ACCOUNTS:
├─ Activity pattern: Precise, scheduled
├─ Work hours: 24/7 (automation)
├─ Login locations: Same server always
├─ Weekends: Same as weekdays
├─ Activity: Regular, predictable
├─ Manager: Often none (or infrastructure)
├─ Password: Changed rarely (stability needed)
├─ Reason for access: Application-specific
└─ Failed logins: Pattern-based (then success)

Example:

Alert: "50 failed logins from service account"

Human account alert:
├─ Verdict: Brute force attempt (SUSPICIOUS)
├─ Action: Reset password, check account

Service account alert:
├─ Pattern: Expected (automation retry)
├─ Verdict: False positive (expected FP)
├─ Action: Fix script/credentials
```

---

## Identity in Investigation

### How L1 Uses Identity Data:

```
STEP 1: Alert mentions user
Example: "john.doe performed unusual action"

STEP 2: Verify identity
├─ Search AD: "john.doe"
├─ Confirm: Real user or typo?
├─ Check: account status (active/disabled?)
├─ Check: Department (matches alert context?)
├─ Check: Manager (for verification)

STEP 3: Understand context
├─ Check: User on vacation? (calendar check)
├─ Check: Business trip? (travel approval)
├─ Check: Contract ended? (still should have access?)
├─ Check: New hire? (unusual for first week activity)

STEP 4: Assess appropriateness
├─ User role: Job title
├─ Required access: Does role need this access?
├─ Group memberships: Has necessary permissions?
├─ Escalation: Is this escalation authorized?

STEP 5: Decision
├─ Access is appropriate? → Normal activity
├─ Access unusual? → Investigate deeper
├─ Access unauthorized? → Possible compromise
```

### Identity Lookup Queries:

```
Quick AD searches for investigation:

Search: Username
├─ Returns: Full user record
├─ Use when: Alert has username

Search: Email address
├─ Returns: User account
├─ Use when: Alert has email instead

Search: User by Department
├─ Returns: All users in dept
├─ Use when: Investigating dept-wide incident

Search: Users in Group
├─ Returns: Group members
├─ Use when: Checking admin access

Search: Users by Status
├─ Returns: Active/disabled/locked
├─ Use when: Looking for terminated employees

Search: Recent changes
├─ Returns: Recently modified accounts
├─ Use when: Looking for unauthorized changes

Search: Service accounts
├─ Returns: Non-human accounts
├─ Use when: Separating service from human activity

Search: External users
├─ Returns: Contractors, guests
├─ Use when: Assessing external access
```

---

## Red Flags: Identity-Based

### Compromised Account Indicators:

```
RED FLAG 1: Disabled account with activity
├─ Account marked: Disabled in AD
├─ But: Recent login attempt detected
├─ Implies: Credentials stolen before disabling
├─ Action: INVESTIGATE IMMEDIATELY

RED FLAG 2: After-hours access by non-IT
├─ User: Regular employee (not admin/on-call)
├─ Time: 03:00 AM (off-hours)
├─ Activity: Accessing sensitive data
├─ Implies: Account possibly compromised
├─ Action: Contact user to verify

RED FLAG 3: Privilege escalation for new user
├─ User: Onboarded < 7 days
├─ Action: Added to admin group
├─ No ticket: No escalation request
├─ Implies: Unauthorized escalation
├─ Action: Investigate access request

RED FLAG 4: Activity from offboarded user
├─ User: Left company 30 days ago
├─ Status: Should be disabled
├─ But: Activity detected today
├─ Implies: Credentials not revoked OR data breach
├─ Action: ESCALATE IMMEDIATELY

RED FLAG 5: Multiple user IDs, same person
├─ Person: Has account1, account2, account3
├─ Pattern: Unusual (should be 1 account)
├─ Implies: Hidden access, privilege escalation
├─ Action: Verify with HR

RED FLAG 6: Service account access pattern
├─ Service account: Unusual time (not scheduled)
├─ Pattern: Changed (not normal automation)
├─ Implies: Compromised or misconfigured
├─ Action: Check automation script status

RED FLAG 7: External user with high privileges
├─ User: Contractor/partner
├─ Access: Admin or sensitive systems
├─ No ticket: No escalation
├─ Implies: Unauthorized access
├─ Action: Verify with manager

RED FLAG 8: Password never changed
├─ User: Account 5 years old
├─ Password age: 5 years
├─ Policy: Should be 90 days max
├─ Implies: Policy not enforced OR legacy account
├─ Action: Reset password, verify account status
```

---

## Real-World Identity Scenarios

### **Scenario 1: Service Account False Positive**

```
ALERT: "admin_backup accessed database at 03:00 AM"
SEVERITY: HIGH

Investigation:

Step 1: Identity check
├─ Search AD: "admin_backup"
├─ Found: Service account
├─ Type: Automation account
├─ Groups: DBA role, Backup automation
└─ Manager: None (service account)

Step 2: Pattern check
├─ Last 30 days activity:
│  └─ 03:00 AM every night
│  └─ Same pattern, same time
│  └─ Very predictable
└─ Very consistent (automation pattern)

Step 3: Business context
├─ Check IT tickets:
│  └─ Backup job scheduled nightly
│  └─ 03:00 AM window approved
└─ Check: Database needs admin for backup

Step 4: Threat assessment
├─ Malware: No (service account)
├─ Unauthorized: No (scheduled backup)
├─ Data theft: No (normal backup job)
└─ Compromise: No

VERDICT: FALSE_POSITIVE
REASON: Service account, expected nightly backup
ACTION: Close alert, document pattern
RECOMMENDATION: Suppress similar alerts in future
```

### **Scenario 2: Contractor Access Expired**

```
ALERT: "Contractor_Dev accessed source code repository"
SEVERITY: MEDIUM

Investigation:

Step 1: Identity check
├─ Search AD: "contractor_dev"
├─ Found: External contractor account
├─ Type: Contractor/temporary
├─ Employment: Ends 2024-06-15
└─ Today: 2024-06-22 (PAST END DATE!)

Step 2: Status check
├─ Account status: Should be disabled
├─ But: Activity detected
├─ Last activity: 2024-06-22 14:30
└─ PROBLEM: Account still active after end date

Step 3: Access assessment
├─ Repository access: Should be revoked
├─ But: Still can access
├─ Files accessed: Source code
├─ Implication: Access not revoked on offboarding

Step 4: Threat assessment
├─ Possible scenarios:
│  ├─ Contractor extended (verify with manager)
│  ├─ Offboarding incomplete (IT issue)
│  └─ Credentials stolen after contract (breach)

VERDICT: SUSPICIOUS
REASON: Account access after contract end date
ACTION: ESCALATE to L2
IMMEDIATE ACTIONS:
├─ Disable account immediately
├─ Audit repository access
├─ Check for data downloads
├─ Contact contractor and manager
└─ Review offboarding process
```

### **Scenario 3: Privilege Escalation Request**

```
ALERT: "alice@company.com added to DBA_ADMIN group"
SEVERITY: HIGH

Investigation:

Step 1: Identity check
├─ Search AD: "alice"
├─ Found: alice@company.com
├─ Department: Data analytics
├─ Job title: Senior analyst
├─ Manager: Bob (manager1@company.com)
└─ Account age: 2 years (established)

Step 2: Context check
├─ Calendar: Any projects?
│  └─ Yes: "Database migration Q3"
├─ Manager approval? Contact...
│  └─ Email chain found: "Approved for migration"
├─ IT ticket: #12345
│  └─ Subject: "Add alice to DBA for project"
│  └─ Approval: Manager + Security team
└─ Timing: Makes sense (project starting)

Step 3: Access appropriateness
├─ Role: Senior analyst on data team
├─ Project: Database migration (requires DBA)
├─ Duration: Temporary (90 days noted in ticket)
├─ Approval: Proper (manager + IT)
└─ Justification: Business need clear

Step 4: Threat assessment
├─ Unauthorized: No (proper approval)
├─ Unexpected: No (documented project)
├─ Compromise: No (normal escalation workflow)
└─ Time: Business hours (expected)

VERDICT: BENIGN
REASON: Authorized privilege escalation for business project
ACTION: Close alert
DOCUMENTATION: Link IT ticket to alert for future reference
```

---

## Common Identity Mistakes

### ❌ **Mistake 1: Not verifying user exists**

**সমস্যা:**
```
Alert: "john_doe performed action"
Assumption: Real user without checking AD
Result: John_doe might be typo or fake account
```

**সমাধান:**
```
Always search AD for username
Verify: Real user, active status, department
```

---

### ❌ **Mistake 2: Confusing service and human accounts**

**সমস্যা:**
```
Alert: "admin failed login 100 times"
Assumption: Brute force attack
Action: Escalate to IR (false alarm)
Reality: backup_admin service account retrying
```

**সমাধান:**
```
Check account type immediately
Service accounts have different patterns
Recognize automation failures vs attacks
```

---

### ❌ **Mistake 3: Not checking user status**

**সমস্যা:**
```
Alert: "employee_x accessed database"
Investigation: Looks normal
Forget to check: Employee left company 6 months ago
Reality: Credentials stolen, account should be disabled
```

**সমাধান:**
```
Always check AD status: Active/Disabled/Locked
Check: Last logon date
Verify: Employment still current
```

---

### ❌ **Mistake 4: Ignoring off-hours context**

**সমস্যা:**
```
Alert: "User access at 03:00 AM"
Assumption: Suspicious
Escalate: To IR
Reality: User on vacation in different timezone
```

**সমাধান:**
```
Check: Calendar for vacation/travel
Check: Timezone (different TZ = different hours)
Understand: User patterns vary
```

---

### ❌ **Mistake 5: Missing contractor access**

**সমস্যা:**
```
Alert: "External user accessed source code"
Assumption: Security breach
Reality: Contractor still has access (should be revoked)
Action: Escalate unnecessarily
```

**সমাধান:**
```
Track contractor end dates
Verify: Access revoked on offboard
Know: Who should/shouldn't have external access
```

---

## Identity Investigation Checklist

### **Quick Identity Verification (2 minutes)**

- [ ] Search AD for username
- [ ] Verify: Real user account
- [ ] Check: Active/Disabled/Locked status
- [ ] Check: Department/Job title (matches context?)
- [ ] Check: Manager (for verification)

### **Deep Identity Check (5 minutes)**

- [ ] User type: Human or service account?
- [ ] Employment status: Current employee/contractor?
- [ ] Contract end date: Current or past?
- [ ] On leave: Vacation/sick/sabbatical?
- [ ] Recent changes: New hire (<30 days)?
- [ ] Group memberships: Has necessary permissions?
- [ ] Privilege level: Admin access appropriate?

### **Context Gathering**

- [ ] Calendar check: Travel/events?
- [ ] IT tickets: Any change requests?
- [ ] HR system: Employment verified?
- [ ] Manager: Can contact for verification?
- [ ] Previous activity: Pattern established?

### **Decision Making**

- [ ] Is access appropriate for role?
- [ ] Is activity expected at this time?
- [ ] Is location/source reasonable?
- [ ] Any red flags from identity check?
- [ ] Need escalation or just documentation?

---

## Mini Quiz: Identity Inventory

### **Question 1: Service account vs human account - key পার্থক্য কোনটি?**

A) Service account এ more access থাকে  
B) Human account এ more access থাকে  
C) Service account activity predictable, human variable  
D) No difference in investigation

**Answer:** C) Service account activity predictable, human variable - এটাই key distinction

---

### **Question 2: Disabled account এ activity থাকলে কি করবেন?**

A) Ignore করুন, normal নয়  
B) Check করুন credentials breach হয়নি কিনা  
C) Escalate করুন immediately  
D) Close করুন alert

**Answer:** C) Escalate করুন immediately - Disabled account activity = RED FLAG

---

### **Question 3: Contractor end date pass হয়ে গেলে activity থাকলে?**

A) Normal, contractor extended  
B) SUSPICIOUS, verify contractor status  
C) False positive, ignore  
D) Just close alert

**Answer:** B) SUSPICIOUS, verify contractor status - Access should be revoked on end date

---

### **Question 4: Off-hours access সবসময় threat?**

A) হ্যা, সবসময় suspicious  
B) না, depends on context  
C) Only for non-IT staff  
D) Only weekends, not weekdays

**Answer:** B) না, depends on context - Check: Travel, timezone, on-call, project deadline

---

### **Question 5: কোন identity source সবচেয়ে reliable?**

A) SIEM logs  
B) Active Directory (AD)  
C) Email system  
D) Firewall logs

**Answer:** B) Active Directory (AD) - এটাই authoritative identity source বেশিরভাগ org এ

---

## সহজ ভাষায় সারসংক্ষেপ

**Identity Inventory = Complete user database**

**Key Identity Sources:**
- **AD:** On-premise user accounts (core)
- **Entra ID:** Cloud accounts (modern)
- **Okta:** SSO and app access
- **Google Workspace:** Cloud office
- **HR Systems:** Employment info (HR Bob, SAP, BambooHR)

**User Types:**
- **Human:** Variable patterns, work hours, role-based
- **Service:** Predictable patterns, 24/7, automation
- **Contractor:** Temporary access, end dates
- **External:** Guest accounts, limited access

**Identity in Investigation:**
1. Verify user exists in AD
2. Check status: Active/Disabled/Locked
3. Confirm employment current
4. Verify access appropriate
5. Check for red flags
6. Make verdict based on context

**Red Flags:**
- Disabled account with activity → ALERT
- After-hours + sensitive access → INVESTIGATE
- Service account pattern changed → CHECK
- Contractor past end date → ESCALATE
- Privilege escalation no ticket → INVESTIGATE
- Multiple accounts same person → VERIFY

**Remember:**
- Service ≠ Human (different patterns)
- Check account status first
- Verify employment current
- Understand user lifecycle
- Context matters (travel, leave, etc.)

---

## Resources for Learning

**Identity source documentation:**
- Microsoft AD documentation
- Entra ID / Azure AD docs
- Okta configuration
- HR system access

**Your company tools:**
- AD query interface
- HR system access
- Employee directory
- Contract tracking

---

**Module 10 Complete! ✅**

এখন আপনি জানেন:
- ✅ Identity inventory কি এবং কেন important
- ✅ 5টি major identity sources
- ✅ User attributes এবং meaning
- ✅ Human vs Service accounts
- ✅ User lifecycle: onboard, active, offboard
- ✅ Identity verification in investigations
- ✅ 8টি red flags for compromise
- ✅ Service account pattern recognition
- ✅ Real-world identity scenarios
- ✅ Common identity mistakes
- ✅ Identity investigation checklist

Progress: **10 of 28 modules complete (36%)**

