# Social Recovery: Key Management for Mass Adoption

## Overview

Self-sovereign identity (SSI) is predicated on users controlling their own cryptographic keys. However, this creates a fundamental usability problem: if a user loses their device or forgets their PIN, they permanently lose access to their digital identity — an unacceptable outcome for a national identity system. This document specifies the key management architecture and social recovery mechanism that resolves this tension without re-centralizing trust.

---

## 1. The Key Management Trilemma

Identity key management for mass adoption faces three conflicting goals:

```
         Usability
            ▲
           /|\
          / | \
         /  |  \
        /   |   \
       ─────────────
  Security   Decentralization
```

- **Usability alone** → Cloud backup with a central provider (Apple iCloud, Google Drive). Simple but centralizes trust and creates a surveillance vector.
- **Security alone** → Hardware security modules and complex seed phrase management. Appropriate for experts; inaccessible to the general population.
- **Decentralization alone** → Pure on-chain self-custody. Maximal sovereignty but maximum risk of permanent loss.

The proposed architecture occupies the *center* of this triangle: biometric-protected device-local keys for daily use, with a distributed social recovery mechanism as a fallback.

---

## 2. Key Hierarchy

The ZK-KYC wallet uses a hierarchical key structure to separate concerns:

```
Root Secret (identity_secret)
    │
    ├── Identity Key (identity_commitment seed)
    │       Used to generate Poseidon commitments for Merkle inclusion
    │       Derived: identity_key = HKDF(identity_secret, "identity")
    │
    ├── Signing Key (BJJ key pair)
    │       Used to authenticate with issuers and sign presentation requests
    │       Derived: signing_key = HKDF(identity_secret, "signing")
    │
    └── Recovery Shares (Shamir Secret Shares of identity_secret)
            Distributed to guardian devices during setup
            Threshold: t-of-n (e.g., 2-of-3 or 3-of-5)
```

The `identity_secret` is generated once during ZKC issuance and never leaves the secure enclave of the user's device in plaintext.

---

## 3. Day-to-Day Authentication: Passkeys and Biometrics

For routine ZK proof generation (verifying age, logging into a service), the user experience must be as simple as Face ID or fingerprint unlock.

**Technical implementation:**

1. The `identity_secret` is stored in the device's **Secure Enclave** (iOS) or **StrongBox KeyStore** (Android), protected by a device-bound biometric key.
2. When generating a ZK proof, the wallet:
   - Requests biometric authentication via the OS API.
   - Upon success, the OS releases the identity_secret from the enclave.
   - The ZKP circuit runs with identity_secret as witness input.
   - identity_secret is zeroized from RAM immediately after proof generation.

```
User taps "Verify Age"
  → Face ID / fingerprint prompt
  → OS Secure Enclave releases identity_secret
  → ZKP circuit: prove(identity_secret, attributes, merkle_path)
  → identity_secret zeroized
  → Proof submitted to verifier
  → "Age verified ✓" shown to user
```

**Key properties:**
- `identity_secret` never leaves the device's secure hardware.
- No password or PIN required for normal use — biometric only.
- Compatible with **FIDO2/WebAuthn passkeys**, enabling web-based ZKC verification flows.
- Aligned with Apple's CryptoKit and Android's BiometricPrompt standards — no custom hardware required.

---

## 4. Social Recovery: Mechanism Specification

Social recovery (Vitalik Buterin, 2021; Gnosis Safe multisig) allows a user to designate a set of **guardians** who can collectively authorize recovery of the `identity_secret` after device loss — without any single guardian knowing the full secret.

### 4.1 Setup Phase (During Initial ZKC Issuance)

```
User selects n guardians (recommended: 3–5)
  → Can be: family members, trusted friends, employer IT dept
  → Each guardian must have their own ZK-KYC wallet (to prevent impersonation)

Wallet generates Shamir Secret Shares:
  shares = SSS.split(identity_secret, threshold=t, n=n)
  (e.g., t=3, n=5: any 3 of 5 guardians can recover)

Each share is:
  1. Encrypted with guardian's public key: enc_share_i = Encrypt(share_i, guardian_pubkey_i)
  2. Stored on guardian's device (not on any server)
  3. Guardian receives a push notification to accept the role

Recovery proof anchor:
  recovery_commitment = Poseidon(identity_commitment, guardian_pubkeys_hash)
  Published to L1 as part of the user's ZKC metadata (not revealing guardian identities)
```

### 4.2 Recovery Phase (After Device Loss)

```
User reports device loss through new device or government KYC office
  → New device generates new ephemeral key pair: (temp_pubkey, temp_privkey)
  → User contacts t-of-n guardians (via phone, in person, or app notification)

Each contacted guardian:
  1. Verifies the recovery request is from the real user (biometric + ZK proof from their own wallet)
  2. Decrypts their share: share_i = Decrypt(enc_share_i, guardian_privkey_i)
  3. Re-encrypts share for new device: re_enc_share_i = Encrypt(share_i, temp_pubkey)
  4. Submits re_enc_share_i to a distributed relay (or directly to user via secure channel)

User reconstructs identity_secret:
  identity_secret = SSS.reconstruct([re_enc_share_1, re_enc_share_2, re_enc_share_3])

User re-registers new device with same identity_commitment:
  → L1 re-issuance: new ZKC with same identity_commitment, new device key
  → Old nullifiers remain valid (no new nullifiers generated yet)
  → Old device's keys are revoked via credential version update
```

**Critical**: Guardians never learn `identity_secret`. They only hold encrypted shares and re-encrypt them for the new device. A guardian colluding with others cannot reconstruct the secret without t simultaneous colluding guardians — and the user is notified of each guardian contact event.

### 4.3 Security Parameters

| Parameter | Recommended Value | Rationale |
|---|---|---|
| Total guardians (n) | 3 or 5 | 3 for simplicity; 5 for higher resilience |
| Recovery threshold (t) | 2/3 or 3/5 | Balance between usability and security |
| Recovery time window | 72 hours | Prevents real-time social engineering; long enough for deliberate recovery |
| Guardian authentication | ZK-KYC wallet biometric | Prevents impersonation by a non-ZKC holder |
| Min. guardian delay | 24 hours per guardian | Prevents rapid coordinated attack |
| Recovery attempt limit | 3 per 30 days | Rate limiting against brute-force social engineering |

---

## 5. Distinguishing Device Loss vs. Device Compromise

The paper's original draft conflates two distinct scenarios requiring different responses:

| Scenario | Description | Required Action |
|---|---|---|
| **Device loss** (most common) | User loses physical access to device; attacker may have it | **Recovery** (regain access) + **Revocation** (invalidate old device key) |
| **Device compromise** (rarer) | Attacker has device and can bypass biometrics (unlikely with Secure Enclave) | **Revocation** only (device key and all active ZKCs are invalidated) |
| **Identity theft** | Attacker has obtained a fraudulent ZKC through KYC fraud | **Issuer revocation** (separate process via KYC authority, not wallet recovery) |

### Device Loss + Recovery Flow
1. User initiates social recovery (as above).
2. After successful reconstruction, user immediately submits a **device key rotation** transaction on L1 (signed with the new device key + recovery proof).
3. Old device's public key is marked as rotated on L1.
4. Any proofs generated from the old device key after this point are rejected.

### Device Compromise Flow (no recovery needed)
1. User authenticates to the KYC issuer's web portal using government-issued CCCD (physical card, NFC).
2. Issuer invalidates the credential linked to the compromised device.
3. User obtains a new ZKC through standard re-enrollment (in-person or online KYC).
4. No guardian involvement needed — the physical CCCD is the ultimate recovery root of trust.

---

## 6. Institutional Custody Option

For elderly users, users with cognitive disabilities, or users who prefer not to manage guardians, an **institutional custody option** is provided:

- The user designates a trusted institution (their bank, a post office, a government office) as sole guardian.
- The institution stores the encrypted share in its HSM system.
- Recovery requires in-person identity verification (physical CCCD + biometric at the institution counter).

This option sacrifices full self-sovereignty for a user-friendly fallback and is explicitly permitted under the architecture's design. The `recovery_commitment` on L1 records which recovery model was chosen, allowing verifiers to apply appropriate risk weighting (self-sovereign recovery = higher trust; institutional = lower trust for high-stakes transactions).

---

## 7. Comparison with Existing Systems

| System | Recovery Mechanism | Centralization Risk |
|---|---|---|
| **Apple iCloud Keychain** | Cloud backup by Apple | High (Apple is single custodian) |
| **Google Account Recovery** | Google recovery phone/email | High (Google dependency) |
| **Gnosis Safe** | On-chain guardian multisig | Low (guardians hold keys) |
| **Argent Wallet** | Social recovery via guardian wallets | Low (similar to proposed) |
| **VNeID (current)** | Password reset via email/SMS | Medium (depends on telco/email provider) |
| **Proposed ZK-KYC** | Shamir shares + guardian wallets + CCCD fallback | **Low-to-Medium** (tunable) |

---

## References

- Buterin, V. (2021). *Why we need wide adoption of social recovery wallets*. https://vitalik.ca/general/2021/01/11/recovery.html
- Shamir, A. (1979). How to share a secret. *Communications of the ACM*, 22(11), 612–613.
- Apple Inc. (2023). *iOS Security Guide: Secure Enclave*. https://support.apple.com/guide/security
- Google. (2023). *Android Security: StrongBox Keymaster*. https://source.android.com/docs/security/features/keystore
- Loopring. (2021). *Counterfactual wallet with social recovery*. https://blogs.loopring.org
- FIDO Alliance. (2023). *FIDO2 / WebAuthn specification*. https://fidoalliance.org/fido2
