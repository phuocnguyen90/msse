# ZKP Scheme Selection: Groth16 vs. PLONK vs. STARK

## Overview

Zero-Knowledge Proof (ZKP) systems are not monolithic. The choice of proving scheme fundamentally determines the trust model, proof size, verification cost, and long-term upgradeability of the ZK-KYC architecture. This section provides a comparative analysis and justifies the recommended scheme for national-scale deployment.

---

## 1. Comparison of Candidate Schemes

| Property | Groth16 | PLONK (UltraPLONK) | zk-STARKs |
|---|---|---|---|
| **Setup** | Per-circuit trusted setup (MPC ceremony) | Universal trusted setup (one-time MPC) | Transparent — no trusted setup |
| **Proof size** | ~200 bytes (smallest) | ~400–800 bytes | ~50–200 KB |
| **Verification time** | ~1–2 ms (constant) | ~2–5 ms (constant) | ~10–50 ms (scales with log²) |
| **Prover time (mobile)** | ~1–3s (mid-range device) | ~2–5s | ~5–30s |
| **Post-quantum safe** | No (BN254 pairing) | No (KZG commitment) | **Yes** (hash-based) |
| **Circuit upgradeability** | Requires new ceremony per change | Reuse universal SRS | No ceremony needed |
| **Ecosystem maturity** | Very mature (Zcash, Tornado Cash) | Mature (Aztec, Polygon zkEVM) | Mature (StarkWare, Polygon Miden) |

---

## 2. Analysis for ZK-KYC Context

### 2.1 Groth16 — Not Recommended as Primary Scheme

Groth16 produces the smallest proofs and fastest verification, making it attractive for mobile clients. However, its critical flaw for a national identity system is the **per-circuit trusted setup requirement**. Each time the KYC credential circuit is modified (e.g., to add a new attribute field, change age verification logic, or patch a vulnerability), a new multi-party computation (MPC) ceremony must be conducted. For a static, well-defined circuit this is acceptable (Zcash has run this ceremony successfully). However, for a national system expected to evolve over years — adding biometric attributes, new regulatory fields, or PQ-safe migrations — this is operationally burdensome and creates governance risk: a ceremony with insufficient participants or that is compromised invalidates the security of all proofs generated under that circuit.

### 2.2 PLONK / UltraPLONK — **Recommended**

PLONK (Gabizon et al., 2019) addresses the principal weakness of Groth16 through its **universal and updatable Structured Reference String (SRS)**. A single MPC ceremony produces a reference string that can support *any* circuit up to a maximum size. Circuit updates, new credential types, and logic changes require only a new circuit compilation step — not a new ceremony. This is decisive for a long-lived national infrastructure.

Key properties for ZK-KYC:
- **Proof size** (~400–800 bytes) remains compact enough for mobile wallets and on-chain storage.
- **Verification is constant-time** (~2–5 ms), suitable for high-frequency L1 verifier contracts.
- **Custom gates** in UltraPLONK natively support range proofs (e.g., `age >= 18`) and hash functions efficiently, directly mapping to KYC attribute checks.
- **Ecosystem**: Aztec Protocol, Polygon zkEVM, and Noir language all support PLONK, providing a mature toolchain.

**Recommended proving system: UltraPLONK with KZG polynomial commitments.**

### 2.3 zk-STARKs — Recommended for Long-Term PQ Migration Path

STARKs require no trusted setup (fully transparent) and are post-quantum secure because their security relies only on collision-resistant hash functions, not on elliptic curve discrete logarithm assumptions. This makes them the natural migration target when quantum threats materialize.

Current limitations for immediate ZK-KYC deployment:
- Large proof size (50–200 KB) is too heavy for on-device storage in wallet credentials and increases L0 anchoring gas costs.
- Slower prover time (5–30s on mobile) creates unacceptable UX for routine KYC checks.

**Recommendation**: Architect the credential format and verifier contracts to be **proof-system agnostic** from day one (Section: L0/L1 Interoperability). STARKs should be adopted as the primary scheme once proof sizes decrease to <10 KB, which is expected within 3–5 years based on current research trajectories (e.g., Polygon Miden, RISC Zero).

---

## 3. Hash Function: Poseidon

The choice of ZKP-friendly hash function is equally critical to performance. Standard SHA-256 or SHA-3, while cryptographically well-understood, are highly inefficient inside arithmetic circuits (requiring thousands of constraints per invocation). For the Merkle tree, commitment scheme, and nullifier derivation within ZK-KYC circuits, this paper recommends **Poseidon** (Grassi et al., 2021).

Poseidon is an algebraic hash function designed specifically for ZK proof systems operating over prime fields. Its constraint count is approximately 8× lower than MiMC and 100× lower than SHA-256 in R1CS/PLONK representations, directly translating to faster proof generation on mobile devices.

**Poseidon is already used by**: Zcash (Sapling), Filecoin, Polygon ID, and Semaphore — giving it the de facto status of the ZK-identity hash standard.

---

## 4. Circuit Architecture for ZK-KYC

The core ZK-KYC proving circuit takes the following private inputs (witness) and produces a compact proof verifiable against public inputs:

```
Private inputs (witness — never leaves user device):
  - identity_secret         : scalar field element (256-bit)
  - identity_attributes     : [name_hash, dob, nationality, ...]
  - merkle_path             : [sibling_hashes × tree_depth]

Public inputs (revealed to verifier):
  - merkle_root             : commitment to current identity set on L0
  - nullifier               : Poseidon(identity_secret, context_id)
  - attribute_claim         : e.g., "age >= 18" or "nationality == VN"
  - issuer_id               : identifier of the KYC issuing authority

Circuit constraints:
  1. Poseidon(identity_secret, identity_attributes) == identity_commitment
  2. MerkleProof(identity_commitment, merkle_path) == merkle_root
  3. nullifier == Poseidon(identity_secret, context_id)
  4. attribute_claim correctly derived from identity_attributes
```

This circuit proves: *"I possess a valid ZKC issued by an authorized KYC provider, my identity is included in the current L0 registry, and the claimed attribute is true — without revealing any other personal information."*

---

## 5. Implementation Toolchain Recommendation

| Component | Recommended Tool | Rationale |
|---|---|---|
| Circuit language | **Noir** (Aztec) or **Circom** | Noir is higher-level, safer; Circom has larger community |
| Proving backend | **Barretenberg** (PLONK) | Native UltraPLONK, used in production by Aztec |
| Mobile SDK | **snarkjs** (WASM) / Aztec SDK | Runs in browser and React Native environments |
| Hash primitive | **Poseidon** | ZK-optimized, widely audited |
| On-chain verifier | Solidity verifier (auto-generated) | Low verification cost (~200k gas) |

---

## References

- Gabizon, A., Williamson, Z. J., & Ciobotaru, O. (2019). PLONK: Permutations over Lagrange-bases for oecumenical noninteractive arguments of knowledge. *IACR ePrint 2019/953*.
- Grassi, L., Khovratovich, D., Rechberger, C., Roy, A., & Schofnegger, M. (2021). Poseidon: A new hash function for Zero-Knowledge proof systems. *USENIX Security 21*, 519–535.
- Groth, J. (2016). On the size of pairing-based non-interactive arguments. *EUROCRYPT 2016*, LNCS 9666, 305–326.
- Ben-Sasson, E., et al. (2018). Scalable, transparent, and post-quantum secure computational integrity. *IACR ePrint 2018/046*.
- Polygon ID team. (2023). *Polygon ID documentation: Circuit design*. https://docs.polygonid.xyz
