# Test seams: in-process host, fakes, and real providers

Load this reference when choosing or justifying a .NET test boundary. A "seam" is where you cut the system to observe behavior; each cut proves some things and leaves others untested. Name which gap a seam closes and which it leaves open before committing to it.

## In-process host: WebApplicationFactory / TestServer

`WebApplicationFactory<TEntryPoint>` (package `Microsoft.AspNetCore.Mvc.Testing`, namespace `Microsoft.AspNetCore.Mvc.Testing`) uses an in-memory `TestServer` by default. In that default mode it does not open a real socket, so it does not exercise real networking, TLS, or external hosting. On framework versions that expose `UseKestrel()`, the same factory can be configured to use Kestrel; that is a different seam and must be checked against the project's package/framework version. The default TestServer mode is fast and stable for an ASP.NET Core request pipeline.

Detection and traps:

- The test project must use `<Project Sdk="Microsoft.NET.Sdk.Web">`.
- `TEntryPoint` is the app's entry-point class, usually `Program`. Top-level statements generate an **internal** `Program`, so the test project cannot see it unless the app declares `public partial class Program { }` or exposes it via `InternalsVisibleTo`.
- `CreateClient()` returns an `HttpClient` that follows redirects and handles cookies automatically.
- Service replacement happens in `ConfigureWebHost` → `IWebHostBuilder.ConfigureServices`, which runs **after** the app's `Program.cs` executes; that is where you swap a real `DbContext`/service for a test double.
- Content-root inference (static files/views not found) is driven by `WebApplicationFactoryContentRootAttribute` keyed on the entry-point assembly name, with a `.sln`-based fallback — a mismatch there produces "content root not found", not a code error.

What the default TestServer mode does **not** prove: real sockets, TLS termination, a reverse proxy or hosting layer, or a real external database. A Kestrel-configured factory can cover socket-level behavior, but still does not by itself prove a production reverse proxy, deployment or external database.

## Real provider: Testcontainers

Testcontainers for .NET (package `Testcontainers`) manages throwaway Docker container instances over the Docker API. Modular providers (e.g. `Testcontainers.PostgreSql`, `Testcontainers.MsSql`, `Testcontainers.Redis`) give you the **real engine** — real SQL dialect, real version differences, real migrations — at the cost of container spin-up latency and a Docker daemon in CI.

Detection and traps:

- It requires a **Docker-API-compatible container runtime** (Docker Desktop on macOS/Windows, Docker on Linux). Remote hosts and Docker alternatives (e.g. Podman) need manual configuration and are not fully tested — detect availability before assuming it.
- It is the right seam when the behavior under test *is* the provider: migrations, dialect-specific SQL, provider-specific types, or a bug that only reproduces on the real engine. It is overkill when the behavior is plain business logic that a fake can cover.
- Containers are throwaway resources: they must be started once, reused where cost matters, and disposed in fixture teardown, with the same disposal-order discipline as any `IAsyncDisposable`.

The two seams are complementary, not interchangeable: `TestServer` is a fast in-process host with **no real network or database**; Testcontainers is a **real provider** that is slow and Docker-dependent. Choosing one does not cover the other's gap.

## In-memory vs real data

- An in-memory database or a fake repository is deterministic and fast, but it is **not** the real provider: it does not reproduce SQL translation, dialect, constraints, or migration behavior. Use it for business logic; do not claim it proves a repository/EF query against the real engine.
- A real database (typically via Testcontainers, or a repository-managed test database) proves provider behavior but is slower, environmental, and can leak state between runs unless schema/data are reset per run.

## Time: inject TimeProvider, use FakeTimeProvider

- Inject `System.TimeProvider` (in-box from .NET 8) into the code under test instead of reading the wall clock, so tests control time. `System.Threading.ITimer` is the timer abstraction paired with it.
- `FakeTimeProvider` (namespace `Microsoft.Extensions.Time.Testing`) drives the injected provider deterministically: `Advance(TimeSpan)`, `SetUtcNow(DateTimeOffset)`, `AutoAdvanceAmount`, `GetUtcNow()`. Use these instead of sleep-based time travel.
- **Package/TFM trap:** the package id is `Microsoft.Extensions.TimeProvider.Testing` (some framework documentation has shown the older namespace `Microsoft.Extensions.Time.Testing`). Check the resolved package version and its assets: for example, package 8.0.0 includes a `net6.0` asset and depends on `Microsoft.Bcl.TimeProvider`, while later package lines may have different target frameworks. `System.TimeProvider` is in-box from .NET 8; older TFMs may use the backport package. Do not reject or emit code based on the TFM alone: verify the exact package/version compatibility, namespace and project references, then choose `FakeTimeProvider`, a compatible package line, a TFM change, or a small clock abstraction.

## Fixture lifetime and disposal

- Prefer per-test isolation when tests mutate shared state; use shared fixtures (`IClassFixture`/collection fixtures and equivalents) only when setup is expensive and the shared state is read-only or safely reset.
- `IAsyncLifetime`/`IDisposable` teardown must run on failure and early-return paths; order disposal explicitly (reverse of creation), and never let one test's teardown depend on another test's state.
- A shared fixture mutated by parallel tests is the classic flaky-test source — see the concurrency section in `SKILL.md`.

## References

- [Integration tests in ASP.NET Core (WebApplicationFactory / TestServer)](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests)
- [WebApplicationFactory&lt;TEntryPoint&gt; API](https://learn.microsoft.com/en-us/dotnet/api/microsoft.aspnetcore.mvc.testing.webapplicationfactory-1)
- [What's new in .NET 8 — Time abstraction (TimeProvider/ITimer)](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-8/runtime)
- [FakeTimeProvider API](https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.time.testing.faketimeprovider)
- [Microsoft.Extensions.TimeProvider.Testing package](https://www.nuget.org/packages/Microsoft.Extensions.TimeProvider.Testing)
- [Microsoft.Bcl.TimeProvider backport package](https://www.nuget.org/packages/Microsoft.Bcl.TimeProvider)
- [Testcontainers for .NET](https://dotnet.testcontainers.org/)
- [Testcontainers package](https://www.nuget.org/packages/Testcontainers)
