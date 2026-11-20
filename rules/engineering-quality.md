---
trigger: always_on
description: Engineering quality, testing, independent review, and release gates.
---
# Engineering quality rules
- Target at least 90% meaningful unit-test coverage for critical business logic; use risk-based coverage elsewhere.
- Require appropriate integration, API, UI, end-to-end, regression, compatibility, accessibility, and performance testing.
- Run security assessment on every release candidate and continuous dependency/vulnerability scanning.
- Developers cannot approve their own work. QA and Code Reviewer are independent gates.
- Critical failed tests or unresolved critical vulnerabilities block release.
- Mandatory All-Agent Step Review: At every lifecycle step and milestone, the CTO must ask each relevant specialist agent if they reviewed the step and if they have domain updates, requirements, or objections. Work cannot advance until all requested changes are resolved.
- Record evidence; never claim tests passed unless they were run and results inspected.
