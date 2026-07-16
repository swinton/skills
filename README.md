# Personal AI Skills

A personal, version-controlled collection of reusable AI skills for recurring workflows.

This repository exists to make useful agent behavior easy to understand, install, test, and improve. It is deliberately a small collection of independent skills, not a general-purpose framework or formal skill standard.

The first skill is [`intent-dictation`](skills/intent-dictation/README.md), which turns rough speech-to-text transcripts into polished, paste-ready writing while preserving the speaker's meaning.

## Layout

```text
.
├── docs/       Repository conventions and contribution guidance
├── scripts/    Installation and validation commands
└── skills/     Independently understandable skill directories
```

## Install

Install one skill into Claude Code:

```sh
./scripts/install intent-dictation
```

Install every skill:

```sh
./scripts/install --all
```

By default, the installer creates symbolic links in `~/.claude/skills`, so repository edits are immediately available. Run `./scripts/install --help` for target-directory and replacement options.

In Claude Code, explicitly invoke the installed skill with `/intent-dictation`, or ask Claude to use the `intent-dictation` skill in a prompt.

## Validate

```sh
./scripts/validate
```

Validation checks skill names, required files, frontmatter names, and YAML evaluation files using Ruby's standard YAML library.

## Add a skill

Read [docs/adding-a-skill.md](docs/adding-a-skill.md). The short version is: create a focused directory under `skills/`, add `SKILL.md` and `README.md`, include representative evaluation cases, then validate and test it in a real workflow.

Skills are expected to evolve based on real-world use. Prefer adding a failed or awkward example to the evaluations before broadening instructions abstractly.

## Current skills

- [`intent-dictation`](skills/intent-dictation/README.md) — turn rough dictation into natural writing without changing its intent.

