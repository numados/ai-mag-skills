---
name: mag-rust-unsafe-review
description: Be the primary reviewer for unsafe Rust, raw pointers, FFI, unsafe traits, unsafe Send/Sync implementations, or safety-sensitive abstractions by tracing validity obligations to executable guards and verification evidence, even when a broader review is also requested.
---

# Rust Unsafe Review

## When to Use

Use when the requested outcome is an unsafe or soundness audit and the scope contains unsafe blocks or functions, raw pointers, unions, transmute, FFI, unsafe traits, unsafe impl Send/Sync, custom allocators, pinning invariants, or a safe abstraction over unsafe code. Explanation-only requests remain explanation tasks even when the code contains unsafe.

When the code contains atomics, custom synchronization, or reclamation, load `references/concurrency-model.md` and trace its state and lifetime invariants.

This skill is read-only unless the user separately authorizes a fix.

## Review the contract

For every unsafe operation, identify:

1. the exact operation and its required safety conditions;
2. the source of each condition: checked locally, guaranteed by a type, guaranteed by a caller, or assumed;
3. lifetime, initialization, alignment, size, aliasing, mutability, provenance and concurrency obligations;
4. panic, reentrancy, cancellation and callback behavior;
5. the smallest safe boundary that contains the invariant.

A SAFETY comment is evidence only when it names the real obligation and the surrounding code or caller makes that obligation true. Do not accept “the caller guarantees safety” without stating what is guaranteed and why.

## Raw pointers and memory

Check separately:

- valid reads/writes for the complete type size, not merely a byte prefix;
- initialization and validity of every bit pattern;
- alignment and whether read_unaligned or raw address construction is required;
- pointer arithmetic bounds and one-past rules;
- aliasing and mutation exclusivity;
- lifetime and deallocation order;
- integer overflow in offsets and lengths;
- panic paths that can leave an invariant broken.

Do not treat read_unaligned as a bounds check. Do not infer that an integer address is a valid pointer.

## FFI and unsafe traits

For FFI, inspect ownership transfer, representation, nullability, lifetimes, thread affinity, callback reentrancy, panic/unwind policy, and cleanup on every return path.

For unsafe trait implementations, verify every promised property. For unsafe Send/Sync, trace all reachable mutable state, interior mutability, raw pointers and destruction behavior. For pinning, verify that values cannot move after the invariant is established.

## Verification evidence

Use static reasoning first. If authorized and supported by the project, use targeted tests, Miri, sanitizers, fuzzing, or concurrency tools. State their limits:

- a passing Miri run covers only executed scenarios and supported operations;
- sanitizers do not prove Rust aliasing or all undefined behavior absent;
- fuzzing explores inputs, not the entire state space;
- Loom explores modeled schedules and has unsupported features.

Do not introduce unsafe merely to optimize a safe implementation.

## Output

~~~markdown
# Unsafe review — <scope>
Verdict: SOUND | NEEDS CHANGES | BLOCKED

## Contracts
- operation: obligation → evidence or missing guard

## Findings
- path:line — violated obligation → reachable consequence → fix direction

## Verification
- checks actually run and their limits

## Not verified
- missing caller, ABI, target, feature, or runtime evidence
~~~

A missing contract can be a finding even when a failure was not executed, but distinguish a proven violation from an unresolved obligation.
