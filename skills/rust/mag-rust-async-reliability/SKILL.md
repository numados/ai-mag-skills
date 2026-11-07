---
name: mag-rust-async-reliability
description: Be the primary reviewer or designer for Rust async and concurrent systems, focusing on cancellation safety, task ownership, shutdown, backpressure, lock correctness, blocking boundaries, and recovery behavior.
---

# Rust Async Reliability

## When to Use

Use for Tokio or other async runtimes, channels, spawned tasks, cancellation, select!, locks, streams, timeouts, retries, shutdown, or shared state across tasks.

Do not apply generic “never hold a lock across await” rules without checking the lock type and actual wait path.

## Model the lifecycle

For each task or operation, describe:

- who creates and owns it;
- what starts it and what makes progress;
- how cancellation, timeout, abort, drop and runtime shutdown affect it;
- how errors are observed or propagated;
- what resources and guards are released;
- how shutdown waits for completion and prevents new work;
- what happens after partial failure or restart.

A dropped JoinHandle may detach a task; dropping a future may stop it before its next poll. Do not assume cancellation runs an async cleanup path.

## Cancellation safety

For every select! or race branch, ask whether it is safe to cancel at every await point. If progress or queue position is part of the required contract, prevent cancellation at that boundary or use an operation-specific mechanism such as permits. Otherwise document and test the intended loss of progress or queue position. Treat a future as cancellation-safe only when the operation's contract supports restart/drop at that point.

Check streams, mutex acquisition, channel send/receive, timers, framed IO, retries and database operations against their actual runtime documentation. Do not infer cancellation safety from the method name.

## Tasks, queues and backpressure

- Keep task ownership explicit with JoinHandle/JoinSet or an equivalent supervisor.
- Bound queues fed by external or untrusted input.
- Define what happens when a receiver is dropped, a send is cancelled, or a worker fails.
- Avoid holding a lock while awaiting a slow, unbounded, or reentrant operation.
- Separate blocking CPU or synchronous IO from runtime worker threads using the repository's approved mechanism.
- Make retry budgets, timeouts, jitter and idempotency explicit.

## Locks and shared state

Identify lock type, scope, acquisition order, fairness, poisoning behavior and every await or callback while held. Tokio's async mutex is designed for guards held across await, but that does not make arbitrary critical sections safe: check deadlocks, starvation, reentrancy and latency. A standard mutex may be preferable when no await is needed.

## Shutdown design

Prefer an explicit shutdown signal plus ownership of all workers. Shutdown should stop admission, notify workers, drain or discard queued work by policy, await task completion, and report failures. Sleeping for a fixed duration is not proof that shutdown completed.

## Output

Report a lifecycle map, concrete failure paths, cancellation/lock/queue findings, recovery ownership, tests needed, and verification limits. Distinguish proven bugs from design questions.
