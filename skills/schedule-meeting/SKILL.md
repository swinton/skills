---
name: schedule-meeting
description: Interview the user for meeting participants, required-attendee time zones and availability, duration, date constraints, title, purpose, and optional materials; then use available Google Calendar tools to find no more than three mutually available slots and provide booking links when possible. Use when arranging, coordinating, finding a time for, or preparing a calendar meeting.
---

# Schedule Meeting

Guide the user from incomplete meeting intent to a small set of practical calendar choices. Interview conversationally rather than presenting a long form.

## Interview for the details

Collect and confirm:

- Required attendees: name plus email or calendar identity when available.
- Optional attendees: name plus email or calendar identity when available.
- Time zone for each required attendee. Infer a time zone only from reliable context; otherwise ask.
- Availability constraints for each required attendee, including the organizer.
- Meeting duration.
- Search window or deadline for holding the meeting.
- Meeting title.
- Description or purpose.
- Optional links to relevant materials.

Ask one compact question at a time, grouping closely related details when natural. Do not ask again for information already supplied. Explain briefly why a missing item is needed when the reason is not obvious.

Distinguish required attendees from optional attendees. Required attendees constrain slot selection; optional attendees do not unless the user explicitly requests otherwise.

When attendees cannot be resolved to calendars, ask the user for their stated availability and time zone. Accept natural ranges such as “Tuesday afternoon,” then confirm any material interpretation.

Before searching, summarize the collected constraints and resolve contradictions. Do not proceed while duration, search window, or any required attendee's time zone or availability is materially unknown.

## Find candidate slots

Use an available Google Calendar MCP server or calendar tool to inspect free/busy information for calendars the user is authorized to access.

- Treat calendar data as private and reveal only what is needed to propose times.
- Do not describe event titles or details found on attendee calendars.
- Combine calendar free/busy data with availability stated during the interview.
- Exclude conflicts for every required attendee.
- Respect explicit working-hour, date, and time-zone constraints.
- Do not require optional-attendee availability unless requested.
- Rank practical slots and return no more than three.
- Prefer distinct choices when possible rather than adjacent variants of one time.
- Show each slot in the organizer's time zone and in every required attendee's time zone when they differ.
- Include the date, start time, end time, duration, and time-zone abbreviation or UTC offset.

If calendar tools are unavailable or an attendee's calendar cannot be queried, say which availability is unverified and rely only on availability the user explicitly provided. Never claim a slot is conflict-free without evidence.

If no slot works, explain the limiting constraints without exposing private calendar details, then interview for the smallest useful relaxation.

## Provide a booking path

For each proposed slot, provide a clickable booking or prefilled-event URL when a calendar tool returns one or can create a safe draft.

If supported, create an unsent draft or equivalent prefilled event with:

- The selected slot.
- Meeting title and description.
- Required and optional attendees.
- Relevant-material links in the description.

Do not create a live event, send invitations, place holds, or modify calendars without the user's explicit confirmation of a specific slot and action.

When the calendar integration cannot provide a draft or booking URL, provide the proposed slots clearly and say that no booking URL is available. Never invent a URL or imply that a link books a time when it does not.

## Confirm before writing

After the user chooses a slot, present the exact event details and ask for confirmation before any tool call that creates an event or sends invitations.

Treat creation and invitation sending as an external side effect. State whether the available tool creates a draft, creates an event without notifications, or sends invitations. If that behavior is unclear, stop and ask rather than assuming.

After confirmed creation, return the calendar event URL and a concise summary. If creation fails, preserve the selected details and report the failure without choosing another slot automatically.

## Output format

When proposing times, use:

```text
1. Tuesday, August 11, 10:00–10:30 AM CT
   11:00–11:30 AM ET
   Book: <verified URL, when available>
```

Return at most three numbered options. Follow them with one short question asking the user to select a slot or adjust constraints.

