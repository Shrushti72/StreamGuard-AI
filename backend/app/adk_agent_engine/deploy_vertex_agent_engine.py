#!/usr/bin/env python3

import os
import vertexai
from vertexai import types
from vertexai.agent_engines import AdkApp

from backend.app.adk_agent_engine.agent import adk_agent


def deploy_to_vertex_agent_engine():
    project_id = os.getenv("PROJECT_ID")
    location = os.getenv("LOCATION", "us-central1")

    if not project_id:
        raise RuntimeError("PROJECT_ID environment variable is not set.")

    staging_bucket = f"gs://{project_id}-agent-engine-staging-uswest1"

    print("=" * 70)
    print("REAL GOOGLE AGENT ENGINE DEPLOYMENT")
    print("=" * 70)
    print(f"Project : {project_id}")
    print(f"Region  : {location}")
    print(f"Bucket  : {staging_bucket}")
    print()

    print("[1/3] Initializing Vertex AI client...")

    client = vertexai.Client(
        project=project_id,
        location=location,
        http_options=dict(api_version="v1beta1"),
    )

    print("      Vertex AI client initialized.")
    print()

    print("[2/3] Creating ADK application...")

    app = AdkApp(
        agent=adk_agent,
    )

    print("      AdkApp created from existing StreamGuard root agent.")
    print()

    print("[3/3] Deploying to Google Agent Runtime...")
    print("      This can take several minutes.")
    print()

    remote_app = client.agent_engines.create(
        agent=app,
        config={
            "staging_bucket": staging_bucket,
            "identity_type": types.IdentityType.AGENT_IDENTITY,
            "requirements": [
                "google-cloud-aiplatform[agent_engines,adk]",
                "google-adk[agent-identity,a2a,mcp]",
                "mcp>=1.24.0,<2.0.0",
                "mcp-grafana==1.2.0",
                "pydantic>=2.6.0",
                "cloudpickle>=3.0.0",
            ],
            "extra_packages": [
                "./backend",
                "./streamguard_agent",
            ],
        },
    )

    resource_name = remote_app.api_resource.name

    print()
    print("=" * 70)
    print("REAL AGENT ENGINE DEPLOYMENT COMPLETE")
    print("=" * 70)
    print()
    print(f"Resource Name:")
    print(resource_name)
    print()
    print("This is the REAL Google Agent Runtime resource.")
    print()
    print("=" * 70)

    return remote_app


if __name__ == "__main__":
    deploy_to_vertex_agent_engine()
