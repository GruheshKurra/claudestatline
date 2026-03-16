#!/usr/bin/env python3
import json, sys, os
from datetime import datetime, timezone, timedelta, date

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)

def get(obj, *keys):
    for k in keys:
        if not isinstance(obj, dict):
            return None
        obj = obj.get(k)
    return obj

model  = get(payload, "model", "display_name") or ""
cwd    = get(payload, "workspace", "current_dir") or ""
ctx    = get(payload, "context_window", "remaining_percentage")
agent  = get(payload, "agent", "name") or ""
branch = get(payload, "worktree", "branch") or ""
vim    = get(payload, "vim", "mode") or ""

home = os.path.expanduser("~")
if cwd == home:
    short_cwd = "~"
elif cwd.startswith(home + "/"):
    tail = cwd[len(home) + 1:].split("/")
    short_cwd = "~/" + "/".join(tail[-2:]) if len(tail) > 1 else "~/" + tail[0]
elif cwd:
    parts = cwd.split("/")
    short_cwd = "/".join(parts[-2:]) if len(parts) > 1 else (parts[-1] or cwd)
else:
    short_cwd = ""

cache_path = sys.argv[1] if len(sys.argv) > 1 else ""
five_h_used = seven_d_used = None
five_h_resets_in = seven_d_resets_in = ""

if cache_path and os.path.isfile(cache_path):
    try:
        cached = json.load(open(cache_path))
        if "error" not in cached:
            five_h_used       = cached.get("five_h_used")
            seven_d_used      = cached.get("seven_d_used")
            five_h_resets_in  = cached.get("five_h_resets_in", "")
            seven_d_resets_in = cached.get("seven_d_resets_in", "")
    except Exception:
        pass

GREEN = "\033[32m"
YELLOW= "\033[33m"
RED   = "\033[31m"
RESET = "\033[0m"

def usage_color(used):
    if used is None:
        return ""
    if used < 50:
        return GREEN
    if used < 80:
        return YELLOW
    return RED

def fmt_usage(used, resets_in, label):
    if used is None:
        return ""
    color = usage_color(used)
    reset_part = f" ·{resets_in}" if resets_in else ""
    return f"{color}{used}%{RESET} {label}{reset_part}"

EDT = timezone(timedelta(hours=-4))
now_edt = datetime.now(EDT)

PROMO_START = datetime(2026, 3, 13, 0, 0, 0, tzinfo=EDT)
PROMO_END   = datetime(2026, 3, 28, 0, 0, 0, tzinfo=EDT)

in_promo = PROMO_START <= now_edt < PROMO_END

if in_promo:
    days_left = (date(2026, 3, 27) - now_edt.date()).days
    days_str = f"·{days_left}d" if days_left > 0 else "·ends today"

    is_weekday = now_edt.weekday() < 5
    is_peak    = is_weekday and (8 <= now_edt.hour < 14)

    if is_peak:
        resume_edt = datetime(now_edt.year, now_edt.month, now_edt.day, 14, 0, tzinfo=EDT)
        mins_left  = int((resume_edt - now_edt).total_seconds() // 60)
        wait_str   = f"{mins_left // 60}h{mins_left % 60:02d}m" if mins_left >= 60 else f"{mins_left}m"
        two_x_badge = f"{RED}2x OFF{RESET} {days_str} (on in {wait_str})"
    else:
        two_x_badge = f"{GREEN}2x ON{RESET} {days_str}"
else:
    two_x_badge = ""

five_h_str  = fmt_usage(five_h_used, five_h_resets_in, "5h")
seven_d_str = fmt_usage(seven_d_used, seven_d_resets_in, "7d")

segments = []
if model:           segments.append(f"🤖 {model}")
if short_cwd:       segments.append(f"📁 {short_cwd}")
if ctx is not None: segments.append(f"💬 {int(ctx)}% ctx")
if agent:           segments.append(f"🦾 {agent}")
if branch:          segments.append(f"🌿 {branch}")
if vim:             segments.append(f"[{vim}]")
if five_h_str:      segments.append(f"⚡ {five_h_str}")
if seven_d_str:     segments.append(f"📅 {seven_d_str}")
if two_x_badge:     segments.append(two_x_badge)

print(" │ ".join(segments))
