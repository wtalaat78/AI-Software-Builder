#!/usr/bin/env python3
"""Antigravity PreToolUse hook: scan content about to be written for hardcoded
secrets before it lands in a project file. Conservative on purpose: it denies
only unambiguous secret formats and asks on suspicious assignments, so normal
code is never blocked. Fails open (allow) on internal error so a broken gate
can never wedge the IDE, and says so in the reason."""
import json, re, sys

DENY_PATTERNS = [
    (re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY( BLOCK)?-----"), "private key material"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    (re.compile(r"\bghp_[A-Za-z0-9]{36}\b"), "GitHub personal access token"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}\b"), "GitHub fine-grained token"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), "Slack token"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{32,}\b"), "API key with sk- prefix"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"), "Google API key"),
]
# Suspicious but plausibly a placeholder or example: ask, do not deny.
ASK_PATTERNS = [
    (re.compile(r"(?i)(password|passwd|secret|api[_-]?key|token)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"),
     "possible hardcoded credential assignment"),
]
PLACEHOLDER_HINT = re.compile(r"(?i)(example|sample|placeholder|dummy|test|changeme|xxx|\.\.\.|<[a-z_-]+>|\{\{)")

WRITE_CONTENT_KEYS = {
    "write_to_file": ["CodeContent"],
    "replace_file_content": ["ReplacementContent"],
    "multi_replace_file_content": [],  # handled via ReplacementChunks
}
MAX_SCAN = 200_000

def out(decision, reason=""):
    print(json.dumps({"decision": decision, "reason": reason}))
    sys.exit(0)

def collect_text(name, args):
    parts = []
    for key in WRITE_CONTENT_KEYS.get(name, []):
        val = args.get(key)
        if isinstance(val, str):
            parts.append(val)
    if name == "multi_replace_file_content":
        chunks = args.get("ReplacementChunks")
        if isinstance(chunks, list):
            for c in chunks:
                if isinstance(c, dict) and isinstance(c.get("ReplacementContent"), str):
                    parts.append(c["ReplacementContent"])
    return "\n".join(parts)

def main():
    try:
        payload = json.load(sys.stdin)
    except Exception as e:
        out("allow", f"security_prewrite_gate: unreadable payload, failing open ({e})")
    call = payload.get("toolCall") or {}
    name = call.get("name") or ""
    args = call.get("args") or {}
    text = collect_text(name, args)
    if not text:
        out("allow")
    text = text[:MAX_SCAN]
    for rx, label in DENY_PATTERNS:
        m = rx.search(text)
        if m and not PLACEHOLDER_HINT.search(text[max(0, m.start()-60):m.end()+60]):
            out("deny", f"Blocked write: content contains {label}. Secrets must come from a secret store or environment, never source. Store it properly and reference it instead.")
    for rx, label in ASK_PATTERNS:
        m = rx.search(text)
        if m and not PLACEHOLDER_HINT.search(text[max(0, m.start()-60):m.end()+60]):
            out("ask", f"Content may contain a {label}. Confirm it is a placeholder/example, or move the secret to a secret store.")
    out("allow")

main()
