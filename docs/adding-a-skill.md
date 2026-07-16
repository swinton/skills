# Adding a skill

1. Choose a focused lowercase kebab-case name.
2. Create `skills/<skill-name>/`.
3. Add a concise, behavior-oriented `SKILL.md`.
4. Add a practical human-readable `README.md`.
5. Add references only when they improve repeated use.
6. Add representative evaluation cases.
7. Run `./scripts/validate`.
8. Install and test the skill in a real workflow.
9. Add the skill to the root README's skill list.

Minimal template:

```text
skills/
└── example-skill/
    ├── SKILL.md
    ├── README.md
    ├── references/       # optional
    └── evals/            # when examples demonstrate behavior
        ├── cases.yaml
        └── README.md
```

Start with the smallest instructions that reliably produce the intended behavior. Add examples from actual failures rather than designing speculative abstractions.

