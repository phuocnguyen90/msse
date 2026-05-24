# DID Methods and Verifiable Credential Format Alignment

## Overview

The proposed ZK-KYC architecture does not exist in isolation. To achieve interoperability with global digital identity infrastructure and avoid proprietary lock-in, it must align with established open standards: **W3C Decentralized Identifiers (DIDs)** and **W3C Verifiable Credentials (VCs)**. This document specifies which DID method and VC format are appropriate for the L0/L1 context, and how they integrate with zero-knowledge proof generation.

---

## 1. Why DID and VC Alignment Matters

Without standards alignment, the ZK-KYC system risks:
- **Vendor lock-in**: A custom credential format incompatible with international wallets (Apple Wallet, Google Wallet, EU EUDI Wallet) prevents cross-border use.
- **Verification fragmentation**: Different L1 chains use incompatible credential schemas, requiring custom integrations for every service.
- **Regulatory non-compliance**: The EU eIDAS 2.0 regulation and ISO/IEC 18013-5 (mobile Driving License) both mandate W3C VC or ISO mDL-compatible formats. Vietnamese issuers interoperating with EU counterparts must comply.

Adopting W3C standards from the start costs little and provides a future-proofed interoperability foundation.

---

## 2. Decentralized Identifiers (DIDs)

### 2.1 What is a DID?

A DID is a globally unique identifier that resolves to a **DID Document** — a JSON-LD object containing the entity's public keys, authentication methods, and service endpoints. DIDs are controlled by their subject, not by a central registry.

```json
{
  "@context": "https://www.w3.org/ns/did/v1",
  "id": "did:zkkyc-vn:ndachain:0x4a3b...c7f2",
  "verificationMethod": [{
    "id": "did:zkkyc-vn:ndachain:0x4a3b...c7f2#key-1",
    "type": "JsonWebKey2020",
    "controller": "did:zkkyc-vn:ndachain:0x4a3b...c7f2",
    "publicKeyJwk": { "crv": "BN254", "x": "...", "y": "..." }
  }],
  "authentication": ["did:zkkyc-vn:ndachain:0x4a3b...c7f2#key-1"]
}
```

### 2.2 DID Method Selection

A DID method defines how DIDs are created, resolved, updated, and deactivated on a specific registry. The choice of DID method determines the trust model for the issuer's identifier.

| DID Method | Registry | Suitable For | Notes |
|---|---|---|---|
| `did:web` | DNS + HTTPS | KYC issuers (banks, gov) | Simple; trust depends on DNS security |
| `did:ethr` | Ethereum | L1 operator identity | Requires Ethereum node access |
| `did:ion` | Bitcoin (Sidetree) | High-assurance issuer DIDs | Highly decentralized; slow resolution |
| `did:key` | No registry | User ephemeral DIDs | Cryptographic only; no on-chain anchor |
| `did:zkkyc-vn` | **L0 (proposed)** | All VN ZK-KYC entities | **Custom method — recommended** |

**Recommended approach: Define a custom `did:zkkyc-vn` method anchored on L0.**

This method:
- Registers all KYC issuers, L1 operators, and (optionally) user pseudonymous identifiers on L0.
- Resolves DID Documents via an L0 state query, inheriting L0's immutability and auditability.
- Is fully open-source and can be submitted to the W3C DID Methods Registry.

### 2.3 `did:zkkyc-vn` Method Specification Sketch

```
DID Syntax:   did:zkkyc-vn:<l1-chain-id>:<base58-public-key-hash>

Example:      did:zkkyc-vn:ndachain:8Uw3pQmNxTZ...

Resolution:   L0 anchor registry lookup by (l1_chain_id, pubkey_hash)
              Returns: DID Document with public key and service endpoints

CRUD:
  Create:  RegisterIssuer or RegisterL1 governance transaction on L0
  Read:    Public L0 state query (no authentication required)
  Update:  Signed transaction by DID controller (key rotation)
  Deactivate: Signed transaction; marks DID as revoked on L0
```

User identities optionally use `did:key` for ephemeral, non-persistent pseudonymous identifiers — a user's DID changes with each credential issuance, preventing correlation at the DID level.

---

## 3. Verifiable Credential Format

### 3.1 Standard W3C VC Structure

A Zero-Knowledge Credential (ZKC) issued by the ZK-KYC system is a **W3C Verifiable Credential** with a ZK-native signature scheme:

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://zkkyc.gov.vn/credentials/v1"
  ],
  "type": ["VerifiableCredential", "ZKKYCCredential"],
  "issuer": "did:zkkyc-vn:ndachain:8Uw3pQ...",
  "issuanceDate": "2025-06-01T00:00:00Z",
  "expirationDate": "2027-06-01T00:00:00Z",
  "credentialSubject": {
    "id": "did:key:z6Mk...",
    "credentialVersion": "2025-06-01",
    "identityCommitment": "0x7a3f...b291",
    "attributes": {
      "nationality": "VN",
      "ageGroup": "18+",
      "kycLevel": 2,
      "issuingAuthority": "MINISTRY_OF_PUBLIC_SECURITY"
    }
  },
  "credentialStatus": {
    "id": "did:zkkyc-vn:ndachain:revocation#0x7a3f",
    "type": "SparseMerkleTreeEntry2025"
  },
  "proof": {
    "type": "BJJSignature2021",
    "created": "2025-06-01T00:00:00Z",
    "verificationMethod": "did:zkkyc-vn:ndachain:8Uw3pQ...#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z3cBs..."
  }
}
```

### 3.2 ZK-Native Signature Scheme: BJJ Signatures

Standard VC proof types (Ed25519, RSA) are not ZK-circuit-friendly — they require thousands of constraints to verify inside a circuit. The **Baby Jubjub (BJJ) signature scheme** (used by iden3/Polygon ID) is an elliptic curve designed specifically to operate efficiently inside ZK circuits over the BN254 scalar field.

**BJJ Signature properties:**
- ~2,500 constraints in a Circom circuit (vs. ~25,000 for Ed25519)
- Supports selective disclosure natively
- Used in production by Polygon ID across millions of credentials

**Recommendation**: Adopt BJJ signatures for ZKC issuance, with a migration path to BLS12-381 (more quantum-resistant relative to BN254) when ecosystem support matures.

### 3.3 BBS+ Signatures for Selective Disclosure

An alternative to the circuit-based approach is **BBS+ signatures** (W3C draft standard, 2023), which support **unlinkable selective disclosure** at the signature level — without requiring a ZK circuit for attribute selection.

```
BBS+ allows:
  Credential has 10 attributes → User reveals only 2 → Signature still verifies
  Different selective disclosures are unlinkable to each other
```

BBS+ signatures are being standardized by W3C as the `BbsBlsSignature2020` proof type and are supported by the EU EUDI Wallet specification.

**Trade-off vs. BJJ + ZKP circuits:**
- BBS+ is simpler to implement and has smaller computational overhead.
- ZKP circuits support more expressive predicates (e.g., `age > 18`, `income_range == "50M-100M VND"`) — not just attribute selection.

**Recommendation**: Support **both** formats:
- BBS+ for basic selective disclosure (simpler verifiers, mobile-first)
- BJJ + UltraPLONK circuits for complex predicate proofs (financial compliance, age gating)

---

## 4. Alignment with Existing Implementations

### 4.1 Semaphore

Semaphore (appliedzkp.org) is an open-source ZK group membership protocol directly relevant to ZK-KYC. The identity model maps as follows:

| Semaphore Concept | ZK-KYC Equivalent |
|---|---|
| Identity commitment | `Poseidon(identity_secret, identity_nullifier)` |
| Group (Merkle tree) | L1 identity registry Merkle tree |
| External nullifier | `context_id` |
| Signal | `attribute_claim` |

ZK-KYC can be implemented as a **specialized Semaphore group** where group membership requires a valid KYC issuance on L1. This avoids re-inventing the ZK group membership primitive and leverages Semaphore's audited contracts.

### 4.2 Polygon ID

Polygon ID is the most production-ready ZK identity framework aligned with W3C VCs. Its architecture maps almost directly:

| Polygon ID Component | ZK-KYC Equivalent |
|---|---|
| Issuer node | KYC authority (bank, MoPS) on L1 |
| Identity state (Iden3 SMT) | L1 identity + revocation Merkle trees |
| Claim (W3C VC) | ZKC (Zero-Knowledge Credential) |
| PolygonID blockchain | L0 anchor registry |
| Verifier contract | L1 service provider verifier |

**Recommendation**: The ZK-KYC L1 can be implemented as a **Polygon ID-compatible issuer node** with a custom DID method pointing to the Vietnamese L0. This provides immediate access to Polygon ID's wallet SDK, verifier contracts, and developer tooling — dramatically reducing implementation time and risk.

---

## 5. Interoperability with EU EUDI Wallet

The European Digital Identity Wallet (EUDI Wallet, eIDAS 2.0) will mandate cross-border digital identity recognition for EU residents and businesses interacting with Vietnam. The EUDI Wallet uses:
- ISO/IEC 18013-5 (mDL format) for driving licenses and national IDs
- W3C VC for other credential types
- OpenID for Verifiable Credentials (OID4VC) as the presentation protocol

The proposed `did:zkkyc-vn` method and W3C VC-based ZKC format are compatible with OID4VC, enabling future mutual recognition with EUDI Wallets — a strategic advantage for Vietnamese exporters and cross-border workers.

---

## References

- W3C Credentials Community Group. (2022). Verifiable Credentials Data Model v1.1. https://www.w3.org/TR/vc-data-model/
- W3C DID Working Group. (2022). Decentralized Identifiers (DIDs) v1.0. https://www.w3.org/TR/did-core/
- Looker, T., et al. (2023). *BBS Cryptosuite v2023* (W3C Draft). https://w3c.github.io/vc-di-bbs/
- iden3 team. (2021). *Baby Jubjub Elliptic Curve*. https://docs.iden3.io/publications/pdfs/Baby-Jubjub.pdf
- Polygon ID team. (2023). *Polygon ID Architecture Overview*. https://docs.polygonid.xyz
- European Commission. (2023). *EUDI Wallet Architecture Reference Framework v1.3*.
- Chandra, A. (2022). *Semaphore: Zero-Knowledge Signaling*. https://semaphore.appliedzkp.org
