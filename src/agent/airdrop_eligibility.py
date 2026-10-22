"""
AI Quantum Protocol ($AIQT) - Airdrop & Early Adopter Eligibility Engine
Scores Solana wallets based on on-chain AI agent engagement, DeFi activity,
and cryptographic attestation participation.
"""

import json
import hashlib
import time

# Allocation: 10% Ecosystem & Community (100,000,000 $AIQT)
AIRDROP_POOL_TOKENS = 100_000_000

class AirdropScorer:
    def __init__(self):
        self.tiers = {
            "TIER_1_QUANTUM_SENTINEL": {"min_score": 80, "base_tokens": 10_000, "multiplier": 2.0},
            "TIER_2_AGENT_BUILDER":    {"min_score": 50, "base_tokens": 5_000,  "multiplier": 1.5},
            "TIER_3_ECOSYSTEM_SCOUT":  {"min_score": 20, "base_tokens": 1_500,  "multiplier": 1.0},
            "TIER_INELIGIBLE":         {"min_score": 0,  "base_tokens": 0,      "multiplier": 0.0}
        }

    def evaluate_wallet(self, wallet_address: str, criteria: dict) -> dict:
        """
        Calculates eligibility score (0-100) based on on-chain and social factors:
        - holds_ai_tokens (bool): +30 pts
        - solana_tx_count (> 50): +25 pts
        - starred_github (bool):  +25 pts
        - joined_telegram (bool): +20 pts
        """
        score = 0
        breakdown = []

        if criteria.get("holds_ai_tokens", False):
            score += 30
            breakdown.append("Active AI Agent Token Holder (+30)")

        if criteria.get("solana_tx_count", 0) >= 50:
            score += 25
            breakdown.append("Solana Mainnet Power User (+25)")
        elif criteria.get("solana_tx_count", 0) >= 10:
            score += 15
            breakdown.append("Solana Active User (+15)")

        if criteria.get("starred_github", False):
            score += 25
            breakdown.append("AIQT GitHub Contributor (+25)")

        if criteria.get("joined_telegram", False):
            score += 20
            breakdown.append("Telegram Verified Pioneer (+20)")

        # Determine Tier
        assigned_tier = "TIER_INELIGIBLE"
        tier_data = self.tiers["TIER_INELIGIBLE"]
        for t_name, t_info in self.tiers.items():
            if score >= t_info["min_score"]:
                assigned_tier = t_name
                tier_data = t_info
                break

        estimated_allocation = int(tier_data["base_tokens"] * tier_data["multiplier"])

        # Cryptographic Verification Hash
        verification_hash = hashlib.sha256(f"{wallet_address}::{score}::{assigned_tier}".encode('utf-8')).hexdigest()

        return {
            "wallet": wallet_address,
            "score": score,
            "tier": assigned_tier,
            "estimated_allocation": estimated_allocation,
            "breakdown": breakdown,
            "verification_hash": verification_hash,
            "timestamp": int(time.time())
        }

if __name__ == "__main__":
    scorer = AirdropScorer()
    sample_wallet = "3bfbCF1UsipVWHBBdkaW3VZqiCCDQ6QVEEbnoK2j7oCh"
    result = scorer.evaluate_wallet(sample_wallet, {
        "holds_ai_tokens": True,
        "solana_tx_count": 65,
        "starred_github": True,
        "joined_telegram": True
    })
    print("Airdrop Eligibility Evaluation:")
    print(json.dumps(result, indent=2))
