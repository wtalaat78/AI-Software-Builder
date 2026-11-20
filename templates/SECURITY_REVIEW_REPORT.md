# Security Review Report

## Binding
- Repository / component:
- Branch:
- Commit SHA reviewed:
- Diff range (if incremental):
- Review date:
- Reviewer agent(s):
- Execution provenance: (specialist actually invoked? inputs given? or CTO assessment)

## Scope
- Areas examined (files / modules):
- Areas NOT reviewed (explicit):

## Attack-surface inventory
| Entry point (route / job / upload / hook) | Authn required | Authz required | Enforced at (file:line) | Status |
|---|---|---|---|---|
|  |  |  |  |  |

## Auth / session / crypto / secrets checklist
| Check | Result (VERIFIED / FINDING / N/A) | Evidence (file:line or test) |
|---|---|---|
| No hardcoded or fallback keys; missing config fails closed |  |  |
| TLS peer verification enabled on all outbound identity/directory connections |  |  |
| Token issuance, expiry, revocation correct |  |  |
| MFA not bypassable via privileged, unauthenticated, or recovery paths |  |  |
| Rate limiting / lockout on auth and code-verification endpoints |  |  |
| No secrets in source, logs, or project memory |  |  |

## Scan results
| Scan (dependency / secret / SAST / DAST / container / IaC) | Tool | Date | Result | Raw output location |
|---|---|---|---|---|
|  |  |  |  |  |

## Negative tests executed
| Test | Command | Observed result | Pass/Fail |
|---|---|---|---|
| Unauthenticated request denied |  |  |  |
| Wrong role denied |  |  |  |
| Invalid / expired token denied |  |  |  |
| Brute-force limited |  |  |  |
| TLS verification enforced |  |  |  |
| Disallowed upload rejected |  |  |  |

## Findings
| # | Severity (critical/high/medium/low) | Location (file:line) | Observed missing control (fact) | Assessed exploitability (inference + basis) | Unresolved context | Remediation | Status |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

## Verdict
- [ ] VERIFIED — no open critical/high findings; evidence attached
- [ ] FINDINGS — open findings listed above; release blocked until critical/high resolved
- [ ] BLOCKED — security-sensitive areas not reviewed

## Validity
This verdict is valid only for the commit SHA above. Any later commit touching authentication, authorization, sessions, MFA, cryptography, keys or secrets, network-facing endpoints, proxies, uploads, directory or identity sync, payments, or permission models invalidates this verdict until the affected scope is re-reviewed.

## Sign-offs
| Agent | Verdict | Commit SHA | Evidence location | Date |
|---|---|---|---|---|
| qa-testing-engineer |  |  |  |  |
| code-reviewer |  |  |  |  |
| cybersecurity-specialist |  |  |  |  |
