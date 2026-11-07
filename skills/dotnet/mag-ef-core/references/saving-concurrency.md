# Saving, Concurrency, and Bulk Bypasses

Load when the request concerns `SaveChanges` atomicity, transactions, retry execution strategies, optimistic concurrency, or `ExecuteUpdate`/`ExecuteDelete`. These are the highest-risk, hardest-to-recall saving rules.

## SaveChanges atomicity (documented)

By default all changes in **one `SaveChanges` call** run in a transaction (when the provider supports transactions), so `SaveChanges` is atomic. `AutoTransactionBehavior` (EF Core 7+) is `WhenNeeded` by default, with `Always` and `Never` available; `Never` disables the implicit transaction and must be used with care (partial commits).

## Manual transactions vs retry strategies (documented)

- Manual transactions use `context.Database.BeginTransactionAsync()`.
- **Manual transaction control is incompatible with implicit retry execution strategies** — combining them throws `InvalidOperationException`. The fix is to wrap the manual transaction in `context.Database.CreateExecutionStrategy().ExecuteAsync(...)`.
- EF creates a **savepoint** automatically when `SaveChanges` runs inside an existing transaction, and rolls back to it on failure — useful for optimistic-concurrency retry. Savepoints are **incompatible with SQL Server MARS**.
- Connection resiliency (`EnableRetryOnFailure` on SQL Server) retries failed commands via an execution strategy; each query/`SaveChanges` is its own retriable unit. Enabling retry **buffers result sets** and can raise memory use for large results.

## Commit-failure ambiguity (documented)

If the connection drops during commit, the outcome is unknown and the strategy retries as if rolled back. Use `IExecutionStrategy.ExecuteInTransaction` with a `verifySucceeded` check (or manual transaction tracking via a status table), and pass `acceptAllChangesOnSuccess: false` to allow retrying `SaveChanges`.

## Optimistic concurrency (documented)

Configure a **concurrency token**: `[Timestamp]`/`IsRowVersion()` for SQL Server `rowversion`, or `IsConcurrencyToken()` for application-managed tokens on providers (like SQLite) with no auto-updating type. On save, EF compares the token; **zero rows affected ⇒ `DbUpdateConcurrencyException`**, which the app must resolve by comparing `OriginalValues`/`CurrentValues`/`DatabaseValues`, refreshing originals, and retrying.

## ExecuteUpdate / ExecuteDelete bypasses (documented, EF Core 7.0+)

`ExecuteUpdate`/`ExecuteDelete` translate LINQ to SQL and run in the database **without loading or tracking entities**, using `SetProperty(...)` (which can reference the current column value, e.g. `b.Rating + 1`). They are an explicit bypass with three hard consequences:

1. **No change-tracker interaction** — they take effect immediately; mixing them with tracked `SaveChanges` on the same entities causes the tracked instance to **overwrite** the bulk change. Avoid mixing.
2. **No implicit transaction** — each call runs in its own transaction; wrap multiple calls in `context.Database.BeginTransaction()` to make them atomic.
3. **No automatic optimistic concurrency** — there is no change tracker; implement it manually by including the concurrency token in the `Where` and treating zero affected rows as a conflict.

`SetProperty` cannot reference navigations directly (project via `Select` to an anonymous type, then `ExecuteUpdate` over it). Insert is not supported (use `Add` + `SaveChanges`), and retrieving original values (OUTPUT) is not supported.

## What to check in a review

1. Is a manual transaction combined with an implicit retry strategy without the `CreateExecutionStrategy().ExecuteAsync` wrapper?
2. Is `SaveChanges`'s implicit transaction relied on across multiple separate `SaveChanges` calls?
3. Is a concurrency token configured, and is `DbUpdateConcurrencyException` handled rather than swallowed?
4. Are `ExecuteUpdate`/`ExecuteDelete` mixed with tracked entities, or multiple calls made without an explicit transaction when atomicity is required?
5. Is commit-failure ambiguity handled for a retrying commit, or assumed safe?
6. Are savepoints relied on under SQL Server MARS?

## Verified vs synthesis

`SaveChanges` atomicity, the manual-vs-retry incompatibility and `ExecuteAsync` wrapper, savepoint/MARS incompatibility, connection-resiliency buffering, commit-failure ambiguity, optimistic-concurrency tokens and `DbUpdateConcurrencyException`, and the three `ExecuteUpdate`/`ExecuteDelete` bypass consequences are documented in the Microsoft EF Core pages. The review checklist is synthesis.

## Official references

- Saving data / transactions: https://learn.microsoft.com/en-us/ef/core/saving/transactions
- Handling concurrency conflicts: https://learn.microsoft.com/en-us/ef/core/saving/concurrency
- Connection resiliency: https://learn.microsoft.com/en-us/ef/core/miscellaneous/connection-resiliency
- ExecuteUpdate and ExecuteDelete: https://learn.microsoft.com/en-us/ef/core/saving/execute-insert-update-delete
