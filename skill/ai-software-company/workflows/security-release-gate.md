# Security and Release Gate

Run this gate on the exact commit intended for release. Record the repo, branch, commit SHA, and diff range in the review report before starting.

1. **Scope and commit binding.** Identify the release candidate commit. All findings, sign-offs, and status claims in this gate bind to that SHA.
2. **Attack-surface inventory.** Enumerate every network-reachable entry point: HTTP routes and handlers, websockets, background jobs, webhooks, file upload paths, admin and internal endpoints, proxies and forward-auth paths. For each one, state the required authentication and authorization and the file:line where it is enforced. An entry point with no explicit enforcement location is a finding, not an assumption.
3. **Auth, session, crypto, and secrets checklist.** Verify: no hardcoded or fallback keys (missing configuration fails closed); TLS peer verification enabled on every outbound identity and directory connection; token issuance, expiry, and revocation correct; MFA cannot be bypassed through privileged, unauthenticated, or recovery paths; rate limiting or lockout on every authentication and code-verification endpoint; secrets absent from source and logs.
4. **Automated scans.** Run dependency, secret, static (SAST), and applicable dynamic, container, and IaC scans. Attach raw results to the report.
5. **Negative tests.** Execute and observe tests proving controls reject abuse: unauthenticated request denied, wrong role denied, invalid or expired token denied, brute-force attempts limited, TLS verification enforced against an untrusted peer, upload of disallowed content rejected.
6. **Triage findings.** Record severity, exploitability, affected assets, exposure (internet-facing vs internal), and remediation for every finding.
7. **Verify fixes.** Re-run the failing checks and the relevant negative tests; attach new evidence.
8. **Independent sign-offs.** QA, Code Reviewer, and Cybersecurity Specialist each sign off in the review register with commit SHA, scope, and evidence. Sign-offs from a runtime that cannot execute the specialist are recorded as CTO assessments and do not satisfy this step.
9. **Staleness check.** Any commit after a sign-off that touches security-sensitive code (authn, authz, sessions, MFA, crypto, keys, network-facing endpoints, proxies, uploads, directory sync, payments, permission models) invalidates that sign-off. Re-run the affected steps before proceeding.
10. **Block release** for unresolved critical or high vulnerabilities, failed mandatory tests, or any security-sensitive component without a current sign-off. The blocking state is reported to the user as BLOCKED, never softened.
11. **Risk acceptance.** Record any approved, time-bounded risk acceptance explicitly: finding, owner, expiry, user approval reference.
12. **Production deployment** requires explicit user approval after steps 1-11 pass.
