# AI Software Development Company — Antigravity Edition

This package implements a 33-role AI software development, vertical domain SME engineering, reverse engineering, FinOps, brand creation, licensing, UI unslopping craft, work log archiving, and product commercialization organization for Antigravity.

## Contents
- `skill/ai-software-company/SKILL.md`: Master CTO orchestration skill.
- `agents/`: 33 specialized Antigravity custom agents (all formatted with validated YAML frontmatter).
- `rules/`: Company-wide safety, engineering quality (90% test coverage gate, all-agent step review gate), project-memory, and bilingual rules.
- `workflows/`: Repeatable project workflows (new project, development, vertical-slice-development, all-agent-step-reviews, work-logging-and-archiving, ui-unslopping, brand & naming, pricing & FinOps, licensing & entitlement, reverse engineering, market research, marketing, security gate, skills discovery). Also mirrored inside `skill/ai-software-company/workflows/`.
- `templates/`: Security review report, project charter, vertical domain specification, work log, all-hands step review matrix, agent handover briefing, brand brief, FinOps & pricing model, licensing specification, commercial EULA, unslop audit report, reverse engineering report, handoff, ADR, milestone, and release checklist templates. Also mirrored inside `skill/ai-software-company/templates/`.
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
- In the Antigravity App, open Customizations and confirm the master skill, rules, and all 33 agents are listed.
- In the CLI, use `/skills` and `/agents`; if needed run `/skills reload` or start a new conversation.
- Invoke `/ai-software-company` to start with the CTO intake workflow.
- The custom agents can be delegated to when Antigravity's subagent orchestration is available.

## Specialized Roles & Capabilities
- **Vertical Domain SME & Industry Architect (`vertical-domain-specialist`)**: Bridges the critical vertical know-how gap. Identifies target industry sectors (FinTech, HealthTech, Logistics, E-Commerce, Legal, PropTech, EdTech, Telecom), injects mandatory regulatory standards (HIPAA, PCI-DSS, SOX, GAAP, ISO 20022), authors ubiquitous language domain specifications, and enforces end-to-end Vertical Slice Architecture (UI $\leftrightarrow$ API $\leftrightarrow$ Domain $\leftrightarrow$ DB $\leftrightarrow$ Tests) to eliminate horizontal integration breakdown.
- **CTO & Team Leader (`cto-team-leader`) with Mandatory All-Agent Step Review**: Orchestrates the 33-role organization. Mandates an explicit Multi-Agent Step Review Sweep at every lifecycle phase, polling each relevant specialist for domain updates and blocking flags before proceeding.
- **Work Log & Knowledge Archivist (`work-log-archiver`)**: Chronologically records all agent actions, touched files, commands, and test verification results in `WORK_LOG.md` and maintains `AGENT_HANDOVER_BRIEFING.md` snapshots for rapid human review and instant, zero-loss context resumption during AI agent or model transitions.
- **UI Unslopping & Craft Specialist (`ui-unslop-specialist`)**: Enforces the 9-pass design craft methodology from [heydamir/unslop](https://github.com/heydamir/unslop) (spacing on 4px grid, quiet tinted-neutral chrome, single accent, Lucide line icons, concise copy, type scale, calm layout, micro-details, single bright moment) across all UI implementations as a mandatory gate before QA.
- **App Feature Reverse Engineer (`reverse-engineering-feature-analyst`)**: Reverse engineers applications from an OSINT, public documentation, API telemetry, and black-box behavioral perspective, creating complete functional specifications and workflow maps.
- **Code & Binary Reverse Engineer (`reverse-engineering-code-specialist`)**: Decompiles and deobfuscates compiled packages (APKs, .NET, Wasm, minified JS bundles, native binaries), extracts database schemas and proprietary algorithms, and authors clean-room modernized source code.
- **Brand Identity & Logo Designer (`brand-identity-logo-designer`)**: Generates product naming candidates (bilingual Arabic & English), brand identity briefs, WCAG 2.1 AA color tokens, typography systems, and detailed generation briefs for Antigravity's built-in `image-generator` subagent to produce visual logos and app icons.
- **FinOps & Pricing Strategist (`finops-cost-pricing-strategist`)**: Models cloud TCO across AWS/GCP/Azure/Oracle, database/compute sizing, LLM token unit costs, and generates SaaS pricing packages (Free, Pro, Enterprise) with gross margin modeling ($\ge 75\%$).
- **Software Licensing & Compliance Specialist (`software-license-compliance-specialist`)**: Defines product code/SKU taxonomy, license types (perpetual, subscription, node-locked HWID, floating, trial), client request payloads, central License Generator Server contracts, and commercial EULA agreements.
- **Market Research & Competitor Intelligence (`market-research-competitor-intelligence`)**: Analyzes competitor feature matrices, pricing tiers, customer pain points, and translates validated gaps into differentiated roadmap features.

## Important limitations
A skill and custom-agent definitions are configuration/instructions, not a guarantee that 33 independent processes run continuously. The CTO must use the orchestration capabilities actually exposed by the installed Antigravity version. GitHub/GitLab integrations, social publishing, advertising, cloud deployments, and other external actions require separately configured integrations and credentials. Approval gates remain mandatory.

## Safety
Production deployment, destructive database changes, production infrastructure changes, major architecture changes, paid services, scope/budget changes, and security-policy changes require explicit user approval. Third-party skill installation requires explicit approval after security review.
