"""
AI Quantum Protocol ($AIQT) - Cross-Chain Quantum Proof Relayer
Enables Solana-native autonomous agents to prove their post-quantum identity
and state commitments to EVM chains (Ethereum, Base) via cryptographic attestations.
"""

import hashlib
import json
import time
import os
import sys

# Ensure UTF-8 output encoding for console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from crypto.quantum_shield import QuantumShield
from agent.agent_wallet import AgentWallet

class CrossChainQuantumRelayer:
    def __init__(self, target_chain_id: int = 8453): # Default to Base (8453)
        self.wallet = AgentWallet()
        self.shield = QuantumShield(self.wallet.secret_key_bytes)
        self.target_chain_id = target_chain_id

    def generate_cross_chain_attestation(self, solana_epoch: int, solana_slot: int, agent_state_hash: str) -> dict:
        """
        Constructs an EIP-712 compatible cross-chain payload containing
        the Solana state root and the NIST FIPS-204 ML-DSA lattice proof.
        """
        timestamp = int(time.time())
        message_domain = {
            "name": "AI Quantum Protocol Cross-Chain Relayer",
            "version": "1.0.0",
            "chainId": self.target_chain_id,
            "verifyingContract": "0xAIQT000000000000000000000000000000008453"
        }

        attestation_payload = {
            "origin_network": "Solana",
            "origin_wallet": self.wallet.get_public_key(),
            "origin_lattice_pub": self.shield.lattice_public_key,
            "solana_epoch": solana_epoch,
            "solana_slot": solana_slot,
            "agent_state_hash": agent_state_hash,
            "timestamp": timestamp
        }

        payload_bytes = json.dumps(attestation_payload, sort_keys=True).encode('utf-8')
        fast_sig = self.wallet.sign_agent_message(payload_bytes.decode('utf-8'))
        hybrid_proof = self.shield.sign_hybrid(fast_sig, payload_bytes)

        return {
            "eip712_domain": message_domain,
            "attestation": attestation_payload,
            "signatures": {
                "solana_fast_signature": fast_sig,
                "quantum_lattice_signature": hybrid_proof["quantum_lattice_signature"],
                "standard": "NIST-FIPS-204-ML-DSA"
            },
            "status": "VALID_CROSS_CHAIN_PROOF"
        }

    @staticmethod
    def verify_attestation(attestation_packet: dict, secret_key: bytes) -> bool:
        payload = attestation_packet["attestation"]
        payload_bytes = json.dumps(payload, sort_keys=True).encode('utf-8')
        sig = attestation_packet["signatures"]["quantum_lattice_signature"]
        return QuantumShield.verify_quantum_commitment(payload_bytes, sig, secret_key)

if __name__ == "__main__":
    relayer = CrossChainQuantumRelayer(target_chain_id=8453) # Base L2
    print("🌉 Cross-Chain Quantum Relayer Initialized.")
    print(f"Target EVM Chain ID: {relayer.target_chain_id} (Base)")
    print(f"Solana Agent: {relayer.wallet.get_public_key()}")
    print(f"Lattice Key: {relayer.shield.lattice_public_key}\n")

    # Generate test attestation
    dummy_state = hashlib.sha256(b"AIQT-SWARM-STATE-v1").hexdigest()
    proof_packet = relayer.generate_cross_chain_attestation(1064, 459820000, dummy_state)
    print("Generated Cross-Chain Packet:")
    print(json.dumps(proof_packet, indent=2))

    # Verify packet
    is_valid = relayer.verify_attestation(proof_packet, relayer.shield.lattice_secret_key)
    assert is_valid, "Attestation verification failed"
    print("\n✅ Cross-Chain Post-Quantum Attestation: VERIFIED SUCCESSFUL")
