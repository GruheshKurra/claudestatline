#!/usr/bin/env python3
import json, glob, os, time
from datetime import datetime, timedelta, timezone

now = datetime.now(timezone.utc)
windows = {
    "5h": now - timedelta(hours=5),
    "7d": now - timedelta(days=7),
}
totals = {"5h": 0, "7d": 0}

COUNTED_FIELDS = ("input_tokens", "output_tokens", "cache_creation_input_tokens")

for path in glob.glob(os.path.expanduser("~/.claude/projects/**/*.jsonl"), recursive=True):
    try:
        with open(path) as f:
            for raw in f:
                try:
                    entry = json.loads(raw.strip())
                    ts_raw = entry.get("timestamp")
                    usage = entry.get("message", {}).get("usage", {})
                    if not usage or not ts_raw:
                        continue
                    if isinstance(ts_raw, str):
                        ts = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
                    else:
                        ts = datetime.fromtimestamp(ts_raw / 1000, tz=timezone.utc)
                    tokens = sum(usage.get(k, 0) or 0 for k in COUNTED_FIELDS)
                    for label, cutoff in windows.items():
                        if ts > cutoff:
                            totals[label] += tokens
                except Exception:
                    pass
    except Exception:
        pass


def compact(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}k"
    return str(n)


print(json.dumps({
    "tokens_5h": totals["5h"],
    "tokens_7d": totals["7d"],
    "fmt_5h": compact(totals["5h"]),
    "fmt_7d": compact(totals["7d"]),
    "ts": time.time(),
}))
