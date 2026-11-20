#!/usr/bin/env python3
"""Antigravity Stop hook: when the agent tries to end its turn, check whether
the workspace has uncommitted changes to security-sensitive files without a
Security Task Card updated alongside them. If so, refuse the stop and send the
agent back to record the card and check evidence (or mark them UNVERIFIED).
Heuristic and fail-open: never blocks a session over its own errors, only
fires on clean model stops (never on user cancellation or error termination),
and gives up after MAX_CONTINUES refusals per conversation so it cannot trap
a session in an endless loop."""
import json, os, re, subprocess, sys

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
        r = subprocess.run(["git", "-C", ws, "status", "--porcelain"],
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

def continues_used(payload):
    """Per-conversation refusal counter stored in the artifact directory."""
    base = payload.get("artifactDirectoryPath") or ""
    conv = payload.get("conversationId") or "unknown"
    if not base or not os.path.isdir(base):
        return 0, None
    path = os.path.join(base, ".security_stop_gate_count")
    try:
        with open(path) as f:
            data = json.load(f)
        return int(data.get(conv, 0)), path
    except Exception:
        return 0, path

def bump(path, conv):
    if not path:
        return
    try:
        data = {}
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
        data[conv] = int(data.get(conv, 0)) + 1
        with open(path, "w") as f:
            json.dump(data, f)
    except Exception:
        pass  # counting failure must never block a stop

def main():
    try:
        payload = json.load(sys.stdin)
    except Exception as e:
        out("", f"security_stop_gate: unreadable payload, failing open ({e})")
    if payload.get("terminationReason") not in ("model_stop", ""):
        out("")  # only police clean stops; user cancellation and error stops pass through
    workspaces = payload.get("workspacePaths") or []
    for ws in workspaces:
        if not os.path.isdir(ws):
            continue
        files = changed_files(ws)
        if not files:
            continue
        has_card = any(CARD.search(f) for f in files)
        sensitive = [f for f in files if SENSITIVE.search(os.path.basename(f)) and not CARD.search(f)]
        if sensitive and not has_card:
            used, path = continues_used(payload)
            if used >= MAX_CONTINUES:
                out("")  # bounded: escalate to a human instead of looping forever
            bump(path, payload.get("conversationId") or "unknown")
            out("continue",
                "Build-time security loop: uncommitted changes touch security-sensitive files "
                f"({', '.join(sensitive[:5])}) without an updated Security Task Card. "
                "Before ending: fill templates/SECURITY_TASK_CARD.md for this change (entry points, "
                "authn/authz enforcement, controls), run its negative tests and record evidence, and "
                "mark any check you could not execute as UNVERIFIED. "
                f"(refusal {used + 1} of {MAX_CONTINUES}; after that the session stops and this escalates to the user)")
    out("")

main()
