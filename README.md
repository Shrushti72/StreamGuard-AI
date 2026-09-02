# StreamGuard AI — Live Broadcast Continuity & Incident Supervisor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-Gemini_Enterprise_ADK-4285F4?logo=google-cloud)](https://cloud.google.com/vertex-ai)
[![Grafana Labs Track](https://img.shields.io/badge/Grafana_Labs_Track-Grafana_Cloud_MCP_Server-F46800?logo=grafana)](https://grafana.com/)

# 🎬 StreamGuard AI

### Agentic AI Reliability Supervisor for Cinema & Video Streaming

StreamGuard AI is an **agentic AI reliability and continuity supervisor for cinema and video-streaming platforms**.

It uses **Google Agent Development Kit (ADK)** and **Gemini** to autonomously investigate streaming health by combining real-time observability data from **Grafana Cloud** with event-stream data from **Confluent Kafka**.

Instead of simply displaying dashboards and alerts, StreamGuard investigates the evidence, correlates signals across systems, identifies likely causes of streaming degradation, and provides actionable recommendations.

---

## 🎯 The Problem

A cinema or video-streaming platform can experience:

* Viewer buffering and playback freezes
* High transcoding latency
* Dropped video frames
* Increased playback errors
* Origin or infrastructure saturation
* Regional service degradation
* Streaming pipeline incidents

Traditional monitoring systems can expose these signals, but engineers still have to manually investigate:

> **What is happening? Why is it happening? How severe is it? What evidence supports the diagnosis? What should we do next?**

StreamGuard AI acts as an **AI operations supervisor** that performs this investigation automatically.

---

## 💡 The Solution

A user can ask the StreamGuard agent:

> **"Check the current streaming health and investigate any active degradation."**

The agent autonomously:

1. Investigates infrastructure telemetry through Grafana MCP.
2. Examines logs, metrics, and incidents.
3. Inspects relevant Kafka topics through Confluent MCP.
4. Consumes relevant event data.
5. Correlates evidence across observability and event-stream systems.
6. Determines the severity and impact.
7. Identifies likely causes based only on retrieved evidence.
8. Clearly distinguishes verified facts from hypotheses.
9. Produces recommended corrective actions.

---

## 🧠 Why It Is Agentic

StreamGuard is not simply an AI-powered dashboard.

The **Google ADK agent decides which information it needs and uses connected MCP tools to investigate the system**.

```text
                    User
                     │
                     ▼
            Google ADK Web UI
                     │
                     ▼
          My_agent_StreamGuard_AI
                     │
              Gemini Reasoning
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
    Grafana MCP          Confluent MCP
          │                     │
          ▼                     ▼
 Prometheus + Loki        Kafka Topics
 Incidents + Metrics      Events + Messages
          │                     │
          └──────────┬──────────┘
                     ▼
             Evidence Correlation
                     │
                     ▼
          Streaming Health Analysis
                     │
                     ▼
       Root-Cause Hypothesis + Actions
```

---

## 🔌 MCP Integrations

### Grafana MCP

Grafana provides the agent with real observability information including:

* Prometheus metrics
* Loki logs
* Streaming telemetry
* Incidents
* Dashboards and operational signals

Example signals include:

```text
CPU utilization
Buffering ratio
Transcoding latency
Dropped frames
Error rate
Origin/transcoder logs
```

### Confluent Kafka MCP

Confluent provides access to the streaming event pipeline.

The agent can inspect and consume relevant Kafka topics such as:

```text
stream-health
continuity-alerts
broadcast-incidents
streamguard-events
```

This gives StreamGuard a second source of operational evidence beyond infrastructure monitoring.

---

## 🔎 Evidence-Based Investigation

A key design principle is:

> **Do not invent telemetry.**

The agent is instructed to distinguish between:

### Verified evidence

Information directly returned by Grafana or Kafka.

### Derived observations

Patterns that can be established from multiple retrieved signals.

### Hypotheses

Possible root causes that require further validation.

For example, if Kafka provides an event without a `region` field, StreamGuard does **not** invent a regional association.

This makes the resulting investigation more trustworthy and auditable.

---

## 🎬 Example Investigation

During testing, StreamGuard correlated real data from both systems.

Grafana telemetry showed severe periodic degradation including:

```text
CPU utilization       > 95%
Buffering ratio       ~5–8+
Transcoding latency   ~700–900 ms+
Dropped frames        hundreds per interval
Error rate            significantly elevated
```

Grafana Loki logs independently showed origin/transcoding warnings.

Confluent Kafka also provided a historical `stream-health` event:

```json
{
  "event": "stream_health",
  "status": "healthy",
  "stream": "main-broadcast",
  "cpu": 42,
  "buffering_ratio": 0.3
}
```

The agent correctly treated this as a historical system-level observation and did not claim regional correlation because the Kafka event contained no `region` or `region_id`.

The agent then identified a **likely recurring origin/transcoding bottleneck** based on the synchronized periodic telemetry.

> Root-cause explanations produced by the agent are treated as hypotheses unless directly supported by retrieved evidence.

---

## ☁️ Google Cloud Architecture

The application is deployed on **Google Cloud Run**.

```text
Google Cloud Run
       │
       ▼
Google ADK Web
       │
       ▼
StreamGuard Agent
       │
       ├── Gemini / Vertex AI
       │
       ├── Grafana MCP
       │      ├── Prometheus
       │      ├── Loki
       │      └── Incidents
       │
       └── Confluent MCP
              └── Kafka
```

The final judge-facing interface is the **actual Google ADK Web UI**, allowing judges to see the agent's events, tool usage, traces, and reasoning workflow.

---

## 🛠️ Technology Stack

| Technology            | Purpose                  |
| --------------------- | ------------------------ |
| Google ADK            | Agent orchestration      |
| Gemini                | Agent reasoning          |
| Vertex AI             | Gemini execution         |
| Grafana MCP           | Observability access     |
| Prometheus            | Metrics                  |
| Loki                  | Logs                     |
| Confluent MCP         | Kafka integration        |
| Apache Kafka          | Event streaming          |
| Google Cloud Run      | Hosted agent application |
| Google Secret Manager | Runtime credentials      |
| Python                | Agent implementation     |

---

## 🚀 Live Demo

**StreamGuard AI — Google ADK Web**

https://streamguard-ai-hgoh7ql2ta-uc.a.run.app

The deployed application runs the real StreamGuard agent on Google Cloud Run.

---

## 📁 Project Structure

```text
StreamGuard-AI/
│
├── backend/
│   ├── app/
│   │   └── adk_agent_engine/
│   │       ├── agent.py
│   │       ├── real_runner.py
│   │       └── deploy_vertex_agent_engine.py
│   │
│   └── main.py
│
├── streamguard_agent/
│   └── agent.py
│
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
│
├── .gcp/
│   └── deploy.sh
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🔐 Security & Credentials

Runtime credentials are not hardcoded in the application.

The deployment uses Google Secret Manager for:

```text
GRAFANA_URL
GRAFANA_SERVICE_ACCOUNT_TOKEN
CONFLUENT_API_KEY
CONFLUENT_API_SECRET
```

The Cloud Run service account is granted the required Google Cloud permissions for:

* Vertex AI
* Agent Registry
* Secret Manager

---

## 🧪 Current Status

### Verified

* ✅ Google ADK Web UI running on Cloud Run
* ✅ Gemini / Vertex AI integration
* ✅ Google Agent Registry integration
* ✅ Grafana MCP integration
* ✅ Prometheus telemetry retrieval
* ✅ Loki log retrieval
* ✅ Grafana incident analysis
* ✅ Confluent Kafka MCP integration
* ✅ Kafka topic inspection
* ✅ Kafka message consumption
* ✅ Multi-source evidence correlation
* ✅ Evidence-based health investigation
* ✅ Live Cloud Run deployment

---

## 🏆 Project Vision

StreamGuard AI aims to move streaming operations from:

> **Monitor → Alert → Human investigates**

to:

> **Monitor → Investigate → Correlate → Explain → Recommend**

The long-term vision is an autonomous AI reliability layer for digital cinema and video-streaming platforms that can continuously investigate streaming health and assist engineering teams before viewer experience is significantly impacted.

---

## 📌 Project Status

**Working prototype / hackathon implementation**

Current deployed revision:

```text
streamguard-ai-00015-2p4
```

Latest GitHub implementation:

```text
649dab5
```

---

## 👩‍💻 Built With

Built as an **Agentic Cinema** project using Google Cloud, Google ADK, Gemini, Grafana MCP, and Confluent Kafka MCP.

This project is open-source software licensed under the [MIT License](LICENSE).
