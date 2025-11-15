# LeanIX Design Agent MCP Server

An intelligent MCP server that exposes AI-powered design standards querying from LeanIX. Built with FastMCP, LangGraph, and OpenAI.

## 🎯 What Is This?

This MCP (Model Context Protocol) server acts as an **intelligent gateway** between AI assistants and LeanIX. It uses AI to understand natural language queries and automatically orchestrates multiple LeanIX tools to fetch design standards, architectural patterns, and best practices.

### The Problem It Solves

**Without this server:**
- AI assistants would need to know 50+ LeanIX tools
- Complex manual tool selection required
- Raw, unformatted data responses
- Requires deep LeanIX expertise

**With this server:**
- 4 simple, focused tools
- AI automatically selects the right LeanIX tools
- Coherent, synthesized answers
- Natural language queries

## 🏗️ Architecture

```
┌─────────────────────────────────┐
│  AI Assistant (MCP Client)      │
│  GitHub Copilot / Claude /      │
│  Cursor / Any MCP Client        │
└────────────┬────────────────────┘
             │ HTTP (MCP Protocol)
             ▼
┌─────────────────────────────────┐
│  Your MCP Server (port 8000)    │
│  ┌───────────────────────────┐  │
│  │  FastMCP Framework        │  │
│  │  4 Intelligent Tools      │  │
│  └───────────┬───────────────┘  │
│              │                   │
│              ▼                   │
│  ┌───────────────────────────┐  │
│  │  AI Agent                 │  │
│  │  - OpenAI GPT             │  │
│  │  - LangGraph ReAct        │  │
│  │  - Query Understanding    │  │
│  │  - Tool Orchestration     │  │
│  └───────────┬───────────────┘  │
└──────────────┼──────────────────┘
               │ HTTP (MCP Protocol)
               ▼
┌─────────────────────────────────┐
│  LeanIX MCP Server              │
│  50+ Low-Level Tools            │
│  (search, get, list, etc.)      │
└─────────────────────────────────┘
```

### Value Proposition

| Feature | Direct LeanIX MCP | Your MCP Server |
|---------|------------------|-----------------|
| **Tools** | 50+ low-level tools | 4 focused tools |
| **Query Style** | Technical, exact parameters | Natural language |
| **Tool Selection** | Manual | AI-powered automatic |
| **Multi-Tool Queries** | Manual orchestration | Automatic |
| **Response Quality** | Raw data | Synthesized, coherent |
| **LeanIX Knowledge** | Required | Not required |
| **Complexity** | 🔴 High | 🟢 Low |

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API key
- Access to a LeanIX MCP server with authentication

### 1. Installation

```bash
# Clone or download this project
cd leanix_design_agent

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini

# LeanIX MCP Server (connects TO LeanIX)
LEANIX_MCP_URL=https://your-leanix-mcp-server.com/mcp
LEANIX_MCP_AUTH_BEARER=your_leanix_bearer_token_here
LEANIX_MCP_TRANSPORT=streamable_http
LEANIX_MCP_SERVER_NAME=leanix

# Your MCP Server Configuration
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8000
```

### 3. Run the Server

**Option A: Using run.py (Recommended)**
```bash
python run.py
```

**Option B: Direct execution**
```bash
python src/server.py
```

**Option C: Development mode with auto-reload**
```bash
fastmcp dev src/server.py
```

**Server will start at:** `http://localhost:8000`

### 4. Verify Server is Running

```bash
# Check server health
curl http://localhost:8000

# Should return MCP server info
```

## 🛠️ Available Tools

The server exposes 4 intelligent tools that MCP clients can use:

### 1. `search_design_standards`
Search for design standards, best practices, and architectural guidelines.

**Parameters:**
- `topic` (string): Topic to search for

**Examples:**
- "event driven architecture"
- "microservices best practices"
- "API design guidelines"
- "cloud deployment standards"

### 2. `get_architecture_patterns`
Get architectural patterns and design guidelines for specific architecture styles.

**Parameters:**
- `architecture_type` (string): Architecture type

**Examples:**
- "microservices"
- "event-driven"
- "serverless"
- "monolithic"
- "SOA"

### 3. `get_technology_standards`
Get technology standards and guidelines for specific technologies or frameworks.

**Parameters:**
- `technology` (string): Technology name

**Examples:**
- "Kafka"
- "Kubernetes"
- "React"
- "PostgreSQL"
- "Docker"

### 4. `get_security_guidelines`
Get security guidelines, best practices, and standards.

**Parameters:**
- `security_area` (string): Security area

**Examples:**
- "API security"
- "authentication"
- "data encryption"
- "network security"
- "OAuth implementation"

## 🔌 Connecting MCP Clients

### Generic MCP Client Configuration

```json
{
  "servers": {
    "leanix-design-agent": {
      "url": "http://localhost:8000",
      "transport": "streamable_http"
    }
  }
}
```

### Example: Python Client

```python
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

async def query_leanix():
    connections = {
        "leanix-design": {
            "transport": "streamable_http",
            "url": "http://localhost:8000"
        }
    }
    
    async with MultiServerMCPClient(connections) as client:
        tools = await client.get_tools()
        print(f"Available tools: {[t.name for t in tools]}")
        
        # Call a tool
        result = await client.call_tool(
            "search_design_standards",
            {"topic": "microservices"}
        )
        print(result)

asyncio.run(query_leanix())
```

### Example: Using FastMCP Client

```python
from fastmcp import FastMCP

# Connect to your server
client = FastMCP("http://localhost:8000")

# Call a tool
result = await client.call_tool(
    "get_architecture_patterns",
    {"architecture_type": "event-driven"}
)
print(result)
```

## 📁 Project Structure

```
leanix_design_agent/
│
├── src/
│   ├── __init__.py           # Package marker
│   ├── server.py             # Main MCP server (consolidated)
│   │   ├── LeanIX client     #   - Connect to LeanIX MCP
│   │   ├── AI agent          #   - Build intelligent agent
│   │   ├── MCP tools (x4)    #   - Tool definitions
│   │   └── Main entry        #   - Server startup
│   └── config.py             # Configuration management
│
├── run.py                    # Entry point script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── .env.example              # Environment template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

### File Descriptions

**`src/server.py`** (208 lines) - The main server file containing:
- **LeanIX Client**: Connection management, tool retrieval, filtering
- **AI Agent**: LangGraph ReAct agent with OpenAI for intelligent querying
- **MCP Tools**: 4 FastMCP tool definitions
- **Server**: FastMCP HTTP server setup

**`src/config.py`** - Configuration classes with validation:
- `OpenAIConfig`: API key, model selection
- `LeanIXMCPConfig`: LeanIX server connection details

**`run.py`** - Simple entry point that imports and runs the server

## ⚙️ Configuration Reference

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | - | ✅ |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` | ❌ |
| `LEANIX_MCP_URL` | LeanIX MCP server URL | - | ✅ |
| `LEANIX_MCP_AUTH_BEARER` | Bearer token for LeanIX | - | ✅ |
| `LEANIX_MCP_TRANSPORT` | Transport protocol | `streamable_http` | ❌ |
| `LEANIX_MCP_SERVER_NAME` | LeanIX server identifier | `leanix` | ❌ |
| `MCP_SERVER_HOST` | Your server host | `0.0.0.0` | ❌ |
| `MCP_SERVER_PORT` | Your server port | `8000` | ❌ |

### OpenAI Model Options

```env
# Most cost-effective (recommended)
OPENAI_MODEL=gpt-4o-mini

# More capable, higher cost
OPENAI_MODEL=gpt-4o

# Turbo models
OPENAI_MODEL=gpt-4-turbo
OPENAI_MODEL=gpt-3.5-turbo
```

## 🔍 How It Works

### Request Flow

1. **MCP Client** sends a tool request:
   ```json
   {
     "tool": "search_design_standards",
     "arguments": {"topic": "microservices"}
   }
   ```

2. **FastMCP** routes to the appropriate tool function

3. **AI Agent**:
   - Connects to LeanIX MCP server
   - Retrieves available LeanIX tools (50+ tools)
   - Filters to relevant tools (search, find, get, fact sheets)
   - Creates a LangGraph ReAct agent with OpenAI
   
4. **ReAct Agent** (Reasoning + Acting):
   - **Reasons**: "User wants microservices design standards"
   - **Acts**: Calls appropriate LeanIX tools
   - **Observes**: Reviews the results
   - **Repeats**: If more information needed
   - **Synthesizes**: Creates coherent final answer

5. **Response** returned to MCP client as formatted text

### Example: Behind the Scenes

**User Query:** "Get microservices best practices"

**What Happens:**
```
1. Your MCP Server receives: get_architecture_patterns("microservices")

2. AI Agent thinks:
   "I need to search LeanIX for microservices patterns"
   
3. AI Agent discovers LeanIX has these tools:
   - search_fact_sheets
   - search_documents  
   - get_technology_stack
   - list_design_patterns
   [... 46 more tools]
   
4. AI Agent filters to relevant tools:
   - search_fact_sheets ✅
   - search_documents ✅
   - get_overview ✅
   
5. AI Agent automatically:
   - Calls search_fact_sheets(type="architecture", name="microservices")
   - Calls search_documents(query="microservices patterns")
   - Combines results
   
6. AI Agent synthesizes:
   "Microservices Best Practices from LeanIX:
    1. Service independence...
    2. API-first design...
    3. Decentralized data..."
    
7. Returns formatted response ✅
```

## 🧪 Development

### Running in Development Mode

```bash
# Auto-reload on file changes
fastmcp dev src/server.py
```

### Testing Tools Manually

```python
# test_manual.py
import asyncio
from src.server import _query_leanix

async def test():
    result = await _query_leanix("Get microservices patterns")
    print(result)

asyncio.run(test())
```

### Debugging

Enable debug logging:

```python
# In src/server.py, change:
logging.basicConfig(level=logging.DEBUG)  # Instead of INFO
```

## 🐛 Troubleshooting

### Server Won't Start

**Error: "OPENAI_API_KEY is not set"**
- ✅ Create `.env` file in project root
- ✅ Add `OPENAI_API_KEY=sk-...`
- ✅ Verify `.env` is in the same directory as `run.py`

**Error: "LEANIX_MCP_URL must be set"**
- ✅ Add `LEANIX_MCP_URL=https://...` to `.env`
- ✅ Verify URL is correct and accessible
- ✅ Check if LeanIX MCP server is running

**Error: Port 8000 already in use**
```bash
# Change port in .env
MCP_SERVER_PORT=8001
```

### Connection Issues

**Can't connect to LeanIX MCP**
- ✅ Verify `LEANIX_MCP_URL` is correct
- ✅ Check bearer token hasn't expired
- ✅ Test URL manually: `curl <LEANIX_MCP_URL>`
- ✅ Verify network/firewall allows connection

**No tools found from LeanIX**
- ✅ Check authentication token permissions
- ✅ Review LeanIX MCP server logs
- ✅ Verify transport type matches: `streamable_http`

### Query Issues

**Slow responses**
- ⚠️ Normal: First query takes longer (agent initialization)
- ⚠️ LeanIX may have slow response times
- ⚠️ Complex queries require multiple tool calls
- ✅ Consider using faster OpenAI model

**Poor quality answers**
- ✅ Try different OpenAI model: `OPENAI_MODEL=gpt-4o`
- ✅ Check if LeanIX has relevant data
- ✅ Rephrase query to be more specific

**OpenAI rate limits**
- ✅ Verify API key has credits
- ✅ Check OpenAI dashboard for limits
- ✅ Consider upgrading OpenAI plan

## 📊 Performance

### Typical Response Times

| Operation | Time | Notes |
|-----------|------|-------|
| First query | 5-10s | Agent initialization + LeanIX connection |
| Subsequent queries | 2-5s | Agent cached |
| Simple queries | 2-3s | Single LeanIX tool call |
| Complex queries | 5-10s | Multiple tool calls + synthesis |

### Optimization Tips

1. **Use `gpt-4o-mini`** - Faster and cheaper
2. **Keep queries specific** - Reduces tool calls needed
3. **Consider caching** - Add caching layer for repeated queries
4. **Connection pooling** - LeanIX client reuses connections

## 📦 Dependencies

```
fastmcp              # MCP server framework
langgraph            # Agent orchestration
langchain            # LLM application framework
langchain-openai     # OpenAI integration
langchain-mcp-adapters  # MCP client support
python-dotenv        # Environment management
```

### Dependency Tree

```
Your MCP Server
├── fastmcp           → MCP server capabilities
├── langgraph         → AI agent orchestration
│   └── langchain     → LLM framework
│       └── langchain-openai  → OpenAI GPT
└── langchain-mcp-adapters    → Connect to LeanIX MCP
```

## 🔒 Security Considerations

- ⚠️ **Never commit `.env`** - Contains API keys and tokens
- 🔒 **Rotate tokens regularly** - Bearer tokens should expire
- 🛡️ **Use HTTPS in production** - Encrypt traffic
- 📝 **Audit queries** - Log what's being asked
- 🔐 **Restrict network access** - Firewall rules for server
- 💰 **Monitor OpenAI usage** - Set budget limits

## 🚀 Production Deployment

### Docker Deployment (Recommended)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY run.py .

EXPOSE 8000
CMD ["python", "run.py"]
```

```bash
# Build
docker build -t leanix-design-agent .

# Run
docker run -p 8000:8000 --env-file .env leanix-design-agent
```

### Environment-Specific Configs

```bash
# Development
.env.development

# Staging
.env.staging

# Production
.env.production
```

### Health Checks

Add health endpoint monitoring:
```bash
curl http://localhost:8000/health
```

## 🤝 Contributing

This is an internal tool. For modifications:

1. Test locally: `fastmcp dev src/server.py`
2. Verify with MCP clients
3. Update README if adding features
4. Ensure `.env` is in `.gitignore`

## 📄 License

[Specify your license]

## 🆘 Support

- **OpenAI Issues**: https://platform.openai.com/docs
- **LeanIX Support**: Contact your LeanIX administrator
- **FastMCP Docs**: https://github.com/jlowin/fastmcp

---

## 🎓 Understanding MCP Architecture

### Why Use MCP?

**MCP (Model Context Protocol)** is a standardized protocol for connecting AI assistants to external tools and data sources.

**Benefits:**
- ✅ Standardized: Works with any MCP-compatible client
- ✅ Tool Discovery: Clients automatically learn available tools
- ✅ Type Safety: Schema-based parameter validation
- ✅ AI-Native: Designed for AI-to-AI communication

### Your Server's Role

Your server is a **middleware/facade** that:
1. **Abstracts Complexity**: 4 simple tools instead of 50+ complex ones
2. **Adds Intelligence**: AI understands and orchestrates queries
3. **Synthesizes Results**: Coherent answers instead of raw data
4. **Domain Focus**: Specialized for design standards

This is a **best practice pattern** in AI architecture! 🎯

---

**Built with ❤️ using FastMCP, LangGraph, and OpenAI**
