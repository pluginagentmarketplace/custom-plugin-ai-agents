# Contributing to Ai Agents Plugin

Thank you for your interest in contributing! This document provides guidelines for contributing to this plugin.

## How to Contribute

### 1. Fork & Clone

```bash
git clone https://github.com/pluginagentmarketplace/custom-plugin-ai-agents.git
cd custom-plugin-ai-agents
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes

- Follow the existing code style
- Add tests if applicable
- Update documentation

### 4. Commit

```bash
git add .
git commit -m "feat: your feature description"
```

### 5. Push & Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Guidelines

### Code Style

- Use consistent formatting
- Add comments for complex logic
- Follow naming conventions

### Commit Messages

Use conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring
- `test:` - Adding tests

### Pull Requests

- Clear description of changes
- Reference related issues
- Keep changes focused

## Golden Format for Skills

When adding new skills, follow the Golden Format:

```
skills/skill-name/
├── SKILL.md          # Skill definition with YAML frontmatter
├── assets/           # Templates, configs, schemas
├── scripts/          # Automation scripts
└── references/       # Documentation, guides
```

## Questions?

Open an issue for questions or suggestions.

---

**Built by Dr. Umit Kacar & Muhsin Elcicek**
