# Feature Development Lifecycle

1. Confirm approved story, acceptance criteria, dependencies, and owner.
2. Architect and API specialist agree on interfaces and data contracts before parallel implementation.
3. Delegate bounded tasks to frontend/backend/mobile/desktop/database/AI agents as relevant.
4. Developers implement changes alongside automated tests and configuration documentation.
5. **MANDATORY UI UNSLOPPING PASS:** For all user-facing code, the `ui-unslop-specialist` audits and refactors screens using the 9-pass [heydamir/unslop](workflows/ui-unslopping.md) methodology (spacing, quiet chrome, single accent, Lucide line icons, concise copy, typography scale, calm layout, and 4px grid alignment).
6. Run static analysis, unit and integration tests (asserting $\ge 90\%$ coverage for critical logic), security scans, and build.
7. QA independently verifies acceptance criteria, accessibility (WCAG 2.1 AA), and regression risk.
8. Code Reviewer independently reviews diff and evidence.
9. Update backlog, project memory, traceability, and milestone status.
