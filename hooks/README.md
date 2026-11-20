# Build-time security hooks for Antigravity (optional, executable)

These hooks are the executable part of the build-time security loop
(`workflows/security-during-development.md`). They use Antigravity's documented
hooks mechanism (`hooks.json`, PreToolUse / Stop events — see
https://antigravity.google/docs/hooks/) to enforce two things while code is
being written, not after:

1. **`security_prewrite_gate.py` (PreToolUse on write tools).** Scans the
   content the agent is about to write for unambiguous hardcoded secrets
   (private key blocks, AWS/GitHub/Slack/Google key formats, `sk-` keys) and
   **denies the write**; suspicious credential assignments trigger an **ask**.
   Placeholder suppression looks at the secret value itself (e.g. the AWS
   documentation key `AKIAIOSFODNN7EXAMPLE`), never at nearby comments — a
   comment saying "test" cannot hide a real key. There is no scan-size cap; a
   cap would be a bypass.
2. **`security_stop_gate.py` (Stop).** When the agent tries to end a fully idle
   turn in a git workspace with uncommitted changes to security-sensitive files
   (auth, session, token, crypto, MFA, admin, upload, payment, TLS, directory
   sync, permissions — matched on the full changed path, with every untracked
   file enumerated) and no Security Task Card among the changes, it refuses the
   stop and sends the agent back to fill the card, run its negative tests, and
   record evidence or `UNVERIFIED`.

## Install into a project workspace

Copy into the target project's `.agents/` directory:

```text
<project>/.agents/hooks.json
<project>/.agents/hooks/security_prewrite_gate.py
<project>/.agents/hooks/security_stop_gate.py
```

Or install globally at `~/.gemini/config/hooks.json` — then edit the commands in
`hooks.json` to absolute script paths, because the hook's working directory is
not guaranteed to be the workspace. Works in Antigravity App, CLI, and IDE;
manage/toggle under Settings > Customizations > Hooks (or `/hooks` in the CLI).

**Canary check after install (do this once):**

1. `/hooks` in the CLI (or Settings > Customizations > Hooks) lists both gates
   as active.
2. `echo '{"toolCall":{"name":"write_to_file","args":{"TargetFile":"t","CodeContent":"x"}}}' | python3 .agents/hooks/security_prewrite_gate.py`
   prints `{"decision": "allow", ...}`.
3. `python3 hooks/test_hooks.py` (from this repo) passes — it exercises both
   gates against simulated payloads including the failure modes below.

**Dependency:** Python 3 on PATH (`python3`; on Windows change the command to
`python`). If Python is missing the hooks fail and Antigravity surfaces the
error — treat a failing gate as `UNVERIFIED`, never as passed.

## Honest limits

- **Not yet exercised by a live Antigravity host.** Schema and payloads follow
  the documented contract and local simulated-payload tests, but the first real
  run inside Antigravity is still pending and should be verified with the
  canary above.
- **Card presence, not freshness or truth.** The stop gate checks that a
  Security Task Card file is among the changed files. A stale or dishonestly
  filled card passes it — evidence quality stays with the reviewer.
- **Committed work is out of reach.** The stop gate reads `git status`; changes
  the agent already committed leave a clean tree and are not inspected.
- **Pattern-based secret detection only.** It catches common key formats and can
  miss obfuscated or unusual secrets; it is not SAST and does not replace
  dependency scanning, review, or the negative tests the task card requires.
- **`run_command` bypass.** The pre-write gate sees only Antigravity's write
  tools; content written via shell commands (heredocs, `sed`) is out of its
  reach. The package ships no CI pipeline to cover that path — the DevSecOps
  role instructions direct wiring one per project, but that is instruction-level
  today, so this bypass is an open gap.
- **Fail-open by design.** Both scripts exit 0 and allow on their own internal
  errors so a broken gate cannot wedge a session (a wedged IDE would push users
  to disable security entirely). The tradeoff: a broken gate protects nothing,
  which is why a failing or absent hook must be recorded as `UNVERIFIED`.
- **Bounded refusals.** The stop gate only fires on fully idle, clean model
  stops — user cancellation, error termination, and not-fully-idle stops pass
  through — and refuses at most 3 times per conversation (mirroring the
  workflow's 3-cycle escalation bound), after which the session may stop and
  the unresolved state escalates to a human. The counter persists in the
  artifact directory with a temp-dir fallback; if no location is writable the
  gate fails open rather than refusing forever.
