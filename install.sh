#!/usr/bin/env bash
set -e

REPO="https://raw.githubusercontent.com/GruheshKurra/claudestatline/main"
CLAUDE_DIR="${HOME}/.claude"
BIN_DIR="${HOME}/.local/bin"
SETTINGS="${CLAUDE_DIR}/settings.json"

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; NC='\033[0m'

log()  { echo -e "${CYAN}[claudestatline]${NC} $1"; }
ok()   { echo -e "${GREEN}[claudestatline]${NC} $1"; }
fail() { echo -e "${RED}[claudestatline]${NC} $1"; exit 1; }

command -v python3 &>/dev/null || fail "python3 is required but not found"
command -v curl   &>/dev/null || fail "curl is required but not found"

mkdir -p "${CLAUDE_DIR}" "${BIN_DIR}"

log "Downloading statusline renderer..."
curl -sSLf "${REPO}/statusline.py" -o "${CLAUDE_DIR}/claudestatline.py" \
    || fail "Failed to download statusline.py — check your internet connection"
chmod +x "${CLAUDE_DIR}/claudestatline.py"

log "Downloading token usage script..."
curl -sSLf "${REPO}/tokens.py" -o "${CLAUDE_DIR}/claudestatline-tokens.py" \
    || fail "Failed to download tokens.py"
chmod +x "${CLAUDE_DIR}/claudestatline-tokens.py"

log "Downloading run script..."
curl -sSLf "${REPO}/run.sh" -o "${BIN_DIR}/claudestatline" \
    || fail "Failed to download run.sh"
chmod +x "${BIN_DIR}/claudestatline"

if [ -f "${SETTINGS}" ]; then
    cp "${SETTINGS}" "${SETTINGS}.bak" \
        || fail "Could not back up settings.json (check permissions on ${SETTINGS})"
    log "Backed up existing settings to ${SETTINGS}.bak"
fi

if command -v python3 &>/dev/null && python3 -c "import json" &>/dev/null; then
    python3 - <<'PYEOF'
import json, os, sys

settings_path = os.path.expanduser("~/.claude/settings.json")
bin_path = os.path.expanduser("~/.local/bin/claudestatline")

if os.path.isfile(settings_path):
    with open(settings_path) as f:
        data = json.load(f)
else:
    data = {}

data["statusLine"] = {"type": "command", "command": bin_path}

with open(settings_path, "w") as f:
    json.dump(data, f, indent=2)

print("Updated settings.json")
PYEOF
else
    fail "Could not update settings.json — update it manually: set statusLine.command to ${BIN_DIR}/claudestatline"
fi

ok "Installation complete!"
ok "Restart Claude Code to see the updated status line."
echo ""
echo "  Status line will show:"
echo "  🤖 model │ 📁 dir │ 💬 ctx% │ ⚡ 19% 5h ·18m │ 📅 36% 7d ·20h │ 2x ON ·11d"
echo ""
echo "  Usage % = amount used (green <50%, yellow <80%, red ≥80%)"
echo "  2x badge is live during Anthropic's March 2026 promotion (ends Mar 27)."
