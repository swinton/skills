"""Tests for changed skill selection."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "changed-skills"


class ChangedSkillsTests(unittest.TestCase):
    def run_in_repo(self, changed_path: str) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"], cwd=repo, check=True
            )
            subprocess.run(
                ["git", "config", "user.name", "Test"], cwd=repo, check=True
            )
            (repo / "skills" / "alpha").mkdir(parents=True)
            (repo / "skills" / "beta").mkdir(parents=True)
            (repo / "skills" / "alpha" / "SKILL.md").write_text("alpha\n")
            (repo / "skills" / "beta" / "SKILL.md").write_text("beta\n")
            (repo / ".github" / "workflows").mkdir(parents=True)
            (repo / "scripts").mkdir()
            (repo / "scripts" / "changed-skills").write_text(SCRIPT.read_text())
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "base"], cwd=repo, check=True)
            base = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=repo, text=True
            ).strip()
            target = repo / changed_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(target.read_text() + "changed\n" if target.exists() else "changed\n")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "change"], cwd=repo, check=True)
            output = subprocess.check_output(
                ["python3", "scripts/changed-skills", "--changed-since", base],
                cwd=repo,
                text=True,
            )
            return output.splitlines()

    def test_skill_change_selects_only_that_skill(self) -> None:
        self.assertEqual(["skills/alpha"], self.run_in_repo("skills/alpha/SKILL.md"))

    def test_shared_security_change_selects_all_skills(self) -> None:
        self.assertEqual(
            ["skills/alpha", "skills/beta"],
            self.run_in_repo(".github/workflows/agent-security.yml"),
        )

    def test_documentation_change_selects_no_skills(self) -> None:
        self.assertEqual([], self.run_in_repo("README.md"))


if __name__ == "__main__":
    unittest.main()
