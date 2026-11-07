# Query Translation and Client Evaluation

Load when the request concerns whether a LINQ query translates to SQL, where client evaluation happens, a query-plan cache leak, or raw SQL. Lead rule: **server-side by default; client evaluation is allowed only in the top-level projection.**

## Server-side by default

EF Core translates LINQ to the provider's query language and executes against the database — even when the entities are already tracked in the context. It converts parts of the query into SQL parameters.

## Client evaluation (documented, version-sensitive)

- Since **EF Core 3.0**, partial client evaluation is allowed only in the **top-level projection** (the final `Select`). An untranslatable expression anywhere else throws a runtime exception. Older EF Core (pre-3.0) evaluated client-side anywhere and logged a warning instead — do not assume that old behavior on a modern detected version.
- Explicit opt-in to client evaluation is `AsEnumerable`/`ToList` (or `AsAsyncEnumerable`/`ToListAsync`); `AsEnumerable` streams while `ToList` buffers.

## Query-plan cache leak (documented)

The translation/query-plan cache can grow unbounded when the expression tree contains constants EF cannot turn into parameters — instance methods captured as `this`, constants in method arguments, and other non-parameterizable constants. Mitigations:

- make helper methods `static` so `this` is not captured;
- pass instance data as explicit arguments;
- hoist constants into local variables that become parameters.

## Raw SQL (documented; method names are version-sensitive)

For queries, begin with `FromSql` on a `DbSet`; for non-query commands use `ExecuteSql`; for scalar results use `SqlQuery` (EF Core 7+; arbitrary unmapped non-entity CLR result types are EF Core 8+ — gate on the detected version). The parameterized/interpolated forms (`FromSql`, `ExecuteSql`) are safe against SQL injection and send values as parameters; the `Raw` forms (`FromSqlRaw`, `ExecuteSqlRaw`) interpolate the string directly and are injection-prone — use them only for values that cannot be parameterized (e.g. schema/column names), and sanitize.

Two constraints: composable `FromSql` SQL must be valid as a subquery (begin with `SELECT`, no stored-procedure calls that break composition), and `FromSql`/`FromSqlRaw` follow the same tracking rules as any LINQ query. On EF Core versions before 7.0, the parameterized method names were `FromSqlInterpolated`/`ExecuteSqlInterpolated` — confirm the exact names against the detected EF Core version rather than assuming the current surface.

## What to check in a review

1. Is an untranslatable expression outside the top-level projection going to throw at runtime?
2. Is `AsEnumerable`/`ToList` used as an accidental client-eval trigger (pulling rows into memory) rather than a deliberate choice?
3. Does a query contain non-parameterizable constants that would leak the query-plan cache?
4. Does raw SQL use the parameterized form, and is any `...Raw` call limited to values that genuinely cannot be parameterized?
5. Is a stored procedure being composed over, producing invalid SQL?

## Verified vs synthesis

The server-side default, the EF Core 3.0 top-projection-only client-eval rule, the `AsEnumerable`/`ToList` opt-in, the query-plan cache leak and mitigations, and the raw-SQL parameterization/injection facts are documented in the Microsoft EF Core pages. The review checklist is synthesis. The pre-7.0 method-name note is version-sensitive: re-confirm against the detected version's documentation.

## Official references

- EF Core querying overview: https://learn.microsoft.com/en-us/ef/core/querying/
- Client vs server evaluation: https://learn.microsoft.com/en-us/ef/core/querying/client-eval
- SQL queries (raw SQL): https://learn.microsoft.com/en-us/ef/core/querying/sql-queries
