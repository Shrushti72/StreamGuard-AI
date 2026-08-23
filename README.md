# StreamGuard AI — Live Broadcast Continuity & Incident Supervisor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-Gemini_Enterprise_ADK-4285F4?logo=google-cloud)](https://cloud.google.com/vertex-ai)
[![Grafana Labs Track](https://img.shields.io/badge/Grafana_Labs_Track-Grafana_Cloud_MCP_Server-F46800?logo=grafana)](https://grafana.com/)

**StreamGuard AI** is an autonomous live broadcast continuity supervisor built for the **Google Cloud Agentic Cinema Hackathon (Grafana Labs Track)**.

It acts as an AI Technical Director during live entertainment events (premiere livestreams, esports tournaments, concerts, awards shows). It continuously monitors ingest pipelines, transcode nodes, Loki logs, and CDN egress metrics via the **official Grafana Cloud MCP Server (`grafana/mcp-grafana`)**, auto-correlates multi-signal anomalies, opens Grafana incidents, and narrates SRE telemetry in plain language for Studio Heads and Executive Producers.

---

## 🌟 Grafana Labs Partner Track Integration & Architecture

```
                                  ┌─────────────────────────────────────────────────────────────┐
                                  │            StreamGuard Director Console UI                  │
                                  │             (Deployed on Google Cloud Run)                  │
                                  └───────────────┬─────────────────────────────┬───────────────┘
                                                  │                             │
                                                  ▼                             ▼
┌──────────────────────────────────────────────────┐         ┌──────────────────────────────────────────────────┐
│      Google Cloud Gemini ADK Agents              │         │        Official Grafana Cloud MCP Server         │
│   (google-genai / google-cloud-aiplatform)       │<───────>│               (grafana/mcp-grafana)              │
├──────────────────────────────────────────────────┤         ├──────────────────────────────────────────────────┤
│ • Signal Correlation & Anomaly Engine            │         │ • query_prometheus_metrics (PromQL)              │
│ • SRE-to-Executive Plain Language Translator    │         │ • query_loki_logs (LogQL)                        │
│ • Automatic Severity & Root Cause Analyzer       │         │ • create_grafana_incident (Incident API)         │
│ • Action Recommendation Generator                │         │ • annotate_grafana_dashboard (Event Marker)      │
└──────────────────────────────────────────────────┘         └──────────────────────────────────────────────────┘
```

### 1. Grafana Cloud MCP Server Integration (`backend/app/mcp/`)
Submissions to the Grafana Labs track must demonstrate active runtime usage of the **Grafana Cloud MCP Server (`grafana/mcp-grafana`)**:
- **PromQL Metrics Querying (`query_prometheus_metrics`)**: Fetches live ingest CPU load, transcode queue depth, CDN bandwidth, and viewer buffer ratios.
- **LogQL Log Analysis (`query_loki_logs`)**: Inspects 5xx HTTP gateway timeouts and transcode drop-frame stack traces.
- **Incident Automation (`create_grafana_incident`)**: Opens official Grafana incidents automatically when critical threshold breaches occur.
- **Dashboard Annotations (`annotate_grafana_dashboard`)**: Places event markers directly on live Grafana dashboards.

### 2. Google Cloud Gemini Enterprise ADK (`backend/app/agents/`)
Powered by Google Cloud SDKs (`google-genai` & `google-cloud-aiplatform`):
- **Gemini 2.5 Flash / 3 Pro**: Correlates multi-signal telemetry (e.g. Origin CPU Spike $\rightarrow$ Transcode Queue Buildup $\rightarrow$ Viewer Buffering 4 mins later).
- **Plain-Language Executive Translator**: Converts complex graphs into clear alerts:
  > *"🚨 Executive Alert: Origin server CPU spiked to 98% in US-East. In ~4 minutes, 18% of Northeast viewers will experience buffering. Scaling Cloud Run transcode worker pods now."*

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
git clone https://github.com/your-username/streamguard-ai.git
cd streamguard-ai

pip install -r requirements.txt
```

### 2. Deploy to Google Cloud Run
Run the included deployment script:
```bash
chmod +x .gcp/deploy.sh
./.gcp/deploy.sh
```

### 3. Access the Live Dashboard
Open your Google Cloud Run service URL (e.g. `https://streamguard-ai-xxxx-uc.a.run.app`).

---

## 🎥 3-Minute Demo Video Blueprint

1. **Problem (0:00 - 0:45)**: Live broadcast buffering during a movie premiere—showing complex SRE Grafana graphs that non-technical Studio Heads cannot interpret under pressure.
2. **Grafana Cloud MCP Server Integration (0:45 - 1:30)**: Show how Gemini ADK calls `grafana/mcp-grafana` tools (`query_prometheus_metrics`, `query_loki_logs`).
3. **Live Anomaly Simulation (1:30 - 2:30)**:
   - Click "🚨 Ingest CPU Spike (98%)".
   - Show StreamGuard AI auto-correlating metrics, opening a Grafana incident, annotating the dashboard, and delivering a plain-language executive alert.
4. **Closing (2:30 - 3:00)**: Show Google Cloud Run live hosting URL and open-source GitHub repository.

---

## 📄 License
This project is open-source software licensed under the [MIT License](LICENSE).
