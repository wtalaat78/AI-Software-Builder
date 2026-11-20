# Vertical Domain Specification & Industry Compliance Matrix

*Project:* [Agreed Product Name]  
*Industry Sector / Vertical:* [e.g., FinTech / HealthTech / Logistics / E-Commerce / PropTech / LegalTech / EdTech / Telecom]  
*Sub-Vertical / Niche:* [e.g., Multi-Currency Ledger & Micro-Lending / Telehealth Electronic Health Records]  
*Authoring Specialist:* `vertical-domain-specialist` (Vertical Domain SME & Industry Architect)  
*Date & Status:* [YYYY-MM-DD] | `ACTIVE & ENFORCED`

---

## 1. Industry Sector & Regulatory Landscape

* **Primary Vertical:** [e.g., FinTech]
* **Target Jurisdictions:** [e.g., US (Federal & State), EU (GDPR / PSD2), Saudi Arabia (SAMA), Egypt (CBE)]
* **Mandatory Regulatory Standards & Compliance Frameworks:**
  - [e.g., PCI-DSS v4.0 for cardholder data processing]
  - [e.g., SOC 2 Type II for security & availability]
  - [e.g., HIPAA / HITECH for Protected Health Information (PHI)]
  - [e.g., GAAP / IFRS for accounting principles]
  - [e.g., ISO 20022 for financial messaging schemas]
* **Audit & Retention Requirements:** [e.g., 7-year immutable audit log retention, append-only ledger]

---

## 2. Ubiquitous Language & Domain Glossary

*Strictly enforced naming conventions based on Domain-Driven Design (DDD). Developers must use these exact terms in code, variables, database columns, and UI labels:*

| Industry Domain Term | Precise Business Definition | Forbidden / Naive Synonyms (Do Not Use) |
| :--- | :--- | :--- |
| `LedgerEntry` | An immutable record of credit or debit against an account. | `balance_update`, `change_money` |
| `PostingDate` | The official accounting date when funds are recognized. | `time`, `click_date` |
| `Settlement` | The actual transfer of funds between institutions. | `pay_done`, `finished` |
| `ChartOfAccounts` | The structured index of financial accounts. | `category_list`, `account_types` |
| `IdempotencyKey` | Unique UUID guaranteeing an operation occurs exactly once. | `request_id`, `trans_token` |

---

## 3. Core Domain Invariants & Mathematical Rules

*These rules must be enforced in the core domain models and database constraints; never trusted to frontend validation alone:*

1. **Invariant 1 (Double-Entry Balance):** $\sum \text{Debits} = \sum \text{Credits}$ for every recorded transaction event. A transaction cannot be committed if out of balance.
2. **Invariant 2 (Append-Only Immutability):** Financial/Medical records cannot be updated via `UPDATE` or deleted via `DELETE`. Adjustments require a new reversing journal entry.
3. **Invariant 3 (Precision & Currency):** Never use floating-point numbers (`FLOAT` or `DOUBLE`) for currency. Always use exact integer minor units (e.g., cents in `BIGINT`) or `NUMERIC(18, 4)`.
4. **Invariant 4 (State Machine Transitions):** [Strictly defined states, e.g., `Draft -> PendingReview -> Authorized -> Settled -> Archived`. No jumping states.]

---

## 4. Industry Reference Data Models & Standards

*Specify official open standards, schemas, or protocols to adhere to rather than inventing naive schemas:*
* **Standard Schemas Adopted:** [e.g., ISO 20022 camt.053, FHIR R4 Patient Resource, SCORM 2004]
* **Key Entity Relationships:**
  - `Entity 1`: [Definition and mandatory fields]
  - `Entity 2`: [Definition and mandatory fields]

---

## 5. Industry Anti-Patterns & Common Traps (FORBIDDEN IN CODE)

*Explicit developer warnings to prevent naive AI-generated blunders:*
- ❌ **Anti-Pattern 1:** [e.g., Storing raw credit card numbers or CVV in database (Violation of PCI-DSS Requirement 3.2)]
- ❌ **Anti-Pattern 2:** [e.g., Naive balance incrementing without transaction locking (Leads to double-spending race conditions)]
- ❌ **Anti-Pattern 3:** [e.g., Soft-deleting audit logs or bypassing tenant data isolation in multi-tenant queries]

---

## 6. Vertical Slice Delivery Breakdown

*The product decomposed into cohesive, end-to-end vertical slices:*

| Slice # | Slice Title | End-to-End Scope (UI + API + Domain + DB) | Mandatory Domain Invariants Tested |
| :--- | :--- | :--- | :--- |
| **Slice 1** | Account Registration & KYC Verification | KYC intake form $\to$ API $\to$ Identity verification service $\to$ Encrypted storage | KYC Tier 1 validation, DOB verification |
| **Slice 2** | Ledger Account Creation & Chart of Accounts | Account setup UI $\to$ API $\to$ Chart of accounts manager $\to$ Accounts table | Account numbering hierarchy, currency assignment |
| **Slice 3** | Fund Deposit & Balanced Ledger Posting | Deposit modal $\to$ Idempotent API $\to$ Double-entry ledger service $\to$ Posting | Debits = Credits balance, Idempotency lock |
