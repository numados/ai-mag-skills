---
name: mag-rust-refactor
description: Refactor existing Rust code without changing observable behavior by freezing a baseline, planning risk-graded moves, preserving public and runtime contracts, and verifying each bounded step; use for refactoring, not review or feature work.
---

# Rust Refactor

## When to Use

Use when the user asks to improve, modernize, simplify, optimize, or restructure existing Rust while keeping behavior stable.

Do not use for a feature or business-rule change. Do not silently change public API, error semantics, evaluation order, cancellation behavior, serialization, or MSRV.

## Freeze the baseline

1. Read repository guidance, Cargo manifests, callers, features, MSRV, lints, tests and benchmarks.
2. Inspect the working tree and preserve unrelated work. Never reset, clean, checkout, or stash the whole tree to undo an agent change.
3. Record current tests, formatting, Clippy status and relevant performance measurements.
4. Decide whether the repository is trusted and whether Cargo execution is authorized. Build scripts, procedural macros and tests execute code; Cargo may write target artifacts or Cargo.lock.
5. If nontrivial logic lacks characterization tests, propose them before changing code.

Behavior includes outputs, errors, panics, side effects, evaluation order, allocation/resource bounds, cancellation, timing-sensitive synchronization, public signatures and feature behavior.

## Plan by risk

Classify every move:

- Mechanical: local syntax or representation change only after proving evaluation order, ownership, panic and error behavior are unchanged.
- Structural: module visibility, crate boundaries, public signatures, trait methods, derives, error types, feature contracts or test seams. Load `references/api-contracts.md` for public type and trait compatibility. Confirm separately.
- Semantic-risk: algorithm, data structure, eager/lazy evaluation, ownership model, generic/`dyn` dispatch, caching, concurrency, allocation, or performance change. Require a benchmark, invariant proof, or explicit user decision.

Examples:

- eager Vec to lazy iterator is semantic-risk when closures can have side effects, panic, return errors, or when the consumer contract changes;
- changing a public return type from a named/boxed trait object to impl Trait is an API change;
- replacing Box with Arc changes ownership and clone behavior;
- const versus static can affect storage, addressability and duplication;
- moving code across modules can change privacy and macro visibility.

## Execute safely

1. Present the ordered plan with exact paths, risk, acceptance checks and non-goals.
2. Implement one bounded step at a time; do not batch unrelated mechanical-looking changes.
3. Run the narrowest relevant tests only after the execution boundary is trusted and authorized; then run formatting/Clippy and workspace/feature checks required by the contract.
4. If a check fails, diagnose the failure and undo only the agent's edits using a saved patch or targeted edit. Do not destroy user work.
5. Measure performance claims; a zero-cost claim needs an argument tied to generated behavior or a benchmark.
6. Request confirmation before public API, semantic-risk, dependency, MSRV, persistence or concurrency changes.

## Output

Report baseline and final verification, changed files, preserved contracts, measured or argued effects, deliberately rejected candidates, and any remaining uncertainty. State explicitly when an axis had no justified change.
