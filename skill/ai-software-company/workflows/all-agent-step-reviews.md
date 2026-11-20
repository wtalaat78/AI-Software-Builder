# All-Agent Step Review & Update Workflow

This workflow governs the **Mandatory Step Review Gate** executed by the **CTO (`cto-team-leader`)** across all 32 agents in the organization. It ensures that no lifecycle step is finalized without actively involving all relevant specialists and incorporating their domain updates.

---

## Core Rule & Mandate

> **The CTO must never progress to the next lifecycle step alone or assume passive agreement.**
> At every step, the CTO MUST explicitly poll the designated specialist agents, confirm they reviewed the work, and collect their domain-specific updates, constraints, and verdicts.

---

## Step-by-Step Execution Protocol

### Step 1: Identify Phase Reviewers
At each project stage, the CTO identifies the mandatory review roster:

| Lifecycle Step | Mandatory Reviewer Agents |
| :--- | :--- |
| **1. Intake, Brand & Licensing** | `business-analyst`, `product-manager`, `brand-identity-logo-designer`, `software-license-compliance-specialist`, `market-research-competitor-intelligence`, `finops-cost-pricing-strategist`, `reverse-engineering-feature-analyst` (if applicable), `work-log-archiver` |
| **2. Requirements & Specs** | `business-analyst`, `product-manager`, `solution-architect`, `technical-writer`, `work-log-archiver` |
| **3. Architecture & System Design** | `solution-architect`, `database-engineer`, `backend-developer`, `cloud-infrastructure-engineer`, `cybersecurity-specialist`, `devsecops-security-engineer`, `api-integration-specialist`, `performance-engineer`, `ai-ml-engineer` (if AI), `work-log-archiver` |
| **4. UI/UX Design & Craft Unslopping**| `ui-ux-designer`, `ui-unslop-specialist` (MANDATORY 9-pass gate), `frontend-developer`, `mobile-developer` (if mobile), `desktop-application-developer` (if desktop), `humanization-editorial`, `work-log-archiver` |
| **5. Feature Implementation & Coding** | `frontend-developer`, `backend-developer`, `database-engineer`, `mobile-developer` / `desktop-application-developer`, `api-integration-specialist`, `ai-ml-engineer`, `ui-unslop-specialist`, `performance-engineer`, `work-log-archiver` |
| **6. Verification, QA & Security** | `qa-testing-engineer` ($\ge 90\%$ critical coverage), `code-reviewer`, `cybersecurity-specialist`, `devsecops-security-engineer`, `software-license-compliance-specialist`, `work-log-archiver` |
| **7. Packaging, Documentation & Release**| `technical-writer`, `humanization-editorial`, `social-media-product-marketing`, `presentation-sales-enablement`, `finops-cost-pricing-strategist`, `release-manager`, `work-log-archiver` |

---

### Step 2: The 4-Question Agent Poll
The CTO queries each identified specialist with 4 standardized questions:
1. **Review Confirmation:** *"Have you reviewed the deliverables and code of this current step?"*
2. **Domain Updates:** *"What domain-specific updates, technical requirements, or additions do you mandate from your discipline?"*
3. **Risks & Blockers:** *"Are there any blockers, security vulnerabilities, performance regressions, or compliance violations?"*
4. **Step Verdict:** *"What is your verdict (`APPROVED`, `APPROVED_WITH_COMMENTS`, `CHANGES_REQUESTED`, or `N/A`)?"*

---

### Step 3: Format and Present the Review Sweep
The CTO compiles and displays the review responses in the conversation and project memory:

```markdown
### 📋 Multi-Agent Step Review Sweep — [Step Name]
| Agent | Role | Status | Key Updates / Requirements |
| :--- | :--- | :--- | :--- |
| `solution-architect` | Solution Architect | APPROVED | Verified microservice boundaries and ADR-003. |
| `cybersecurity-specialist`| Security Specialist| CHANGES_REQUESTED | Must add JWT refresh token rotation and rate limiting. |
| `database-engineer` | Database Engineer | APPROVED_WITH_COMMENTS | Ensure composite index on (tenant_id, created_at). |
| `ui-unslop-specialist` | UI Craft Specialist| APPROVED | Passed 9-pass craft audit on 4px grid. |
| `work-log-archiver` | Knowledge Archivist| APPROVED | All actions and telemetry recorded in WORK_LOG.md. |
```

---

### Step 4: Resolve Changes Requested
If any agent returns `CHANGES_REQUESTED`:
1. The CTO pauses progression.
2. The feedback is assigned to the appropriate developer or designer to implement the required changes.
3. The affected specialist re-reviews the modified work.
4. Only when all polled agents are `APPROVED` or `APPROVED_WITH_COMMENTS` does the CTO proceed to the next step.

---

### Step 5: Archival
The `work-log-archiver` commits the completed review matrix to `13-project-memory/STEP_REVIEWS/STEP_XX_REVIEW.md` and appends a summary entry to `WORK_LOG.md`.
