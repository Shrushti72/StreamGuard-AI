# StreamGuard AI — Live Broadcast Continuity & Incident Supervisor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-Gemini_Enterprise_ADK-4285F4?logo=google-cloud)](https://cloud.google.com/vertex-ai)
[![Grafana Labs Track](https://img.shields.io/badge/Grafana_Labs_Track-Grafana_Cloud_MCP_Server-F46800?logo=grafana)](https://grafana.com/)

# 🎬 StreamGuard AI

## Agentic AI Reliability Supervisor for Cinema & Video Streaming

StreamGuard AI is an **agentic AI reliability and continuity supervisor for cinema, OTT, and video-streaming platforms**.

It investigates streaming degradation by autonomously correlating **Grafana Cloud observability data** with **Confluent Kafka event streams**, using **Google Agent Development Kit (ADK)** and **Gemini** to reason over operational evidence.

Instead of requiring engineers to manually inspect dashboards, logs, alerts, incidents, and event streams, StreamGuard AI performs a multi-source investigation and produces an evidence-based operational report.

It helps answer:

> **What is failing? Where is it failing? What evidence supports the diagnosis? What might be causing it? How many viewers could be affected? What should the operator investigate next?**

StreamGuard AI can also record operational incident context back into Grafana through annotations and provides **Grafana Agent Observability** for monitoring the AI agent itself.

---

## 🚀 Live Demo

### Hosted Application

**Google Cloud Run**

https://streamguard-ai-793289044855.us-central1.run.app/dev-ui/?app=streamguard_agent

### Source Code

https://github.com/Shrushti72/StreamGuard-AI

---

# 🎯 The Problem

Modern cinema and OTT platforms depend on complex streaming pipelines involving:

- Content ingest
- Transcoding
- Origin infrastructure
- CDN delivery
- Regional edge infrastructure
- Playback services
- Event-streaming systems

During a major movie premiere, live cinema event, or high-traffic streaming release, infrastructure problems can quickly become viewer-facing incidents.

Typical symptoms include:

- Playback buffering
- Stream freezes
- Dropped frames
- High transcoding latency
- CPU saturation
- Playback errors
- Regional degradation
- Incorrect alert routing
- Inconsistent telemetry between systems

Traditional observability platforms provide the telemetry, but engineers still have to manually correlate information across multiple systems.

The real operational question is not simply:

> "Is CPU high?"

It is:

> **"Is the streaming experience degrading, where is it happening, what evidence explains it, and what should we do next?"**

---

# 💡 The Solution

StreamGuard AI acts as an **AI-powered streaming reliability investigator**.

An operator can provide a high-level request such as:

```text
Investigate the current streaming health and identify the most likely cause.
```

The agent autonomously investigates the available observability and event-streaming data and correlates the evidence before producing a final report.

The workflow combines:

```text
Operator Request
       ↓
StreamGuard AI
       ↓
Google ADK + Gemini
       ↓
┌───────────────────────┬───────────────────────┐
│                       │
▼                       ▼
Grafana MCP             Confluent MCP
│                       │
▼                       ▼
Metrics + Logs          Kafka Events
Incidents + Alerts      Topics + Schemas
│                       │
└───────────┬───────────┘
            ↓
    Evidence Correlation
            ↓
     Root Cause Analysis
            ↓
 Streaming Impact + Actions
```

---

# 🧠 Core Capabilities

## 1. Agentic Investigation

The operator provides a high-level goal instead of manually specifying individual dashboards, queries, or data sources.

StreamGuard AI determines which available tools and sources are relevant to the investigation.

---

## 2. Grafana Observability Investigation

Through **Grafana Cloud MCP**, StreamGuard AI can investigate:

- Prometheus metric names
- Prometheus labels
- Prometheus metric values
- Loki labels
- Loki logs
- Datasource information
- Alert groups
- Grafana incidents
- Incident details

The agent can dynamically discover available telemetry and investigate the signals relevant to the current problem.

---

## 3. Confluent Kafka Investigation

Through **Confluent MCP**, StreamGuard AI investigates the event-streaming layer.

The agent can:

- Discover Kafka topics
- Inspect schema subjects
- Consume Kafka messages
- Analyze stream-health events
- Compare Kafka events with Grafana observations

Example topics used by StreamGuard AI include:

```text
stream-health
continuity-alerts
broadcast-incidents
streamguard-events
```

---

# 🔗 Multi-Source Correlation

A key capability of StreamGuard AI is correlating evidence across monitoring and event-streaming systems.

Instead of looking at isolated metrics, the agent can reason across a chain such as:

```text
CPU Saturation
      ↓
Transcoding Latency
      ↓
Dropped Frames
      ↓
Viewer Buffering
      ↓
Playback Degradation
```

The agent can then compare these observations against Kafka stream-health events and other operational telemetry.

This creates a unified investigation instead of requiring engineers to inspect Grafana and Kafka independently.

---

# 🔎 Evidence-Based Reasoning

StreamGuard AI is designed to avoid presenting assumptions as confirmed telemetry.

Each investigation separates information into three levels.

### ✅ Verified Evidence

Facts directly returned by Grafana or Confluent tools.

Example:

```text
CPU utilization exceeded 90%.
Transcoding latency exceeded 700 ms.
Dropped frames increased during degradation.
```

### 🔎 Derived Observations

Patterns obtained by correlating multiple verified observations.

Example:

```text
CPU spikes coincide with increased transcoding latency,
frame drops, and elevated viewer buffering.
```

### ⚠️ Hypotheses

Possible explanations that require additional investigation.

Example:

```text
The recurring CPU pattern may indicate a background
process competing with the transcoding workload.
```

This separation makes the investigation more transparent and defensible.

---

# 🌎 Regional Correlation Safety

StreamGuard AI does not invent regional relationships when the available telemetry does not contain the required fields.

For example, a Kafka event may contain:

```json
{
  "event": "stream_health",
  "status": "healthy",
  "stream": "main-broadcast",
  "cpu": 42,
  "buffering_ratio": 0.3
}
```

If the event does not contain:

```text
region
region_id
```

the agent does not claim that the event belongs to a particular region.

Instead, it explicitly states that direct regional correlation is not possible for that event.

This prevents unsupported conclusions from being presented as operational facts.

---

# 📊 Example Investigation

A StreamGuard AI investigation can identify a pattern such as:

```text
CPU utilization       → >90%
Transcoding latency   → >700 ms
Dropped frames        → elevated
Buffering             → severe
Playback errors       → elevated
```

The agent can then organize the investigation into:

### Verified Evidence

```text
Repeated CPU saturation coincides with
increased transcoding latency and frame drops.
```

### Derived Observation

```text
Transcoding resource pressure appears to propagate
into playback-quality degradation.
```

### Hypothesis

```text
A recurring background process may be competing
with the transcoding workload.
```

### Recommended Operator Actions

```text
1. Profile the affected workload.
2. Inspect recurring jobs and background processes.
3. Review container CPU allocation.
4. Audit alert-routing rules.
```

The system provides operator-oriented recommendations rather than blindly executing destructive production changes.

---

# ✍️ Grafana Write-Back

StreamGuard AI is not limited to read-only observability.

When operational context should be recorded, the agent can create a **Grafana annotation through the Grafana MCP integration**.

This enables a closed-loop workflow:

```text
Observe
   ↓
Investigate
   ↓
Correlate
   ↓
Reason
   ↓
Recommend
   ↓
Record operational context in Grafana
```

Grafana therefore acts as both:

- A source of operational evidence
- A destination for investigation context

This creates a practical **bidirectional Grafana workflow**.

---

# 🤖 Multi-Agent Architecture

StreamGuard AI uses specialized Google ADK agents.

## Root Agent

The root agent coordinates the overall investigation.

Responsibilities:

- Understand the operator request
- Delegate investigation tasks
- Coordinate specialized agents
- Combine evidence
- Produce the final investigation report

---

## Broadcast Monitoring Agent

The Grafana-focused agent specializes in streaming observability.

Responsibilities include:

- Prometheus metrics
- Prometheus labels
- Loki logs
- Grafana incidents
- Alert groups
- Datasource information
- Operational annotations

---

## Event Streaming Agent

The Confluent-focused agent specializes in event-streaming telemetry.

Responsibilities include:

- Kafka topics
- Kafka schemas
- Kafka messages
- Stream-health events
- Cross-system event correlation

---

# 🧩 System Architecture

```text
                     ┌───────────────────────┐
                     │       Operator        │
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │    StreamGuard AI     │
                     │      Root Agent       │
                     └───────────┬───────────┘
                                 │
                         Google ADK + Gemini
                                 │
                ┌────────────────┴────────────────┐
                │                                 │
                ▼                                 ▼
     ┌────────────────────┐          ┌────────────────────┐
     │ Broadcast           │          │ Event Streaming    │
     │ Monitoring Agent    │          │ Agent              │
     └─────────┬──────────┘          └──────────┬─────────┘
               │                                │
               ▼                                ▼
     ┌────────────────────┐          ┌────────────────────┐
     │ Grafana Cloud MCP  │          │ Confluent MCP      │
     └─────────┬──────────┘          └──────────┬─────────┘
               │                                │
        ┌──────┼───────┐                        │
        ▼      ▼       ▼                        ▼
   Prometheus Loki Incidents                 Kafka
        │      │       │                        │
        └──────┴───────┴──────────┬─────────────┘
                                  │
                                  ▼
                       Evidence Correlation
                                  │
                                  ▼
                       Root Cause Analysis
                                  │
                                  ▼
                    Viewer Impact + Actions
                                  │
                     ┌────────────┴────────────┐
                     ▼                         ▼
              Grafana Annotation       Agent Observability
```

---

# 📈 Agent Observability

StreamGuard AI also makes the **AI agent itself observable** using **Grafana Agent Observability**.

This provides visibility into:

- Conversations
- Model generations
- Model calls
- Tool calls
- Execution flow
- Latency
- Token usage
- Estimated cost

This creates two levels of observability.

### Streaming System Observability

```text
Prometheus
Loki
Grafana Incidents
Confluent Kafka
```

### AI Agent Observability

```text
Gemini generations
ADK execution
MCP tool calls
Latency
Tokens
Estimated cost
```

Together:

```text
              StreamGuard AI
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
   Streaming System      AI Agent System
    Observability         Observability
          │                   │
          ▼                   ▼
 Grafana + Confluent     Agent Observability
          │                   │
          └─────────┬─────────┘
                    ▼
             Operator Insight
```

---

# 🔬 Real Agent Execution

StreamGuard AI has been validated using real Google ADK execution traces.

A real investigation includes execution paths such as:

```text
Root Agent
    ↓
Agent Handoff
    ↓
Broadcast Monitoring Agent
    ↓
Gemini Reasoning
    ↓
Grafana MCP
    ├── list_datasources
    ├── list_prometheus_metric_names
    ├── query_prometheus
    ├── list_prometheus_label_names
    ├── list_prometheus_label_values
    ├── list_loki_label_names
    ├── list_loki_label_values
    ├── query_loki_logs
    ├── list_alert_groups
    ├── list_incidents
    └── get_incident
    ↓
Event Streaming Agent
    ↓
Gemini Reasoning
    ↓
Confluent MCP
    ├── list_kafka_topics
    ├── list_schema_subjects
    └── consume_kafka_messages
    ↓
Evidence Correlation
    ↓
Final Investigation Report
```

This demonstrates that the result is produced through **real agent execution and real MCP tool calls**, rather than a static or hard-coded response.

---

# ☁️ Google Cloud Deployment

StreamGuard AI is hosted on **Google Cloud Run**.

### Production Service

```text
Service:
streamguard-ai

Region:
us-central1
```

### Runtime Architecture

```text
Internet
   ↓
Google Cloud Run
   ↓
Google ADK
   ↓
Gemini
   ├───────────────┐
   ▼               ▼
Grafana MCP    Confluent MCP
```

Sensitive credentials are stored using **Google Cloud Secret Manager** and injected into the Cloud Run runtime.

---

# 🔐 Security

StreamGuard AI does not commit credentials or API tokens to GitHub.

Sensitive credentials are stored using Google Cloud Secret Manager.

Examples include:

```text
Grafana URL
Grafana service account token
Confluent API key
Confluent API secret
Agent Observability token
```

Secrets are injected into the runtime instead of being stored in source code.

**Never commit credentials, API keys, tokens, or passwords to the repository.**

---

# 🛡️ Operational Safety

StreamGuard AI is designed as an **operator-assistance system**, rather than an uncontrolled autonomous remediation engine.

The agent:

- Investigates telemetry
- Correlates evidence
- Explains likely causes
- Estimates impact when supported by data
- Recommends actions
- Records investigation context when appropriate

It does not blindly execute destructive production changes.

This preserves human operational control while reducing investigation time.

---

# 🎬 Cinema & OTT Use Cases

## 🎥 Movie Premieres

Detect and investigate streaming degradation during high-traffic movie releases.

## 📺 OTT Platforms

Identify playback-quality problems across infrastructure and delivery layers.

## 🎞️ Live Cinema Events

Monitor streaming infrastructure and correlate operational events during high-demand events.

## ▶️ On-Demand Video

Investigate transcoding, buffering, frame-drop, and playback-quality degradation.

## 🌎 Regional Streaming

Identify geographically isolated degradation when telemetry contains reliable regional identifiers.

---

# 💬 Example Questions for the Agent

### General Health

```text
Investigate the current streaming health.
```

### Root Cause

```text
What is the most likely root cause of the current degradation?
Separate verified evidence from hypotheses.
```

### Regional Impact

```text
Which regions are experiencing the worst playback quality?
```

### Kafka Correlation

```text
Compare the Kafka stream-health events with Grafana metrics and logs.
Do they tell the same story?
```

### Evidence Validation

```text
Can you prove that the West region is degraded?
Do not rely only on the incident title.
```

### Viewer Impact

```text
Approximately how many viewers could be affected?
Only estimate this if the telemetry supports it.
```

### Grafana Write-Back

```text
What incident context should be recorded back in Grafana?
```

### Agent Observability

```text
What did the agent do during this investigation?
```

---

# 📸 Screenshots

The repository contains screenshots demonstrating the major components of StreamGuard AI.

## 1. StreamGuard AI — ADK Web UI

[StreamGuard AI ADK Web UI](https://chatgpt.com/c/01-adk-web-ui.png)

The StreamGuard AI agent running through the Google ADK Web interface.

---

## 2. Grafana MCP

[Grafana MCP](https://chatgpt.com/c/02-grafana-mcp.png)

StreamGuard AI querying Grafana observability data through MCP.

---

## 3. Confluent Kafka

[Confluent Kafka](https://chatgpt.com/c/03-confluent-kafka.png)

StreamGuard AI discovering Kafka topics and consuming event-stream data through Confluent MCP.

---

## 4. Multi-Source Investigation

[Multi-Source Investigation](https://chatgpt.com/c/04-multi-source-investigation.png)

A real investigation combining Grafana and Confluent evidence.

---

## 5. Google ADK Traces

[Google ADK Traces](https://chatgpt.com/c/05-adk-traces.png)

Real ADK execution showing agent handoffs, Gemini calls, and MCP tool execution.

---

## 6. Grafana Write-Back

[Grafana Write-Back](https://chatgpt.com/c/06-grafana-writeback.png)

StreamGuard AI recording operational investigation context back into Grafana.

---

## 7. Agent Observability

[Grafana Agent Observability](https://chatgpt.com/c/07-agent-observability.png)

Grafana Agent Observability showing model generations, execution telemetry, token usage, and estimated cost.

---

## 8. Architecture

[StreamGuard AI Architecture](https://chatgpt.com/c/08-architecture.png)

End-to-end StreamGuard AI architecture.

---

# 🧪 Validation

The project has been validated across the following components:

| Component | Status |
|---|---|
| Google ADK | ✅ Working |
| Gemini | ✅ Working |
| ADK Web UI | ✅ Working |
| Google Cloud Run | ✅ Deployed |
| Grafana MCP | ✅ Working |
| Prometheus queries | ✅ Working |
| Loki queries | ✅ Working |
| Grafana incidents | ✅ Working |
| Grafana annotations | ✅ Verified |
| Confluent MCP | ✅ Working |
| Kafka topic discovery | ✅ Working |
| Kafka message consumption | ✅ Working |
| Multi-agent investigation | ✅ Working |
| Evidence correlation | ✅ Working |
| Agent Observability | ✅ Working |
| Token tracking | ✅ Working |
| Cost tracking | ✅ Working |
| Agent execution traces | ✅ Working |
| Google Cloud Secret Manager | ✅ Configured |

---

# 📁 Repository Structure

```text
StreamGuard-AI/
│
├── streamguard_agent/
│   └── agent.py
│
├── screenshots/
│   ├── 01-adk-web-ui.png
│   ├── 02-grafana-mcp.png
│   ├── 03-confluent-kafka.png
│   ├── 04-multi-source-investigation.png
│   ├── 05-adk-traces.png
│   ├── 06-grafana-writeback.png
│   ├── 07-agent-observability.png
│   └── 08-architecture.png
│
├── requirements.txt
├── Dockerfile
├── README.md
└── LICENSE
```

---

# ⚙️ Local Development

## Prerequisites

- Python 3.11+
- Google Cloud project
- Gemini / Vertex AI access
- Google ADK
- Grafana Cloud account
- Grafana MCP access
- Confluent Cloud account
- Confluent MCP access

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Credentials

Configure credentials through environment variables or Google Cloud Secret Manager.

### Grafana

```text
GRAFANA_URL
GRAFANA_SERVICE_ACCOUNT_TOKEN
```

### Confluent

```text
CONFLUENT_API_KEY
CONFLUENT_API_SECRET
```

### Agent Observability

```text
AGENTO11Y_ENDPOINT
AGENTO11Y_PROTOCOL
AGENTO11Y_AUTH_MODE
AGENTO11Y_AUTH_TENANT_ID
AGENTO11Y_AUTH_TOKEN
```

**Never commit credentials or tokens to the repository.**

---

## Run Locally

Start the Google ADK Web interface:

```bash
adk web streamguard_agent \
  --host 0.0.0.0 \
  --port 8080
```

For Google Cloud Shell, configure the appropriate Cloud Shell origin using the ADK Web `--allow_origins` option.

---

# 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Google Gemini | Agent reasoning |
| Google ADK | Agent framework and orchestration |
| Google Cloud Run | Hosted application |
| Google Cloud Secret Manager | Secure credential storage |
| Grafana Cloud | Observability and incident data |
| Grafana MCP | Metrics, logs, incidents and annotations |
| Prometheus | Streaming infrastructure metrics |
| Loki | Streaming infrastructure logs |
| Confluent Cloud | Event streaming |
| Confluent MCP | Kafka investigation |
| Grafana Agent Observability | AI agent telemetry |
| Python | Application implementation |

---

# 🌟 What Makes StreamGuard AI Different?

## 1. Agentic Investigation

The operator provides a goal instead of manually constructing every query.

## 2. Multi-System Reasoning

Grafana observability and Confluent Kafka events are investigated together.

## 3. Evidence-First RCA

The agent clearly separates verified evidence, derived observations, and hypotheses.

## 4. Safe Correlation

The agent does not invent regional relationships when telemetry lacks the necessary identifiers.

## 5. Bidirectional Grafana Integration

The agent can investigate Grafana and record operational context back through annotations.

## 6. Observable AI

Grafana Agent Observability exposes model calls, tool calls, latency, tokens, conversations, and estimated cost.

## 7. Operator-Centric Design

The system produces actionable recommendations while keeping humans in control of production remediation.

---

# 🏗️ End-to-End Workflow

```text
1. Operator reports a streaming problem
                 ↓
2. StreamGuard AI receives the investigation goal
                 ↓
3. Root agent delegates to specialized agents
                 ↓
4. Grafana agent investigates metrics, logs and incidents
                 ↓
5. Confluent agent investigates Kafka events
                 ↓
6. Gemini reasons across the collected evidence
                 ↓
7. Evidence is separated from observations and hypotheses
                 ↓
8. Streaming impact is summarized
                 ↓
9. Recommended operator actions are generated
                 ↓
10. Relevant incident context can be recorded in Grafana
                 ↓
11. Agent execution is captured by Agent Observability
```

---

# 📌 Key Design Principles

### Evidence Over Assumptions

The agent should only make claims supported by available telemetry.

### Cross-System Correlation

Important incidents often require combining multiple observability sources.

### Human-in-the-Loop Operations

The agent assists engineers instead of making uncontrolled production changes.

### Explainable Investigation

The final response makes it clear why a conclusion was reached.

### Observable AI

The AI system itself should be observable, measurable, and debuggable.

---

# 🏆 Hackathon Alignment

StreamGuard AI was built for the **Agentic Cinema: The Blockbuster Hackathon**.

The project focuses on the reliability challenges behind modern cinema, OTT, and video-streaming experiences.

It combines:

```text
Google Cloud
     +
Gemini
     +
Google ADK
     +
Grafana Cloud MCP
     +
Confluent Kafka MCP
     +
Grafana Agent Observability
```

The result is an agentic reliability workflow that transforms:

```text
Telemetry
   ↓
Investigation
   ↓
Correlation
   ↓
Reasoning
   ↓
Operational Insight
```

---

# 🎯 Why This Matters

For a streaming operator, the value is not another dashboard.

The value is reducing the time between:

```text
Something is wrong
        ↓
We understand what is happening
        ↓
We know what evidence supports it
        ↓
We know what to investigate next
```

StreamGuard AI brings these steps together into one agentic workflow.

---

# 📜 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for the complete license text.

---

# 👩‍💻 Author

**Shrushti Wakchaure**

Built with:

- Google Cloud
- Gemini
- Google Agent Development Kit
- Grafana Cloud
- Grafana MCP
- Confluent Kafka
- Confluent MCP
- Grafana Agent Observability

---

# 🎬 Final Takeaway

> **When a major movie or streaming event starts failing, StreamGuard AI turns scattered observability signals into an evidence-based reliability investigation.**

It helps operators answer:

**What happened?**

**Where did it happen?**

**What evidence supports it?**

**What might be causing it?**

**How many viewers could be affected?**

**What should the operator investigate next?**

And when appropriate:

**What incident context should be recorded back into Grafana?**

---

## ⭐ StreamGuard AI

**Observe → Investigate → Correlate → Reason → Recommend**

### Making cinema and video-streaming reliability more intelligent, explainable, and operationally actionable.
