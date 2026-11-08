# Async lifecycle and progress contracts

Load this reference when the code creates futures or tasks, races operations, implements wakeups, bounds work, or shuts down a runtime. Runtime-specific behavior must be checked against the resolved runtime version and official documentation.

## Polling and wakeups

A future makes progress only when its `poll` implementation runs, but constructing a future may already start external work, and work driven by other tasks or threads can continue without polling. `Pending` is correct only when the future has arranged for the current task to be woken when progress may be possible. A poll implementation should return promptly and must not perform blocking I/O, blocking waits, or unbounded CPU work.

For a shared readiness protocol, check the predicate, register or replace the current waker, and re-check the predicate under the same synchronization protocol before returning `Pending`. A wakeup is a hint to try again, not proof that the predicate is true. Avoid self-wake busy loops that turn missing readiness notifications into CPU consumption.

Raw wakers, pin projections, and self-referential state are unsafe contracts. Do not copy a teaching executor or `RawWaker` example without proving clone, wake, drop, ownership, and lifetime behavior.

## Composition and spawned tasks

Composition such as `join!` drives child futures as part of the current task. A spawned task is separately owned by the runtime and normally adds `'static` and possibly `Send` bounds. Record who owns each task, who observes its result, and what dropping the parent or a handle does. A dropped handle may detach rather than cancel. Joining observes completion and failure; it is not the same as merely dropping a handle.

Do not infer cancellation, cleanup, fairness, or detach behavior from a method name. Check the exact runtime contract.

## Cancellation and bounded work

Analyze every await boundary that can be dropped or raced. Check whether cancellation loses queue position, partial writes, permits, state transitions, or retry progress. A future is cancellation-safe only when its operation-specific contract permits drop and restart at that point.

A bounded input channel does not by itself bound spawned tasks, semaphore waiters, or started blocking work. Acquire capacity at the boundary that owns the work. If a wrapper can be aborted while the underlying blocking closure continues, the permit must remain associated with that actual work, or a fixed worker pool/cooperative stop mechanism must enforce the bound.

Keep synchronous I/O, blocking waits, and CPU-heavy work separate. `spawn_blocking` or an equivalent mechanism moves work; it does not automatically make it interruptible. Verify abort and runtime-shutdown behavior for the exact runtime version.

## Shutdown and recovery

Define admission stop, the signal, drain or discard policy, worker ownership, completion waiting, and failure reporting. Await worker completion instead of sleeping for a fixed duration. Decide what happens to in-flight, queued, and newly submitted work after timeout, restart, or partial failure.

## Testing

Use deterministic poll points or a controlled runtime when possible. Test cancellation at each operation-specific boundary, sender and receiver loss, queue limits, worker failure, shutdown completion, and restart behavior. Stress tests and schedule exploration increase evidence but do not prove all schedules or runtime/platform behavior.
