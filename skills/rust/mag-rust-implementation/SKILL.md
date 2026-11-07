---
name: mag-rust-implementation
description: Implement an authorized Rust feature or bug fix in an existing repository by preserving local contracts, designing tests at behavior seams, handling errors and ownership explicitly, and verifying the real feature and workspace configuration; use for implementation, not project-only planning or review.
---

# Rust Implementation

## When to Use

Use for an authorized Rust feature, bug fix, API integration, test addition, Cargo change, or bounded implementation task. This skill is self-contained: inspect layout and compatibility here, and use specialized skills only as optional additional lenses.

Do not silently broaden a behavior change into a refactor, dependency upgrade, workspace redesign, or API redesign.

## Before editing

1. Read repository instructions, the relevant Cargo manifests, edition, rust-version/MSRV, features, lints, toolchain and nearby code.
2. Inspect the current branch and working tree. Preserve unrelated edits and staged files.
3. Trace the entry point, callers, state ownership, error paths, cancellation or concurrency boundaries, and downstream consumers.
4. State the intended behavior, affected files, non-goals, and verification plan.
5. For an uncertain requirement, ask the smallest question that changes the implementation. Do not turn a possible improvement into scope.

## Design and implementation

- Prefer the smallest change that fits established boundaries.
- Make invalid states difficult to represent with enums, newtypes, validated constructors, and private fields where justified.
- Preserve error sources and context; do not replace structured errors with strings merely to simplify control flow.
- Make ownership visible. Choose borrow, move, clone, Arc, or interior mutability for a stated lifetime or concurrency reason.
- Bound external input, queues, retries, recursion, allocations, and resource lifetimes where untrusted input can grow them.
- Treat public signatures, feature behavior, MSRV, serialization, and persistence as compatibility surfaces.
- Do not add unsafe for convenience. If unsafe or FFI is required, record validity, aliasing, initialization, lifetime, ABI and unwind obligations in the implementation plan; a separate unsafe review can provide an additional lens but is not a prerequisite.
- In async code, design cancellation, shutdown, task ownership, backpressure, and blocking boundaries before writing the happy path.

## Tests and verification

Add or update tests at the business-rule seam:

- unit tests for private invariants;
- integration or contract tests for public behavior;
- error, boundary, cancellation, and recovery cases;
- feature-gated tests for supported configurations;
- property or fuzz tests when the input space or invariant warrants them.

Use the narrowest repository-supported commands first, then the required workspace/feature matrix. Before any Cargo command, assess whether the repository is trusted and whether execution was authorized: build scripts, procedural macros and tests execute code and Cargo may write target artifacts or Cargo.lock. Use --locked when the repository's policy requires an unchanged lockfile; it does not imply offline execution. Do not build untrusted code without explicit authorization.

Verify formatting, Clippy policy, docs and generated code where applicable. Report exact commands and actual results. Never claim completion from an unrun check.

## Output

Report:

- changed behavior and non-goals;
- files and contracts changed;
- tests added or updated;
- commands and results;
- compatibility, performance, security, and remaining-risk notes.
