"""
AI Quantum Protocol ($AIQT) - Token-2022 Specification & Launch Simulator
Generates Solana Token-2022 configuration, verifies mathematical allocations,
and prepares on-chain metadata for DEXScreener / Raydium.
"""

import json
import os
import hashlib

def generate_token_spec():
    TOTAL_SUPPLY = 1_000_000_000  # 1 Billion
    DECIMALS = 9
    BASE_UNITS = TOTAL_SUPPLY * (10 ** DECIMALS)

    allocations = {
        "public_liquidity_dex": {
            "percentage": 60,
            "tokens": int(TOTAL_SUPPLY * 0.60),
            "description": "Raydium / DEX liquidity paired with SOL, 100% LP burned"
        },
        "agent_staking_pool": {
            "percentage": 15,
            "tokens": int(TOTAL_SUPPLY * 0.15),
            "description": "Yield reserve for verified high-performance autonomous agents"
        },
        "protocol_development": {
            "percentage": 10,
            "tokens": int(TOTAL_SUPPLY * 0.10),
            "description": "Multi-sig treasury with 6-month cliff and 18-month vesting"
        },
        "marketing_and_ecosystem": {
            "percentage": 10,
            "tokens": int(TOTAL_SUPPLY * 0.10),
            "description": "KOL partnerships, hackathons, and developer grants"
        },
        "flagship_agent_treasury": {
            "percentage": 5,
            "tokens": int(TOTAL_SUPPLY * 0.05),
            "description": "Autonomous AI Agent seed fund for compute & automated buybacks"
        }
    }

    # Verify 100% sum
    total_percent = sum(item["percentage"] for item in allocations.values())
    total_tokens = sum(item["tokens"] for item in allocations.values())
    assert total_percent == 100, f"Error: Allocation total is {total_percent}%"
    assert total_tokens == TOTAL_SUPPLY, f"Error: Token total is {total_tokens}"

    metadata = {
        "name": "AI Quantum Protocol",
        "symbol": "AIQT",
        "description": "The first post-quantum autonomous agent network on Solana. High-speed M2M settlements secured by lattice-based cryptography.",
        "image": "https://raw.githubusercontent.com/aiqt-protocol/branding/main/logo.png",
        "external_url": "https://aiqt.network",
        "attributes": [
            {"trait_type": "Network", "value": "Solana"},
            {"trait_type": "Standard", "value": "Token-2022"},
            {"trait_type": "Security", "value": "Post-Quantum Dilithium/Falcon Hybrid"},
            {"trait_type": "Agentic M2M", "value": "Enabled"}
        ],
        "properties": {
            "category": "utility",
            "creators": [
                {"address": "AIQTxAgent1111111111111111111111111111111111", "share": 100}
            ]
        }
    }

    token_config = {
        "program_id": "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb", # Token-2022 standard
        "symbol": "AIQT",
        "name": "AI Quantum Protocol",
        "decimals": DECIMALS,
        "total_supply": TOTAL_SUPPLY,
        "total_supply_base_units": str(BASE_UNITS),
        "transfer_fee_basis_points": 50, # 0.5% M2M burn/fee
        "maximum_fee": str(5_000 * (10 ** DECIMALS)),
        "extensions": [
            "TransferFeeConfig",
            "MetadataPointer",
            "TokenMetadata"
        ],
        "allocations": allocations,
        "onchain_metadata": metadata
    }

    os.makedirs("config", exist_ok=True)
    with open("config/aiqt_token_spec.json", "w", encoding="utf-8") as f:
        json.dump(token_config, f, indent=2)

    with open("config/metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("SUCCESS: Token-2022 Specification generated and mathematically verified.")
    print(f"Total Supply: {TOTAL_SUPPLY:,} $AIQT across {DECIMALS} decimals.")
    return token_config

if __name__ == "__main__":
    generate_token_spec()
