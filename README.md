# SOC Level 1 Analyst Course

Complete beginner-to-advanced training for SOC Level 1 analysts.

**Language:** Bangla-English mixed | **Level:** Beginner → Advanced | **Duration:** 40+ hours

---

## 📋 Quick Start

1. **Start here:** [Module 1: Introduction to SOC](modules/module-01-introduction-to-soc/)
2. **Progress:** Complete modules 1-28 sequentially
3. **Labs:** Practice with labs in modules 24-26
4. **Assessment:** Final exam in module 28

---

## 📚 Course Structure

### Phase 1: Foundations (Modules 1-7)
- Module 01: Introduction to SOC
- Module 02: SOC Team Structure
- Module 03: SOC Tools & Environment
- Module 04: Events, Logs & Alerts
- Module 05: Alert Properties
- Module 06: Alert Prioritisation
- Module 07: Alert Triage Fundamentals

### Phase 2: Investigation Skills (Modules 8-16)
- Module 08: Alert Verdicts
- Module 09: Investigation Methodology
- Module 10: Identity Inventory
- Module 11: Asset Inventory
- Module 12: Threat Intelligence Lookups
- Module 13: Network Diagrams
- Module 14: Workbooks, Playbooks, Runbooks
- Module 15: Enrichment Process
- Module 16: SIEM Investigation

### Phase 3: Professional Skills (Modules 17-23)
- Module 17: Common Alert Scenarios
- Module 18: Alert Reporting
- Module 19: Alert Escalation
- Module 20: SOC Communication
- Module 21: SOC Metrics & Objectives
- Module 22: SOC Improvement & Learning
- Module 23: Professional Skills & Resilience

### Phase 4: Practical Application (Modules 24-28)
- Module 24: Beginner Practical Lab
- Module 25: Intermediate Practical Lab
- Module 26: Advanced Practical Lab
- Module 27: Capstone Project
- Module 28: Final Assessment

---

## 📁 Directory Structure & File Index

```
soc-level-1-analyst-course/
├── 📄 README.md (this file)
├── 📄 CHANGELOG.md (release history)
├── 📄 CONTRIBUTING.md (contribution guidelines)
├── 📄 LICENSE (course license)
├── 📄 .gitignore (git configuration)
│
├── 📁 docs/
│   ├── 📄 course-overview.md (course summary)
│   ├── 📄 course-roadmap.md (learning path)
│   ├── 📄 learning-objectives.md (module objectives)
│   ├── 📄 prerequisites.md (requirements)
│   ├── 📄 glossary.md (SOC terminology)
│   ├── 📄 soc-l1-career-path.md (career guidance)
│   └── 📄 idea.md (course concept notes)
│
├── 📁 modules/ (28 complete modules)
│   ├── 📂 module-01-introduction-to-soc/
│   │   └── index.md (483 lines - SOC basics, CIA triad, team structure)
│   ├── 📂 module-02-soc-team-structure/
│   │   └── index.md (954 lines - team roles, escalation, careers)
│   ├── 📂 module-03-soc-tools-and-environment/
│   │   └── index.md (895 lines - SIEM, EDR, SOAR, TI platforms)
│   ├── 📂 module-04-events-logs-and-alerts/
│   │   └── index.md (874 lines - event vs log vs alert)
│   ├── 📂 module-05-alert-properties/
│   │   └── index.md (955 lines - 10 alert properties, fields)
│   ├── 📂 module-06-alert-prioritisation/
│   │   └── index.md (931 lines - severity, SLA, prioritization)
│   ├── 📂 module-07-alert-triage-fundamentals/
│   │   └── index.md (1062 lines - 5-step triage process)
│   ├── 📂 module-08-alert-verdicts/
│   │   └── index.md (1177 lines - TP, FP, BENIGN, SUSPICIOUS, ESCALATED)
│   ├── 📂 module-09-investigation-methodology/
│   │   └── index.md (1208 lines - 4-phase investigation)
│   ├── 📂 module-10-identity-inventory/
│   │   └── index.md (1066 lines - user context, AD, HR systems)
│   ├── 📂 module-11-asset-inventory/
│   │   └── index.md (995 lines - system context, CMDB, criticality)
│   ├── 📂 module-12-threat-intelligence-lookups/
│   │   └── index.md (1023 lines - TI platforms, reputation)
│   ├── 📂 module-13-network-diagrams/
│   │   └── index.md (882 lines - network architecture, zones)
│   ├── 📂 module-14-workbooks-playbooks-runbooks/
│   │   └── index.md (883 lines - documentation types)
│   ├── 📂 module-15-enrichment-process/
│   │   └── index.md (874 lines - enrichment workflow)
│   ├── 📂 module-16-siem-investigation/
│   │   └── index.md (910 lines - SIEM queries, pivoting)
│   ├── 📂 module-17-common-alert-scenarios/
│   │   └── index.md (800 lines - 7 real-world scenarios)
│   ├── 📂 module-18-alert-reporting/
│   │   └── index.md (858 lines - Five Ws, documentation)
│   ├── 📂 module-19-alert-escalation/
│   │   └── index.md (806 lines - escalation criteria)
│   ├── 📂 module-20-soc-communication/
│   │   └── index.md (876 lines - professional communication)
│   ├── 📂 module-21-soc-metrics-objectives/
│   │   └── index.md (723 lines - metrics, KPIs, SLA)
│   ├── 📂 module-22-soc-improvement-learning/
│   │   └── index.md (899 lines - continuous improvement)
│   ├── 📂 module-23-professional-skills-resilience/
│   │   └── index.md (872 lines - stress management, ethics)
│   ├── 📂 module-24-beginner-practical-lab/
│   │   └── index.md (539 lines - real scenario investigation)
│   ├── 📂 module-25-intermediate-practical-lab/
│   │   └── index.md (576 lines - mixed red flags scenario)
│   ├── 📂 module-26-advanced-practical-lab/
│   │   └── index.md (538 lines - active incident scenario)
│   ├── 📂 module-27-capstone-project/
│   │   └── index.md (536 lines - full shift simulation)
│   └── 📂 module-28-final-assessment/
│       └── index.md (753 lines - 30-question exam)
│
├── 📁 playbooks/ (6 SOC playbooks)
│   ├── 📄 phishing-alert-playbook.md (61 lines - email verification steps)
│   ├── 📄 malware-alert-playbook.md (71 lines - malware detection response)
│   ├── 📄 vpn-bruteforce-playbook.md (66 lines - brute force investigation)
│   ├── 📄 unusual-login-playbook.md (63 lines - location anomaly check)
│   ├── 📄 suspicious-powershell-playbook.md (61 lines - PS execution analysis)
│   └── 📄 network-scanning-playbook.md (68 lines - reconnaissance response)
│
├── 📁 diagrams/ (visual guides)
│   ├── 📄 README.md (diagram descriptions)
│   └── 📁 ascii/ (6 ASCII diagrams, 395 lines total)
│       ├── 📄 01-soc-team-structure.txt (organizational hierarchy)
│       ├── 📄 02-alert-triage-flow.txt (L1 decision process)
│       ├── 📄 03-escalation-workflow.txt (multi-level escalation)
│       ├── 📄 04-event-to-alert-flow.txt (SIEM pipeline)
│       ├── 📄 05-soc-metrics-flow.txt (metrics collection)
│       └── 📄 06-network-vpn-firewall.txt (network architecture)
│
├── 📁 docs/ (documentation)
│   ├── course-overview.md
│   ├── course-roadmap.md
│   ├── glossary.md
│   ├── learning-objectives.md
│   ├── prerequisites.md
│   ├── soc-l1-career-path.md
│   └── idea.md
│
├── 📁 assets/ (images & media)
│   └── (ready for course illustrations)
│
├── 📁 datasets/ (sample data for labs)
│   └── (SIEM logs, alerts, inventory data)
│
├── 📁 labs/ (structured lab exercises)
│   └── (supporting lab materials)
│
├── 📁 quizzes/ (assessment files)
│   └── (quiz questions & answers)
│
├── 📁 solutions/ (answer keys)
│   └── (lab & quiz solutions)
│
├── 📁 references/ (quick references)
│   └── (cheatsheets, lookup guides)
│
├── 📁 runbooks/ (technical procedures)
│   └── (step-by-step technical runbooks)
│
├── 📁 scripts/ (utility scripts)
│   └── (automation & helper scripts)
│
├── 📁 templates/ (document templates)
│   └── (escalation, report templates)
│
└── 📁 workbooks/ (investigation workbooks)
    └── (workbook examples & templates)
```

---

## 📊 Course Statistics

| Metric | Value |
|--------|-------|
| **Total Modules** | 28 |
| **Total Content Lines** | ~23,500 |
| **Playbooks** | 6 |
| **Diagrams** | 6 |
| **Theoretical Modules** | 23 |
| **Practical Labs** | 4 |
| **Capstone Modules** | 1 |
| **Assessment Questions** | 30 |
| **Estimated Learning Time** | 40+ hours |
| **Language** | Bangla-English mixed |

---

## 🎯 Learning Outcomes

After completing this course, you will be able to:

✅ Understand SOC operations and team structure  
✅ Triage alerts systematically (5-step process)  
✅ Investigate alerts using enrichment techniques  
✅ Determine alert verdicts (TP/FP/Benign/Suspicious)  
✅ Escalate appropriately to L2/L3 teams  
✅ Write professional alert reports  
✅ Communicate clearly with stakeholders  
✅ Understand SOC metrics and performance targets  
✅ Handle real-world incident scenarios  
✅ Apply continuous improvement mindset  

---

## 🚀 Getting Started

### Prerequisites
- Basic computer security knowledge
- Familiarity with Windows/Linux
- Understanding of networking basics
- Motivation to learn cybersecurity

### How to Use This Course

1. **Read Module 1** to understand SOC fundamentals
2. **Follow sequentially** through Modules 2-23
3. **Complete practical labs** in Modules 24-26
4. **Do capstone** in Module 27 (full shift simulation)
5. **Take final exam** in Module 28

### Time Commitment

- **Per module:** 1-2 hours
- **Practical labs:** 2-3 hours each
- **Capstone:** 2-3 hours
- **Total:** 40+ hours

---

## 📖 How to Navigate

### For Learners
1. Start: `modules/module-01-introduction-to-soc/index.md`
2. Reference: `docs/learning-objectives.md` for guidance
3. Practice: `modules/module-24-beginner-practical-lab/index.md`
4. Review: `playbooks/` for real procedures

### For Instructors
1. Overview: `docs/course-overview.md`
2. Roadmap: `docs/course-roadmap.md`
3. Materials: All in `modules/` folder
4. Assessment: Module 28 final exam

### For Reference
- **Glossary:** `docs/glossary.md`
- **Career Path:** `docs/soc-l1-career-path.md`
- **Diagrams:** `diagrams/` folder
- **Playbooks:** `playbooks/` folder

---

## 📝 File Summary

| Directory | Purpose | Status |
|-----------|---------|--------|
| modules/ | Core course content (28 modules) | ✅ Complete |
| playbooks/ | SOC alert response procedures | ✅ Complete |
| diagrams/ | Visual guides & architecture | ✅ Complete |
| docs/ | Documentation & guidance | ✅ Complete |
| datasets/ | Sample data for labs | 📋 Ready |
| templates/ | Document templates | 📋 Ready |
| solutions/ | Answer keys | 📋 Ready |
| references/ | Quick reference guides | 📋 Ready |
| assets/ | Images & media | 📋 Ready |
| scripts/ | Utility scripts | 📋 Ready |

---

## 🔄 Updates & Contributions

See `CONTRIBUTING.md` for guidelines on:
- Reporting issues
- Submitting improvements
- Adding new content
- Fixing errors

See `CHANGELOG.md` for release history.

---

## 📄 License

This course is provided as educational material. See `LICENSE` for details.

---

## 🎓 Certificate

Upon completing all 28 modules and passing the final assessment (70%+), you will receive a course completion certificate.

---

## 💡 Tips for Success

1. **Take notes** while reading each module
2. **Review mini-quizzes** to reinforce learning
3. **Complete practical labs** - hands-on practice is essential
4. **Study playbooks** - reference real procedures
5. **Review diagrams** - visual understanding helps
6. **Join study groups** - collaborative learning
7. **Practice repeatedly** - repetition builds confidence
8. **Reference glossary** - SOC terminology can be complex

---

## 🤝 Support

- **Questions:** Review relevant module sections
- **Issues:** Check CONTRIBUTING.md
- **Feedback:** Contribute improvements
- **Career guidance:** See docs/soc-l1-career-path.md

---

## 📧 Contact

For course information, visit the project repository.

---

**Last Updated:** 2024-06-22  
**Version:** 1.0  
**Status:** Complete & Ready for Production

---

**Welcome to the SOC! Good luck on your journey! 🛡️**
