# Agent guidance

Keep this repository lightweight. Do not add frameworks, package managers, runtime services, or elaborate evaluation systems without a demonstrated need.

Prefer Python for repository automation and scripts. Use `uv` for Python execution and dependency management, and do not introduce another scripting language unless the workflow has a demonstrated requirement that Python cannot reasonably meet.

Current priority: Make `intent-dictation` genuinely useful before expanding the repository.

When changing this repository:

- Treat each skill as an independently understandable unit.
- Keep `SKILL.md` instructions precise, concise, and behavior-oriented.
- Prefer concrete examples over abstract prose.
- Preserve the intended meaning and failure boundaries of existing skills.
- Do not silently broaden, weaken, or reinterpret a skill's behavior.
- Add or update evaluation cases whenever behavior changes.
- Keep references focused and include them only when they improve repeated use.
- Avoid runtime-specific scripts unless the workflow requires them.
- Run `./scripts/validate` before completing work.
- Test installation or execution paths affected by the change.
- Keep generated artifacts, transcripts, private data, and temporary files out of Git.
- Update documentation when introducing a new convention.
- Explain why significant changes are needed, not only what changed.
