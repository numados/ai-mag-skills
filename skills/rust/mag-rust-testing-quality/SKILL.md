---
name: mag-rust-testing-quality
description: Design or assess Rust test strategy and quality gates at behavior seams, including unit/integration/doc tests, property tests, fuzzing, feature matrices, MSRV, Miri, Loom, Clippy, and dependency policy; use for test strategy, not ordinary feature implementation.
---

# Rust Testing Quality

## When to Use

Use when adding tests, assessing coverage, designing a test strategy, introducing property tests or fuzzing, checking feature combinations, or defining Rust CI quality gates. Load `references/concurrency-model.md` when the tested invariant concerns atomics, publication, waits, locks, or reclamation.

Do not equate line coverage, one passing example, or a tool's green result with proof of correctness.

## Start from behavior

1. Identify the invariant or user-visible contract.
2. Choose the narrowest seam that observes it without testing private implementation details unnecessarily.
3. Include success, boundary, invalid, error, cancellation, concurrency and recovery cases relevant to the behavior.
4. Preserve deterministic fixtures and explain tests that depend on time, network, filesystem, randomness or external services.

Use unit tests for private invariants, integration tests for public contracts, doc tests for documented usage, compile-fail or UI tests for type-system and diagnostic contracts, and end-to-end tests only where integration behavior matters. Run examples and promised `no_std` targets when they are part of the project contract, and check generated-code drift where applicable.

## Property and fuzz testing

Choose a property with an oracle:

- round-trip or inverse relationship;
- invariant preservation;
- equivalence to a trusted implementation;
- monotonicity, idempotence or bounded resource behavior.

Reject tautological properties that call the same implementation as both system and oracle. For fuzzing, define input construction, corpus ownership, crash replay, regression fixtures, timeout/resource limits and sanitizer policy. A fuzz target is a separate executable surface; follow the repository's cargo-fuzz/workspace convention.

Randomized tests find explored failures; they are not exhaustive verification.

## Configuration matrix

For supported repositories, derive the matrix from declared contract:

- MSRV and current stable;
- default and no-default features;
- meaningful optional-feature combinations;
- workspace members, targets, examples, benches and docs;
- supported platforms or runtimes.

Avoid blindly testing every feature power set when combinations are invalid or the cost is disproportionate. Record excluded combinations and why.

## Tool limits and gates

- cargo fmt checks formatting, not behavior.
- Clippy catches selected patterns; repository lint policy decides severity.
- Miri explores executed code and does not detect every undefined behavior.
- Loom explores modeled schedules and cannot represent every runtime or platform feature.
- cargo-audit checks known advisories; cargo-deny can enforce broader dependency, license and source policy. Neither proves a dependency is safe.
- Public libraries may need API compatibility checks and doc-test coverage.

Use repository-supported commands and pin or document tool versions when reproducibility matters.

## Output

Return a test matrix with behavior, seam, fixture, command, expected signal and limitation. Include missing evidence, flaky or environmental tests, and the smallest high-value additions. Do not recommend a tool without identifying the property or policy it verifies.
