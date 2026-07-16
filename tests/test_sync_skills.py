"""Unit tests for sync_skills hashing and state persistence."""

from __future__ import annotations

import json
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import sync_skills


class HashSkillDirectoryTests(unittest.TestCase):
    """Verify stable, sensitive, and appropriately filtered skill hashing."""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.skill_dir = Path(self.temporary_directory.name) / "example-skill"
        self.skill_dir.mkdir()
        (self.skill_dir / "SKILL.md").write_text(
            "---\nname: example-skill\ndescription: Test.\n---\n",
            encoding="utf-8",
        )
        (self.skill_dir / "reference.txt").write_text("alpha", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_hash_is_stable_across_repeated_runs(self) -> None:
        first = sync_skills.hash_skill_dir(self.skill_dir)
        second = sync_skills.hash_skill_dir(self.skill_dir)
        self.assertEqual(first, second)

    def test_hash_changes_when_file_content_changes(self) -> None:
        original = sync_skills.hash_skill_dir(self.skill_dir)
        (self.skill_dir / "reference.txt").write_text("beta", encoding="utf-8")
        self.assertNotEqual(original, sync_skills.hash_skill_dir(self.skill_dir))

    def test_hash_changes_when_file_is_renamed(self) -> None:
        original = sync_skills.hash_skill_dir(self.skill_dir)
        (self.skill_dir / "reference.txt").rename(self.skill_dir / "renamed.txt")
        self.assertNotEqual(original, sync_skills.hash_skill_dir(self.skill_dir))

    def test_hash_ignores_git_and_python_cache_content(self) -> None:
        original = sync_skills.hash_skill_dir(self.skill_dir)
        ignored_files = {
            ".git/config": "git metadata",
            "__pycache__/module.pyc": "compiled",
            ".pytest_cache/state": "pytest",
            ".DS_Store": "finder metadata",
        }
        for relative_name, contents in ignored_files.items():
            path = self.skill_dir / relative_name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding="utf-8")
        self.assertEqual(original, sync_skills.hash_skill_dir(self.skill_dir))


class StateTests(unittest.TestCase):
    """Verify synchronization state persistence."""

    def test_load_missing_state_returns_empty_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_file = Path(directory) / ".sync-state.json"
            self.assertEqual({}, sync_skills.load_state(state_file))

    def test_save_and_load_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_file = Path(directory) / ".sync-state.json"
            state = {
                "example-skill": {
                    "api_hash": "def456",
                    "api_skill_id": "skill_example",
                    "claude_ai_hash": "abc123",
                }
            }
            sync_skills.save_state(state_file, state)
            self.assertEqual(state, sync_skills.load_state(state_file))
            self.assertEqual(
                state,
                json.loads(state_file.read_text(encoding="utf-8")),
            )


class StatusOutputTests(unittest.TestCase):
    """Verify that drift output gives exact, targeted next commands."""

    def test_status_prints_commands_only_for_new_and_changed_skills(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skills_dir = root / "skills"
            state_file = skills_dir / ".sync-state.json"
            for name in ("changed-skill", "current-skill", "new-skill"):
                skill_dir = skills_dir / name
                skill_dir.mkdir(parents=True)
                (skill_dir / "SKILL.md").write_text(
                    f"---\nname: {name}\ndescription: Test.\n---\n",
                    encoding="utf-8",
                )

            state = {
                "changed-skill": {"claude_ai_hash": "outdated"},
                "current-skill": {
                    "claude_ai_hash": sync_skills.hash_skill_dir(
                        skills_dir / "current-skill"
                    )
                },
            }
            sync_skills.save_state(state_file, state)
            output = StringIO()
            args = Namespace(
                skills_dir=skills_dir,
                state_file=state_file,
                check=False,
            )

            with redirect_stdout(output):
                result = sync_skills.command_status(args)

            rendered = output.getvalue()
            self.assertEqual(0, result)
            for name in ("new-skill", "changed-skill"):
                self.assertIn(
                    f"uv run sync_skills.py bundle {name}",
                    rendered,
                )
                self.assertIn(
                    f"uv run sync_skills.py mark-synced {name}",
                    rendered,
                )
            self.assertNotIn(
                "uv run sync_skills.py bundle current-skill",
                rendered,
            )
            self.assertNotIn(
                "uv run sync_skills.py mark-synced current-skill",
                rendered,
            )


if __name__ == "__main__":
    unittest.main()
