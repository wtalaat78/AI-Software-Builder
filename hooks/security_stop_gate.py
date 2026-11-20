#!/usr/bin/env python3
"""Antigravity Stop hook: when the agent tries to end its turn, check whether
the workspace has uncommitted changes to security-sensitive files without a
Security Task Card present among the changes. If so, refuse the stop and send
the agent back to record the card and check evidence (or mark them UNVERIFIED).

Bounds and fail-open behavior:
- Only fires on fully idle, clean model stops; user cancellation, error
  termination, and not-fully-idle stops always pass through.
- Refusals are capped at MAX_CONTINUES per conversation (mirrors the 3-cycle
  escalation bound in workflows/security-during-development.md); after that the
  stop is allowed and the unresolved state is for a human to handle.
- The counter persists in artifactDirectoryPath, falling back to the system
  temp dir. If neither is writable the gate fails open (allows the stop) rather
  than refusing forever — a counter that cannot persist must not mean an
  unbounded loop.
- It checks card PRESENCE among changed files only: not freshness, not truthful
  content. Evidence quality stays with the reviewer.
- Blind spot by design: changes the agent already committed leave a clean git
  status and are not inspected; this gate sees uncommitted work only."""
import json, os, re, subprocess, sys, tempfile

SENSITIVE = re.compile(
    r"(?i)(auth|login|logout|session|token|jwt|oauth|mfa|totp|otp|crypto|encrypt|decrypt|secret|credential|"
    r"password|permission|rbac|role|admin|upload|payment|billing|checkout|proxy|gateway|tls|cert|ldap|directory)"
)
CARD = re.compile(r"(?i)SECURITY[-_ ]?TASK[-_ ]?CARD")
MAX_CONTINUES = 3  # mirrors the 3-cycle escalation bound in the workflow

def out(decision="", reason=""):
    print(json.dumps({"decision": decision, "reason": reason}))
    sys.exit(0)

def changed_files(ws):
    try:
        # -uall: enumerate every untracked file, including inside new
        # directories — plain git status collapses those to "?? dir/" and the
        # sensitive file inside would be missed.
        r = subprocess.run(["git", "-C", ws, "status", "--porcelain", "--untracked-files=all"],
                           capture_output=True, text=True, timeout=10)
    except Exception:
        return None  # not a git workspace or git unavailable: stay out of the way
    if r.returncode != 0:
        return None
    files = []
    for line in r.stdout.splitlines():
        path = line[3:] if len(line) > 3 else ""
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        path = path.strip().strip('"')
        if path:
            files.append(path)
    return files

def counter_path(payload):
    """Per-conversation refusal counter; artifact dir first, temp dir fallback."""
    conv = re.sub(r"[^A-Za-z0-9_-]", "_", payload.get("conversationId") or "unknown")
    name = f".security_stop_gate_{conv}"
    base = payload.get("artifactDirectoryPath") or ""
    candidates = [os.path.join(base, name)] if base and os.path.isdir(base) else []
    candidates.append(os.path.join(tempfile.gettempdir(), name))
    for path in candidates:
        try:
            with open(path, "a"):
                pass
            return path
        except Exception:
            continue
    return None

def continues_used(path):
    try:
        with open(path) as f:
            return int((f.read() or "0").strip())
    except Exception:
        return 0

def bump(path, n):
    try:
        with open(path, "w") as f:
            f.write(str(n))
    except Exception:
        pass

def main():
    try:
        payload = json.load(sys.stdin)
    except Exception as e:
        out("", f"security_stop_gate: unreadable payload, failing open ({e})")
    if payload.get("terminationReason") not in ("model_stop", ""):
        out("")  # only police clean stops; user cancellation and error stops pass through
    if payload.get("fullyIdle") is False:
        out("")  # background work still running: not a real end of turn
    workspaces = payload.get("workspacePaths") or []
    for ws in workspaces:
        if not os.path.isdir(ws):
            continue
        files = changed_files(ws)
        if not files:
            continue
        has_card = any(CARD.search(f) for f in files)
        sensitive = [f for f in files if SENSITIVE.search(f) and not CARD.search(f)]
        if sensitive and not has_card:
            path = counter_path(payload)
            if path is None:
                out("", "security_stop_gate: no writable counter location, failing open rather than refusing forever")
            used = continues_used(path)
            if used >= MAX_CONTINUES:
                out("")  # bounded: escalate to a human instead of looping forever
            bump(path, used + 1)
            out("continue",
                "Build-time security loop: uncommitted changes touch security-sensitive files "
                f"({', '.join(sensitive[:5])}) without a Security Task Card among the changes. "
                "Before ending: fill templates/SECURITY_TASK_CARD.md for this change (entry points, "
                "authn/authz enforcement, controls), run its negative tests and record evidence, and "
                "mark any check you could not execute as UNVERIFIED. "
                f"(refusal {used + 1} of {MAX_CONTINUES}; after that the session stops and this escalates to the user)")
    out("")

main()
