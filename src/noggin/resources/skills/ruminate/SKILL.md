---
disable-model-invocation: true
name: ruminate
description: Reconcile noggin memory with a bounded set of recent commits, working-tree changes, or supplied session records, correcting stale knowledge and consolidating discoveries.
---

# Ruminate

Read `noggin/index.md`, [memory conventions](../noggin/references/memory.md),
and the [templates](../noggin/templates/) relevant to proposed changes.
If noggin is absent, explain how to initialize it before reconciliation.

Use the user's requested time range, commits, paths, or supplied sessions. If
none is given, inspect the working-tree diff and up to ten recent commits,
and state that boundary. Handle a repository without commits gracefully.
Inspect relevant code and tests behind commit summaries before recording claims.
Use session records only when supplied or already accessible within authorized
scope; do not search global agent logs automatically.

Compare the evidence with current memories. Identify missing explanations,
stale facts, conflicting rules, completed plans, and duplicate pages. Check
scope and chronology before treating a difference as a contradiction. Git
history demonstrates changes; it does not prove why someone made them or that
tests passed.

Update current wiki knowledge, add useful ledger outcomes, adjust plans only
when completion criteria are supported, and supersede obsolete principles
with reasons and replacement links. Preserve historically useful context.
Do not promote inferred preferences into established rules. Surface unresolved
contradictions rather than selecting an unsupported account.

Keep semantic indexes and inbound links current when merging or moving pages.
Avoid deleting historical entries merely because they describe older behavior.
Report the review boundary, memory changes, and remaining uncertainties. Make
no edits when the reviewed evidence adds nothing useful.
