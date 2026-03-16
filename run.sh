#!/usr/bin/env bash
CACHE_FILE="${HOME}/.claude/claudestatline-cache.json"
TOKENS_SCRIPT="${HOME}/.claude/claudestatline-tokens.py"
RENDERER_SCRIPT="${HOME}/.claude/claudestatline.py"
CACHE_TTL=300

refresh_cache() {
    python3 "${TOKENS_SCRIPT}" > "${CACHE_FILE}" 2>/dev/null
}

if [ ! -f "${CACHE_FILE}" ]; then
    refresh_cache
else
    last_mod=$(python3 -c "import os,time; print(int(time.time()-os.path.getmtime('${CACHE_FILE}')))" 2>/dev/null || echo 9999)
    if [ "${last_mod}" -gt "${CACHE_TTL}" ]; then
        refresh_cache &
    fi
fi

python3 "${RENDERER_SCRIPT}" "${CACHE_FILE}"
