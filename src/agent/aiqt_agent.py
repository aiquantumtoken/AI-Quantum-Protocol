import os
import sys
import json
import urllib.request

# Ensure UTF-8 output encoding for console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from agent_wallet import AgentWallet

# Add parent directory to path to access telegram_notify
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from telegram_notify import send_telegram_message

SOLANA_RPC = "https://api.mainnet-beta.solana.com"

class AIQTAgent:
    """
    Flagship Autonomous Intelligence Agent for $AIQT.
    Runs autonomous market checks, signs verifiable agent tasks,
    and reports to the team.
    """
    def __init__(self):
        self.wallet = AgentWallet()
        print(f"🤖 AIQT Flagship Agent initialized.")
        print(f"🔑 Public Key: {self.wallet.get_public_key()}")

    def check_solana_network(self) -> dict:
        req_data = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getEpochInfo"
        }).encode('utf-8')

        req = urllib.request.Request(
            SOLANA_RPC,
            data=req_data,
            headers={"Content-Type": "application/json", "User-Agent": "AIQT-Agent/1.0"}
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return data.get("result", {})
        except Exception as e:
            return {"error": str(e)}

    def run_market_intelligence_cycle(self) -> str:
        epoch_info = self.check_solana_network()
        epoch = epoch_info.get("epoch", "N/A")
        slot = epoch_info.get("absoluteSlot", "N/A")

        task_payload = f"AIQT-INTEL-CYCLE: Solana Epoch {epoch}, Slot {slot}"
        signature = self.wallet.sign_agent_message(task_payload)

        report = (
            f"🧠 *AIQT Autonomous Agent Update*\n"
            f"• *Status:* Active & Monitoring Solana Mainnet\n"
            f"• *Agent Wallet:* `{self.wallet.get_public_key()[:8]}...{self.wallet.get_public_key()[-6:]}`\n"
            f"• *Current Epoch:* `{epoch}` | *Slot:* `{slot}`\n"
            f"• *Cryptographic Proof:* `{signature[:16]}...`\n"
            f"• *Target Token:* `$AIQT` (AI Quantum Protocol)\n\n"
            f"✅ *Next Step:* SPL Token-2022 deployment preparation & initial community assets."
        )
        return report

if __name__ == "__main__":
    agent = AIQTAgent()
    report = agent.run_market_intelligence_cycle()
    print("\n--- REPORT OUTPUT ---")
    print(report)
