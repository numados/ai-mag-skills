# Anti-patterns and examples

Common ways shift-left orchestration goes wrong, and what to do instead.

## Forcing a method or metric

- **Forcing TDD.** "Write the test first" is `mag-tdd`'s decision, only when the user wants test-first. Shift-left cares about when a risk is caught, not the order of red and green. A verification matrix is valid without a single test-first cycle.
- **Forcing a coverage percentage.** A line covered by an assertion-free test proves nothing. Report explored paths and gaps; do not set a number the project does not already enforce.
- **Forcing a test pyramid.** A request that is mostly one integration boundary does not need a layer-per-layer pyramid. Choose seams by risk.
- **Forcing live network or real services.** A recorded or fake contract is often the earliest reliable seam. Reach for a real provider only when the provider contract itself is the risk under test.
- **Forcing all categories.** Security, performance, and compatibility are candidate risk domains, not required rows. Include only what the change can actually introduce.

## Claiming a seam is reliable when it is not

- A unit test that asserts internal steps passes while the integration is still wrong; it is not the earliest reliable seam for the integration risk.
- A test depending on wall-clock time, network, or randomness is environmental; its green is not proof.
- A command the agent did not run is "not run", never "passing".

## Duplicating specialized skills

- Re-implementing .NET seam and test-platform detection duplicates `mag-dotnet-testing-quality`. This skill names the seam and hands the mechanics over.
- Re-implementing red-green-refactor duplicates `mag-tdd`.
- Re-reviewing the whole change duplicates `mag-code-review`; this skill reports gaps, the review reports defects.

## Ignoring repository rules

A project's existing test framework, seam conventions, and CI gates are authoritative. A generic recommendation that contradicts them is wrong even if it looks "more shifted left". Detect the actual conventions first.

## Examples

### A payment integration spanning a new API, a database write, and an external provider

Distinguish risks instead of lumping them into "test it":

- **Business rule** (a discount applies only above a threshold) — unit seam, deterministic, earliest.
- **Wiring** (the handler reads the right configuration and calls the provider with the right key) — integration seam against a fake or recorded provider.
- **Provider semantics** (what happens on timeout) — contract check first; a real provider only if the contract is the risk.
- **Data integrity** (a write and a provider call that must not double-apply) — integration or end-to-end against a real or equivalent store.

Each risk gets its own row and its own seam; none of them is "just write an integration test".

### A cross-stack quality gate

A feature touching a Rust service and a .NET API. The matrix is one view: which risks each side owns, which checks run in CI and in what order, and what can only be verified in a shared environment. The per-stack seam and platform mechanics are handed to `mag-rust-testing-quality` and `mag-dotnet-testing-quality`; the orchestration stays with this skill.

This example is generic: it illustrates a cross-stack boundary, not a specific product. Apply the same split to any two technologies with a shared contract.
