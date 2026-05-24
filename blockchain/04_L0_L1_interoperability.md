# L0/L1 Interoperability Protocol: Trust-Minimized Anchoring

## Overview

The proposed ZK-KYC architecture derives its security and sovereignty guarantees from a clean separation between the L0 public trust layer and the L1 application chains (such as NDAChain). However, this separation is only as strong as the **interoperability protocol** that connects them. This document specifies how L1 chains anchor their state to L0, how verifiers validate proofs against L0-anchored roots, and how the system avoids re-introducing centralization through the bridge mechanism itself.

---

## 1. Core Problem: Cross-Layer State Verification

An L1 KYC system maintains its own Merkle tree of registered identity commitments. When a user presents a ZK proof on L1, the verifier contract checks:

```
MerkleProof(identity_commitment, merkle_path) == merkle_root
```

But who guarantees that the `merkle_root` itself is authentic and has not been tampered with by the L1 operator? Without a neutral trust anchor, the L1 operator (e.g., NDAChain administrators) can unilaterally insert fake identities, censor legitimate ones, or roll back the identity set.

**The solution**: L1 periodically commits a hash of its current identity Merkle root to L0. Once anchored on L0, this root is immutable and publicly auditable, even if the L1 operator is compromised or acts maliciously.

---

## 2. Anchoring Protocol

### 2.1 L1 → L0 Root Anchoring

At regular intervals (or upon each significant identity set update), an authorized L1 operator submits an `AnchorMerkleRoot` transaction to L0:

```
AnchorMerkleRoot {
    l1_chain_id     : bytes32    // unique identifier for the L1 chain
    l1_block_height : uint64     // L1 block at which the root was computed
    identity_root   : bytes32    // Poseidon Merkle root of identity commitments
    revocation_root : bytes32    // Sparse Merkle root of revoked credentials
    timestamp       : uint64     // Unix timestamp
    operator_sig    : bytes64    // L1 operator's signature (registered on L0)
}
```

Upon acceptance by L0 validators, this anchor is permanently recorded and indexed by `(l1_chain_id, l1_block_height)`.

**Anchoring frequency:**
- For high-frequency L1 chains (banking): every 10 minutes or 1,000 new registrations, whichever comes first.
- For low-frequency L1 chains (government services): daily batch.
- Emergency anchoring: immediately upon mass revocation events.

### 2.2 L0 Anchor Contract Interface (Pseudocode)

```solidity
interface IL0AnchorRegistry {
    struct Anchor {
        bytes32 identityRoot;
        bytes32 revocationRoot;
        uint64  l1BlockHeight;
        uint64  timestamp;
        address operator;
    }

    // Submit a new anchor from an authorized L1
    function submitAnchor(
        bytes32 l1ChainId,
        Anchor calldata anchor,
        bytes calldata operatorSignature
    ) external;

    // Query the latest anchor for a given L1
    function getLatestAnchor(bytes32 l1ChainId)
        external view returns (Anchor memory);

    // Query a historical anchor (for audit/dispute)
    function getAnchorAtHeight(bytes32 l1ChainId, uint64 l1BlockHeight)
        external view returns (Anchor memory);

    // Check if a given root was ever valid for an L1
    function wasRootValid(bytes32 l1ChainId, bytes32 identityRoot)
        external view returns (bool, uint64 validFrom, uint64 validUntil);
}
```

---

## 3. Proof Verification Flow (End-to-End)

```
┌─────────────────────────────────────────────────────────┐
│                     USER DEVICE                         │
│                                                         │
│  1. Fetch latest anchor from L0:                        │
│     anchor = L0.getLatestAnchor("NDAChain")             │
│     merkle_root = anchor.identityRoot                   │
│                                                         │
│  2. Generate ZK proof (UltraPLONK):                     │
│     proof = prove(                                      │
│       witness:  { identity_secret, attributes,          │
│                   merkle_path },                        │
│       public:   { merkle_root, nullifier,               │
│                   attribute_claim, context_id }         │
│     )                                                   │
│                                                         │
│  3. Submit to L1 verifier:                              │
│     L1Verifier.verify(proof, merkle_root, nullifier,    │
│                        context_id, attribute_claim)     │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  L1 VERIFIER CONTRACT                   │
│                                                         │
│  4. Check nullifier not reused                          │
│  5. Validate merkle_root against L0:                    │
│     assert L0.wasRootValid("NDAChain", merkle_root)     │
│  6. Verify ZK proof (on-chain verifier)                 │
│  7. Mark nullifier as used                              │
│  8. Emit VerificationSucceeded event                    │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  L0 ANCHOR REGISTRY                     │
│                                                         │
│  (Immutable record of all historical Merkle roots)      │
│  (Publicly auditable by regulators, civil society)      │
└─────────────────────────────────────────────────────────┘
```

**Critical**: The L1 verifier contract **does not trust the proof-submitter's claimed Merkle root**. It independently queries L0 to confirm that the submitted root was indeed anchored by the legitimate L1 operator at some point in the past. This prevents an attacker from submitting a proof against a fabricated root.

---

## 4. Handling Merkle Root Staleness

A ZK proof is always generated against a specific Merkle root (the one anchored to L0 at the time the user fetches it). Since the identity set grows over time, older roots become "stale" — they do not reflect more recently registered or revoked identities.

**Staleness policy:**

```
Proof accepted if:
  anchor.timestamp >= now - MAX_PROOF_STALENESS
  AND anchor.revocationRoot is current (checked separately)

MAX_PROOF_STALENESS:
  - Low-risk context (loyalty programs, age verification): 7 days
  - Medium-risk context (banking onboarding): 24 hours
  - High-risk context (large financial transfers, voting): 1 hour
```

Verifying applications on L1 set their own staleness threshold in their contract configuration. Users whose proof is rejected due to staleness must regenerate a new proof against the latest root — a process that takes seconds on a modern device.

**Note**: Revocation root staleness is more critical than identity root staleness. Even if the identity root is 24 hours old, a revocation that occurred 1 hour ago must be reflected. This motivates a **dual-root architecture**: the identity Merkle root and revocation Sparse Merkle root are anchored separately, with different update frequencies.

---

## 5. Multi-L1 Interoperability

Multiple L1 chains may coexist under the same L0 (e.g., NDAChain for government services, a banking consortium L1, a healthcare L1). A user holding ZKCs from different L1 issuers can present them to any L1 verifier, provided:

1. The issuing L1 is registered on L0 (via `RegisterL1` governance transaction).
2. The verifying L1 explicitly trusts the issuing L1 (configurable whitelist in the verifier contract).

This creates a federated identity network where:
- **Intra-L1 verification** (same issuer and verifier chain): direct root lookup.
- **Cross-L1 verification** (different issuer and verifier): both roots are anchored on L0, enabling trustless cross-chain verification without a bridge operator.

---

## 6. Comparison with Existing Interoperability Protocols

| Protocol | Mechanism | Relevance to ZK-KYC |
|---|---|---|
| **IBC (Cosmos Inter-Blockchain Communication)** | Light client proofs of counterparty chain state | Closest analogue; could be adapted for L0/L1 root verification |
| **Polkadot XCMP** | Relay chain validates parachain state | Direct architectural precedent for L0 role |
| **Ethereum L2 bridges** | Optimistic or ZK rollup state roots posted to L1 | ZK rollup anchoring is essentially the same mechanism proposed here |
| **W3C DID Resolution** | DID documents resolve via DID method registries | Complementary standard for credential issuer identification |

The proposed anchoring protocol most closely resembles the **ZK rollup state commitment** model, where an L2 operator posts a compressed state root (here: identity Merkle root) to a settlement layer (here: L0), enabling trustless verification without replaying all L2 transactions.

---

## References

- Kwon, J., & Buchman, E. (2016). Cosmos: A Network of Distributed Ledgers.
- Wood, G. (2016). Polkadot: Vision for a Heterogeneous Multi-Chain Framework. *Polkadot Whitepaper*.
- Thibault, L. T., Bhatt, T., & Cécile, C. (2022). Blockchain Scaling Using Rollups: A Comprehensive Survey. *IEEE Access*, 10.
- W3C Credentials Community Group. (2022). Decentralized Identifiers (DIDs) v1.0. https://www.w3.org/TR/did-core/
