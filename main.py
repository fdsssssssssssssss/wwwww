import time
import requests
from datetime import datetime

GAME_URL = "https://www.roblox.com/games/124120394261371/Dollhouse-Roleplay-Modded-BACK"

# Replace with your Discord webhook URL
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1411677477260234752/E1ZP2u57kQ8O6WHTawNUDtEwUPiCvF_GVGxoz_QUWttaBS5qAr4qgRPEqes7EDT4-7FL"

def send_discord_message(message: str):
    try:
        payload = {"content": message}
        response = requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
        if response.status_code != 204:
            print(f"[ERROR] Failed to send webhook: {response.status_code} {response.text}")
    except requests.RequestException as e:
        print(f"[ERROR] Could not send webhook: {e}")

def check_game_status():
    try:
        response = requests.get(GAME_URL, allow_redirects=True, timeout=10)
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        if "/games/check/" in response.url or response.status_code == 404:
            msg = f"🚨 [BANNED] Game taken down at {timestamp}\nRedirected to: {response.url}"
            print(msg)
            send_discord_message(msg)
        elif response.status_code == 200:
            print(f"[ACTIVE] {timestamp} - Game is still available.")
        else:
            print(f"[UNKNOWN] {timestamp} - Status {response.status_code} at {response.url}")

    except requests.RequestException as e:
        print(f"[ERROR] Could not check game status: {e}")

if __name__ == "__main__":
    while True:
        check_game_status()
        time.sleep(10)  # wait 10 seconds
