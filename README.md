# AI Quantum Protocol ($AIQT)

> **The First Post-Quantum Autonomous Agent Network on Solana.**

[![Solana](https://img.shields.io/badge/Network-Solana-9945FF?logo=solana)](https://solana.com)
[![Token](https://img.shields.io/badge/Ticker-$AIQT-00FFA3)](#)
[![Status](https://img.shields.io/badge/Status-Development-orange)](#)

---

## Overview
**$AIQT** is an autonomous machine-to-machine cryptocurrency built on Solana, specifically engineered to secure and power AI agent swarms under post-quantum cryptographic standards.

### Key Highlights
* **Solana Speed:** Sub-second finality for high-velocity agent micropayments.
* **Quantum-Resilient Security:** Mitigating the exposed Ed25519 public-key vulnerabilities inherent to 24/7 automated agent wallets.
* **Proof-of-Agent-Performance:** Staking & slashing mechanism holding autonomous bots accountable for data quality and trade execution.
* **Autonomous Deflation:** 0.5% protocol burn on every inter-agent task settlement.

---

## Repository Structure
```
├── WHITEPAPER.md               # Complete cryptographic and economic whitepaper
├── 30_day_launch_plan.md       # Master day-by-day roadmap
├── telegram_notify.py          # Secure Telegram bridge for team alerts
├── .env                        # Local configuration
└── src/
    └── agent/
        ├── agent_wallet.py     # Autonomous agent key management
        ├── aiqt_agent.py       # Live Solana mainnet agent monitor & signer
        └── agent_wallet.json   # Local agent key identity
```

---

## Running the Flagship Agent
```bash
python src/agent/aiqt_agent.py
```
