---
trigger: model_decision
description: Use when creating, updating, or resuming a software project and its persistent memory.
---
# Persistent project memory
- Store durable decisions, status, backlog, risks, approvals, and handoffs in project files, not only chat.
- Chronologically record every agent action, file modification, terminal command, and test result in `WORK_LOG.md` (managed by `work-log-archiver`) for fast review and auditability.
- Maintain an up-to-date `AGENT_HANDOVER_BRIEFING.md` so any incoming AI agent or new model can immediately resume in-flight work with 100% context fidelity.
- Use Git for source history and Markdown for project memory.
- Do not commit secrets, credentials, private keys, or sensitive customer data.
- Update CURRENT_STATUS.md and relevant handoff/decision files after each major milestone.
