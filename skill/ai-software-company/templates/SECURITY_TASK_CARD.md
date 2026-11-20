# Security Task Card — <task or change name>

- Task/change:
- Commit SHA(s):
- Implementer:
- Independent reviewer (not the implementer):
- Security-sensitive surface: `yes` / `N/A — no security-sensitive surface`

Security-sensitive means: authentication, authorization, sessions/tokens, MFA, cryptography, keys and secrets, network-facing endpoints or proxies, file upload, directory or identity sync, payments, permission or role models.

## Entry points added or changed

| Entry point (route / handler / job / webhook / upload / admin) | Authn + authz required | Enforced at (file:line) |
|---|---|---|
|  |  |  |

An entry point with no enforcement location is a finding, not an assumption.

## Controls built or modified

- (rate limiting, TLS verification, key handling, input validation, session handling, ...)

## Required negative tests — must be observed passing before "done"

- [ ] Unauthenticated request denied
- [ ] Wrong role denied
- [ ] Invalid or expired token denied
- [ ] Brute-force / code-guessing limited
- [ ] Untrusted TLS peer rejected
- [ ] Disallowed upload rejected
- [ ] <task-specific negative test>

## Build-time check evidence

| Check | Tool + version | Commit SHA | Raw output location | Result |
|---|---|---|---|---|
| Secret scan |  |  |  | PASS / FAIL / UNVERIFIED |
| Dependency (SCA) scan |  |  |  | PASS / FAIL / UNVERIFIED |
| SAST |  |  |  | PASS / FAIL / UNVERIFIED |
| Security negative tests |  |  |  | PASS / FAIL / UNVERIFIED |

A check that could not run in this runtime is `UNVERIFIED`, never passed by default, and blocks any GREEN claim until executed.

## Findings opened

| Finding | Severity | Observed evidence (file:line) | Exploitability assessment (basis, not assumption) | Owner | Due |
|---|---|---|---|---|---|

## Remediation loop (per finding)

- Reported to implementer (date, by whom):
- Fix + negative test added or refreshed:
- Re-run evidence (command, observed output, date):
- Re-verified by original reviewer: `VERIFIED` / `FINDINGS` / `UNVERIFIED`
- Cycle count (escalate to CTO after 3 failed cycles, or at once on critical disagreement):

## Independent review

- Reviewer:
- Verdict: `VERIFIED` / `FINDINGS` / `BLOCKED` / `UNVERIFIED`
- Scope reviewed:
- Scope NOT reviewed:
