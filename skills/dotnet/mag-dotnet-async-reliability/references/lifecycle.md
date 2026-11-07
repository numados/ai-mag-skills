# Async Reliability — Lifecycle and Version Reference

Load this reference when `SKILL.md` points here for the version matrix, the detailed lifecycle model, or the ownership/cancellation decision paths. It supplements the SKILL; do not treat it as a replacement for reading the actual repository contract.

## Detect the contract separately

These are independent facts and must be detected, not assumed:

- **SDK** — `global.json`, `dotnet --version`, the `Sdk` attribute in `.csproj` (`<Project Sdk="...">`).
- **Language version** — `<LangVersion>` in `.csproj`/`Directory.Build.props` (e.g. `latest`, `12.0`, `13.0`). The SDK's default LangVersion is not the SDK version; it is selected from the effective target framework and compiler context, so it can vary between projects using the same SDK.
- **Target framework (TFM)** — `<TargetFramework>` or `<TargetFrameworks>` (`net8.0`, `net9.0`, `netstandard2.0`, ...). This gates which APIs exist.
- **Runtime** — `dotnet --list-runtimes`, or the `RuntimeFrameworkVersion`/roll-forward policy in deployment.
- **Package versions** — `Directory.Packages.props` or `<PackageReference>` versions (e.g. `Microsoft.Extensions.Hosting`, `System.Threading.Channels`).
- **Analyzers** — `<AnalysisLevel>`, `WarningsAsErrors`, `TreatWarningsAsErrors`, and enabled analyzer packages. These change what the build treats as a failure, independent of TFM.

Verify a version-sensitive rule against the target TFM, not the newest version you know.

## Version matrix (verified against official docs)

Minimum versions for async-relevant APIs. Check the actual TFM before recommending any of these.

| API | Minimum version | Notes |
|---|---|---|
| `System.Threading.Channels` (`Channel<T>`, `BoundedChannelFullMode`) | .NET Core 3.0 (docs list .NET 5 as earliest current); package for older TFMs | Bound queues; full modes `Wait`, `DropWrite`, `DropNewest`, `DropOldest`. |
| `IAsyncEnumerable` / `await foreach` | C# 8 / .NET Core 3.0 | LangVersion-gated, not just TFM. |
| `Task.WaitAsync(TimeSpan)` / `WaitAsync(CancellationToken)` | .NET 6 | Throws `TimeoutException` on timeout, `OperationCanceledException` on cancellation; does not cancel the underlying task. |
| `Task.WaitAsync(TimeSpan, CancellationToken)` | .NET 6 | Adds a timeout and cancellation token to the wait. |
| `Task.WaitAsync(TimeSpan, TimeProvider)` | .NET 8 | The `TimeProvider` overload enables deterministic timeout tests. |
| `Parallel.ForEachAsync` | .NET 6 | Bounded degree of parallelism with cancellation. |
| `PeriodicTimer` | .NET 6 | Timer loop that supports `await` and cancellation cleanly. |
| `ConfigureAwaitOptions` (`None`, `ContinueOnCapturedContext`, `SuppressThrowing`, `ForceYielding`) | .NET 8 | Pass to `ConfigureAwait`/`Task.ConfigureAwait`. |
| `CancellationTokenSource.CancelAsync` | .NET 8 | Async cooperative cancel signal for shutdown paths. |
| `TimeProvider` (and `FakeTimeProvider` in `Microsoft.Extensions.TimeProvider.Testing`) | .NET 8 | Abstraction for injectable, testable time. |
| `Task.WhenEach` | .NET 9 | Await tasks as each completes (with `await foreach`); before .NET 9 use a channel or `Task.WhenAny` loop. |

Do not present .NET 8/9 APIs as universal defaults. For an older TFM, state the replacement pattern (e.g. a channel/`WhenAny` loop instead of `WhenEach`, a `Task.Delay` race only when no `WaitAsync` exists).

## Lifecycle model template

Fill this in for each task/operation before judging or changing code:

1. **Creator/owner** — which component constructs the task/CTS/scope; who disposes it.
2. **Starter** — which code starts the work; is it fire-and-forget or awaited?
3. **Progress** — what drives completion (I/O, timer, another task, a loop).
4. **Cancellation** — which token(s) reach it; does it honor them at every await; what does it do on cancel (release? partial write? no-op?).
5. **Timeout** — is there a deadline; is the deadline distinct from the caller token; who fires it.
6. **Fault** — where exceptions surface; are they observed; is partial work cleaned up.
7. **Shutdown** — how a process/application stop reaches it; grace period; drain-or-discard policy.
8. **Resources** — registrations (`Register`), semaphores, channels, scoped services, locks; when released.
9. **Aftermath** — retry, restart, or orphaned work after partial failure/cancel.

## Ownership and propagation decision paths

- **Who disposes the CTS?** The component that created it. If a method receives a `CancellationToken` but no source, it must not dispose anything; the caller owns lifetime. If the method creates a linked source, it owns and disposes that source (and unregisters its registration).
- **Do we thread the token?** Whenever an awaitable accepts a token and the operation is caller-bound, pass the token through. Dropping it is the most common cause of "cancel did nothing" and "shutdown hangs".
- **Timeout token vs caller token.** Use `CreateLinkedTokenSource(callerToken)` then `CancelAfter(timeout)`. Capture which token fired (`IsCancellationRequested` on each) so a timeout is reported as a timeout and a caller cancel as a caller cancel. Dispose the linked source in a `finally`/`using`; `CancellationTokenSource` is synchronously disposable.
- **When to `ConfigureAwait(false)`.** Library code should avoid capturing the synchronization context so it does not deadlock callers. Application code that must resume on the UI thread or inside a request context should capture it. Decide per boundary; never blanket-apply.

## WhenAll / WhenAny / WaitAsync failure and cancellation semantics

- `Task.WhenAll` — returns a task that completes when all complete. If any task faults, the result is faulted (and awaiting throws an exception; `Task.Exception` holds the aggregate). Otherwise, if any task cancels, the result is canceled. It never cancels the still-running siblings. Bound the fan-out first.
- `Task.WhenAny` — returns a proxy for the first completed task. Await the **original** task to get its result/exception; observe or cancel the losers. A `WhenAny` loop is a poor substitute for `WhenEach` or a channel when order/backpressure matter.
- `Task.WaitAsync` — adds a timeout or cancellation to the wait, not to the work. The underlying task is not canceled; if it later faults and nobody observes it, that fault leaks. Only use it when "stop waiting but let the work finish (or cancel it separately)" is the intended contract.

## Channels and backpressure decisions

- Bound channels fed by untrusted/external input; the full-mode choice is a contract, document it (`Wait` = backpressure, `DropWrite` = silently discard the incoming item when full, `DropNewest`/`DropOldest` = bounded loss). Do not treat a successful write call in a drop mode as proof that the item was retained.
- On `ChannelClosedException` or reader/writer completion, stop and observe rather than looping on a closed channel.
- A single consumer with `ReadAllAsync` is usually clearer and safer than a hand-rolled receive loop with `WaitToReadAsync`.

## Verified official references

Focused links, cited only as authority for the version facts above:

- Task-based Asynchronous Pattern (TAP): https://learn.microsoft.com/en-us/dotnet/standard/asynchronous-programming-patterns/task-based-asynchronous-pattern-tap
- Cancellation in managed threads: https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads
- `Task.WaitAsync`: https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.task.waitasync
- `Task.WhenEach`: https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.task.wheneach
- `ConfigureAwaitOptions`: https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.configureawaitoptions
- `CancellationTokenSource.CancelAsync`: https://learn.microsoft.com/en-us/dotnet/api/system.threading.cancellationtokensource.cancelasync
- `TimeProvider`: https://learn.microsoft.com/en-us/dotnet/api/system.timeprovider
- `Parallel.ForEachAsync`: https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.parallel.foreachasync
- `PeriodicTimer`: https://learn.microsoft.com/en-us/dotnet/api/system.threading.periodictimer
- Channels overview: https://learn.microsoft.com/en-us/dotnet/core/extensions/channels
- Worker services (BackgroundService/HostedService): https://learn.microsoft.com/en-us/dotnet/core/extensions/workers
- `ValueTask`: https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.valuetask
- `Task.ConfigureAwait`: https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.task.configureawait

If a link is unreachable at read time, say so and do not assert the version fact from memory; fall back to the repository's actual TFM and source.
