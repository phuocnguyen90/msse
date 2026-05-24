# Paper Framework: Non-Technical Audience + Demonstrated Technical Depth
## Final Framework for English Journal Submission

**Core Tension Resolved:**
The paper must be readable by a policy audience *and* credible to a technical reviewer.
The solution is not to simplify the technical work — it is to **separate the register**.

> The body text makes the argument in plain language.
> Figures, tables, and worked examples carry the technical proof.
> The appendix holds the full specification for those who want to verify.

A non-technical reader finishes the paper understanding the argument.
A technical reviewer finishes the paper convinced the authors did the actual work.

---

## Proposed Title

*Verify Without Collecting: A Deployable Zero-Knowledge KYC Architecture for Vietnam's Personal Data Protection Law*

The word **deployable** is doing critical work: it signals this is not a theoretical proposal.

---

## The Paper's Credibility Signals (What Proves You Did the Work)

Technical depth for a non-technical audience is not shown through dense prose — it is shown through:

1. **A worked transaction trace**: walk one real KYC interaction through the full system, step by step, with actual data structures (shown as a figure, not explained in prose).
2. **A constraint table**: the ZK circuit complexity budget shown as a table. Non-technical readers skip it. Technical reviewers treat it as the litmus test.
3. **A benchmark table**: proof generation times by device tier, on-chain costs per verification. These numbers either hold up or they don't — there is no way to fake them convincingly.
4. **A concrete integration path for NDAChain**: not "NDAChain could become a Layer 1" but "here is the specific API change, the specific transaction type, and the specific governance vote required."
5. **A named open-source foundation**: "this architecture can be prototyped using Polygon ID's issuer node with the following modifications" — this is a falsifiable, verifiable claim that signals real implementation knowledge.

These five elements are distributed across the paper as figures and tables. They are never in the prose narrative. The prose says what the system does; the figures show that it works.

---

## Structural Overview

```
Abstract                                              (~250 words)
1. Introduction                                       (~700 words)
2. The Compliance Problem: Why Existing Systems Fail  (~800 words)
3. Technical Background (Accessible)                  (~700 words)
4. The Proposed ZK-KYC Architecture                  (~1,500 words)
   [Contains: Figure 1, Figure 2, Table 1]
5. Integration Path: From Architecture to Deployment  (~1,200 words)
   [Contains: Figure 3, Table 2, Table 3]
6. Stakeholder Impact Analysis                        (~800 words)
7. Strategic Comparison                               (~900 words)
   [Contains: Table 4]
8. Risk and Limitation Analysis                       (~900 words)
9. Policy Recommendations                             (~600 words)
10. Conclusion                                        (~400 words)
Technical Appendix (A–J)                             (separate section)
```

Total body: ~8,500 words.

---

## Section-by-Section Framework

---

### Abstract (~250 words)

**Structure:** Problem → Gap → Method → Result → Implication.
Written for both audiences simultaneously: non-technical readers get the argument; technical reviewers get the specifics.

**Must include in the abstract:**
- The specific legal trigger (LPDP 2025, Art. 3 data minimization)
- The specific technical approach (ZK-SNARK-based credential architecture with L0/L1 separation)
- One concrete number (e.g., "demonstrated to support Vietnam's estimated 90 peak TPS national verification load at under $0.01 per verification")
- The governance argument (sovereignty + open innovation vs. corporate or monolithic alternatives)
- The NDAChain integration finding

---

### Section 1 — Introduction (~700 words)

**Reader's question:** *Why does this matter, and what did you actually do?*

**Address:**
- Open with the LPDP compliance gap — not with technology.
- State the tension: the two currently debated paths (corporate platforms vs. closed national system) each resolve only half the problem. Frame the paper as resolving the full tension.
- **Bouncer analogy**: one paragraph. This is the conceptual key for non-technical readers. Return to it in Section 3.
- **Explicit contributions** (bulleted, written so both audiences can assess them):
  - A hybrid L0/L1 ZK-KYC architecture specification with a concrete integration path for NDAChain
  - A ZK circuit design for Vietnamese KYC attributes, with constraint budget and mobile benchmark data
  - A revocation mechanism satisfying LPDP Art. 14 (right to erasure) without re-introducing linkability
  - A comparative strategic analysis across three national identity architecture paths
  - Seven sequenced policy recommendations with a 2026–2029+ implementation roadmap

**Tone note:** The contributions list is where the technical reviewer decides whether to read the paper carefully. Every bullet must be specific and falsifiable.

---

### Section 2 — The Compliance Problem: Why Existing Systems Fail (~800 words)

**Reader's question:** *Can't we just improve what we have?*

**Prose style:** Policy brief. No jargon. Three-part structure.

**2.1 How Current KYC Works**
- "Collect-and-protect": every service collects full ID, stores it, retrieves it for verification.
- The filing cabinet analogy: a better lock does not reduce what is in the cabinet.
- Scale: by the time a Vietnamese citizen has a bank account, a SIM card, and an insurance policy, their personal data exists in at least three separate databases, each independently vulnerable.

**2.2 Three Structural Conflicts with LPDP**
Present as a table — this is the first technical credibility signal for the legal-technical reviewers at the target venues (Government Information Quarterly, CLSR).

| LPDP Requirement | Article | Current System Behavior | Why It Cannot Be Patched |
|---|---|---|---|
| Data minimization | Art. 3 | Collects full PII for every interaction | Architecture requires full data to function; selective collection breaks existing flows |
| Non-linkability | Art. 4, 12 | Single national ID links all interactions | Identifier is designed for correlation; removing it breaks system identity |
| Right to erasure | Art. 14 | Data held across N independent databases | Cascading deletion across systems is operationally infeasible at scale |
| Accountability | Art. 37 | Audit requires accessing all downstream systems | No single authoritative compliance record exists |

**2.3 The VNeID Case**
- VNeID represents the current best-in-class government response: a unified digital ID with NFC chip verification.
- Specific limitation: VNeID verification discloses the full chip contents (name, DOB, address, ID number, biometric hash) to the verifier — the definition of a data minimization failure.
- Not a criticism of the implementation. A criticism of the architecture it was built on.

---

### Section 3 — Technical Background (Accessible) (~700 words)

**Reader's question:** *What is this technology, and how do I know it works?*

**This is the only section that explains technology. Keep it to one concept: proof without disclosure. Everything else is context.**

**3.1 The Core Concept**
- The bouncer analogy revisited and extended.
- One additional analogy for the "mathematical proof" aspect:
  > A university can issue a sealed letter confirming a graduate's degree without revealing their grades, thesis topic, or attendance record. The sealed letter is not a summary — it is a cryptographically signed statement that the claim is true. The university does not track who the graduate shows it to.
- Name the technology: zero-knowledge proof. One sentence of definition. Move on.

**3.2 Proof That It Scales: Existing Deployments**
This subsection is the most important for non-technical readers skeptical of "new technology." Present as a short table:

| Deployment | Organization | Scale | What It Verifies |
|---|---|---|---|
| Google Wallet Age Verification | Google | Hundreds of millions of devices | Age ≥ 18 without revealing date of birth |
| World ID | Worldcoin | 6M+ verified users | Unique human identity without biometric storage |
| Polygon ID | Polygon | 10M+ credentials issued | Custom attribute claims for DeFi compliance |
| EU EUDI Wallet | European Commission | Regulatory pilot, 27 countries | National ID + professional credentials |

**Point of the table:** The question is not whether this works. It works. The question is who governs the infrastructure it runs on.

**3.3 The Governance Gap These Deployments Leave**
- Google Wallet: works for age verification; does not address national sovereignty.
- World ID: addresses Sybil resistance; not designed for regulatory KYC compliance.
- Polygon ID: closest to a general-purpose ZK-KYC system; designed for open blockchain environments, not national infrastructure governance.

**This paper's contribution is the governance architecture for a national deployment, built on these proven components.**

---

### Section 4 — The Proposed ZK-KYC Architecture (~1,500 words)

**Reader's question:** *What exactly are you proposing?*

**Prose:** Plain language throughout.
**Figures:** Two figures carry the technical depth. Prose references them but does not explain them.

**4.1 Design Principles**
Four principles stated as plain-language requirements:
1. Verification must require no personal data transfer — only a verified answer.
2. The same identity must be unrecognizable across different services.
3. No single organization — including the government — should be able to unilaterally alter or suppress identity records.
4. The system must be upgradeable without re-issuing all existing credentials.

**4.2 The Two-Layer Structure**
- Road / buildings analogy (from non-technical framework).
- **Public Trust Layer (Layer 0)**: stores only cryptographic fingerprints — mathematical summaries that prove a record exists without revealing its content. Governed by a defined set of validators including government ministries and independent participants. No single entity controls it.
- **Application Layer (Layer 1)**: where actual services operate. NDAChain is the primary government-authorized Layer 1. Banks, fintech companies, and hospitals operate their own Layer 1 systems. Each anchors its identity records to the public layer.

**[FIGURE 1: System Architecture Diagram]**
*Three-tier diagram: Citizen Wallet → Layer 1 (multiple: NDAChain, Bank L1, Health L1) → Layer 0 (Public Trust Layer). Arrows labeled with action names in plain language: "presents proof," "confirms credential is valid," "anchors identity record." No mathematics. One call-out box per layer describing its role in one sentence.*

**4.3 The Credential Lifecycle**
Walk through as a narrative with a named character (Minh, a Vietnamese citizen opening a bank account). Four stages:
1. **Issuance (one-time)**: Minh visits a government office (or uses the VNeID app) for initial registration. The system generates a privacy-preserving credential — a sealed mathematical envelope — that Minh's phone holds. No personal data leaves the government system. The credential is stored only on Minh's phone.
2. **Service verification**: When Minh opens a bank account, his phone generates a fresh proof — not a copy of the credential, but a one-time answer to the bank's specific question. The bank receives the answer. It does not receive the credential.
3. **Cross-service unlinkability**: When Minh later checks into a hotel, the hotel receives a different one-time answer. Even if the bank and hotel compare notes, they cannot determine the answers came from the same person.
4. **Revocation**: If Minh loses his phone, he reports it. The credential is cancelled within minutes — the next time any organization checks, the answer comes back invalid. Minh re-enrolls with a new device.

**[FIGURE 2: Credential Lifecycle Sequence Diagram]**
*Four-column sequence diagram: Citizen / KYC Issuer / Layer 1 Verifier / Layer 0. Rows: Issuance, Verification, Cross-service check, Revocation. Each interaction labeled in plain English. Technical details (transaction type, root hash) shown in a footnote below the figure, not in the prose.*

**4.4 What Layer 0 Actually Stores**
This is the key technical point that must survive the prose:
- Layer 0 does not store names, ID numbers, or any personal data.
- It stores a mathematical fingerprint (Merkle root) of the identity registry at a point in time — a number that allows anyone to verify that a given credential was valid at that moment, without revealing whose credential it was.
- A regulator querying Layer 0 learns: "Organization X had 1,000,000 verified customers on this date." They do not learn who those customers are.

**[TABLE 1: What Is and Is Not Stored at Each Layer]**

| Data Element | On Citizen's Phone | On Layer 1 (e.g., Bank) | On Layer 0 (Public) |
|---|---|---|---|
| Full name | Encrypted in credential | ✗ Never received | ✗ Never stored |
| Date of birth | Encrypted in credential | ✗ Never received | ✗ Never stored |
| CCCD number | Encrypted in credential | ✗ Never received | ✗ Never stored |
| "Customer is verified" | Generated as proof | ✓ Result logged | ✗ |
| Compliance attestation | ✗ | Hash only | ✓ Anchored |
| Credential validity | ✓ | Checked via Layer 0 | ✓ Root hash only |

*This table is the single most important thing for legal and policy reviewers to see. It is what LPDP compliance looks like technically.*

---

### Section 5 — Integration Path: From Architecture to Deployment (~1,200 words)

**Reader's question:** *Is this actually buildable, or is it a thought experiment?*

**This section is the primary technical credibility signal. It answers: "We didn't theorize this — we mapped the actual integration."**

**Prose:** Accessible but specific. The tables carry the technical load.

**5.1 Foundation: What Already Exists**
- The proposed architecture does not require inventing new technology.
- Polygon ID (open-source, Apache 2.0) provides: a credential issuance node, a ZK proof circuit, a mobile wallet SDK, and verifier contracts — all production-tested at 10M+ credential scale.
- Semaphore (open-source, MIT) provides: the group membership and nullifier mechanism.
- W3C Verifiable Credential standard provides: the credential format and metadata schema.
- The proposed contribution: a governance layer and NDAChain integration path that ties these components into a nationally deployable system.

Estimated open-source code reuse: approximately 70% of implementation effort. This is not a claim about ease — it is a claim about risk reduction.

**5.2 The NDAChain Integration Path**
This is the most politically significant section for Vietnamese policymakers.

**Plain language statement**: NDAChain does not need to be rebuilt. It needs to be repositioned.

Specific changes required (presented as a table — this is where the technical depth lives):

**[TABLE 2: NDAChain Integration Requirements]**

| Component | Current NDAChain | Required Change | Effort Estimate |
|---|---|---|---|
| Identity record format | Internal consortium format | Add W3C VC wrapper with BJJ signature | Medium — schema change, no chain change |
| Identity state publication | Internal to consortium | Add `AnchorMerkleRoot` transaction to public L0 | Medium — new transaction type |
| Credential issuance | Not yet implemented | Deploy Polygon ID issuer node, adapted to NDAChain | High — new component |
| Verifier contracts | Not yet implemented | Deploy ZK proof verifier + nullifier registry | Medium — audited open-source base |
| Revocation mechanism | Not yet implemented | Deploy Sparse Merkle Tree revocation registry | Medium — iden3 library available |
| Governance | Consortium vote | Add L0 registration process + DID method spec | Low — governance decision |
| Wallet app | VNeID app | Add ZKC storage + proof generation module | High — new user-facing feature |

**Plain language summary**: The hardest changes are to the citizen-facing wallet and the new credential issuance component — both of which have open-source foundations. The NDAChain chain itself requires no architectural change.

**5.3 The ZK Circuit: What It Checks (Without Explaining How)**
Non-technical prose:
> The mathematical proof generated by a citizen's phone checks three things simultaneously: (1) the citizen's credential was issued by an authorized government body; (2) the credential has not been revoked; (3) the specific claim being made (e.g., "age over 18") is true. The proof reveals none of the underlying data. It takes between 0.3 and 6 seconds to generate, depending on the citizen's device.

Technical depth in table:

**[TABLE 3: System Performance by Verification Tier]**

| Use Case | Verification Tier | Proof Generation (mid-range phone) | On-Chain Cost | Recommended For |
|---|---|---|---|---|
| Full KYC onboarding (new bank account) | Tier 1 | 1–3 seconds | ~$0.01 | High-stakes, one-time |
| Re-authentication (return customer) | Tier 2 | 0.3–0.8 seconds | ~$0.002 | Repeated, medium-stakes |
| Age gate / simple claim | Tier 3 | < 0.1 seconds | ~$0.0006 | High-frequency, low-stakes |

*For context: Vietnam's estimated peak national verification load is approximately 90 transactions per second, distributed across all Layer 1 systems. Each Layer 1 handles its own verification load; Layer 0 processes only batch anchoring updates (< 20 transactions per second). These figures are within the demonstrated capacity of current open-source ZK infrastructure.*

**5.4 Phased Implementation Roadmap**
Not a Gantt chart — a plain-language sequencing of what must happen before what.

*Phase 1 (2026): Prove the concept is legally sound and technically integrable*
- Legal: obtain formal opinion on LPDP compatibility of ZKC credential architecture.
- Technical: deploy a Polygon ID issuer node on a NDAChain testnet. Issue 1,000 test credentials. Run one bank's onboarding flow through ZK verification.
- Governance: draft the `did:zkkyc-vn` DID method specification. Submit to W3C registry.

*Phase 2 (2027–2028): Pilot with regulatory oversight*
- Expand to three banks and one government service (e.g., tax filing).
- Anchor NDAChain identity roots to a pilot Layer 0 instance.
- Measure: compliance cost reduction, user onboarding time, breach incident rate.
- Draft the Digital Identity Liability Sub-Decree based on pilot findings.

*Phase 3 (2029+): National rollout and sovereignty consolidation*
- Establish the national Layer 0 with full validator governance.
- Open Layer 1 registration to private sector operators.
- Begin ASEAN bilateral recognition discussions (technical compatibility is already present).

---

### Section 6 — Stakeholder Impact Analysis (~800 words)

**Reader's question:** *What changes for the people and organizations involved?*

**Four stakeholder profiles. Plain language. Honest about tradeoffs. Each profile: two paragraphs.**

**6.1 Citizens**: sovereignty over personal data; one-time registration; recovery mechanism for device loss; institutional fallback for non-digital users.

**6.2 Financial Institutions and Businesses**: reduced cost and liability from not storing PII; faster onboarding; compliance reporting via cryptographic attestation; integration investment required.

**6.3 Government (Issuer and Regulator)**: shift from data warehouse to trust infrastructure operator; near-real-time compliance audit via Layer 0; Layer 0 governance responsibility; liability framework drafting required.

**6.4 Foreign Digital Platforms**: integration with national identity standard is required to operate; metadata sovereignty preserved; W3C compatibility means no custom development for compliant platforms.

---

### Section 7 — Strategic Comparison (~900 words)

**Reader's question:** *Why not Google Wallet or NDAChain standalone?*

**7.1 Three Paths, Honestly Characterized**
Each path gets one paragraph of genuine advantages, then one paragraph of the structural limitation.

**[TABLE 4: Strategic Comparison]**

| Dimension | Corporate Platform (e.g., Google) | Closed National (NDAChain standalone) | Proposed Hybrid L0/L1 |
|---|---|---|---|
| LPDP Art. 3 compliance | Partial — proof is private; metadata is not | Partial — linkability via unified ID | Full — by design |
| National sovereignty | Low — foreign-controlled infrastructure | High — but closed to private sector | High + open |
| Private sector innovation | Low — vendor terms govern | Low — consortium approval required | High — permissionless Layer 1 |
| Upgrade resilience | Medium — vendor-controlled | Low — hard fork risk to history integrity | High — L1 upgradeable, L0 stable |
| International interoperability | High (W3C/EUDI compatible) | Low — custom format | High (W3C/EUDI/OID4VC compatible) |
| Time to first deployment | Fast | Medium | Medium (Phase 1 is low-risk) |
| NDAChain compatibility | Incompatible | Native | Extends NDAChain's role |

**7.2 The Hard Fork Problem (Plain Language)**
- One key technical point that changes the strategic assessment of the closed national model — explained without jargon.
- A chain that must be fundamentally changed to fix a flaw has retroactively undermined its own central claim (that its records are permanent and reliable).
- The L0/L1 separation eliminates this: application layer changes (NDAChain upgrades) do not touch the trust foundation layer.

**7.3 The Metadata Sovereignty Point**
- Even a privacy-preserving corporate platform collects metadata — which services you verify for, how often, at what times.
- For a national identity system, this metadata is the surveillance record. It reveals political activity, financial behavior, and social relationships.
- National Layer 0 + open wallet standard: this metadata is not generated.

---

### Section 8 — Risk and Limitation Analysis (~900 words)

**Reader's question:** *What could go wrong, and are you being honest about it?*

**Four objections, addressed directly. Plain language. No deflection.**

**8.1 Device Loss and Recovery**
- Specific mechanism: Shamir Secret Sharing distributed to 3–5 designated guardians (family members, employer, etc.). Recovery threshold: any 3 of 5. Recovery time window: 72 hours.
- Institutional fallback: commune-level government office with physical CCCD verification.
- Mandatory setup: recovery configuration must be completed during initial registration, not offered as optional.

**8.2 Surveillance Risk**
- Direct acknowledgment: the architecture prevents mass behavioral surveillance via Layer 0.
- Acknowledged limitation: the government's control of Layer 1 issuance (NDAChain) means credential denial to specific individuals remains possible — identical to today's situation with physical ID issuance.
- What the architecture does not solve: governance of issuance fairness. This is a rule-of-law problem, not a technical one.

**8.3 Technology Maturity**
- Core components are production-proven (cite Table in Section 3.2).
- Novel elements: governance architecture and NDAChain integration.
- Explicit risk mitigation: phased deployment starting with a controlled pilot minimizes exposure to novel integration risks.

**8.4 Quantum Computing**
- One paragraph, no jargon: the mathematics underlying current digital security — including this system — would be vulnerable to a sufficiently powerful quantum computer. No such computer exists today. Leading estimates place the risk horizon at 10–15 years.
- The system is designed for crypto-agility: the mathematical algorithms can be replaced without replacing the governance structure or re-issuing credentials. This is an explicit design requirement documented in the technical appendix (Appendix H).

**8.5 Limitations of This Paper**
- The integration path is specified, not implemented. Pilot deployment is the next required step.
- The security analysis assumes the governance structure operates as designed. State capture of the validator set is an acknowledged political risk outside the technical scope.
- Full formal security proofs of the composite system are not provided and are left to future work.

---

### Section 9 — Policy Recommendations (~600 words)

**Reader's question:** *What should actually happen, in what order?*

Seven numbered recommendations, sequenced by time horizon and dependency. Each recommendation: one sentence of action, one sentence of rationale.

1. **Commission a legal opinion (2026)**: formal LPDP compatibility assessment of ZKC architecture. *Rationale: removes the largest institutional uncertainty before technical investment begins.*

2. **Run a controlled pilot (2026–2027)**: two commercial banks + one government service. Issue ZKCs; run ZK verification for one defined use case. *Rationale: validates integration assumptions and generates evidence for regulatory confidence.*

3. **Adopt W3C VC as the national credential standard (2026)**: a standards decision, not a deployment. *Rationale: prevents future lock-in; costs little; signals commitment to international interoperability.*

4. **Reposition NDAChain as an authorized Layer 1 (2027)**: pilot the `AnchorMerkleRoot` protocol on a testnet Layer 0, using data from recommendation 2. *Rationale: preserves the NDAChain investment while enabling the sovereignty and openness benefits of the layered architecture.*

5. **Establish a Credential Governance Office (2027)**: within MIC, responsible for issuer registry, credential schema, and Layer 0 governance rules. *Rationale: the architecture requires an institutional home; a governance vacuum will produce fragmentation.*

6. **Enact a Digital Identity Liability Sub-Decree (2028)**: clarify legal responsibilities of citizens, issuers, and verifiers. *Rationale: private sector adoption will stall without clear liability rules; existing electronic transactions law provides the legal basis.*

7. **Open bilateral recognition discussions with ASEAN and EU (2029+)**: the `did:zkkyc-vn` standard is technically compatible with EU EUDI Wallet and W3C VC ecosystems; political recognition is the remaining barrier. *Rationale: cross-border digital identity recognition is an economic competitiveness issue, not only a governance one.*

---

### Section 10 — Conclusion (~400 words)

Three paragraphs:

**Paragraph 1: The argument, condensed**
Vietnam's LPDP creates a genuine architectural crisis for KYC systems — one that cannot be resolved by incremental improvement. The proposed ZK-KYC hybrid architecture resolves this crisis by separating trust settlement from application logic, enabling organizations to verify identity attributes without collecting personal data.

**Paragraph 2: The strategic significance**
The choice between a corporate-controlled and a closed government-controlled identity infrastructure is a false binary. The layered architecture proposed here enables national sovereignty over the trust foundation, open innovation in the application layer, and full LPDP compliance by design — simultaneously.

**Paragraph 3: The broader implication**
Vietnam is not alone in this challenge. Data minimization requirements similar to the LPDP are being enacted across Southeast Asia and beyond. A national identity infrastructure built on the principles described here — verifiable, sovereign, interoperable, and upgradeable — is a model for the region, not only a solution for one country.

---

## How the Technical Appendix Works

The appendix exists for one purpose: **to make every technical claim in the main body verifiable by a specialist reader**.

Structure it as a direct reference map:

| Appendix | Validates This Main-Body Claim | Key Content |
|---|---|---|
| A: Circuit Specification | Table 3 proof generation times | Constraint budget breakdown; PLONK UltraPLONK justification |
| B: Nullifier Construction | Section 4.3 cross-service unlinkability claim | Poseidon(identity_secret, context_id) formula; on-chain registry |
| C: L0 Consensus Design | Section 4.2 "no single entity controls it" claim | Tendermint BFT; 2-tier validator governance; transaction types |
| D: L0/L1 Interoperability | Table 2 AnchorMerkleRoot integration | Full protocol specification; staleness policy |
| E: Revocation Mechanism | Section 4.3 "cancelled within minutes" claim | Sparse Merkle Tree non-membership proof; dual-root anchoring |
| F: Scalability Benchmarks | Table 3 performance figures | National TPS analysis; off-chain vs. on-chain cost model |
| G: DID and VC Standards | Section 5.2 "no custom development" claim | did:zkkyc-vn spec; W3C VC + BJJ alignment; EUDI compatibility |
| H: Post-Quantum Migration | Section 8.4 "crypto-agility" claim | 3-phase migration; NIST FIPS 203/204/205 alignment |
| I: Social Recovery | Section 8.1 specific recovery mechanism | SSS parameters; guardian authentication; institutional fallback |
| J: Legal Contract Enforceability | Section 4 smart contract claim | Judicial Oracle Network; 4-of-6 multisig; formal verification requirement |

The appendix does not need to be readable by the general audience. It needs to be technically airtight.

---

## Final Checklist: Does This Paper Do Both Jobs?

| Requirement | How It Is Met |
|---|---|
| Non-technical reader can follow the argument | Prose body uses plain language throughout; analogies are consistent |
| Technical reviewer sees real depth | Tables 1–4, Figures 1–3, and Appendices A–J carry the specification |
| "We did the work" is demonstrated | Table 2 (NDAChain integration requirements) is the falsifiable claim that signals genuine implementation analysis |
| Not a theoretical guess | Named open-source stack (Polygon ID, Semaphore, Cosmos SDK); specific code-reuse estimate (70%); concrete Phase 1 pilot design |
| Policy-actionable | 7 numbered recommendations with explicit dependencies and time horizons |
| Limitations are honest | Section 8.5 explicitly states what the paper does not prove |
