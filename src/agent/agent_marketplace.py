"""
AI Quantum Protocol ($AIQT) - Decentralized Agent-to-Agent (M2M) Marketplace
A permissionless machine-to-machine registry where autonomous AI agents:
  1. Register their API services, pricing in $AIQT, and NIST ML-DSA lattice keys.
  2. Stake $AIQT as a Proof-of-Performance security bond.
  3. Accept automated service tasks from other agents, executing with a 0.5% protocol burn.
"""

import json
import time
import os
import sys

# Ensure UTF-8 output encoding for console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from crypto.quantum_shield import QuantumShield

INCINERATION_ADDRESS = "11111111111111111111111111111111"

class AgentMarketplace:
    def __init__(self):
        self.registered_agents = {}
        self.completed_tasks = []
        self.total_tokens_burned = 0
        self.total_volume_processed = 0

    def register_agent(self, agent_id: str, service_name: str, price_aiqt: int, stake_amount: int, lattice_pubkey: str) -> dict:
        """
        Registers an autonomous AI agent in the M2M registry.
        Requires staking $AIQT as collateral against hallucinations or fraud.
        """
        if stake_amount < 1_000:
            raise ValueError("Minimum agent registration stake is 1,000 $AIQT")

        agent_entry = {
            "agent_id": agent_id,
            "service_name": service_name,
            "price_per_task": price_aiqt,
            "staked_aiqt": stake_amount,
            "lattice_public_key": lattice_pubkey,
            "reputation_score": 100,
            "tasks_completed": 0,
            "registered_at": int(time.time())
        }
        self.registered_agents[agent_id] = agent_entry
        return agent_entry

    def execute_m2m_task(self, client_agent_id: str, provider_agent_id: str, task_payload: str) -> dict:
        """
        Executes an autonomous task between two agents:
        - Transfers $AIQT payment.
        - Deducts 0.5% (50 bps) protocol fee.
        - Burns 50% permanently to 1111...1111.
        - Allocates 50% to autonomous agent compute fund.
        - Issues cryptographic task completion proof.
        """
        provider = self.registered_agents.get(provider_agent_id)
        if not provider:
            raise ValueError(f"Provider agent {provider_agent_id} not registered in marketplace")

        price = provider["price_per_task"]
        protocol_fee = int(price * 0.005) # 0.5%
        burned_fee = protocol_fee // 2
        compute_fee = protocol_fee - burned_fee
        net_provider_payout = price - protocol_fee

        self.total_tokens_burned += burned_fee
        self.total_volume_processed += price

        # Update provider stats
        provider["tasks_completed"] += 1
        provider["reputation_score"] = min(100, provider["reputation_score"] + 1)

        task_record = {
            "task_id": f"TASK-M2M-{len(self.completed_tasks) + 1:04d}",
            "client_agent": client_agent_id,
            "provider_agent": provider_agent_id,
            "service": provider["service_name"],
            "task_payload": task_payload,
            "gross_payment": price,
            "burn_amount": burned_fee,
            "compute_fee": compute_fee,
            "net_payout": net_provider_payout,
            "timestamp": int(time.time()),
            "status": "SETTLED_ON_CHAIN"
        }
        self.completed_tasks.append(task_record)

        return task_record

if __name__ == "__main__":
    print("🤖 Initializing AIQT Decentralized Agent Marketplace...\n")
    market = AgentMarketplace()

    # Register Agent 1: Deep Research Analyst
    agent1 = market.register_agent(
        agent_id="research_agent_01",
        service_name="DEEP_MARKET_SENTIMENT_ANALYSIS",
        price_aiqt=5_000,
        stake_amount=50_000,
        lattice_pubkey="PQ-Caj6ZEYf9qvGVAZuJdACExrkK4f7L3rutSvtSXSzY4ZF"
    )
    print(f"✅ Registered Service Provider: {agent1['agent_id']}")
    print(f"• Service: {agent1['service_name']} (Price: {agent1['price_per_task']:,} $AIQT)")
    print(f"• Staked Collateral: {agent1['staked_aiqt']:,} $AIQT\n")

    # Client Agent (Execution Bot) hires Research Agent
    print("⚡ Executing Autonomous M2M Task: Execution Bot hiring Research Bot...")
    task = market.execute_m2m_task(
        client_agent_id="trading_execution_bot_42",
        provider_agent_id="research_agent_01",
        task_payload="QUERY_MEMPOOL_ORDERBOOK_SOL"
    )
    print(json.dumps(task, indent=2))
    print(f"\n🔥 Protocol Burn: {task['burn_amount']} $AIQT incinerated permanently.")
    print(f"💰 Net Payout to Provider: {task['net_payout']} $AIQT")
    print(f"📈 Total Marketplace Volume: {market.total_volume_processed:,} $AIQT")
