# Vertical Slice Development Workflow

This workflow replaces disconnected horizontal layering (building all DB tables, then all APIs, then all UI in silos) with **End-to-End Vertical Slice Engineering** governed by the **Vertical Domain SME (`vertical-domain-specialist`)** and **CTO (`cto-team-leader`)**.

---

## Core Philosophy: Horizontal Silos vs. Vertical Slices

```
❌ HORIZONTAL SILOING (Leads to integration collapse & domain mismatch):
   [Layer 1: All Database Schemas in isolation]
   [Layer 2: All API Controllers without real domain rules]
   [Layer 3: All Frontend UI screens with mocked or naive data]
   --> Result: Disconnected layers, broken business calculations, missing compliance.

✅ VERTICAL SLICE ARCHITECTURE (Cohesive, working end-to-end features):
   Slice 1: [UI Component] <-> [API Endpoint] <-> [Domain Rules & SME Invariants] <-> [DB Schema] <-> [E2E Test]
   Slice 2: [UI Component] <-> [API Endpoint] <-> [Domain Rules & SME Invariants] <-> [DB Schema] <-> [E2E Test]
   --> Result: Every slice is 100% functional, verified, compliant, and demonstrable immediately.
```

---

## Step-by-Step Vertical Slice Lifecycle

### Step 1: Slice Definition & Vertical SME Review
1. The Product Manager and Business Analyst define a thin, cohesive user capability (e.g., *"Customer deposits funds into wallet with double-entry ledger entry and KYC tier verification"*).
2. The **Vertical Domain SME (`vertical-domain-specialist`)** reviews the slice against `13-project-memory/VERTICAL_DOMAIN_SPEC.md` to specify:
   * **Domain Invariants:** Strict mathematical or regulatory rules (e.g., wallet balance = sum of verified ledger transactions; debits = credits).
   * **Required Industry Fields:** Non-obvious compliance attributes (e.g., currency ISO 4217 code, transaction reference ID, tax breakdown, audit timestamps).
   * **Forbidden Anti-patterns:** Disallowing naive shortcuts (e.g., directly incrementing an integer balance without an immutable ledger entry).

### Step 2: Contract & Data Modeling (Architect + Database Engineer)
1. **Contract First:** The Solution Architect and API Specialist draft the request/response schema (OpenAPI/Zod/TypeScript types).
2. **Schema & Migration:** The Database Engineer defines the exact tables, constraints, foreign keys, and indexes needed solely for this vertical slice.
3. Both ensure database constraints enforce the vertical SME's invariants at the storage layer.

### Step 3: Domain Logic & Backend Implementation
1. The Backend Developer implements the domain model and service logic.
2. Business validation and industry calculations are strictly encapsulated in domain entities, not leaked into frontend code or scattered across handlers.
3. Unit tests are authored immediately, asserting all boundary conditions and domain edge cases.

### Step 4: Frontend UI Implementation & Craft Unslopping
1. The Frontend Developer connects the UI directly to the real slice endpoint (or contract mock if developing in parallel).
2. Realistic industry mock data is used—never generic "Lorem Ipsum" or fake placeholders.
3. **Mandatory UI Unslopping Pass:** The `ui-unslop-specialist` audits and refactors the slice interface across the 9 craft passes (4px grid, quiet chrome, single accent, Lucide line icons, concise copy, type scale, nested radius math).

### Step 5: End-to-End Integration Verification
1. The QA Testing Engineer writes and executes an end-to-end automated integration test:
   * Action triggered via UI / API client.
   * State mutated through domain service.
   * Final record verified directly in the database.
   * Critical business logic unit test coverage verified $\ge 90\%$.
2. The Cybersecurity Specialist validates input sanitization, rate-limiting, and authorization checks.

### Step 6: Vertical SME Sign-Off & All-Agent Step Review
1. The `vertical-domain-specialist` reviews the end-to-end slice implementation to confirm compliance with industry laws, standards, and calculations.
2. The CTO leads the **All-Agent Step Review Sweep** ([workflows/all-agent-step-reviews.md](workflows/all-agent-step-reviews.md)).
3. The `work-log-archiver` logs the verified slice in `13-project-memory/WORK_LOG.md` and transitions the story to `DONE` in `BACKLOG.md`.
4. Only upon 100% completion and verification does the organization begin the next vertical slice.
