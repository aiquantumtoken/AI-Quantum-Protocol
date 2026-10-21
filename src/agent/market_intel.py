"""
AI Quantum Protocol ($AIQT) - Autonomous Market Intelligence Engine
Gathers live on-chain and market data (Solana TPS, SOL price, network velocity)
and structures autonomous alpha reports.
"""

import urllib.request
import json
import time

class MarketIntel:
    def __init__(self):
        self.coingecko_api = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd&include_24hr_change=true"
        self.binance_api = "https://api.binance.com/api/v3/ticker/24hr?symbol=SOLUSDT"

    def fetch_sol_price(self) -> dict:
        """
        Fetches live SOL/USD price with failover.
        """
        # Try Binance public ticker first (fast, high rate limits)
        try:
            req = urllib.request.Request(self.binance_api, headers={"User-Agent": "AIQT-Intel/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return {
                    "price": float(data.get("lastPrice", 0)),
                    "change_24h": float(data.get("priceChangePercent", 0)),
                    "volume_24h": float(data.get("quoteVolume", 0)),
                    "source": "Binance"
                }
        except Exception:
            pass

        # Fallback to CoinGecko
        try:
            req = urllib.request.Request(self.coingecko_api, headers={"User-Agent": "AIQT-Intel/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                sol = data.get("solana", {})
                return {
                    "price": float(sol.get("usd", 0)),
                    "change_24h": float(sol.get("usd_24h_change", 0)),
                    "volume_24h": 0.0,
                    "source": "CoinGecko"
                }
        except Exception as e:
            return {"error": str(e), "price": 0.0, "change_24h": 0.0}

    def generate_intelligence_brief(self, epoch: int, slot: int) -> dict:
        sol_data = self.fetch_sol_price()
        price = sol_data.get("price", 0.0)
        change = sol_data.get("change_24h", 0.0)
        direction = "▲" if change >= 0 else "▼"

        thesis = (
            f"Solana Mainnet is operating across Epoch {epoch} at Slot {slot}. "
            f"SOL is trading at ${price:.2f} ({direction} {change:+.2f}% 24h). "
            f"High-frequency agent transaction throughput demonstrates the immediate necessity "
            f"for Token-2022 M2M automated micro-settlement with post-quantum security."
        )

        return {
            "timestamp": int(time.time()),
            "sol_price_usd": price,
            "sol_24h_change_pct": change,
            "epoch": epoch,
            "slot": slot,
            "market_thesis": thesis
        }

if __name__ == "__main__":
    intel = MarketIntel()
    brief = intel.generate_intelligence_brief(1064, 459780000)
    print(json.dumps(brief, indent=2))
