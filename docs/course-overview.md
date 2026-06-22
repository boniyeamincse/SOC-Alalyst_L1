# SOC Level 1 Analyst Course Outline

## Beginner to Advanced Level

---

## Module 1: Introduction to SOC

### 1.1 What is SOC?

### 1.2 Purpose of SOC

### 1.3 SOC and CIA Triad

### 1.4 Why Organisations Need SOC

### 1.5 Common SOC Use Cases

### 1.6 In-House SOC vs Managed SOC

### 1.7 SOC Career Path Overview

---

## Module 2: SOC Team Structure and Responsibilities

### 2.1 SOC Team Overview

### 2.2 SOC L1 Analyst Role

### 2.3 SOC L2 Analyst Role

### 2.4 SOC L3 Analyst Role

### 2.5 SOC Engineer Role

### 2.6 SOC Manager Role

### 2.7 Daily Duties of SOC L1 Analyst

### 2.8 Role-Based SOC Workflow

---

## Module 3: SOC Tools and Environment

### 3.1 What is SIEM?

### 3.2 What is EDR?

### 3.3 What is SOAR?

### 3.4 Firewall and VPN Logs

### 3.5 Email Security Gateway

### 3.6 Threat Intelligence Platforms

### 3.7 Ticketing and Case Management Tools

### 3.8 SOC Dashboard Overview

---

## Module 4: Events, Logs, and Alerts

### 4.1 What is a Log?

### 4.2 What is an Event?

### 4.3 What is an Alert?

### 4.4 Difference Between Event and Alert

### 4.5 From Events to Alerts

### 4.6 Detection Rules

### 4.7 Alert Noise and Alert Fatigue

### 4.8 Common SOC Alert Types

---

## Module 5: Alert Properties

### 5.1 Alert Time

### 5.2 Event Time vs Alert Time

### 5.3 Alert Name

### 5.4 Alert Severity

### 5.5 Alert Status

### 5.6 Alert Verdict

### 5.7 Alert Assignee

### 5.8 Alert Description

### 5.9 Alert Fields

### 5.10 Affected User, Host, and IP

### 5.11 Source and Destination Information

---

## Module 6: Alert Severity and Prioritisation

### 6.1 What is Alert Severity?

### 6.2 Low Severity Alerts

### 6.3 Medium Severity Alerts

### 6.4 High Severity Alerts

### 6.5 Critical Severity Alerts

### 6.6 Picking the Right Alert

### 6.7 Asset Criticality

### 6.8 User Privilege Level

### 6.9 Business Impact

### 6.10 Alert Prioritisation Workflow

---

## Module 7: SOC L1 Alert Triage Fundamentals

### 7.1 What is Alert Triage?

### 7.2 Purpose of Alert Triage

### 7.3 L1 Role in Alert Triage

### 7.4 L2 Role in Alert Triage

### 7.5 SOC Engineer Role in Alert Quality

### 7.6 SOC Manager Role in Triage Quality

### 7.7 Triage Mindset for Beginners

### 7.8 Basic Triage Questions

### 7.9 Triage Mistakes to Avoid

---

## Module 8: Alert Verdicts and Classifications

### 8.1 What is a Verdict?

### 8.2 True Positive

### 8.3 False Positive

### 8.4 Benign or Expected Activity

### 8.5 Suspicious Activity

### 8.6 Needs Escalation

### 8.7 Unknown or Inconclusive Verdict

### 8.8 When to Close an Alert

### 8.9 When Not to Close an Alert

### 8.10 Verdict Decision Tree

---

## Module 9: SOC Investigation Methodology

### 9.1 Investigation Flow

### 9.2 Who, What, When, Where, Why Method

### 9.3 Timeline Building

### 9.4 Evidence Collection

### 9.5 Context Gathering

### 9.6 Log Correlation

### 9.7 Identifying Normal vs Abnormal Activity

### 9.8 Determining Business Impact

### 9.9 Final Investigation Decision

---

## Module 10: Identity Inventory for SOC

### 10.1 What is Identity Inventory?

### 10.2 Why Identity Inventory is Important

### 10.3 User Accounts

### 10.4 Service Accounts

### 10.5 Privileged Accounts

### 10.6 User Role and Department

### 10.7 User Location and Working Hours

### 10.8 User Access Rights

### 10.9 Identity Inventory Sources

### 10.10 Active Directory and Entra ID

### 10.11 SSO Providers

### 10.12 HR Systems

### 10.13 BambooHR, SAP, and HiBob

### 10.14 Custom CSV or Excel Inventory

---

## Module 11: Asset Inventory for SOC

### 11.1 What is Asset Inventory?

### 11.2 Why Asset Inventory is Important

### 11.3 Servers

### 11.4 Workstations

### 11.5 Laptops

### 11.6 Hostname and IP Address

### 11.7 Operating System

### 11.8 Asset Owner

### 11.9 Asset Purpose

### 11.10 Asset Location

### 11.11 Asset Criticality

### 11.12 Asset Inventory Sources

### 11.13 AD, SIEM, EDR, MDM, and CMDB

---

## Module 12: Threat Intelligence and Lookups

### 12.1 What is Threat Intelligence?

### 12.2 Why SOC L1 Uses Threat Intelligence

### 12.3 IP Reputation Lookup

### 12.4 Domain Reputation Lookup

### 12.5 URL Reputation Lookup

### 12.6 File Hash Lookup

### 12.7 GeoIP Lookup

### 12.8 ASN and ISP Lookup

### 12.9 VPN, Proxy, and Tor Detection

### 12.10 Threat Intelligence Limitations

### 12.11 Using TI in Alert Verdicts

---

## Module 13: Network Diagrams for SOC Analysts

### 13.1 What is a Network Diagram?

### 13.2 Why Network Diagrams Matter

### 13.3 Firewall Placement

### 13.4 VPN Subnet

### 13.5 Office Subnet

### 13.6 Database Subnet

### 13.7 DMZ Network

### 13.8 Public Services

### 13.9 Internal Services

### 13.10 Understanding Source and Destination IPs

### 13.11 Understanding NAT and IP Translation

### 13.12 Attack Path Reconstruction

### 13.13 VPN Brute Force Scenario

### 13.14 Internal Network Scanning Scenario

---

## Module 14: SOC Workbooks, Playbooks, Runbooks, and Workflows

### 14.1 What is a Playbook?

### 14.2 What is a Runbook?

### 14.3 What is a Workflow?

### 14.4 What is a Workbook?

### 14.5 Difference Between Playbook, Runbook, Workflow, and Workbook

### 14.6 Why L1 Analysts Use Workbooks

### 14.7 Workbook Structure

### 14.8 Enrichment Phase

### 14.9 Investigation Phase

### 14.10 Escalation Phase

### 14.11 Workbook Example: Unusual Login Location

### 14.12 Workbook Example: VPN Brute Force

### 14.13 Workbook Example: Malware Alert

---

## Module 15: Enrichment Process

### 15.1 What is Enrichment?

### 15.2 User Enrichment

### 15.3 Host Enrichment

### 15.4 IP Enrichment

### 15.5 Domain and URL Enrichment

### 15.6 Threat Intelligence Enrichment

### 15.7 Identity Inventory Enrichment

### 15.8 Asset Inventory Enrichment

### 15.9 Enrichment Checklist

### 15.10 Enrichment Output for Investigation

---

## Module 16: SIEM Investigation for SOC L1

### 16.1 SIEM Search Basics

### 16.2 Searching by Username

### 16.3 Searching by Hostname

### 16.4 Searching by Source IP

### 16.5 Searching by Destination IP

### 16.6 Searching by Time Range

### 16.7 Searching by File Hash

### 16.8 Searching by Process Name

### 16.9 Searching by Command Line

### 16.10 Correlating Multiple Logs

### 16.11 Login Logs

### 16.12 VPN Logs

### 16.13 Firewall Logs

### 16.14 Endpoint Logs

### 16.15 Email Logs

---

## Module 17: Common SOC L1 Alert Scenarios

### 17.1 Unusual Login Location

### 17.2 Impossible Travel

### 17.3 Multiple Failed Login Attempts

### 17.4 VPN Brute Force

### 17.5 Successful Login After Brute Force

### 17.6 Suspicious PowerShell Execution

### 17.7 Malware Detection

### 17.8 Phishing Email

### 17.9 Suspicious File Download

### 17.10 Data Exfiltration

### 17.11 RDP Brute Force

### 17.12 Internal Port Scanning

### 17.13 Privilege Escalation

### 17.14 Admin Account Abuse

---

## Module 18: Alert Reporting

### 18.1 What is Alert Reporting?

### 18.2 Why L1 Analysts Write Reports

### 18.3 Report Purpose

### 18.4 Report Quality Standards

### 18.5 Five Ws Reporting Method

### 18.6 Who

### 18.7 What

### 18.8 When

### 18.9 Where

### 18.10 Why

### 18.11 Evidence Summary

### 18.12 Final Verdict Explanation

### 18.13 Report Template

### 18.14 Good Report vs Bad Report

### 18.15 Report Writing Practice

---

## Module 19: Alert Escalation

### 19.1 What is Escalation?

### 19.2 Why Escalation is Important

### 19.3 When to Escalate to L2

### 19.4 True Positive Escalation

### 19.5 Suspicious Alert Escalation

### 19.6 Critical Alert Escalation

### 19.7 Malware Escalation

### 19.8 Account Compromise Escalation

### 19.9 Sensitive Asset Escalation

### 19.10 Escalation Steps

### 19.11 Assigning Alert to L2

### 19.12 Notifying L2

### 19.13 Escalation Message Format

### 19.14 Requesting Senior Support

### 19.15 Escalation Mistakes to Avoid

---

## Module 20: SOC Communication

### 20.1 Communication in SOC

### 20.2 Communication with L2 Analyst

### 20.3 Communication with SOC Manager

### 20.4 Communication with IT Team

### 20.5 Communication with HR Team

### 20.6 Communication with User

### 20.7 Communication During Critical Alerts

### 20.8 Emergency Contact Process

### 20.9 What to Do if L2 is Unavailable

### 20.10 Safe User Verification

### 20.11 Avoiding Compromised Communication Channels

### 20.12 Shift Handover Communication

### 20.13 Incident Communication Basics

---

## Module 21: SOC Metrics and Objectives

### 21.1 SOC Objectives

### 21.2 Why Metrics Matter

### 21.3 Alerts Count

### 21.4 False Positive Rate

### 21.5 Alert Escalation Rate

### 21.6 Threat Detection Rate

### 21.7 Metric Formulas

### 21.8 Healthy Alert Volume

### 21.9 Alert Noise

### 21.10 Alert Fatigue

### 21.11 SOC Reliability

### 21.12 L1 Analyst Performance Metrics

---

## Module 22: SLA, MTTD, MTTA, and MTTR

### 22.1 What is SLA?

### 22.2 SOC Team Availability

### 22.3 8/5 SOC Model

### 22.4 24/7 SOC Model

### 22.5 Mean Time to Detect

### 22.6 Mean Time to Acknowledge

### 22.7 Mean Time to Respond

### 22.8 MTTD Formula

### 22.9 MTTA Formula

### 22.10 MTTR Formula

### 22.11 Critical Alert SLA

### 22.12 SLA Breach

### 22.13 SLA Example Scenarios

---

## Module 23: Improving SOC Metrics as an L1 Analyst

### 23.1 Why L1 Analysts Should Care About Metrics

### 23.2 Improving False Positive Rate

### 23.3 Detection Rule Tuning Feedback

### 23.4 False Positive Remediation

### 23.5 Improving MTTD

### 23.6 Improving MTTA

### 23.7 Improving MTTR

### 23.8 Faster Alert Acknowledgement

### 23.9 Faster Escalation

### 23.10 Better Report Writing

### 23.11 Better Alert Prioritisation

### 23.12 Using Automation

### 23.13 Using SOAR

### 23.14 Improving Workbook Quality

---

## Module 24: Beginner Practical Labs

### 24.1 Lab: Identify Alert Properties

### 24.2 Lab: Classify Alert Severity

### 24.3 Lab: Identify Event vs Alert

### 24.4 Lab: Basic SIEM Search

### 24.5 Lab: User Lookup

### 24.6 Lab: Host Lookup

### 24.7 Lab: IP Reputation Lookup

### 24.8 Lab: True Positive vs False Positive

---

## Module 25: Intermediate Practical Labs

### 25.1 Lab: Unusual Login Investigation

### 25.2 Lab: VPN Brute Force Investigation

### 25.3 Lab: Malware Alert Triage

### 25.4 Lab: Phishing Alert Triage

### 25.5 Lab: Suspicious PowerShell Investigation

### 25.6 Lab: Internal Network Scanning Investigation

### 25.7 Lab: Asset Inventory Based Investigation

### 25.8 Lab: Identity Inventory Based Investigation

### 25.9 Lab: Alert Report Writing

### 25.10 Lab: L2 Escalation Message

---

## Module 26: Advanced SOC L1 Investigation Skills

### 26.1 Advanced Triage Mindset

### 26.2 Alert Correlation

### 26.3 Timeline Reconstruction

### 26.4 Attack Chain Understanding

### 26.5 Initial Access Identification

### 26.6 Reconnaissance Detection

### 26.7 Lateral Movement Indicators

### 26.8 Privilege Abuse Indicators

### 26.9 Data Exfiltration Indicators

### 26.10 Compromised Account Indicators

### 26.11 Compromised Host Indicators

### 26.12 High-Quality Escalation

---

## Module 27: Capstone Project

### 27.1 Capstone Scenario Overview

### 27.2 Alert Review

### 27.3 Enrichment

### 27.4 SIEM Investigation

### 27.5 Identity Inventory Lookup

### 27.6 Asset Inventory Lookup

### 27.7 Network Diagram Review

### 27.8 Timeline Creation

### 27.9 Verdict Selection

### 27.10 Alert Report Writing

### 27.11 Escalation Decision

### 27.12 Final SOC L1 Case Presentation

---

## Module 28: Final Assessment

### 28.1 Theory Quiz

### 28.2 Alert Properties Test

### 28.3 Verdict Decision Test

### 28.4 SIEM Search Test

### 28.5 Reporting Test

### 28.6 Escalation Test

### 28.7 SOC Metrics Calculation Test

### 28.8 Final Practical Investigation

### 28.9 Course Completion Review

### 28.10 SOC L1 Readiness Checklist
