# Migrations and Provider Realism

Load when the request concerns adding/applying migrations, deployment strategy, or choosing a database/test double. Two concerns: **migrations lifecycle** (schema evolution) and **provider realism** (does the test double behave like the real database?).

## Migrations lifecycle (documented)

- Migrations compare the current model against a **model snapshot** and generate source files tracked in source control; applied migrations are recorded in a **history table**, so only new ones apply.
- Add with `dotnet ef migrations add <Name>`; apply locally with `dotnet ef database update`.
- Deployment: `dotnet ef database update` is fine for **local development** but less suitable for **production**. Prefer a **migration bundle** (EF Core 6+) for deployment automation, or a **reviewed SQL script** when SQL approval is required. A **separate migrations project** is recommended for platform-specific apps.
- `ToTable(..., t => t.ExcludeFromMigrations())` excludes a type from a context's migrations (resolves cross-context conflicts).

## Provider realism (documented)

- Choose between the **production database system** and a **test double**. The **in-memory provider does not behave like the real database** (no transactions, no raw SQL, different case-sensitivity) and is **discouraged**.
- **Mocking `DbSet` is complex and discouraged.**
- **SQLite in-memory** is a better relational double but still differs (no provider-specific `EF.Functions`).
- The documented recommendation is at least some tests against the **production database system**; a repository layer can exclude EF from tests at an architectural cost.

## What to check in a review

1. Is `dotnet ef database update` being recommended for a production deployment instead of a bundle or reviewed script?
2. Is a type shared across contexts missing `ExcludeFromMigrations`, causing conflicts?
3. Is the in-memory provider or `DbSet` mocking used where real provider behavior matters (transactions, raw SQL, collation, concurrency)?
4. Are at least some tests run against the production database system?

## Boundary with the testing specialist

This reference states the **provider-realism hierarchy** (production DB > SQLite in-memory > never in-memory/`DbSet` mocking). Test-host and fixture-lifetime mechanics (`WebApplicationFactory`, Testcontainers, spinning up a real database) belong to `mag-dotnet-testing-quality`; hand the host mechanics there and keep only the realism decision here.

## Verified vs synthesis

The migrations lifecycle, deployment options, `ExcludeFromMigrations`, and the provider-realism hierarchy (in-memory discouraged, `DbSet` mocking discouraged, SQLite as a better-but-different double, prefer production-DB tests) are documented in the Microsoft EF Core pages. The review checklist and the testing-specialist boundary note are synthesis.

## Official references

- Migrations: https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/
- Testing EF Core applications: https://learn.microsoft.com/en-us/ef/core/testing/
