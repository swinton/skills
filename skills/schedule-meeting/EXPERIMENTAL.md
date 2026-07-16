# Experimental

## Why

Google Calendar MCP integrations vary in tool names and in whether they support free/busy queries, draft events, event creation, invitation sending, and event URLs. This workflow needs real-world testing against the installed integration.

## Known limitations or risks

- Calendar availability may be unavailable for external or unresolved attendees.
- Natural-language availability and time zones can be ambiguous.
- A calendar integration may create and send an event in one operation instead of supporting a draft.
- Booking URLs may not be available for every proposed slot.
- Incorrect tool assumptions could create an event or notify attendees unexpectedly, so explicit confirmation is required.

## Feedback needed

- Which Google Calendar MCP tools are available in the target Claude Code environment.
- Whether free/busy works across the calendars Steve commonly schedules with.
- Whether the integration can create safe drafts or return prefilled event URLs.
- Whether the interview feels concise while collecting enough information.
- Whether proposed times are accurate across daylight-saving transitions.

## Graduation criteria

- Complete at least five real scheduling workflows across two or more time zones.
- Confirm required-attendee availability is handled accurately.
- Verify event creation and invitation semantics for the installed calendar integration.
- Verify no event is created or invitation sent before explicit confirmation.
- Record and address material failures in the evaluation cases.

