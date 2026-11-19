#!/bin/bash
# Установка навыков для группы Orzu Medical (macOS, Linux). Запуск: bash install.sh
set -e
SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills"
mkdir -p "$DEST"
cp -R "$SRC/skills/." "$DEST/"
echo ""
echo "Готово. Установлены навыки: $(ls "$SRC/skills" | tr '\n' ' ')"
echo "Перезапустите Claude Code и наберите /airl-dwh"
