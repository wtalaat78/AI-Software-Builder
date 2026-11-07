# Software Licensing, Product Codes, and Entitlement Lifecycle

1. **Product Code & SKU Formulation:**
   - The Licensing Specialist defines the standardized product code taxonomy: `[COMPANY]-[PRODUCT]-[EDITION]-[PLATFORM]-[YEAR/REV]` (e.g. `TW-APPGUARD-ENT-WIN-2026`).
   - Assign integer bitmasks or string keys for every feature, module, and capacity limit (e.g. `FEATURE_API_EXPORT = 0x01`, `FEATURE_ADV_ANALYTICS = 0x02`, `MAX_SEATS = 50`).
2. **License Type Selection:**
   - Determine applicable license modalities:
     * **Perpetual:** Never expires, with optional maintenance/updates expiration date.
     * **Subscription:** Strictly time-bound with configurable grace periods (e.g. 7-14 days).
     * **Node-Locked (HWID):** Bound to client machine hardware.
     * **Floating / Network:** Managed by an on-premises local license server tracking concurrent seats.
     * **Trial / Evaluation:** Time-limited with restricted feature bits and watermark flags.
3. **Client-Side License Request Mechanism:**
   - Client generates a deterministic Hardware ID (HWID) by hashing machine identifiers (CPU serial, BIOS UUID, primary MAC) using salted SHA-256.
   - Client packages a License Request file or JSON payload:
     ```json
     {
       "product_code": "TW-APPGUARD-ENT-WIN-2026",
       "client_hwid": "a8f5c3...4e9b",
       "licensee_name": "ACME Corporation",
       "contact_email": "admin@acme.com",
       "request_timestamp": "2026-11-07T12:00:00Z",
       "client_version": "1.0.0",
       "nonce": "d41d8cd98f00b204e9800998ecf8427e"
     }
     ```
   - Request can be transmitted via online HTTPS API or saved to a `.req` file for air-gapped / offline enterprise activation.
4. **License Generator Server Contract:**
   - Central License Generator Server receives the activation request.
   - Server validates customer purchase/subscription status in the entitlement database.
   - Server generates a cryptographically signed license payload using an asymmetric private key (Ed25519 or RSA-4096):
     ```json
     {
       "license_id": "LIC-2026-984321",
       "product_code": "TW-APPGUARD-ENT-WIN-2026",
       "license_type": "NodeLocked_Subscription",
       "licensee": "ACME Corporation",
       "hwid_bound": "a8f5c3...4e9b",
       "issued_at": "2026-11-07T12:05:00Z",
       "expires_at": "2027-11-07T23:59:59Z",
       "features": ["CORE", "API_EXPORT", "ADV_ANALYTICS"],
       "max_seats": 25,
       "signature": "MEUCIQDx8...bL4bAIgX..."
     }
     ```
   - Server returns the signed `.lic` file or JSON token to the client.
5. **Client-Side Verification & Anti-Tampering:**
   - Client verifies the cryptographic signature against the embedded public key.
   - Client verifies that the current machine's HWID matches `hwid_bound` (if node-locked).
   - Client verifies that `current_system_time` is between `issued_at` and `expires_at` (with monotonic clock check to block clock rollback).
   - Validated feature flags are injected into the application runtime.
6. **Inbound Open Source Audit & Commercial EULA:**
   - Audit all npm/pip/nuget/cargo dependencies to verify no copyleft licenses (GPL/AGPL) conflict with proprietary distribution.
   - Produce `THIRD_PARTY_NOTICES.md` listing all third-party components and licenses.
   - Finalize the customized End User License Agreement (`COMMERCIAL_EULA.md`) with owner company IP protections.
