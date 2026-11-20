# Build-Time Security Loop

Security work happens while code is being built, not only in a final review. This workflow binds security requirements, tests, and evidence to each change. The `devsecops-security-engineer` owns the build-time checks; independent verification by the `cybersecurity-specialist` and `code-reviewer` still applies at milestone and release.

## 1. Before implementation: security requirements per task

- For every task that touches security-sensitive code (authentication, authorization, sessions/tokens, MFA, cryptography, keys and secrets, network-facing endpoints or proxies, file upload, directory or identity sync, payments, permission or role models), the implementing developer records a Security Task Card ([templates/SECURITY_TASK_CARD.md](templates/SECURITY_TASK_CARD.md)) **before** writing code:
  - the entry points the task adds or changes (routes, handlers, websockets, background jobs, webhooks, upload paths, admin and internal endpoints);
  - the authentication and authorization each entry point requires, and where it will be enforced;
  - the controls being built (rate limiting, TLS verification, key handling, input validation, session handling);
  - the negative tests that must be observed passing before the task can be called done: unauthenticated denied, wrong role denied, invalid/expired token denied, brute-force or code-guessing limited, untrusted TLS peer rejected, disallowed upload rejected — as applicable.
- Tasks with no security-sensitive surface record `N/A — no security-sensitive surface` instead of skipping silently.

## 2. During implementation: per-change checks

- The implementing developer runs the task card's negative tests as part of the task's own test suite — in the same change, not later.
- The `devsecops-security-engineer` wires build-time checks so they run on every change, not once at release: secret scanning, dependency (SCA) scanning, SAST where the stack supports it, and the test suite including the security negative tests. These checks fail the task/build; warning-only is not acceptable.
- Every entry point the change adds is appended to the attack-surface inventory with its enforcement location (file:line) as it is added. An entry point with no recorded enforcement is a finding at build time, not a release-time surprise.

## 3. Evidence and status per change

- Each check records: tool and version, command, commit SHA, and raw output location. A check that cannot run in the current runtime is recorded as `UNVERIFIED` with the exact missing capability — it is never treated as passed, and it blocks any later GREEN claim until executed.
- Task status follows evidence: negative tests observed passing means the security portion is `VERIFIED`; failing tests or missing controls mean `FINDINGS` / `BLOCKED`; checks not runnable mean `UNVERIFIED`.
- The builder of a control is not its sole judge. The `cybersecurity-specialist` reviews the task card and its evidence before the change counts as reviewed; when the runtime cannot invoke the specialist, the CTO records a CTO assessment, which does not satisfy independent review. The independent gates in [workflows/development.md](workflows/development.md) and [workflows/security-release-gate.md](workflows/security-release-gate.md) still apply at milestone and release.

## 4. DevSecOps ownership summary

- Owns: wiring the checks into the build, keeping them blocking, storing raw evidence per change, keeping the attack-surface inventory current as entry points are added, and tracking every security finding to closure with severity, owner, and due date.
- Does not own: approving the security of the code the checks cover. Independent review stays with the `cybersecurity-specialist` and `code-reviewer`.

## Limits of this workflow

These instructions coordinate agents; they do not mechanically force any runtime to run tools. Where the runtime cannot execute a scanner or a test, the correct recorded state is `UNVERIFIED`, and user-facing status must say so — never GREEN by default.
