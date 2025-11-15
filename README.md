# LeanIX Design Agent

An intelligent AI agent that retrieves design standards and architectural guidelines from LeanIX using natural language queries. Built with LangChain, LangGraph, and the Model Context Protocol (MCP).

## Overview

The LeanIX Design Agent is a conversational AI tool that connects to your LeanIX Enterprise Architecture Management platform and intelligently searches for design standards, best practices, and architectural guidelines. Instead of manually navigating through LeanIX, simply ask questions in natural language and let the AI agent find the information you need.

### Key Features

- 🤖 **Intelligent Querying**: Uses OpenAI GPT models to understand your questions and determine the best approach to find information
- 🔗 **LeanIX Integration**: Connects to LeanIX via the Model Context Protocol (MCP)
- 🎯 **Focused Tool Selection**: Automatically filters and uses only relevant LeanIX tools (search, find, get, overview, fact sheets)
- ⚡ **Async Operations**: Built with async/await for efficient performance
- 🛠️ **ReAct Agent Pattern**: Leverages LangGraph's ReAct (Reasoning + Acting) pattern for intelligent decision-making

## Architecture

```
┌─────────────────┐
│   User Input    │
│   (Topic)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   main.py       │
│  Entry Point    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│          agent.py                   │
│  ┌─────────────────────────────┐   │
│  │  LangGraph ReAct Agent      │   │
│  │  + OpenAI GPT Model         │   │
│  └─────────────────────────────┘   │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│    mcp_leanix_client.py             │
│  ┌─────────────────────────────┐   │
│  │  MCP Multi-Server Client    │   │
│  │  + Tool Discovery           │   │
│  └─────────────────────────────┘   │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  LeanIX MCP     │
│  Server         │
└─────────────────┘
```

## Prerequisites

- **Python 3.10+**
- **OpenAI API Key** - For GPT model access
- **LeanIX MCP Server** - Running and accessible LeanIX MCP server
- **LeanIX Authentication Token** - Bearer token for API authentication

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd leanix_design_agent
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# LeanIX MCP Configuration
LEANIX_MCP_SERVER_NAME=leanix
LEANIX_MCP_TRANSPORT=streamable_http
LEANIX_MCP_URL=https://your-leanix-mcp-server.com/mcp
LEANIX_MCP_AUTH_BEARER=your_leanix_bearer_token_here
```

#### Configuration Options

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | - | ✅ Yes |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` | No |
| `LEANIX_MCP_SERVER_NAME` | Identifier for the LeanIX server | `leanix` | No |
| `LEANIX_MCP_TRANSPORT` | Transport protocol (`streamable_http` or `sse`) | `streamable_http` | No |
| `LEANIX_MCP_URL` | URL of your LeanIX MCP server | - | ✅ Yes |
| `LEANIX_MCP_AUTH_BEARER` | Bearer token for LeanIX authentication | - | ✅ Yes |

## Usage

### Command Line Mode

```bash
# Query with inline topic
python main.py "event driven architecture"

# Query multiple words
python main.py microservices best practices

# Complex queries
python main.py "API design standards for REST services"
```

### Interactive Mode

```bash
python main.py
# You'll be prompted: "Enter topic: "
# Type your query and press Enter
```

### Example Queries

```bash
# Architecture patterns
python main.py "event driven architecture"

# Technology standards
python main.py "cloud deployment guidelines"

# Design principles
python main.py "microservices design patterns"

# Specific technologies
python main.py "Kafka messaging standards"

# Security guidelines
python main.py "API security best practices"
```

### Example Output

```
Topic: event driven architecture

Fetching design standards from LeanIX...

=== Design Standards for Event Driven Architecture ===

1. Event-Driven Architecture Pattern
   - Use asynchronous messaging for loose coupling
   - Implement event sourcing for audit trails
   - Use message brokers like Kafka or RabbitMQ

2. Best Practices
   - Define clear event schemas
   - Implement idempotent event handlers
   - Use event versioning strategies

[Additional details from LeanIX...]
```

## Project Structure

```
leanix_design_agent/
│
├── main.py                  # Entry point - handles user input
├── agent.py                 # Agent logic - builds and runs the AI agent
├── mcp_leanix_client.py     # LeanIX MCP client - connects to LeanIX
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
└── README.md               # This file
```

## How It Works

### 1. **Tool Discovery**
When the agent starts, it connects to the LeanIX MCP server and discovers all available tools:
- Search tools
- Find tools
- Get tools
- Overview tools
- Fact sheet tools

### 2. **Tool Filtering**
The agent filters tools to focus on read-only operations relevant to design standards retrieval.

### 3. **Intelligent Querying**
Using the ReAct (Reasoning + Acting) pattern:
- The AI model reasons about what information is needed
- Selects appropriate LeanIX tools to call
- Processes the results
- May call additional tools if needed
- Synthesizes a final answer

### 4. **Response Generation**
The agent returns a comprehensive response with design standards, best practices, and guidelines from LeanIX.

## Components Deep Dive

### `main.py` - Entry Point
- Accepts user input from command line or interactive prompt
- Initializes the async runtime
- Displays results

### `agent.py` - Agent Logic
- **`build_design_standard_agent()`**: Creates a LangGraph ReAct agent
  - Loads LeanIX tools via MCP
  - Filters to relevant tools
  - Configures OpenAI GPT model
  - Sets system prompt
  
- **`query_design_standards(topic)`**: Executes the agent
  - Takes a topic string
  - Invokes the agent
  - Returns the final response

- **`_filter_design_standard_tools()`**: Filters tools by keywords
  - Keeps tools related to search, find, get, overview, fact sheets
  - Ensures only relevant read operations are used

### `mcp_leanix_client.py` - MCP Client
- **`build_connections_config()`**: Builds MCP connection configuration
  - Configures transport (HTTP/SSE)
  - Sets up authentication headers
  
- **`get_leanix_tools()`**: Retrieves available tools from LeanIX
  - Connects to MCP server
  - Discovers and loads tools
  - Returns tool list

### `config.py` - Configuration
- Loads environment variables from `.env` file
- Validates required configuration
- Provides typed configuration objects

## Troubleshooting

### Common Issues

#### 1. **"OPENAI_API_KEY is not set"**
- Ensure you've created a `.env` file in the project root
- Verify the API key is correctly set: `OPENAI_API_KEY=sk-...`
- Check that `python-dotenv` is installed

#### 2. **"LEANIX_MCP_URL must be set"**
- Ensure `LEANIX_MCP_URL` is set in your `.env` file
- Verify the URL is correct and accessible
- Check if the MCP server is running

#### 3. **Connection Errors**
- Verify your LeanIX MCP server is running and accessible
- Check network connectivity
- Ensure the bearer token is valid and not expired
- Verify the transport type matches your server configuration

#### 4. **No Tools Found**
- Check LeanIX MCP server logs for errors
- Verify authentication token has proper permissions
- Ensure the MCP server is properly configured

#### 5. **Agent Not Responding**
- Check OpenAI API rate limits
- Verify your API key has sufficient credits
- Try reducing query complexity
- Check for network issues

### Debug Mode

To see which tools are loaded, run:

```bash
python mcp_leanix_client.py
```

This will list all available LeanIX MCP tools.

To test the agent directly:

```bash
python agent.py
```

This will run a test query for "event driven" architecture.

## Dependencies

- **langgraph** - Agent orchestration framework
- **langchain** - LLM application framework
- **langchain-openai** - OpenAI integration for LangChain
- **langchain-mcp-adapters** - MCP protocol adapters for LangChain
- **mcp** - Model Context Protocol implementation
- **python-dotenv** - Environment variable management

## Advanced Configuration

### Using Different OpenAI Models

```env
# For more capable responses (higher cost)
OPENAI_MODEL=gpt-4o

# For faster, cheaper responses
OPENAI_MODEL=gpt-4o-mini

# For legacy compatibility
OPENAI_MODEL=gpt-3.5-turbo
```

### Custom Transport Protocols

If your LeanIX MCP server uses SSE (Server-Sent Events):

```env
LEANIX_MCP_TRANSPORT=sse
```

## Security Considerations

- ⚠️ **Never commit your `.env` file** to version control
- 🔒 Store API keys and tokens securely
- 🔐 Use environment-specific credentials (dev, staging, prod)
- 🛡️ Rotate bearer tokens regularly
- 📝 Audit agent queries in production environments

## Performance Tips

1. **Model Selection**: Use `gpt-4o-mini` for faster responses and lower costs
2. **Query Specificity**: More specific queries lead to faster, more relevant results
3. **Connection Reuse**: The MCP client is designed to be efficient with connections

## Future Enhancements

Possible improvements for this project:

- [ ] Add caching for frequently queried topics
- [ ] Implement streaming responses for real-time feedback
- [ ] Add support for multiple LeanIX workspaces
- [ ] Create a web UI for easier interaction
- [ ] Add conversation history for follow-up questions
- [ ] Implement tool usage analytics
- [ ] Add support for creating/updating design standards (write operations)
- [ ] Create a batch processing mode for multiple queries

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Specify your license here]

## Support

For issues, questions, or contributions:
- Create an issue in the repository
- Contact the maintainers
- Check LeanIX and LangChain documentation

## Acknowledgments

- Built with [LangChain](https://langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/)
- Powered by [OpenAI](https://openai.com/)
- Integrates with [LeanIX](https://www.leanix.net/)
- Uses [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

---

**Note**: This project requires access to a LeanIX MCP server. Ensure you have the necessary permissions and infrastructure in place before using this tool.

