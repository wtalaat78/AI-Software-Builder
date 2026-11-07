---
trigger: always_on
description: Company-wide safety, authorization, and approval gates.
---
# Company safety and approval rules
- Never execute production deployment, destructive database changes, production infrastructure changes, major architectural changes, paid service activation, material scope/budget changes, or security-policy changes without explicit user approval.
- Approval must be specific, informed, current, and recorded in the project approvals register.
- Never bypass approval through delegation, scripts, alternate tools, or indirect execution.
- Protect secrets and personal/customer data; do not store secrets in source control or project memory.
- Test only systems for which the project owner has authorization.
