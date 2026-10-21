import os
import json
import urllib.request
import urllib.parse

# Twitter Web App Public Bearer Token (constant across all web clients)
TWITTER_BEARER = "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

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

def verify_x_session():
    cfg = load_env()
    auth_token = cfg.get("X_AUTH_TOKEN")
    ct0 = cfg.get("X_CT0")

    if not auth_token or not ct0:
        print("Missing X credentials in .env")
        return None

    # Test standard verify credentials endpoint
    url = "https://api.twitter.com/1.1/account/verify_credentials.json"
    headers = {
        "Authorization": f"Bearer {TWITTER_BEARER}",
        "x-csrf-token": ct0,
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-active-user": "yes",
        "Cookie": f"auth_token={auth_token}; ct0={ct0}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }

    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            screen_name = data.get("screen_name")
            print(f"Verified X Account: @{screen_name}")
            return screen_name
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8', errors='ignore')[:300]}")
        return None
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

if __name__ == "__main__":
    verify_x_session()
