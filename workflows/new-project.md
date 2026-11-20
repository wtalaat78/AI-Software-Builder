# New Project Intake & Pre-Coding Agreement

1. **Intake Interview (English by default):**
   - CTO interviews the user about the software: purpose, target users/market, key features, platform targets (Web, Mobile, Desktop, API), and timeline/constraints.
   - **MANDATORY LICENSING INTAKE QUESTION:** The CTO MUST ask:
     > *"Does this software require licensing integration (e.g., product code/SKU taxonomy, License Generator Server activation, hardware ID / HWID node-locking, subscription key validation, trial restrictions), or is it un-licensed, internal, or pure SaaS?"*
2. **Entity, Brand & Licensing Discovery:**
   - Gather or confirm the **Owner Company Name** (corporate entity, founder, or organization owning the IP).
   - Involve the `brand-identity-logo-designer` to generate **Product Name** options with semantic meaning, domain/handle viability, and phonetic strength.
   - Formulate **Logo and visual brand concepts** (providing prompts for Antigravity's `image-generator` subagent).
   - Involve `market-research-competitor-intelligence` for competitor feature/pricing benchmarks and `finops-cost-pricing-strategist` for early infrastructure cost models.
   - If licensing is required, involve the `software-license-compliance-specialist` to define the product code schema, license types, request mechanism (`.req`/JSON), and License Generator Server contract (see `workflows/license-and-entitlement.md`).
3. **MANDATORY PRE-CODING GATE (Brand, Entity & Licensing Agreement):**
   - Present the proposed:
     * **Owner Company Name**
     * **Agreed Product Name**
     * **Approved Logo & Visual Concept**
     * **Agreed Licensing Integration Strategy** (License Generator Server + HWID activation, perpetual/subscription terms, or explicitly confirmed N/A)
   - **HARD BLOCKER:** No source code generation, repository scaffolding, database creation, or implementation may begin until the user explicitly reviews and agrees to all four items.
4. **MANDATORY ALL-AGENT STEP REVIEW SWEEP:**
   - Before completing intake and transitioning to architecture/implementation, the CTO executes an **All-Agent Step Review Sweep** ([workflows/all-agent-step-reviews.md](workflows/all-agent-step-reviews.md)).
   - The CTO explicitly asks `business-analyst`, `product-manager`, `brand-identity-logo-designer`, `software-license-compliance-specialist`, `market-research-competitor-intelligence`, `finops-cost-pricing-strategist`, and `work-log-archiver`:
     > *"Have you reviewed the intake, branding, and licensing strategy? Do you have any updates or requirements from your domain?"*
   - All agent feedback and updates are recorded in `13-project-memory/WORK_LOG.md`.
5. **Planning & Architecture:**
   - Once all intake reviews are approved, the Business Analyst crafts the BRD/acceptance criteria, the Product Manager creates the MVP roadmap, and the Solution Architect establishes ADRs and data models.
6. **Workspace Setup & Development:**
   - Create the project workspace directories, project charter, backlog, and handoffs, and commence development.
