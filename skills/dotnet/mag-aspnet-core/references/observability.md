# Logging, Redaction, and Observability

Load when the request concerns what to log, how to avoid leaking sensitive data into logs, or how to make a service observable. The foundation is **structured logging**; redaction is a compliance layer wired through that pipeline; observability adds correlated traces on top.

## Structured logging

ASP.NET Core logging is structured via `ILogger<TCategoryName>`. Log **category**, **level**, and **provider** are independent configuration axes — changing one does not imply another. Default providers come from `WebApplication.CreateBuilder` / `Host.CreateDefaultBuilder`. Prefer structured logging over ad-hoc `Console.WriteLine`, and pass structured state (`logger.LogInformation("Order {OrderId} placed", order.Id)`) rather than string-concatenating values into the message.

The principle the docs state plainly: sensitive information — personal data, credentials, financial details — **must never be written to logs in plain text**.

## Redaction

Redaction is delivered by the `Microsoft.Extensions.Compliance.Redaction` package, with built-in redactors such as:

- `ErasingRedactor` — replaces the value with an empty string.
- `HmacRedactor` — HMACSHA256-based; **experimental** (using it emits warning `EXTEXP0002`; suppress only deliberately with `NoWarn`/`#pragma`). Its `Key` must be base64 and ≥ 44 characters, use distinct keys per deployment, and `KeyId` is appended to each redacted value so values under different `KeyId`s are not correlatable.

Register with `AddRedaction(...)` and map redactors to **data classifications** via `SetRedactor<T>` / `SetFallbackRedactor<T>` / `SetHmacRedactor(...)`.

To redact in logs specifically: install `Microsoft.Extensions.Telemetry`, call `builder.EnableRedaction()` in the logging builder, and annotate sensitive parameters with a `[DataClassification]`-derived attribute (e.g. `[Private]`), producing output like `User SSN: *****`.

## Observability

Observability means structured logs plus correlated distributed traces, so a request can be followed across services. .NET exposes tracing through `Activity` and OpenTelemetry integration; emit/forward traces and attach correlation IDs instead of relying on log lines alone. Treat specific OpenTelemetry wiring (exporters, resource attributes, sampling) as version-sensitive — verify against the current documentation and the resolved package versions rather than asserting a fixed recipe.

## What to check in a review

1. Is sensitive data logged in plain text (personal data, credentials, financial details)?
2. Is redaction enabled and are classifications/redactors mapped, or is there a hole where sensitive parameters reach the log?
3. Is `HmacRedactor` used without acknowledging its experimental status and key requirements?
4. Are logs structured (structured state, stable category/level), or string-interpolated ad-hoc?
5. Is there correlated tracing, or only disconnected log lines?

## Verified vs synthesis

The structured-logging model, the never-log-secrets principle, the redaction package/redactors, the `HmacRedactor` experimental status and key requirements, and the `EnableRedaction` + classification-attribute wiring are documented in the Microsoft logging, compliance, and data-redaction pages. The review checklist and the "logs plus correlated traces" framing are synthesis.

## Official references

- Logging in .NET and ASP.NET Core: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/logging/
- .NET extensions compliance: https://learn.microsoft.com/en-us/dotnet/core/extensions/compliance
- Redact sensitive data: https://learn.microsoft.com/en-us/dotnet/core/extensions/data-redaction
- Observability with OpenTelemetry: https://learn.microsoft.com/en-us/dotnet/core/diagnostics/observability-with-otel
