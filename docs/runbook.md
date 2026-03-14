# 🏦 NBFC Patch Health Monitor — Runbook

## Document Info
| Field | Details |
|-------|---------|
| Version | 1.0 |
| Author | Nitin |
| Last Updated | March 2026 |
| Classification | Internal Use Only |
| Compliance | RBI IT Framework |

---

## 1. Purpose
This runbook provides step-by-step instructions to deploy and run the NBFC Post-Patch Health Monitor in a production environment (office VDI / jump server) after every ManageEngine patch cycle.

---

## 2. Problem Statement
Post OS patching, Windows app servers frequently:
- Drop from Azure Active Directory domain silently
- Show high CPU / memory usage
- Have critical services stopped
- Cause app downtime that is only discovered when users complain

This tool automates post-patch validation across all app servers and generates an audit-ready report.

---

## 3. Architecture
```
VDI / Jump Server
      │
      ▼
Health Checker (Python)
      │
      ├──── SSH/WMI ──▶ APPWIN01 (check domain, CPU, memory, services)
      ├──── SSH/WMI ──▶ APPWIN02 (check domain, CPU, memory, services)
      └──── SSH/WMI ──▶ APPWIN03 (check domain, CPU, memory, services)
                              │
                              ▼
                    JSON audit trail + HTML report
                              │
                              ▼
                    Email to team / manager
```

---

## 4. Prerequisites

### On VDI / Jump Server:
- Python 3.8+
- Git
- Network access to app servers (ports 80, 443, WMI)
- Read-only credentials for app servers

### Install dependencies:
```bash
git clone https://github.com/nitin020997/patch-health-monitor
cd patch-health-monitor
pip3 install -r health-checker/requirements.txt
```

---

## 5. Configuration

Edit `health-checker/config.ini` with real server details:
```ini
[servers]
appwin01 = 10.0.1.45
appwin02 = 10.0.1.46
appwin03 = 10.0.1.47

[thresholds]
cpu_critical = 85
memory_critical = 85

[domain]
expected_domain = CORP.NBFC.LOCAL

[alerts]
teams_webhook = https://your-org.webhook.office.com/xxxxx
smtp_host = smtp.office365.com
smtp_port = 587
smtp_user = devops@nbfc.com
alert_recipients = manager@nbfc.com,windowsadmin@nbfc.com
```

---

## 6. Running the Tool

### Step 1 — Run health checks:
```bash
cd patch-health-monitor
python3 health-checker/checker.py
```

### Step 2 — Generate report:
```bash
python3 reports/generate.py
```

### Step 3 — Open report:
```bash
# On Windows VDI
start reports/health_report.html

# On Linux jump server
xdg-open reports/health_report.html
```

### Step 4 — Share report:
Email `reports/health_report.html` to your manager and team.

---

## 7. Interpreting the Report

| Status | Meaning | Action |
|--------|---------|--------|
| ✅ HEALTHY | All checks passed | No action needed |
| ⚠️ WARNING | CPU/Memory high | Monitor closely |
| ❌ CRITICAL | Domain dropped or unreachable | Immediate action |

### Domain Drop (Most Critical):
```
Symptom  → Domain Status shows "DROPPED"
Impact   → Users cannot authenticate to app
Action   → Immediately notify Windows AD admin
           Server needs to be rejoined to domain
           Reference: AD team runbook section 4.2
```

### High CPU/Memory:
```
Symptom  → CPU > 85% or Memory > 85%
Impact   → App performance degraded
Action   → Check which process is consuming resources
           Restart app service if needed
           Escalate to app team if persists
```

---

## 8. Scheduling (Post Patch Automation)

Schedule the tool to run automatically after ManageEngine patch window:

### Linux / Mac (cron):
```bash
crontab -e

# Run at 3am every Sunday (after patch window)
0 3 * * 0 cd /opt/patch-health-monitor && python3 health-checker/checker.py && python3 reports/generate.py
```

### Windows (Task Scheduler):
```
Action    → python3 health-checker/checker.py
Schedule  → After patch maintenance window
User      → Service account with read access
```

---

## 9. Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Server shows UNREACHABLE | Firewall blocking | Check SG / firewall rules on port 80 |
| Domain check always true | WMI not configured | Enable WMI on target servers |
| Report not generating | Wrong file path | Check config.ini paths |
| Email not sending | SMTP blocked | Use Teams webhook instead |

---

## 10. RBI Audit Evidence

This tool generates the following audit artifacts:

| Artifact | Location | Retention |
|----------|----------|-----------|
| Raw health data | `reports/health_results.json` | 1 year |
| HTML report | `reports/health_report.html` | 1 year |
| Tool source code | GitHub | Permanent |

These artifacts demonstrate:
- ✅ Post-patch validation process exists
- ✅ Automated monitoring in place
- ✅ Incident detection capability
- ✅ Audit trail maintained

---

## 11. Contact

| Role | Responsibility |
|------|---------------|
| DevOps Engineer (Nitin) | Tool owner, report generation |
| Windows AD Admin | Domain rejoin on CRITICAL alerts |
| App Team | Service restart on HIGH resource alerts |

---

*This document is confidential and for internal use only.*
*Maintained by DevOps Team | RBI IT Framework Compliant*