# AI Software Development Company — Antigravity Edition

This package implements a 30-role AI software development, reverse engineering, FinOps, brand creation, licensing, and product commercialization organization for Antigravity.

## Contents
- `skill/ai-software-company/SKILL.md`: Master CTO orchestration skill.
- `agents/`: 30 specialized Antigravity custom agents (all formatted with validated YAML frontmatter).
- `rules/`: Company-wide safety, engineering quality (90% test coverage gate), project-memory, and bilingual rules.
- `workflows/`: Repeatable project workflows (new project, development, brand & naming, pricing & FinOps, licensing & entitlement, reverse engineering, market research, marketing, security gate, skills discovery). Also mirrored inside `skill/ai-software-company/workflows/`.
- `templates/`: Project charter, brand brief, FinOps & pricing model, licensing specification, commercial EULA, reverse engineering report, handoff, ADR, milestone, and release checklist templates. Also mirrored inside `skill/ai-software-company/templates/`.
- `scripts/`: Windows PowerShell install, verify, and uninstall scripts.
- `PROMPT_TO_BUILD_AND_VERIFY.md`: Prompt to use inside Antigravity for validation and setup.

## Recommended installation
Windows + Antigravity App and CLI, global scope:
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\Install-AntigravityCompany.ps1 -Scope Global
.\scripts\Verify-AntigravityCompany.ps1 -Scope Global
```

Workspace installation:
```powershell
.\scripts\Install-AntigravityCompany.ps1 -Scope Workspace -WorkspacePath "C:\path\to\your\repo"
.\scripts\Verify-AntigravityCompany.ps1 -Scope Workspace -WorkspacePath "C:\path\to\your\repo"
```

Global paths follow the documented Antigravity locations under `~/.gemini/config/`. Workspace paths use `.agents/`. The package does not install third-party skills, MCP servers, paid services, or execute remote scripts.

## After installation
- In the Antigravity App, open Customizations and confirm the master skill, rules, and all 30 agents are listed.
- In the CLI, use `/skills` and `/agents`; if needed run `/skills reload` or start a new conversation.
- Invoke `/ai-software-company` to start with the CTO intake workflow.
- The custom agents can be delegated to when Antigravity's subagent orchestration is available.

## Specialized Roles & Capabilities
- **App Feature Reverse Engineer (`reverse-engineering-feature-analyst`)**: Reverse engineers applications from an OSINT, public documentation, API telemetry, and black-box behavioral perspective, creating complete functional specifications and workflow maps.
- **Code & Binary Reverse Engineer (`reverse-engineering-code-specialist`)**: Decompiles and deobfuscates compiled packages (APKs, .NET, Wasm, minified JS bundles, native binaries), extracts database schemas and proprietary algorithms, and authors clean-room modernized source code.
- **Brand Identity & Logo Designer (`brand-identity-logo-designer`)**: Generates product naming candidates (bilingual Arabic & English), brand identity briefs, WCAG 2.1 AA color tokens, typography systems, and detailed generation briefs for Antigravity's built-in `image-generator` subagent to produce visual logos and app icons.
- **FinOps & Pricing Strategist (`finops-cost-pricing-strategist`)**: Models cloud TCO across AWS/GCP/Azure/Oracle, database/compute sizing, LLM token unit costs, and generates SaaS pricing packages (Free, Pro, Enterprise) with gross margin modeling ($\ge 75\%$).
- **Software Licensing & Compliance Specialist (`software-license-compliance-specialist`)**: Defines product code/SKU taxonomy, license types (perpetual, subscription, node-locked HWID, floating, trial), client request payloads, central License Generator Server contracts, and commercial EULA agreements.
- **Market Research & Competitor Intelligence (`market-research-competitor-intelligence`)**: Analyzes competitor feature matrices, pricing tiers, customer pain points, and translates validated gaps into differentiated roadmap features.

## Important limitations
A skill and custom-agent definitions are configuration/instructions, not a guarantee that 30 independent processes run continuously. The CTO must use the orchestration capabilities actually exposed by the installed Antigravity version. GitHub/GitLab integrations, social publishing, advertising, cloud deployments, and other external actions require separately configured integrations and credentials. Approval gates remain mandatory.

## Safety
Production deployment, destructive database changes, production infrastructure changes, major architecture changes, paid services, scope/budget changes, and security-policy changes require explicit user approval. Third-party skill installation requires explicit approval after security review.
