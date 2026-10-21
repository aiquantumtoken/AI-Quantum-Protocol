import os
import sys
import urllib.request
import urllib.parse
import json

def load_env(env_path=".env"):
    config = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    config[key.strip()] = val.strip().strip('"').strip("'")
    return config

def send_telegram_message(message: str) -> bool:
    config = load_env()
    token = config.get("TELEGRAM_BOT_TOKEN")
    chat_id = config.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Error: Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=payload, method="POST")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("ok", False)
    except Exception as e:
        print(f"Failed to send telegram message: {e}")
        return False

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Test notification from your AI workspace."
    success = send_telegram_message(msg)
    if success:
        print("Message sent successfully!")
    else:
        sys.exit(1)
