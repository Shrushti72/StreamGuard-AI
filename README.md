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

https://streamguard-ai-793289044855.us-central1.run.app

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
This project is open-source software licensed under the [MIT License](LICENSE).
