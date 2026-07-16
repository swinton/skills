# Who Am I

`whoami` reports which GitHub account is authenticated through GitHub CLI. It invokes `gh api user` and turns the response into a compact identity summary instead of dumping raw JSON.

The summary includes the login, display name, profile URL, account type, creation date, and useful optional profile fields when available. It does not expose tokens, credential files, or unrelated private data.

## Requirements

- GitHub CLI (`gh`)
- An authenticated GitHub account
- Network access to the GitHub API

Check authentication manually with:

```sh
gh auth status
```

## Install

From the repository root:

```sh
./scripts/install whoami
```

Or install every repository skill:

```sh
./scripts/install --all
```

## Invoke

In Claude Code:

```text
/whoami
```

Run it non-interactively and write the summary to stdout:

```sh
printf '%s\n' '/whoami' | claude -p
```

You can also ask:

```text
Use the whoami skill to tell me which GitHub account is authenticated.
```

This skill is intentionally simple and is useful as an end-to-end test of skill installation, invocation, shell-tool access, GitHub authentication, and formatted output.
