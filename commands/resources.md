---
name: resources
description: AI Agent Learning Resources
allowed-tools: Read
---

# AI Agent Learning Resources

Get curated, high-quality resources for AI agent development.

## Usage

```
/resources [topic] [type]
```

**Parameters:**
- `topic`: AI agent topic (agent-fundamentals, rag-systems, etc.)
- `type`: Optional - `docs`, `tutorials`, `courses`, `papers`, `repos`

## Examples

```
/resources ai-agents
/resources rag-systems tutorials
/resources multi-agent papers
/resources tool-calling repos
```

---

## Official Documentation

### LLM Providers

**Anthropic Claude**
```
📚 Claude Documentation
- API Reference: https://docs.anthropic.com/en/api
- Tool Use Guide: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- Prompt Engineering: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- Building Effective Agents: https://www.anthropic.com/research/building-effective-agents
```

**OpenAI**
```
📚 OpenAI Documentation
- API Reference: https://platform.openai.com/docs/api-reference
- Function Calling: https://platform.openai.com/docs/guides/function-calling
- Assistants API: https://platform.openai.com/docs/assistants/overview
- Cookbook: https://cookbook.openai.com/
```

### Agent Frameworks

**LangChain / LangGraph**
```
📚 LangChain Ecosystem
- LangChain Docs: https://python.langchain.com/docs/
- LangGraph Docs: https://langchain-ai.github.io/langgraph/
- LangSmith: https://docs.smith.langchain.com/
- GitHub: https://github.com/langchain-ai/langchain
```

---

## Tutorials

### Agent Fundamentals
```
🎓 Interactive Tutorials

1. LangChain Agent Tutorial (Free)
   URL: https://python.langchain.com/docs/tutorials/agents/
   Time: 2-3 hours
   Topics: ReAct, tools, memory

2. LangGraph Quick Start (Free)
   URL: https://langchain-ai.github.io/langgraph/tutorials/
   Time: 3-4 hours
   Topics: State machines, checkpoints

3. Anthropic Agent Patterns (Free)
   URL: https://github.com/anthropics/anthropic-cookbook
   Time: 4-6 hours
   Topics: Claude agents, tool use
```

### RAG Systems
```
🎓 RAG Tutorials

1. LangChain RAG Tutorial (Free)
   URL: https://python.langchain.com/docs/tutorials/rag/
   Time: 2-3 hours
   Topics: Basic RAG pipeline

2. Pinecone RAG Guide (Free)
   URL: https://www.pinecone.io/learn/retrieval-augmented-generation/
   Time: 3-4 hours
   Topics: Production RAG

3. RAGAS Evaluation (Free)
   URL: https://docs.ragas.io/en/stable/
   Time: 1-2 hours
   Topics: RAG metrics
```

---

## Video Courses

### Free Courses
```
🎥 Free Learning

1. DeepLearning.AI - LangChain Courses
   - LangChain for LLM Application Development
   - LangChain: Chat with Your Data
   - Building Systems with ChatGPT API
   URL: https://www.deeplearning.ai/short-courses/

2. Prompt Engineering Guide
   URL: https://www.promptingguide.ai/
   Topics: Prompting techniques, chain-of-thought

3. LangChain YouTube Channel
   URL: https://www.youtube.com/@LangChain
   Topics: Weekly updates, tutorials
```

### Paid Courses
```
💰 Premium Courses

1. Building AI Agents (DeepLearning.AI)
   Price: Subscription
   Topics: Production agents, evaluation

2. Full Stack LLM Bootcamp (FSDL)
   URL: https://fullstackdeeplearning.com/
   Price: Free recordings, paid live
   Topics: LLMOps, deployment
```

---

## Research Papers

### Must-Read Papers
```
📄 Foundational Papers

1. ReAct: Synergizing Reasoning and Acting in LLMs
   URL: https://arxiv.org/abs/2210.03629
   Key: Thought-Action-Observation loop

2. Chain-of-Thought Prompting
   URL: https://arxiv.org/abs/2201.11903
   Key: Step-by-step reasoning

3. Retrieval-Augmented Generation (RAG)
   URL: https://arxiv.org/abs/2005.11401
   Key: Grounding LLMs in knowledge

4. MemGPT: Memory Management for LLMs
   URL: https://arxiv.org/abs/2310.08560
   Key: Long-term memory systems

5. Generative Agents: Interactive Simulacra
   URL: https://arxiv.org/abs/2304.03442
   Key: Agent memory and behavior
```

### Recent Papers (2024-2025)
```
📄 Latest Research

1. Building Effective Agents (Anthropic, 2024)
   URL: https://www.anthropic.com/research/building-effective-agents
   Key: Production patterns

2. Multi-Agent Research System (Anthropic, 2025)
   URL: https://www.anthropic.com/engineering/multi-agent-research-system
   Key: Orchestrator-worker pattern

3. Claude Agent SDK Documentation
   Key: Claude-native agent patterns
```

---

## GitHub Repositories

### Official Repos
```
📦 Framework Repositories

LangChain: https://github.com/langchain-ai/langchain
LangGraph: https://github.com/langchain-ai/langgraph
Anthropic SDK: https://github.com/anthropics/anthropic-sdk-python
OpenAI SDK: https://github.com/openai/openai-python
```

### Example Projects
```
📦 Learning Repositories

1. Anthropic Cookbook
   URL: https://github.com/anthropics/anthropic-cookbook
   Topics: Claude patterns, tool use

2. OpenAI Cookbook
   URL: https://github.com/openai/openai-cookbook
   Topics: Function calling, embeddings

3. LangChain Templates
   URL: https://github.com/langchain-ai/langchain/tree/master/templates
   Topics: Production patterns
```

### Multi-Agent Frameworks
```
📦 Multi-Agent Repos

1. AutoGen (Microsoft)
   URL: https://github.com/microsoft/autogen
   Topics: Multi-agent conversations

2. CrewAI
   URL: https://github.com/joaomdmoura/crewAI
   Topics: Role-based agents

3. MetaGPT
   URL: https://github.com/geekan/MetaGPT
   Topics: Software development agents
```

---

## Tools & Libraries

### Vector Databases
```
🗄️ Vector Store Options

Pinecone: https://www.pinecone.io/ (Managed)
Weaviate: https://weaviate.io/ (Hybrid search)
Qdrant: https://qdrant.tech/ (High performance)
Chroma: https://www.trychroma.com/ (Local dev)
pgvector: https://github.com/pgvector/pgvector (PostgreSQL)
```

### Embedding Models
```
🔢 Embedding Options

OpenAI: text-embedding-3-small/large
Cohere: embed-v3
Voyage AI: voyage-3
Open Source: BGE, E5, GTE
```

### Safety & Guardrails
```
🛡️ Safety Tools

Guardrails AI: https://docs.guardrailsai.com/
NeMo Guardrails: https://github.com/NVIDIA/NeMo-Guardrails
```

---

## Community

### Discord Servers
```
💬 Active Communities

LangChain Discord: https://discord.gg/langchain
Anthropic Discord: https://discord.gg/anthropic
OpenAI Discord: https://discord.gg/openai
```

### Twitter/X Accounts
```
🐦 Follow for Updates

@LangChainAI - LangChain official
@AnthropicAI - Anthropic official
@OpenAI - OpenAI official
@hwchase17 - Harrison Chase (LangChain)
```

---

## Quick Reference by Topic

| Topic | Best Resource |
|-------|---------------|
| Agent Fundamentals | LangGraph Tutorials |
| LLM Integration | Official SDK Docs |
| RAG Systems | LangChain RAG Tutorial |
| Tool Calling | Anthropic Tool Use Guide |
| Multi-Agent | Anthropic Multi-Agent Paper |
| Agent Memory | MemGPT Paper |
| Agent Safety | OWASP LLM Top 10 |

---

**Get resources:** `/resources [topic]`
