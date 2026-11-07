---
name: mag-dotnet-async-reliability
description: Design, review, or fix .NET async and concurrency reliability — Task/ValueTask ownership, CancellationToken propagation, linked token lifetime, exception observation, Task.WhenAll/WhenAny/WaitAsync semantics, graceful shutdown and hosted/background services, bounded channels and backpressure, shared mutable state, and ConfigureAwait rules. Use when the user asks to design, review, diagnose, or fix async/await, cancellation, timeouts, concurrency, parallel work, or shutdown in C#/.NET code. Use mag-dotnet-performance instead for measured throughput or allocation optimization, mag-csharp-review for a read-only multi-category review where async is not the dominant concern, and mag-aspnet-core for request-pipeline, middleware, and DI-lifetime specifics.
---

# .NET Async and Concurrency Reliability

## When to Use

Use for Task/ValueTask code, async/await, cancellation tokens, timeouts, linked CTS, WhenAll/WhenAny, channels and producer/consumer queues, Parallel.ForEachAsync, semaphores and shared state, BackgroundService/IHostedService, graceful shutdown, or any concurrent C#/.NET system whose correctness depends on cancellation, ordering, ownership, or shutdown behavior.

Do not treat parallelism as automatically beneficial, and do not optimize for throughput here: measured performance belongs to `mag-dotnet-performance`. Do not reroute a review/diagnosis/design request into an edit. Do not apply a "never hold a lock across await" rule without identifying the primitive and the actual wait path.

## Mode and scope govern what you may do

1. Establish the mode from the request: **review/diagnose/design** is read-only; **fix/implement** permits editing only the files and behavior the user authorized. Do not broaden a fix into a refactor, dependency change, or shutdown redesign.
2. Read repository instructions and the relevant `.csproj`/`.sln`, then detect the contract separately: **SDK version, LangVersion, target framework (TFM), runtime, and package/analyzer versions** are independent facts and must not be conflated. Gate every version-sensitive API against the actual TFM, not the newest you know.
3. Read `references/lifecycle.md` when you need the verified API-version matrix, the full lifecycle model template, or the ownership/cancellation decision paths.

## Model the lifecycle first

Before judging or changing any async code, describe each task and operation:

- who creates it, who starts it, and who awaits it;
- what makes progress and what can suspend it;
- how cancellation, timeout, fault, and process shutdown affect it;
- how exceptions are observed and who observes them;
- what resources, guards, and registrations it holds and when they are released;
- what happens after partial failure, retry, or restart.

A `Task` that nobody awaits or observes can hide a fault until finalization; a `ValueTask` may be consumed once. Do not assume "cancelled" means "stopped": the underlying work keeps running unless the token is actually threaded into it and honored.

## Cancellation ownership and propagation

- The caller owns the `CancellationToken` and creates/disposes the `CancellationTokenSource`. A callee observes the token but must not dispose a token or CTS it did not create.
- Thread the caller's token through every awaitable that accepts one, end to end. Silently dropping it mid-chain breaks prompt cancellation and shutdown.
- Do not replace a real token with `CancellationToken.None` just to make a signature compile; that permanently disconnects the operation from its caller.
- A `CancellationToken.Register` callback returns an IDisposable registration: dispose it when the interest ends, or it leaks and fires later than intended.
- Do not call `CancellationTokenSource.Cancel()` and assume it is the same thing as the caller having stopped waiting — distinguish the two (see timeout below).

## Linked token sources and timeouts

- Combine a caller token with a deadline via `CancellationTokenSource.CreateLinkedTokenSource` and set the timeout with `CancelAfter`. Dispose the linked source and any registrations once the operation finishes; a leaked linked CTS keeps the registration graph alive.
- Keep the caller token and the timeout as separate tokens, or at least record which one fired, so you can attribute the cancellation to a deadline versus a caller disconnect.
- Prefer `Task.WaitAsync(TimeSpan, CancellationToken)` (.NET 6+, with `TimeProvider` overload in .NET 8+) over ad-hoc `Task.Delay` races. `WaitAsync` throws `TimeoutException` on timeout and `OperationCanceledException` on cancellation, and — critically — it does **not** cancel the underlying task.

## Exceptions and observation

- Never let a task's exception go unobserved. In .NET Framework 4.5+ and .NET Core/.NET 5+, an unobserved exception is **not** rethrown from the finalizer — it is silently swallowed (`TaskScheduler.UnobservedTaskException` fires but by default does nothing), so the failure is lost. Only .NET Framework 4.0 terminates the process by default. Store and await/observe every started task.
- `async void` is only for event handlers. An exception it throws escapes to the synchronization context and can crash the process. Prefer `async Task`.
- When one task in `Task.WhenAll` faults, the returned task is faulted but the other tasks keep running — `WhenAll` never cancels siblings. Awaiting throws the first exception; `task.Exception` holds the full `AggregateException` if you need every failure.

## WhenAll, WhenAny, WaitAsync semantics

- `Task.WhenAny` returns a proxy task for the first completion. To surface the result or exception you must await the **original** task, and you must still observe or cancel the losers, or they leak unobserved.
- For a task-per-item fan-out, bound the degree of concurrency (semaphore or `Parallel.ForEachAsync`), because `WhenAll` over an unbounded collection issues unbounded parallel work.
- Do not assume cancellation propagates to siblings through `WhenAll`/`WhenAny`/`WaitAsync`; it does not automatically. Each operation must receive the token.

## Timeout versus cancellation, and who stopped waiting

- A timeout means a deadline passed; the operation may still be running. A cancellation is a cooperative request to stop. Report which occurred, and do not collapse one into the other.
- When a caller cancels its wait (disconnect, `WaitAsync`, `WhenAny` timeout branch), the wait ends but the underlying work may not. Check whether the token reaches the operation and whether the operation honors it before claiming the work stopped.

## Graceful shutdown and background services

- Prefer an explicit shutdown path plus ownership of every worker (`BackgroundService`, `IHostedService`, or an equivalent supervisor). Shutdown must: stop admitting new work, signal workers with the stopping token, drain or discard queued work by stated policy, await completion within a bounded grace period, then report what did not finish.
- Sleeping a fixed duration is not proof of shutdown. Assert that workers actually stopped and that no new work was admitted after the signal.
- `BackgroundService.ExecuteAsync` is a `Task`; it must return when the stopping token is signaled, not run forever ignoring it.

## Bounded channels, work queues, and backpressure

- Bound any queue fed by external or untrusted producers. Use `System.Threading.Channels` and choose `BoundedChannelFullMode` (`Wait`, `DropWrite`, `DropNewest`, `DropOldest`) deliberately, then document the chosen drop/wait behavior.
- Define what happens when the reader completes or a writer fails: the `Channel` completes the reader/writer, and code must handle `ChannelClosedException` and observe completion rather than spinning.
- Prefer `ReadAllAsync`/`await foreach` over hand-rolled receive loops; prefer a bounded channel plus a single consumer over unbounded `Task.Run` fan-out.

## Shared mutable state

- Identify the synchronization primitive, its scope, lock ordering, deadlock/starvation/reentrancy, and every await or callback that can occur while state is held.
- Do not hold a `Monitor`/`lock` across an `await`: `Monitor` is thread-affine and an async continuation may resume on another thread. When a critical section must span an await, use `SemaphoreSlim.WaitAsync` (with a clear ownership/dispose story) or restructure so the await does not hold state.
- Use `Interlocked` for atomic scalar updates, and treat any state shared across tasks as needing an explicit invariant and owner.

## ValueTask consumption hazards

- Consume a `ValueTask` exactly once. Storing it for one later await can be valid when the producer's lifetime permits it; re-awaiting, consuming a copy more than once, or awaiting it from multiple continuations is unsafe because it may wrap a pooled `IValueTaskSource` (common in ASP.NET Core high-performance paths).
- Convert with `AsTask()` when the result must be awaited more than once or combined in `WhenAll`. Prefer plain `Task` unless the pooling/zero-allocation benefit is real and understood.

## Anti-patterns to check

- `Task.Run` around I/O-bound work — it burns a thread-pool thread instead of using the async I/O path. `Task.Run` is for CPU-bound work or for offloading from a UI/synchronization context, not for "making it async".
- Unconditional `ConfigureAwait(false)` — it is a library-versus-application decision, not a blanket rule. Library code avoids capturing the context; UI and request-scoped application code often must capture it. State the reason, do not sprinkle it.
- Blind concurrent use of scoped resources (DI scoped services, `DbContext`) across parallel tasks — a scope is not thread-safe and must not be shared across concurrent consumers.
- Assuming `Cancel()` or `WaitAsync` stopped the underlying work when the token was never threaded in.

## Test the failure, cancel, and shutdown paths

Add or update tests at the reliability seams, not just the happy path:

- cancellation: assert `OperationCanceledException` and that the underlying resource was actually released, not merely that the exception surfaced;
- timeout: assert `TimeoutException` and that the deadline is distinguishable from cancellation;
- shutdown: assert workers stop within the grace period and that admission stopped;
- backpressure: assert the bound holds and the chosen drop/wait policy fires;
- exception observation: assert every started task is awaited/observed.

State the actual checks run and their real results — the command or harness used and the observed outcome. Never claim a path passed from an unrun check.

## Output

Report a lifecycle map, concrete failure paths, findings by category (ownership, cancellation, linked-token lifetime, exception observation, WhenAll/WhenAny/WaitAsync, shutdown, channel/backpressure, shared state, ValueTask), recovery ownership, tests needed, and verification limits. Distinguish proven bugs from design questions, and name the exact lines or smallest causal anchor for each finding.
