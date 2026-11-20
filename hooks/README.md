# Build-time security hooks for Antigravity (optional, executable)

These hooks are the executable part of the build-time security loop
(`workflows/security-during-development.md`). They use Antigravity's documented
hooks mechanism (`hooks.json`, PreToolUse / Stop events) to enforce two things
while code is being written, not after:

1. **`security_prewrite_gate.py` (PreToolUse on write tools).** Scans the
   content the agent is about to write for unambiguous hardcoded secrets
   (private key blocks, AWS/GitHub/Slack/Google key formats, `sk-` keys) and
   **denies the write**; suspicious credential assignments trigger an **ask**.
   Placeholders and examples are not blocked.
2. **`security_stop_gate.py` (Stop).** When the agent tries to end its turn in
   a git workspace with uncommitted changes to security-sensitive files (auth,
   session, token, crypto, MFA, admin, upload, payment, TLS, directory sync,
   permissions) and no Security Task Card was updated alongside them, it refuses
   the stop and sends the agent back to fill the card, run its negative tests,
   and record evidence or `UNVERIFIED`.

## Install into a project workspace

Copy into the target project's `.agents/` directory:

```text
<project>/.agents/hooks.json
<project>/.agents/hooks/security_prewrite_gate.py
<project>/.agents/hooks/security_stop_gate.py
```

Or install globally at `~/.gemini/config/hooks.json` (commands must then use
absolute script paths). Works in Antigravity App, CLI, and IDE; manage/toggle
under Settings > Customizations > Hooks (or `/hooks` in the CLI).

**Dependency:** Python 3 on PATH (`python3`; on Windows change the command to
`python`). If Python is missing the hooks fail and Antigravity surfaces the
error — treat a failing gate as `UNVERIFIED`, never as passed.

## Honest limits

- Pattern-based and conservative: it catches common secret formats and missing
  task-card evidence. It does not replace SAST, dependency scanning, review, or
  the negative tests the task card requires, and it can miss obfuscated secrets.
- The pre-write gate sees only content passed through Antigravity's write tools;
  content written via `run_command` (e.g. heredocs) is out of its reach — that
  path needs the pipeline checks in the DevSecOps role.
- The stop gate is a heuristic over git status and file names; it stays out of
  the way in non-git workspaces and on non-matching changes.
- Both scripts fail open on their own internal errors so a broken gate cannot
  wedge a session; a fail-open event is recorded in the hook's reason.
- The stop gate only fires on clean model stops — user cancellation and error
  terminations always pass through — and it refuses a stop at most 3 times per
  conversation (mirroring the workflow's 3-cycle escalation bound), after which
  the session is allowed to stop and the unresolved state escalates to a human.
  It can never trap a session in an endless loop.
- Fail-open is a deliberate choice: these hooks are a backstop, and a wedged
  IDE would push users to disable security entirely. The tradeoff is that a
  broken gate silently provides no protection — which is why a failing or
  absent hook must be recorded as `UNVERIFIED`, not assumed working.
