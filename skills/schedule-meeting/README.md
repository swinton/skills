# Schedule Meeting

`schedule-meeting` interviews you for the information needed to arrange a meeting, checks required-attendee availability with an available Google Calendar integration, and proposes no more than three practical slots.

This skill is experimental. See [EXPERIMENTAL.md](EXPERIMENTAL.md).

## What it collects

- Required and optional attendees.
- Each required attendee's time zone and availability.
- Duration and the date range in which to search.
- Meeting title and purpose.
- Optional links for the invitation.

Required attendees constrain the proposed times. Optional attendees are added to the invitation but do not block a slot unless requested.

## Requirements

For calendar-backed availability and event links, Claude Code needs an authenticated Google Calendar MCP server or tool with suitable calendar access. The skill can still coordinate from availability you provide manually, but it must label those results as unverified.

The exact Google Calendar tool is intentionally not hard-coded while this skill is experimental. Calendar integrations differ in free/busy, draft-event, event-creation, and invitation behavior.

## Install

Experimental skills are excluded from bulk installation by default. Install this skill explicitly:

```sh
./scripts/install schedule-meeting
```

Or include all experimental skills:

```sh
./scripts/install --all --include-experimental
```

## Invoke

In Claude Code:

```text
/schedule-meeting
```

Or:

```text
Use the schedule-meeting skill. Interview me to arrange a 30-minute meeting with Jordan next week.
```

The skill should ask for missing details incrementally, inspect calendar availability when possible, and return at most three choices. It must ask for explicit confirmation before creating an event or sending invitations.

## Safety

- Calendar contents are private; the skill should expose only availability, not unrelated event details.
- A proposed slot is not a reservation.
- Booking links must come from a verified calendar tool or safe draft flow.
- The skill must not create events, place holds, or send invitations without confirmation.

## Improve the skill

Add fictionalized failures and reference answers to `evals/cases.yaml`. Useful feedback includes interview friction, time-zone errors, false availability claims, weak slot ranking, missing booking links, and unclear creation semantics.

