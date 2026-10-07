# Memory conventions

## Stores and ownership

- `vision.md`: project purpose, goals, scope, and deliberate non-goals.
- `wiki/`: current architecture, domain knowledge, procedures, and explanations.
- `ledger/`: dated accounts of completed work, decisions, outcomes, and useful failed approaches.
- `plans/`: proposed or active work, dependencies, and completion criteria.
- `principles/`: durable rules with rationale, scope, exceptions, and evidence.

`index.md` is the front door. `principles.md` is a dedicated index of principle
pages. Group links under semantic headings such as Core, Architecture, or
Verification. Add a short description beside each link. Do not regenerate
curated indexes alphabetically or introduce a second source of truth.

## Files and links

Use descriptive lowercase hyphenated filenames. Plans use
`plan-<subject>-<short-id>.md`; ledger entries use `YYYY-MM-DD-<subject>.md`.
Choose a short unique identifier for each new plan and keep its filename stable.

Wiki links resolve from `noggin/`, regardless of the source page's directory:
`[[principles/boundaries]]` and `[[principles/boundaries.md]]` are equivalent.
Use whole-document links only: no aliases, heading anchors, or path traversal.
Links between memories use wiki syntax; code and external evidence use ordinary
Markdown links or explicit repository paths and commit identifiers.

When moving a page, update inbound links. Link new pages from `index.md` or a
reachable topic index; link principles from `principles.md`. Keep completed
plans accessible but move their links out of active work sections.

## Structure and evidence

Use the matching template. Required headings are retained; optional sections
are omitted when empty. Replace template prompts with actual content, and never
fill unknown facts just to complete the structure. Wiki body headings may vary
with the subject. Dates are ISO `YYYY-MM-DD` using the user's current date.
Preserve `created` when editing and change `updated` when content changes.

Plan statuses: `proposed`, `active`, `blocked`, `completed`, `cancelled`.
Principle statuses: `proposed`, `established`, `superseded`.
Wiki pages describe current understanding; ledger entries describe events.

Distinguish what the user decided, what code or tests demonstrate, and what is
inferred. Include concrete supporting references and verification limits. A
one-off agent preference is not a durable principle. Establish a principle
when supported by an explicit project decision or demonstrated practice;
otherwise mark it proposed. Existing project instructions retain precedence.

When evidence conflicts with memory, check scope and chronology, update current
knowledge, and preserve historically useful decisions in the ledger. Mark a
superseded principle and link its replacement rather than silently erasing it.
Do not record secrets, full transcripts, or incidental conversation details.
