---
name: mag-aspnet-core
description: Design, review, diagnose, or fix ASP.NET Core applications — request pipeline and middleware ordering, authentication and resource-based authorization, dependency-injection lifetimes, caching with tenant isolation, outbound HTTP resilience and cancellation, and structured logging/redaction/observability — by detecting the SDK, target framework, ASP.NET Core version, package graph, and provider as separate facts and gating every version-sensitive claim on them. Use for middleware, auth, DI lifetime, caching, resilience, or observability work; route async-correctness-dominant work to mag-dotnet-async-reliability, data-access work to mag-ef-core, read-only multi-category review to mag-csharp-review, and project/build compatibility to mag-dotnet-project.
---

# ASP.NET Core

## When to Use

Use when the request is about an ASP.NET Core application's request pipeline, middleware, authentication/authorization, dependency injection, caching, outbound HTTP resilience, or logging/redaction/observability — whether to design it, review it, diagnose a defect, or fix an authorized change.

Route elsewhere when a different concern dominates:

| Request is primarily | Use |
|---|---|
| Cancellation ownership, timeouts, background services, `WhenAll`/channels, shared state, `ConfigureAwait` | `mag-dotnet-async-reliability` |
| EF Core querying, tracking, transactions, migrations, provider behavior | `mag-ef-core` |
| A read-only multi-category code audit where ASP.NET is one lens among many | `mag-csharp-review` |
| Creating a project, resolving SDK/TFM/package compatibility, or a build failure | `mag-dotnet-project` |
| A plain bug or feature in C# logic with no web-specific concern | `mag-csharp-implementation` |

An ordinary controller action or middleware body is not automatically this skill; it becomes this skill when the concern is the pipeline, lifetime, caching, resilience, or observability contract. A request that only asks for an explanation does not authorize edits.

## Mode governs what you may change

Establish the mode from the request. **Review / diagnose / design / "investigate" is read-only**: read, trace, and report, but do not edit code or project files. **Fix / implement** permits editing only the files and behavior the user authorized; do not broaden a fix into a middleware reordering, a DI-lifetime change, or a dependency add/removal.

Reading code, project files, and `dotnet --version`/`--list-sdks`/`--list-runtimes` is safe. These are effect-bearing and require authorization, stated before you run them: `dotnet restore`/`build`/`run` (network, generators, writes to `obj/`/`bin/`), installing or updating packages or tools, publishing/deploying, and any write to a remote service or cache backend.

## Detect the web contract first

These are independent facts; detect and report them, do not collapse them into "the ASP.NET version":

- **SDK** — `global.json`, `dotnet --list-sdks`.
- **Target framework** — `<TargetFramework>`/`<TargetFrameworks>`.
- **Framework / ASP.NET Core version** — the `Microsoft.AspNetCore.App` framework reference, `FrameworkReference`, or the resolved `Microsoft.AspNetCore.*` package versions; this gates which middleware and APIs exist (e.g. output caching, `MapStaticAssets`, `HybridCache`).
- **Package graph** — `Directory.Packages.props`/`PackageReference`, especially `Microsoft.Extensions.Http.Resilience`, `Microsoft.Extensions.Compliance.Redaction`, `Microsoft.Extensions.Telemetry`.
- **Provider / environment** — hosting model (minimal API vs MVC), the cache and resilience packages in use, and whether the app is single-tenant or multi-tenant.

Version-sensitive claims are gated on the effective framework and package versions, not the newest release you know. A user-asserted version with no project file in scope is unverified: answer conditionally and say what a confirming file would change.

## The pipeline and middleware order

Middleware order is request order in one direction and the reverse for the response; ordering is a correctness, security, and performance concern. `UseCors` must precede `UseResponseCaching`; culture-reading middleware must follow `UseRequestLocalization`; endpoint-specific `[EnableRateLimiting]` requires `UseRateLimiter` after `UseRouting` (rate-limiting middleware and attributes are ASP.NET Core 7+; on net6.0 they do not exist); authentication runs before authorization, which runs before the endpoint. Authentication middleware does not short-circuit unauthenticated requests by itself. See `references/request-pipeline.md` for the position constraints and the full ordering model.

## Authentication and authorization are two layers

Authentication establishes identity; authorization decides access and does nothing unless configured. Requiring authenticated users everywhere needs a fallback authorization policy, not merely registering authentication. Endpoint-level authorization is declarative (`[Authorize]`, roles, policies built from `IAuthorizationRequirement`). Resource-level authorization — deciding against a loaded entity — is imperative: inject `IAuthorizationService` and call `AuthorizeAsync(user, resource, policy)`, because declarative attributes are evaluated before data binding and before the resource exists. See `references/authorization.md`.

## Dependency injection and lifetimes

Resolve services with the lifetime that matches their state: `Transient` for stateless per-resolution work, `Scoped` for per-request state, `Singleton` for app-wide state. A singleton must not hold a scoped service (captive dependency) — it silently becomes a singleton and can leak request state or a `DbContext` across requests. `DbContext` is registered scoped; do not capture it into a singleton or a background service. See `references/dependency-injection.md`.

## Caching and tenant isolation

`IMemoryCache` and the response-cache middleware are app-wide and shared across tenants. Never cache tenant-sensitive data under a tenant-agnostic key; scope keys by tenant identity and vary response-cache entries by tenant. Do not insert arbitrary user input as a cache key. See `references/caching.md`, where the tenant rules are labeled as synthesis, not a verbatim Microsoft rule.

## Outbound HTTP, resilience, and cancellation

The standard resilience handler retries **all** HTTP methods by default, including `POST`, which can duplicate side effects; disable retries for unsafe methods (`DisableForUnsafeHttpMethods()` or an explicit allow-list of idempotent methods) for any non-read-only call. Thread `HttpContext.RequestAborted` through outbound calls so a disconnected client stops consuming resources. See `references/http-resilience.md`.

## Logging, redaction, and observability

Use structured logging (`ILogger<T>`); never write personal data, credentials, or financial details to logs in plain text. Redaction is wired through the logging pipeline with classification attributes and redactors; `HmacRedactor` is experimental. Observability means structured logs plus correlated traces, not ad-hoc `Console.WriteLine`. See `references/observability.md`.

## Output

Report, in order:

1. The detected web contract: SDK, TFM, framework/ASP.NET Core version, and the packages that matter for the concern.
2. The pipeline/lifetime/caching/resilience/observability model of the code in scope, anchored to exact lines or the smallest causal anchor.
3. Findings by category, each labeled **proven** (traced to the code) versus **hypothesis**, and each change classified as necessary versus optional.
4. The authorization boundary: what you changed, what you did not, and why.
5. Commands actually run and their observed results; state explicitly when no build/test was run and what the unrun check would confirm.
6. Limits and remaining risks, including any version-sensitive claim you could not confirm against the detected contract.

Distinguish confirmed Microsoft-documented behavior from synthesis in every reference you cite; do not present a derived recommendation as a doc rule.
