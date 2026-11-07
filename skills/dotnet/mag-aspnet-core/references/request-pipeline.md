# Request Pipeline and Middleware Order

Load when the request concerns middleware composition, ordering defects, short-circuiting, or response/caching/compression interaction. This reference encodes ordering as **position constraints between pairs**, not a single frozen list, because several middleware positions are scenario-dependent.

## Why order is a contract, not style

Middleware runs in the order added in `Program.cs`; the response flows back through the same chain in reverse. A middleware that must observe an earlier middleware's effect (or add headers/culture before a later one reads them) depends on that relative position. Ordering mistakes are correctness, security, and performance defects, not cosmetics.

## Position constraints (Microsoft-documented)

- **CORS before response caching** — `UseCors` must precede `UseResponseCaching` so CORS headers are present on cached responses. A cached response without CORS headers is not reusable by the intended cross-origin caller.
- **Request localization before culture readers** — `UseRequestLocalization` must precede any middleware that reads request culture.
- **Rate limiter after routing** — when endpoint-specific limiters (`[EnableRateLimiting]`) are used, `UseRateLimiter` must come after `UseRouting`, because the limiter needs the selected endpoint.
- **Authentication → Authorization → endpoint** — `UseAuthentication` runs before `UseAuthorization`, and both precede endpoint mapping (`MapControllers`, `MapRazorPages`, `MapControllerRoute`). Authentication middleware does **not** short-circuit unauthenticated requests; authorization is evaluated only after the framework selects the endpoint.
- **Exception handling near the front** — `UseExceptionHandler` (or `UseDeveloperExceptionPage` in Development) should be early so it can catch exceptions from later middleware and return a structured error response.

## Scenario-dependent pairs

- **Response caching vs response compression** — `UseResponseCaching` before `UseResponseCompression` can cache the compressed representation, but risks storing multiple representations (one per compression algorithm). There is no single correct order; choose and document the intended representation.
- **Static files** — `UseStaticFiles`/`MapStaticAssets` serves static content without hitting the rest of the pipeline; place it before routing where static files should bypass auth-less endpoints, and after authentication where static content must be protected.

## Canonical order for a typical MVC/Razor Pages pipeline

For a standard app, the order is approximately: exception handling → `UseHsts` → `UseHttpsRedirection` → static files → `UseCookiePolicy` → `UseRouting` → `UseCors` → `UseAuthentication` → `UseAuthorization` → `UseSession` (Razor Pages/MVC only) → endpoint mapping. Treat this as the default starting point, then apply the pairwise constraints above for the features actually present.

## What to check in a review

1. Does CORS precede response caching?
2. Does culture-reading middleware follow request localization?
3. Is the rate limiter after routing when endpoint-specific limiters exist?
4. Is the order authentication → authorization → endpoint preserved?
5. Does any middleware assume an earlier middleware already ran a step it needs?
6. Is exception handling early enough to catch failures from the rest of the chain?
7. Is the response-caching/compression representation choice explicit and documented?

## Verified vs synthesis

The pairwise constraints and the canonical order above are stated in the Microsoft middleware documentation. The "position constraints between pairs, not a frozen list" framing and the review checklist are synthesis (a structuring of documented facts), not a verbatim doc rule.

## Official references

- ASP.NET Core Middleware: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/
