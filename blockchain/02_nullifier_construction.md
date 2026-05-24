# Nullifier Construction: Privacy-Preserving Anti-Sybil Mechanism

## Overview

Nullifiers are the cryptographic mechanism that prevents double-use of a credential (e.g., registering the same identity twice under different pseudonyms) without violating user privacy. This is one of the most technically subtle components of the ZK-KYC architecture and requires explicit specification.

---

## 1. The Core Problem: Sybil Resistance Without Linkability

In a privacy-preserving identity system, the verifier never sees the user's real identity. This creates an inherent tension:

- **Anti-Sybil requirement**: The system must prevent one real person from obtaining multiple digital identities or submitting the same credential multiple times in contexts where uniqueness matters (e.g., one vote per person, one bank account per citizen).
- **Privacy requirement**: The mechanism that enforces uniqueness must not allow a verifier — or an observer of the L0 ledger — to correlate different uses of the same credential across contexts (unlinkability).

A naive approach (publishing a hash of the identity) would solve Sybil resistance but enable full linkability: every service the user visits would see the same identifier, effectively re-creating a national ID number on-chain.

---

## 2. Nullifier Construction Design

### 2.1 Context-Scoped Nullifiers

The solution is to make the nullifier **context-dependent**, so that the same underlying identity produces a *different* nullifier for each application context, while still being deterministic within a context (preventing re-use within that context).

**Nullifier derivation formula:**

```
nullifier = Poseidon(identity_secret, context_id)
```

Where:
- `identity_secret` is a secret scalar known only to the user, derived from their ZKC issuance process and stored in their wallet.
- `context_id` is a public, application-specific identifier (e.g., a smart contract address, a service domain hash, or a regulatory scope identifier such as `"AML_BANKING_VN_2025"`).

**Properties:**
- The same user visiting Bank A and Bank B produces different nullifiers → **cross-context unlinkability**.
- The same user attempting to register twice at Bank A produces the same nullifier → **intra-context Sybil prevention**.
- The nullifier reveals nothing about `identity_secret` (one-way function) → **zero-knowledge**.

### 2.2 Full Nullifier Circuit Constraint

Within the ZK-KYC proving circuit, the nullifier is verified as follows:

```
// Private inputs
identity_secret : Fp  // user's secret key
identity_commitment : Fp  // Poseidon(identity_secret, attribute_hash)

// Public inputs
nullifier : Fp
context_id : Fp  // provided by the verifying application

// Circuit constraints
assert nullifier == Poseidon(identity_secret, context_id)
assert identity_commitment is member of merkle_tree(merkle_root)
```

The proof simultaneously demonstrates:
1. The nullifier was correctly derived from a real `identity_secret`.
2. That `identity_secret` corresponds to a commitment registered on L0.
3. No other information about the user is leaked.

---

## 3. On-Chain Nullifier Registry

To enforce uniqueness, verifying contracts on L1 must maintain a **nullifier set**: a mapping of previously seen nullifiers for a given context.

```solidity
// Simplified L1 verifier contract
contract ZKKYCVerifier {
    // context_id => nullifier => used
    mapping(bytes32 => mapping(bytes32 => bool)) public nullifierRegistry;

    function verify(
        bytes calldata proof,
        bytes32 merkleRoot,
        bytes32 nullifier,
        bytes32 contextId,
        bytes32 attributeClaim
    ) external returns (bool) {
        require(!nullifierRegistry[contextId][nullifier], "Nullifier already used");
        require(isValidMerkleRoot(merkleRoot), "Stale or invalid root");
        require(verifyProof(proof, merkleRoot, nullifier, contextId, attributeClaim), "Invalid proof");

        nullifierRegistry[contextId][nullifier] = true;
        emit VerificationSucceeded(nullifier, contextId, attributeClaim);
        return true;
    }
}
```

**Key design decisions:**
- The nullifier registry is **scoped per `context_id`**, not global. This means L1 contracts for banking, voting, and e-commerce each maintain their own nullifier set — preventing cross-domain correlation even at the contract level.
- The `merkleRoot` parameter is validated against the L0-anchored root, ensuring only KYC-issued identities are accepted (see: L0/L1 Interoperability).

---

## 4. Nullifier Lifecycle and Credential Revocation Interaction

A nuance arises when a credential is revoked (e.g., the user loses their device or the KYC provider discovers fraud): previously issued nullifiers may still be valid in the nullifier registry but the underlying identity is no longer valid.

Two mitigation strategies:

### Strategy A: Short-lived Nullifiers (Recommended for high-risk contexts)
Include a **timestamp or epoch number** in the nullifier derivation:
```
nullifier = Poseidon(identity_secret, context_id, epoch)
```
Applications require proofs generated within the current epoch (e.g., valid for 24 hours). This forces re-verification periodically, giving revocation events time to propagate before the next valid nullifier can be generated.

### Strategy B: Nullifier Binding to Credential Version
Include the **credential version hash** in the nullifier:
```
nullifier = Poseidon(identity_secret, context_id, credential_version)
```
When a credential is revoked and re-issued (with a new `credential_version`), all prior nullifiers become unusable even if the `identity_secret` is known. This is suitable for lower-frequency, high-stakes operations (property registration, voting).

---

## 5. Comparison with Existing ZK Identity Systems

| System | Nullifier Construction | Scope |
|---|---|---|
| **Zcash (Sapling)** | `PRF_nf(spending_key, rho)` | Per-note (single-use) |
| **Semaphore** | `Poseidon(identity_secret, externalNullifier)` | Per signal/group |
| **Polygon ID** | Signal-scoped, derived from private key | Per credential presentation |
| **Proposed ZK-KYC** | `Poseidon(identity_secret, context_id [, epoch])` | Per service context |

The proposed construction most closely follows Semaphore's model (Chandra & Gurkan, 2022), which has been formally analyzed and is deployed in production (Unirep, Worldcoin's privacy layer).

---

## 6. Security Assumptions and Threat Model

| Threat | Mitigation |
|---|---|
| Adversary learns `nullifier` and attempts to reverse `identity_secret` | Poseidon is one-way under standard hash security assumptions |
| Two applications collude to link nullifiers to one user | Impossible: different `context_id` → different nullifier |
| User reuses credential in same context | Detected: nullifier already in registry |
| Compromised KYC issuer generates fake identities | Nullifiers still valid but underlying Merkle root is corrupted — addressed in revocation (see: `05_revocation_mechanism.md`) |
| Quantum adversary inverts Poseidon | Low risk: Poseidon's security over prime fields has no known quantum speedup beyond Grover's algorithm (halves bit security, manageable with 256-bit fields) |

---

## References

- Gabizon, A. (2016). How transactions between shielded addresses work. *Zcash Blog*.
- Bowe, S., Gabizon, A., & Green, M. (2019). A multi-party protocol for constructing the public parameters of the Pinocchio zk-SNARK. *Financial Cryptography Workshops 2018*.
- Chandra, A., & Gurkan, K. (2022). *Semaphore: Zero-Knowledge Signaling on Ethereum*. https://semaphore.appliedzkp.org
- Grassi, L., et al. (2021). Poseidon: A new hash function for Zero-Knowledge proof systems. *USENIX Security 21*.
- Worldcoin Foundation. (2023). *World ID Protocol: Technical whitepaper*. https://worldcoin.org/whitepaper
