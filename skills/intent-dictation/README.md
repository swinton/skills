# Intent Dictation

`intent-dictation` turns rough speech-to-text transcripts into natural, paste-ready writing. It removes speech artifacts, applies spoken corrections and formatting instructions, and protects the speaker's meaning, uncertainty, voice, and technical details.

It is useful for Slack messages, emails, product documents, GitHub issues, prompts, notes, and personal messages.

## What it does not do

It does not transcribe audio, run speech recognition, invent missing facts, strengthen claims, or act as a general writing assistant detached from the original intent.

## Install

From the repository root:

```sh
./scripts/install intent-dictation
```

Claude Code 2.1.197 reports that installed skills resolve through slash commands. Start Claude Code and invoke:

```text
/intent-dictation
```

You can also state the skill and destination directly:

```text
Use the intent-dictation skill. This is a Slack message:

<rough transcript>
```

For a strict paste-ready response:

```text
Use the intent-dictation skill. Return only the polished text:

<rough transcript>
```

## Apple Dictation workflow

1. Dictate the rough text into Claude Code or another text field.
2. Include the likely destination, such as “Slack message,” “email,” “Codex prompt,” or “notes.”
3. Ask Claude to use `intent-dictation` and return only the finished writing.
4. Copy the result into the destination.

Destination context can be short:

```text
Use the intent-dictation skill. This is an email. Do not add a greeting or sign-off.

<rough transcript>
```

For a clipboard-oriented terminal workflow, Claude Code's locally verified `-p/--print` option accepts a prompt non-interactively. On macOS:

```sh
pbpaste | { printf '%s\n\n' \
  'Use the intent-dictation skill. Return only the polished text.'; cat; } \
  | claude -p | pbcopy
```

This reads a transcript from the clipboard, sends the instruction and transcript to Claude, and copies Claude's output back to the clipboard. Review sensitive or high-stakes text before pasting it elsewhere.

## Improve the skill

Add representative cases to `evals/cases.yaml`. Include a rough input, a reference output, and invariants describing meaning that must remain true. Real failed examples are especially valuable, but remove private or sensitive details first.

Run:

```sh
./scripts/validate
```

## Known limitations

- Ambiguous dictation may remain ambiguous or receive a `[?]` marker.
- Punctuation spoken inside technical strings can be difficult to distinguish from prose.
- Output can vary while still satisfying the same invariants.
- The skill depends on the language model following its instructions; evaluations are currently reviewed by humans.

