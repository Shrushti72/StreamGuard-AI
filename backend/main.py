import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from backend.app.simulator.telemetry_simulator import telemetry_simulator
from backend.app.agents.broadcast_supervisor_agent import broadcast_supervisor_agent
from backend.app.mcp.grafana_mcp_client import grafana_mcp_client
from backend.app.adk_agent_engine.agent import adk_agent

app = FastAPI(
    title="StreamGuard AI — Google Cloud Agent Platform ADK Engine",
    description="Native Google Cloud ADK + Vertex AI Agent Engine + Grafana Cloud MCP Server",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Native Google Cloud ADK Agent Platform Endpoint
@app.post("/api/adk/query")
def run_google_adk_query(
    prompt: str = "Check the current broadcast health using Grafana MCP tools. Do not invent telemetry."
):
    """
    Execute the real StreamGuard Google ADK root agent.
    The root agent uses the configured Grafana MCP and Confluent MCP toolsets.
    """
    from backend.app.adk_agent_engine.real_runner import run_adk

    return {
        "status": "success",
        "framework": "Google Cloud ADK",
        "agent": "My_agent_StreamGuard_AI",
        "response": run_adk(prompt),
    }

# API Endpoints
@app.get("/api/telemetry/stream")
def get_telemetry_stream():
    return telemetry_simulator.get_current_metrics()

@app.post("/api/mcp/analyze")
def analyze_broadcast():
    return broadcast_supervisor_agent.analyze_broadcast_health()

@app.post("/api/simulator/inject")
def inject_anomaly(anomaly_type: str = "ENCODER_OVERLOAD"):
    if anomaly_type == "RESET":
        telemetry_simulator.reset_anomaly()
        return {"status": "NORMAL", "message": "Telemetry restored to baseline."}
    
    telemetry_simulator.inject_anomaly(anomaly_type)
    return {"status": "ANOMALY_ACTIVE", "anomaly_type": anomaly_type}

@app.get("/api/mcp/tools")
def get_grafana_mcp_tools():
    return {
        "mcp_server": "grafana/mcp-grafana (Official Grafana Cloud MCP Endpoint)",
        "adk_framework": "Google Cloud Agent Development Kit (ADK)",
        "tool_count": len(grafana_mcp_client.list_active_mcp_tools()),
        "tools": grafana_mcp_client.list_active_mcp_tools()
    }

@app.get("/api/mcp/audit")
def get_mcp_audit_logs():
    return {
        "status": "CONNECTED_TO_GRAFANA_CLOUD_MCP",
        "mcp_server_version": "grafana/mcp-grafana v1.2.0",
        "total_tool_invocations": len(grafana_mcp_client.tool_calls_history),
        "history": grafana_mcp_client.tool_calls_history[-20:]
    }

# Static Files & Web UI
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/", response_class=HTMLResponse)
    def read_root():
        index_path = os.path.join(frontend_dir, "index.html")
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f:
                return f.read()
        return "<h1>StreamGuard AI Google ADK Backend Running</h1>"
