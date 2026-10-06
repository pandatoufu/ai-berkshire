# AI Berkshire Agent Guide

This repository contains investment research workflows, reports, and shared
validation tools. Keep compatibility with Claude Code, Codex, opencode, and
Antigravity AI Agent users.

## Project Layout

- `skills/*.md`: Claude Code slash-command source files. This is the canonical
  workflow source for every client.
- `.agents/skills/*/SKILL.md`: Antigravity skill packages, generated from
  `skills/*.md` for Antigravity AI Agent (`agy` CLI, Antigravity IDE, Antigravity 2.0).
- `.agents/rules/*.md`: Antigravity modular workspace rules (research rigor,
  financial validation, report guidelines).
- `.agents/skills.json`: Antigravity skills registration manifest.
- `codex-skills/*/SKILL.md`: Codex skill packages. Most are generated from
  `skills/*.md`; Codex-only hand-written packages are allowed when clearly
  marked and no same-named `skills/*.md` source exists.
- `codex-prompts/*.md`: generated Codex custom prompts for slash-command
  style entry points. These are a compatibility layer; skills remain preferred.
- `.opencode/commands/*.md`: generated opencode slash commands (`/<name>`),
  adapted from `skills/*.md`.
- `.opencode/skills/*/SKILL.md`: generated opencode agent skills, adapted from
  `skills/*.md`.
- `opencode.json`: opencode project config. It loads `CLAUDE.md` as an extra
  instruction file alongside the auto-loaded `AGENTS.md`.
- `tools/*.py`: shared financial validation and data tools used by all systems.
- `reports/`: research outputs. Do not rewrite unrelated reports while changing
  tooling or skills.
- `scripts/sync-antigravity.py`: regenerates Antigravity skills from `skills/*.md`.
- `scripts/sync-codex-skills.py`: regenerates Codex skills from `skills/*.md`.
- `scripts/sync-opencode.py`: regenerates opencode commands and skills from
  `skills/*.md`.
- `scripts/install-antigravity.sh` / `scripts/install-antigravity.bat`:
  installs Antigravity skills locally.
- `scripts/install-codex-skills.sh` / `scripts/install-codex-skills.bat`:
  installs Codex skills locally.
- `scripts/install-codex-prompts.sh` / `scripts/install-codex-prompts.bat`:
  installs generated Codex slash prompts locally.
- `scripts/install-opencode.sh` / `scripts/install-opencode.bat`:
  installs generated opencode commands and skills locally.
- `scripts/install-claude-commands.sh` / `scripts/install-claude-commands.bat`:
  installs Claude Code commands locally.

## Compatibility Rules

- Treat `skills/*.md` as the canonical workflow source.
- After changing any file in `skills/`, run:
  `python3 scripts/sync-antigravity.py`
  and:
  `python3 scripts/sync-codex-skills.py`
  and:
  `python3 scripts/sync-opencode.py`
- If slash prompt compatibility is needed, also run:
  `python3 scripts/sync-codex-prompts.py`
- Do not manually edit generated `.agents/skills/*/SKILL.md`,
  `codex-skills/*/SKILL.md`, `.opencode/commands/*.md`, or
  `.opencode/skills/*/SKILL.md` unless also updating the corresponding source in `skills/`.
- For Codex-only hand-written packages under `codex-skills/`, keep them clearly
  marked as Codex-only and do not create a same-named `skills/*.md` file unless
  intentionally adopting the workflow for Claude Code too.
- Keep tool paths compatible with the documented checkout path:
  `~/ai-berkshire/tools/...`
- Keep `CLAUDE.md` for Claude Code behavior, this unified `AGENTS.md` for Antigravity,
  Codex, and opencode behavior, and `opencode.json` for opencode project config.

## Antigravity AI Agent Capability Mapping

| Capability / Task | Antigravity Native Tool | Description & Best Practice |
| :--- | :--- | :--- |
| **Exact Math & Python Tools** | `run_command` (bash) | Run `tools/financial_rigor.py`, `tools/report_audit.py`, etc. |
| **Inspect Files & Drafts** | `view_file` | Read reports, past memos, and tool code |
| **Draft New Reports** | `write_to_file` | Create formatted Markdown reports under `reports/` |
| **Surgical Content Updates** | `replace_file_content` | Precision edits for existing reports or configs |
| **Public Web Research** | `search_web` & `read_url_content` | Search filings, transcripts, and financial news |
| **Multi-Agent Research** | `invoke_subagent` (`research`, `self`) | Parallel research across masters or data sources |
| **Ambiguity Clarification** | `ask_question` | Clarify ticker, exchange, or investment horizon |

## Research Quality Rules

- Before starting any research, run the `date` command to confirm today's
  date. Treat that date as the baseline for "latest" data (prices, market cap,
  most recent filings), and state the data cutoff date in the report header.
  Never assume the current date from training data.
- Financial data must come from at least two independent sources when the skill
  requires verification.
- Use exact arithmetic tools for market cap, valuation, cross-source checks, and
  scenario analysis:
  `python3 tools/financial_rigor.py ...`
- Use report audit tooling before treating generated research as publishable:
  `python3 tools/report_audit.py ...`
- Clearly label low-confidence conclusions, incomplete data, and source gaps.
- This project is for learning and research, not investment advice.

## Editing Rules

- Preserve existing report files unless the task specifically asks to change
  them.
- Keep changes scoped to the requested skill, tool, script, or documentation.
- Before finishing a skill/tool change, run the relevant syntax or generation
  check. For compatibility changes, run:
  `python3 scripts/sync-antigravity.py`
  and:
  `python3 scripts/sync-codex-skills.py`
- To verify generated Antigravity artifacts are current without rewriting files, run:
  `python3 scripts/sync-antigravity.py --check`
- To verify generated Codex artifacts are current without rewriting files, run:
  `python3 scripts/sync-codex-skills.py --check`
  and, when slash prompts are relevant:
  `python3 scripts/sync-codex-prompts.py --check`
- To verify generated opencode artifacts are current without rewriting files,
  run:
  `python3 scripts/sync-opencode.py --check`
