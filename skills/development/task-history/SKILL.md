---
name: task-history
description: Recover and explain the current state, decisions, progress or remaining work of a development task from available records and evidence. Use for task history and status questions, including task links or identifiers; not to implement, plan, change records or review code merely because a task is mentioned.
---

# Task history

Answer the user's question from evidence, without changing the task, repository or remote state. Do not assume a tracker, storage format, MCP server or other specific tool.

## Resolve and recover

- Identify the task from the supplied context, link or ID using authorized read-only capabilities. If multiple tasks or sources remain plausible, ask which one is intended. If a necessary source is inaccessible, say so and request the smallest useful reference or excerpt; do not invent its contents.
- Where available, start with the current status and latest meaningful event. Follow links to the plan, decisions, earlier events, code, tests or other evidence only as needed for the question. An index or a latest event may be missing, stale or incomplete: use the accessible sources without assuming an ordering or format they do not establish.
- Distinguish recorded intent, decisions, completed work, actual verification, open issues and proposals. Check current code or tests when the question calls for present behavior or confirmation; a record of intent or a historical passing test does not establish current behavior. Identify conflicting or stale records instead of silently choosing one; cite the relevant sources.

## Answer

Lead with the requested status or conclusion, followed by the evidence, remaining work and material uncertainty. Provide references precise enough to find the supporting record or code; do not guess line numbers. If evidence does not establish an answer, say what is missing and suggest the smallest next check. A history question does not authorize implementation or updating the history.
