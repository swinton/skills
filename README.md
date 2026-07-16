# Personal AI Skills

[![CI](https://github.com/swinton/skills/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/swinton/skills/actions/workflows/ci.yml)

A curated collection of personal AI skills.

Stable skills are workflows I trust and use regularly. Experimental skills are ideas under active development. Every stable skill began life as an experiment.

This repository keeps useful agent behavior version-controlled, understandable, installable, and easy to improve. It is deliberately a small collection of independent skills, not a general-purpose framework or formal skill standard.

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

Experimental skills are excluded from bulk installation by default. Include them explicitly:

```sh
./scripts/install --all --include-experimental
```

Installing an experimental skill by name is allowed and prints a warning.

By default, the installer creates symbolic links in `~/.claude/skills`, so repository edits are immediately available. Run `./scripts/install --help` for target-directory and replacement options.

In Claude Code, explicitly invoke an installed skill with its slash command, such as `/intent-dictation` or `/whoami`.

## Run a skill non-interactively

Claude Code's `-p/--print` mode reads a prompt from stdin and writes the result to stdout. Prepend the skill's slash command to incoming data with a shell group:

```sh
{ printf '%s\n\n' '/intent-dictation'; cat; } | claude -p
```

This is the standard one-line pattern for a skill that transforms stdin:

```sh
producer | { printf '%s\n\n' '/skill-name'; cat; } | claude -p | consumer
```

For example:

```sh
pbpaste | { printf '%s\n\n' '/intent-dictation'; cat; } | claude -p | pbcopy
```

For a skill that needs no additional input:

```sh
printf '%s\n' '/whoami' | claude -p
```

Run non-interactive commands from a directory you trust. Skills that use external tools still require those tools, authentication, network access, and any applicable Claude Code permissions.

## Keep skill surfaces in sync

Claude Code reads installed skills directly from disk. Personal skills in Claude Chat and Cowork share an account-level list but require a manual ZIP upload through Customize > Skills. The optional workspace Skills API is a third, independent target.

```sh
uv run sync_skills.py status
uv run sync_skills.py bundle [skill-name]
uv run sync_skills.py mark-synced <skill-name>
uv run sync_skills.py mark-synced --all
uv run sync_skills.py push-api [skill-name]
```

`status` compares each canonical skill with the last manually recorded claude.ai upload. `bundle` creates upload-ready ZIPs in `dist/`; after uploading them, use `mark-synced`. `push-api` requires `ANTHROPIC_API_KEY` and targets only the separate workspace-level Skills API—it cannot update personal claude.ai skills.

## Validate

```sh
./scripts/validate
```

Validation checks skill names, required files, frontmatter names, and the evaluation-case schema using Ruby's standard YAML library.

Run every behavioral evaluation:

```sh
./scripts/eval --all
```

The evaluator installs the skills into an isolated temporary home, invokes each skill through Claude Code, and uses a separate structured judge call to check the candidate against the case invariants. Stable-skill failures block after one retry. Experimental-skill failures are reported but do not produce a failing exit status unless `--strict-experimental` is supplied.

Evaluation requires Claude Code and `ANTHROPIC_API_KEY`. Use `./scripts/eval --all --dry-run` to inspect case discovery without making model calls. CI writes complete candidate outputs and judge explanations to downloadable JSON and JUnit artifacts.

GitHub Actions runs validation, Python unit tests, evaluator tests, installation smoke tests, and all skill evaluations. Configure `ANTHROPIC_API_KEY` as a repository Actions secret, then require the `Validate` and `Stable skill evals` checks in branch protection.

## Add a skill

Read [docs/adding-a-skill.md](docs/adding-a-skill.md). The short version is: create a focused directory under `skills/`, add `SKILL.md` and `README.md`, include representative evaluation cases, then validate and test it in a real workflow.

Skills are expected to evolve based on real-world use. Prefer adding a failed or awkward example to the evaluations before broadening instructions abstractly.

## Experimental skills

A skill is experimental when its directory contains a non-empty `EXPERIMENTAL.md`. The marker should explain why the skill is experimental, its known limitations or risks, the feedback needed, and its graduation criteria.

Experimental skills are deliberately easy to try but excluded from `./scripts/install --all` unless `--include-experimental` is supplied. Remove the marker when the graduation criteria are met.

## Current skills

- [`intent-dictation`](skills/intent-dictation/README.md) — turn rough dictation into natural writing without changing its intent.
- [`schedule-meeting`](skills/schedule-meeting/README.md) **(experimental)** — interview for meeting details, check required-attendee availability, and propose bookable slots.
- [`whoami`](skills/whoami/README.md) — report the identity of the GitHub account authenticated through `gh`.
