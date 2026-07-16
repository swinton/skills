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

## Validate

```sh
./scripts/validate
```

Validation checks skill names, required files, frontmatter names, and YAML evaluation files using Ruby's standard YAML library.

## Add a skill

Read [docs/adding-a-skill.md](docs/adding-a-skill.md). The short version is: create a focused directory under `skills/`, add `SKILL.md` and `README.md`, include representative evaluation cases, then validate and test it in a real workflow.

Skills are expected to evolve based on real-world use. Prefer adding a failed or awkward example to the evaluations before broadening instructions abstractly.

## Experimental skills

A skill is experimental when its directory contains a non-empty `EXPERIMENTAL.md`. The marker should explain why the skill is experimental, its known limitations or risks, the feedback needed, and its graduation criteria.

Experimental skills are deliberately easy to try but excluded from `./scripts/install --all` unless `--include-experimental` is supplied. Remove the marker when the graduation criteria are met.

## Current skills

- [`intent-dictation`](skills/intent-dictation/README.md) — turn rough dictation into natural writing without changing its intent.
- [`whoami`](skills/whoami/README.md) — report the identity of the GitHub account authenticated through `gh`.
