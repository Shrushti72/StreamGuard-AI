from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class TelemetryPoint(BaseModel):
    timestamp: str
    ingest_cpu_pct: float
    transcode_queue_depth: int
    cdn_egress_gbps: float
    buffer_ratio_pct: float
    audio_video_desync_ms: float
    active_viewers: int

class AnomalyEvent(BaseModel):
    anomaly_id: str
    event_name: str
    severity: str  # CRITICAL, WARNING, INFO
    affected_subsystem: str  # INGEST, TRANSCODE, CDN, AUDIO
    root_cause_metric: str
    estimated_impact_time_mins: float
    technical_details: str

class ExecutiveAlert(BaseModel):
    alert_id: str
    event_name: str
    headline: str
    plain_language_narrative: str
    impact_summary: str
    recommended_action: str
    grafana_incident_id: Optional[str] = None
    grafana_annotation_timestamp: str
    timestamp: str

class GrafanaMCPToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    response_status: str
    result_summary: str
