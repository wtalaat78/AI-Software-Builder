#!/usr/bin/env python3
"""Regression tests for the build-time security hooks. Run: python3 test_hooks.py
Covers the decisions each gate must make and the failure modes found in
independent review (unbounded refusals when the counter cannot persist,
untracked-directory blind spot, comment-based suppression, scan truncation,
fullyIdle and cancellation pass-through, ASIA temporary keys, secrets in write
descriptions, cached-approval bypass via force_ask, the author.md false
positive, and internal-error fail-open)."""
import json, os, subprocess, sys, tempfile, unittest, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
PRE = os.path.join(HERE, "security_prewrite_gate.py")
STOP = os.path.join(HERE, "security_stop_gate.py")

def run(script, payload):
    r = subprocess.run([sys.executable, script], input=payload if isinstance(payload, str) else json.dumps(payload),
                       capture_output=True, text=True, timeout=15)
    assert r.returncode == 0, f"exit {r.returncode}: {r.stderr}"
    return json.loads(r.stdout)

def write_payload(name, args):
    return {"toolCall": {"name": name, "args": args}}

class TestPrewriteGate(unittest.TestCase):
    def test_denies_private_key(self):
        d = run(PRE, write_payload("write_to_file", {"TargetFile": "k.js",
                "CodeContent": "const k = `-----BEGIN PRIVATE KEY-----\nMIIE\n-----END PRIVATE KEY-----`;"}))
        self.assertEqual(d["decision"], "deny")

    def test_denies_aws_key_inside_multi_replace_chunk(self):
        d = run(PRE, write_payload("multi_replace_file_content", {"TargetFile": "a.js",
                "ReplacementChunks": [{"ReplacementContent": 'const k = "AKIAZZ9X8Y7W6V5U4T3S";'}]}))
        self.assertEqual(d["decision"], "deny")

    def test_denies_ghp_and_sk_and_aiza(self):
        for token in ["ghp_" + "a" * 36, "sk-" + "b" * 40, "AIza" + "c" * 35]:
            d = run(PRE, write_payload("write_to_file", {"TargetFile": "t.js", "CodeContent": f'const t = "{token}";'}))
            self.assertEqual(d["decision"], "deny", token[:12])

    def test_allows_aws_documentation_example_key(self):
        d = run(PRE, write_payload("write_to_file", {"TargetFile": "doc.js",
                "CodeContent": "// example: AKIAIOSFODNN7EXAMPLE from AWS docs"}))
        self.assertEqual(d["decision"], "allow")

    def test_comment_saying_test_does_not_suppress_real_key(self):
        # Review finding: a nearby comment must not hide a genuine-format key.
        d = run(PRE, write_payload("write_to_file", {"TargetFile": "t.js",
                "CodeContent": '// test data below\nconst key = "AKIAZZ9X8Y7W6V5U4T3S";'}))
        self.assertEqual(d["decision"], "deny")

    def test_force_asks_on_hardcoded_password_allows_placeholder_value(self):
        # force_ask (not ask): documented decision that ignores cached
        # "Always Allow" approvals, so a suspected credential always prompts.
        d = run(PRE, write_payload("replace_file_content", {"TargetFile": "c.js",
                "ReplacementContent": 'const dbPassword = "Sup3rSecretValue!";'}))
        self.assertEqual(d["decision"], "force_ask")
        d = run(PRE, write_payload("replace_file_content", {"TargetFile": "c.js",
                "ReplacementContent": 'const dbPassword = "<db-password-here>";'}))
        self.assertEqual(d["decision"], "allow")

    def test_denies_asia_temporary_aws_key(self):
        # Review finding: STS temporary keys (ASIA...) were missed.
        d = run(PRE, write_payload("write_to_file", {"TargetFile": "t.js",
                "CodeContent": 'const k = "ASIAZZ9X8Y7W6V5U4T3S";'}))
        self.assertEqual(d["decision"], "deny")

    def test_denies_secret_hidden_in_description(self):
        # Review finding: the write tools' Description text was not scanned.
        d = run(PRE, write_payload("write_to_file", {"TargetFile": "c.js",
                "CodeContent": "export const x = 1;",
                "Description": "adds client, key AKIAZZ9X8Y7W6V5U4T3S for now"}))
        self.assertEqual(d["decision"], "deny")
        d = run(PRE, write_payload("multi_replace_file_content", {"TargetFile": "c.js",
                "Description": 'password = "Sup3rSecretValue!"',
                "ReplacementChunks": [{"ReplacementContent": "export const x = 2;"}]}))
        self.assertEqual(d["decision"], "force_ask")

    def test_internal_error_still_fails_open_with_json(self):
        # Review finding: unhandled internal errors exited nonzero without a
        # JSON reason; every failure path must emit valid JSON and fail open.
        d = run(PRE, {"toolCall": {"name": "write_to_file", "args": "not-a-dict"}})
        self.assertEqual(d["decision"], "allow")
        self.assertIn("failing open", d["reason"])

    def test_secret_after_large_filler_is_not_truncated_away(self):
        # Review finding: a scan cap is a bypass.
        filler = "// " + "x" * 300000 + "\n"
        d = run(PRE, write_payload("write_to_file", {"TargetFile": "big.js",
                "CodeContent": filler + 'const k = "AKIAZZ9X8Y7W6V5U4T3S";'}))
        self.assertEqual(d["decision"], "deny")

    def test_clean_write_and_non_write_tool_allow(self):
        self.assertEqual(run(PRE, write_payload("write_to_file", {"TargetFile": "u.js",
                "CodeContent": "export const add=(a,b)=>a+b;"}))["decision"], "allow")
        self.assertEqual(run(PRE, {"toolCall": {"name": "run_command", "args": {"CommandLine": "npm test"}}})["decision"], "allow")

    def test_broken_payload_fails_open(self):
        d = run(PRE, "not json")
        self.assertEqual(d["decision"], "allow")
        self.assertIn("failing open", d["reason"])

class TestStopGate(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        subprocess.run(["git", "init", "-q"], cwd=self.dir, check=True)
        subprocess.run(["git", "-C", self.dir, "config", "user.email", "t@t.t"], check=True)
        subprocess.run(["git", "-C", self.dir, "config", "user.name", "t"], check=True)
        with open(os.path.join(self.dir, "app.js"), "w") as f:
            f.write("console.log(1)")
        subprocess.run(["git", "-C", self.dir, "add", "."], check=True)
        subprocess.run(["git", "-C", self.dir, "commit", "-qm", "init"], check=True)
        self.art = tempfile.mkdtemp()

    def payload(self, **kw):
        p = {"terminationReason": "model_stop", "fullyIdle": True,
             "workspacePaths": [self.dir], "conversationId": "test-conv",
             "artifactDirectoryPath": self.art}
        p.update(kw)
        return p

    def touch(self, rel, content="x"):
        path = os.path.join(self.dir, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)

    def test_refuses_thrice_then_allows(self):
        self.touch("auth.js")
        p = self.payload(conversationId=f"bound-{uuid.uuid4()}")
        for i in range(3):
            self.assertEqual(run(STOP, p)["decision"], "continue", f"attempt {i+1}")
        self.assertEqual(run(STOP, p)["decision"], "")  # bounded

    def test_counter_falls_back_to_tempdir_when_artifact_dir_missing(self):
        # Review finding: missing artifactDirectoryPath caused endless continues.
        self.touch("auth.js")
        p = self.payload(conversationId=f"fallback-{uuid.uuid4()}", artifactDirectoryPath="/nonexistent/dir")
        for i in range(3):
            self.assertEqual(run(STOP, p)["decision"], "continue", f"attempt {i+1}")
        self.assertEqual(run(STOP, p)["decision"], "")

    def test_user_cancel_and_error_and_not_idle_pass_through(self):
        self.touch("auth.js")
        self.assertEqual(run(STOP, self.payload(conversationId=f"uc-{uuid.uuid4()}", terminationReason="user_cancel"))["decision"], "")
        self.assertEqual(run(STOP, self.payload(conversationId=f"er-{uuid.uuid4()}", terminationReason="error"))["decision"], "")
        self.assertEqual(run(STOP, self.payload(conversationId=f"ni-{uuid.uuid4()}", fullyIdle=False))["decision"], "")

    def test_card_present_allows(self):
        self.touch("auth.js")
        self.touch("SECURITY_TASK_CARD.md", "# card")
        self.assertEqual(run(STOP, self.payload())["decision"], "")

    def test_non_sensitive_change_allows(self):
        self.touch("README.md", "docs")
        self.assertEqual(run(STOP, self.payload())["decision"], "")

    def test_nested_untracked_sensitive_file_detected(self):
        # Review finding: new directory collapses to "?? src/" without -uall.
        self.touch(os.path.join("src", "auth", "login.js"))
        d = run(STOP, self.payload(conversationId=f"nested-{uuid.uuid4()}"))
        self.assertEqual(d["decision"], "continue")

    def test_author_md_is_not_sensitive(self):
        # Review finding: substring matching flagged "author.md" as "auth".
        self.touch("author.md", "# about the author")
        self.assertEqual(run(STOP, self.payload())["decision"], "")

    def test_plurals_and_derivatives_still_match(self):
        self.touch("roles.py")
        self.assertEqual(run(STOP, self.payload(conversationId=f"pl-{uuid.uuid4()}"))["decision"], "continue")
        subprocess.run(["git", "-C", self.dir, "add", "."], check=True)
        subprocess.run(["git", "-C", self.dir, "commit", "-qm", "x"], check=True)
        self.touch("encryption.js")
        self.assertEqual(run(STOP, self.payload(conversationId=f"dv-{uuid.uuid4()}"))["decision"], "continue")

    def test_internal_error_still_fails_open_with_json(self):
        self.touch("auth.js")
        d = run(STOP, self.payload(conversationId={"bad": "type"}))
        self.assertEqual(d["decision"], "")
        self.assertIn("failing open", d["reason"])

    def test_non_git_workspace_allows(self):
        plain = tempfile.mkdtemp()
        self.assertEqual(run(STOP, self.payload(workspacePaths=[plain]))["decision"], "")

if __name__ == "__main__":
    unittest.main(verbosity=2)
