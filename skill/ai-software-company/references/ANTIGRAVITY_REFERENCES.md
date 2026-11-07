# Antigravity implementation references

This package targets the current Antigravity customization model and uses documented paths. Verify the current official docs before upgrading or changing installation behavior.

- Skills: https://antigravity.google/docs/skills
- Customization discovery: https://antigravity.google/docs/customization-discovery
- Custom subagents: https://antigravity.google/docs/subagents
- Rules: https://antigravity.google/docs/rules
- Hooks: https://antigravity.google/docs/hooks
- Features: https://antigravity.google/docs/features
- Getting started: https://antigravity.google/docs/getting-started

Current documented locations:
- Global skill: `~/.gemini/config/skills/<skill-name>/SKILL.md`
- Global custom agents: `~/.gemini/config/agents/<agent-name>.md` or `<agent-name>/agent.md`
- Global rules: `~/.gemini/config/rules/*.md`
- Workspace equivalents: `.agents/skills/`, `.agents/agents/`, `.agents/rules/`

The installer supports global installation and workspace installation. It backs up existing files before replacing them.
