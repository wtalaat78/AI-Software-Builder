# Security and Release Gate
1. Run dependency, secret, static, and applicable dynamic/container/IaC scans.
2. Review threat model and security changes.
3. Triage findings with severity, exploitability, affected assets, and remediation.
4. Verify fixes and rerun relevant tests.
5. QA and Code Reviewer independently sign off.
6. Block release for unresolved critical vulnerabilities or mandatory test failures.
7. Record any approved, time-bounded risk acceptance.
8. Request explicit user approval before production deployment.
