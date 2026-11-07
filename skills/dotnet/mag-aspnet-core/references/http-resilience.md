# Outbound HTTP, Resilience, and Cancellation

Load when the request concerns an `HttpClient`, retry/circuit-breaker/hedging behavior, or whether a retry can duplicate a side effect. The primary rule: **the standard resilience handler retries all HTTP methods by default, including unsafe ones, and that can duplicate side effects.**

## The package and the handler

Resilience for `HttpClient` is delivered by the `Microsoft.Extensions.Http.Resilience` package (which depends on `Microsoft.Extensions.Resilience` and Polly). Add it with `AddStandardResilienceHandler` on an `IHttpClientBuilder`. Treat availability as package/version-gated — confirm the package is referenced and its version before assuming the API exists for the target framework.

## The unsafe-retry hazard (documented)

The standard resilience handler retries **all** HTTP methods by default — including `POST` — so a retry after a timeout or a 5xx can re-run a non-idempotent operation and insert the same record twice, charge twice, or send a notification twice.

For any non-read-only outbound call, disable retries for unsafe methods:

- `options.Retry.DisableForUnsafeHttpMethods()` — disables `POST`, `PATCH`, `PUT`, `DELETE`, `CONNECT` (RFC "unsafe" = non-read-only semantics); or
- `options.Retry.DisableFor(HttpMethod.Post, HttpMethod.Delete, ...)` — an explicit list.

Hedging (`AddStandardHedgingHandler`) retries **slow** requests **in parallel**, which is equally unsafe for non-idempotent methods; apply the same idempotency reasoning there.

## Standard handler defaults (documented, for the current package)

Treat these as the documented defaults of the standard handler as shipped, and re-check the resolved package version rather than trusting them blindly:

- **Retry** — up to 3 retries after the original request (up to 4 attempts total), exponential backoff with jitter, ~2s initial delay.
- **Circuit breaker** — 10% failure ratio, minimum throughput 100, 30s sampling duration, 5s break.
- **Attempt timeout** — 10s.
- **Total request timeout** — bounds the whole attempt-plus-retry sequence.

Retry and the circuit breaker handle HTTP **500+, 408, 429** and the exceptions `HttpRequestException` and Polly's `TimeoutRejectedException`.

## Cancellation

Thread `HttpContext.RequestAborted` through every outbound call. A client that disconnects should stop the work: an outbound call that ignores the request's cancellation token keeps consuming a connection and doing work nobody will receive. When you add a resilience handler, do not drop the token — pass it through `HttpClient`'s cancellation parameter so a request abort actually cancels the attempt.

## What to check in a review

1. Is a non-idempotent method (`POST`/`PATCH`/`PUT`/`DELETE`) sent through a client whose retry policy still retries it?
2. Is hedging enabled for a non-idempotent call?
3. Is the caller's `RequestAborted` token passed to the outbound call, or dropped?
4. Is the resilience package actually referenced, and its version known, before its API is assumed?

## Verified vs synthesis

The retries-all-methods default, `DisableForUnsafeHttpMethods`, hedging semantics, and the default numbers are documented in the Microsoft HTTP-resilience page. The instruction to thread `RequestAborted` is standard ASP.NET Core cancellation guidance combined with the resilience facts; the review checklist is synthesis.

## Official references

- Build resilient HTTP apps: https://learn.microsoft.com/en-us/dotnet/core/resilience/http-resilience
- HTTP context and `RequestAborted`: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/http-context
