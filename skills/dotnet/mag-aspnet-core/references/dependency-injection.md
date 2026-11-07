# Dependency Injection and Lifetimes

Load when the request concerns service registration, lifetimes, a captive dependency, scoped state leaking across requests, or a `DbContext` held by the wrong owner.

## Three lifetimes

- **Transient** — created each time it is resolved. Use for stateless, cheap services.
- **Scoped** — created once per scope (in ASP.NET Core, once per request). Use for per-request state. `DbContext` is registered scoped by `AddDbContext`.
- **Singleton** — created once for the application lifetime. Use only for app-wide, thread-safe state.

The rule is not "longest lifetime wins"; it is that a service's state must not outlive the scope it belongs to.

## Captive dependencies

A singleton must not depend on a scoped or transient service whose own dependencies are scoped. The container will resolve it once at the singleton's construction, effectively promoting it to singleton — so a scoped `DbContext` captured by a singleton becomes a shared instance across requests, which is a correctness and thread-safety defect. The container may warn about this ("captive dependency"), but do not rely on the warning alone to catch every case.

## Request scope and background work

- A scoped service is valid for the lifetime of one request. Do not hold it and use it after the request ends, and do not capture it into a `BackgroundService`/hosted service, which has no request scope.
- For background work that needs per-unit-of-work state, create a scope (`IServiceScopeFactory.CreateScope()`) for that unit of work and dispose it, rather than borrowing the request's scoped services.

## Resolving the right way

- Prefer constructor injection. Service-locator style (`IServiceProvider.GetService`) is a fallback; when a singleton must access request-scoped state, resolve from `HttpContext.RequestServices` inside the request, not from a captured root provider.
- In middleware, the request's scoped services come from `HttpContext.RequestServices`, not from the constructor-injected singleton provider.

## Tenant-scoped state (synthesis)

In a multi-tenant app, any per-tenant value (tenant ID, tenant connection string) is request-scoped state. Register the resolver as scoped so it is resolved fresh per request; do not bake the current tenant into a singleton. This is derived guidance consistent with the lifetime rules, not a named Microsoft multi-tenancy section.

## What to check in a review

1. Does a singleton hold a scoped service or a `DbContext`?
2. Is a scoped service used after the request ends or inside a background service without a fresh scope?
3. Is the tenant/request identity resolved from a scoped source rather than a singleton?
4. Is service-locator style used where constructor injection would do, or used off the root provider where `RequestServices` is required?

## Verified vs synthesis

Lifetime definitions, the captive-dependency hazard, and the scoped `DbContext` registration are documented in the ASP.NET Core DI page. The tenant-scoped-state paragraph and the review checklist are synthesis.

## Official references

- Dependency injection in ASP.NET Core: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection
