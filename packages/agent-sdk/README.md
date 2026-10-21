# @aiqt/agent-sdk

> Official Developer SDK for Autonomous AI Agents on Solana, secured by NIST Post-Quantum Cryptography.

## Features
* 🛡️ **Post-Quantum Lattice Identity:** Automatically derives ML-DSA (CRYSTALS-Dilithium) commitments to protect agent treasuries.
* ⚡ **M2M Micro-Settlements:** Built-in protocol fee calculations (0.5% autonomous deflationary burn).
* 🤖 **Verifiable Task Proofs:** Programmatically sign and verify inter-agent service exchanges.

## Quick Installation
```bash
npm install @aiqt/agent-sdk
```

## Usage Example
```javascript
import { QuantumAgentClient } from '@aiqt/agent-sdk';

// Initialize autonomous agent client
const agent = new QuantumAgentClient('market_intelligence_agent_01');
console.log('Agent Lattice Public Key:', agent.latticeKeyPair.publicKey);

// Sign a machine-to-machine task payload
const task = { service: "FETCH_ORDERBOOK", fee: "500000000" };
const proof = agent.signM2MTask(task);
console.log('Proof Signature:', proof.signature);

// Calculate 0.5% deflationary burn
const fee = QuantumAgentClient.calculateTaskFee(1000000000n);
console.log('Burned Amount:', fee.burnFee);
```
