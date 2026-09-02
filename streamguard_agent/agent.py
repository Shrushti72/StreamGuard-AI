import os
import base64
from functools import cached_property

from google.auth import default
from google.genai import Client
from google.genai.types import HttpOptions, HttpRetryOptions

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context

from google.adk.integrations.agent_registry import AgentRegistry
from google.adk.auth.credential_manager import CredentialManager
from google.adk.integrations.agent_identity import GcpAuthProvider
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams, StreamableHTTPConnectionParams
from agento11y import Client as Agento11yClient
from agento11y_google_adk import with_agento11y_google_adk_callbacks
from mcp import StdioServerParameters


# ============================================================
# GOOGLE CLOUD CONFIGURATION
# ============================================================

PROJECT_ID = os.environ.get(
    "GOOGLE_CLOUD_PROJECT",
    "project-5f28ba74-3df1-4c73-ab3",
)

LOCATION = "global"  #

os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


# ============================================================
# GEMINI GLOBAL LOCATION
# ============================================================

class GlobalGemini(Gemini):
    """
    Routes Gemini requests through the global Vertex AI endpoint
    with retry/backoff for transient rate-limit responses.
    """

    def __init__(self, **kwargs):
        kwargs["retry_options"] = HttpRetryOptions(
            attempts=5,
            initial_delay=2.0,
            max_delay=30.0,
            exp_base=2.0,
            jitter=1.0,
            http_status_codes=[429, 500, 502, 503, 504],
        )
        super().__init__(**kwargs)

    @cached_property
    def api_client(self) -> Client:
        return Client(
            vertexai=True,
            project=PROJECT_ID,
            location="global",
            http_options=HttpOptions(
                retry_options=self.retry_options,
            ),
        )


# ============================================================
# AGENT REGISTRY AUTHENTICATION
# ============================================================

# Register Google Cloud authentication so ADK can resolve
# Agent Registry authentication bindings automatically.
CredentialManager.register_auth_provider(
    GcpAuthProvider()
)


# ============================================================
# AGENT REGISTRY CLIENT
# ============================================================

registry = AgentRegistry(
    project_id=PROJECT_ID,
    location=LOCATION,
)



# ============================================================
# GRAFANA MCP SERVER
# ============================================================

grafana_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="mcp-grafana",
            args=["-t", "stdio", "--disable-proxied"],
            env={
                "GRAFANA_URL": os.environ["GRAFANA_URL"],
                "GRAFANA_SERVICE_ACCOUNT_TOKEN": os.environ[
                    "GRAFANA_SERVICE_ACCOUNT_TOKEN"
                ],
            },
        ),
    ),
)


# ============================================================
# CONFLUENT KAFKA MCP SERVER
# ============================================================

# The registered Confluent MCP endpoint is a Streamable HTTP server.
# Connect directly to the endpoint using the verified Confluent
# API-key/API-secret Basic authentication.
CONFLUENT_MCP_URL = (
    "https://mcp.asia-south1.gcp.confluent.cloud"
    "/mcp/v1/organizations/"
    "25bf86f4-a307-4dbe-a530-89090e74f12a"
)


def confluent_mcp_headers(_context):
    api_key = os.environ["CONFLUENT_API_KEY"]
    api_secret = os.environ["CONFLUENT_API_SECRET"]

    encoded = base64.b64encode(
        f"{api_key}:{api_secret}".encode()
    ).decode()

    return {
        "Authorization": f"Basic {encoded}",
    }


confluent_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=CONFLUENT_MCP_URL,
        timeout=30.0,
        sse_read_timeout=300.0,
    ),
    header_provider=confluent_mcp_headers,
)


# ============================================================
# Grafana Agent Observability
agento11y_client = Agento11yClient()
agento11y_callbacks = with_agento11y_google_adk_callbacks(
    None,
    client=agento11y_client,
    provider_resolver="auto",
)

# Compatibility adapter for Google ADK 2.8.x:
# ADK calls after_tool_callback with "tool_response",
# while the Agent Observability integration expects "result".
_agento11y_after_tool = agento11y_callbacks.get("after_tool_callback")

if _agento11y_after_tool is not None:
    async def _adk_compatible_after_tool_callback(
        tool, args, tool_context, tool_response
    ):
        return await _agento11y_after_tool(
            tool=tool,
            args=args,
            tool_context=tool_context,
            result=tool_response,
        )

    agento11y_callbacks["after_tool_callback"] = (
        _adk_compatible_after_tool_callback
    )

# BROADCAST MONITORING AGENT
# ============================================================

broadcast_monitoring = LlmAgent(
    name="broadcast_monitoring",

    model=GlobalGemini(
        model="gemini-3.5-flash"
    ),

    description=(
        "Monitors live broadcast infrastructure using "
        "Grafana Cloud metrics and logs, detects technical "
        "anomalies, correlates incidents, and triggers "
        "Grafana incident and dashboard annotation actions."
    ),

    instruction="""
You are the Broadcast Monitoring subagent for StreamGuard AI.

Your job is to monitor live broadcast infrastructure using
the connected Grafana Cloud MCP tools.

Monitor:

- Origin and ingest CPU utilization
- Transcode queue depth
- CDN egress
- Viewer buffering ratio
- Audio/video synchronization delay
- Broadcast errors
- Dropped frames
- Stream failures

Use the Grafana MCP tools to retrieve real telemetry.

When investigating a problem:

1. Query Grafana Prometheus metrics.
2. Query Grafana Loki logs when necessary.
3. Correlate related signals.
4. Determine the likely root cause.
5. Identify affected systems.
6. Estimate the viewer impact only when supported by telemetry.
7. Create a Grafana incident for confirmed significant incidents.
8. Create a Grafana dashboard annotation for important events.

Never invent telemetry values.

INCIDENT SEVERITY AND ACTION RULES:

- Do not assign a formal severity such as Sev-1, Critical, Major,
  or High unless a severity policy or explicit threshold is provided
  by the retrieved data or instructions.
- If no formal severity policy exists, describe the observed condition
  using evidence-based language such as "significant regional
  degradation" or "serious viewer-impacting issue."
- Clearly distinguish observed telemetry from inferred root cause.
- Do not claim that a specific component such as CDN, origin,
  transcoder, network, or edge infrastructure is the confirmed cause
  unless the retrieved telemetry supports that conclusion.
- Recommendations must be presented as recommendations, not confirmed
  facts.
- Do not invent thresholds, durations, capacities, failover targets,
  routing destinations, or recovery procedures.
- Do not recommend restarting or failing over infrastructure unless
  the available evidence supports that action.
- Estimate viewer impact only when supported by retrieved telemetry.

If Grafana data is unavailable, clearly state that telemetry
could not be retrieved.

When reporting an incident, use this format:

What happened:
Root cause:
Impact:
Recommended action:

Always explain technical problems in simple language suitable
for a Studio Head or Executive Producer.
""",

    tools=[
        grafana_toolset
    ],
    **agento11y_callbacks,
)


# ============================================================
# EVENT STREAMING AGENT
# ============================================================

event_streaming = LlmAgent(
    name="event_streaming",

    model=GlobalGemini(
        model="gemini-3.5-flash"
    ),

    description=(
        "Handles real-time broadcast events and event "
        "streaming through Confluent Kafka."
    ),

    instruction="""
You are the Event Streaming subagent for StreamGuard AI.

Your job is to handle real-time broadcast events.

Monitor and process events such as:

- Stream health changes
- Script or configuration updates
- Broadcast incidents
- Onset telemetry events
- Continuity alerts

Use the connected Confluent Kafka MCP tools.


The StreamGuard Confluent Kafka environment is:
- environment_id: env-zzg5v7
- cluster_id: lkc-0xd5w6p

Use these values only when a Kafka MCP tool explicitly requires
environment_id or cluster_id.

IMPORTANT TOOL ARGUMENT RULES:
- list_kafka_topics: provide environment_id and cluster_id.
- describe_kafka_topic: provide the required arguments defined by the live tool schema.
- consume_kafka_messages: provide environment_id, cluster_id, and topic_name. max_messages is optional.
- list_schema_subjects: provide the required arguments defined by the live tool schema.
- read_schema_subject: provide the required arguments defined by the live tool schema.
- Use environment_id="env-zzg5v7" and cluster_id="lkc-0xd5w6p" when the live Kafka MCP tools require them.
- Never invent additional arguments or event data.

Publish important events to the appropriate Kafka topics.

Use structured event information.

Never invent event data.

CORRELATION RULE:
Never correlate a Kafka event to a specific Grafana region unless
the Kafka event itself contains a region or region_id field.

If the Kafka event has no region field:
- State that regional correlation is not possible.
- Compare Kafka values with Grafana values only as an
  overall/system-level comparison.
- Do not claim that the Kafka event represents West, South,
  Midwest, or Northeast.

If Kafka data is unavailable, clearly state that it is unavailable.
""",

    tools=[
        confluent_toolset
    ],
    **agento11y_callbacks,
)


# ============================================================
# GOOGLE SEARCH AGENT
# ============================================================

google_search_agent = LlmAgent(
    name="streamguard_google_search_agent",

    model=GlobalGemini(
        model="gemini-3.5-flash"
    ),

    description=(
        "Agent specialized in performing Google searches."
    ),

    instruction="""
Use Google Search when current public web information
is required.

Do not use web search as a replacement for Grafana telemetry.

Grafana MCP must be used for StreamGuard infrastructure
metrics and logs.
""",

    tools=[
        GoogleSearchTool()
    ],
)


# ============================================================
# URL CONTEXT AGENT
# ============================================================

url_context_agent = LlmAgent(
    name="streamguard_url_context_agent",

    model=GlobalGemini(
        model="gemini-3.5-flash"
    ),

    description=(
        "Agent specialized in fetching content from URLs."
    ),

    instruction="""
Use the URL context tool when the user provides a URL
whose contents need to be retrieved or analyzed.
""",

    tools=[
        url_context
    ],
)


# ============================================================
# ROOT STREAMGUARD AI AGENT
# ============================================================

root_agent = LlmAgent(
    name="My_agent_StreamGuard_AI",

    model=GlobalGemini(
        model="gemini-3.5-flash"
    ),

    description=(
        "Autonomous cinema and video-streaming reliability and incident "
        "supervisor for cinema and video-streaming reliability."
    ),

    sub_agents=[
        broadcast_monitoring,
        event_streaming,
    ],

    instruction="""
You are StreamGuard AI, an autonomous Cinema & Video-Streaming Reliability
Supervisor for cinema and video-streaming platforms, including
OTT premieres, live cinema events, and on-demand playback.

Your primary responsibility is to identify broadcast
infrastructure problems early and coordinate the appropriate
response.

Use the Broadcast Monitoring subagent for:

- Ingest health
- CPU utilization
- Transcode queue depth
- CDN egress
- Viewer buffering
- Audio/video synchronization
- Broadcast errors
- Dropped frames
- Stream failures
- Grafana metrics
- Grafana logs
- Grafana incidents
- Grafana annotations

When telemetry shows an anomaly:

1. Identify the abnormal signal.
2. Correlate related signals.
3. Determine the likely root cause.
4. Explain the expected viewer impact.
5. Recommend the appropriate operational response.
6. Create a Grafana incident when the issue is significant.
7. Create a Grafana annotation when appropriate.

Never invent telemetry or event data.

CROSS-SYSTEM CORRELATION RULES:

- Treat Grafana as the source for infrastructure and broadcast-health
  telemetry.
- Treat Kafka as the source for broadcast events, incidents, and
  continuity context.
- Correlate Kafka and Grafana only when the retrieved data provides
  sufficient evidence for the correlation.
- A Kafka event may only be associated with a specific Grafana region
  when that Kafka event contains a matching region or region_id field.
- If a Kafka event has no region or region_id field, explicitly state
  that regional correlation is not possible.
- Never use a generic Kafka event to claim that a particular region
  caused or experienced an incident.
- If Grafana shows a regional anomaly but Kafka has no corresponding
  regional event, describe it as an observed Grafana regional issue,
  not a Kafka-confirmed regional incident.
- Clearly distinguish observed facts, correlations, and inferred causes.
- Never invent telemetry, event fields, thresholds, incident records,
  or causal relationships.

If telemetry cannot be retrieved, explicitly say so.

Always explain technical problems in simple language
suitable for a Studio Head or Executive Producer.

Example:

"US-East ingest CPU reached 98%. This is increasing the
transcode queue and may cause viewer buffering.
Recommended action: increase transcode capacity."
""",

    tools=[
        agent_tool.AgentTool(
            agent=google_search_agent
        ),
        agent_tool.AgentTool(
            agent=url_context_agent
        ),
    ],
    **agento11y_callbacks,
)
