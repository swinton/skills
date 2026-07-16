# Adding a skill

1. Choose a focused lowercase kebab-case name.
2. Create `skills/<skill-name>/`.
3. Add a concise, behavior-oriented `SKILL.md`.
4. Add a practical human-readable `README.md`.
5. Add references only when they improve repeated use.
6. Add representative evaluation cases with self-contained prompts, reference outputs, and behavioral invariants.
7. Add `EXPERIMENTAL.md` if the skill is still emerging.
8. Run `./scripts/validate`.
9. Install and test the skill in a real workflow.
10. Add the skill to the root README's skill list, labeled `(experimental)` when applicable.

Run the new skill's cases locally:

```sh
./scripts/eval --skill example-skill
```

Use `--dry-run` to verify discovery without model calls. Experimental failures are non-blocking unless `--strict-experimental` is supplied.

Minimal template:

```text
skills/
└── example-skill/
    ├── SKILL.md
    ├── README.md
    ├── EXPERIMENTAL.md  # optional lifecycle marker
    ├── references/       # optional
    └── evals/            # when examples demonstrate behavior
        ├── cases.yaml
        └── README.md
```

Start with the smallest instructions that reliably produce the intended behavior. Add examples from actual failures rather than designing speculative abstractions.

For an experimental skill, use the marker template in [conventions.md](conventions.md). Document why it is experimental, known limitations or risks, feedback needed, and observable graduation criteria.
