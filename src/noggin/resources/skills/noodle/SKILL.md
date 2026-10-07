---
disable-model-invocation: true
name: noodle
description: Plan engineering work in a noggin-enabled project, splitting a task into actionable subtasks with dependencies, affected areas, risks, and verification.
---

# Noodle

Read `noggin/index.md`, `noggin/vision.md`, and applicable principles. Read
[memory conventions](../noggin/references/memory.md) and the
[plan template](../noggin/templates/plan.md). If noggin is absent, explain the
initialization command rather than writing into an invented store.

Investigate the current implementation before deciding the plan. Identify
affected components and their callers, public interfaces, data changes, tests,
and operational consequences. Scale investigation and plan detail to the task.
Avoid turning a small change into a speculative redesign.

Define an observable outcome. Split work into bounded subtasks with their
dependencies and expected results. Account for credible compatibility risks,
verification, and recovery where relevant. Distinguish blocking questions from
choices that can be made using available evidence; record assumptions explicitly.

Search existing plans and update a matching one where appropriate. Save the plan
under `noggin/plans/` using the template and naming conventions, and add a
descriptive wiki link under an appropriate heading in `noggin/index.md`.
Use `proposed` until work starts. Keep status and checkboxes honest as work
progresses; a written plan is not evidence of implementation.

Return the plan path, main affected areas, and unresolved decisions. Planning
alone does not authorize execution; continue implementation when the user's
request already includes it.
