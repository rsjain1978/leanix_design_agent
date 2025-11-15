import asyncio
from typing import List
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langchain_core.tools import BaseTool
from config import openai_config
from mcp_leanix_client import get_leanix_tools

def _filter_design_standard_tools(tools: List[BaseTool]) -> List[BaseTool]:
    if not tools:
        return tools
    keywords = ["search", "find", "get", "overview", "fact", "sheet"]
    f = []
    for t in tools:
        if any(k in t.name.lower() for k in keywords):
            f.append(t)
    return f or tools

async def build_design_standard_agent():
    leanix_tools = await get_leanix_tools()
    design_tools = _filter_design_standard_tools(leanix_tools)
    model = ChatOpenAI(model=openai_config.model, temperature=0.1)
    system_prompt = SystemMessage(content="""You fetch Design Standards from LeanIX using MCP tools.""")
    app = create_react_agent(
        model, design_tools,
        state_modifier=lambda s: {**s, "messages":[system_prompt]+s.get("messages", [])},
    )
    return app

async def query_design_standards(topic: str) -> str:
    app = await build_design_standard_agent()
    result = await app.ainvoke({
        "messages":[{"role":"user","content":f"Fetch design standards for: {topic}"}]
    })
    return result["messages"][-1].content

if __name__ == "__main__":
    asyncio.run(query_design_standards("event driven"))
