# Developer Roadmap Plugin for Claude Code

> **Comprehensive developer learning plugin covering 65+ technology roadmaps from [roadmap.sh](https://roadmap.sh)**

Transform your Claude Code experience into an intelligent learning companion that guides you through complete technology roadmaps with specialized AI agents, interactive skills, and personalized learning paths.

---

## 🚀 Quick Start

### Installation

**Option 1: Direct from GitHub**
```bash
git clone https://github.com/pluginagentmarketplace/custom-plugin-ai-agents.git
cd custom-plugin-ai-agents/custom-plugin-developer-roadmap
```

**Option 2: One-Line Install (Future Marketplace)**
```bash
claude plugin add developer-roadmap
```

### Using the Plugin

Once installed, start with:
```
/learn
```

This opens an interactive guide to choose your learning path from 7 specializations.

---

## 📦 What's Included

### 7 Specialized AI Agents

| Agent | Expertise | Roadmaps Covered |
|-------|-----------|------------------|
| **Frontend Development** | React, Vue, Angular, TypeScript, UI/UX | 10 roadmaps |
| **Backend Development** | Node.js, Spring Boot, APIs, Databases | 8 roadmaps |
| **Mobile Development** | Android, iOS, React Native, Flutter | 6 roadmaps |
| **DevOps & Infrastructure** | Docker, Kubernetes, AWS, Terraform | 7 roadmaps |
| **AI & Data Science** | ML, AI Agents, Data Engineering, MLOps | 9 roadmaps |
| **Programming Languages** | Python, Java, Go, Rust, C++, Algorithms | 9 roadmaps |
| **Architecture & Management** | System Design, Security, Leadership | 16 roadmaps |

**Total: 65+ Technology Roadmaps**

### 30+ Invokable Skills

Each agent has 4-6 specialized skills that are automatically loaded when working with specific technologies:

**Frontend Skills:**
- `react-development` - React hooks, patterns, and best practices
- `typescript-mastery` - Advanced TypeScript with generics
- `css-modern` - Flexbox, Grid, animations, responsive design
- `nextjs-fullstack` - Next.js App Router and Server Components
- `vue-development` - Vue 3 Composition API and Pinia
- `performance-optimization` - Core Web Vitals and optimization

**Backend Skills:**
- `nodejs-api-development` - Express.js and REST APIs
- `spring-boot-development` - Enterprise Java applications
- `graphql-api-design` - GraphQL schemas and resolvers
- `database-architecture` - SQL/NoSQL database design
- `api-security` - Authentication and authorization

**Mobile Skills:**
- `android-kotlin-development` - Jetpack Compose and MVVM
- `ios-swift-development` - SwiftUI and Combine
- `react-native-development` - Cross-platform React Native
- `flutter-development` - Flutter and Dart

**DevOps Skills:**
- `docker-containerization` - Dockerfile and containers
- `kubernetes-orchestration` - K8s deployments and services
- `aws-cloud-architecture` - AWS infrastructure design
- `terraform-iac` - Infrastructure as Code

**AI/Data Skills:**
- `ml-model-development` - Scikit-learn and ML pipelines
- `ai-agent-systems` - LangChain, RAG, autonomous agents
- `python-development` - Modern Python with async/await
- `java-enterprise` - Spring Boot microservices

**Architecture Skills:**
- `software-architecture` - Design patterns and SOLID
- `system-design` - Scalable distributed systems
- `security-engineering` - OWASP and threat modeling
- `database-optimization` - Query optimization and tuning

### 5 Interactive Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/learn` | Start your developer journey | `/learn` |
| `/roadmap` | View technology roadmap | `/roadmap react` |
| `/assess` | Test your knowledge | `/assess python intermediate` |
| `/resources` | Get curated learning materials | `/resources kubernetes` |
| `/project` | Find project ideas | `/project react beginner` |

---

## 🎯 Features

### 1. **Intelligent Agent System**

Agents automatically activate based on your conversation context:

```
User: "Help me build a React dashboard with TypeScript"
→ Frontend Development Agent activates
→ Loads react-development and typescript-mastery skills
→ Provides production-ready code examples
```

### 2. **Comprehensive Roadmaps**

Every roadmap includes:
- ✅ Learning progression (Beginner → Expert)
- ✅ Key technologies and tools
- ✅ Best practices and common pitfalls
- ✅ Project ideas by skill level
- ✅ Career paths and salary ranges
- ✅ Curated resources

### 3. **Hands-On Projects**

100+ project ideas across all technologies:
- **Beginner:** Todo apps, weather dashboards, calculators
- **Intermediate:** E-commerce, chat apps, APIs
- **Advanced:** Microservices, AI systems, scalable platforms

### 4. **Knowledge Assessments**

Test your understanding:
- Quick checks (5-10 questions)
- Comprehensive evaluations (20-30 questions)
- Interview preparation mode
- Hands-on coding challenges
- Personalized recommendations

### 5. **Curated Resources**

For each technology, access:
- Official documentation
- Interactive tutorials
- Video courses (free and paid)
- Books and references
- Community forums and Discord servers
- Certification paths

---

## 📚 Usage Examples

### Frontend Development

```
"I want to learn React"
→ Frontend Agent provides complete React roadmap

"Create a React component with useState and useEffect"
→ react-development skill generates production-ready code

"Optimize my Next.js app for Core Web Vitals"
→ performance-optimization skill provides optimization strategies
```

### Backend Development

```
"Design a RESTful API for a blog"
→ Backend Agent provides API architecture

"Set up JWT authentication in Node.js"
→ nodejs-api-development skill provides implementation

"How do I prevent SQL injection?"
→ api-security skill explains security best practices
```

### DevOps & Infrastructure

```
"Create a Kubernetes deployment for my app"
→ DevOps Agent generates K8s manifests

"Write Terraform code for AWS infrastructure"
→ terraform-iac skill provides IaC templates

"Set up a CI/CD pipeline"
→ Agent guides through GitHub Actions setup
```

### AI & Data Science

```
"Build a customer churn prediction model"
→ AI/Data Agent provides ML pipeline

"Create an AI agent with RAG"
→ ai-agent-systems skill provides LangChain implementation

"Design an ETL pipeline"
→ Agent provides data engineering architecture
```

---

## 🏗️ Plugin Architecture

```
custom-plugin-developer-roadmap/
├── .claude-plugin/
│   └── plugin.json .................. Plugin manifest
│
├── agents/ .......................... 7 specialized agents
│   ├── 01-frontend-development.md
│   ├── 02-backend-development.md
│   ├── 03-mobile-development.md
│   ├── 04-devops-infrastructure.md
│   ├── 05-ai-data-science.md
│   ├── 06-programming-languages.md
│   └── 07-architecture-management.md
│
├── skills/ .......................... 30+ invokable skills
│   ├── react-development/SKILL.md
│   ├── nodejs-api-development/SKILL.md
│   ├── kubernetes-orchestration/SKILL.md
│   ├── ai-agent-systems/SKILL.md
│   └── ... (27 more)
│
├── commands/ ........................ 5 slash commands
│   ├── learn.md
│   ├── roadmap.md
│   ├── assess.md
│   ├── resources.md
│   └── project.md
│
├── hooks/ ........................... Automation hooks
│   └── hooks.json
│
├── scripts/ ......................... Hook scripts
│   ├── auto-load-skills.sh
│   ├── init-project.sh
│   └── generate-recommendations.sh
│
├── README.md ........................ This file
├── ARCHITECTURE.md .................. Technical architecture
└── LICENSE .......................... MIT License
```

---

## 🎓 Learning Paths

### Path 1: Frontend Developer (4-8 months)

1. **Foundations** (1-2 months)
   - HTML, CSS, JavaScript basics
   - Git version control
   - `/roadmap html`, `/roadmap css`, `/roadmap javascript`

2. **React Ecosystem** (2-3 months)
   - React fundamentals and hooks
   - TypeScript integration
   - State management
   - `/roadmap react`, `/roadmap typescript`

3. **Advanced Frontend** (1-3 months)
   - Next.js full-stack
   - Performance optimization
   - Testing strategies
   - `/roadmap nextjs`, `/assess react advanced`

### Path 2: Backend Developer (6-12 months)

1. **Language Choice** (2-3 months)
   - Python, Node.js, or Java
   - Database fundamentals (SQL)
   - `/roadmap python` or `/roadmap nodejs`

2. **API Development** (3-4 months)
   - RESTful API design
   - Authentication and security
   - Database design
   - `/roadmap api-design`, `/roadmap backend`

3. **Production Skills** (2-4 months)
   - Testing and CI/CD
   - Docker and deployment
   - Microservices patterns
   - `/roadmap docker`, `/assess backend advanced`

### Path 3: Full-Stack Developer (8-12 months)

Combine Frontend + Backend paths with:
- `/roadmap full-stack`
- `/project nextjs advanced` (full-stack projects)
- Database and DevOps basics

### Path 4: DevOps Engineer (6-12 months)

1. **Linux & Fundamentals** (2 months)
   - Linux administration, Bash scripting
   - `/roadmap linux`, `/roadmap bash`

2. **Containerization** (2 months)
   - Docker mastery
   - `/roadmap docker`

3. **Orchestration & Cloud** (3-4 months)
   - Kubernetes, AWS
   - Terraform IaC
   - `/roadmap kubernetes`, `/roadmap aws`, `/roadmap terraform`

4. **CI/CD & Automation** (2-3 months)
   - Pipeline design, monitoring
   - `/roadmap devops`, `/assess kubernetes advanced`

### Path 5: Data Scientist / AI Engineer (6-12 months)

1. **Python & Math** (2-3 months)
   - Python programming
   - Statistics and linear algebra
   - `/roadmap python`

2. **Machine Learning** (3-4 months)
   - Supervised/unsupervised learning
   - Model evaluation
   - `/roadmap machine-learning`, `/roadmap data-scientist`

3. **Specialization** (2-4 months)
   - AI Agents, MLOps, or Data Engineering
   - `/roadmap ai-agents`, `/roadmap mlops`, `/roadmap data-engineer`

---

## 🔧 Advanced Usage

### Custom Learning Paths

Create your own roadmap:
```
"I want to become a blockchain developer. Create a custom 6-month learning path."
→ Architecture Agent generates personalized roadmap combining:
   - Programming fundamentals (JavaScript/Solidity)
   - Blockchain concepts
   - Smart contract development
   - Web3 tools
```

### Interview Preparation

```
/assess system-design interview
→ Get real system design interview questions
→ Practice with feedback

/project backend advanced
→ Build portfolio projects
→ Demonstrate real-world skills
```

### Technology Comparison

```
"Should I use React or Vue for my startup?"
→ Frontend Agent compares:
   - Learning curve
   - Ecosystem maturity
   - Job market demand
   - Performance characteristics
```

---

## 📊 Metrics & Coverage

| Metric | Count |
|--------|-------|
| **Technology Roadmaps** | 65+ |
| **AI Agents** | 7 |
| **Invokable Skills** | 30+ |
| **Slash Commands** | 5 |
| **Project Ideas** | 100+ |
| **Learning Hours Covered** | 2000+ |
| **Code Examples** | 500+ |
| **Best Practices** | 200+ |

---

## 🤝 Contributing

This plugin is based on the excellent work from [roadmap.sh](https://roadmap.sh) by [Kamran Ahmed](https://github.com/kamranahmedse).

To contribute:
1. Fork the repository
2. Create a feature branch
3. Add new skills, agents, or commands
4. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🌟 Support

- **GitHub Issues:** [Report bugs or request features](https://github.com/pluginagentmarketplace/custom-plugin-ai-agents/issues)
- **Discussions:** [Ask questions and share ideas](https://github.com/pluginagentmarketplace/custom-plugin-ai-agents/discussions)
- **Roadmap.sh:** Visit [roadmap.sh](https://roadmap.sh) for the original interactive roadmaps

---

## 🎯 Roadmap Coverage

<details>
<summary><b>All 65+ Roadmaps (Click to expand)</b></summary>

### Frontend (10)
- Frontend Developer, Frontend Developer (Beginner)
- React, Vue, Angular, Next.js
- TypeScript, JavaScript, HTML, CSS
- UX Design

### Backend (8)
- Backend Developer, Backend Developer (Beginner)
- API Design
- Node.js, Spring Boot, ASP.NET Core, Laravel, PHP
- GraphQL

### Mobile (6)
- Android, iOS
- React Native, Flutter
- Kotlin, Swift

### DevOps & Infrastructure (7)
- DevOps, DevOps (Beginner)
- Docker, Kubernetes
- AWS, Linux, Terraform, Cloudflare

### AI & Data (9)
- AI Engineer, AI Agents
- Data Scientist, Data Analyst, Data Engineer
- Machine Learning, MLOps
- BI Analyst, Prompt Engineering

### Programming Languages (9)
- Python, Java, Go, Rust, C++
- JavaScript, TypeScript
- Computer Science, Data Structures & Algorithms
- Bash/Shell, SQL

### Architecture & Management (16)
- Software Architect, System Design, Design System
- Cyber Security, Blockchain
- PostgreSQL DBA, MongoDB, Redis
- Product Manager, Engineering Manager
- QA, Technical Writer, DevRel
- Game Developer (Client & Server Side)
- Full Stack

</details>

---

**Start your developer journey today!** 🚀

```
/learn
```
