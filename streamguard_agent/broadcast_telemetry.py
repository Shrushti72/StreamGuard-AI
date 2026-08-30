from opentelemetry.trace import SpanKind
import time
import random
import logging
import os

from opentelemetry import metrics, trace
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter


# ============================================================
# STREAMGUARD BROADCAST TELEMETRY SIMULATOR
# ============================================================

RESOURCE = Resource.create({
    "service.name": "streamguard-broadcast",
    "service.namespace": "streamguard",
    "deployment.environment": "demo",
    "broadcast.name": "premiere-livestream",
})


# ============================================================
# GRAFANA CLOUD OTLP CONFIGURATION
# ============================================================

GRAFANA_OTLP_ENDPOINT = os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"].rstrip("/")
GRAFANA_OTLP_HEADERS_RAW = os.environ["OTEL_EXPORTER_OTLP_HEADERS"]

GRAFANA_OTLP_HEADERS = {}
for item in GRAFANA_OTLP_HEADERS_RAW.split(","):
    key, value = item.split("=", 1)
    GRAFANA_OTLP_HEADERS[key.strip()] = value.strip()

METRICS_ENDPOINT = GRAFANA_OTLP_ENDPOINT + "/v1/metrics"
TRACES_ENDPOINT = GRAFANA_OTLP_ENDPOINT + "/v1/traces"
LOGS_ENDPOINT = GRAFANA_OTLP_ENDPOINT + "/v1/logs"


# ============================================================
# METRICS
# ============================================================

metric_exporter = OTLPMetricExporter(
    endpoint=METRICS_ENDPOINT,
    headers=GRAFANA_OTLP_HEADERS,
)

metric_reader = PeriodicExportingMetricReader(
    metric_exporter,
    export_interval_millis=5000,
)

meter_provider = MeterProvider(
    resource=RESOURCE,
    metric_readers=[metric_reader],
)

metrics.set_meter_provider(meter_provider)

meter = metrics.get_meter("streamguard.broadcast")


cpu = meter.create_gauge(
    "stream_cpu_usage_percent",
    description="Broadcast encoder/origin CPU utilization",
    unit="%",
)

transcode_latency = meter.create_gauge(
    "stream_transcode_latency_ms",
    description="Transcoding latency",
    unit="ms",
)

buffering = meter.create_gauge(
    "stream_buffering_ratio",
    description="Viewer buffering ratio",
    unit="ratio",
)

error_rate = meter.create_gauge(
    "stream_error_rate_percent",
    description="Broadcast error rate",
    unit="%",
)

dropped_frames = meter.create_gauge(
    "stream_dropped_frames_total",
    description="Dropped video frames",
    unit="frames",
)

viewer_count = meter.create_gauge(
    "stream_viewers",
    description="Active viewers",
    unit="viewers",
)


# ============================================================
# TRACES
# ============================================================

tracer_provider = TracerProvider(
    resource=RESOURCE
)

tracer_provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint=TRACES_ENDPOINT,
            headers=GRAFANA_OTLP_HEADERS,
        )
    )
)

trace.set_tracer_provider(tracer_provider)

tracer = trace.get_tracer("streamguard.broadcast")


# ============================================================
# LOGS
# ============================================================

logger_provider = LoggerProvider(
    resource=RESOURCE
)

logger_provider.add_log_record_processor(
    BatchLogRecordProcessor(
        OTLPLogExporter(
            endpoint=LOGS_ENDPOINT,
            headers=GRAFANA_OTLP_HEADERS,
        )
    )
)

handler = LoggingHandler(
    level=logging.INFO,
    logger_provider=logger_provider,
)

logger = logging.getLogger("streamguard.broadcast")
logger.setLevel(logging.INFO)
logger.addHandler(handler)


# ============================================================
# SIMULATION
# ============================================================

STREAM = "main-broadcast"
REGIONS = ["northeast", "west", "south", "midwest"]

iteration = 0

print("")
print("============================================================")
print(" StreamGuard Broadcast Telemetry Simulator")
print("============================================================")
print(" Stream: main-broadcast")
print(" Destination: Grafana Cloud")
print(" Metrics + Logs + Traces")
print(" Press CTRL+C to stop")
print("============================================================")
print("")


try:
    while True:

        iteration += 1

        # Every 6th cycle intentionally creates an incident.
        incident = iteration % 6 == 0

        if incident:
            cpu_value = random.uniform(88, 97)
            latency_value = random.uniform(650, 950)
            buffering_value = random.uniform(5.0, 9.0)
            error_value = random.uniform(3.0, 7.0)
            dropped_value = random.randint(100, 500)
            viewers_value = random.randint(85000, 120000)

            status = "incident"

        else:
            cpu_value = random.uniform(35, 55)
            latency_value = random.uniform(120, 220)
            buffering_value = random.uniform(0.1, 0.8)
            error_value = random.uniform(0.0, 0.4)
            dropped_value = random.randint(0, 8)
            viewers_value = random.randint(85000, 120000)

            status = "healthy"


        attributes = {
            "stream": STREAM,
            "region": random.choice(REGIONS),
            "component": "broadcast-pipeline",
        }


        # -----------------------------
        # Metrics
        # -----------------------------

        cpu.set(cpu_value, attributes)
        transcode_latency.set(latency_value, attributes)
        buffering.set(buffering_value, attributes)
        error_rate.set(error_value, attributes)
        dropped_frames.set(dropped_value, attributes)
        viewer_count.set(viewers_value, attributes)


        # -----------------------------
        # Trace
        # -----------------------------

        with tracer.start_as_current_span(
    "broadcast.health.check",
    kind=SpanKind.SERVER,
) as span:

            span.set_attribute(
                "broadcast.stream",
                STREAM
            )

            span.set_attribute(
                "broadcast.status",
                status
            )

            span.set_attribute(
                "broadcast.cpu_percent",
                cpu_value
            )

            span.set_attribute(
                "broadcast.transcode_latency_ms",
                latency_value
            )

            span.set_attribute(
                "broadcast.buffering_ratio",
                buffering_value
            )

            span.set_attribute(
                "broadcast.error_rate_percent",
                error_value
            )

            if incident:
                span.add_event(
                    "broadcast_anomaly_detected",
                    {
                        "reason": "High CPU and transcoding latency",
                        "stream": STREAM,
                        "region": attributes["region"],
                    },
                )


        # -----------------------------
        # Logs
        # -----------------------------

        if incident:

            logger.error(
                "BROADCAST INCIDENT: origin CPU spike and "
                "transcoding latency detected; viewer buffering "
                "risk is elevated. stream=%s cpu=%.1f "
                "latency_ms=%.1f buffering=%.2f error_rate=%.2f",
                STREAM,
                cpu_value,
                latency_value,
                buffering_value,
                error_value,
            )

        else:

            logger.info(
                "Broadcast healthy: stream=%s cpu=%.1f "
                "latency_ms=%.1f buffering=%.2f "
                "error_rate=%.2f",
                STREAM,
                cpu_value,
                latency_value,
                buffering_value,
                error_value,
            )


        print(
            f"[{iteration:03d}] "
            f"{status.upper():8} | "
            f"CPU {cpu_value:5.1f}% | "
            f"Latency {latency_value:6.1f}ms | "
            f"Buffer {buffering_value:4.2f} | "
            f"Errors {error_value:4.2f}%"
        )

        time.sleep(10)


except KeyboardInterrupt:

    print("\nStopping StreamGuard telemetry simulator...")

    meter_provider.shutdown()
    tracer_provider.shutdown()
    logger_provider.shutdown()

    print("Telemetry simulator stopped.")
