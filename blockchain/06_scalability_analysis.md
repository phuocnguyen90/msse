# Scalability Analysis: TPS, Proof Generation, and Benchmark Estimates

## Overview

Claims of national-scale viability require quantitative support. This document provides throughput analysis, latency benchmarks, and capacity estimates for the proposed ZK-KYC architecture across its three computational layers: client-side proof generation, L1 verification, and L0 Merkle root anchoring.

---

## 1. National-Scale Transaction Volume Estimates

To size the system, we first estimate the realistic load from Vietnam's digital economy:

| Use Case | Current Daily Volume (Estimate) | Peak TPS |
|---|---|---|
| Banking KYC onboarding (new accounts) | ~50,000/day | 1–2 TPS |
| E-KYC for financial transactions (AML checks) | ~5,000,000/day | 58 TPS |
| E-government service access | ~500,000/day | 6 TPS |
| E-commerce age/identity verification | ~2,000,000/day | 23 TPS |
| **Total estimated peak** | **~7.5M verifications/day** | **~90 TPS** |

*Sources: State Bank of Vietnam annual report 2023; VNeID deployment statistics (VCDC, 2025).*

These figures are **distributed across L1 chains**, not concentrated on L0. Each L1 handles its own verification traffic. L0 only processes batch Merkle root anchors — not individual verifications.

---

## 2. L0 Throughput Requirement

L0 receives one `AnchorMerkleRoot` transaction per L1 chain per anchoring interval. With an estimated 100 registered L1 chains anchoring every 10 minutes:

```
L0 TPS = 100 L1 chains × 1 anchor / 600 seconds = 0.17 TPS
```

Even in a highly scaled future scenario with 1,000 L1 chains anchoring every minute:
```
L0 TPS = 1,000 / 60 = 16.7 TPS
```

**L0 throughput requirement is trivially low** (~1–20 TPS). Any modern BFT consensus system (including Tendermint, which handles 1,000+ TPS) is orders of magnitude above this requirement. L0 is never a bottleneck.

---

## 3. L1 Verification Throughput

Each L1 verifier contract processes individual ZK proof verifications. The bottleneck here is the on-chain proof verification cost.

### 3.1 On-Chain Verification Cost (PLONK/UltraPLONK)

| Operation | Gas Cost (EVM-equivalent) | Time at 15M gas/block |
|---|---|---|
| PLONK proof verification | ~200,000–400,000 gas | 38–75 verifications/block |
| Groth16 verification | ~200,000 gas | 75 verifications/block |
| Nullifier set write | ~20,000 gas | negligible |

For a 2-second block time on a modern L1 (similar to Polygon PoS):
```
Throughput = 75 verifications/block × 0.5 blocks/second = 37.5 TPS per L1
```

A banking L1 handling 58 peak TPS would need **2 parallel verifier contract instances** or a block gas limit increase — both routine scaling techniques.

**Alternative**: Off-chain verification with on-chain nullifier commitment. The verifier node checks the ZK proof off-chain and only posts the nullifier to the chain. This reduces on-chain cost to ~20,000 gas per verification, supporting **750+ TPS per L1** at the same block parameters.

---

## 4. Client-Side Proof Generation Benchmarks

The most critical UX metric is how long it takes a user's mobile device to generate a ZK proof. This determines whether the system is practically usable.

### 4.1 Published Benchmarks (Groth16 + Poseidon, similar circuit complexity)

| Device Category | Proving Time | Reference |
|---|---|---|
| Flagship (iPhone 15 Pro, Snapdragon 8 Gen 3) | 0.8–1.5 seconds | Polygon ID SDK benchmarks (2023) |
| Mid-range (Snapdragon 695, Exynos 1280) | 2–4 seconds | Semaphore mobile benchmarks |
| Entry-level (Snapdragon 480, Helio G85) | 5–10 seconds | snarkjs WASM benchmarks |
| Google Wallet MDL verification | < 2 seconds | Stapelberg (2025) |

### 4.2 Vietnam Device Distribution Context

Based on 2024 Vietnam smartphone market data (IDC Vietnam):
- Flagship (>$500): ~8% of active devices
- Mid-range ($150–500): ~45% of active devices
- Entry-level (<$150): ~47% of active devices

**Conservative estimate**: ~47% of users on entry-level devices would experience 5–10 second proof generation times. This is acceptable for high-stakes, low-frequency KYC events (bank account opening) but unacceptable for frequent micro-verifications (every app login).

### 4.3 Mitigation: Tiered Proof Complexity

Different contexts require different circuit complexity:

```
Tier 1 — Full KYC proof (onboarding):
  Circuit: identity membership + attribute claims + non-revocation
  Constraints: ~50,000
  Proving time: 2–10 seconds (acceptable for once-per-relationship)

Tier 2 — Lightweight verification (re-authentication):
  Circuit: nullifier derivation + recent root membership only
  Constraints: ~5,000
  Proving time: 0.2–1 second (acceptable for frequent use)

Tier 3 — Minimal claim (age gate):
  Circuit: single attribute predicate only
  Constraints: ~1,000
  Proving time: < 0.1 second (real-time UX)
```

Applications select the minimum tier required for their risk level.

### 4.4 Delegated Proving for Low-End Devices

For entry-level devices where even Tier 1 proving time is unacceptable, a **privacy-preserving delegated proving** option is available:

1. User generates a blinded version of their witness using a one-time random blinding factor.
2. Blinded witness is sent to a trusted proving server (operated by the KYC issuer or a neutral party).
3. Proving server generates the proof without learning the user's identity (by design of the blinding).
4. Proof is returned to the user's device for submission.

This is analogous to blind signatures in e-cash systems and preserves zero-knowledge properties while offloading computation. The user must trust the proving server not to log the blinded witness, which is mitigated by using multiple servers with secret-sharing (threshold proving).

---

## 5. Merkle Tree Update Throughput

The identity Merkle tree on each L1 must handle new user registrations:

| Metric | Value |
|---|---|
| New KYC registrations/day (Vietnam, 2025) | ~50,000 |
| Merkle tree insertions/second (peak) | ~2–3 |
| Poseidon Merkle update time (depth=26, 67M leaves) | ~5 ms per insertion |
| Batch insertion (1,000 at once) | ~200 ms |
| Root recomputation after batch | O(depth) = 26 hash operations |

A daily batch insert of 50,000 new identities takes approximately:
```
50,000 / 1,000 (batch size) × 200ms = 10 seconds
```
Negligible. Incremental updates throughout the day add at most 3 TPS to the L1 database.

---

## 6. End-to-End Latency Estimates

| Step | Latency |
|---|---|
| Fetch latest L0 anchor | 50–200 ms (API call) |
| Generate ZK proof (mid-range device, Tier 1) | 2–4 seconds |
| Submit proof to L1 verifier | 100–500 ms |
| L1 block confirmation | 2–5 seconds |
| **Total end-to-end (typical)** | **5–10 seconds** |
| **Total end-to-end (Tier 3, flagship device)** | **< 1 second** |

For comparison, a traditional centralized KYC API call (e.g., VNeID OCSP-style check) takes 200–800 ms in ideal conditions but suffers from server-side queuing under load, potentially degrading to 5–30 seconds at peak traffic — comparable to or worse than the ZK approach.

---

## 7. Storage Requirements

| Component | Storage per User | 67M Users (Vietnam) |
|---|---|---|
| Identity commitment (bytes32) | 32 bytes | 2.1 GB |
| Merkle path (depth 26) | ~832 bytes | 55 GB |
| Revocation SMT leaf | 32 bytes | 2.1 GB |
| ZKC (user wallet) | ~500 bytes | N/A (on-device) |
| **L1 total state** | **~64 bytes on-chain** | **~4.3 GB** |

The L1 on-chain state is dominated by the Merkle tree leaves and is well within the capacity of any modern blockchain database. Merkle paths are stored off-chain by users in their wallets.

---

## References

- Polygon ID team. (2023). *Polygon ID SDK: Mobile benchmarks*. https://docs.polygonid.xyz
- Semaphore contributors. (2023). *Semaphore: Performance analysis*. https://semaphore.appliedzkp.org
- Stapelberg, A. (2025). It's now easier to prove age and identity with Google Wallet. *Google Blog*.
- IDC Vietnam. (2024). *Vietnam Smartphone Market Report Q4 2024*.
- State Bank of Vietnam. (2023). *Annual Report on Digital Banking Statistics*.
