---
name: mag-task-execution
description: Execute an authorized development plan or resume a multi-phase implementation, verifying each phase and reviewing the completed change. Use for planned implementation and task resumption; not for research-only, planning-only, history questions or standalone code review.
---

# Task execution

Implement only the authorized outcome. Scale the process to the change: a small standalone edit does not need a formal multi-phase workflow. A saved plan or task record alone is not permission to implement, commit, push, deploy, install dependencies or change remote state.

## Restore and check

- Identify the request, authorized scope, relevant plan, decisions and acceptance criteria. For resumed work, use the available task record and latest meaningful event, then inspect linked details as needed. If identity, authorization or a consequential decision is unclear, ask rather than guessing. Continue independent work only when it is safe and authorized.
- Inspect repository instructions, current code, tests and working-tree changes before editing. Preserve unrelated work. Verify that the plan still fits current source and requirements; if source or scope has materially drifted, stop affected work and revise the plan, seeking approval for a scope change. Do not treat an old excerpt as current source.
- Identify dependencies, unresolved decisions and required checks for the next phase. Do not execute a step that could expose behavior dependent on an unresolved decision. If a necessary source, tool or permission is unavailable, report the limitation and stop the affected work rather than inventing evidence or approval.

## Execute and verify

- Work in coherent phases, using appropriate implementation and testing practices. Optional specialized skills may help but are not required. Make the smallest complete change for each authorized outcome; avoid unrelated cleanup.
- Verify each phase with focused, executable checks against the intended behavior and relevant integration. Record actual results, failures and checks not run; an environment failure is not proof of a passing or failing behavior. Investigate failures before continuing dependent work.
- Review the completed changes against scope, contracts, correctness and tests. Validate suspected findings against evidence; fix confirmed in-scope issues, rerun affected checks and re-review the fixes. Repeat until no confirmed actionable issue remains, or stop with the specific blocker and remaining risk. Do not claim a clean review if verification was incomplete.

## Preserve and report state

When the user or surrounding workflow expects task tracking, use its established, accessible and authorized record. At meaningful phases and review iterations, preserve the task and phase, intent versus actual changes, decisions and links to evidence, checks and results, unverified items, blockers and next action. Keep corrections understandable rather than concealing earlier conclusions. A failed record write is not a successful log: disclose it, retain a usable handoff, and ask how to persist it if needed. Do not invent a storage location, assume an available tool has write access, or write remotely without authorization. If tracking is expected but no suitable destination is known, ask where to save the handoff; a small standalone task needs no new journal by default.

Report what changed, verification actually performed, remaining risks or blockers and next action. Distinguish completed work from planned or unverified work.
