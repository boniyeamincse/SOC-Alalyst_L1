# Module 21: SOC Metrics and Objectives

## Learning Objectives

এই মডিউলের শেষে আপনি শিখবেন:

- SOC metrics কি এবং কেন গুরুত্বপূর্ণ
- Key metrics: Alert volume, FP rate, escalation rate
- Performance metrics: MTTD, MTTA, MTTR (next module detail)
- L1 Analyst metrics
- Metrics dashboard এবং reporting
- কীভাবে metrics calculate হয়
- Metrics-driven decisions
- Common metric mistakes
- Real metric examples

---

## শুরুর আগে: একটি গল্প

রিনা একজন SOC manager। মাসিক report তৈরি করছে।

Without metrics:
```
Report: "SOC working fine I think"
Executive: "What does 'fine' mean? 
           How many threats caught? 
           How fast did we respond?"
Report: "Uh... I don't know?"
```

With metrics:
```
Report:
├─ Alerts processed: 8,240 (↑5% from last month)
├─ False positive rate: 7.2% (↓0.8% - improving)
├─ Escalation rate: 12% (↑ due to new rules)
├─ MTTD (Mean Time To Detect): 4 hours
├─ MTTA (Mean Time To Acknowledge): 8 minutes
├─ MTTR (Mean Time To Respond): 2 hours
└─ Threat detection rate: 94%

Executive: "Good trend. FP rate improving. 
          Detection rate high. Approved budget 
          for additional resources."
```

**Metrics = Language of SOC success.**

---

## SOC Metrics কি?

### Definition:

**Metrics = Measurable data about SOC performance.**

```
Metrics tell:
├─ How much work (volume)
├─ How good quality (accuracy)
├─ How fast response (speed)
├─ How many threats (detection)
└─ How efficient (cost-effectiveness)
```

### Why Metrics Matter:

```
For L1 Analyst:
├─ Understand performance expectations
├─ See what matters to management
├─ Track personal improvement
├─ Get recognition for good work
└─ Learn from trends

For Manager:
├─ Understand team capacity
├─ Plan resources/hiring
├─ Identify improvement areas
├─ Report to executive
└─ Benchmark against industry

For Executive:
├─ Make budget decisions
├─ Understand security posture
├─ Report to board
├─ Plan security strategy
└─ Evaluate effectiveness
```

---

## Key SOC Metrics

### **Metric 1: Alert Volume**

```
Definition: How many alerts processed

Calculation:
Total alerts received in period (week/month/year)

Example:
├─ Monday: 280 alerts
├─ Tuesday: 320 alerts
├─ Wednesday: 290 alerts
├─ Thursday: 310 alerts
├─ Friday: 350 alerts
└─ Total: 1,550 alerts/week
   Average: 310 alerts/day

Trend tracking:
├─ Last month: 12,000 alerts
├─ This month: 15,240 alerts
└─ Trend: ↑27% (increase)

What it means:
├─ More traffic = More threats
├─ Increase = More detection or more attacks
├─ Decrease = System tuning or fewer threats
└─ Management view: Team capacity/staffing need

Target: Variable (depends on organization)
```

---

### **Metric 2: False Positive Rate**

```
Definition: % of alerts that are NOT real threats

Calculation:
(False Positives / Total Alerts) × 100

Example:
├─ Total alerts: 1,000
├─ True positives: 150 (confirmed threats)
├─ False positives: 850 (not threats)
└─ FP Rate: (850/1000) × 100 = 85%

Industry benchmark:
├─ Good: < 10% FP rate
├─ Average: 10-20% FP rate
├─ Poor: > 20% FP rate

Trend tracking:
├─ Last month: 12% FP rate
├─ This month: 8.5% FP rate
└─ Trend: ↓ (improving)

What it means:
├─ High FP = Alert fatigue, wasted time
├─ Low FP = Good rules, high quality
├─ Improvement = Rule tuning working
└─ Management view: Alert rule effectiveness

Target: < 10% (best practice)
```

---

### **Metric 3: Escalation Rate**

```
Definition: % of alerts escalated to L2

Calculation:
(Escalated Alerts / Total Alerts) × 100

Example:
├─ Total alerts: 1,000
├─ Escalated to L2: 120
├─ Escalation rate: (120/1000) × 100 = 12%

Healthy rate:
├─ Good: 5-15%
├─ Too high: > 20% (may indicate over-escalation)
├─ Too low: < 5% (may indicate under-escalation)

Trend:
├─ Last month: 8% escalation
├─ This month: 12% escalation
└─ Reason: New detection rules added

What it means:
├─ High escalation = Many complex cases
├─ Low escalation = Good at closing cases
├─ Sudden increase = New threat pattern
├─ Management view: L1 capability assessment

Target: 10-15% (depends on organization)
```

---

### **Metric 4: Alert Handling Time (MTTA)**

Mean Time To Acknowledge

```
Definition: Average time from alert to L1 action

Calculation:
Sum of (Time L1 acknowledged - Time alert arrived) 
/ Number of alerts

Example:
├─ Alert 1: 5 minutes to acknowledge
├─ Alert 2: 8 minutes
├─ Alert 3: 3 minutes
├─ Alert 4: 12 minutes
├─ Average: (5+8+3+12)/4 = 7 minutes

Target:
├─ Critical alerts: < 5 minutes
├─ High: < 15 minutes
├─ Medium: < 30 minutes
├─ Low: < 1 hour

SLA:
├─ Company commits: "95% of alerts acknowledged < 15 min"
├─ If missing SLA: Hiring/staffing problem
└─ Benchmark: < 10 minutes average

What it means:
├─ Fast MTTA = Responsive SOC
├─ Slow MTTA = Backlog, understaffed
├─ Trending worse = Team overloaded
└─ Management view: Team responsiveness

Your goal: < 10 minutes average
```

---

### **Metric 5: Investigation Time (MTTA)**

Mean Time To Triage + Investigate

```
Definition: Average time from alert to verdict

Calculation:
Sum of (Time investigation complete - Time alert)
/ Number of alerts closed

Example (L1 portion):
├─ Alert 1: 12 minutes (triage + investigate)
├─ Alert 2: 18 minutes
├─ Alert 3: 8 minutes
├─ Alert 4: 22 minutes
└─ Average: (12+18+8+22)/4 = 15 minutes

Target:
├─ By L1 alone: < 20 minutes
├─ Before L2 escalation: < 30 minutes

What it means:
├─ Fast investigation = Efficient analyst
├─ Slow investigation = Complex cases or inefficient
├─ Trending worse = Need training/tools
└─ Management view: Analyst productivity

Your goal: < 15 minutes average per alert
```

---

### **Metric 6: Threat Detection Rate**

```
Definition: % of actual threats detected

Calculation:
(Threats detected by system / All threats that existed) × 100

Example:
├─ Actual breaches/incidents: 50 (from post-mortem)
├─ Detected by SOC: 47
├─ Detection rate: (47/50) × 100 = 94%

Industry benchmark:
├─ Good: 90-99%
├─ Average: 75-90%
├─ Poor: < 75%

Trend:
├─ Last year: 85% detection
├─ This year: 92% detection
└─ Improvement: New tools, better rules

What it means:
├─ High detection = Strong security posture
├─ Low detection = Blind spots, need improvement
├─ Improvement = Money on tools/training working
└─ Management view: Security effectiveness

Target: > 90%
```

---

## L1 Analyst Personal Metrics

### What's Measured About You:

```
PRODUCTIVITY:
├─ Alerts handled/shift: Target 40-60
├─ Average investigation time: Target < 15 min
├─ Tickets closed/shift: Target 40-50
└─ Ticket volume increase: Track improvement

QUALITY:
├─ False positive rate: Target < 10% of YOUR alerts
├─ Escalation accuracy: Target > 90%
   (How many escalations are actually confirmed?)
├─ L2 confirmation rate: Did L2 agree with your verdict?
└─ Re-investigation rate: How many come back?

RELIABILITY:
├─ SLA compliance: % of alerts handled in time
├─ Attendance/punctuality
├─ On-call reliability
└─ Documentation completeness

PROFESSIONAL:
├─ Communication quality
├─ Team collaboration
├─ Training completion
└─ Certification progress
```

### Your Monthly Review Might Look Like:

```
L1 Analyst: john.doe - Month: June 2024

PRODUCTIVITY:
├─ Alerts handled: 8,240 (Target: 8,000) ✓
├─ Avg investigation time: 14 min (Target: 15) ✓
├─ Tickets closed: 1,850 (Target: 1,600) ✓

QUALITY:
├─ FP rate: 8.2% (Target: <10%) ✓
├─ Escalation accuracy: 92% (Target: 90%) ✓
├─ L2 agreement rate: 88% (Target: 85%) ✓

SLA COMPLIANCE:
├─ Critical SLA: 96% met (Target: 95%) ✓
├─ High SLA: 94% met (Target: 95%) ⚠
└─ Overall: 95% (Good)

ASSESSMENT:
├─ Exceeding productivity targets
├─ Quality metrics strong
├─ One area to improve: High priority SLA
└─ Overall rating: Exceeds Expectations

ACTION ITEMS:
├─ Recognize: Strong productivity & quality
├─ Train: High-priority alert handling
└─ Career: Ready for advanced topics
```

---

## SOC Metrics Dashboard

### What a Dashboard Might Show:

```
┌─────────────────────────────────────────────┐
│ SOC METRICS DASHBOARD - Real-time           │
├─────────────────────────────────────────────┤
│                                             │
│ TODAY:                                      │
│ ├─ Alerts: 310 (Avg: 310/day)             │
│ ├─ FP Rate: 8.1% (Trend: ↓)               │
│ ├─ Escalations: 12 (3.9%)                 │
│ └─ Threats detected: 8                    │
│                                             │
│ THIS WEEK:                                  │
│ ├─ Alerts: 1,550 (↑7% from last week)    │
│ ├─ FP Rate: 8.5% (↓0.3%)                 │
│ ├─ MTTA: 8 minutes                       │
│ ├─ MTTD: 4 hours                         │
│ ├─ Escalation rate: 12%                  │
│ ├─ Detection rate: 94%                   │
│ └─ SLA Compliance: 96%                   │
│                                             │
│ THIS MONTH:                                 │
│ ├─ Alerts: 6,200                         │
│ ├─ TP count: 620 (10%)                   │
│ ├─ FP count: 5,580 (90%)                 │
│ ├─ Incidents confirmed: 3                │
│ └─ Avg incident response: 1.5 hours      │
│                                             │
│ ALERTS BY SEVERITY:                        │
│ ├─ Critical: 5 (1.6%)                    │
│ ├─ High: 47 (15.2%)                      │
│ ├─ Medium: 155 (50%)                     │
│ └─ Low: 103 (33.2%)                      │
│                                             │
│ TOP ALERT TYPES:                           │
│ ├─ Brute Force: 45 (14.5%)               │
│ ├─ Unusual Login: 52 (16.8%)             │
│ ├─ Malware: 18 (5.8%)                    │
│ ├─ Phishing: 32 (10.3%)                  │
│ └─ Other: 163 (52.6%)                    │
│                                             │
└─────────────────────────────────────────────┘
```

---

## How Metrics Drive SOC Decisions

### Example: High FP Rate

```
Observation: FP rate increased from 7% to 14%

Investigation:
├─ Which alert type? "Unusual Login" spike
├─ When did it increase? Last week
├─ What changed? New detection rule added
└─ Why? Rule too sensitive

Decision:
├─ Option 1: Tune rule threshold
├─ Option 2: Add whitelist
├─ Option 3: Disable rule
├─ Option 4: Improve rule logic

Action:
├─ Tune threshold (raises bar for alerting)
├─ Test with historical data
├─ Deploy updated rule
└─ Monitor FP rate (expect ↓ next week)

Result:
├─ New FP rate: 9% ✓
├─ Still catching real threats: YES
└─ Decision validated
```

---

### Example: Low Escalation Rate

```
Observation: Escalation rate only 5% (below 10% target)

Interpretation options:
├─ Are L1s too confident? (closing too many)
├─ Are rules good? (not generating bad alerts)
├─ Are cases simple? (all solvable at L1)
├─ Is training adequate? (analysts capable)

Investigation:
├─ Check: L2 re-investigation rate (how many come back?)
├─ Check: MTTD/MTTR (detecting and solving fast)
├─ Check: Threat detection rate (catching real threats)

If concerning:
├─ Might be under-escalating
├─ Need to review recent escalations
├─ Train on escalation criteria

If positive:
├─ L1 team is very capable
├─ Detection rules are good
├─ Celebrate success
```

---

## Common Metric Mistakes

### ❌ **Mistake 1: Vanity metrics**

**সমস्या:**
```
"We handled 10,000 alerts!"
But: 95% false positives
Reality: Busywork, no value
```

**সমাধান:**
```
Focus on: Quality not just volume
├─ FP rate (accuracy)
├─ Detection rate (effectiveness)
├─ MTTD/MTTA/MTTR (speed)
└─ Not just alert count
```

---

### ❌ **Mistake 2: Wrong incentives**

**समस्या:**
```
"Close alerts as fast as possible"
Result: Poor investigation, quality drops
```

**समाधान:**
```
Balance speed + quality:
├─ Target: < 15 min investigation
├─ AND: > 90% accuracy
└─ Not just speed
```

---

### ❌ **Mistake 3: Ignoring trends**

**समस्या:**
```
"FP rate is 8%"
Don't look at: trend (was 5%, now 8%)
Miss: degradation signal
```

**समाधान:**
```
Track trends:
├─ Compare week/month
├─ Identify direction (↑ or ↓)
├─ Understand why
└─ Act on trends
```

---

### ❌ **Mistake 4: Metric manipulation**

**समस्या:**
```
Close alerts without investigating (false closure)
Just to hit KPI targets
```

**समाधान:**
```
Metrics should drive behavior:
├─ Quality metrics prevent gaming
├─ L2 re-investigation catches false closure
├─ Honesty in metrics
```

---

## Metrics Checklist

### **Your Monthly Review:**

- [ ] Alert volume: Track and trend
- [ ] FP rate: Track accuracy
- [ ] Escalation rate: Compare to target
- [ ] MTTA: Track responsiveness
- [ ] MTTD: Track investigation speed
- [ ] SLA compliance: % met target
- [ ] Detection rate: Threats caught
- [ ] Quality feedback: L2 agreement

### **Manager's Monthly Review:**

- [ ] All L1 metrics aggregated
- [ ] Trends identified
- [ ] Issues flagged
- [ ] Capacity assessment
- [ ] Training needs
- [ ] Resource planning
- [ ] Report to executive

### **Personal Goal Setting:**

- [ ] Understand metrics that matter
- [ ] Set personal targets aligned with team
- [ ] Track progress
- [ ] Identify improvement areas
- [ ] Celebrate wins

---

## Mini Quiz: Metrics

### **Question 1: False Positive Rate 12% মানে কি?**

A) 12% of alerts are real threats  
B) 12% of alerts are not real threats  
C) 12 false positives total  
D) Alert system 12% broken

**Answer:** B) 12% of alerts are not real threats - Industry target < 10%

---

### **Question 2: MTTA 8 minutes মানে?**

A) Alert নিতে 8 minutes  
B) Acknowledge করতে 8 minutes গড়  
C) Investigation 8 minutes  
D) Escalate করতে 8 minutes

**Answer:** B) Acknowledge করতে 8 minutes গড় - Mean Time To Acknowledge

---

### **Question 3: Detection rate 94% মানে?**

A) 94% alerts are real threats  
B) 94% of actual threats detected  
C) 94% of alerts investigated  
D) 94% SLA met

**Answer:** B) 94% of actual threats detected - 6% threats missed

---

### **Question 4: Escalation rate 15% কি সাধারণত good?**

A) Too high, over-escalating  
B) Normal range (10-20%)  
C) Too low, under-escalating  
D) Perfect, target

**Answer:** B) Normal range (10-20%) - Depends on organization

---

### **Question 5: Alert volume বেড়েছে 20%, কি করবেন?**

A) Ignore, normal variation  
B) Investigate: more attacks or better detection?  
C) Hire more people  
D) Disable rules

**Answer:** B) Investigate: more attacks or better detection? - Understand trend before acting

---

## সহজ ভাষায় সারসংক্ষেপ

**SOC Metrics = Performance measurement**

**Key Metrics:**
- **Alert Volume:** কত alert আসে
- **FP Rate:** % false positives (target <10%)
- **Escalation Rate:** % escalated to L2 (target 10-15%)
- **MTTA:** Avg time to acknowledge (target <10 min)
- **MTTD:** Avg time to investigate (target <15 min)
- **Detection Rate:** % actual threats caught (target >90%)

**L1 Metrics Tracked:**
- Alerts handled/shift (40-60)
- Avg investigation time (<15 min)
- FP rate (<10%)
- Escalation accuracy (>90%)
- SLA compliance (>95%)

**Dashboard Shows:**
- Real-time metrics
- Trends (↑ or ↓)
- Alerts by type/severity
- Performance vs target

**Why Metrics Matter:**
- Drive decision making
- Identify improvement areas
- Show security posture
- Justify budget/resources

**Common Mistakes:**
- Focus on volume, not quality
- Wrong incentives (speed over accuracy)
- Ignore trends (just look at current)
- Metric manipulation (fake closure)

**Remember:**
- Quality > Volume
- Balance speed + accuracy
- Track trends
- Honest metrics

---

## Resources for Learning

**Your company dashboard:**
- Check daily metrics
- Understand targets
- Track personal progress

**Benchmarks:**
- SANS SOC metrics
- Industry standards
- Your company baseline

---

**Module 21 Complete! ✅**

এখন আপনি জানেন:
- ✅ SOC metrics কি
- ✅ Key metrics: alert volume, FP rate, escalation rate
- ✅ MTTA, MTTD, detection rate
- ✅ L1 personal metrics
- ✅ Metrics dashboard
- ✅ How metrics drive decisions
- ✅ Common metric mistakes
- ✅ Metrics checklist

Progress: **21 of 28 modules complete (75%)**

🎉 **3/4 THROUGH THE COURSE!** 🎉

