import time
import random
from typing import List, Dict, Any
from backend.app.models.broadcast_schemas import TelemetryPoint

class TelemetrySimulator:
    """
    Simulates real-time broadcast stream metrics & anomaly scenarios for premiere livestreams.
    """
    def __init__(self):
        self.active_event_name = "CYBERPUNK MOVIE PREMIERE - GLOBAL LIVESTREAM"
        self.active_viewers = 1450000
        self.anomaly_active = False
        self.active_anomaly_type = "NORMAL"

    def get_current_metrics(self) -> TelemetryPoint:
        now = time.strftime("%H:%M:%S")
        
        if self.active_anomaly_type == "ENCODER_OVERLOAD":
            return TelemetryPoint(
                timestamp=now,
                ingest_cpu_pct=98.4,
                transcode_queue_depth=142,
                cdn_egress_gbps=420.5,
                buffer_ratio_pct=4.8,
                audio_video_desync_ms=120.0,
                active_viewers=self.active_viewers
            )
        elif self.active_anomaly_type == "CDN_THROTTLING":
            return TelemetryPoint(
                timestamp=now,
                ingest_cpu_pct=48.2,
                transcode_queue_depth=12,
                cdn_egress_gbps=180.2,
                buffer_ratio_pct=8.9,
                audio_video_desync_ms=25.0,
                active_viewers=self.active_viewers
            )
        elif self.active_anomaly_type == "AUDIO_DESYNC":
            return TelemetryPoint(
                timestamp=now,
                ingest_cpu_pct=52.1,
                transcode_queue_depth=15,
                cdn_egress_gbps=510.0,
                buffer_ratio_pct=0.8,
                audio_video_desync_ms=450.0,
                active_viewers=self.active_viewers
            )

        # Baseline Normal Telemetry
        return TelemetryPoint(
            timestamp=now,
            ingest_cpu_pct=round(42.0 + random.uniform(-3, 3), 1),
            transcode_queue_depth=random.randint(5, 12),
            cdn_egress_gbps=round(520.0 + random.uniform(-10, 10), 1),
            buffer_ratio_pct=round(0.4 + random.uniform(-0.1, 0.1), 2),
            audio_video_desync_ms=round(15.0 + random.uniform(-2, 2), 1),
            active_viewers=self.active_viewers + random.randint(-500, 500)
        )

    def inject_anomaly(self, anomaly_type: str):
        self.anomaly_active = True
        self.active_anomaly_type = anomaly_type

    def reset_anomaly(self):
        self.anomaly_active = False
        self.active_anomaly_type = "NORMAL"

telemetry_simulator = TelemetrySimulator()
