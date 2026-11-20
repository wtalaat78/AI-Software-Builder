---
trigger: always_on
description: Engineering quality, testing, independent review, evidence-based verdicts, and release gates.
---
# Engineering quality rules
- Target at least 90% meaningful unit-test coverage for critical business logic; use risk-based coverage elsewhere.
- Require appropriate integration, API, UI, end-to-end, regression, compatibility, accessibility, and performance testing.
- Run security assessment on every release candidate and continuous dependency/vulnerability scanning.
- Developers cannot approve their own work. QA and Code Reviewer are independent gates.
- Critical failed tests or unresolved critical vulnerabilities block release.
- Mandatory All-Agent Step Review: At every lifecycle step and milestone, the CTO must ask each relevant specialist agent if they reviewed the step and if they have domain updates, requirements, or objections. Work cannot advance until all requested changes are resolved.
- Record evidence; never claim tests passed unless they were run and results inspected.

# Evidence-based verdicts
- Every review, QA, or security verdict cites: the exact commit SHA examined, the files and areas covered with file:line references, and the commands and tests actually executed with their observed output.
- Use three verdicts only: `VERIFIED` (examined, evidence attached, no open issues), `FINDINGS` (examined, open issues listed with severity), `NOT REVIEWED` (not examined). Anything not examined is reported as `NOT REVIEWED`; absence of findings is never inferred from absence of looking.
- A passing happy-path test suite is not evidence that security controls, failure paths, or unauthorized-access cases behave correctly. Those require their own negative tests.
- When the runtime cannot actually invoke a specialist agent, the CTO records that step as a CTO assessment, never as a specialist sign-off. Simulated or assumed reviews are labeled as such and do not satisfy independent gates.

# Commit-bound sign-offs and staleness
- Every sign-off records: reviewer agent, date, commit SHA, scope covered, and evidence location in the project memory.
- A sign-off is valid only for the commit it examined. Any later commit touching security-sensitive code invalidates the affected sign-offs until re-review. Security-sensitive means: authentication, authorization, sessions/tokens, MFA, cryptography, keys and secrets, network-facing endpoints or proxies, file upload, directory or identity sync, payments, and permission or role models.
- Before any release, milestone readiness claim, or status report, re-check every sign-off against the current commit. Stale sign-offs downgrade status to AMBER until refreshed.

# Fail-closed engineering
- No silent security fallbacks. Missing encryption keys, unavailable TLS verification, bypass or backdoor codes, and default administrative credentials must fail startup or reject the request, never degrade into an insecure default.
- Authorization is enforced at every privileged handler, deny by default. Route and middleware coverage is enumerated and reviewed explicitly, including admin, internal, and "temporary" endpoints.

# Truthful status
- `GREEN` / ready: the current commit carries current `VERIFIED` sign-offs from QA, Code Reviewer, and Security; zero unresolved critical or high findings; no unreviewed security-sensitive component.
- `AMBER`: sign-offs stale, only minor findings open, or known coverage gaps with a dated remediation plan.
- `RED` / `BLOCKED`: unresolved critical or high findings, failed mandatory tests, or any unreviewed security-sensitive component. A RED project is never described as ready, staging-ready, or releasable.
- Terms such as "production-ready" and "enterprise-grade" require GREEN evidence. Otherwise state precisely what is verified, what is not verified, and what remains.
