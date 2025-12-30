---
name: roadmap
description: View AI Agent Development Roadmap
allowed-tools: Read
---

# AI Agent Development Roadmap

Display comprehensive learning roadmaps for AI agent development topics.

## Usage

```
/roadmap [topic]
```

## Available Roadmaps

### Core Topics
- `agent-fundamentals` - Architectures, ReAct, cognitive loops
- `llm-integration` - APIs, prompting, cost optimization
- `rag-systems` - Embeddings, vector stores, retrieval
- `tool-calling` - Function calling, schemas, validation
- `multi-agent` - Orchestration, coordination, workflows
- `agent-memory` - Short/long-term, retrieval, context
- `agent-safety` - Guardrails, filtering, compliance

### Full Roadmap
- `ai-agents` - Complete AI agent development path

## Examples

```
/roadmap ai-agents
/roadmap tool-calling
/roadmap rag-systems
/roadmap multi-agent
```

---

## Example: AI Agents Full Roadmap

```
/roadmap ai-agents
```

### Overview
AI agents are autonomous systems that use LLMs to reason, plan, and act to accomplish tasks. They represent the evolution from simple chatbots to intelligent assistants.

**Market Demand:** Very High (2024-2025)
**Key Players:** Anthropic, OpenAI, LangChain, Microsoft
**Frameworks:** LangGraph, Claude Agent SDK, AutoGPT

---

### Learning Path

#### Phase 1: Foundations (Month 1-2)
```
✅ LLM Basics
   └── Prompt engineering
   └── API integration (Claude, OpenAI)
   └── Token management

✅ Agent Fundamentals
   └── ReAct pattern (Thought → Action → Observation)
   └── Tool use basics
   └── Simple loops

✅ First Agent
   └── Build with LangGraph
   └── Add 2-3 tools
   └── Error handling
```

#### Phase 2: Core Skills (Month 3-4)
```
✅ RAG Systems
   └── Embeddings and chunking
   └── Vector databases
   └── Retrieval optimization

✅ Tool Calling
   └── JSON Schema design
   └── Claude Tool Use
   └── OpenAI Functions

✅ Memory Systems
   └── Conversation buffer
   └── Vector memory
   └── Context management
```

#### Phase 3: Advanced Patterns (Month 5-6)
```
✅ Multi-Agent Systems
   └── Orchestrator-Worker
   └── Hierarchical patterns
   └── Agent communication

✅ Production Readiness
   └── Safety guardrails
   └── Monitoring
   └── Cost optimization

✅ Deployment
   └── Streaming responses
   └── Error recovery
   └── Scaling patterns
```

---

### Technology Stack

| Category | Recommended | Alternatives |
|----------|-------------|--------------|
| LLM | Claude Sonnet 4 | GPT-4, Gemini |
| Framework | LangGraph | CrewAI, AutoGen |
| Vector DB | Pinecone | Weaviate, Qdrant |
| Embeddings | text-embedding-3 | Cohere, Voyage |
| Safety | Guardrails AI | Custom filters |

---

### Key Skills Checklist

#### Beginner
- [ ] Understand ReAct pattern
- [ ] Make LLM API calls
- [ ] Implement basic tool use
- [ ] Handle API errors

#### Intermediate
- [ ] Build RAG pipelines
- [ ] Design tool schemas
- [ ] Implement memory systems
- [ ] Create agent workflows

#### Advanced
- [ ] Multi-agent orchestration
- [ ] Production safety patterns
- [ ] Performance optimization
- [ ] Custom agent architectures

---

### Project Ideas

| Level | Project | Time |
|-------|---------|------|
| Beginner | Todo Agent with 3 tools | 8-12h |
| Beginner | Q&A over documents | 12-16h |
| Intermediate | Research Assistant | 30-40h |
| Intermediate | Code Review Agent | 40-50h |
| Advanced | Multi-Agent Research System | 80-100h |
| Advanced | Autonomous Coding Agent | 100+h |

---

### Career Path

| Role | Skills Required | Salary Range |
|------|----------------|--------------|
| AI Engineer | Agent basics, RAG | $120K-180K |
| Senior AI Engineer | Multi-agent, Production | $180K-250K |
| AI Architect | System design, Leadership | $250K-350K |

---

### Resources

**Official Documentation:**
- [Anthropic Docs](https://docs.anthropic.com/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [OpenAI Docs](https://platform.openai.com/docs)

**Learning:**
- Building Effective Agents (Anthropic)
- LangChain Tutorials
- DeepLearning.AI Courses

**Community:**
- LangChain Discord
- Anthropic Discord
- AI Twitter/X community

---

### Related Skills (Activate with plugin)

| Skill | Bonded Agent |
|-------|--------------|
| `ai-agent-basics` | 01-ai-agent-fundamentals |
| `llm-integration` | 02-llm-integration |
| `rag-systems` | 03-rag-systems |
| `tool-calling` | 04-tool-calling |
| `multi-agent` | 05-multi-agent |
| `agent-memory` | 06-agent-memory |
| `agent-safety` | 07-agent-safety |

---

**Next Steps:**
1. `/learn` - Start your learning journey
2. `/assess [topic]` - Test your knowledge
3. `/project [topic] [level]` - Find projects to build
