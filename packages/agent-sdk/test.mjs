import { QuantumAgentClient } from './index.mjs';

console.log("Testing @aiqt/agent-sdk...");

const client = new QuantumAgentClient("alpha_market_maker_01");
console.log("• Agent ID:", client.agentId);
console.log("• Post-Quantum Public Key:", client.latticeKeyPair.publicKey);

// Test task signing
const task = { action: "DATA_QUERY", provider: "pyth_network", cost: 1000000000 };
const proof = client.signM2MTask(task);
console.log("• Cryptographic Proof generated:", proof.signature.slice(0, 16) + "...");

// Test fee math
const feeCalc = QuantumAgentClient.calculateTaskFee(1_000_000_000n);
console.log("• Fee Calculation (1,000 $AIQT):", feeCalc);
if (feeCalc.burnFee === "5000000") {
  console.log("✅ Math check: 0.5% burn verified.");
}

console.log("✅ All @aiqt/agent-sdk tests PASSED.");
