# Software License, Product Code & Entitlement Specification

- Product Name:
- Owner Company Name:
- License Architect:
- Date:
- Status: Draft / Approved

## 1. Product Code & SKU Architecture
- Standard SKU Format: `[COMPANY]-[PRODUCT]-[EDITION]-[TIER]-[VERSION]`
- Product Code: `PRD-XXXX-XXX-2026`
- Supported Editions:
  * Community / Starter: `[CODE]-COMM`
  * Professional: `[CODE]-PRO`
  * Enterprise: `[CODE]-ENT`

## 2. Feature Bitmasks & Module Gating
| Bit / Key | Feature Flag | Description | Included Editions |
| :--- | :--- | :--- | :--- |
| `0x0001` | `FEATURE_CORE_API` | Core REST/GraphQL API access | All |
| `0x0002` | `FEATURE_DATA_EXPORT` | Bulk CSV/JSON export | Pro, Enterprise |
| `0x0004` | `FEATURE_SSO_SAML` | Enterprise SSO / Active Directory | Enterprise |
| `0x0008` | `FEATURE_AUDIT_LOGS` | Immutable compliance audit trails | Enterprise |
| `0x0010` | `FEATURE_MULTI_TENANT` | Multi-organization isolation | Enterprise |

## 3. Supported License Types
- [ ] **Perpetual:** Major version locked with optional 12-month maintenance date
- [ ] **Subscription:** Time-bound (Monthly / Annual) with grace period: `14 days`
- [ ] **Node-Locked (HWID):** Bound to salted SHA-256 machine hash (CPU, UUID, MAC)
- [ ] **Floating Network License:** Concurrent seat limit enforced via internal server
- [ ] **Evaluation / Trial:** Time-bombed for `30 days`, watermarking enabled

## 4. License Request & Server Activation Architecture
- **Hardware ID (HWID) Formulation:**
  `Salted SHA-256( CPU_Serial + BIOS_UUID + Primary_MAC_Address + Salt )`
- **Client Request Format:** JSON payload or `.req` file containing:
  `product_code`, `client_hwid`, `licensee_name`, `timestamp`, `nonce`
- **Server Cryptographic Signing Algorithm:** Ed25519 (Recommended) or RSA-4096
- **Signed License Structure (`.lic` / JSON Web Signature):**
  - Header: Algorithm, Key ID (`kid`)
  - Payload: License ID, Product Code, Licensee, HWID Bound, Expiration Date, Feature Bitmask, Seat Quota
  - Signature: Server private key cryptographic signature
- **Client Verification Logic:**
  1. Signature check using embedded public key
  2. HWID match check (if Node-Locked)
  3. System time validation with monotonicity check (prevents clock rollback)
  4. Grace period handling if activation server is temporarily unreachable (offline tolerance: `7 days`)

## 5. Security & Key Management
- Private Signing Key Storage: Managed via AWS KMS, GCP Cloud KMS, or HashiCorp Vault.
- Client Public Key: Hardcoded and obfuscated within client binaries.
- Key Rotation Policy: Annual key rotation with backward compatibility for existing issued licenses.
