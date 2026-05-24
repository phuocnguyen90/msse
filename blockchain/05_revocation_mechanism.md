# Revocation Mechanism: Privacy-Preserving Credential Invalidation

## Overview

Credential revocation is one of the most technically challenging problems in privacy-preserving identity systems. In traditional PKI, revocation is straightforward but privacy-invasive: a Certificate Revocation List (CRL) or OCSP server publicly lists all revoked certificate serial numbers. In a ZK-KYC system, naive publication of revoked credential identifiers would break unlinkability — an observer could correlate revocation events with specific users.

This document specifies a privacy-preserving revocation mechanism suitable for a national ZK-KYC system, addressing the fundamental **privacy-revocation tension**.

---

## 1. The Privacy-Revocation Tension

A revocation mechanism must satisfy two contradictory-seeming requirements:

1. **Effectiveness**: When a credential is revoked (lost device, fraud detected, user request), all subsequent proofs using that credential must fail verification — immediately and universally across all L1 verifiers.
2. **Privacy**: The act of checking whether a credential is revoked must not reveal *which* credential is being checked, preventing observers from building a revocation-based linkability attack.

Specifically, a naive approach where revoked credential commitments are published in a public list would allow an adversary to check every identity commitment in the set against the revocation list, identifying which users have been revoked and correlating their activities.

---

## 2. Candidate Revocation Schemes

### 2.1 Certificate Revocation List (CRL) — Not Recommended

Publish a list of revoked credential hashes on L0. Simple to implement but:
- **Privacy violation**: Revoked identities are publicly identified.
- **Scalability issue**: List grows unboundedly; full download required for offline verification.
- Inappropriate for a ZK privacy system.

### 2.2 RSA/Pairing-Based Accumulators — Viable but Complex

A cryptographic accumulator compresses a set of values into a single digest, with the property that membership (or non-membership) can be proven without revealing the set.

**Non-membership proof via RSA accumulator:**
- Revoked credentials are accumulated into a single value `acc`.
- A user proves: `credential ∉ revocation_set` without revealing `credential`.
- Proof size: ~256 bytes; verification: ~1 ms.

**Drawbacks:**
- RSA accumulators require a **trusted setup** for the modulus `N = pq` (if `p` and `q` are known, the accumulator is forgeable).
- Dynamic updates (adding new revocations) require recomputing witness for all non-revoked credentials — computationally expensive at national scale.

### 2.3 Sparse Merkle Tree (SMT) Non-Membership Proof — **Recommended**

A Sparse Merkle Tree is a Merkle tree over the full key space (e.g., 2^256 leaves), where most leaves are empty. A credential commitment is mapped to a leaf: empty leaf = valid, non-empty leaf = revoked.

**Non-membership proof:**
To prove that `credential` is *not* revoked, the user proves:
```
SparseMerkleProof(credential_commitment, revocation_tree_root) == EMPTY_LEAF
```

This is a standard Merkle inclusion proof of the "empty" value at the credential's position. The proof reveals:
- That the credential mapped to position X in the tree.
- That position X is empty (not revoked).
- Nothing about which credential it is (the commitment is a one-way function of the identity secret).

**Properties:**
- **No trusted setup**: Pure hash-based, transparent.
- **Constant proof size**: O(tree_depth) = O(256) hashes ≈ 8 KB using Poseidon.
- **Efficient updates**: Adding a revocation only requires updating a single path (O(log N) operations).
- **Batch updates**: Multiple revocations can be processed in one SMT update, with the new root published as a single L0 anchor.
- **Used in production**: iden3 (Polygon ID), Merkle Patricia Tries (Ethereum state), Signal Protocol.

---

## 3. Proposed Revocation Architecture

### 3.1 Dual-Root Structure

The L0 anchor for each L1 contains two Merkle roots:

```
Anchor {
    identity_root    : bytes32   // Merkle root of all registered identity commitments
    revocation_root  : bytes32   // Sparse Merkle root of all revoked commitments
    timestamp        : uint64
}
```

The ZK-KYC proving circuit is extended with a non-membership proof:

```
// Extended circuit public inputs
merkle_root        : bytes32    // identity Merkle root
revocation_root    : bytes32    // revocation SMT root
nullifier          : bytes32
attribute_claim    : bytes32

// Additional private inputs
revocation_path    : [sibling_hashes × 256]  // SMT non-membership path

// Additional circuit constraint
assert SparseMerkleNonMembership(
    identity_commitment,
    revocation_path,
    revocation_root
) == true
```

The user's wallet automatically fetches the latest revocation root from L0 and includes the non-membership proof in every ZK proof generation. The verifier checks both the identity root (inclusion) and revocation root (non-inclusion) simultaneously in a single proof.

### 3.2 Revocation Issuance Process

```
┌──────────────────────────────────────────────────────────┐
│              REVOCATION EVENT TRIGGER                    │
│  (Lost device / Fraud detected / User request)           │
└─────────────────────┬────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────┐
│           KYC ISSUER (Authorized L1 Operator)            │
│                                                          │
│  1. Identify credential_commitment to revoke             │
│     (from issuer's internal KYC record — NOT public)     │
│  2. Update revocation SMT:                               │
│     new_revocation_root = SMT.insert(                    │
│         credential_commitment, REVOKED_FLAG              │
│     )                                                    │
│  3. Anchor to L0:                                        │
│     L0.submitAnchor(l1_chain_id, {                       │
│         identity_root: unchanged,                        │
│         revocation_root: new_revocation_root,            │
│         timestamp: now                                   │
│     })                                                   │
└──────────────────────────────────────────────────────────┘
                      │
                      ▼  (within next anchor interval — max 10 min)
┌──────────────────────────────────────────────────────────┐
│           L0 PUBLIC ANCHOR REGISTRY                      │
│  New revocation_root is globally visible                 │
│  All L1 verifiers now reject proofs from revoked cred    │
└──────────────────────────────────────────────────────────┘
```

**Key privacy property**: The issuer inserts `credential_commitment` (a hash, not raw identity data) into the SMT. The public SMT root changes, but no observer can determine *which* credential was revoked from the root change alone. The only entity that knows the mapping from `credential_commitment` to a real person is the issuer — who already had that information.

---

## 4. Revocation Latency and Risk Tiering

Different contexts require different revocation propagation guarantees:

| Risk Level | Example Use Case | Max Revocation Latency | Verification Requirement |
|---|---|---|---|
| **Critical** | Voting, large transfers | < 15 minutes | Proof must use root anchored within last 1 hour |
| **High** | Banking KYC, loan approval | < 2 hours | Proof must use root anchored within last 24 hours |
| **Medium** | E-commerce, hotel check-in | < 24 hours | Proof must use root anchored within last 7 days |
| **Low** | Age verification, newsletter | Best effort | No staleness check on revocation root |

L1 verifier contracts encode the applicable tier in their configuration, automatically rejecting proofs with revocation roots older than the allowed threshold.

---

## 5. Emergency Revocation

For high-severity cases (mass credential compromise, issuer key leakage), the standard batch anchor cycle is too slow. An **emergency revocation path** is defined:

1. Authorized issuers may submit an `EmergencyRevocation` transaction to L0 directly, bypassing the normal batch cycle.
2. L0 validators process this within 1 block (~5 seconds under Tendermint BFT).
3. A global `EMERGENCY_REVOCATION_FLAG` is set for the affected L1 chain, causing all L1 verifiers to reject *all* proofs from that chain until a clean revocation root is anchored.

This is a nuclear option reserved for catastrophic events, analogous to a CA certificate distrust action in traditional PKI.

---

## 6. Comparison with Existing Systems

| System | Revocation Method | Privacy-Preserving? | Proof Overhead |
|---|---|---|---|
| **Traditional PKI (OCSP)** | Online query to CA server | No | Network round trip |
| **W3C VC Status List 2021** | Bitstring at known URL | Partial (bit position linkable) | ~1 KB download |
| **Iden3 / Polygon ID** | Sparse Merkle Tree non-membership | **Yes** | ~8 KB Poseidon path |
| **Hyperledger Indy** | Tails file + cryptographic accumulator | Yes | ~256 bytes |
| **Proposed ZK-KYC** | SMT non-membership (dual-root) | **Yes** | ~8 KB, in-circuit |

---

## References

- Reyzin, L., & Reyzin, N. (2002). Better than BiBa: Short one-time signatures with fast signing and verifying. *ACISP 2002*, LNCS 2384, 144–153.
- Boneh, D., Bünz, B., & Fisch, B. (2019). Batching techniques for accumulators with applications to IOPs and stateless blockchains. *CRYPTO 2019*.
- iden3 team. (2021). *Iden3 Sparse Merkle Tree specification*. https://docs.iden3.io
- Sporny, M., et al. (2023). *Verifiable Credential Status List 2021* (W3C Working Draft). https://www.w3.org/TR/vc-status-list/
- Polygon ID team. (2023). *Polygon ID: On-chain verification with revocation*. https://docs.polygonid.xyz/verifier/on-chain-verification/
