# Work Logging and Knowledge Archiving Workflow

This workflow is executed by the **Work Log & Knowledge Archivist (`work-log-archiver`)** under CTO orchestration to maintain persistent, chronological project history, enable rapid stakeholder review, and guarantee seamless context recovery during AI agent/model transitions.

---

## Triggers

1. **Task / Feature Completion:** Immediately after any specialist agent completes an assigned ticket, bugfix, design, or test suite.
2. **Milestone Sign-Off:** When a project reaches a formal phase transition (e.g., Discovery $\to$ Architecture $\to$ Implementation $\to$ QA $\to$ Release).
3. **AI Agent / Model Switch:** Whenever the user switches models, Antigravity compacts session memory, a new subagent takes over, or a human engineer steps in.
4. **Significant Technical Decision:** When an Architecture Decision Record (ADR) or critical configuration change occurs.

---

## Step-by-Step Archiving Procedure

### Step 1: Capture Execution Telemetry
The archiver gathers factual execution data from the executing agent:
* **Executing Agent:** Identity and role (e.g., `backend-developer`, `database-engineer`).
* **Task Objective:** Ticket ID, user story, or bug summary.
* **Files Affected:** Complete file paths and operation types (`Created`, `Modified`, `Deleted`, `Read`).
* **Commands Run:** Exact terminal/CLI commands, flags, and exit codes ($0$ for success, non-zero for failures).
* **Test & Verification Results:** Test framework run, number of passing/failing tests, assertions verified, code coverage achieved.
* **Key Decisions & Rationale:** Why an approach was chosen over alternatives.
* **Blockers / Risks / Open Decisions:** Any newly identified impediments or pending approvals.

### Step 2: Format Standard Log Entry
Structure the collected information using the unified Work Log format:

```markdown
### [YYYY-MM-DD HH:MM:SS] Task: <Task Title> (<Ticket ID>)
* **Agent:** `<agent-name>` (`<Role Description>`)
* **Objective:** <One-sentence summary of the task goal>
* **Files Touched:**
  - `Created`: `<path/to/file>`
  - `Modified`: `<path/to/file>` (lines X-Y)
* **Commands Executed:**
  - `<command string>` (Exit code: 0)
* **Verification & Test Evidence:**
  - `<test command>`: X passed, 0 failed. Coverage: Y%.
* **Decisions & Rationale:**
  - <Technical decision made and why>
* **Status & Next Steps:**
  - Status: `COMPLETED` | `IN_PROGRESS` | `BLOCKED`
  - Next: `<specific next task and assigned role>`
```

### Step 3: Append to Project Memory
1. Append the formatted entry to `13-project-memory/WORK_LOG.md`.
2. For long-running projects, archive daily logs under `13-project-memory/work-logs/YYYY-MM-DD.md`.
3. Verify that zero plaintext credentials, private keys, or personal tokens are included.

### Step 4: Synchronize Project Status Boards
1. Update `13-project-memory/CURRENT_STATUS.md` with:
   * Current active phase and milestone status.
   * Last completed item and timestamp.
   * Currently active task and owner.
2. Update `13-project-memory/BACKLOG.md` to transition completed items to `DONE`.

---

## AI Agent Switching & Continuity Protocol

When an AI agent or model is changed (e.g., switching from one model to another, resuming after context compaction, or reviving stopped subagents):

### A. Pre-Handoff Archival (Outgoing Agent)
The outgoing agent or archiver compiles `13-project-memory/AGENT_HANDOVER_BRIEFING.md`:
1. **Executive Snapshot:** Current product state, approved brand name, agreed licensing model, and active sprint goal.
2. **Work Accomplished:** Concise summary of all verified and tested components.
3. **In-Flight Tasks:** Exact code lines or modules currently being modified.
4. **Immediate Next Step:** The single next action the successor agent must execute.
5. **Known Pitfalls & Constraints:** Unmet edge cases, non-working tests, or environment quirks.

### B. Post-Handoff Ingestion (Incoming Agent)
The newly initialized agent follows this rapid 4-step onboarding sequence:
1. **Read `AGENT_HANDOVER_BRIEFING.md`:** Absorb current state, active constraints, and immediate objectives.
2. **Review the Last 3-5 Entries in `WORK_LOG.md`:** Understand the exact chronological sequence leading to the handoff.
3. **Verify Local Environment:**
   - Run `git status` to inspect modified/untracked files.
   - Run existing automated test suite to confirm baseline green state.
4. **Resume Execution:** Pick up the immediate next task without asking the user to repeat already documented context.
