# Skill conventions

These conventions are intentionally lightweight and may change as the repository gains real usage.

Each skill should:

1. Live at `skills/<skill-name>/`.
2. Use a lowercase kebab-case name.
3. Include a `SKILL.md`.
4. Include a human-readable `README.md`.
5. Include evaluation cases when input/output examples can demonstrate behavior.
6. Keep supporting material in `references/`.
7. Focus on one repeatable workflow.
8. Define non-goals and failure-sensitive behavior explicitly.
9. Avoid unnecessary runtime-specific scripts.
10. Produce paste-ready output by default when its purpose is writing.

Frontmatter should contain a `name` matching the directory and a concrete `description` that states what the skill does and when it should trigger.

Evaluation cases are behavioral documentation and model-graded regression tests, not exact-match tests. Every case in `evals/cases.yaml` must contain:

- A unique lowercase kebab-case `id`.
- A concise `description`.
- A self-contained `prompt` that can be sent to the installed skill.
- A representative `expected` response.
- Non-empty `invariants` describing behavior and meaning that must hold.

The invariants are authoritative; wording may differ from the reference output. Keep tool-dependent cases deterministic by expressing external results as fixtures in the prompt. Live authenticated integration checks belong outside required pull-request CI.

Stable-skill eval failures block CI after one automatic retry. Eval failures for skills containing `EXPERIMENTAL.md` are visible but non-blocking by default. Run `./scripts/eval --all --strict-experimental` before graduating an experimental skill.

Pull-request and push CI evaluates only affected skills. Any changed path under `skills/<skill-name>/` selects that skill. Changes to shared evaluation or installation behavior select every skill. Scheduled, manual, and strict graduation runs evaluate the complete suite.

Every skill, including experimental skills, must pass the agent-security scan. Security findings are not relaxed by experimental status. Treat the scan as supplemental evidence: it detects known malicious and risky patterns but does not certify safety or replace source review and least-privilege execution.

## Experimental status

Add a non-empty `EXPERIMENTAL.md` to mark an emerging skill as experimental. This marker is the source of truth; do not add lifecycle metadata to `SKILL.md` frontmatter.

Use this template:

```markdown
# Experimental

## Why

Explain why the skill is not yet considered stable.

## Known limitations or risks

- List concrete limitations or failure-sensitive behavior.

## Feedback needed

- Describe the real-world evidence needed to improve confidence.

## Graduation criteria

- State the observable conditions required to consider the skill stable.
```

List experimental skills as `(experimental)` in the root README. Remove `EXPERIMENTAL.md` to graduate a skill after its criteria are met.
