# Quick Start Guide

Get started with AI Agents Assistant in 5 minutes.

## Prerequisites

- Python 3.10+
- API keys for LLM providers (optional but recommended)

## Installation

```bash
# Clone the repository
git clone https://github.com/pluginagentmarketplace/custom-plugin-ai-agents.git
cd custom-plugin-ai-agents

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the root directory:

```env
# Required for Claude-based scripts
ANTHROPIC_API_KEY=sk-ant-...

# Required for OpenAI-based scripts
OPENAI_API_KEY=sk-...

# Optional: Local Ollama
OLLAMA_BASE_URL=http://localhost:11434
```

## Running Example Scripts

### 1. ReAct Agent (LangGraph)

```bash
cd skills/ai-agent-basics/scripts
python react_agent.py "What is 25 * 47?"
```

### 2. Multi-Provider LLM Client

```bash
cd skills/llm-integration/scripts
python multi_provider_client.py "Explain quantum computing briefly"
```

### 3. Hybrid RAG Pipeline

```bash
cd skills/rag-systems/scripts

# Create sample documents
mkdir -p docs
echo "Python is a programming language." > docs/sample.txt

# Run RAG
python hybrid_rag_pipeline.py docs "What is Python?"
```

### 4. Claude Tool Use

```bash
cd skills/tool-calling/scripts
python claude_tool_use.py "What is 100 divided by 4?"
```

### 5. Orchestrator-Worker System

```bash
cd skills/multi-agent/scripts
python orchestrator_worker.py "Research AI trends and summarize findings"
```

### 6. Multi-Layer Memory

```bash
cd skills/agent-memory/scripts
python multi_layer_memory.py
```

### 7. Safety Guardrails

```bash
cd skills/agent-safety/scripts
python safety_guardrails.py
```

## Learning Path

1. **Start with Basics**: Read `agents/01-ai-agent-fundamentals.md`
2. **Try Examples**: Run the scripts above
3. **Modify & Experiment**: Customize the scripts for your use case
4. **Build Your Agent**: Combine patterns from multiple skills

## Skill Overview

| Skill | Focus | Key Patterns |
|-------|-------|--------------|
| ai-agent-basics | Agent fundamentals | ReAct, Plan-Execute |
| llm-integration | LLM API usage | Multi-provider, Streaming |
| rag-systems | Retrieval | Hybrid search, Chunking |
| tool-calling | Function calling | Claude tools, OpenAI functions |
| multi-agent | Coordination | Orchestrator-Worker |
| agent-memory | State management | Buffer, Vector, Summary |
| agent-safety | Guardrails | Injection detection, Filtering |

## Common Issues

### API Key Errors

```
Error: ANTHROPIC_API_KEY environment variable not set
```

**Solution**: Export your API key:
```bash
export ANTHROPIC_API_KEY=your-key-here
```

### Import Errors

```
ModuleNotFoundError: No module named 'langchain'
```

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### ChromaDB Errors

```
Error: sqlite3.OperationalError
```

**Solution**: Delete the `chroma_db` folder and retry:
```bash
rm -rf chroma_db
```

## Next Steps

- Read the full agent documentation in `/agents/`
- Explore skill details in `/skills/*/SKILL.md`
- Use `/commands/` for learning paths and resources
- Check `CONTRIBUTING.md` for contribution guidelines

## Support

- GitHub Issues: [Report a bug](https://github.com/pluginagentmarketplace/custom-plugin-ai-agents/issues)
- Documentation: See `/docs/` folder
