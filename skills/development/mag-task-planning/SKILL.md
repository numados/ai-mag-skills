---
name: mag-task-planning
description: Create an actionable implementation plan for a development task from a written request, tracker URL or ID, or available research. Use when the desired outcome is a task plan, including a plan grounded in existing code. Do not trigger merely for a link, a request to implement, review changes, or design an isolated interface.
---

# Task planning

Produce a plan that someone can execute and verify, without implementing it. Planning is read-only: do not modify product files, trackers, or remote state. Reply in chat by default; write a plan file only when requested or permitted by the surrounding workflow. A request for a plan does not authorize implementation.

## Establish the task and evidence

- Identify the desired outcome, authorized scope, constraints and supplied sources. A written task is enough to start; a research handoff is optional. Distinguish requirements and user decisions from observed facts, proposals and assumptions. Repository conventions inform implementation but do not authorize new product behavior.
- Resolve a tracker URL or ID with suitable available read-only capabilities, without assuming a provider or access. If an ID is ambiguous, ask which source it identifies. If a decision-relevant source is inaccessible, report the gap and request the smallest useful excerpt or clarification. Do not install tools, authenticate or change state without authorization.
- Inspect relevant current repository instructions, code, contracts, configuration, tests and consumers as needed. When current source is accessible, inspect it instead of assuming an older excerpt or handoff still applies. When it is unavailable, distinguish supplied excerpts from verified current behavior and give a useful preliminary plan where possible. Before implementation, verify the actual source; if it differs materially, stop and revise the affected plan before proceeding. Cite useful paths or source references, and distinguish an unsuccessful search from proof that something does not exist.

## Shape the plan

- Map each requirement to the existing integration points and intended change, including affected behavior, interfaces, data and downstream consumers where relevant. Describe coherent, appropriately sized steps and dependencies; avoid speculative layers or unrelated cleanup.
- Do not silently add scope-bearing behavior such as a public interface, persistence, infrastructure or new failure semantics. Label implementation choices as proposals and explain material trade-offs; established facts do not grant product scope. Even a conditional scenario needs evidence or approval for its expected outcome; do not invent failure or recovery rules. Seek authorization when a choice changes scope or requires a product decision.
- Investigate decision-relevant unknowns before asking. If evidence cannot resolve a consequential choice, state its impact and ask the smallest specific question that unlocks the next decision; avoid a speculative checklist of possible future requirements. For each step that could expose behavior affected by that decision, explicitly mark the step blocked and name the decision or evidence that unblocks it; do not list it as an independently executable change or treat an unverified option as settled. Technical separability alone does not establish safety. Before reporting, check the dependency labels: if a step depends on a blocked decision, that step must also be blocked, even if presented as a draft or proposal. Check acceptance criteria and tests for conflicting expected outcomes. Continue planning genuinely independent work and label non-blocking uncertainties without delaying the whole plan.
- Define observable acceptance criteria and executable, focused checks that exercise the actual behavior and integration, including relevant failure and compatibility cases. Identify existing tests or commands when verified; otherwise describe a concrete test and disclose that its command or environment needs confirmation. Do not claim checks have run when they have not.

## Report

Right-size the response to the task: state the outcome and scope, relevant evidence and current integration, ordered steps, acceptance criteria and verification, and material risks or open decisions. Separate authorized requirements from proposed choices and note inaccessible sources and unverified assumptions. For a small change, a compact list may be sufficient; for a blocked decision, provide the useful partial plan and focused question rather than false precision.

When the user or surrounding workflow expects task tracking, prepare a plan handoff with task identity, scope and approval status, evidence, phases and dependencies, checks, open decisions and next action. Save it locally only when the destination and write are authorized; otherwise provide it in chat for the surrounding workflow. Do not invent a destination or write to remote state. If persistence is expected but no suitable destination is known, ask; report any failed write. A saved plan does not authorize implementation.
