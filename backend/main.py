import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from backend.app.simulator.telemetry_simulator import telemetry_simulator
from backend.app.agents.broadcast_supervisor_agent import broadcast_supervisor_agent
from backend.app.mcp.grafana_mcp_client import grafana_mcp_client

app = FastAPI(
    title="StreamGuard AI — Live Broadcast Continuity Supervisor",
    description="Google Cloud Gemini ADK + Grafana Cloud MCP Server (grafana/mcp-grafana) for Live Broadcast Health & Incident Telemetry",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        return "<h1>StreamGuard AI Backend Running</h1>"
