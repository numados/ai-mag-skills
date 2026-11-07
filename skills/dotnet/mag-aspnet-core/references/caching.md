# Caching and Tenant Isolation

Load when the request concerns `IMemoryCache`, `IDistributedCache`, response caching, cache keys, expiration, or whether one tenant can observe another tenant's cached value.

## The two cache abstractions

- `IMemoryCache` — in-memory, process-local, can store any object. On a server farm without sticky sessions, process-local caches diverge; use a distributed cache for cross-instance consistency.
- `IDistributedCache` — shared across instances, but limited to `byte[]` values; serialize explicitly.

The response-cache **middleware** is a third thing: it caches server responses keyed by HTTP `Cache-Control` headers, for **public GET/HEAD** API responses, always honoring RFC 9111 semantics.

## Expiration and limits (documented)

- A cached entry with only a **sliding** expiration can effectively never expire under continuous access; combine sliding with an **absolute** expiration. Expiration is lazy — there is no background timer; activity triggers scans.
- `SizeLimit` has **no defined unit**, is not enforced against real memory pressure by the runtime, and every entry must set a size when a limit is configured. A shared (framework-provided) cache with size limits can fail because not every consumer sets sizes — use a dedicated cache singleton when size-limiting.
- Do not insert arbitrary/external user input as a cache key: it enables unpredictable memory consumption.

## Response-cache variation (documented)

- `VaryByHeader` and `VaryByQueryKeys` vary the stored response. `VaryByQueryKeys` requires the middleware to be enabled or it throws at runtime; the wildcard `*` varies by all query keys.
- `Cache-Control: private` must not be stored by a shared cache; `public` may be. Response caching is only useful for public, read-only GET/HEAD responses.
- Output caching (policy-driven, better for UI) is a separate, version-gated API (available from a specific ASP.NET Core version — check the detected framework version); `HybridCache` is newer still and separately version-gated. Do not assume either exists for the target framework.

## Tenant isolation (synthesis — not a named Microsoft section)

The ASP.NET docs state that `IMemoryCache`, `IDistributedCache`, and the response-cache middleware are **app-wide and shared across tenants and requests**; there is no dedicated multi-tenancy caching section. The documented mechanics imply these rules for a multi-tenant app:

1. **Scope cache keys by tenant identity** — a key must include the tenant, or one tenant reads another tenant's cached value.
2. **Vary response-cache entries by tenant** — `VaryByHeader` on a tenant header, or an equivalent custom key, so a cached response is not served to the wrong tenant.
3. **Never cache tenant-sensitive data under a tenant-agnostic key** — if the value is tenant-specific, the key must be too.

Treat these as derived requirements activated only when tenancy is present, not as a verbatim doc rule.

## What to check in a review

1. Does a cache key omit the tenant identity while the value is tenant-specific?
2. Does a response-cache entry lack tenant variation (`VaryByHeader`/custom key)?
3. Is arbitrary user input used as a cache key?
4. Is a sliding-only expiration relied on to eventually expire?
5. Is `SizeLimit` used on a shared cache where not all consumers set sizes?
6. Is a process-local `IMemoryCache` assumed to be consistent across a server farm?

## Official references

- Cache in-memory in ASP.NET Core: https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory
- Response caching in ASP.NET Core: https://learn.microsoft.com/en-us/aspnet/core/performance/caching/response
- Output caching in ASP.NET Core: https://learn.microsoft.com/en-us/aspnet/core/performance/caching/output
