# Semaphore and Polygon ID as Technical Precedents

## Overview

The ZK-KYC architecture proposed in this paper does not emerge from a theoretical vacuum. Two open-source systems — **Semaphore** and **Polygon ID** — have implemented core components of ZK-based identity in production environments, providing empirical validation of technical claims and practical implementation guidance. This section analyzes both systems as technical precedents, maps their architectures to the proposed ZK-KYC design, and derives lessons for national-scale deployment.

---

## 1. Semaphore: ZK Group Membership Signaling

### 1.1 System Description

Semaphore (appliedzkp.org) is a zero-knowledge protocol that allows members of a group to signal anonymously — proving membership without revealing identity. Originally developed by Barry WhiteHat and Kobigurk at the Ethereum Foundation (2019), it has since been formalized and maintained by the Applied ZKP group.

**Core mechanism:**
1. A user generates an identity: `identity_commitment = Poseidon(identity_secret, identity_nullifier)`
2. An authorized manager adds the commitment to an on-chain Merkle tree (the "group").
3. To signal (e.g., vote, authenticate, claim), the user generates a ZK proof that:
   - Their commitment is in the group's Merkle tree.
   - They know the `identity_secret`.
   - Their `nullifier = Poseidon(identity_secret, external_nullifier)` has not been used before in this context.

### 1.2 Production Deployments

| Project | Use Case | Scale |
|---|---|---|
| **Worldcoin (World ID)** | Proof of personhood (iris biometric → Semaphore group) | >6M users (2024) |
| **Unirep** | Anonymous reputation system | Research/production |
| **zkBridge** | Cross-chain anonymous signaling | Production |
| **Bandada** | Private group coordination | Production |
| **PSE Anon Voting** | Anonymous on-chain voting | Production pilots |

### 1.3 Mapping to ZK-KYC Architecture

| Semaphore Component | ZK-KYC Equivalent | Notes |
|---|---|---|
| Group manager | KYC issuer (bank, MoPS) | Manages who is added to the identity tree |
| Identity commitment | `Poseidon(identity_secret, attributes_hash)` | ZK-KYC extends with attribute binding |
| Merkle tree (on-chain) | L1 identity registry | Same structure; ZK-KYC anchors root to L0 |
| External nullifier | `context_id` (application scope) | Prevents cross-context linkability |
| Signal | `attribute_claim` | ZK-KYC adds predicate proofs on attributes |
| Verifier contract | L1 service verifier contract | Direct reuse possible |

**Key insight**: ZK-KYC is essentially a **Semaphore group where admission requires a verified KYC issuance**, and signals carry attribute claims rather than arbitrary messages. The core ZKP circuit can be derived from Semaphore's audited circuit with extensions for attribute predicate proofs.

### 1.4 Lessons from Semaphore

- **Circuit audit is non-negotiable**: Semaphore's circuit has undergone multiple independent audits (PSE, Audit team). For a national system, a similar level of scrutiny (2–3 independent audits from internationally recognized firms) is required before production deployment.
- **Merkle tree depth matters**: Semaphore uses configurable depth (20 = 1M members by default). For Vietnam's ~67M citizens, a depth of 27 is required (2^27 ≈ 134M). This is straightforward but must be specified upfront, as changing tree depth after deployment requires migrating all existing commitments.
- **Client library maturity**: Semaphore's JavaScript SDK (`@semaphore-protocol/identity`, `@semaphore-protocol/group`, `@semaphore-protocol/proof`) is production-ready and could be adapted for the ZK-KYC mobile wallet SDK.

---

## 2. Polygon ID: Production ZK Identity Infrastructure

### 2.1 System Description

Polygon ID (launched 2022) is a full-stack, W3C-aligned ZK identity system built on iden3's protocol. It is the most complete open-source implementation of ZK-native identity and the closest architectural parallel to the proposed ZK-KYC system.

**Architecture layers:**
```
User Wallet (Polygon ID App / SDK)
    │ holds W3C VCs with BJJ signatures
    │ generates ZK proofs on demand
    ▼
Issuer Node (KYC authority)
    │ issues credentials to user DIDs
    │ maintains identity and revocation SMTs
    ▼
Verifier (Service provider)
    │ defines query (e.g., "age > 18")
    │ verifies ZK proof on-chain or off-chain
    ▼
Blockchain (Polygon PoS / Ethereum)
    │ stores identity state hash
    │ stores revocation tree hash
    │ anchors issuer DID documents
```

### 2.2 Production Scale and Adoption

| Metric | Value (2024) |
|---|---|
| Issuer nodes deployed | >500 globally |
| Credentials issued | >10 million |
| Verifier integrations | >200 |
| Supported credential types | Government ID, KYC, education, membership |
| Audit status | Multiple audits by Veridise, Hexens |

Polygon ID has been adopted by major DeFi protocols for KYC compliance (Aave, Compound governance), EU identity pilots, and national government identity projects (Montenegro, Palau).

### 2.3 Mapping to ZK-KYC Architecture

| Polygon ID Component | ZK-KYC L0/L1 Equivalent |
|---|---|
| Identity State (iden3 SMT roots) | L1 identity + revocation Merkle roots |
| Blockchain (Polygon) | **L0** (decentralized trust anchor) |
| Issuer Node | KYC authority on L1 (bank, NDAChain) |
| Polygon ID Wallet | ZK-KYC citizen wallet app |
| Verifier contract | L1 service provider verifier |
| `did:polygonid` | `did:zkkyc-vn` (custom L0-anchored method) |

**Critical observation**: The L0 in the proposed architecture plays exactly the role that **Polygon PoS (the blockchain) plays in Polygon ID** — as the immutable anchor for identity state roots. The proposed architecture merely decouples this settlement layer from any single corporate or government entity and re-anchors it on a public BFT chain.

This means the **existing Polygon ID issuer node and verifier contract codebase can be directly adapted** for ZK-KYC by:
1. Replacing the `did:polygonid` resolver with a `did:zkkyc-vn` resolver pointing to L0.
2. Replacing Polygon PoS state anchoring with L0 `AnchorMerkleRoot` transactions.
3. Extending the credential schema with Vietnamese regulatory fields (KYC level, LPDP compliance flag).

### 2.4 Polygon ID Circuit Architecture

The `credentialAtomicQuerySig` circuit (the core Polygon ID ZKP circuit) proves:

```
Given:
  - A W3C VC signed with a BJJ signature
  - A Merkle path proving the VC's commitment is in the issuer's identity tree
  - A non-membership path proving the VC is not in the revocation tree

Prove (without revealing the VC):
  - The issuer's signature is valid on the VC
  - The VC's issuer is in the L0 trusted registry
  - The specific attribute claim satisfies the verifier's query
    (e.g., birthday.year <= 2007 for age > 18)
  - The nullifier for this context has not been used
```

This circuit directly implements all requirements of the ZK-KYC proof outlined in section 3 of the main paper. Adopting this circuit with appropriate modifications provides:
- An already-audited implementation (~50,000 Circom constraints)
- Existing mobile SDK support (iOS, Android, React Native)
- Compatibility with the global Polygon ID verifier ecosystem

### 2.5 Lessons from Polygon ID

- **Issuer node operational burden**: Running a Polygon ID issuer node requires maintaining an off-chain database of issued credentials (for revocation management) alongside the on-chain SMT roots. This operational complexity must be accounted for in the governance framework — KYC issuers (banks, government agencies) need technical capacity or a managed service option.
- **Credential schema governance**: Polygon ID uses a schema marketplace (schema.iden3.io). For ZK-KYC, a government-maintained credential schema registry (defining the exact fields and types for Vietnamese KYC credentials) is needed to ensure interoperability across all L1 issuers.
- **Query language standardization**: Polygon ID's Verifiable Presentation Request (VPR) query language allows verifiers to specify complex attribute predicates. Adopting this standard for ZK-KYC verifiers avoids inventing a new query language.

---

## 3. Worldcoin / World ID: Proof of Personhood at Scale

While not a KYC system, World ID (based on Semaphore + iris biometrics) is the largest deployed ZK identity system (>6M users). It demonstrates:

- **Hardware-assisted biometric binding**: The Orb device generates a `iris_commitment` that is added to the Semaphore group, binding a biometric to a ZK identity without storing the biometric on-chain. The ZK-KYC system can apply the same principle using Vietnamese CCCD chip biometrics (fingerprint, facial image) during issuance — the biometric hash becomes the identity commitment seed.
- **Sybil resistance at scale**: World ID successfully prevents one person from registering multiple times using biometric uniqueness checks on-device. For ZK-KYC, the equivalent is the existing CCCD (citizen ID card) database uniqueness constraint — the KYC issuer verifies the CCCD number is not already registered before issuing a ZKC.

---

## 4. Recommended Open-Source Stack

Based on the analysis of existing systems, the following open-source stack is recommended for the ZK-KYC implementation:

| Layer | Component | Source |
|---|---|---|
| **ZK circuits** | Polygon ID `credentialAtomicQuerySig` + extensions | Apache 2.0, github.com/iden3/circuits |
| **Circuit language** | Circom 2.x | MIT, github.com/iden3/circom |
| **Proving library** | snarkjs (browser/Node) + RapidSNARK (native) | GPL-3.0 |
| **Mobile wallet SDK** | Polygon ID Flutter SDK (adapted) | Apache 2.0 |
| **Issuer node** | Polygon ID issuer-node (adapted) | Apache 2.0 |
| **Verifier contracts** | Polygon ID verifier contracts (adapted) | Apache 2.0 |
| **Group management** | Semaphore contracts (for batch operations) | MIT |
| **DID resolver** | Universal Resolver + custom `did:zkkyc-vn` driver | Apache 2.0 |
| **Credential schema** | schema.iden3.io (forked for Vietnamese registry) | Open |

Total estimated open-source code reuse: **~70% of implementation effort**, with Vietnamese-specific customization focused on credential schemas, DID method, regulatory compliance fields, and L0 integration.

---

## References

- Baylina, J., & Bellés-Muñoz, M. (2021). *Baby Jubjub Elliptic Curve*. iden3. https://docs.iden3.io
- Chandra, A., & Gurkan, K. (2022). *Semaphore: Zero-Knowledge Signaling on Ethereum*. https://semaphore.appliedzkp.org
- Polygon ID team. (2023). *Polygon ID: Technical documentation*. https://docs.polygonid.xyz
- Worldcoin Foundation. (2023). *World ID 2.0: Technical whitepaper*. https://worldcoin.org/whitepaper
- WhiteHat, B. (2020). *Semaphore: A privacy gadget built on Ethereum*. https://medium.com/coinmonks/to-mixers-and-beyond-presenting-semaphore-a-privacy-gadget-built-on-ethereum-4c8b00857c9b
- PSE (Privacy + Scaling Explorations). (2023). *Semaphore audit report*. Ethereum Foundation.
