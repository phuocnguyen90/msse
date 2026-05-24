# Circuit Complexity, Proof Size, and Verification Cost Analysis

## Overview

A technically rigorous treatment of ZK-KYC requires a quantitative analysis of the proving circuit's computational complexity. This document specifies the circuit constraint budget, proof size for each proving system, verification gas costs, and the resulting impact on end-to-end system performance. These metrics directly respond to reviewer questions about practical feasibility at national scale.

---

## 1. Circuit Constraint Budget

A ZK circuit is composed of **arithmetic constraints** over a prime field. The number of constraints determines:
- **Proof generation time** (proportional to O(N log N) for PLONK FFTs)
- **Proving key size** (proportional to N)
- **Verification time** (constant for SNARKs — independent of N)

The ZK-KYC circuit is decomposed into sub-circuits with individual constraint budgets:

| Sub-Circuit | Description | Estimated Constraints (PLONK) |
|---|---|---|
| **Identity commitment** | `id_commitment = Poseidon(identity_secret, attributes_hash)` | ~500 |
| **Merkle inclusion proof** | Merkle path verification, depth=27 | ~5,400 (200/level × 27) |
| **Attribute predicate** | Range proof: `birthday.year ≤ 2007` (age ≥ 18) | ~2,000 |
| **Nullifier derivation** | `nullifier = Poseidon(identity_secret, context_id)` | ~500 |
| **Revocation non-membership** | Sparse Merkle non-membership, depth=256 | ~25,600 (100/level × 256) |
| **Issuer signature verification** | BJJ signature check on ZKC | ~2,500 |
| **Context binding** | Public input consistency checks | ~200 |
| **Total (Full KYC Tier 1)** | | **~36,700 constraints** |

**Note**: The revocation non-membership proof dominates the constraint budget due to the deep sparse Merkle tree. An optimization is to use a **batched non-membership proof** with a shallower SMT (depth=40 supports 1 trillion revocations, ~4,000 constraints) at the cost of a larger on-chain revocation state.

### Lightweight Tier Constraint Budgets

```
Tier 2 (re-authentication, no attribute claims):
  Identity commitment + Merkle inclusion + Nullifier = ~6,400 constraints

Tier 3 (age gate only, pre-issued session token):
  Single predicate over cached inclusion proof = ~1,000 constraints
```

---

## 2. Proof Size by Proving System

Proof size affects wallet storage, network transmission, and on-chain calldata costs:

| Proving System | Proof Size | Notes |
|---|---|---|
| **Groth16** | ~192 bytes | Fixed size; smallest possible |
| **PLONK (standard)** | ~736 bytes | 23 × 32-byte field elements |
| **UltraPLONK** | ~800–1,200 bytes | Larger due to lookup arguments |
| **Marlin** | ~896 bytes | |
| **zk-STARK (FRI)** | ~50–200 KB | Hash-based; post-quantum safe |
| **Nova (folding scheme)** | ~1 KB + accumulator | Good for recursive proofs |

**Recommended**: UltraPLONK at ~1 KB. This is:
- Small enough for QR code encoding (max ~3 KB for QR v40)
- Negligible in a wallet credential store
- On-chain calldata cost: ~1,000 bytes × 16 gas/byte = **16,000 gas** (≈$0.001 at current ETH prices, far less on an L2/L1)

For comparison, an HTTPS session handshake transmits ~5–10 KB of certificate data, making the ZK proof considerably more compact than today's PKI overhead.

---

## 3. Verification Cost Analysis

### 3.1 On-Chain Verification (L1 Smart Contract)

ZK proof verification on-chain is a fixed-cost operation regardless of the circuit size — this is the defining advantage of SNARKs over STARKs.

| Operation | Gas Cost (EVM) | USD Equivalent (at 10 gwei, ETH=$3,000) |
|---|---|---|
| **PLONK verification** | ~300,000 gas | ~$0.009 |
| **Groth16 verification** | ~200,000 gas | ~$0.006 |
| **Nullifier set write** | ~20,000 gas | ~$0.0006 |
| **Merkle root lookup** | ~2,100 gas (SLOAD) | ~$0.00006 |
| **Total per verification** | ~322,000 gas | **~$0.01** |

At Vietnamese L1 chain parameters (no open market gas pricing; flat fee model):
- Assuming gas equivalent to 10,000 VND per verification (≈$0.40)
- For 7.5M verifications/day: **75,000,000,000 VND/day** (~$3M/day) — clearly unsustainable for all verifications to be on-chain.

**Solution**: **Off-chain verification with on-chain nullifier registration only**:
- Verifier node checks the ZK proof off-chain (< 5ms, free).
- Only the nullifier (32 bytes) is written on-chain.
- On-chain cost per verification: ~20,000 gas for SSTORE = ~$0.0006.
- For 7.5M verifications/day: **150,000,000 gas/day** ≈ 10 blocks on a high-throughput L1 chain. Fully feasible.

**Hybrid model** (recommended):
- High-stakes verifications (banking, voting): Full on-chain ZK proof verification (~$0.01/verification, acceptable for critical use cases).
- Routine verifications (app logins, age gates): Off-chain verification + on-chain nullifier only (~$0.0006/verification).

### 3.2 Off-Chain Verification Performance

Off-chain PLONK verification runs on standard server hardware:

| Hardware | Verification Time | Throughput |
|---|---|---|
| Intel Xeon (single core) | ~5 ms | 200 TPS/core |
| 8-core server | ~0.6 ms | 1,600 TPS |
| GPU-accelerated | ~0.1 ms | 10,000 TPS |

A single verification server handles well above the estimated 90-peak-TPS national demand. Horizontal scaling via load balancing is trivial and follows standard web service patterns.

---

## 4. Proof Generation Time (Client-Side)

The dominating user experience factor is how long it takes to generate a proof on-device.

### 4.1 Complexity Analysis

For PLONK with N constraints, proof generation requires:
```
Main operations:
  FFT (forward):  O(N log N)  — domain size = 2^ceil(log2(N))
  MSM (multi-scalar multiplication):  O(N)  — the bottleneck

For N = 36,700 constraints:
  Effective domain size: 2^16 = 65,536
  FFT operations: ~65,536 × 16 = ~1M field multiplications
  MSM: ~65,536 EC point additions over BN254
```

Modern BN254 MSM benchmarks on mobile hardware:
- **Apple A17 Pro** (iPhone 15 Pro): ~65K point MSM in ~150ms → Full proof ~300ms
- **Snapdragon 8 Gen 2** (flagship Android): ~65K MSM in ~200ms → Full proof ~400ms
- **Snapdragon 695** (mid-range): ~65K MSM in ~800ms → Full proof ~1.5s
- **Helio G85** (entry-level): ~65K MSM in ~3s → Full proof ~6s

**For Tier 1 (36,700 constraints)**, the effective range is **0.3–6 seconds** depending on device tier.

**For Tier 3 (1,000 constraints)**:
- 2^10 = 1,024 domain size
- MSM: ~1,024 point additions
- All devices: **< 50ms** — imperceptible to users.

### 4.2 Optimization Techniques

| Technique | Speedup | Implementation Effort |
|---|---|---|
| **RapidSNARK** (native C++ prover) | 3–5× vs. snarkjs WASM | Medium (build pipeline) |
| **GPU acceleration** (mobile GPU) | 2–4× on devices with GPU compute | High (OpenCL/Metal shaders) |
| **Circuit optimization** (removing redundant constraints) | 20–40% reduction | Medium (circuit redesign) |
| **Poseidon2** (vs. Poseidon) | ~40% fewer hash constraints | Low (drop-in replacement) |
| **Reduced revocation SMT depth** | Up to 70% constraint reduction | Medium (depth 40 vs 256) |

Combining RapidSNARK + Poseidon2 + reduced SMT depth reduces Tier 1 constraints to ~15,000–20,000 and proving time to **0.3–3 seconds** across the full device range.

---

## 5. Proving Key and Verification Key Size

| Artifact | Size (PLONK, N=65,536) | Distribution Method |
|---|---|---|
| **Proving key** | ~50–100 MB | Downloaded once at wallet installation; cached locally |
| **Verification key** | ~1–2 KB | Embedded in verifier smart contract bytecode |
| **Universal SRS** (shared) | ~500 MB | Stored by wallet; downloaded once, used by all circuits |

The 50–100 MB proving key download is a one-time cost at wallet installation (similar to a standard mobile app update). Over a 4G connection at 10 Mbps, this takes ~40–80 seconds. Subsequent proof generations use the cached key.

**Optimization**: Delta updates to the proving key when the circuit is updated (rather than full re-download) reduce ongoing maintenance bandwidth.

---

## 6. Summary: Complexity at a Glance

```
┌─────────────────────────────────────────────────────────────────┐
│                  ZK-KYC Complexity Summary                      │
├──────────────────────┬──────────────────────────────────────────┤
│ Circuit constraints  │ ~37K (Tier 1) / ~6K (T2) / ~1K (T3)     │
│ Proof size           │ ~1 KB (UltraPLONK)                       │
│ Proving time (mid)   │ 1–3 seconds (Tier 1)                     │
│ Proving time (T3)    │ < 50 ms                                  │
│ On-chain verify cost │ ~300K gas (~$0.01)                       │
│ Off-chain verify     │ ~5 ms per proof                          │
│ L0 TPS required      │ < 20 TPS (batch anchoring only)          │
│ L1 TPS capacity      │ 200–10,000 TPS (off-chain verify model)  │
│ Proving key size     │ ~50–100 MB (one-time download)           │
│ Verification key     │ ~1–2 KB (embedded in contract)           │
└──────────────────────┴──────────────────────────────────────────┘
```

---

## References

- Gabizon, A., Williamson, Z. J., & Ciobotaru, O. (2019). PLONK. *IACR ePrint 2019/953*.
- Polygon ID team. (2023). *Circuit benchmarks — credentialAtomicQuerySig*. https://docs.polygonid.xyz
- Grassi, L., et al. (2023). Poseidon2: A faster version of the Poseidon hash function. *IACR ePrint 2023/323*.
- iden3. (2022). *Benchmarks: Circom circuits on mobile devices*. https://github.com/iden3/snarkjs
- Bünz, B., et al. (2020). Proof-carrying data and hearsay arguments from signature cards. *ITCS 2020*.
- Matter Labs. (2023). *Boojum: High-performance PLONK prover*. https://github.com/matter-labs/era-boojum
