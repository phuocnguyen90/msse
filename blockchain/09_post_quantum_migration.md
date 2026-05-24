# Post-Quantum Security Migration Path

## Overview

The cryptographic foundations of the proposed ZK-KYC architecture — specifically elliptic curve pairings (BN254) used in PLONK/Groth16 and KZG polynomial commitments — are vulnerable to attacks by sufficiently powerful quantum computers via Shor's algorithm. For a national identity infrastructure expected to operate for decades, quantum resilience is not merely an academic concern but a long-term security requirement.

This document specifies the concrete migration path to post-quantum (PQ) secure cryptography, including timeline estimates, interim mitigations, and the architectural features of the L0/L1 design that enable this migration without disrupting existing credentials.

---

## 1. Quantum Threat Assessment

### 1.1 Vulnerable Components

| Component | Algorithm | Quantum Attack | Time to Break (CRQC) |
|---|---|---|---|
| ZKP proving system (PLONK/Groth16) | KZG commitments over BN254 | Shor's algorithm on ECDLP | Hours (with 4,000+ logical qubits) |
| BJJ signatures (credential issuance) | Baby Jubjub EC signatures | Shor's algorithm | Hours |
| Nullifier derivation (Poseidon) | Hash function | Grover's algorithm (quadratic speedup) | Doubles required input size |
| Merkle tree (Poseidon) | Hash function | Grover's algorithm | Manageable: 256-bit → effective 128-bit |
| DID key pairs (BN254/BLS) | Elliptic curve | Shor's algorithm | Hours |

**Key distinction**: Hash-based components (Poseidon Merkle trees, nullifiers) face only a *quadratic* speedup from Grover's algorithm, which is mitigated by using 256-bit inputs (leaving 128-bit effective security — acceptable for most threat models). **Elliptic curve components face complete breakage** via Shor's algorithm on a Cryptographically Relevant Quantum Computer (CRQC).

### 1.2 Timeline Estimates

Expert consensus on CRQC timelines (as of 2025):
- **IBM, Google**: "Fault-tolerant CRQC by 2033–2040" (based on current error-correction progress)
- **NIST**: "Act as if capable adversaries will break current EC crypto by 2030" (PQC transition guidance)
- **NSA**: Mandated migration away from EC-based systems for national security systems by 2030

**For a system deployed in 2026–2028, the risk window is 5–15 years** — entirely within the expected operational lifetime of a national identity infrastructure. Quantum migration must be planned now, not retroactively.

### 1.3 "Harvest Now, Decrypt Later" Risk

Even before a CRQC exists, adversaries can record encrypted ZKP transcripts today and decrypt them retroactively once quantum computers mature. For identity systems, this means:
- Encrypted KYC verification sessions recorded in 2026 could be decrypted in 2035, potentially revealing user identity patterns.
- Credential issuance signatures recorded today could be forged in the future to create backdated fraudulent credentials.

This justifies **beginning PQ migration before CRQCs exist**, particularly for the highest-assurance components (credential issuance signatures).

---

## 2. NIST Post-Quantum Standards (2024)

NIST finalized its first PQ cryptography standards in August 2024:

| Standard | Algorithm | Type | Use Case in ZK-KYC |
|---|---|---|---|
| **FIPS 203** | ML-KEM (CRYSTALS-Kyber) | Key Encapsulation | Secure channel for issuer-user communication |
| **FIPS 204** | ML-DSA (CRYSTALS-Dilithium) | Digital Signature | **Credential issuance signatures** (replace BJJ) |
| **FIPS 205** | SLH-DSA (SPHINCS+) | Hash-based Signature | Backup signing; long-term archival |

**Not yet standardized (in evaluation):**
- **FALCON** (NIST Round 4): Compact lattice-based signatures; likely standardized 2025–2026.
- **PQ-ZKPs**: Hash-based (STARKs) or lattice-based ZK proofs. No NIST standard yet; research-stage.

---

## 3. Migration Strategy: Three-Phase Approach

The migration is structured across three phases, each corresponding to a different risk level and implementation complexity:

### Phase 1 (2026–2028): Crypto-Agility Infrastructure

**Goal**: Ensure the system can swap cryptographic algorithms without re-issuing all credentials or redeploying the L0 chain.

**Actions:**
1. **Versioned credential schema**: Every ZKC includes a `cryptoVersion` field:
   ```json
   {
     "credentialSubject": { ... },
     "cryptoVersion": "v1-plonk-bn254",
     "proof": { "type": "BJJSignature2021", ... }
   }
   ```
   Version `v2-dilithium3` and `v3-stark-poseidon` are pre-defined in the schema registry.

2. **Algorithm-agnostic verifier contracts**: L1 verifier contracts dispatch to different ZK verification modules based on the `cryptoVersion` in the proof:
   ```solidity
   function verify(bytes calldata proof, bytes32 version, ...) external {
       if (version == keccak256("v1-plonk-bn254")) {
           return _verifyPlonk(proof, ...);
       } else if (version == keccak256("v3-stark-poseidon")) {
           return _verifyStark(proof, ...);
       }
       revert("Unsupported crypto version");
   }
   ```

3. **L0 anchor format includes crypto version**: The `AnchorMerkleRoot` transaction includes the hash function used for the Merkle tree, allowing future anchors to use PQ-safe hashes.

**Outcome**: No user impact. The system silently supports multiple algorithms simultaneously. New credentials can be issued in the new scheme while old credentials remain valid.

---

### Phase 2 (2028–2031): Hybrid Signatures on New Credentials

**Goal**: New credentials issued after Phase 2 launch use **dual signatures**: a classical BJJ signature (for current verifier compatibility) and a PQ Dilithium3 signature (for future-proofed security).

**Credential structure:**
```json
{
  "proof": [
    {
      "type": "BJJSignature2021",
      "proofValue": "z3cBs...",
      "validUntil": "2031-01-01"
    },
    {
      "type": "DilithiumSignature2028",
      "proofValue": "a7fX...",
      "validUntil": "2036-01-01"
    }
  ]
}
```

Users with older credentials (BJJ-only) can voluntarily re-enroll to obtain dual-signature credentials. High-risk contexts (financial transfers >500M VND, voting) may mandate dual-signature credentials after 2030.

**ZK proof generation impact**: Dilithium3 signatures are large (~2.5 KB) and not yet efficient inside ZK circuits. In Phase 2, the PQ signature is verified **outside the ZK circuit** (by the issuer, not the verifier), while the ZKP itself still uses BJJ for circuit efficiency. This provides PQ protection at the issuance step (harvest-now-decrypt-later risk) while maintaining verifier performance.

---

### Phase 3 (2031+): Full PQ-ZKP Migration

**Goal**: Replace elliptic curve ZKPs with hash-based or lattice-based ZK proofs that are quantum-resistant throughout the entire verification pipeline.

**Technology candidates:**

| System | Approach | Status (2025) |
|---|---|---|
| **zk-STARKs** (StarkWare, Polygon Miden) | Hash-based; transparent setup | Production; proof size 50–200 KB |
| **Lattice-based SNARKs** | Learning With Errors (LWE) | Research; not yet production-ready |
| **STARK + FRI** (RISC Zero) | Hash-based recursive proofs | Production; shrinking proof sizes |

**Transition trigger**: Begin Phase 3 migration when STARK proof sizes reach <10 KB for the ZK-KYC circuit (expected 2028–2031 based on current research trajectory — STARK proof sizes have halved every 18 months since 2020).

**Migration process:**
1. Deploy new `ZKKYCVerifier_v3` contract supporting STARKs on all L1 chains.
2. New credentials issued with STARK-compatible circuit format.
3. Old credentials (BJJ/PLONK) remain verifiable until their expiration date (max 2 years from issuance).
4. After all BJJ credentials have expired, the `ZKKYCVerifier_v1` contract is deprecated.

No credential re-issuance ceremony is needed — the **natural expiry cycle of 2-year credentials** handles the transition window.

---

## 4. Poseidon Hash: Post-Quantum Status

The Poseidon hash function used for Merkle trees and nullifiers has a distinct security profile from EC-based components:

- Poseidon's security is based on the hardness of solving systems of polynomial equations over prime fields — no known quantum algorithm provides exponential speedup over Grover's (which only provides quadratic speedup).
- With 256-bit inputs and outputs, Grover's algorithm reduces effective security to 128 bits — equivalent to AES-128, which is considered acceptable for most threat models through 2050 under current projections.
- Poseidon can be upgraded to Poseidon2 (2023 update with improved security analysis and ~40% lower constraint count) without breaking existing Merkle proofs.

**Recommendation**: Poseidon (and Poseidon2) **requires no migration** for quantum resilience. The primary migration concern is the elliptic curve signature and commitment components.

---

## 5. Governance of the Migration

The L0 on-chain governance mechanism (Section: L0 Consensus) is used to coordinate the migration:

```
Timeline governance actions:

2026: GovernanceVote("ADOPT_CRYPTO_VERSIONING_V1")
      → Activates versioned credential schemas and verifier dispatching

2028: GovernanceVote("MANDATE_HYBRID_SIGNATURES_HIGH_RISK")
      → Requires dual BJJ+Dilithium3 for Tier 1 credentials

2030: GovernanceVote("MANDATE_HYBRID_SIGNATURES_ALL")
      → All new credentials must include Dilithium3 signature

2031+: GovernanceVote("ACTIVATE_PQ_ZKP_VERIFIER_V3")  [conditional on STARK size milestone]
       → Activates STARK-based verifier contracts

2033+: GovernanceVote("DEPRECATE_BJJ_VERIFIER_V1")
       → Final deprecation after all V1 credentials expire
```

Each governance vote requires 2/3 supermajority of L0 validators, ensuring no single party can force an unilateral migration.

---

## References

- NIST. (2024). *Post-Quantum Cryptography: FIPS 203, 204, 205*. https://csrc.nist.gov/pqcrypto
- NSA. (2022). *Commercial National Security Algorithm Suite 2.0*. NSA Cybersecurity Advisory.
- Bernstein, D. J., & Lange, T. (2017). Post-quantum cryptography. *Nature*, 549(7671), 188–194.
- Lê Toàn. (2024). Bảo mật hậu lượng tử. *Tạp chí Thông tin và Truyền thông*, số 4/2024.
- StarkWare Industries. (2023). *STARK proof size roadmap*. https://starkware.co
- RISC Zero. (2024). *Succinct STARK proofs: Current benchmarks*. https://risc0.com
- Polygon Miden. (2024). *Miden VM: Zero-knowledge virtual machine*. https://polygon.technology/miden
