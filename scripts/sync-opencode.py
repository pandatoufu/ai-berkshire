#!/usr/bin/env python3
"""Generate opencode commands and skills from AI Berkshire skill sources.

The canonical workflow lives in `skills/*.md` (Claude Code command sources).
This script adapts each one for opencode:

- `.opencode/commands/<name>.md`     slash-command entry points (`/<name>`)
- `.opencode/skills/<name>/SKILL.md` on-demand agent skills

Run with `--check` to verify generated artifacts are current without writing.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
OPENCODE = ROOT / ".opencode"
COMMANDS = OPENCODE / "commands"
OPENCODE_SKILLS = OPENCODE / "skills"


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


def adapter_note(source_name: str) -> str:
    return (
        "## opencode adapter note\n\n"
        f"This workflow is generated from `skills/{source_name}`; the canonical "
        "source is shared by Claude Code, Codex, and opencode.\n\n"
        "- `$ARGUMENTS` is the user's request in this session.\n"
        "- Map Claude-only tool names to opencode tools: Task/Agent → the `task` "
        "tool (subagents), WebSearch/WebFetch → `websearch`/`webfetch`, "
        "Bash → `bash`, Read/Write/Edit → `read`/`write`/`edit`.\n"
        "- Run shared project tools from the repository root, e.g. "
        "`python3 tools/financial_rigor.py ...`.\n"
        "- Run the `date` command first to confirm today's date, and state the "
        "data cutoff date in the report header.\n\n"
    )


def body_for(source_text: str) -> str:
    _, body = split_frontmatter(source_text)
    return body.rstrip() + "\n"


def command_content(source: Path, source_text: str) -> str:
    name = source.stem
    title = first_heading(source_text, name)
    description = f"AI Berkshire 投研工作流：{title}"
    return (
        "---\n"
        f"description: {yaml_quote(description)}\n"
        "agent: build\n"
        "---\n\n"
        + adapter_note(source.name)
        + body_for(source_text)
    )


def skill_content(source: Path, source_text: str) -> str:
    name = source.stem
    title = first_heading(source_text, name)
    description = (
        f"AI Berkshire 投研工作流：{title}。"
        f"当用户要求该工作流或输入 /{name} 时使用。"
    )
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {yaml_quote(description)}\n"
        "---\n\n"
        + adapter_note(source.name)
        + body_for(source_text)
    )


def main() -> None:
    check = "--check" in sys.argv[1:]
    unknown_args = [arg for arg in sys.argv[1:] if arg != "--check"]
    if unknown_args:
        joined = ", ".join(unknown_args)
        raise SystemExit(f"Unknown argument(s): {joined}")

    if not check:
        COMMANDS.mkdir(parents=True, exist_ok=True)
        OPENCODE_SKILLS.mkdir(parents=True, exist_ok=True)

    count = 0
    stale: list[str] = []
    for source in sorted(SKILLS.glob("*.md")):
        name = source.stem
        source_text = source.read_text(encoding="utf-8")

        targets = [
            (COMMANDS / f"{name}.md", command_content(source, source_text)),
            (OPENCODE_SKILLS / name / "SKILL.md", skill_content(source, source_text)),
        ]

        for target, content in targets:
            if check:
                if not target.exists() or target.read_text(encoding="utf-8") != content:
                    stale.append(str(target.relative_to(ROOT)))
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
        count += 1

    if check:
        if stale:
            print("opencode artifacts are out of date:")
            for path in stale:
                print(f"  {path}")
            raise SystemExit(1)
        print(f"Checked {count} opencode commands and skills in {OPENCODE.relative_to(ROOT)}")
        return

    print(f"Generated {count} opencode commands in {COMMANDS.relative_to(ROOT)}")
    print(f"Generated {count} opencode skills in {OPENCODE_SKILLS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
