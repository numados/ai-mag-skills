# Rust skills

Independent Rust skills for reliable project structure, implementation, review, refactoring, unsafe code, async systems, testing, and explanation.

## Skills

| Skill | Use when |
|---|---|
| [rust-project](rust-project/SKILL.md) | Starting or extending a Rust package, crate, or workspace |
| [rust-implementation](rust-implementation/SKILL.md) | Implementing a Rust feature or fix with tests and verification |
| [rust-review](rust-review/SKILL.md) | Auditing Rust code, a diff, crate, or repository without editing |
| [rust-refactor](rust-refactor/SKILL.md) | Refactoring Rust while preserving observable behavior |
| [rust-unsafe-review](rust-unsafe-review/SKILL.md) | Reviewing unsafe Rust, FFI, raw pointers, or unsafe trait implementations |
| [rust-async-reliability](rust-async-reliability/SKILL.md) | Designing or reviewing async, concurrent, or shutdown behavior |
| [rust-testing-quality](rust-testing-quality/SKILL.md) | Designing tests, property tests, fuzzing, feature matrices, or quality gates |
| [rust-explain](rust-explain/SKILL.md) | Explaining concrete Rust code and its surrounding data flow |

These skills are independent. Use only the skill matching the request. Tool execution, dependency installation, commits, and destructive repository operations still require explicit authorization.

## Design principles

- The repository contract wins: edition, MSRV, features, lints, API policy, and local precedent.
- A lockfile describes one resolved graph; it does not replace a library's declared compatibility range.
- Unsafe comments describe executable invariants; prose is not a substitute for checks.
- Async correctness includes cancellation, shutdown, ownership, backpressure, and recovery.
- Tests provide evidence for covered scenarios, not proof of all behavior.
- Review findings require a reachable failure path and concrete impact.
