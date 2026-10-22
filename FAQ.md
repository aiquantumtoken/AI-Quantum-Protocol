# AI Quantum Protocol ($AIQT) - Frequently Asked Questions (FAQ)

---

### 1. What is AI Quantum Protocol ($AIQT)?
$AIQT is the first post-quantum machine-to-machine (M2M) settlement currency and smart custody layer built natively on Solana (Token-2022). It protects autonomous AI agents from future quantum computer attacks while enabling frictionless sub-cent agent-to-agent micropayments.

---

### 2. Why do 24/7 autonomous AI agents need post-quantum security?
Human crypto investors store their private keys on offline hardware wallets (like Ledger) and only sign transactions occasionally. In contrast, autonomous AI agents run 24/7 on cloud servers, signing thousands of transactions daily with hot keys in server memory. Every transaction exposes their public key on the Solana ledger.

Because standard Solana addresses use **Ed25519 (elliptic curves)**, a Cryptographically Relevant Quantum Computer (CRQC) running Shor's algorithm can derive an agent's private key from an exposed public key in polynomial time $\mathcal{O}((\log N)^3)$. $AIQT$ solves this with **Dual-Tier Quantum Vaults** using **NIST FIPS-204 ML-DSA (CRYSTALS-Dilithium)** lattice commitments.

---

### 3. How does the Dual-Tier Quantum Vault work?
To prevent the "signature bloat" crisis (where 3KB post-quantum signatures slow down high-speed blockchains):
* **Tier 1 Fast Path (< 10,000 $AIQT):** Uses standard Solana Ed25519 for routine sub-second micropayments (~400ms latency, 64-byte signature).
* **Tier 2 Quantum Shield (≥ 10,000 $AIQT):** Mandates a secondary NIST FIPS-204 ML-DSA lattice dual-signature. Even if an attacker steals the agent's server hot key, the treasury cannot be drained without solving high-dimensional lattice math.

---

### 4. How does the 0.5% M2M deflationary burn work?
$AIQT leverages Solana Token-2022's native `TransferFeeConfig` extension. Every time an agent hires another agent or pays an API fee:
* An immutable **0.5% (50 basis points)** fee is processed directly on-chain.
* **50% of the fee is permanently incinerated** to the Solana dead address (`11111111111111111111111111111111`), continuously contracting the circulating supply.
* **50% of the fee funds autonomous agent compute/GPU resources**.

---

### 5. What are the tokenomics and supply numbers?
* **Total Supply:** 1,000,000,000 $AIQT (1 Billion, permanently fixed).
* **60% Public DEX Liquidity:** Paired with SOL on Raydium with **100% of LP tokens burned permanently**.
* **15% Agent Staking Reserve:** Performance yield for third-party autonomous bots.
* **10% Core Development:** Multi-sig locked with 6-month cliff and 18-month linear vesting.
* **10% Ecosystem Grants & Marketing:** Builder hackathons and marketing amplification.
* **5% Flagship Agent Treasury:** Seed capital for the autonomous agent swarm.

---

### 6. Can the developers mint more tokens or freeze wallets?
**No.** All authorities are permanently secured:
* **Mint Authority:** Revoked immediately following genesis mint. No one can ever print another token.
* **Freeze Authority:** Completely disabled (`freezeAuthority = None`). Wallets cannot be frozen or blacklisted.
* **Audit Score:** 100/100 Clean score verified (`AUDIT_REPORT.md`).

---

### 7. How do external developers integrate $AIQT?
We offer two open-source developer packages:
1. **Core SDK:** `@aiqt/agent-sdk` (v0.1.0) on npm.
2. **ElizaOS Plugin:** `@aiqt/plugin-solana-quantum` for the largest open-source agent framework in crypto.
3. **Developer CLI:** `bin/aiqt-cli.mjs` for 1-command agent scaffolding.

---

### 8. Where can I view the live code and pitch deck?
* **Web Portal:** https://aiquantumtoken.github.io/AI-Quantum-Protocol/
* **Interactive Pitch Deck:** https://aiquantumtoken.github.io/AI-Quantum-Protocol/pitch.html
* **Airdrop Checker:** https://aiquantumtoken.github.io/AI-Quantum-Protocol/airdrop.html
* **GitHub Repository:** https://github.com/aiquantumtoken/AI-Quantum-Protocol
