"""
AI Quantum Protocol ($AIQT) - Complete End-to-End Test Suite
Validates all cryptographic, economic, and autonomous agent modules.
"""

import unittest
import json
import os
import sys

# Ensure UTF-8 output encoding for console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.crypto.quantum_shield import QuantumShield
from src.crypto.cross_chain_relayer import CrossChainQuantumRelayer
from src.agent.agent_wallet import AgentWallet
from src.agent.quantum_vault import QuantumAgentVault
from src.agent.agent_marketplace import AgentMarketplace
from src.agent.buyback_burn_bot import BuybackBurnBot

class TestAIQTProtocol(unittest.TestCase):

    def test_token_specification(self):
        with open("config/aiqt_token_spec.json", "r", encoding="utf-8") as f:
            spec = json.load(f)
        self.assertEqual(spec["total_supply"], 1_000_000_000)
        self.assertEqual(spec["decimals"], 9)
        self.assertEqual(spec["transfer_fee_basis_points"], 50)
        self.assertEqual(spec["program_id"], "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb")
        
        allocations = spec["allocations"]
        total_pct = sum(a["percentage"] for a in allocations.values())
        self.assertEqual(total_pct, 100)

    def test_quantum_shield_signing_and_verification(self):
        shield = QuantumShield()
        self.assertTrue(shield.lattice_public_key.startswith("PQ-"))
        payload = b"TEST_M2M_TASK_PAYLOAD_AIQT"
        sig_data = shield.sign_hybrid("fast_ed25519_sig", payload)
        self.assertEqual(sig_data["algorithm"], "Hybrid-Ed25519+ML-DSA-v1")
        self.assertEqual(sig_data["nist_standard"], "FIPS-204-ML-DSA")
        
        is_valid = QuantumShield.verify_quantum_commitment(
            payload,
            sig_data["quantum_lattice_signature"],
            shield.lattice_secret_key
        )
        self.assertTrue(is_valid)

    def test_dual_tier_quantum_vault(self):
        vault = QuantumAgentVault(high_value_threshold=10_000)
        
        # Test low-value fast path
        tx_low = vault.authorize_transaction("Recipient111", 500, "MICRO_TASK")
        self.assertEqual(tx_low["tier"], "TIER_1_HOT_PATH")
        self.assertIsNone(tx_low["quantum_lattice_signature"])
        
        # Test high-value quantum shield
        tx_high = vault.authorize_transaction("Recipient222", 25_000, "TREASURY_REBALANCE")
        self.assertEqual(tx_high["tier"], "TIER_2_QUANTUM_SHIELDED")
        self.assertIsNotNone(tx_high["quantum_lattice_signature"])
        self.assertEqual(tx_high["protection"], "NIST FIPS-204 ML-DSA Dual-Lock")

    def test_agent_marketplace_and_burn_fee(self):
        market = AgentMarketplace()
        market.register_agent("analyst_01", "SENTIMENT", 2000, 10_000, "PQ-TEST")
        
        task = market.execute_m2m_task("client_01", "analyst_01", "EXEC_TASK")
        self.assertEqual(task["gross_payment"], 2000)
        # 0.5% of 2000 is 10. Split 50/50 is 5 burn, 5 compute
        self.assertEqual(task["burn_amount"], 5)
        self.assertEqual(task["compute_fee"], 5)
        self.assertEqual(task["net_payout"], 1990)
        self.assertEqual(market.total_tokens_burned, 5)

    def test_buyback_burn_bot(self):
        bot = BuybackBurnBot()
        res = bot.simulate_or_execute_burn(task_volume_tokens=1_000_000)
        # 0.5% fee is 5,000. 50% burned is 2,500
        self.assertEqual(res["event"]["burned_tokens"], 2500)
        self.assertEqual(res["event"]["cumulative_burned"], 2500)

    def test_cross_chain_relayer_attestation(self):
        relayer = CrossChainQuantumRelayer(target_chain_id=8453)
        attestation = relayer.generate_cross_chain_attestation(1064, 459800000, "dummy_state_root")
        self.assertEqual(attestation["status"], "VALID_CROSS_CHAIN_PROOF")
        self.assertEqual(attestation["attestation"]["origin_network"], "Solana")
        
        is_valid = CrossChainQuantumRelayer.verify_attestation(attestation, relayer.shield.lattice_secret_key)
        self.assertTrue(is_valid)

if __name__ == "__main__":
    unittest.main()
