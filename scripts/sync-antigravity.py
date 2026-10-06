#!/usr/bin/env python3
"""Generate Antigravity skills from AI Berkshire canonical skill sources.

The canonical workflow lives in `skills/*.md` (Claude Code command sources).
This script adapts each one for Antigravity AI Agent (agy CLI, Antigravity IDE, Antigravity 2.0):

- `.agents/skills/<name>/SKILL.md` on-demand agent skills

Run with `--check` to verify generated artifacts are current without writing.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAUDE_SKILLS = ROOT / "skills"
AGENTS_DIR = ROOT / ".agents"
AGENTS_SKILLS = AGENTS_DIR / "skills"
CODEX_SKILLS = ROOT / "codex-skills"


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5 :].lstrip("\n")


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def yaml_quote(value: str) -> str:
    value = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{value}"'


def metadata_for(name: str, source_name: str, source_text: str) -> str:
    existing, body = split_frontmatter(source_text)
    if existing:
        has_name = re.search(r"(?m)^name:\s*", existing) is not None
        has_description = re.search(r"(?m)^description:\s*", existing) is not None
        lines = []
        if not has_name:
            lines.append(f"name: {name}")
        if not has_description:
            title = first_heading(body, name)
            lines.append(
                "description: "
                + yaml_quote(
                    f"AI Berkshire 投资研究工作流：{title}。当用户需要执行该分析或请求相关研究时激活。"
                )
            )
        lines.append(existing.rstrip())
        return "---\n" + "\n".join(lines) + "\n---\n\n"

    title = first_heading(source_text, name)
    description = (
        f"AI Berkshire 投资研究工作流：{title}。当用户需要执行该分析或请求相关研究时激活。"
    )
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {yaml_quote(description)}\n"
        "---\n\n"
    )


def antigravity_body(name: str, source_name: str, source_text: str) -> str:
    _, body = split_frontmatter(source_text)
    note = (
        "## Antigravity adapter note\n\n"
        f"This skill is generated from `skills/{source_name}` for Antigravity AI Agent "
        "(agy CLI, Antigravity IDE, Antigravity 2.0).\n\n"
        "- Treat `$ARGUMENTS` as the user's research request in the current Antigravity session.\n"
        "- Map general agent capabilities to Antigravity tools:\n"
        "  - Subagents: Use `invoke_subagent` (e.g. `research` subagent for deep web/data dives, "
        "`self` for isolated sub-tasks) for parallel execution.\n"
        "  - Terminal / scripts: Use `run_command` with bash to execute local validation tools.\n"
        "  - File operations: Use `view_file` to inspect files, `replace_file_content` for surgical updates, "
        "and `write_to_file` to create report files.\n"
        "  - Web research: Use `search_web` and `read_url_content` (or configured MCP scrapers like Firecrawl).\n"
        "  - Interactive clarification: Use `ask_question` when clarification is needed on ticker, market, or scope.\n"
        "- Use shared project tools from `tools/` in this repository:\n"
        "  - Run `python3 tools/financial_rigor.py ...` for exact valuation and financial arithmetic.\n"
        "  - Run `python3 tools/report_audit.py ...` to verify completed research reports.\n"
        "  - Run `python3 tools/reports_index.py` before finalizing new reports.\n"
        "- Before starting research, run the `date` command to confirm today's date; "
        "treat it as the baseline for \"latest\" data and state the data cutoff date in the report header.\n"
        "- Preserve research quality: cross-check key financial metrics with at least 2 independent sources, "
        "rigorously separate facts from opinions, and explicitly state uncertainties.\n\n"
    )
    return note + body.rstrip() + "\n"


def sync_memo_craft_skill(check: bool, stale: list[str]) -> None:
    source_memo = CODEX_SKILLS / "investment-memo-craft" / "SKILL.md"
    if not source_memo.exists():
        return
    target_dir = AGENTS_SKILLS / "investment-memo-craft"
    target = target_dir / "SKILL.md"
    source_text = source_memo.read_text(encoding="utf-8")
    
    # Adapt note for Antigravity
    content = source_text.replace(
        "Codex-only writing and layout overlay",
        "Writing and layout overlay for Antigravity and Codex",
    ).replace(
        "Turn investment research into a decision-ready Codex research report.",
        "Turn investment research into a decision-ready research report for Antigravity AI Agent.",
    )

    if check:
        if not target.exists() or target.read_text(encoding="utf-8") != content:
            stale.append(str(target.relative_to(ROOT)))
    else:
        target_dir.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def main() -> None:
    check = "--check" in sys.argv[1:]
    unknown_args = [arg for arg in sys.argv[1:] if arg != "--check"]
    if unknown_args:
        joined = ", ".join(unknown_args)
        raise SystemExit(f"Unknown argument(s): {joined}")

    if not check:
        AGENTS_SKILLS.mkdir(parents=True, exist_ok=True)

    count = 0
    stale: list[str] = []
    for source in sorted(CLAUDE_SKILLS.glob("*.md")):
        name = source.stem
        source_text = source.read_text(encoding="utf-8")
        target_dir = AGENTS_SKILLS / name
        target = target_dir / "SKILL.md"
        content = metadata_for(name, source.name, source_text) + antigravity_body(
            name, source.name, source_text
        )
        if check:
            if not target.exists() or target.read_text(encoding="utf-8") != content:
                stale.append(str(target.relative_to(ROOT)))
        else:
            target_dir.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        count += 1

    # Also handle investment-memo-craft overlay skill
    sync_memo_craft_skill(check, stale)
    if not check or not stale:
        count += 1

    if check:
        if stale:
            print("Antigravity skills are out of date:")
            for path in stale:
                print(f"  {path}")
            raise SystemExit(1)
        print(f"Checked {count} Antigravity skills in {AGENTS_SKILLS.relative_to(ROOT)}")
        return

    print(f"Generated {count} Antigravity skills in {AGENTS_SKILLS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
