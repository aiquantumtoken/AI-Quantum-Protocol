# AI Quantum Protocol ($AIQT) Technical Architecture

> **Dual-Tier Quantum-Safe Custody and Machine-to-Machine Settlements for Autonomous Agents on Solana.**

---

## 1. The Autonomous Agent Attack Surface

Traditional cryptocurrency security assumes a **human signer** who guards their private keys in an offline hardware wallet (e.g., Ledger). Autonomous AI agents break this security model completely:

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE AGENT SECURITY CRISIS                    │
├───────────────────────────────┬─────────────────────────────────┤
│ HUMAN CRYPTO HOLDER           │ 24/7 AUTONOMOUS AI AGENT        │
├───────────────────────────────┼─────────────────────────────────┤
│ • Keys stored in cold storage │ • Keys reside in live memory on │
│ • Signed 1-2 times per week   │   cloud servers / RPC nodes     │
│ • Physical confirmation needed│ • Signs 10,000+ txs per day     │
│ • Zero exposure to automated  │ • Exposed public keys in the    │
│   mempool key reconstruction  │   mempool open to Shor's attack │
└───────────────────────────────┴─────────────────────────────────┘
```

On Solana, all standard accounts utilize **Ed25519 (Edwards-curve Digital Signature Algorithm)**. A Cryptographically Relevant Quantum Computer (CRQC) running Shor's algorithm can derive an Ed25519 private key from an exposed public key in polynomial time $\mathcal{O}((\log N)^3)$. Because autonomous agents continuously reveal their public keys during automated operations, they are the most vulnerable targets in Web3.

---

## 2. The Dual-Tier Quantum Vault Solution

To solve this without sacrificing Solana's 400ms transaction finality, `$AIQT` introduces a **Dual-Tier Vault Model**:

```
                       ┌─────────────────────────┐
                       │  Agent Action Request   │
                       └────────────┬────────────┘
                                    │
                         Is Amount >= 10,000 $AIQT?
                                    │
                    ┌───────────────┴───────────────┐
                   NO                              YES
                    │                               │
                    ▼                               ▼
       ┌────────────────────────┐      ┌─────────────────────────┐
       │   TIER 1: FAST PATH    │      │ TIER 2: QUANTUM SHIELD  │
       │  Standard Solana Ed25519│      │ Ed25519 + NIST ML-DSA   │
       │  Sub-second execution  │      │ Lattice Commitment      │
       │  Low-value micro fees  │      │ Full Shor's Immunity    │
       └────────────────────────┘      └─────────────────────────┘
```

### Tier 1: Fast-Path Micropayments (< Threshold)
* Used for everyday autonomous agent tasks: paying for RPC calls, hiring sub-agents, or querying Pyth/Chainlink oracle feeds.
* Standard Solana execution ensures high TPS and sub-cent fees.

### Tier 2: Quantum-Shielded Treasury Transfers (≥ Threshold)
* Any transaction moving significant capital (e.g., liquidity rebalancing, staking, treasury withdrawals) **must produce a valid NIST FIPS-204 ML-DSA (CRYSTALS-Dilithium) signature**.
* Even if an attacker steals the agent's hot server private key, **they cannot drain the vault** because the quantum lattice lock invalidates single-signature withdrawals.

---

## 3. Token-2022 Deflationary Flywheel

$AIQT is deployed using the Solana **Token-2022 Program** (`TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`), leveraging the native `TransferFeeConfig` extension:

$$\text{Burn Amount} = \frac{\text{Transaction Amount} \times 50\text{ bps}}{10,000} = 0.5\%$$

```
   ┌───────────────────────────────────────────────┐
   │ Autonomous Agents Transact & Hire Each Other  │
   └───────────────────────┬───────────────────────┘
                           │
                           ▼
          0.5% Protocol Fee Deducted on-chain
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
    50% Burned Permanently       50% Fuels Autonomous
   (Supply Contractive Pressure)   Agent Compute / GPU
```

---

## 4. Competitive Matrix

| Feature | Legacy Solana Agent Coins | **AI Quantum Protocol ($AIQT)** |
| :--- | :--- | :--- |
| **Blockchain** | Solana SPL (Legacy) | **Solana Token-2022** |
| **Quantum Resistance** | ❌ None (Vulnerable Ed25519) | ✅ **NIST FIPS-204 ML-DSA Lattice** |
| **Autonomous Vault Security** | Single Hot Server Key | **Dual-Tier Quantum Lock** |
| **M2M Deflationary Sink** | ❌ Manual buybacks only | ✅ **Native 0.5% Automated Burn** |
| **Open Developer SDK** | Fragmented | ✅ **`@aiqt/agent-sdk` (v0.1.0)** |
