#!/usr/bin/env python3
"""
Add Previous / Next page navigation to every module index.md file.
Run from the repo root:  python3 scripts/add_navigation.py
"""

import os
import re

MODULES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "modules")

# Ordered list of all 28 modules
MODULES = [
    ("module-01-introduction-to-soc",          "Module 01: Introduction to SOC"),
    ("module-02-soc-team-structure",            "Module 02: SOC Team Structure"),
    ("module-03-soc-tools-and-environment",     "Module 03: SOC Tools & Environment"),
    ("module-04-events-logs-and-alerts",        "Module 04: Events, Logs & Alerts"),
    ("module-05-alert-properties",              "Module 05: Alert Properties"),
    ("module-06-alert-prioritisation",          "Module 06: Alert Prioritisation"),
    ("module-07-alert-triage-fundamentals",     "Module 07: Alert Triage Fundamentals"),
    ("module-08-alert-verdicts",                "Module 08: Alert Verdicts"),
    ("module-09-investigation-methodology",     "Module 09: Investigation Methodology"),
    ("module-10-identity-inventory",            "Module 10: Identity Inventory"),
    ("module-11-asset-inventory",               "Module 11: Asset Inventory"),
    ("module-12-threat-intelligence-lookups",   "Module 12: Threat Intelligence Lookups"),
    ("module-13-network-diagrams",              "Module 13: Network Diagrams"),
    ("module-14-workbooks-playbooks-runbooks",  "Module 14: Workbooks, Playbooks & Runbooks"),
    ("module-15-enrichment-process",            "Module 15: Enrichment Process"),
    ("module-16-siem-investigation",            "Module 16: SIEM Investigation"),
    ("module-17-common-alert-scenarios",        "Module 17: Common Alert Scenarios"),
    ("module-18-alert-reporting",               "Module 18: Alert Reporting"),
    ("module-19-alert-escalation",              "Module 19: Alert Escalation"),
    ("module-20-soc-communication",             "Module 20: SOC Communication"),
    ("module-21-soc-metrics-objectives",        "Module 21: SOC Metrics & Objectives"),
    ("module-22-soc-improvement-learning",      "Module 22: SOC Improvement & Learning"),
    ("module-23-professional-skills-resilience","Module 23: Professional Skills & Resilience"),
    ("module-24-beginner-practical-lab",        "Module 24: Beginner Practical Lab"),
    ("module-25-intermediate-practical-lab",    "Module 25: Intermediate Practical Lab"),
    ("module-26-advanced-practical-lab",        "Module 26: Advanced Practical Lab"),
    ("module-27-capstone-project",              "Module 27: Capstone Project"),
    ("module-28-final-assessment",              "Module 28: Final Assessment"),
]

# Marker so we never add navigation twice
NAV_MARKER = "<!-- nav-footer -->"

def build_nav(index):
    """Return the navigation block for the module at position `index` (0-based)."""
    total = len(MODULES)

    # Previous link
    if index == 0:
        prev_link = "*(This is the first module)*"
    else:
        prev_dir, prev_title = MODULES[index - 1]
        prev_link = f"[⬅️ {prev_title}](../{prev_dir}/index.md)"

    # Next link
    if index == total - 1:
        next_link = "*(This is the last module)*"
    else:
        next_dir, next_title = MODULES[index + 1]
        next_link = f"[{next_title} ➡️](../{next_dir}/index.md)"

    nav = (
        f"\n\n---\n\n"
        f"{NAV_MARKER}\n"
        f"## 🧭 Navigation\n\n"
        f"| | |\n"
        f"|---|---|\n"
        f"| **Previous** | {prev_link} |\n"
        f"| **Next** | {next_link} |\n"
        f"| **🏠 Course Home** | [STUDY_NOTES.md](../../STUDY_NOTES.md) |\n"
    )
    return nav


def process_module(index, folder, title):
    path = os.path.join(MODULES_DIR, folder, "index.md")
    if not os.path.isfile(path):
        print(f"  ⚠️  MISSING: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove existing nav block if already added (idempotent)
    if NAV_MARKER in content:
        # Strip everything from the last "---\n\n<!-- nav-footer -->" onwards
        cut = content.rfind("\n\n---\n\n" + NAV_MARKER)
        if cut != -1:
            content = content[:cut]

    # Strip trailing whitespace / newlines, then append nav
    content = content.rstrip()
    content += build_nav(index)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  ✅ Updated: {folder}/index.md")


def main():
    print(f"\n📂 Modules directory: {MODULES_DIR}\n")
    for i, (folder, title) in enumerate(MODULES):
        process_module(i, folder, title)
    print(f"\n🎉 Done! Navigation added to {len(MODULES)} modules.\n")


if __name__ == "__main__":
    main()
