#!/usr/bin/env bash
# Pre-commit-msg hook: scan staged files for items that should NOT be in version control.
# Fires on `git diff --cached*` (the first command the tw-emoji-commit skill runs).
# Non-blocking: injects a warning via hookSpecificOutput.additionalContext so Claude
# can confirm with the user before drafting the commit message.

set -u

# Drain stdin (PreToolUse payload) so the hook input pipe doesn't SIGPIPE — we don't need it.
cat >/dev/null 2>&1 || true

staged="$(git diff --cached --name-only 2>/dev/null)"
[ -z "$staged" ] && exit 0

# Patterns for files that almost certainly should NOT be in version control.
# Each line is an extended regex matched against the file path.
patterns=$(cat <<'PATTERNS'
(^|/)\.env($|\.)
(^|/)\.envrc$
\.pem$
\.key$
(^|/)id_rsa($|\.)
(^|/)id_ed25519($|\.)
(^|/)id_ecdsa($|\.)
\.p12$
\.pfx$
(^|/)secrets?\.(json|ya?ml|toml|ini)$
(^|/)credentials?\.(json|ya?ml|toml|ini)$
(^|/)\.aws/credentials$
(^|/)\.npmrc$
(^|/)\.pypirc$
(^|/)\.netrc$
\.sqlite3?$
(^|/)node_modules/
(^|/)\.venv/
(^|/)__pycache__/
\.pyc$
(^|/)\.DS_Store$
(^|/)Thumbs\.db$
(^|/)\.idea/
(^|/)\.vscode/settings\.json$
\.log$
PATTERNS
)

flagged=""
while IFS= read -r f; do
  [ -z "$f" ] && continue
  while IFS= read -r p; do
    [ -z "$p" ] && continue
    if echo "$f" | grep -qE "$p"; then
      flagged+="  - $f  (matched: $p)"$'\n'
      break
    fi
  done <<< "$patterns"
done <<< "$staged"

if [ -n "$flagged" ]; then
  msg="⚠️ 偵測到 staged 檔案中可能不該進入版本控制的項目：

${flagged}
請在產生 commit message 前，**先用 AskUserQuestion 詢問使用者**：
  1) 從 staging 移除這些檔案（git restore --staged <file>）並加入 .gitignore；或
  2) 確認確實要納入版本控制，繼續產生 commit message。

未獲使用者確認前，請勿直接產生 commit message。"

  jq -n --arg ctx "$msg" '{
    "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "additionalContext": $ctx
    }
  }'
fi

exit 0
