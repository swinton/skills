---
name: whoami
description: Identify the GitHub account currently authenticated through GitHub CLI and return a concise, meaningful profile summary from `gh api user`. Use when checking which GitHub identity, account, or credentials are active, or when testing skill installation, invocation, and tool access.
---

# Who Am I

Run:

```sh
gh api user
```

Use the response to report the authenticated GitHub identity. Include:

- Display name and login, preferring `Name (@login)` when both exist.
- Profile URL.
- Account type.
- Site administrator status only when true.
- Location, company, and bio when present.
- Account creation date.

Omit empty optional fields. Convert timestamps to readable dates without changing their calendar date. Keep the response compact and human-readable rather than returning the full JSON object.

Do not display tokens, authorization headers, environment variables, credential locations, email addresses, private profile fields, or unrelated API data.

If `gh` is unavailable, say that GitHub CLI is required. If authentication or the API request fails, report the failure plainly and suggest `gh auth status`; do not guess which account is active.

Return only the identity summary by default. Include command details or raw JSON only when directly requested.

Example:

```text
Steve Winton (@swinton)
https://github.com/swinton
Type: User
Location: Franklin, TN
GitHub member since: October 6, 2008
```

