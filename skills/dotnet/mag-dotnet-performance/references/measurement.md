# Measurement workflow

Load this reference when you need the concrete steps to build a reproducible baseline, pick isolated versus end-to-end evidence, point the right diagnostic at the right signal, or check a version-sensitive performance API. It is a workflow, not a list of automatic defects.

## 1. Pin the measurement contract

Write down, before any run:

- **Workload** — the exact operation or request mix, input size, and how load is generated.
- **Metrics and targets** — throughput (ops/s), latency percentiles (p50/p95/p99), allocations/op, GC collections or pause time, startup time, sustained CPU. Record the threshold that means "done".
- **Environment** — machine, CPU, OS, memory, .NET runtime version (`dotnet --list-runtimes`), and build configuration (Debug vs Release, `Optimize`, `DebugType`). A number without these is not reproducible.
- **Comparison rule** — baseline first, then one change at a time, same config and environment throughout. A benchmark that changes two variables at once proves nothing.

## 2. Build the baseline

1. Measure the current code under the fixed workload. Use Release with optimizations; measure both a cold run and a steady-state run, because tiered compilation and warm-up change the numbers.
2. Record throughput, percentiles, and allocations, not a single mean. A mean hides the tail; an allocation count without a scale hides GC pressure.
3. Save the raw output and the environment. Everything later is compared against this snapshot.

## 3. Attribute the cost

Point the cheapest available signal at the problem before choosing a tool. In order of increasing weight:

| Cost to find | Signal / tool | What it shows |
|---|---|---|
| Counters (CPU, GC, thread-pool, lock contention) | `dotnet-counters` | Live rates: GC collections, allocated bytes, thread-pool queue depth, `monitor-lock-contention-count`, CPU |
| Allocations / GC detail | `dotnet-gcdump`, `dotnet-trace` (GC events), BenchmarkDotNet `[MemoryDiagnoser]` | Allocation sources, gen0/gen1/gen2, LOH/pinned-object pressure |
| CPU hot paths | `dotnet-trace` (CPU sampling), `dotnet-dump` with `clrstack`/`dumpheap` | Which methods consume CPU or hold memory |
| Startup / JIT | `dotnet-trace` (startup), `DOTNET_ReadyToRun`, tiered-compilation settings | Cold-start cost, ReadyToRun vs JIT, tiering behavior |

These tools are .NET diagnostics (`dotnet-counters`, `dotnet-trace`, `dotnet-gcdump`, `dotnet-dump`), normally installed as global tools — installing or attaching them is an effect-bearing step requiring authorization. Reading code and project files and planning the measurement require none.

## 4. Isolated microbenchmarks versus end-to-end evidence

**Isolated microbenchmarks** (BenchmarkDotNet is the standard .NET library) isolate one operation's steady-state CPU, allocation, and per-invocation overhead. They are right for: confirming a small well-isolated claim, comparing two local implementations, or quantifying allocations of a single method. They are wrong for: end-to-end latency, IO, contention, startup, or orchestration — a microbenchmark that improves does not prove the service improved.

**Realistic end-to-end evidence** — a representative load against the real path, watched with counters and traces — proves the user-visible metric. It is the only evidence that validates a system-level before/after claim.

Keep the two separate and label each claim with the evidence kind that supports it.

## 5. Gating and version-sensitive checks

Apply an optimization only when a measured cost it removes is proven, and verify version-sensitive APIs against the effective TFM. Relevant surface, with the knob and the version-sensitive point:

- **Tiered compilation** — on by default since .NET Core 3.0; `TieredCompilation` runtime config / MSBuild property. **Dynamic PGO** (`TieredPGO`) is enabled by default in .NET 8+; in .NET 7 it was opt-in. Verify the default for the effective runtime rather than assuming.
- **ReadyToRun** — precompiled code that trades some peak optimization for faster startup; a build/publish option, not a source-level change.
- **`Span<T>` / `Memory<T>`** — `Span` is a `ref struct`: it cannot be boxed or stored in a heap field; it can be a field of another `ref struct`. Generic use requires an API/type that permits ref-struct arguments (such as an applicable `allows ref struct` constraint in newer C#). It cannot cross an `await` or iterator suspension, and it cannot escape through an escaping lambda; newer C# versions permit some ref-struct locals in async/iterators when they remain within a non-suspending region. `Memory` is the heap-safe counterpart. Check the API you are calling accepts `Span`/`ReadOnlySpan` (many `System.Text.Json`, `Stream`, and parsing APIs do on modern TFMs).
- **`ArrayPool<T>`** — rent/return semantics, `clearArray: true` for sensitive data; available across modern TFMs, pooled-buffer ownership is your obligation, not the pool's.
- **`ValueTask` / `IValueTaskSource`** — `ValueTask` since .NET Core 2.1; consume it once. Storing it for one later await can be valid when the producer's lifetime permits it, but repeated or concurrent consumption is unsafe with pooled sources.
- **SIMD / intrinsics** — `System.Numerics` vector types broadly available; `System.Runtime.Intrinsics.*` require checking `IsSupported` and target architecture.

When a rule depends on a version you have not confirmed, say so and route to the current official documentation for the effective version.

## 6. Report format

For every measurement, record: workload, environment, configuration, baseline, after, metric (with percentiles where latency is the goal), attribution (proven vs hypothesized), and limitations. State the exact commands run and the actual observed output. If no measurement was run, present the plan and do not claim an improvement.

## Focused official references

- Memory and spans — https://learn.microsoft.com/en-us/dotnet/standard/memory-and-spans/
- `ref` structure types — https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/ref-struct
- `ArrayPool<T>` — https://learn.microsoft.com/en-us/dotnet/api/system.buffers.arraypool-1
- `Memory<T>` — https://learn.microsoft.com/en-us/dotnet/api/system.memory-1
- `ValueTask` — https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.valuetask
- Garbage collection fundamentals — https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals
- Workstation and server GC — https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/workstation-server-gc
- Runtime configuration: compilation (tiered compilation, PGO, ReadyToRun) — https://learn.microsoft.com/en-us/dotnet/core/runtime-config/compilation
- What's new in .NET 8 runtime (Dynamic PGO enabled by default) — https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-8/runtime
- Runtime configuration: garbage collector — https://learn.microsoft.com/en-us/dotnet/core/runtime-config/garbage-collector
- The managed thread pool — https://learn.microsoft.com/en-us/dotnet/standard/threading/the-managed-thread-pool
- SIMD and hardware intrinsics — https://learn.microsoft.com/en-us/dotnet/standard/simd
- .NET diagnostics tools (counters, trace, gcdump, dump) — https://learn.microsoft.com/en-us/dotnet/core/diagnostics/
- BenchmarkDotNet documentation — https://benchmarkdotnet.org/
- LINQ deferred execution — https://learn.microsoft.com/en-us/dotnet/standard/linq/deferred-execution-lazy-evaluation
