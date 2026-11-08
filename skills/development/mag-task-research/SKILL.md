---
name: mag-task-research
description: Understand a development problem, investigate evidence and unanswered questions, and identify a justified solution direction before implementation planning. Use when the user asks to research or investigate a task from a written description, tracker link or ID, or establish what should be solved and why. Research does not produce an implementation plan. Do not trigger merely because a link or ID accompanies a direct implementation, plan-only, internal design or code-review request.
---

# Task research

Understand the problem, what outcome would solve it and which solution direction the evidence supports. Establish what is known, what is requested and what remains undecided. Research may compare and recommend solution directions; concrete architecture, code design, implementation steps and sequencing belong to planning, not this stage. Scale the investigation to the task and its risks. Research does not authorize implementation, product-file changes or tracker updates. Memory-record writes are allowed only through the optional integration below or an otherwise authorized handoff destination; they do not permit other remote mutations. Respond in chat unless persistence is requested or permitted by the surrounding workflow.

## Optional memory

If `mag-task-storage` is available in the harness skill catalog or explicitly supplied, read and apply it to recover this task, find useful existing knowledge and preserve the research handoff within its destination and permission rules. Its presence enables this integration, not automatic knowledge promotion. Without it, keep the existing chat-default behavior and optional handoff; do not require storage or invent a replacement protocol.

## Establish the sources

- Identify the task and its authoritative input: the user's description, supplied documents, tracker item and clarifications as applicable. Read decision-relevant supplied material, including linked sources when accessible and authorized. Do not assume a tracker provider or a particular tool or access method.
- For an ambiguous bare ID, use available context to identify the source; if identity remains ambiguous, ask which tracker or project it belongs to. Use available read-only capabilities to resolve a reference when authorized. Do not install tools, authenticate or expose credentials or sensitive content without authorization.
- Let the questions drive source discovery, not just the supplied source list. Seek relevant evidence through available, authorized capabilities: project and related-system sources, task discussions and decisions, documentation, logs or measurements, and existing knowledge where useful. Check which sources can answer each material question; verify search results against the underlying source. Broaden the search when the evidence is insufficient or conflicting, not merely to use every tool or collect every accessible document.
- If a decision-relevant source is inaccessible, say what could not be read and why, then request the smallest useful input, such as the relevant text. Continue with bounded findings from available evidence; do not invent the missing content.

## Investigate

- Frame the problem before judging a proposed fix: who is affected, what happens now, what outcome is wanted and which constraints define success. Investigate causes when relevant; distinguish an observed symptom from a supported cause. Treat a requested mechanism as a candidate unless the user has made it a requirement.
- Inspect relevant current project instructions, code, contracts, configuration, tests and documentation as available. Trace the affected behavior and its entry points, dependencies and consumers where needed. Prefer focused searches and reads; a search with no matches is not proof that a capability does not exist.
- Separate authorized requirements and scope from existing behavior, technical facts, assumptions, suggestions and potential options. Distinguish the current state from the requested target; an example or proposed solution is not automatically a requirement. A business term does not prove a particular code value, status, mapping or implementation exists: cite the evidence for that mapping or say it is unknown.
- Cite sources and relevant file locations or tracker sections for consequential claims. Verify exact line numbers before citing them; if unavailable, cite the known function or excerpt rather than guessing.
- Check accessible evidence before asking about a discoverable fact. If sources conflict, identify the conflict and its authority rather than silently choosing; a user clarification can define intent but does not by itself prove how current code behaves. When a consequential choice remains unresolved, explain its impact and ask the smallest precise question of the appropriate authority. Prioritize the question that unlocks the next decision; avoid a speculative checklist of possible future requirements. Label non-blocking unknowns without unnecessarily stopping the investigation.

## Synthesize a solution direction

Use the findings to explain what needs to change and why it would address the problem. Compare plausible directions when there is a meaningful choice, including a simpler or existing capability where relevant; recommend the best-supported direction for the evidenced constraints and explain material trade-offs. Keep recommendations distinct from approved decisions and state what evidence could change the conclusion. Do not turn the direction into a development plan, choose detailed new component designs or prescribe files to change and phases; identify affected existing areas and feasibility constraints only as evidence for planning.

## Report

Summarize the problem, desired outcome and evidenced scope, relevant current behavior and affected areas, the supported solution direction, constraints or risks, and material open questions. For consequential questions investigated, capture the answer, supporting evidence and its implication; do not report only the questions left unanswered. Cite evidence beside claims, distinguish proposals from decisions, and disclose inaccessible sources and investigation limits. Do not imply a complete understanding or guarantee correctness beyond the evidence.

When the user or surrounding workflow expects task tracking, prepare a research handoff with task identity, problem and desired outcome, answered questions and evidence, solution directions and rationale, decisions, unresolved questions and next action. Use the optional memory integration when available; otherwise save locally only when the destination and write are authorized, or provide it in chat. Do not invent a destination; a remote memory write requires the integration's explicit permission boundary and does not authorize tracker or other remote changes. If persistence is expected but no suitable destination is known, ask; report any failed write.
