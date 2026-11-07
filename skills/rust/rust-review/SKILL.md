---
name: rust-review
description: Perform a read-only multi-category review of Rust code, a crate, repository, or diff, reporting only verified correctness, safety, compatibility, reliability, performance, or material maintainability problems; use unsafe-review or async-reliability instead when that specialist scope is primary.
---

# Rust Review

## When to Use

Use for a read-only review of Rust code, a local diff, commit range, crate, repository, or pasted excerpt.

Do not edit source, format files, install dependencies, commit, or post review comments. Do not turn style preferences or generic test advice into findings.

## Scope and method

1. Establish the exact revision and scope. Read repository instructions and the relevant Cargo contract.
2. For a repository, inspect the risk surface in this order: unsafe/FFI, inputs and panics, errors, public API, ownership/allocation, async/concurrency, state/recovery, tests, and quality gates.
3. Trace each suspicion through callers, guards, feature flags, configuration, and consumers. A snippet proves only what it contains; list missing context instead of guessing.
4. Verify candidates with source and focused checks when safe and authorized. Cargo commands can execute build scripts and proc macros and can write Cargo.lock or target; ask before building untrusted code and disclose that limitation.
5. For a diff or commit review, drop candidates that are pre-existing and not activated, exposed, widened, or worsened by the change. For a repository, crate, file, or snippet snapshot review, report a present reachable defect in the requested scope even when no change introduced it. In all modes require a reachable trigger, concrete impact, causal anchor, and evidence.

## Review lenses

Check:

- unsafe validity, alignment, initialization, aliasing, provenance and safety contracts;
- unchecked input, indexing, arithmetic, allocation and panic paths;
- preserved error sources, context, retry semantics and cancellation behavior;
- public API, semver, feature, MSRV, serialization and dependency contracts;
- clones, allocations, blocking work, lock scope, task lifetime and queue bounds;
- state transitions, cleanup, restart, shutdown and recovery;
- tests for changed behavior, failure paths, feature combinations and public docs;
- formatting and lint policy only when it affects the repository contract.

Do not flag a lock across await without identifying the lock type, wait path, lock ordering and concrete consequence. An async mutex may be designed for a guard held across await.

## Findings

A reportable finding must include:

- exact file and line or the smallest causal anchor;
- violated contract or invariant;
- reachable trigger;
- behavior and impact;
- existing guard or why it is insufficient;
- smallest safe fix or regression-test direction.

Classify as Blocker or Issue. Omit formatting preferences and low-value nits. For absence findings, cite the file or manifest and explain the concrete consequence; do not require a fictional line number.

## Output

~~~markdown
# Rust review — <scope>
Revision: <branch/commit/status>
Verdict: SOUND | ISSUES | BLOCKERS

## Blockers
- path:line — problem; trigger and impact; fix direction.

## Issues
- path:line — problem; trigger and impact; fix direction.

## Done right
- concrete verified strengths, or “nothing notable in the reviewed scope”.

## Not verified
- missing callers, unavailable build, untrusted execution boundary, or other limits.
~~~

Report only verified, in-scope findings. Never claim that a clean review proves the absence of all defects.
