---
name: mag-dotnet-performance
description: Diagnose and optimize a measured .NET performance problem by establishing workload and target metrics, building a reproducible baseline on the detected SDK/TFM/runtime, attributing cost to CPU, IO, allocation/GC, contention, thread-pool, or startup, and gating span, pooling, ValueTask, JIT, LINQ, or vectorization changes on before/after evidence plus version verification. Use for a measured performance problem or an authorized optimization; do not use for speculative micro-optimization, architecture rewrites, generic debugging, or async-correctness-dominant work, and treat a review/diagnosis/design request as read-only.
---

# .NET Performance

## When to Use

Use for a measured .NET performance problem: slow request, high CPU, allocation or GC pressure, tail latency, throughput shortfall, startup time, or an authorized optimization of an identified hotspot. The work is diagnosing and verifying real performance, not rewriting code toward an imagined "faster".

Route elsewhere when the primary outcome is not measured performance:

- async/concurrency correctness — cancellation, ownership, deadlock, unbounded queues, shutdown — dominates → `mag-dotnet-async-reliability`;
- a read-only multi-category code review with performance as one lens among many → `mag-csharp-review`;
- creating/extending a project or resolving build/toolchain compatibility → `mag-dotnet-project`;
- a bug, missing feature, or ordinary behavior change with no performance goal → `mag-csharp-implementation`.

Do not replace the generic diagnosis skill for functional bugs, and do not turn a latency investigation into an architecture rewrite. If async correctness is the dominant cause of the slowness, hand it to the async specialist; performance diagnosis here stops at the boundary.

## Mode governs what you may change

Establish the mode from the request. **Review / diagnose / design / "investigate" is read-only**: measure, read, plan, and report, but do not edit code or project files. **Fix / optimize** permits editing only the files and behavior the user authorized, and only after the bottleneck is proven. If no baseline exists and measurement is not authorized, stay in plan mode: output a measurement plan with labeled hypotheses and change nothing — never claim an improvement. A measurement plan is always allowed; running benchmarks, profiling, or builds is a separate, effect-bearing step (see below).

## Establish the problem and the measurement contract

1. Name the workload, the current metric, and the target: throughput (ops/s), latency (mean plus percentiles p50/p95/p99 — the tail matters), allocations per operation, GC pause/collection counts, startup time, or sustained CPU. "Make it faster" is not a metric; state the number and the threshold that would make the work done.
2. Read repository instructions and detect the toolchain as independent facts — do not collapse them into "the .NET version": **SDK** (`global.json`), **language version** (`<LangVersion>`), **target framework** (`<TargetFramework>`/`<TargetFrameworks>`), **runtime** (`runtimeconfig.json`, self-contained/RID), **packages** (`Directory.Packages.props`, `PackageReference`, lock files), and **analyzers/quality gates** (`AnalysisLevel`, `TreatWarningsAsErrors`, `.editorconfig`). Version-sensitive performance claims are gated on the effective TFM and runtime, not the newest release you know.
3. Record the environment: machine, CPU, OS, memory, .NET runtime version, and configuration (Debug vs Release, `Optimize`). A benchmark is not reproducible without it.
4. State what is in scope and what is not, and how the result will be verified.

## Build a reproducible baseline first

Do not optimize without a baseline: you cannot report an improvement you cannot measure, and a regression you did not notice is still a regression.

- Measure the current code under a fixed, repeatable workload before changing anything. Use the same build configuration and environment for every later comparison.
- Prefer Release builds with optimizations enabled; a Debug result measures the wrong thing. Note tiered compilation and warm-up effects — a cold first run and a steady-state run can differ by orders of magnitude.
- Capture the baseline's throughput, percentiles, and allocations, not a single number. A mean alone hides the tail; an allocation count without a scale hides GC pressure.

See `references/measurement.md` for the focused workflow: isolated microbenchmarks versus realistic end-to-end evidence, and which tool to point at which signal.

## Attribute the cost before touching code

Separate the bottleneck from hypotheses. Measure where time and allocations actually go, then map the result to a category and a location:

- **CPU** — hot method, algorithmic cost, redundant work, JIT-unfriendly shapes;
- **IO** — blocking or repeated reads/writes, chatty network calls, missing caching, sync-over-async waiting on IO;
- **allocation / GC** — per-call allocations, boxing, string or collection churn, large-object or pinned-object pressure;
- **contention** — lock scope and frequency, shared state, atomic churn;
- **thread pool** — starvation, `Task.Run` around IO-bound work, unbounded parallelism, blocking on the pool;
- **startup / JIT** — cold-start cost, ReadyToRun or tiered-compilation effects, eager initialization.

Record the evidence for each category (counter values, trace frames, allocation sources) and mark each as **proven** or **hypothesis**. A profiler or counter points at the code path; it does not, by itself, prove that removing that cost is safe or sufficient. Before optimizing, name the smallest change that addresses the measured cost and the test that would prove it.

## Choose isolated versus realistic evidence deliberately

- **Isolated microbenchmarks** (BenchmarkDotNet and equivalents) isolate a single operation's steady-state cost — CPU, allocation, per-invocation overhead — with statistical rigor. They prove a micro-cost, not end-to-end value, and they can mislead when the real cost is orchestration, IO, contention, or startup. Use them to confirm a small, well-isolated claim, not to justify a system-level change.
- **Realistic end-to-end evidence** (a representative load against the real path, with counters and traces) proves the user-visible metric. Use it to establish the baseline and to verify any before/after claim that matters at the service level.

Report which kind of evidence supports each claim. A microbenchmark that improves does not establish that the workload improved; say so instead of implying it.

## Optimization levers — gated on evidence and version

Each lever below is only justified by a measured cost it demonstrably removes. Do not apply it speculatively, and verify any version-sensitive API against the effective TFM (see `references/measurement.md` for the official-documentation routing).

- **Spans and slices** (`Span<T>`/`ReadOnlySpan<T>`, `string.AsSpan()`) — remove allocation and copying on hot paths. A `Span<T>` is a `ref struct`: it cannot be boxed or stored in a heap field; it can be a field of another `ref struct`. Generic use requires an API/type that permits ref-struct arguments (such as an applicable `allows ref struct` constraint in newer C#). It cannot cross an `await` or iterator suspension, and it cannot escape through a captured lambda/local function; newer C# versions permit some ref-struct locals in async/iterators when they remain within a non-suspending region. Use `Memory<T>`/`ReadOnlyMemory<T>` where the buffer must cross an `await`, a heap boundary, or an API expecting a heap-safe type. Never hold a span across an unsupported boundary to make code compile.
- **Pooling** (`ArrayPool<T>`, `StringBuilder` pooling, object pooling) — trades a small pool-management cost for fewer allocations, and it introduces ownership and secrecy obligations. `ArrayPool<T>.Shared.Return(array, clearArray: true)` is the default for sensitive data: rented buffers may contain another tenant's data, so clear before return and never expose a rented buffer beyond the code that rented it. Return exactly what was rented (same length, same instance), return on every path including exceptions, and do not use the array after returning it.
- **`ValueTask`** — avoids an allocation for frequently-completed-async results. Consume it exactly once; storing it for one later await can be valid when the producer's lifetime permits it, but re-awaiting, consuming a copy more than once, or racing continuations is unsafe because it may wrap a pooled `IValueTaskSource`. Convert with `AsTask()` when it must be awaited more than once or combined in `WhenAll`. Prefer `Task` unless the pooling benefit is measured and understood.
- **JIT / tiered compilation** — tiered compilation is on by default since .NET Core 3.0; Dynamic PGO (`TieredPGO`) is enabled by default in .NET 8+. Treat `ReadyToRun`, `TieredCompilation`, and PGO as runtime-configuration knobs, not as source-level wins; verify the default for the effective runtime before attributing behavior to them. A micro-optimization that fights the JIT (duplicated inlining, manual loop unrolling) can make steady-state code slower — measure it.
- **LINQ** — prefer a single pass over repeated enumeration, and avoid deferred enumeration in a loop or re-evaluation of a sequence you enumerate more than once; materialize once when the source is expensive or re-enumerated. These are correctness-and-cost tradeoffs, not a ban on LINQ: keep the more readable form until a measurement says otherwise.
- **Vectorization / SIMD** (`System.Numerics`, hardware intrinsics) — a real lever for data-parallel hot loops, at the cost of complexity, platform sensitivity, and review burden. Apply only where a measured CPU-bound loop dominates and the data layout supports it, and check `System.Runtime.Intrinsics` availability and hardware support for the target.

Any of these changes must preserve observable behavior, lifetimes, safety, and the public contract. A micro-optimization that changes results, leaks a buffer, or breaks a caller is a defect, not an optimization.

## Operations with effects

Reading code, project files, and `dotnet --version`/`--list-sdks`/`--list-runtimes` is safe and read-only. These steps have effects and require authorization — say which one you need and what it does before running it:

- `dotnet restore`/`build`/`run`/`test` — hit the network, execute analyzers/generators/test code, and write `obj/`, `bin/`, and lock files;
- installing or updating packages or tools — adding `BenchmarkDotNet` is a dependency change; `dotnet tool install` for `dotnet-counters`/`dotnet-trace`/`dotnet-gcdump`/`dotnet-dump` writes global-tool state;
- profiling and tracing — attach to or launch a process, capture and write trace/dump artifacts;
- production profiling, remote writes, or attaching to an unowned live service — out of scope unless the user explicitly authorizes a specific, safe action;
- executing untrusted benchmark or target code — out of scope without explicit authorization.

A measurement plan, the metric definitions, and the before/after reporting format are produced without any of these: you can design the measurement without running it.

## Output

Report:

- the workload, target metric, and environment;
- the baseline numbers and the after numbers, both reproducible (same config, same environment, same load);
- percentiles and tail latency, throughput, and allocations — not only the mean;
- the attribution: which cost category and code path was proven versus hypothesized;
- the change made (if any), why it addresses the measured cost, and the safety/lifetime/behavior arguments for it;
- limitations and tradeoffs, and any checks you did not run and why.

If no measurements were taken, say so explicitly and present a measurement plan instead of an optimization — do not claim an improvement from unrun benchmarks or unsupported reasoning. Use the report format in `references/measurement.md` (§6). When the case resolves to a boundary — async-correctness-dominant slowness or a project/toolchain cause — the deliverable is the routing decision with the criteria that produced it, not findings or fixes. State unverified version-sensitive claims as unverified rather than asserting them.
