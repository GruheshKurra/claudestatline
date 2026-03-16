# claudestatline

A minimal, curl-installable status line for [Claude Code](https://claude.ai/claude-code) that shows model, directory, context window, token usage, and a live **2x usage badge** tied to Anthropic's March 2026 promotion.

## What it shows

```
🤖 claude-sonnet-4-6 │ 📁 ~/Projects/myapp │ 💬 73% ctx │ ⚡ 142k 5h │ 📅 890k 7d │ 2x ON ·11d
```

| Segment | Meaning |
|---|---|
| 🤖 `model` | Active Claude model |
| 📁 `dir` | Current working directory (shortened) |
| 💬 `X% ctx` | Remaining context window percentage |
| 🦾 `agent` | Active sub-agent name (if any) |
| 🌿 `branch` | Current git branch (if in a worktree) |
| ⚡ `Xk 5h` | Tokens used in the last 5 hours |
| 📅 `Xk 7d` | Tokens used in the last 7 days |
| 🟢 `2x ON ·Xd` | 2x is active right now — X days left in promotion |
| 🔴 `2x OFF ·Xd` | Peak hours — 2x paused, shows time until it resumes |

## Install

```bash
curl -sSL https://raw.githubusercontent.com/GruheshKurra/claudestatline/main/install.sh | bash
```

Restart Claude Code after installing.

## Requirements

- Python 3.8+
- Claude Code CLI
- `curl`

## How it works

Three files are installed:

| File | Location | Role |
|---|---|---|
| `claudestatline` | `~/.local/bin/` | Shell wrapper — caches token scan every 5 minutes |
| `claudestatline.py` | `~/.claude/` | Reads status JSON from stdin, renders the line |
| `claudestatline-tokens.py` | `~/.claude/` | Scans `~/.claude/projects/**/*.jsonl` for token usage |

`~/.claude/settings.json` is updated to point `statusLine.command` at the wrapper. Your original settings are backed up as `settings.json.bak`.

## The 2x badge — March 2026 promotion

Anthropic's [March 2026 usage promotion](https://support.claude.com/en/articles/14063676-claude-march-2026-usage-promotion) doubles limits during off-peak hours from **March 13–27, 2026**.

**2x is ON:** all weekends + weekdays outside 8 AM–2 PM ET (5:30 PM–11:30 PM IST)
**2x is OFF:** weekdays 8 AM–2 PM ET only (5:30 PM–11:30 PM IST)

The badge:
- Shows **green `2x ON ·Xd`** when the doubled limits are active
- Shows **red `2x OFF ·Xd (on in Xh)`** during peak hours, with time until it resumes
- Disappears completely after March 27

## Uninstall

```bash
rm -f ~/.local/bin/claudestatline \
       ~/.claude/claudestatline.py \
       ~/.claude/claudestatline-tokens.py \
       ~/.claude/claudestatline-cache.json
```

Then restore your original settings:

```bash
cp ~/.claude/settings.json.bak ~/.claude/settings.json
```

## Author

[Gruhesh Sri Sai Karthik Kurra](https://github.com/GruheshKurra)
