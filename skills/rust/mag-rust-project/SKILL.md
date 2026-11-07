---
name: mag-rust-project
description: Structure or extend a Rust package, crate, or workspace by following repository precedent, checking edition/MSRV/features and dependency compatibility, and choosing test and module boundaries without speculative reorganization.
---

# Rust Project

## When to Use

Use when creating a Rust project, adding a crate or target, deciding where a module or test belongs, splitting a library and binary, or checking a version-sensitive API before implementation.

Do not use this skill to refactor an existing project without a concrete structural request.

## Establish the project contract

1. Locate the nearest Cargo.toml and read repository guidance, CONTRIBUTING files, toolchain files, Cargo config, rustfmt, Clippy, deny, and CI configuration.
2. Identify whether the target is an application, library, proc-macro, no_std crate, workspace member, example, benchmark, or fuzz target.
3. Record edition, declared rust-version/MSRV, default and optional features, dependency declarations, workspace inheritance, and public API policy.
4. Inspect analogous modules, targets, tests, and dependency direction before choosing a location.
5. Preserve existing structure. Do not introduce a workspace, lib target, new crate, or new public API only because it is fashionable.

## Compatibility

Separate three facts:

- The manifest range is the compatibility promise to downstream users.
- Cargo.lock is the locally resolved graph and is authoritative for reproducing this checkout.
- MSRV is the minimum compiler version the package promises, not the compiler currently installed.

For a library, verify new syntax and dependency APIs against the declared MSRV and the supported dependency range. For an application, the lockfile may be the main reproducibility contract, but still respect the repository's stated policy. If the lower bound matters, use the repository's minimal-version or MSRV job; do not invent a command that the project does not support.

Before using an unfamiliar API, check local dependency source or generated docs, then the exact resolved docs.rs version and authoritative Rust/Cargo documentation. State any unverified stabilization or feature assumption.

## Layout guidance

Prefer these only when they match the project:

- Library logic in src/lib.rs and concept modules; a binary target remains a thin argument/IO/error boundary.
- Unit tests beside private logic; integration tests in tests/ named by behavior or scenario.
- Examples and benchmarks compile as part of their intended verification.
- Fuzz targets normally use a separate fuzz workspace root and are not casually added as a parent workspace member.
- Keep dependency direction acyclic and make public exports deliberate.

## Decision output

Return:

1. Current project shape and relevant contract.
2. Recommended target path and why existing precedent supports it.
3. Public API, dependency, feature, MSRV, and test consequences.
4. Verification commands appropriate to the repository.
5. Unknowns that require source or documentation lookup.

Do not claim an API exists, a feature is enabled, or a build passed until verified.
