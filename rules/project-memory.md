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

# Review and approval register
- Keep one register (for example `REVIEWS.md` or `APPROVALS.md`) with one entry per sign-off: reviewer agent, date, commit SHA, scope covered, verdict (`VERIFIED` / `FINDINGS` / `NOT REVIEWED`), and a link or path to the evidence.
- Status files and milestone reports may quote only register entries that are valid for the current commit. Quoting a stale entry without marking it stale is a status-truthfulness violation.
- Record specialist execution provenance: which agent actually ran, the inputs and commit it received, and what it returned. If a role was not executed, log `NOT EXECUTED`; never backfill a plausible verdict.

# Status consistency
- `CURRENT_STATUS.md` must describe the current tree, not the tree as of the last review. `work-log-archiver` cross-checks status claims against the register and the commit history on every milestone and flags drift.
- When code advances past reviewed state, mark affected approvals stale in the same commit that records the new work, so status can never silently lag code.
