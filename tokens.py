#!/usr/bin/env python3
import json, subprocess, time, sys
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError

USAGE_URL = "https://api.anthropic.com/api/oauth/usage"
BETA_HEADER = "oauth-2025-04-20"


def get_token():
    try:
        raw = subprocess.check_output(
            ["security", "find-generic-password", "-s", "Claude Code-credentials", "-w"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        creds = json.loads(raw)
        return creds["claudeAiOauth"]["accessToken"]
    except Exception:
        return None


def time_until(iso_str):
    try:
        target = datetime.fromisoformat(iso_str)
        now = datetime.now(timezone.utc)
        secs = int((target - now).total_seconds())
        if secs <= 0:
            return "now"
        h, m = divmod(secs // 60, 60)
        if h > 0:
            return f"{h}h{m:02d}m"
        return f"{m}m"
    except Exception:
        return "?"


token = get_token()

if not token:
    print(json.dumps({"error": "no_token", "ts": time.time()}))
    sys.exit(0)

try:
    req = Request(
        USAGE_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "anthropic-beta": BETA_HEADER,
        }
    )
    with urlopen(req, timeout=3) as resp:
        data = json.loads(resp.read())

    five_h  = data.get("five_hour") or {}
    seven_d = data.get("seven_day") or {}

    five_h_used  = five_h.get("utilization") or 0
    seven_d_used = seven_d.get("utilization") or 0

    five_h_used_pct  = round(five_h_used)
    seven_d_used_pct = round(seven_d_used)

    print(json.dumps({
        "five_h_used":       five_h_used_pct,
        "seven_d_used":      seven_d_used_pct,
        "five_h_resets_in":  time_until(five_h.get("resets_at", "")),
        "seven_d_resets_in": time_until(seven_d.get("resets_at", "")),
        "ts": time.time(),
    }))

except (URLError, Exception):
    print(json.dumps({"error": "api_fail", "ts": time.time()}))
