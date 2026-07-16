---
name: intent-dictation
description: Transform rough dictation and speech-to-text transcripts into polished, natural, paste-ready writing while preserving intended meaning, tone, uncertainty, technical details, and spoken corrections. Use for dictated Slack messages, emails, documents, prompts, notes, personal messages, or any request to clean up speech artifacts without rewriting the speaker's intent.
---

# Intent Dictation

Transform the transcript into writing that expresses the speaker's intent naturally. Do not merely produce a cleaner literal transcript.

## Apply the transformation

- Remove filler, accidental repetition, and abandoned sentence starts.
- Resolve self-corrections and use the speaker's final intended wording.
- Add punctuation, paragraph breaks, and lightweight structure appropriate to the destination.
- Convert spoken structure into written structure, including paragraphs and requested lists.
- Preserve warmth, humor, directness, hesitation, and other meaningful tone.
- Prefer concise, concrete language without flattening the speaker's voice.
- Infer a lightweight destination style when supplied: conversational for chat, complete and well-paragraphed for email, structured for documents and prompts, and compact for notes.

Read `references/personal-style.md` when personal voice matters. Read `references/vocabulary.md` when the transcript contains Steve's products, tools, or recurring technical terms.

## Preserve meaning

Treat fidelity as the highest priority.

- Do not add facts, arguments, commitments, actions, people, dates, numbers, or technical details.
- Do not increase certainty or remove meaningful uncertainty.
- Do not change the requested action or who is responsible for it.
- Do not strengthen a tentative claim into a definitive one.
- Do not improve an argument by inventing supporting claims.
- Keep ambiguous wording when it can safely remain ambiguous.

## Apply spoken editing instructions

Interpret editing phrases as commands and omit them from the result unless context clearly makes them literal. Apply instructions such as:

- “scratch that,” “ignore that,” or “don't include that”
- “actually,” “let me rephrase,” or “change Tuesday to Thursday”
- “new paragraph,” “bullet list,” or “numbered list”
- “quote” and “end quote”
- “make that less formal” or “make that more concise”

Use the corrected or reformatted content, not the spoken command.

## Protect technical content

Preserve exact text where possible for commands, code, paths, URLs, domains, API routes, environment variables, product names, identifiers, error messages, versions, dates, times, and acronyms.

Do not normalize an unusual technical term merely because it looks wrong. If dictation likely misheard a material technical item and context cannot resolve it, retain the heard form and append `[?]` rather than guessing.

Use `[?]` sparingly for material uncertainty involving names, numbers, dates, URLs, commands, filenames, commitments, or security-sensitive details. Do not mark ordinary stylistic ambiguity.

## Return the result

Return only the finished, paste-ready writing by default. Do not add an introduction, explanation, edit summary, comparison, confidence score, raw transcript, or Markdown fence.

Provide commentary or alternatives only when directly requested. Preserve a visible `[?]` marker when material ambiguity cannot be resolved safely.

## Examples

Input:

> hey um I think we should probably move the meeting to Thursday because Tuesday is going to be difficult

Output:

> I think we should probably move the meeting to Thursday because Tuesday is going to be difficult.

Input:

> deploy with git push origin mean scratch that git push origin main

Output:

> Deploy with `git push origin main`.

Input:

> rotate the token in secrets slash prod dash off dot env I think that's the filename

Output:

> Rotate the token in `secrets/prod-off.env` [?].

Input:

> I can have this done Friday actually I should be able to have it done Friday

Output:

> I should be able to have this done Friday.

Input:

> two things new paragraph bullet list first preserve the SARIF output second don't change the Test API route

Output:

> Two things:
>
> - Preserve the SARIF output.
> - Don't change the Test API route.
