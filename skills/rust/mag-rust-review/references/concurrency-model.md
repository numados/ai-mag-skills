<!-- Generated from skills/rust/mag-rust-async-reliability/references/concurrency-model.md. Do not edit this copy; run python3 scripts/sync-skill-resources.py in the catalog repository. No source checkout is needed at runtime. -->

# Concurrent Rust proof checklist

Load this reference for atomics, custom locks or channels, condition variables, publication, unsafe synchronization, or claims about lock-free behavior. Safe atomic code does not automatically require an unsafe review. Use the unsafe section when the design contains unsafe code or a safe abstraction over unsafe state.

## State the invariant

Write a small table before choosing an ordering:

| State | Who reads or writes it | When is it initialized | What makes it visible | What keeps it alive |
|---|---|---|---|---|

Identify whether the requirement is an independent atomic value, a coherent snapshot, publication of non-atomic data, mutual exclusion, progress, or memory reclamation. “No data race” is not the same as “the reader sees a valid related state.”

## Publication and ordering

For publication, identify the release operation, the acquire operation that observes its value, and the non-atomic data covered by that happens-before edge. `Relaxed` gives atomicity and per-atomic modification order, not cross-variable publication. It can be correct for independent counters when no coherent snapshot or publication invariant exists. Do not replace a missing invariant with blanket `SeqCst`.

For read-modify-write operations, reason about the load and store parts separately. Acquire affects the load part and Release affects the store part. A compare-exchange failure is a load, not a store. Verify the legal success and failure orderings against the current Rust documentation before prescribing a combination. Use weak compare-exchange only where spurious failure is handled by a retry loop.

## Waiting and wakeups

A notification is not the condition. Associate waiting with a predicate and re-check it after every wake, including spurious wakes. The state transition and the decision to sleep must use the synchronization protocol that prevents a lost wake. For condition variables, parking, futex-like waits, and runtime notifications, verify the abstraction's exact contract rather than applying one universal recipe.

## Unsafe synchronization

`UnsafeCell` permits interior mutation but supplies no synchronization. For a custom guard or lock, record initialization, read/write exclusivity, the lifetime of references, unlock-on-drop behavior, panic and leak paths, deallocation ownership, and every `Send`/`Sync` bound. Exclusive access can require `T: Send`; shared references to `T` require `T: Sync`. An acquire/release pair does not repair an incorrect auto-trait implementation.

For raw pointers or lock-free structures, answer what keeps each allocation alive while it is read and what prevents ABA or address reuse. `SeqCst` does not solve use-after-free, reclamation, or lifetime errors. Prefer standard synchronization or a maintained reclamation scheme unless a custom primitive is required and justified.

## Portability and evidence

Separate correctness from target-specific performance. “Works on x86” is not evidence for weakly ordered targets. Check target atomic availability, cache contention, OS primitives, and the supported platform matrix. A passing Miri run covers executed supported interpreter paths. Loom covers its model and schedules. Stress tests do not prove rare schedules, starvation, FFI behavior, timeouts, reclamation, or every processor.
