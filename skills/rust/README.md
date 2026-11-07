# Rust skills

Independent Rust skills for reliable project structure, implementation, review, refactoring, unsafe code, async systems, testing, and explanation.

## Skills

| Skill | Use when |
|---|---|
| [mag-rust-project](mag-rust-project/SKILL.md) | Starting or extending a Rust package, crate, or workspace |
| [mag-rust-implementation](mag-rust-implementation/SKILL.md) | Implementing a Rust feature or fix with tests and verification |
| [mag-rust-review](mag-rust-review/SKILL.md) | Auditing Rust code, a diff, crate, or repository without editing |
| [mag-rust-refactor](mag-rust-refactor/SKILL.md) | Refactoring Rust while preserving observable behavior |
| [mag-rust-unsafe-review](mag-rust-unsafe-review/SKILL.md) | Reviewing unsafe Rust, FFI, raw pointers, or unsafe trait implementations |
| [mag-rust-async-reliability](mag-rust-async-reliability/SKILL.md) | Designing or reviewing async, concurrent, or shutdown behavior |
| [mag-rust-testing-quality](mag-rust-testing-quality/SKILL.md) | Designing tests, property tests, fuzzing, feature matrices, or quality gates |
| [mag-rust-explain](mag-rust-explain/SKILL.md) | Explaining concrete Rust code and its surrounding data flow |

These skills are independent. Use only the skill matching the request. Tool execution, dependency installation, commits, and destructive repository operations still require explicit authorization.

## Design principles

- The repository contract wins: edition, MSRV, features, lints, API policy, and local precedent.
- A lockfile describes one resolved graph; it does not replace a library's declared compatibility range.
- Unsafe comments describe executable invariants; prose is not a substitute for checks.
- Async correctness includes cancellation, shutdown, ownership, backpressure, and recovery.
- Tests provide evidence for covered scenarios, not proof of all behavior.
- Review findings require a reachable failure path and concrete impact.
