# Evaluation cases

These cases describe expected behavior without calling the live GitHub API. Expected outputs are reference answers; invariants matter more than exact formatting.

Live verification should install the skill and invoke `/whoami` in Claude Code with an authenticated `gh` session.

Required CI uses the included API-response fixtures and disables tools, so it cannot expose credentials or depend on GitHub availability.
