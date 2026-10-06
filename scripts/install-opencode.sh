#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${OPENCODE_CONFIG_DIR:-$HOME/.config/opencode}"

python3 "$ROOT/scripts/sync-opencode.py"
mkdir -p "$DEST/commands" "$DEST/skills"

cp "$ROOT"/.opencode/commands/*.md "$DEST/commands/"

for skill_dir in "$ROOT"/.opencode/skills/*; do
  [ -d "$skill_dir" ] || continue
  name="$(basename "$skill_dir")"
  rm -rf "$DEST/skills/$name"
  cp -R "$skill_dir" "$DEST/skills/$name"
done

chmod +x "$ROOT"/tools/*.py "$ROOT"/tools/*.sh 2>/dev/null || true

echo "Installed opencode commands to $DEST/commands"
echo "Installed opencode skills to $DEST/skills"
echo "Restart opencode to pick up new commands and skills."
