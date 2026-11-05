---
name: task-research
description: Investigate a development task before implementation or planning using a written description or a tracker link or ID. Use when the user asks to research, investigate or establish the context and open questions for a task. Do not trigger merely because a link or ID accompanies a direct implementation, plan-only, internal design or code-review request.
---

# Task research

Establish what is known, what is requested and what remains undecided. Scale the investigation to the task and its risks. Research is read-only: do not implement, change product files or modify tracker or other remote state. Respond in chat unless a file is requested or the surrounding workflow permits one.

## Establish the sources

- Identify the task and its authoritative input: the user's description, supplied documents, tracker item and clarifications as applicable. Read decision-relevant supplied material, including linked sources when accessible and authorized. Do not assume a tracker provider or a particular tool or access method.
- For an ambiguous bare ID, use available context to identify the source; if identity remains ambiguous, ask which tracker or project it belongs to. Use available read-only capabilities to resolve a reference when authorized. Do not install tools, authenticate or expose credentials or sensitive content without authorization.
- If a decision-relevant source is inaccessible, say what could not be read and why, then request the smallest useful input, such as the relevant text. Continue with bounded findings from available evidence; do not invent the missing content.

## Investigate

- Inspect relevant current project instructions, code, contracts, configuration, tests and documentation as available. Trace the affected behavior and its entry points, dependencies and consumers where needed. Prefer focused searches and reads; a search with no matches is not proof that a capability does not exist.
- Separate authorized requirements and scope from existing behavior, technical facts, assumptions, suggestions and potential options. Distinguish the current state from the requested target; an example or proposed solution is not automatically a requirement. A business term does not prove a particular code value, status, mapping or implementation exists: cite the evidence for that mapping or say it is unknown.
- Cite sources and relevant file locations or tracker sections for consequential claims. Verify exact line numbers before citing them; if unavailable, cite the known function or excerpt rather than guessing.
- Check accessible evidence before asking about a discoverable fact. If sources conflict, identify the conflict and its authority rather than silently choosing; a user clarification can define intent but does not by itself prove how current code behaves. When a consequential choice remains unresolved, explain its impact and ask the smallest precise question of the appropriate authority. Prioritize the question that unlocks the next decision; avoid a speculative checklist of possible future requirements. Label non-blocking unknowns without unnecessarily stopping the investigation.

## Report

Summarize the task and its evidenced scope, relevant current behavior and affected areas, constraints or risks, and material open questions. Cite evidence beside claims, distinguish proposals from decisions, and disclose inaccessible sources and investigation limits. Do not imply a complete understanding or guarantee correctness beyond the evidence.

When the user or surrounding workflow expects task tracking, prepare a research handoff with task identity, evidence and sources, decisions, unresolved questions and next action. Save it locally only when the destination and write are authorized; otherwise provide it in chat for the surrounding workflow. Do not invent a destination or write to remote state. If persistence is expected but no suitable destination is known, ask; report any failed write.
