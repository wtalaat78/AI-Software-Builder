# Feature Development Lifecycle

1. **Task Intake & Pre-Development Alignment:**
   - Confirm approved story, acceptance criteria, dependencies, and assigned agent owner.
2. **Interface & Contract Review Sweep:**
   - Solution Architect, API Specialist, Database Engineer, and Cybersecurity Specialist agree on interfaces, schemas, and security controls before implementation starts.
   - Security-sensitive tasks record a Security Task Card — entry points, required authn/authz, controls, and the negative tests that must pass — **before** implementation (see [workflows/security-during-development.md](workflows/security-during-development.md) and [templates/SECURITY_TASK_CARD.md](templates/SECURITY_TASK_CARD.md)).
3. **Bounded Delegation & Implementation:**
   - CTO delegates bounded tasks to frontend/backend/mobile/desktop/database/AI agents.
   - Developers implement code accompanied by automated unit tests, configuration documentation, and the negative security tests from the task card — run in the same change, not deferred.
4. **Mandatory UI Unslopping Pass:**
   - For all user-facing screens and components, the `ui-unslop-specialist` audits and refactors code using the 9-pass [heydamir/unslop](workflows/ui-unslopping.md) methodology (4px grid, quiet chrome, single accent, Lucide line icons, concise copy, type scale, calm layout, micro-details).
5. **Continuous Verification & Security Scans (DevSecOps-owned, build-time):**
   - Run static analysis, automated unit/integration tests (asserting $\ge 90\%$ critical logic coverage), dependency vulnerability scans, and build validation.
   - The `devsecops-security-engineer` owns these checks at build time: they run on every change, they block rather than warn, and each run stores tool, version, commit SHA, and raw output (see [workflows/security-during-development.md](workflows/security-during-development.md)). A check that cannot run in the current runtime is recorded `UNVERIFIED` — never treated as passed.
6. **Independent Quality & Security Gates:**
   - `qa-testing-engineer` independently verifies acceptance criteria, edge cases, accessibility (WCAG 2.1 AA), and regression risk.
   - `code-reviewer` independently reviews diff, maintainability, and architectural conformance. Developers cannot approve their own code.
   - `cybersecurity-specialist` conducts SAST/DAST verification.
7. **MANDATORY ALL-AGENT STEP REVIEW SWEEP:**
   - Before milestone sign-off, the CTO executes an **All-Agent Step Review Sweep** ([workflows/all-agent-step-reviews.md](workflows/all-agent-step-reviews.md)).
   - The CTO queries all involved specialists:
     > *"Have you reviewed the implementation diff, test evidence, and security reports? Do you have any domain updates, requirements, or objections?"*
   - Each agent registers their status (`APPROVED`, `APPROVED_WITH_COMMENTS`, `CHANGES_REQUESTED`). Any requested changes must be resolved before sign-off.
8. **Archival & Handover Update:**
   - `work-log-archiver` commits the review sweep, modified files, commands run, and test coverage to `13-project-memory/WORK_LOG.md` and updates `AGENT_HANDOVER_BRIEFING.md`.
