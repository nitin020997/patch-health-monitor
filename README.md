# 🏦 NBFC Post-Patch Health Monitor

> Automatically validate server health after every patch cycle and generate an audit-ready report — no manual checking, no guesswork.

Built for regulated environments (RBI compliant NBFC infrastructure) where post-patch failures cause silent downtime and manual validation is error-prone.

---

## 🚨 Problem This Solves

| Before | After |
|--------|-------|
| Patch runs at night | Patch runs at night |
| App breaks silently | Tool detects issue at 2:01am |
| Users complain at 9am | Alert fired before business hours |
| Manual SSH into each server | Automated check across all servers |
| No audit trail | JSON + HTML report generated automatically |
| RBI audit asks for evidence | 6 months of timestamped reports ready |

---

## 🔍 What It Checks

- ✅ Server reachability (ping)
- ✅ Azure AD domain join status (catches "domain chhodna" 😄)
- ✅ CPU usage threshold (alerts if >85%)
- ✅ Memory usage threshold (alerts if >85%)
- ✅ Critical service status
- ✅ App port responsiveness

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────────┐
│           NBFC Network / Local Mac           │
│                                             │
│  ┌──────────────┐    ┌──────────────────┐   │
│  │Health Checker│───▶│  APPWIN01 ✅     │   │
│  │  (Python)    │───▶│  APPWIN02 ❌     │   │
│  │              │───▶│  APPWIN03 ✅     │   │
│  └──────┬───────┘    └──────────────────┘   │
│         │                                   │
│         ▼                                   │
│  ┌──────────────┐    ┌──────────────────┐   │
│  │  JSON Report │    │   HTML Report    │   │
│  │  (audit log) │    │  (for manager)   │   │
│  └──────────────┘    └──────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## 🚀 Run Locally (Mac)
```bash
# Clone
git clone https://github.com/nitin020997/patch-health-monitor
cd patch-health-monitor

# Run everything
docker compose up --build

# Generate HTML report
python3 reports/generate.py

# Open report
open reports/health_report.html
```

---

## 🏢 Deploy at Office (Production)

1. Pull repo on your VDI / jump server
2. Update `health-checker/config.ini` with real server IPs:
```ini
[servers]
appwin01 = 10.0.1.45
appwin02 = 10.0.1.46
appwin03 = 10.0.1.47

[thresholds]
cpu_critical = 85
memory_critical = 85

[alerts]
teams_webhook = https://your-org.webhook.office.com/...
smtp_host = smtp.office365.com
smtp_port = 587
```

3. Run checker:
```bash
python3 health-checker/checker.py
python3 reports/generate.py
```

4. Schedule it post-patch via cron:
```bash
# Run health check at 3am after patch window
0 3 * * 0 cd /opt/patch-monitor && python3 health-checker/checker.py
```

---

## 📁 Project Structure
```
patch-health-monitor/
├── servers/
│   ├── appwin01/     # Healthy server simulation
│   ├── appwin02/     # Domain dropped simulation ❌
│   └── appwin03/     # Healthy server simulation
├── health-checker/
│   ├── checker.py    # Main health check logic
│   └── config.ini    # Server config (swap for prod)
├── reports/
│   ├── generate.py   # HTML report generator
│   ├── health_results.json  # Raw audit trail
│   └── health_report.html   # Human readable report
├── alerts/
│   └── alert.py      # Email / Teams alerting
└── docker-compose.yml
```

---

## 🔒 RBI Compliance Notes

- All health checks are **read-only** — no changes made to servers
- Every check generates a **timestamped JSON audit trail**
- HTML reports are **retained per run** for audit evidence
- Domain drop detection covers the most common post-patch failure in Windows environments
- Designed for **ap-south-1 (Mumbai)** region — RBI data residency compliant

---

## 🛣️ Roadmap

- [ ] Microsoft Teams webhook alerts
- [ ] Email alerts via SMTP
- [ ] Prometheus metrics export
- [ ] Grafana dashboard
- [ ] Kubernetes deployment
- [ ] Auto-schedule post ManageEngine patch cycle

---

## 🧰 Tech Stack

Python • Docker • Flask • GitHub Actions (coming soon)

---

*Built by a DevOps engineer who got tired of manually checking servers after every patch cycle.* 😄