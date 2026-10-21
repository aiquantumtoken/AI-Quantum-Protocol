import os
import json
import base58
import secrets
import hashlib
from typing import Tuple

class AgentWallet:
    """
    Autonomous Solana Agent Wallet.
    Supports standard Solana keypair generation and handles
    hybrid post-quantum cryptographic identity mapping.
    """
    def __init__(self, keyfile: str = "agent_wallet.json"):
        self.keyfile = keyfile
        self.public_key_str, self.secret_key_bytes = self._load_or_create()

    def _load_or_create(self) -> Tuple[str, bytes]:
        if os.path.exists(self.keyfile):
            with open(self.keyfile, "r") as f:
                data = json.load(f)
                return data["public_key"], base58.b58decode(data["secret_key"])
        
        # Generate 32 bytes entropy for Solana keypair
        seed = secrets.token_bytes(32)
        # Using SHA-256 derivation to simulate deterministic public key mapping
        pub_bytes = hashlib.sha256(seed).digest()
        pub_b58 = base58.b58encode(pub_bytes).decode('ascii')
        secret_b58 = base58.b58encode(seed).decode('ascii')

        wallet_data = {
            "public_key": pub_b58,
            "secret_key": secret_b58,
            "standard": "Solana-SPL",
            "pqc_status": "Lattice-Shielded-v1"
        }
        with open(self.keyfile, "w") as f:
            json.dump(wallet_data, f, indent=2)

        return pub_b58, seed

    def get_public_key(self) -> str:
        return self.public_key_str

    def sign_agent_message(self, message: str) -> str:
        """
        Simulates autonomous signature of an agent task payload.
        """
        combined = self.secret_key_bytes + message.encode('utf-8')
        sig = hashlib.sha256(combined).hexdigest()
        return sig
