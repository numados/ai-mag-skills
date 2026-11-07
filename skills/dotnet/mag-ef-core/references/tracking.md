# Change Tracking, Identity Resolution, and Loading

Load when the request concerns which instances a query returns, whether updates are persisted, tracking overhead, or the N+1 problem. Three ideas interlock here: **tracking** (does the context watch the entity for changes?), **identity resolution** (same row → same instance?), and **loading** (when are related entities fetched?).

## Tracking and identity resolution (documented)

- Queries returning entity types are **tracking by default**; changes are persisted by `SaveChanges`, and tracking also fixes up navigation properties against already-tracked entities.
- A tracking query does **identity resolution**: if the row is already tracked, the **same instance** is returned (current/original values are not overwritten); otherwise a new instance is attached.
- A no-tracking query skips the change tracker and returns a **new instance each time**, even for the same row. No-tracking is for read-only results and is generally quicker.
- `AsNoTracking()` opts out per query; the context default can be `QueryTrackingBehavior.NoTracking` / `UseQueryTrackingBehavior(...)`, with `AsTracking()` to opt back in.
- **`AsNoTrackingWithIdentityResolution()`** (EF Core 5.0+) performs identity resolution *without* tracking, using a stand-alone change tracker scoped to the query — results are not tracked by the context.
- **Custom projections still track the entity types they contain** (e.g. an anonymous type holding a `Blog`). Only a result containing no entity type is untracked.

## Loading strategies (documented)

| Strategy | Mechanism | When | N+1 risk |
|---|---|---|---|
| **Eager** | `Include`/`ThenInclude` in the query | Load related data you will need, up front | No (single/multiple queries), but can produce a cartesian explosion with multiple collection navigations |
| **Explicit** | `Reference`/`Collection(...).Load()` (or `.Query()` to filter) | Load on demand, at a chosen point | Yes, if called per entity in a loop |
| **Lazy** | `UseLazyLoadingProxies` + `virtual` navigations, or `ILazyLoader` | Transparent load on navigation access | Yes — the classic N+1: one query per navigation access per entity |

Lazy loading is opt-in and must be enabled (proxies with `virtual` navigations on inheritable classes, or `ILazyLoader` injection). It issues a query the first time an unloaded navigation is accessed on each entity (subsequent accesses of that loaded navigation do not re-query), so looping over entities and touching navigations still produces the N+1 pattern by default; enable it deliberately, not incidentally.

## Split queries and the cartesian explosion (documented)

A single query with multiple collection `Include`s can cause a **cartesian explosion** — the joined rows multiply and duplicate data is transferred. `AsSplitQuery()` issues an additional SQL query per included collection navigation instead; the trade-off is multiple round trips and, with `Skip`/`Take`, a requirement for fully unique ordering to avoid incorrect results on some EF Core versions. Prefer `AsNoTracking` when loading collections you do not intend to modify.

## What to check in a review

1. Is a query left tracking when the results are read-only (unnecessary overhead)?
2. Is a no-tracking query treated as if it returned the same instance for repeated reads (it does not)?
3. Does a custom projection unexpectedly track an entity inside an anonymous type?
4. Is a navigation accessed in a loop (N+1) instead of eager/explicitly loaded?
5. Is lazy loading enabled without an acknowledged N+1 risk?
6. Do multiple collection `Include`s risk a cartesian explosion, and is `AsSplitQuery`/ordering considered?

## Verified vs synthesis

The tracking/no-tracking semantics, identity-resolution rules, `AsNoTrackingWithIdentityResolution` (5.0+), projection-tracking nuance, the three loading strategies, the N+1 warning, and the cartesian-explosion/split-query behavior are documented in the Microsoft EF Core pages. The review checklist and the strategy table are synthesis (structuring of documented facts).

## Official references

- Tracking vs no-tracking queries: https://learn.microsoft.com/en-us/ef/core/querying/tracking
- Change tracking in EF Core: https://learn.microsoft.com/en-us/ef/core/change-tracking/
- Identity resolution in EF Core: https://learn.microsoft.com/en-us/ef/core/change-tracking/identity-resolution
- Loading related data: https://learn.microsoft.com/en-us/ef/core/querying/related-data/
- Single vs split queries: https://learn.microsoft.com/en-us/ef/core/querying/single-split-queries
