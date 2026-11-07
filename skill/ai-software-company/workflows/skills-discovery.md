# Skills and Tool Discovery Lifecycle

1. **Trigger:** Any specialist agent (e.g. Architect, Backend, QA, Mobile, DevOps) encounters a tooling gap, missing MCP server, or specialized external integration requirement.
2. **Scouting:** The Skills Research Agent queries the Agent Marketplace (`search_marketplace`) using short keyword variants (product name, abbreviation, capability) and explores verified developer resources.
3. **Security & Supply Chain Audit:**
   - Audit maintainer reputation, release frequency, license, and CVE history.
   - Inspect required tool permissions, network egress behavior, environment variable access, and installation scripts.
4. **Duplicate & Overlap Check:** Compare candidate against existing skills in `~/.gemini/config/skills/` and `.agents/skills/` to prevent conflicting instructions.
5. **Installation Strategy Selection:**
   - **Marketplace Path:** Present a 1-sentence rationale and the official `<plugin-card catalog-id="...">` allowing the user to install with 1 click in the Antigravity UI.
   - **Local Custom Skill Path:** If no official skill exists, write a tested, minimal local skill directly into the workspace (`.agents/skills/<name>/SKILL.md`) following the `writing-skills` standard.
   - **CLI / Package Path:** If an external CLI/tool is needed, prepare the exact installation command and rollback command for explicit user approval.
6. **Handoff:** Notify the requesting specialist and CTO with the ready-to-use tool instructions or newly activated capabilities.
