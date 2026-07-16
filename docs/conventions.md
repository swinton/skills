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

