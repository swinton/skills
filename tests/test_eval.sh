#!/bin/sh

set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TMPDIR_ROOT=$(mktemp -d)
trap 'rm -rf "$TMPDIR_ROOT"' EXIT HUP INT TERM

FAKE="$TMPDIR_ROOT/claude"
STATE="$TMPDIR_ROOT/state"
FAKE_GIT="$TMPDIR_ROOT/git"

cat >"$FAKE" <<'EOF'
#!/bin/sh
input=$(cat)
case " $* " in
  *" --system-prompt-file "*)
    found_system_prompt=true
    ;;
  *)
    found_system_prompt=false
    ;;
esac
if [ "${FAKE_MODE:-pass}" = "error" ]; then
  echo "simulated API failure" >&2
  exit 1
fi
if [ "$found_system_prompt" = false ] && printf '%s' "$input" | grep -q '^Evaluate this candidate output'; then
  if [ "${FAKE_MODE:-pass}" = "retry" ]; then
    count=0
    [ ! -f "$FAKE_STATE" ] || count=$(cat "$FAKE_STATE")
    count=$((count + 1))
    printf '%s\n' "$count" >"$FAKE_STATE"
    [ "$count" -gt 1 ] && result='{"pass":true,"reason":"recovered","failed_invariants":[]}' || result='{"pass":false,"reason":"first failure","failed_invariants":["test"]}'
  elif [ "${FAKE_MODE:-pass}" = "fail" ]; then
    result='{"pass":false,"reason":"failed","failed_invariants":["test"]}'
  else
    result='{"pass":true,"reason":"passed","failed_invariants":[]}'
  fi
else
  [ "$found_system_prompt" = true ] || {
    echo "candidate call omitted --system-prompt-file" >&2
    exit 1
  }
  result='Candidate response'
fi
printf '{"result":%s}\n' "$(printf '%s' "$result" | ruby -rjson -e 'puts JSON.generate(STDIN.read)')"
EOF
chmod +x "$FAKE"

cat >"$FAKE_GIT" <<'EOF'
#!/bin/sh
case "${FAKE_GIT_MODE:-skill}" in
  skill)
    printf '%s\n' skills/whoami/SKILL.md README.md
    ;;
  global)
    printf '%s\n' scripts/eval
    ;;
  docs)
    printf '%s\n' README.md docs/conventions.md
    ;;
esac
EOF
chmod +x "$FAKE_GIT"

dry_run=$("$ROOT/scripts/eval" --all --dry-run)
printf '%s\n' "$dry_run" | grep -q 'intent-dictation/remove-fillers'
printf '%s\n' "$dry_run" | grep -q '30 case(s)'

changed=$(FAKE_GIT_MODE=skill GIT_BIN="$FAKE_GIT" "$ROOT/scripts/eval" --all --changed-since base --dry-run)
printf '%s\n' "$changed" | grep -q 'whoami/complete-profile'
printf '%s\n' "$changed" | grep -q '4 case(s)'
if printf '%s\n' "$changed" | grep -q 'intent-dictation/'; then
  echo "error: unchanged skill was selected" >&2
  exit 1
fi

global=$(FAKE_GIT_MODE=global GIT_BIN="$FAKE_GIT" "$ROOT/scripts/eval" --all --changed-since base --dry-run)
printf '%s\n' "$global" | grep -q '30 case(s)'

docs=$(FAKE_GIT_MODE=docs GIT_BIN="$FAKE_GIT" "$ROOT/scripts/eval" --all --changed-since base --dry-run)
printf '%s\n' "$docs" | grep -q '0 case(s)'

CLAUDE_BIN="$FAKE" "$ROOT/scripts/eval" --skill whoami --case sparse-profile --output "$TMPDIR_ROOT/pass.json" --junit "$TMPDIR_ROOT/pass.xml" >/dev/null
ruby -rjson -e 's=JSON.parse(File.read(ARGV[0])); abort unless s["passed"] == 1 && s["blocking_failures"] == 0' "$TMPDIR_ROOT/pass.json"
grep -q '<testsuite name="skill-evals" tests="1" failures="0">' "$TMPDIR_ROOT/pass.xml"

FAKE_MODE=retry FAKE_STATE="$STATE" CLAUDE_BIN="$FAKE" "$ROOT/scripts/eval" --skill whoami --case sparse-profile --output "$TMPDIR_ROOT/retry.json" >/dev/null
ruby -rjson -e 's=JSON.parse(File.read(ARGV[0])); abort unless s["flaky"] == 1 && s["blocking_failures"] == 0' "$TMPDIR_ROOT/retry.json"

if FAKE_MODE=fail CLAUDE_BIN="$FAKE" "$ROOT/scripts/eval" --skill whoami --case sparse-profile >/dev/null; then
  echo "error: stable failure did not block" >&2
  exit 1
fi

FAKE_MODE=fail CLAUDE_BIN="$FAKE" "$ROOT/scripts/eval" --skill schedule-meeting --case three-slot-limit >/dev/null
if FAKE_MODE=fail CLAUDE_BIN="$FAKE" "$ROOT/scripts/eval" --skill schedule-meeting --case three-slot-limit --strict-experimental >/dev/null; then
  echo "error: strict experimental failure did not block" >&2
  exit 1
fi
if FAKE_MODE=error CLAUDE_BIN="$FAKE" "$ROOT/scripts/eval" --skill schedule-meeting --case three-slot-limit >/dev/null; then
  echo "error: evaluation infrastructure failure did not block" >&2
  exit 1
fi

echo "eval runner tests passed"
