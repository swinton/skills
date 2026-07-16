# Evaluation cases

These cases document the intended interview, availability, proposal, and confirmation behavior. Expected outputs are reference answers rather than exact-match tests; invariants matter most.

Calendar tool results are represented as fixtures. Live testing with the target Google Calendar MCP integration is required before graduating the skill.

CI runs every fixture case, but failures remain non-blocking while the skill contains `EXPERIMENTAL.md`. A strict run is available with `./scripts/eval --skill schedule-meeting --strict-experimental`.
