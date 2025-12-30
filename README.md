<div align="center">

<!-- Animated Typing Banner -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=1000&color=2E9EF7&center=true&vCenter=true&multiline=true&repeat=true&width=600&height=100&lines=AI+Agents+Assistant;Production-Grade+Agent+Development;Claude+Code+Plugin" alt="AI Agents Assistant" />

<br/>

<!-- Badge Row 1: Status Badges -->
[![Version](https://img.shields.io/badge/Version-2.0.0-blue?style=for-the-badge)](https://github.com/pluginagentmarketplace/custom-plugin-ai-agents/releases)
[![License](https://img.shields.io/badge/License-Custom-yellow?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen?style=for-the-badge)](#)
[![SASMP](https://img.shields.io/badge/SASMP-v1.3.0-blueviolet?style=for-the-badge)](#)

<!-- Badge Row 2: Content Badges -->
[![Agents](https://img.shields.io/badge/Agents-7-orange?style=flat-square&logo=robot)](#-agents)
[![Skills](https://img.shields.io/badge/Skills-7-purple?style=flat-square&logo=lightning)](#-skills)
[![Commands](https://img.shields.io/badge/Commands-5-green?style=flat-square&logo=terminal)](#-commands)

<br/>

<!-- Quick CTA Row -->
[📦 **Install Now**](#-quick-start) · [🤖 **Explore Agents**](#-agents) · [📖 **Documentation**](#-documentation) · [⭐ **Star this repo**](https://github.com/pluginagentmarketplace/custom-plugin-ai-agents)

---

### What is this?

> **AI Agents Assistant** is a Claude Code plugin with **7 production-grade agents** for building AI agent systems using LangChain, LangGraph, Anthropic, and OpenAI patterns.

</div>

---

## 📑 Table of Contents

<details>
<summary>Click to expand</summary>

- [Quick Start](#-quick-start)
- [Features](#-features)
- [Agents](#-agents)
- [Skills](#-skills)
- [Commands](#-commands)
- [Best Practices](#-best-practices)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

</details>

---

## 🚀 Quick Start

### Prerequisites

- Claude Code CLI v2.0.27+
- Active Claude subscription

### Installation (Choose One)

<details open>
<summary><strong>Option 1: From Marketplace (Recommended)</strong></summary>

```bash
# Step 1️⃣ Add the marketplace
/plugin add marketplace pluginagentmarketplace/custom-plugin-ai-agents

# Step 2️⃣ Install the plugin
/plugin install custom-plugin-ai-agents@pluginagentmarketplace-ai-agents

# Step 3️⃣ Restart Claude Code
# Close and reopen your terminal/IDE
```

</details>

<details>
<summary><strong>Option 2: Local Installation</strong></summary>

```bash
# Clone the repository
git clone https://github.com/pluginagentmarketplace/custom-plugin-ai-agents.git
cd custom-plugin-ai-agents

# Load locally
/plugin load .

# Restart Claude Code
```

</details>

### ✅ Verify Installation

After restart, you should see these agents:

```
custom-plugin-ai-agents:01-ai-agent-fundamentals
custom-plugin-ai-agents:02-llm-integration
custom-plugin-ai-agents:03-rag-systems
custom-plugin-ai-agents:04-tool-calling
custom-plugin-ai-agents:05-multi-agent
custom-plugin-ai-agents:06-agent-memory
custom-plugin-ai-agents:07-agent-safety
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **7 Agents** | Production-grade AI agent specialists |
| 🛠️ **7 Skills** | Atomic capabilities with code examples |
| ⌨️ **5 Commands** | Quick slash commands for learning |
| 🔄 **SASMP v1.3.0** | Full protocol compliance |
| 📚 **2024-2025 Patterns** | LangGraph, Claude Tool Use, OpenAI Functions |

---

## 🤖 Agents

### 7 Production-Grade Agents

| # | Agent | Expertise |
|---|-------|-----------|
| 1 | **AI Agent Fundamentals** | ReAct patterns, cognitive loops, architectures |
| 2 | **LLM Integration** | API orchestration, prompting, cost optimization |
| 3 | **RAG Systems** | Embeddings, chunking, hybrid search, reranking |
| 4 | **Tool Calling** | Function calling, schemas, validation |
| 5 | **Multi-Agent** | Orchestrator-worker, hierarchical systems |
| 6 | **Agent Memory** | Short/long-term, semantic retrieval |
| 7 | **Agent Safety** | Guardrails, filtering, compliance |

### Agent Capabilities

Each agent includes:
- ✅ Clear role & responsibility boundaries
- ✅ Input/Output schemas (TypeScript)
- ✅ Error handling patterns
- ✅ Fallback strategies
- ✅ Token/cost optimization configs
- ✅ Troubleshooting decision trees
- ✅ Production code examples

---

## 🛠️ Skills

### 7 Atomic Skills

| Skill | Bonded Agent | Purpose |
|-------|--------------|---------|
| `ai-agent-basics` | 01-ai-agent-fundamentals | Build ReAct agents with LangGraph |
| `llm-integration` | 02-llm-integration | Integrate Claude, OpenAI, local models |
| `rag-systems` | 03-rag-systems | Build production RAG pipelines |
| `tool-calling` | 04-tool-calling | Implement function calling |
| `multi-agent` | 05-multi-agent | Build orchestrator-worker systems |
| `agent-memory` | 06-agent-memory | Add memory to agents |
| `agent-safety` | 07-agent-safety | Implement safety guardrails |

### Invoke Skills

```python
# Example: Invoke the RAG skill
Skill("custom-plugin-ai-agents:rag-systems")
```

---

## ⌨️ Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/learn` | Start your AI agent journey | `/learn` |
| `/roadmap` | View learning roadmap | `/roadmap ai-agents` |
| `/assess` | Test your knowledge | `/assess tool-calling intermediate` |
| `/resources` | Get learning resources | `/resources rag-systems tutorials` |
| `/project` | Find project ideas | `/project multi-agent advanced` |

---

## 📋 Best Practices (2024-2025)

### From LangChain/LangGraph
- Use LangGraph for new agent implementations
- Implement human-in-the-loop checkpoints
- Add observability with LangSmith

### From Anthropic
- One job per subagent
- Orchestrator handles global planning
- Keep tool permissions narrow

### From OpenAI
- Enable strict mode for function calling
- Use structured outputs
- Implement circuit breakers

---

## 📁 Project Structure

```
custom-plugin-ai-agents/
├── 📁 .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── 📁 agents/              # 7 production agents
│   ├── 01-ai-agent-fundamentals.md
│   ├── 02-llm-integration.md
│   ├── 03-rag-systems.md
│   ├── 04-tool-calling.md
│   ├── 05-multi-agent.md
│   ├── 06-agent-memory.md
│   └── 07-agent-safety.md
├── 📁 skills/              # 7 atomic skills
├── 📁 commands/            # 5 slash commands
├── 📁 hooks/
├── 📄 README.md
├── 📄 CHANGELOG.md
└── 📄 LICENSE
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [LICENSE](LICENSE) | License information |

### External Resources

| Resource | Link |
|----------|------|
| LangGraph Docs | https://langchain-ai.github.io/langgraph/ |
| Anthropic Docs | https://docs.anthropic.com/ |
| OpenAI Docs | https://platform.openai.com/docs |
| OWASP LLM Top 10 | https://owasp.org/www-project-top-10-for-large-language-model-applications/ |

---

## 📅 Metadata

| Field | Value |
|-------|-------|
| **Version** | 2.0.0 |
| **Last Updated** | 2025-01-01 |
| **Status** | Production Ready |
| **SASMP** | v1.3.0 |
| **Agents** | 7 |
| **Skills** | 7 |
| **Commands** | 5 |

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

1. Fork the repository
2. Create your feature branch
3. Follow the production patterns in existing agents
4. Submit a pull request

---

## ⚠️ Security

> **Important:** This repository contains patterns for AI agent development.
>
> - ✅ Always implement safety guardrails
> - ✅ Follow OWASP LLM Top 10 guidelines
> - ✅ Test for prompt injection vulnerabilities
> - ✅ Report security issues privately via [Issues](../../issues)

---

## 📝 License

Copyright © 2025 **Dr. Umit Kacar** & **Muhsin Elcicek**

Custom License - See [LICENSE](LICENSE) for details.

---

## 👥 Contributors

<table>
<tr>
<td align="center">
<strong>Dr. Umit Kacar</strong><br/>
Senior AI Researcher & Engineer
</td>
<td align="center">
<strong>Muhsin Elcicek</strong><br/>
Senior Software Architect
</td>
</tr>
</table>

---

<div align="center">

**Made with ❤️ for the Claude Code Community**

[![GitHub](https://img.shields.io/badge/GitHub-pluginagentmarketplace-black?style=for-the-badge&logo=github)](https://github.com/pluginagentmarketplace)

</div>
