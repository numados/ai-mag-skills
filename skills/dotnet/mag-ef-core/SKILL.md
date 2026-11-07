---
name: mag-ef-core
description: Design, review, diagnose, or fix Entity Framework Core data access — query translation and client evaluation, change tracking and identity resolution, loading strategies and N+1, context lifetime and pooling with tenant-state isolation, transactions/retry/optimistic concurrency, ExecuteUpdate/Delete bypasses, migrations, and provider realism — by detecting the EF Core version, database provider, DbContext registration, and package graph as separate facts and gating version-sensitive behavior on them. Use for querying, tracking, saving, concurrency, migrations, or provider-behavior work; route pure SQL/stored-procedure design away from the EF model, testing-host mechanics to mag-dotnet-testing-quality, and ASP.NET pipeline/lifetime concerns to mag-aspnet-core.
---

# Entity Framework Core

## When to Use

Use when the request concerns EF Core: query translation, tracking, loading strategy, context lifetime, transactions, concurrency, bulk `ExecuteUpdate`/`ExecuteDelete`, migrations, or choosing a provider/test double. Whether to design, review, diagnose, or fix an authorized change.

Route elsewhere when a different concern dominates:

| Request is primarily | Use |
|---|---|
| Test host/fixture lifetime mechanics (`WebApplicationFactory`, Testcontainers, real-database harness) | `mag-dotnet-testing-quality` (this skill only states the provider-realism hierarchy) |
| ASP.NET Core pipeline, DI-lifetime, caching, or observability | `mag-aspnet-core` |
| Async correctness of the surrounding code (cancellation, ownership, `WhenAll`) | `mag-dotnet-async-reliability` |
| A read-only multi-category code audit where EF is one lens among many | `mag-csharp-review` |
| Plain C# logic with no data-access concern | `mag-csharp-implementation` |

An ordinary query is not automatically this skill; it becomes this skill when the concern is translation, tracking, loading, lifetime, concurrency, or provider behavior. A request that only asks for an explanation does not authorize edits.

## Mode governs what you may change

Establish the mode. **Review / diagnose / design / "investigate" is read-only**: read, trace, and report, do not edit. **Fix / implement** permits editing only the files and behavior the user authorized; do not broaden a fix into a schema change, a provider swap, or a query-shape rewrite.

Reading code and project files is safe. Effect-bearing steps require authorization, stated before you run them: `dotnet restore`/`build`/`test` (network, generators, writes to `obj/`/`bin/`), `dotnet ef` commands (which can generate migrations and apply them to a database), applying or reverting a migration against a real database, and any write to a remote database.

## Detect the EF contract first

These are independent facts; detect and report them separately:

- **EF Core version** — the `Microsoft.EntityFrameworkCore` (and `.Relational`/provider) `PackageReference` version. This gates client-eval behavior, `ExecuteUpdate`/`ExecuteDelete`, `AsNoTrackingWithIdentityResolution`, `ConfigureDbContext`, and the SQL API surface.
- **Database provider** — `UseSqlServer`/`UseSqlite`/`UseNpgsql`/`UseInMemoryDatabase`/etc., and its package version. The provider decides what translates, whether `rowversion` vs application-managed concurrency tokens apply, and what testing realism is achievable.
- **DbContext registration** — `AddDbContext` (scoped) vs `AddDbContextPool` vs `AddDbContextFactory`, and whether a tenant/request value is set in `OnConfiguring`.
- **Project structure** — whether migrations live in the app project or a separate migrations project, and the tooling (`dotnet ef`) availability.

Version-sensitive claims are gated on the detected EF Core version and provider, not the newest release you know. A user-asserted version with no project file in scope is unverified: answer conditionally.

## Query translation and client evaluation

EF Core translates LINQ to the provider's SQL and evaluates as much as possible on the server; queries always execute against the database even when the entities are already in the context. Since EF Core 3.0, untranslatable expressions outside the top-level `Select` throw at runtime (older versions fell back to client evaluation with a warning). Explicit opt-in to client evaluation is `AsEnumerable`/`ToList` (or their async forms). See `references/translation.md`, including the query-plan cache leak and raw-SQL guidance.

## Change tracking and identity resolution

Queries returning entity types are **tracking by default**; a tracking query performs identity resolution (same row → same instance), while no-tracking queries return a new instance per row. `AsNoTracking()` opts out per query; `AsNoTrackingWithIdentityResolution()` (EF Core 5.0+) resolves identity without tracking. A custom projection still tracks the entity types it contains. See `references/tracking.md`.

## Loading and N+1

Choose the loading strategy deliberately: eager (`Include`/`ThenInclude`) loads related data in the query, explicit (`Reference`/`Collection(...).Load()`) loads it later on demand, lazy loads transparently on navigation access (and risks the N+1 problem). See `references/tracking.md` for the strategy table and split-query caveat.

## Context lifetime and pooling

`DbContext` is a short-lived unit of work and is not thread-safe. `AddDbContext` registers scoped; for non-request-aligned scopes use `AddDbContextFactory`. Context pooling (`AddDbContextPool`) reuses instances across requests — effectively a singleton — so per-request state (such as a tenant ID) must **not** be set in `OnConfiguring` (which runs once per pooled instance); inject it via a scoped wrapper. See `references/contexts-pooling.md`.

## Transactions, concurrency, and retry

One `SaveChanges` call is atomic by default. Manual transactions are incompatible with implicit retry execution strategies and must be wrapped in `CreateExecutionStrategy().ExecuteAsync(...)`. Optimistic concurrency uses a concurrency token and surfaces `DbUpdateConcurrencyException` on zero rows affected. See `references/saving-concurrency.md`.

## ExecuteUpdate / ExecuteDelete

These translate to SQL and run in the database **without** loading or tracking entities, without an implicit transaction, and without automatic optimistic concurrency — they bypass the change tracker and `SaveChanges`. Do not mix them with tracked `SaveChanges` on the same entities. See `references/saving-concurrency.md`.

## Migrations and provider realism

Migrations compare the model to a snapshot and record applied migrations in a history table. `dotnet ef database update` is fine for local dev but not the production-default; a migration bundle or reviewed SQL script is the safer deployment path. For testing, prefer the production database system over SQLite in-memory, and never use the in-memory provider or `DbSet` mocking as a substitute for real provider behavior. See `references/migrations-testing.md`.

## Output

Report, in order:

1. The detected EF contract: EF Core version, provider and its version, DbContext registration, and migration/project structure.
2. The query/tracking/lifetime/concurrency model of the code in scope, anchored to exact lines or the smallest causal anchor.
3. Findings by category, each labeled **proven** versus **hypothesis**, and each change classified as necessary versus optional.
4. The authorization boundary: what you changed, what you did not, and why.
5. Commands actually run and their observed results; state explicitly when no build/test/migration was run and what the unrun step would confirm.
6. Limits and remaining risks, including any version-sensitive claim you could not confirm against the detected EF Core version and provider.

Distinguish confirmed Microsoft-documented behavior from synthesis in every reference; do not present a derived recommendation as a doc rule, and do not assume a newer EF Core API exists on an older detected version.
