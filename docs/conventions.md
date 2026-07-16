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

Evaluation cases are behavioral documentation, not exact-match tests. Prefer representative inputs, reference outputs, and invariants that identify meaning which must not change.

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
