# Contributing to AI Agents Plugin

Thank you for your interest in contributing!

## How to Contribute

1. **Fork** the repository
2. **Create** your feature branch (`git checkout -b feature/amazing-feature`)
3. **Follow** the Golden Format for new skills
4. **Test** your changes thoroughly
5. **Commit** your changes (`git commit -m 'feat: Add amazing feature'`)
6. **Push** to the branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

## Guidelines

### Code Standards
- Follow existing code style
- Add comments for complex logic
- Update documentation as needed

### Agent Development
- Use YAML frontmatter with required fields
- Include `sasmp_version: "1.3.0"`
- Add `eqhm_enabled: true`

### Skill Development
- Follow Golden Format structure:
  ```
  skills/skill-name/
  ├── SKILL.md
  ├── assets/
  ├── scripts/
  └── references/
  ```
- Include bonded_agent reference

### Testing
- Test all new features locally
- Verify agent/skill bonding
- Check plugin validation passes

## Questions?

Open an issue for any questions or suggestions.

---

© 2025 Dr. Umit Kacar & Muhsin Elcicek. All Rights Reserved.
