---
name: mag-shift-left-testing
description: Orchestrate cross-stack quality from requirements and design through implementation and CI. Identify risks early, choose the earliest reliable verification seam for each, and produce a verification matrix before implementation, then hand per-stack work to specialized skills and report unverified gaps. Use when planning a new feature, change, or quality gate that spans components, technologies, or external dependencies and the user wants to know what to verify, where, and how early. Do not trigger for ordinary testing or a small bug fix in an already-understood component, a single test addition, a code review, or a test-first (TDD) request. Repository and project rules remain authoritative.
---

# Shift-left testing

Move verification to the earliest point where it can reliably catch a risk, and keep one view of what is verified, where, and what still is not. This skill owns the cross-cutting quality plan; it does not replace the skills that execute one stack or one practice.

## When to use

Use when the outcome is a quality decision that spans the lifecycle: a new feature or change touching several components, technologies, or external dependencies; a request to decide what to verify before implementation, how to catch problems early, or what CI should gate on; an explicit shift-left request.

Do not use it for:

- implementing a feature or executing a plan (`mag-code-construction`, `mag-task-execution`);
- a code review of a change (`mag-code-review`);
- test-first development of one behavior (`mag-tdd`);
- a single-stack test-strategy or test-boundary question (`mag-dotnet-testing-quality`, `mag-rust-testing-quality`);
- investigating one consequential unknown (`mag-task-gap-drill`);
- a small bug fix or test addition in an already-understood component, where existing conventions already answer the question.

A mention of "tests" or "quality" is not enough to trigger. Trigger on the orchestration need — several risks, several seams, or a decision about when and where to verify — not on the presence of tests in the request.

## Establish scope and facts

1. Identify the requested outcome, authorized scope, requirements, and any design or plan. Distinguish requirements and user decisions from assumptions and proposals; repository and project rules are authoritative over this skill's defaults.
2. Inspect the relevant existing code, contracts, configuration, tests, CI workflow, and project instructions. Reuse verified context while current. State what was inspected and what was unavailable.
3. Do not invent requirements, test categories, or gate levels. A project's existing test and CI conventions take precedence; this skill fills the orchestration gap, it does not impose one.

## Identify risks early

Walk the requirements and design from the point of view of "what can fail and when would we first know":

- business-rule correctness and boundary/error cases;
- integration and seam risks (wrong contract, wrong wiring, wrong lifetime);
- external dependencies (APIs, databases, queues, providers) and their failure, ordering, and recovery semantics;
- concurrency, state, and data-integrity risks;
- compatibility, security, and operational risks — only where the change can actually introduce them.

Prioritize by demonstrated reach and impact, not by listing every possible category. A risk is real only when you can trace a plausible failure and its consequence through the actual design. For each risk, record the observable signal that would count as catching it, not just the risk's name.

For a risk whose behavior depends on an unknown contract or an undecided requirement, flag it as a gap rather than inventing a check. Use `mag-task-gap-drill` when one consequential unknown deserves its own read-only investigation.

## Choose the earliest reliable seam per risk

For each risk, choose the earliest lifecycle point where a check can reliably observe the signal:

- requirement or design review (ambiguity, impossible contract, missing acceptance criterion);
- static or compile-time analysis (types, contracts, lints, forbidden patterns);
- a focused unit or component seam;
- an integration seam against a fake, an in-process host, or a real provider;
- an end-to-end or environment-level check;
- a CI gate or release check.

"Earliest reliable" means both conditions hold: the seam is as early as possible and its signal is trustworthy for this risk. A seam that is flaky, asserts the wrong thing, or depends on unavailable state is not a reliable earliest seam; move later or to a different seam rather than pretend. Prefer the smallest boundary that can observe the signal without pinning implementation details.

Do not force:

- TDD or any test-first order (`mag-tdd` owns that choice, and only when requested);
- a coverage percentage (coverage is an explored-paths signal, not correctness);
- a universal test pyramid (choose seams by risk, not by layer);
- live network or real external services (a fake or recorded contract is often the earliest reliable seam);
- all test categories (include only those relevant to the actual risks).

Load [risk-to-seam decisions](references/decision-matrix.md) for the mapping and trade-offs when choosing or justifying a seam.

## Produce the verification matrix before implementation

Build one table as the single view of what will be verified:

| Risk | Signal to catch | Earliest reliable seam | Check (how to run) | Phase | Gap or open decision |

For each row, name the concrete check (an existing command when known, otherwise a described check and the fact that its command or environment is unconfirmed), the phase where it runs, and any gap. Rows with no reliable seam yet are gaps, not silent omissions. Produce this matrix before implementation so it can steer the plan; it is not a promise that every check already passes.

## Compose with specialized skills

This skill owns the cross-cutting matrix and the risk-to-seam decisions. Hand each execution to the skill that owns it; do not re-implement its guidance:

- implementation plan — `mag-task-planning`;
- internal structure and contracts — `mag-code-design`;
- implementation — `mag-code-construction` or `mag-task-execution`;
- test-first red-green-refactor, only when requested — `mag-tdd`;
- in-stack test seams, fixtures, and test-platform commands — `mag-dotnet-testing-quality` (C#/.NET) or `mag-rust-testing-quality` (Rust);
- post-implementation review of the change — `mag-code-review`;
- a single consequential unknown — `mag-task-gap-drill`.

Read the relevant skill when it is available rather than merely naming it, and apply it under this request's scope and permission boundaries. If a skill is unavailable, proceed with the agent's own knowledge without claiming the skill was used. Do not require, install, or claim unavailable capabilities.

## Report

Lead with the outcome: the risk inventory and the verification matrix, the seams chosen and why, and the gaps that remain unverified.

State honestly:

- checks actually run, with commands and results, versus checks described but not run;
- seams that need an environment, provider, or decision that is not available;
- what repository/project rules overrode this skill's defaults;
- any risk left without a reliable seam, and the smallest next step to close or accept it.

A matrix is a plan, not proof. Do not imply a check passed or a seam is reliable without having observed it.
