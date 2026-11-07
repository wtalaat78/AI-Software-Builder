# Authorized Reverse Engineering and Application Modernization

This workflow defines the dual-track methodology for deconstructing existing software applications into complete feature specifications and modernized source code.

---

## Track 1: Feature-Level & Behavioral Reverse Engineering (Search & OSINT)
*Led by: `reverse-engineering-feature-analyst`*

1. **Target Scoping & Authorization Check:**
   - Confirm authorized scope, target platform, accessible endpoints, and public intelligence sources.
2. **OSINT & Public Research Sweep:**
   - Search official documentation, user guides, changelogs, patent filings, and developer portals.
   - Analyze public forums, app store user feedback, and tech teardowns for undocumented features and edge-case behaviors.
3. **Black-Box Interaction & Workflow Mapping:**
   - Map end-to-end user journeys, screen flows, state machines, validation rules, and permission models.
   - Deconstruct application functionality into a hierarchical Feature Inventory matrix.
4. **Network & Protocol Reversing:**
   - Capture and analyze HTTP/REST, GraphQL, WebSocket, or gRPC telemetry.
   - Reconstruct API request/response schemas, parameter types, authentication handshakes, and error codes.
5. **Feature Specification Delivery:**
   - Package findings into a formal Software Requirements Specification (SRS) and user stories with testable acceptance criteria for the Business Analyst and Product Manager.

---

## Track 2: Code-Level & Binary Reverse Engineering (Decompilation & Logic Extraction)
*Led by: `reverse-engineering-code-specialist`*

1. **Artifact Ingestion & Format Identification:**
   - Inspect target binaries/packages: Android APK/AAB, .NET assemblies (DLL/EXE), JavaScript web bundles/Electron, WebAssembly (Wasm), or native PE/ELF binaries.
2. **Decompilation & Abstract Syntax Tree (AST) Recovery:**
   - Decompile bytecodes using appropriate decompilers (JADX for Android, ILSpy/dnSpy for .NET, AST unpackers for JS/TS bundles, Wasm disassemblers).
   - Deobfuscate variable names, restore control flow structures, and recover symbol tables.
3. **Data Model & Schema Extraction:**
   - Reconstruct database schemas, ORM models, serialization formats, and relational integrity constraints.
   - Extract internal data structures, enums, state machines, and configuration files.
4. **Algorithmic Recovery & Clean-Room Translation:**
   - Isolate core business algorithms, calculation logic, and protocol state machines.
   - Author clean-room specifications and rewrite algorithms into modern, idiomatic languages (TypeScript, Go, Python, C#, Kotlin) without copy-pasting copyrighted legacy code fragments.
5. **Verification & Modernization Handoff:**
   - Author comprehensive unit tests asserting the exact parity of the modernized code against legacy outputs.
   - Hand off clean code modules to the Backend Developer, Frontend Developer, and Solution Architect.

---

## Governance & Clean-Room IP Protection
*Led by: `cto-team-leader` & `software-license-compliance-specialist`*

1. Maintain strict clean-room boundaries: separate specification generation from implementation.
2. Verify that no proprietary secrets, private credentials, or copyrighted binary fragments are shipped into the new codebase.
3. Obtain explicit user approvals before making any changes that affect production environments or external integrations.
