---
disable-model-invocation: true
name: noggin
description: Read, write, and maintain project memory in noggin/ when retrieving project knowledge, recording decisions, or updating its wiki, ledger, vision, and principles.
---

# Noggin

Read `noggin/index.md`, then open only memories relevant to the task. Read
`noggin/vision.md` for scope and `noggin/principles.md` for applicable rules.
If the store is absent, explain that `noggin init --agent codex` creates it;
do not invent existing memory.

Before writing, read [the memory conventions](references/memory.md). Use the
matching template in `templates/`: [vision](templates/vision.md),
[plan](templates/plan.md), [ledger](templates/ledger.md),
[principle](templates/principle.md), or [wiki](templates/wiki.md).
Read only the templates needed for the update.

Search for an existing page before creating one. Update the page that owns the
subject, preserve useful history, and keep its index links current. Record
evidence and uncertainty rather than turning an inference into an established
fact. Prefer a small useful update over a transcript dump.

Use `$noodle` for substantive task planning, `$jot` to capture the current
session, and `$ruminate` to reconcile recent changes with memory. These skills
share the conventions and templates shipped here.
