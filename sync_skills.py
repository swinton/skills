#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "anthropic>=0.40.0",
# ]
# ///
"""Detect Claude skill drift, build upload bundles, and optionally push to the API.

Claude Code reads the canonical skills directory directly. Personal skills in
claude.ai require a manual ZIP upload, while the workspace Skills API is a
separate optional synchronization target.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import zipfile
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any


DEFAULT_SKILLS_DIR = Path(
    os.environ.get("CLAUDE_SKILLS_DIR", Path.home() / ".claude" / "skills")
).expanduser()
DEFAULT_BUNDLE_DIR = Path("dist")
STATE_FILENAME = ".sync-state.json"
SKILLS_BETA = "skills-2025-10-02"

IGNORE_NAMES = {
    ".DS_Store",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    STATE_FILENAME,
    "__pycache__",
}


class SyncError(RuntimeError):
    """A user-facing synchronization error."""


def is_ignored(relative_path: Path) -> bool:
    """Return whether a relative skill path should be excluded."""

    return any(part in IGNORE_NAMES for part in relative_path.parts)


def iter_skill_files(skill_dir: Path) -> Iterable[tuple[Path, Path]]:
    """Yield ``(absolute_path, relative_path)`` pairs in stable path order."""

    for path in sorted(skill_dir.rglob("*"), key=lambda item: item.as_posix()):
        if not path.is_file():
            continue
        relative_path = path.relative_to(skill_dir)
        if not is_ignored(relative_path):
            yield path, relative_path


def iter_skill_dirs(skills_dir: Path) -> Iterable[Path]:
    """Yield valid immediate child skill directories in name order."""

    if not skills_dir.is_dir():
        raise SyncError(f"No skills directory found at {skills_dir}")

    for entry in sorted(skills_dir.iterdir(), key=lambda item: item.name):
        if entry.is_dir() and (entry / "SKILL.md").is_file():
            yield entry


def hash_skill_dir(skill_dir: Path) -> str:
    """Return a stable SHA-256 hash of relative file names and file bytes.

    Length-prefixing prevents ambiguous concatenations. File metadata,
    directory ordering, ignored generated files, and timestamps do not affect
    the result.
    """

    if not (skill_dir / "SKILL.md").is_file():
        raise SyncError(f"Not a skill directory: {skill_dir}")

    digest = hashlib.sha256()
    for path, relative_path in iter_skill_files(skill_dir):
        encoded_path = relative_path.as_posix().encode("utf-8")
        contents = path.read_bytes()
        digest.update(len(encoded_path).to_bytes(8, "big"))
        digest.update(encoded_path)
        digest.update(len(contents).to_bytes(8, "big"))
        digest.update(contents)
    return digest.hexdigest()


def load_state(state_file: Path) -> dict[str, dict[str, Any]]:
    """Load synchronization state, returning an empty mapping when absent."""

    if not state_file.exists():
        return {}
    try:
        state = json.loads(state_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SyncError(f"Could not read state file {state_file}: {error}") from error
    if not isinstance(state, dict) or any(
        not isinstance(name, str) or not isinstance(record, dict)
        for name, record in state.items()
    ):
        raise SyncError(f"State file {state_file} must contain an object of skill records")
    return state


def save_state(state_file: Path, state: dict[str, dict[str, Any]]) -> None:
    """Atomically save synchronization state as deterministic JSON."""

    state_file.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(state, indent=2, sort_keys=True) + "\n"
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=state_file.parent,
            prefix=f".{state_file.name}.",
            delete=False,
        ) as temporary:
            temporary.write(serialized)
            temporary_path = Path(temporary.name)
        temporary_path.replace(state_file)
    except OSError as error:
        raise SyncError(f"Could not write state file {state_file}: {error}") from error


def select_skills(skills_dir: Path, target: str | None) -> list[Path]:
    """Return all skills or one named skill, raising for an unknown target."""

    skills = list(iter_skill_dirs(skills_dir))
    if target is None:
        return skills
    selected = [skill for skill in skills if skill.name == target]
    if not selected:
        raise SyncError(f"No skill named '{target}' found in {skills_dir}")
    return selected


def classify_skills(
    skills: Sequence[Path], state: dict[str, dict[str, Any]]
) -> tuple[list[str], list[str], list[str]]:
    """Classify skills as new, changed, or synced for claude.ai."""

    new: list[str] = []
    changed: list[str] = []
    current: list[str] = []
    for skill_dir in skills:
        current_hash = hash_skill_dir(skill_dir)
        record = state.get(skill_dir.name)
        if record is None or not record.get("claude_ai_hash"):
            new.append(skill_dir.name)
        elif record["claude_ai_hash"] != current_hash:
            changed.append(skill_dir.name)
        else:
            current.append(skill_dir.name)
    return new, changed, current


def zip_skill(skill_dir: Path, output_dir: Path) -> Path:
    """Create a deterministic ZIP with the skill directory at its root."""

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{skill_dir.name}.zip"
    with zipfile.ZipFile(
        output_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for path, relative_path in iter_skill_files(skill_dir):
            archive_path = (Path(skill_dir.name) / relative_path).as_posix()
            info = zipfile.ZipInfo(archive_path, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (path.stat().st_mode & 0xFFFF) << 16
            archive.writestr(info, path.read_bytes())
    return output_path


def command_status(args: argparse.Namespace) -> int:
    """Report drift from the last recorded personal claude.ai upload."""

    state = load_state(args.state_file)
    skills = select_skills(args.skills_dir, None)
    if not skills:
        print("No skills found.")
        return 0

    new, changed, current = classify_skills(skills, state)
    print(f"Canonical source: {args.skills_dir}\n")
    if new:
        print(f"NEW (never marked synced) — {len(new)}:")
        for name in new:
            print(f"  + {name}")
    if changed:
        print(f"\nCHANGED since last claude.ai upload — {len(changed)}:")
        for name in changed:
            print(f"  * {name}")
    if current:
        print(f"\nUp to date — {len(current)}:")
        for name in current:
            print(f"  = {name}")

    if new or changed:
        print(
            "\nPersonal claude.ai skills cannot currently be updated through a "
            "public API."
        )
        print("Run `bundle` and upload the ZIPs through Customize > Skills.")
        print("After uploading, run `mark-synced <name>` (or `--all`).")
        return 1 if args.check else 0

    print("\nNothing to upload. Personal claude.ai skills are marked in sync.")
    return 0


def command_bundle(args: argparse.Namespace) -> int:
    """Bundle one or every canonical skill for manual claude.ai upload."""

    skills = select_skills(args.skills_dir, args.skill)
    if not skills:
        print("No skills found.")
        return 0
    for skill_dir in skills:
        output_path = zip_skill(skill_dir, args.bundle_dir)
        print(f"Bundled {skill_dir.name} -> {output_path}")
    print("\nUpload via claude.ai Customize > Skills (+ > Create skill).")
    return 0


def command_mark_synced(args: argparse.Namespace) -> int:
    """Record current hashes after successful manual claude.ai uploads."""

    state = load_state(args.state_file)
    skills = select_skills(args.skills_dir, None if args.all else args.skill)
    if not skills:
        print("No skills found.")
        return 0
    for skill_dir in skills:
        current_hash = hash_skill_dir(skill_dir)
        state.setdefault(skill_dir.name, {})["claude_ai_hash"] = current_hash
        print(f"Marked {skill_dir.name} as synced (hash {current_hash[:12]}...)")
    save_state(args.state_file, state)
    return 0


def api_files(skill_dir: Path) -> list[tuple[str, bytes]]:
    """Build SDK upload tuples that retain the required top-level directory."""

    return [
        ((Path(skill_dir.name) / relative_path).as_posix(), path.read_bytes())
        for path, relative_path in iter_skill_files(skill_dir)
    ]


def command_push_api(args: argparse.Namespace) -> int:
    """Push changed skills to the separate workspace-level Skills API."""

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SyncError("ANTHROPIC_API_KEY is not set; cannot push to the Skills API")

    try:
        import anthropic
    except ImportError as error:
        raise SyncError(
            "The anthropic SDK is unavailable; run this command through uv"
        ) from error

    client = anthropic.Anthropic(api_key=api_key)
    state = load_state(args.state_file)
    skills = select_skills(args.skills_dir, args.skill)
    failures = 0

    print(
        "Target: workspace Skills API (separate from personal claude.ai skills)."
    )
    for skill_dir in skills:
        name = skill_dir.name
        current_hash = hash_skill_dir(skill_dir)
        record = state.get(name, {})
        if record.get("api_hash") == current_hash:
            print(f"{name}: unchanged, skipping API push")
            continue

        try:
            skill_id = record.get("api_skill_id")
            if skill_id:
                response = client.beta.skills.versions.create(
                    skill_id,
                    files=api_files(skill_dir),
                    betas=[SKILLS_BETA],
                )
                print(
                    f"{name}: pushed version {response.version} "
                    f"to existing skill {skill_id}"
                )
            else:
                response = client.beta.skills.create(
                    display_title=name,
                    files=api_files(skill_dir),
                    betas=[SKILLS_BETA],
                )
                skill_id = response.id
                print(f"{name}: created workspace skill {skill_id}")
            state.setdefault(name, {})["api_hash"] = current_hash
            state[name]["api_skill_id"] = skill_id
            save_state(args.state_file, state)
        except Exception as error:  # SDK exceptions vary by transport/status.
            failures += 1
            print(f"{name}: API push failed — {error}", file=sys.stderr)

    if failures:
        print(
            "Personal claude.ai uploads are unaffected and still require "
            "bundle + manual upload.",
            file=sys.stderr,
        )
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""

    parser = argparse.ArgumentParser(
        description="Detect and synchronize drift across Claude skill surfaces.",
        epilog=(
            "Personal claude.ai skill uploads remain UI-only. push-api targets "
            "the separate workspace Skills API."
        ),
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=DEFAULT_SKILLS_DIR,
        help=f"canonical skills directory (default: {DEFAULT_SKILLS_DIR})",
    )
    parser.add_argument(
        "--state-file",
        type=Path,
        help=f"sync state file (default: SKILLS_DIR/{STATE_FILENAME})",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="report claude.ai drift")
    status_parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 when new or changed personal skills are found",
    )
    status_parser.set_defaults(handler=command_status)

    bundle_parser = subparsers.add_parser(
        "bundle", help="build ZIPs for manual claude.ai upload"
    )
    bundle_parser.add_argument("skill", nargs="?", help="bundle only this skill")
    bundle_parser.add_argument(
        "--output-dir",
        dest="bundle_dir",
        type=Path,
        default=DEFAULT_BUNDLE_DIR,
        help=f"bundle destination (default: {DEFAULT_BUNDLE_DIR})",
    )
    bundle_parser.set_defaults(handler=command_bundle)

    mark_parser = subparsers.add_parser(
        "mark-synced", help="record a completed manual claude.ai upload"
    )
    mark_target = mark_parser.add_mutually_exclusive_group(required=True)
    mark_target.add_argument("skill", nargs="?", help="skill that was uploaded")
    mark_target.add_argument("--all", action="store_true", help="mark every skill")
    mark_parser.set_defaults(handler=command_mark_synced)

    api_parser = subparsers.add_parser(
        "push-api", help="push to the separate workspace Skills API"
    )
    api_parser.add_argument("skill", nargs="?", help="push only this skill")
    api_parser.set_defaults(handler=command_push_api)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Parse arguments and run the selected command."""

    parser = build_parser()
    args = parser.parse_args(argv)
    args.skills_dir = args.skills_dir.expanduser().resolve()
    args.state_file = (
        args.state_file.expanduser().resolve()
        if args.state_file
        else args.skills_dir / STATE_FILENAME
    )
    if hasattr(args, "bundle_dir"):
        args.bundle_dir = args.bundle_dir.expanduser().resolve()
    try:
        return args.handler(args)
    except SyncError as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
