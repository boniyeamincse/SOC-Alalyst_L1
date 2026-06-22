# SOC Diagrams

Visual representations of SOC operations, workflows, and architecture.

## Diagram Files

### 1. SOC Team Structure
**File:** `ascii/01-soc-team-structure.txt`

Organization hierarchy and responsibilities:
- CISO → Manager → L1/L2/L3/IR teams
- L1: Alert handling and triage
- L2: Investigation and analysis
- L3: Engineering and detection
- IR: Incident response

### 2. Alert Triage Flow
**File:** `ascii/02-alert-triage-flow.txt`

L1 analyst decision process:
1. Verify alert accuracy
2. Quick investigation (8-12 min)
3. Verdict decision (TP/FP/Benign/Suspicious)
4. Action (Close or Escalate)

Time budget: 15 minutes max

### 3. Escalation Workflow
**File:** `ascii/03-escalation-workflow.txt`

Multi-level escalation process:
- L1 decision: Close or Escalate?
- L2 receives ticket with evidence
- L2 decision: Close, Further investigate, or Escalate?
- Possible escalation to L3 (forensics) or IR (incident)

### 4. Event to Alert Flow
**File:** `ascii/04-event-to-alert-flow.txt`

Data transformation pipeline:
1. Raw events (login, file access, traffic, etc.)
2. Log collection (Windows, Syslog, Firewall, EDR)
3. SIEM normalization and indexing
4. Detection rules applied
5. Alert generation
6. Alert queue assignment to L1

### 5. SOC Metrics Flow
**File:** `ascii/05-soc-metrics-flow.txt`

Metrics collection and reporting:
- Daily metrics: Alert volume, FP rate, escalation rate
- Performance: MTTA, MTTD, MTTR
- Dashboards: Real-time, daily, weekly, monthly
- Executive reporting: Trends and achievements

### 6. Network Architecture
**File:** `ascii/06-network-vpn-firewall.txt`

Network security zones:
- External zone (Internet - Untrusted)
- DMZ (Internet-facing servers)
- Internal zone (Corporate network - Trusted)
- VPN gateway for remote access
- Firewall rules and segmentation
- Trust zone boundaries

## Usage

Each diagram is provided as ASCII text for easy viewing in:
- Terminal/console
- Text editors
- GitHub/GitLab
- Markdown documents

## Adding Diagrams

To add new diagrams:

1. Create ASCII version in `ascii/` folder
2. Use clear boxes and arrows
3. Include legend/explanation
4. Reference relevant module
5. Update this README

## Integration

Diagrams are referenced in course modules:
- Module 2: Team structure
- Module 6: Prioritization flow
- Module 7: Triage process
- Module 13: Network diagrams
- Module 15: Enrichment flow
- Module 19: Escalation process
- Module 21: Metrics tracking

## Format Notes

- ASCII art for universality
- Compatible with all viewers
- Responsive (no rendering issues)
- Easy to modify/update
- Suitable for documentation

---

**Last updated:** 2024-06-22
