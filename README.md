# claudestatline

A lightweight, curl-installable status line for [Claude Code](https://claude.ai/claude-code).

Shows your active model, working directory, context window, **live usage limits** (pulled directly from Anthropic's API), and a real-time **2x promotion badge** for the March 2026 usage promotion.

---

## Preview

```
🤖 claude-sonnet-4-6 │ 📁 ~/Projects/myapp │ 💬 73% ctx │ ⚡ 19% 5h ·18m │ 📅 36% 7d ·20h │ 2x ON ·11d
```

| Segment | Meaning |
|---|---|
| 🤖 `model` | Active Claude model |
| 📁 `dir` | Current working directory (last 2 path parts) |
| 💬 `X% ctx` | Context window remaining |
| 🦾 `agent` | Active sub-agent name (when running) |
| 🌿 `branch` | Current git branch (when in a worktree) |
| ⚡ `19% 5h ·18m` | 5-hour usage used · resets in 18m |
| 📅 `36% 7d ·20h` | 7-day usage used · resets in 20h |
| 🟢 `2x ON ·11d` | 2x promotion active, 11 days left |
| 🔴 `2x OFF ·Xd` | Peak hours (2x paused), shows time until it resumes |

**Usage % colors:** green < 50% · yellow < 80% · red ≥ 80%

---

## Install

```bash
curl -sSLf https://raw.githubusercontent.com/GruheshKurra/claudestatline/main/install.sh | bash
```

Then **restart Claude Code**.

### Requirements

- macOS (uses Keychain to read your Claude Code auth token)
- Python 3.8+
- Claude Code CLI with an active login

---

## How it works

Three files are installed into `~/.claude/` and `~/.local/bin/`:

| File | Installed to | Role |
|---|---|---|
| `run.sh` | `~/.local/bin/claudestatline` | Shell wrapper — manages the 5-min cache refresh |
| `statusline.py` | `~/.claude/claudestatline.py` | Reads Claude Code's status JSON from stdin, renders the line |
| `tokens.py` | `~/.claude/claudestatline-tokens.py` | Fetches live usage data from Anthropic's API |

`~/.claude/settings.json` is updated to point `statusLine.command` at the wrapper. Your original settings are backed up as `settings.json.bak`.

### Usage data

Usage limits are fetched directly from `https://api.anthropic.com/api/oauth/usage` using your Claude Code OAuth token (read from the macOS Keychain — no token is stored or hardcoded). Results are cached for 5 minutes and refreshed in the background so the status line never blocks.

---

## The 2x badge — March 2026 promotion

Anthropic's [March 2026 usage promotion](https://support.claude.com/en/articles/14063676-claude-march-2026-usage-promotion) doubles usage limits during off-peak hours from **March 13–27, 2026**.

| When | Badge |
|---|---|
| Weekends + weekdays outside 8 AM–2 PM ET | `🟢 2x ON ·Xd` |
| Weekdays 8 AM–2 PM ET (peak hours) | `🔴 2x OFF ·Xd (on in Xh)` |
| After March 27, 2026 | Badge disappears |

> For users in IST: peak hours are **5:30 PM – 11:30 PM IST** on weekdays.

---

## Uninstall

```bash
rm -f ~/.local/bin/claudestatline \
       ~/.claude/claudestatline.py \
       ~/.claude/claudestatline-tokens.py \
       ~/.claude/claudestatline-cache.json
cp ~/.claude/settings.json.bak ~/.claude/settings.json
```

---

## Author

[Gruhesh Sri Sai Karthik Kurra](https://github.com/GruheshKurra)
