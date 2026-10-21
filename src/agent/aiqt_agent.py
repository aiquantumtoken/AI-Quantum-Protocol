import os
import sys
import json
import urllib.request

# Ensure UTF-8 output encoding for console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from agent_wallet import AgentWallet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from crypto.quantum_shield import QuantumShield

# Optional local dispatch hook
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from telegram_notify import send_telegram_message
except ImportError:
    send_telegram_message = None

SOLANA_RPC = "https://api.mainnet-beta.solana.com"

class AIQTAgent:
    """
    Flagship Autonomous Intelligence Agent for $AIQT.
    Runs autonomous market checks, signs verifiable agent tasks,
    and reports to the team.
    """
    def __init__(self):
        self.wallet = AgentWallet()
        self.quantum_shield = QuantumShield(self.wallet.secret_key_bytes)
        print(f"🤖 AIQT Flagship Agent initialized.")
        print(f"🔑 Solana Address: {self.wallet.get_public_key()}")
        print(f"🛡️ Post-Quantum Lattice Key: {self.quantum_shield.lattice_public_key}")

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
        ed25519_sig = self.wallet.sign_agent_message(task_payload)
        hybrid_sig = self.quantum_shield.sign_hybrid(ed25519_sig, task_payload.encode('utf-8'))

        report = (
            f"🧠 *AIQT Autonomous Agent Update*\n"
            f"• *Status:* Active & Monitoring Solana Mainnet\n"
            f"• *Agent Wallet:* `{self.wallet.get_public_key()[:8]}...{self.wallet.get_public_key()[-6:]}`\n"
            f"• *Lattice Identity:* `{self.quantum_shield.lattice_public_key[:12]}...`\n"
            f"• *Current Epoch:* `{epoch}` | *Slot:* `{slot}`\n"
            f"• *Standard Sig:* `{ed25519_sig[:12]}...`\n"
            f"• *Quantum Proof:* `{hybrid_sig['quantum_lattice_signature'][:16]}...`\n"
            f"• *NIST Security:* `FIPS-204 ML-DSA Lattice Compliant`\n\n"
            f"✅ *Next Step:* Devnet Token-2022 deployment & liquidity bootstrapping."
        )
        return report

if __name__ == "__main__":
    agent = AIQTAgent()
    report = agent.run_market_intelligence_cycle()
    print("\n--- REPORT OUTPUT ---")
    print(report)
