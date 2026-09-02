import asyncio
import uuid

from google.adk.apps import App
from google.adk.agents.context_cache_config import ContextCacheConfig
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from streamguard_agent.agent import root_agent


APP_NAME = "streamguard"
USER_ID = "streamguard-web-user"

_session_service = InMemorySessionService()

app = App(
    name=APP_NAME,
    root_agent=root_agent,
    context_cache_config=ContextCacheConfig(),
)

_runner = Runner(
    app=app,
    session_service=_session_service,
)


async def _run_adk(prompt: str) -> str:
    session_id = str(uuid.uuid4())

    await _session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    message = types.Content(
        role="user",
        parts=[types.Part(text=prompt)],
    )

    final_text = ""

    async for event in _runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                texts = [
                    part.text
                    for part in event.content.parts
                    if getattr(part, "text", None)
                ]
                if texts:
                    final_text = "\n".join(texts)

    return final_text


def run_adk(prompt: str) -> str:
    return asyncio.run(_run_adk(prompt))
