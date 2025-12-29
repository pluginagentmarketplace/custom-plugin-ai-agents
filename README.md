<div align="center">

<!-- Animated Typing Banner -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=1000&color=2E9EF7&center=true&vCenter=true&multiline=true&repeat=true&width=600&height=100&lines=Ai+Agents+Assistant;7+Agents+%7C+27+Skills;Claude+Code+Plugin" alt="Ai Agents Assistant" />

<br/>

<!-- Badge Row 1: Status Badges -->
[![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge)](https://github.com/pluginagentmarketplace/custom-plugin-ai-agents/releases)
[![License](https://img.shields.io/badge/License-Custom-yellow?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen?style=for-the-badge)](#)
[![SASMP](https://img.shields.io/badge/SASMP-v1.3.0-blueviolet?style=for-the-badge)](#)

<!-- Badge Row 2: Content Badges -->
[![Agents](https://img.shields.io/badge/Agents-7-orange?style=flat-square&logo=robot)](#-agents)
[![Skills](https://img.shields.io/badge/Skills-27-purple?style=flat-square&logo=lightning)](#-skills)
[![Commands](https://img.shields.io/badge/Commands-5-green?style=flat-square&logo=terminal)](#-commands)

<br/>

<!-- Quick CTA Row -->
[📦 **Install Now**](#-quick-start) · [🤖 **Explore Agents**](#-agents) · [📖 **Documentation**](#-documentation) · [⭐ **Star this repo**](https://github.com/pluginagentmarketplace/custom-plugin-ai-agents)

---

### What is this?

> **Ai Agents Assistant** is a Claude Code plugin with **7 agents** and **27 skills** for ai agents development.

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
custom-plugin-ai-agents:04-devops-infrastructure
custom-plugin-ai-agents:07-architecture-management
custom-plugin-ai-agents:01-frontend-development
custom-plugin-ai-agents:05-ai-data-science
custom-plugin-ai-agents:06-programming-languages
... and 2 more
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **7 Agents** | Specialized AI agents for ai agents tasks |
| 🛠️ **27 Skills** | Reusable capabilities with Golden Format |
| ⌨️ **5 Commands** | Quick slash commands |
| 🔄 **SASMP v1.3.0** | Full protocol compliance |

---

## 🤖 Agents

### 7 Specialized Agents

| # | Agent | Purpose |
|---|-------|---------|
| 1 | **04-devops-infrastructure** | DevOps and infrastructure expert specializing in Docker, Kub |
| 2 | **07-architecture-management** | Software architecture, system design, security, and engineer |
| 3 | **01-frontend-development** | Expert in frontend development, UI frameworks, and modern we |
| 4 | **05-ai-data-science** | AI and Data Science expert specializing in machine learning, |
| 5 | **06-programming-languages** | Programming languages expert covering Python, Java, Go, Rust |
| 6 | **02-backend-development** | Backend development expert specializing in API design, datab |
| 7 | **03-mobile-development** | Mobile development expert for Android, iOS, React Native, an |

---

## 🛠️ Skills

### Available Skills

| Skill | Description | Invoke |
|-------|-------------|--------|
| `react-native-development` | Use when building cross-platform mobile apps with React Nati | `Skill("custom-plugin-ai-agents:react-native-development")` |
| `graphql-api-design` | Design efficient GraphQL APIs with schemas, resolvers, and D | `Skill("custom-plugin-ai-agents:graphql-api-design")` |
| `docker-containerization` | Master containerization with Docker multi-stage builds, Comp | `Skill("custom-plugin-ai-agents:docker-containerization")` |
| `database-optimization` | Optimize database performance through indexing, query optimi | `Skill("custom-plugin-ai-agents:database-optimization")` |
| `vue-development` | Vue 3 development using Composition API, reactivity, Vue Rou | `Skill("custom-plugin-ai-agents:vue-development")` |
| `python-development` | Master modern Python development with type hints, async/awai | `Skill("custom-plugin-ai-agents:python-development")` |
| `kubernetes-orchestration` | Orchestrate containerized applications with Deployments, Ser | `Skill("custom-plugin-ai-agents:kubernetes-orchestration")` |
| `ml-model-development` | Build machine learning models with scikit-learn, feature eng | `Skill("custom-plugin-ai-agents:ml-model-development")` |
| `ios-swift-development` | Use when building iOS applications with SwiftUI, Combine, as | `Skill("custom-plugin-ai-agents:ios-swift-development")` |
| `css-modern` | Modern CSS layouts with Flexbox, Grid, animations, responsiv | `Skill("custom-plugin-ai-agents:css-modern")` |
| ... | +17 more | See skills/ directory |

---

## ⌨️ Commands

| Command | Description |
|---------|-------------|
| `/resources` | Learning Resources |
| `/learn` | Start Your Developer Roadmap Journey |
| `/assess` | Knowledge Assessment |
| `/project` | Project Ideas by Skill Level |
| `/roadmap` | View Technology Roadmap |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [LICENSE](LICENSE) | License information |

---

## 📁 Project Structure

<details>
<summary>Click to expand</summary>

```
custom-plugin-ai-agents/
├── 📁 .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── 📁 agents/              # 7 agents
├── 📁 skills/              # 27 skills (Golden Format)
├── 📁 commands/            # 5 commands
├── 📁 hooks/
├── 📄 README.md
├── 📄 CHANGELOG.md
└── 📄 LICENSE
```

</details>

---

## 📅 Metadata

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Last Updated** | 2025-12-29 |
| **Status** | Production Ready |
| **SASMP** | v1.3.0 |
| **Agents** | 7 |
| **Skills** | 27 |
| **Commands** | 5 |

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

1. Fork the repository
2. Create your feature branch
3. Follow the Golden Format for new skills
4. Submit a pull request

---

## ⚠️ Security

> **Important:** This repository contains third-party code and dependencies.
>
> - ✅ Always review code before using in production
> - ✅ Check dependencies for known vulnerabilities
> - ✅ Follow security best practices
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
