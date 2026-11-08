---
name: mag-dotnet-testing-quality
description: Design or assess .NET test strategy and quality gates at the right behavior seam — choosing between in-process TestServer/WebApplicationFactory, in-memory fakes, and real providers via Testcontainers; managing fixture lifetime and disposal; injecting TimeProvider and using FakeTimeProvider on compatible TFMs; handling cancellation, concurrency, serialization, and coverage; and detecting the test platform (VSTest vs Microsoft.Testing.Platform/TUnit) with its correct run commands. Use for test strategy, test-boundary, or test-platform questions; never impose a framework or package, and never equate coverage or a green run with correctness.
---

# .NET Testing Quality

## When to Use

Use when the user asks to add tests at the right boundary, choose between an in-memory and a real test seam, design deterministic fixtures, assess coverage, fix flaky or slow tests at the test-boundary level, or detect/respect the configured test runner and its commands.

Do not use it for implementing a feature (that is `mag-csharp-implementation`), for a read-only multi-category code review (`mag-csharp-review`), for async/concurrency *design* as the dominant concern (`mag-dotnet-async-reliability`), or for a measured application performance problem (`mag-dotnet-performance`). A test that is flaky because the *application* has a race is async-reliability work, not a fixture problem; separate the test-boundary cause from the application cause before routing.

Compose with the generic TDD skill for red-green-refactor discipline; this skill owns the .NET seam and platform decisions, not the red-green loop.

## Start from the behavior and its seam

1. Name the invariant or user-visible contract under test, then choose the narrowest seam that observes it without pinning private implementation details.
2. Detect the repository contract as independent facts before proposing anything: **SDK** (`global.json`), **LangVersion**, **TFM(s)**, **runtime**, **packages** (`Directory.Packages.props`/`PackageReference`), and — decisively here — **the test runner** the repository actually configures. Do not assume xUnit/NUnit/MSTest, and do not assume `dotnet test` means VSTest.
3. Include success, boundary, invalid, error, cancellation, concurrency, and recovery cases relevant to the behavior — not all of them unconditionally.
4. Make fixtures deterministic: name how the test controls time, network, filesystem, randomness, and external services, and mark any test that still depends on the wall clock or a live service as environmental.

The seam decision and its tradeoffs — in-process `TestServer`/`WebApplicationFactory<TEntryPoint>` versus a selected real host or provider, in-memory databases versus real engines, and `TimeProvider` injection with `FakeTimeProvider` — live in `references/test-seams.md`. Load it when choosing or justifying a boundary. For unfamiliar or version-sensitive APIs and packages, use `references/technology-evidence.md` as well.

## Detect the test platform

Do not reach for a run command until you know which platform the test project targets. The consequences of getting this wrong are silent: `dotnet test` has a VSTest mode and a Microsoft.Testing.Platform (MTP) mode, and TUnit is built on MTP, not VSTest. Read `references/testing-platform.md` when the prompt names a runner, a `dotnet test` flag, a coverage collector, or a "why aren't my tests discovered / why is `--logger` ignored" problem. The reference covers:

- VSTest vs MTP, and the .NET 10 SDK `runner` selection (`global.json` / `DOTNET_TEST_RUNNER`);
- TUnit run commands and its incompatibilities (no `Microsoft.NET.Test.Sdk`, no coverlet; flags after `--`);
- the mixed-VSTest/MTP-solution hazard and the TRX-report extension requirement.

## Fixture lifetime, cancellation, concurrency, serialization

- **Lifetime and disposal.** Choose per-test isolation versus shared fixtures (`IClassFixture`/collection fixtures and equivalents) from the cost and the shared-state risk, not habit. Ensure `IAsyncLifetime`/`IDisposable` teardown runs on failure and early-return paths, and that disposal order is defined. A shared fixture is a correctness hazard if parallel tests mutate it.
- **Cancellation.** Thread a `CancellationToken` through test async methods and the operation under test; test timeout and cancellation paths with a real `CancellationTokenSource`, not sleep. Distinguish "the operation honored cancellation" from "the test gave up".
- **Concurrency.** Know the runner's parallelism policy (several runners parallelize by default or by configuration) and constrain shared state accordingly: parallel tests sharing mutable static/DI state or a single fixture is the classic flaky-test source.
- **Serialization.** Never let tests depend on each other or on execution order; a test that passes only after another one has mutated shared state is an ordering bug, not a passing test.
- **Coverage.** Treat coverage as an *explored-paths* signal, never proof of correctness: a line covered by an assertion-free test proves nothing, and a green run proves only the scenarios that ran. Use the coverage mechanism that matches the detected platform (VSTest collectors vs the runner's own coverage flag) — see `references/testing-platform.md`.

## Boundaries and honest commands

- **Do not impose a framework or package.** Use the repository's configured runner and its existing test packages. `FakeTimeProvider`, Testcontainers, and a Web SDK test project are *options* whose compatibility you detect, not defaults to mandate. Check the effective package version and compatible assets; do not turn a remembered TFM rule into a universal prohibition. Testcontainers still needs a Docker-API-compatible runtime.
- **Do not equate one green run or a coverage percentage with correctness.**
- **Treat restore/build/test as effect-bearing.** Restore downloads packages; build/test execute analyzers, source generators, and test code. State the exact command you would run and what it does, and never claim a test passed, failed, or was measured from a command you did not run. Read-only inspection (`dotnet --version`, `--list-sdks`, reading project files) is safe.

## Output

Return a test matrix: behavior, seam, fixture, platform/command, expected signal, and limitation per row. Include:

- the detected SDK, TFM, and test runner as separate facts (state `not detected` when no project file is in scope);
- the seam choice and its justification (what it proves, what it leaves untested);
- missing evidence, environmental/flaky tests, and the smallest high-value additions;
- every command not actually run, stated as `not run`.

Do not recommend a tool, package, or seam without naming the property it verifies and the gap it closes.
