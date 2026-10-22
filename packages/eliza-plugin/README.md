# @aiqt/plugin-solana-quantum

> Official ElizaOS Plugin for AI Quantum Protocol ($AIQT) on Solana.

Grants any autonomous AI agent running on [ElizaOS](https://github.com/elizaOS/eliza) post-quantum cryptographic custody and machine-to-machine settlement capabilities.

## Installation
```bash
npm install @aiqt/plugin-solana-quantum
```

## Setup in ElizaOS Character
Add `"@aiqt/plugin-solana-quantum"` to your `character.json`:

```json
{
  "name": "MyAgent",
  "plugins": ["@aiqt/plugin-solana-quantum"]
}
```

## Features
* 🛡️ **NIST FIPS-204 ML-DSA Lattice Signatures:** Dual-tier signing protects autonomous server treasuries from discrete log quantum attacks.
* 🔥 **Autonomous Deflationary M2M Sink:** Automatically routes 0.5% protocol fee on agent tasks, burning 50% permanently to `1111...1111`.
* ⚡ **Live Solana Telemetry Provider:** Feeds real-time Epoch, Slot, and cluster performance directly into agent context.
