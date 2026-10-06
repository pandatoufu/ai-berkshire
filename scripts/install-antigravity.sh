#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Antigravity supports workspace .agents/ natively.
# For global availability across any workspace, install into ~/.gemini/config/skills:
DEST="${AGY_SKILLS_DIR:-$HOME/.gemini/config/skills}"

python3 "$ROOT/scripts/sync-antigravity.py"
mkdir -p "$DEST"

for skill_dir in "$ROOT"/.agents/skills/*; do
  [ -d "$skill_dir" ] || continue
  name="$(basename "$skill_dir")"
  rm -rf "$DEST/$name"
  cp -R "$skill_dir" "$DEST/$name"
done

chmod +x "$ROOT"/tools/financial_rigor.py "$ROOT"/tools/report_audit.py "$ROOT"/tools/*.sh "$ROOT"/scripts/*.py "$ROOT"/scripts/*.sh 2>/dev/null || true

echo "✓ Antigravity workspace skills synchronized in $ROOT/.agents/skills"
echo "✓ Antigravity global skills installed to $DEST"
echo "Note: Antigravity IDE and agy CLI will automatically discover project skills in .agents/"
