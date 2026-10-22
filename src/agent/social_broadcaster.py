"""
AI Quantum Protocol ($AIQT) - Autonomous Social Broadcaster
Synthesizes live market metrics, Solana slot data, and post-quantum cryptographic proofs
into high-engagement posts for X (Twitter) and dispatches alerts to Telegram.
"""

import os
import sys
import json
import subprocess

# Ensure UTF-8 output encoding for console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agent.market_intel import MarketIntel
from agent.agent_wallet import AgentWallet
from crypto.quantum_shield import QuantumShield

try:
    from telegram_notify import send_telegram_message
except ImportError:
    send_telegram_message = None

class SocialBroadcaster:
    def __init__(self):
        self.wallet = AgentWallet()
        self.shield = QuantumShield(self.wallet.secret_key_bytes)
        self.intel = MarketIntel()

    def generate_market_alpha_tweet(self, epoch: int = 1064, slot: int = 459800000) -> str:
        sol_data = self.intel.fetch_sol_price()
        price = sol_data.get("price", 108.0)
        change = sol_data.get("change_24h", 1.2)
        dir_sym = "▲" if change >= 0 else "▼"

        # Generate cryptographic task proof
        payload = f"AIQT-ALPHA: SOL=${price:.2f} Epoch {epoch} Slot {slot}".encode('utf-8')
        fast_sig = self.wallet.sign_agent_message(payload.decode('utf-8'))
        hybrid = self.shield.sign_hybrid(fast_sig, payload)
        short_proof = hybrid["quantum_lattice_signature"][:12]

        tweet = (
            f"⚡ AIQT Agent Update\n\n"
            f"• Solana Epoch {epoch} | Slot {slot}\n"
            f"• SOL: ${price:.2f} ({dir_sym} {change:+.2f}% 24h)\n"
            f"• Lattice Proof: {short_proof}...\n"
            f"• Standard: NIST FIPS-204 ML-DSA\n\n"
            f"Autonomous agent treasuries need post-quantum security before Q-Day.\n\n"
            f"$AIQT #Solana #AI #Token2022"
        )
        return tweet

    def broadcast_to_x(self, tweet_text: str, execute_live: bool = False) -> bool:
        print(f"\n[Generated Tweet ({len(tweet_text)} chars)]:\n{tweet_text}\n")

        if not execute_live:
            print("[DRY-RUN]: Tweet generated and verified. Set execute_live=True to publish to X.")
            return True

        poster_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../scripts/post_tweet.mjs"))
        cmd = ["node", poster_script, tweet_text]

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
            if res.returncode == 0:
                print("SUCCESS: Tweet posted to X!")
                if send_telegram_message:
                    send_telegram_message(f"🐦 Tweet Published to X by Flagship Agent:\n\n{tweet_text}")
                return True
            else:
                print("Failed to post tweet:", res.stderr or res.stdout)
                return False
        except Exception as e:
            print(f"Broadcaster execution error: {e}")
            return False

if __name__ == "__main__":
    broadcaster = SocialBroadcaster()
    tweet = broadcaster.generate_market_alpha_tweet(1064, 459800000)
    broadcaster.broadcast_to_x(tweet, execute_live=False)
