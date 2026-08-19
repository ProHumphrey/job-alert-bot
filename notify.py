"""
Sends a push notification via ntfy.sh (free, no account needed).

Setup (one-time, on your iPhone):
  1. Install the "ntfy" app from the App Store.
  2. Open it, tap "+", subscribe to the exact topic name you set in
     config.NTFY_TOPIC (treat it like a secret password — anyone who knows
     the topic name can subscribe to your alerts).
  3. That's it. This script POSTs to https://ntfy.sh/<topic> and the app
     pushes it straight to your lock screen.
"""
import requests
import config


def send(title: str, body: str, url: str = None):
    headers = {
        "Title": title.encode("utf-8"),
        "Priority": "high",
        "Tags": "briefcase",
    }
    if url:
        headers["Click"] = url

    try:
        requests.post(
            f"https://ntfy.sh/{config.NTFY_TOPIC}",
            data=body.encode("utf-8"),
            headers=headers,
            timeout=15,
        )
    except requests.RequestException as e:
        print(f"[notify] failed to send push: {e}")
