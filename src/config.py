import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

@dataclass
class OpenAIConfig:
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

@dataclass
class LeanIXMCPConfig:
    server_name: str = os.getenv("LEANIX_MCP_SERVER_NAME", "leanix")
    transport: str = os.getenv("LEANIX_MCP_TRANSPORT", "streamable_http")
    url: str | None = os.getenv("LEANIX_MCP_URL")
    auth_bearer: str | None = os.getenv("LEANIX_MCP_AUTH_BEARER")

openai_config = OpenAIConfig()
leanix_config = LeanIXMCPConfig()

if not openai_config.api_key:
    raise RuntimeError("OPENAI_API_KEY is not set")
if leanix_config.transport in ("streamable_http", "sse") and not leanix_config.url:
    raise RuntimeError("LEANIX_MCP_URL must be set")
