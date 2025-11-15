#!/usr/bin/env python3
"""Entry point for running the LeanIX Design Agent MCP Server."""

if __name__ == "__main__":
    from src.server import mcp
    import os
    import logging
    from src.config import openai_config, leanix_config
    
    logger = logging.getLogger("leanix-design-agent")
    
    host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_SERVER_PORT", "8000"))
    
    logger.info("Starting LeanIX Design Agent MCP Server")
    logger.info(f"Server URL: http://{host}:{port}")
    logger.info(f"OpenAI Model: {openai_config.model}")
    logger.info(f"LeanIX URL: {leanix_config.url}")
    
    mcp.run(transport="streamable_http", host=host, port=port)

