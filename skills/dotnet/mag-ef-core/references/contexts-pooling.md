# Context Lifetime and Pooling

Load when the request concerns `DbContext` lifetime, thread-safety, `AddDbContextFactory`, context pooling, or whether per-request state (such as a tenant ID) leaks across pooled instances. This is the highest-security-risk set of EF facts: pooled contexts plus tenant state plus driver state.

## Unit-of-work lifetime (documented)

- `DbContext` is **not thread-safe**; do not share one instance across threads, and always `await` async calls immediately. Parallel operations on one instance are unsupported.
- It is a short-lived **unit of work**: create → track → change → `SaveChanges` → dispose. Detaching is unnecessary in that flow; if you must detach, `ChangeTracker.Clear()` beats per-entity detach.
- In ASP.NET Core DI, `AddDbContext` registers **scoped** (one per request). For scopes that do not align with a request (Blazor circuits, multiple units of work per request), use **`AddDbContextFactory`** and dispose the created contexts yourself.

## Context pooling (documented)

- `AddDbContextPool` (default pool size 1024; `PooledDbContextFactory` without DI) **reuses context instances across requests — effectively a singleton**. EF resets its own internal state on return to the pool. This is **orthogonal** to database connection pooling, which is driver-level (ADO.NET).
- **Tenant-state hazard:** `OnConfiguring` runs only once per pooled instance, so it cannot set per-request state such as a **tenant ID**. The documented pattern is a **scoped** `IDbContextFactory` wrapper that pulls a pooled context and injects the tenant ID per scope.
- **Driver-state hazard:** EF resets its own state but **not** state in the underlying database driver (a manually opened `DbConnection`, ADO.NET state). Restore that before returning the context to the pool, or it leaks across requests.
- `ConfigureDbContext` (applies additional configuration around `AddDbContext`) is version-gated (EF Core 9.0+) — check the detected version before assuming it exists.

## Tenant filter primitives (documented, complements pooling)

A multi-tenant model often uses a **global query filter** (`HasQueryFilter(b => b.TenantId == tenantId)`) to scope every query to the current tenant. The filter must read the tenant ID from the context instance (constructor/property), and `IgnoreQueryFilters()` bypasses it deliberately. A single `HasQueryFilter` call overwrites a prior one on the same entity type — combine filters with `&&` rather than calling it twice. The named-filter overload (`HasQueryFilter(name, filter)`, enabling named filter sets per query) exists only on EF Core 10+; on earlier versions combine predicates into one expression and toggle via `IgnoreQueryFilters()`. This is the tenant primitive that the pooled-context wrapper must keep correct.

## What to check in a review

1. Is a `DbContext` shared across threads or held past its unit of work?
2. Is tenant/request state set in `OnConfiguring` on a pooled context?
3. Is a manually opened connection/ADO.NET state left on the context when it returns to the pool?
4. Is a tenant filter reading the tenant from a per-context value, not a static/singleton?
5. Is `IgnoreQueryFilters()` used anywhere it would silently cross tenants?

## Verified vs synthesis

Unit-of-work lifetime, thread-safety, `AddDbContext` scoping, `AddDbContextFactory`, pooling semantics and the two pooling hazards, and the global-query-filter tenant pattern are documented in the Microsoft EF Core pages. The "highest-risk set" framing and the review checklist are synthesis.

## Official references

- DbContext configuration and lifetime: https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/
- Advanced performance topics (pooling): https://learn.microsoft.com/en-us/ef/core/performance/advanced-performance-topics
- Global query filters: https://learn.microsoft.com/en-us/ef/core/querying/filters
