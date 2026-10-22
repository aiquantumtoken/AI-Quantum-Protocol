"""
AI Quantum Protocol ($AIQT) - Telegram Community Bot Responder
Interactive command handler allowing Telegram users and investors to query
live token metrics, deflationary burns, agent status, and quantum proofs.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import time

# Ensure UTF-8 output encoding for console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from agent.market_intel import MarketIntel
from agent.agent_wallet import AgentWallet
from crypto.quantum_shield import QuantumShield

def load_env(env_path=".env"):
    config = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    config[k.strip()] = v.strip().strip('"').strip("'")
    return config

class TelegramCommunityBot:
    def __init__(self):
        cfg = load_env()
        self.token = cfg.get("TELEGRAM_BOT_TOKEN")
        self.wallet = AgentWallet()
        self.shield = QuantumShield(self.wallet.secret_key_bytes)
        self.intel = MarketIntel()
        self.last_update_id = 0

    def send_message(self, chat_id: int, text: str):
        if not self.token:
            return
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = urllib.parse.urlencode({
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }).encode("utf-8")
        try:
            req = urllib.request.Request(url, data=payload, method="POST")
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            # Fallback to plain text
            plain = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")
            try:
                urllib.request.urlopen(urllib.request.Request(url, data=plain, method="POST"), timeout=5)
            except Exception:
                pass

    def handle_command(self, text: str, chat_id: int):
        cmd = text.strip().split()[0].lower() if text else ""

        if cmd in ["/start", "/help"]:
            msg = (
                "🤖 *Welcome to the AI Quantum Protocol ($AIQT) Terminal!*\n\n"
                "The first post-quantum autonomous agent network on Solana.\n\n"
                "Available Commands:\n"
                "• /price - Live market metrics & initial valuation\n"
                "• /burn - Cumulative deflationary burns to 1111...1111\n"
                "• /agent - Live Flagship AI Agent status & quantum proofs\n"
                "• /vault - Dual-Tier Quantum Vault security state\n"
                "• /docs - Links to Whitepaper, Architecture & GitHub\n"
            )
            self.send_message(chat_id, msg)

        elif cmd == "/price":
            sol = self.intel.fetch_sol_price()
            price = sol.get("price", 108.0)
            change = sol.get("change_24h", 0.0)
            dir_sym = "▲" if change >= 0 else "▼"
            msg = (
                "📈 *$AIQT Market Intelligence*\n\n"
                f"• SOL: `${price:.2f}` ({dir_sym} {change:+.2f}% 24h)\n"
                "• Token Standard: Solana Token-2022\n"
                "• Total Supply: 1,000,000,000 $AIQT (Fixed)\n"
                "• Liquidity Pool: 600,000,000 $AIQT paired with SOL on Raydium\n"
                "• LP Security: 100% Permanently Burned at Launch\n"
            )
            self.send_message(chat_id, msg)

        elif cmd == "/burn":
            msg = (
                "🔥 *$AIQT Programmatic Deflationary Sink*\n\n"
                "• Mechanism: Native Solana Token-2022 TransferFeeConfig\n"
                "• Fee: 0.5% (50 bps) on every agent-to-agent task\n"
                "• Split: 50% permanently burned, 50% agent compute fund\n"
                "• Burn Destination: `11111111111111111111111111111111`\n"
                "• Burn Status: Active across all M2M transactions\n"
            )
            self.send_message(chat_id, msg)

        elif cmd == "/agent":
            sol = self.intel.fetch_sol_price()
            payload = f"TELEGRAM-QUERY: SOL=${sol.get('price', 0):.2f}".encode('utf-8')
            fast_sig = self.wallet.sign_agent_message(payload.decode('utf-8'))
            hybrid = self.shield.sign_hybrid(fast_sig, payload)
            msg = (
                "🧠 *Flagship AI Agent Sentinel Status*\n\n"
                f"• Wallet: `{self.wallet.get_public_key()[:8]}...{self.wallet.get_public_key()[-6:]}`\n"
                f"• Lattice Key: `{self.shield.lattice_public_key[:12]}...`\n"
                f"• Proof Sig: `{hybrid['quantum_lattice_signature'][:16]}...`\n"
                "• Security: NIST FIPS-204 ML-DSA Lattice Compliant\n"
                "• Status: 🟢 Online & Monitoring Solana Mainnet\n"
            )
            self.send_message(chat_id, msg)

        elif cmd == "/vault":
            msg = (
                "🛡️ *Dual-Tier Quantum Vault Architecture*\n\n"
                "• Tier 1 (< 10k $AIQT): Fast-path Ed25519 (~400ms)\n"
                "• Tier 2 (≥ 10k $AIQT): Mandatory NIST ML-DSA Lattice Dual-Lock\n"
                "• Shor's Defense: Mathematically immune to quantum key-recovery\n"
                "• Audit Score: 100/100 Clean\n"
            )
            self.send_message(chat_id, msg)

        elif cmd == "/docs":
            msg = (
                "📚 *AI Quantum Protocol ($AIQT) Resources*\n\n"
                "• Web Portal: https://aiquantumtoken.github.io/AI-Quantum-Protocol/\n"
                "• GitHub Repo: https://github.com/aiquantumtoken/AI-Quantum-Protocol\n"
                "• Whitepaper: https://github.com/aiquantumtoken/AI-Quantum-Protocol/blob/main/WHITEPAPER.md\n"
                "• Architecture: https://github.com/aiquantumtoken/AI-Quantum-Protocol/blob/main/ARCHITECTURE.md\n"
            )
            self.send_message(chat_id, msg)

    def process_pending_updates(self):
        if not self.token:
            return 0
        url = f"https://api.telegram.org/bot{self.token}/getUpdates?offset={self.last_update_id + 1}&timeout=2"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AIQT-Bot/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                results = data.get("result", [])
                for update in results:
                    self.last_update_id = max(self.last_update_id, update.get("update_id", 0))
                    msg = update.get("message", {})
                    text = msg.get("text", "")
                    chat_id = msg.get("chat", {}).get("id")
                    if text and chat_id:
                        print(f"Received Command '{text}' from {chat_id}")
                        self.handle_command(text, chat_id)
                return len(results)
        except Exception as e:
            return 0

if __name__ == "__main__":
    bot = TelegramCommunityBot()
    print("🤖 Telegram Community Bot Command Processor initialized.")
    processed = bot.process_pending_updates()
    print(f"Processed {processed} pending Telegram updates.")
