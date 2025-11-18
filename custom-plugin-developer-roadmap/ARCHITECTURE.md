# Plugin Architecture

Technical architecture and design decisions for the Developer Roadmap Plugin.

---

## Overview

The Developer Roadmap Plugin is a comprehensive Claude Code plugin that provides intelligent learning guidance across 65+ technology roadmaps. It uses a multi-agent architecture with specialized skills and interactive commands.

---

## Design Principles

### 1. **Modularity**
- Each agent is independent and specialized
- Skills are reusable across agents
- Commands are standalone and composable

### 2. **Discoverability**
- Trigger words automatically activate relevant agents
- Skills load contextually based on conversation
- Commands provide clear entry points

### 3. **Scalability**
- Easy to add new roadmaps, agents, or skills
- Agent system supports unlimited specializations
- Plugin can grow with new technologies

### 4. **User-Centric**
- Learning paths tailored to skill level
- Interactive assessments provide feedback
- Resources curated for practical learning

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Claude Code                         │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│              Developer Roadmap Plugin                   │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │         plugin.json (Manifest)                 │    │
│  │  - Agent definitions                           │    │
│  │  - Skill registry                              │    │
│  │  - Command mappings                            │    │
│  │  - Trigger words                               │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Agents     │  │   Skills     │  │  Commands    │ │
│  │   (7 MD      │  │   (30+ MD    │  │  (5 MD       │ │
│  │   files)     │  │   files)     │  │  files)      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│  ┌──────────────┐  ┌──────────────────────────────────┐│
│  │   Hooks      │  │        Scripts                   ││
│  │   (JSON)     │  │        (Bash automation)         ││
│  └──────────────┘  └──────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                  User Interaction                       │
│  - Natural language queries                             │
│  - Slash commands                                       │
│  - Code generation requests                             │
└─────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Agents (7 Specialized AI Agents)

**Purpose:** Provide domain expertise for specific technology areas

**Structure:**
```markdown
---
description: Agent specialization
capabilities: [List of capabilities]
---

# Agent Name

## When to Use This Agent
[Trigger scenarios]

## Core Expertise
[Technologies and patterns]

## Skill Areas
[Linked skills]

## Example Use Cases
[Practical examples]

## Learning Path Support
[Beginner → Expert progression]

## Best Practices
[Industry standards]

## Collaboration
[How this agent works with others]
```

**Agent Design Decisions:**

1. **Frontend Development Agent**
   - **Rationale:** 10 roadmaps (React, Vue, Angular, etc.) share UI/UX concepts
   - **Triggers:** `react`, `vue`, `angular`, `frontend`, `component`, `ui`, `css`
   - **Skills:** 6 frontend-focused skills
   - **Coverage:** Client-side development, modern frameworks, performance

2. **Backend Development Agent**
   - **Rationale:** 8 roadmaps (Node.js, Spring Boot, etc.) share API/database patterns
   - **Triggers:** `backend`, `api`, `nodejs`, `database`, `microservices`
   - **Skills:** 5 backend-focused skills
   - **Coverage:** Server-side logic, APIs, databases, security

3. **Mobile Development Agent**
   - **Rationale:** 6 roadmaps for native and cross-platform mobile
   - **Triggers:** `mobile`, `android`, `ios`, `flutter`, `react native`
   - **Skills:** 4 mobile platform skills
   - **Coverage:** Android, iOS, cross-platform frameworks

4. **DevOps & Infrastructure Agent**
   - **Rationale:** 7 roadmaps for deployment and operations
   - **Triggers:** `devops`, `docker`, `kubernetes`, `aws`, `terraform`, `ci/cd`
   - **Skills:** 4 infrastructure skills
   - **Coverage:** Containers, orchestration, cloud, IaC

5. **AI & Data Science Agent**
   - **Rationale:** 9 roadmaps for ML, data engineering, analytics
   - **Triggers:** `ai`, `machine learning`, `data science`, `mlops`, `prompt engineering`
   - **Skills:** 4 AI/data skills
   - **Coverage:** ML models, AI agents, data pipelines, analytics

6. **Programming Languages Agent**
   - **Rationale:** 9 roadmaps for languages and CS fundamentals
   - **Triggers:** `python`, `java`, `go`, `rust`, `algorithm`, `data structure`
   - **Skills:** 4 programming skills
   - **Coverage:** Language mastery, algorithms, type systems

7. **Architecture & Management Agent**
   - **Rationale:** 16 roadmaps for system design, security, leadership
   - **Triggers:** `architecture`, `system design`, `security`, `product manager`, `scalability`
   - **Skills:** 4 architecture skills
   - **Coverage:** Design patterns, distributed systems, security, leadership

### 2. Skills (30+ Invokable Skills)

**Purpose:** Provide deep, focused expertise in specific technologies

**Structure (SKILL.md):**
```markdown
---
name: skill-id
description: When to use this skill (max 150 chars)
---

# Skill Name

## Quick Start
[Immediate practical example]

## Key Concepts
[2-3 fundamental concepts with code]

## Common Patterns
[3-4 production-ready patterns]

## Best Practices
[Industry standards]

## Common Pitfalls
[What to avoid]

## Resources
[Links to docs, tutorials]
```

**Skill Design Decisions:**

- **Granularity:** Each skill focuses on ONE technology or pattern
  - ✅ `react-development` - focused on React
  - ❌ `frontend-frameworks` - too broad

- **Reusability:** Skills can be invoked by multiple agents
  - `python-development` used by both AI/Data and Programming agents

- **Practical Focus:** Every skill includes production-ready code examples
  - Real implementations, not toy examples
  - Error handling, TypeScript types, best practices

- **Progressive Disclosure:**
  - Quick Start: Immediate value (copy-paste ready)
  - Key Concepts: Understanding the "why"
  - Common Patterns: Real-world scenarios
  - Best Practices: Professional standards

### 3. Commands (5 Interactive Slash Commands)

**Purpose:** Provide structured entry points for learning workflows

**Structure:**
```markdown
# Command Title

Usage examples and description

## Interactive Content
[Guides, examples, recommendations]
```

**Command Design Decisions:**

1. **/learn** - Discovery & Onboarding
   - **Purpose:** Help users find their learning path
   - **Output:** Overview of 7 specializations
   - **Next Actions:** Invoke agents or use other commands

2. **/roadmap [technology]** - Roadmap Viewer
   - **Purpose:** Display comprehensive learning path
   - **Output:** Beginner → Expert progression, resources, projects
   - **Parameterized:** Accepts any of 65+ technology names

3. **/assess [technology] [level]** - Knowledge Testing
   - **Purpose:** Identify skill gaps and track progress
   - **Output:** Quiz questions, score, personalized recommendations
   - **Modes:** Quick check, comprehensive, interview prep, coding challenge

4. **/resources [technology] [type]** - Resource Finder
   - **Purpose:** Curated learning materials
   - **Output:** Docs, tutorials, courses, books, communities
   - **Filtered:** By resource type (docs, videos, books, etc.)

5. **/project [technology] [level]** - Project Ideas
   - **Purpose:** Hands-on learning through building
   - **Output:** Project ideas with tech stack, features, time estimates
   - **Leveled:** Beginner, intermediate, advanced, expert

### 4. Hooks & Scripts

**Purpose:** Automate workflows and enhance user experience

**Hook Types:**

1. **onAgentInvoke** - Auto-load relevant skills
   ```bash
   # When Frontend Agent is invoked:
   → Load: react-development, typescript-mastery, css-modern, etc.
   ```

2. **onProjectCreate** - Initialize project structure
   ```bash
   # User: "/project react beginner"
   → Scaffold: npx create-next-app with TypeScript + Tailwind
   ```

3. **onAssessmentComplete** - Generate recommendations
   ```bash
   # After assessment:
   → Analyze score
   → Generate personalized learning plan
   → Suggest resources and projects
   ```

---

## Data Flow

### User Query → Agent Activation

```
┌─────────────────┐
│ User Query      │
│ "Build a React  │
│  dashboard"     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Trigger Match   │
│ "react" keyword │
│ detected        │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ Frontend Agent Invoked  │
│ - Loads agent MD file   │
│ - Activates hook        │
└────────┬────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Auto-load Skills         │
│ - react-development      │
│ - typescript-mastery     │
│ - performance-optimization│
└────────┬─────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Generate Response       │
│ - Use agent knowledge   │
│ - Apply skill patterns  │
│ - Provide code examples │
└─────────────────────────┘
```

### Slash Command Execution

```
┌──────────────────┐
│ User Command     │
│ /roadmap react   │
└────────┬─────────┘
         │
         ▼
┌─────────────────────┐
│ Command Parser      │
│ - Command: roadmap  │
│ - Param: react      │
└────────┬────────────┘
         │
         ▼
┌────────────────────────┐
│ Load Command MD        │
│ commands/roadmap.md    │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────────┐
│ Process Template           │
│ - Replace [technology]     │
│ - Fetch roadmap data       │
│ - Format output            │
└────────┬───────────────────┘
         │
         ▼
┌────────────────────────────┐
│ Display Result             │
│ - Learning path            │
│ - Key skills               │
│ - Projects & resources     │
└────────────────────────────┘
```

---

## Technology Stack

### Plugin Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Agents** | Markdown + YAML frontmatter | Agent definitions |
| **Skills** | Markdown + YAML frontmatter | Skill documentation |
| **Commands** | Markdown | Interactive commands |
| **Hooks** | JSON configuration | Automation triggers |
| **Scripts** | Bash | Hook implementations |
| **Manifest** | JSON | Plugin metadata |

### Claude Code Integration

- **Agent System:** Uses Claude Code's native agent framework
- **Skills:** Invokable via skill name
- **Commands:** Slash command prefix (`/`)
- **Hooks:** Event-driven automation
- **Triggers:** Keyword-based agent activation

---

## Scalability Considerations

### Adding New Roadmaps

1. **Identify the specialization** (frontend, backend, etc.)
2. **Update relevant agent** with new roadmap information
3. **Create skill if needed** (if technology is significantly different)
4. **Update plugin.json** with new skill reference
5. **Add to /learn command** roadmap list

### Adding New Agents

1. **Create agent MD file** in `agents/`
2. **Define 3-5 specialized skills** in `skills/`
3. **Update plugin.json:**
   ```json
   {
     "agents": [
       {
         "id": "new-agent",
         "name": "New Agent",
         "description": "...",
         "file": "agents/08-new-agent.md",
         "triggers": ["keyword1", "keyword2"]
       }
     ]
   }
   ```
4. **Add hook script** for auto-loading skills
5. **Update /learn command** with new specialization

### Adding New Commands

1. **Create command MD file** in `commands/`
2. **Update plugin.json:**
   ```json
   {
     "commands": [
       {
         "name": "new-command",
         "description": "...",
         "file": "commands/new-command.md",
         "usage": "/new-command [params]"
       }
     ]
   }
   ```
3. **Test command execution**

---

## Performance Optimizations

### 1. Lazy Loading
- Skills load on-demand, not upfront
- Reduces initial context size
- Faster agent activation

### 2. Trigger Optimization
- Specific keywords prevent false activations
- Multiple trigger words increase coverage
- Balanced between precision and recall

### 3. Content Organization
- Quick Start sections provide immediate value
- Progressive disclosure (simple → complex)
- Markdown formatting optimized for readability

---

## Security Considerations

### 1. Script Safety
- All hook scripts are sandboxed
- No external API calls without user consent
- File operations limited to project directory

### 2. Data Privacy
- No personal data collected
- Assessment scores stored locally (if implemented)
- No telemetry or tracking

### 3. Code Generation
- Generated code follows security best practices
- Includes input validation examples
- Warns about common vulnerabilities (SQL injection, XSS, etc.)

---

## Future Enhancements

### Planned Features

1. **Progress Tracking**
   - Save assessment scores
   - Track learning milestones
   - Visualize skill progression

2. **Personalized Recommendations**
   - AI-powered learning path generation
   - Based on career goals and current skills
   - Adaptive difficulty

3. **Community Features**
   - Share custom learning paths
   - Collaborative projects
   - Peer code reviews

4. **Integration with Platforms**
   - GitHub repository analysis
   - LeetCode problem recommendations
   - Course platform integration (Udemy, Coursera)

5. **Advanced Assessments**
   - Real coding challenges (auto-graded)
   - System design interviews with feedback
   - Portfolio project reviews

---

## Maintenance

### Regular Updates

1. **Roadmap Updates** (Monthly)
   - Sync with roadmap.sh changes
   - Add new technologies
   - Update best practices

2. **Code Examples** (Quarterly)
   - Update to latest framework versions
   - Add new patterns and libraries
   - Deprecate outdated practices

3. **Resources** (Monthly)
   - Verify link validity
   - Add new courses and tutorials
   - Update pricing and availability

---

## Testing Strategy

### Manual Testing
- ✅ Each agent activates with correct triggers
- ✅ Skills load contextually
- ✅ Commands execute with parameters
- ✅ Hooks trigger on events
- ✅ Scripts execute without errors

### Validation
- ✅ YAML frontmatter is valid
- ✅ JSON files are well-formed
- ✅ Markdown renders correctly
- ✅ Links are not broken
- ✅ Code examples are syntactically correct

---

## License

MIT License - See LICENSE file

---

**Last Updated:** 2025-01-18

For questions or suggestions, open an issue on GitHub.
