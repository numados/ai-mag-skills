---
name: mag-csharp-implementation
description: Implement an authorized C# or .NET feature, bug fix, API integration, or test addition by detecting the effective SDK, language version, target framework, runtime, and package versions and preserving local contracts; own nullability, value/reference/equality semantics, exceptions, disposal, async propagation, and behavior-seam verification. Use for implementation, not review-only, project-only, lifecycle-first, or performance-first requests.
---

# C# Implementation

## When to Use

Use for an authorized C#/.NET feature, bug fix, API integration, test addition, or bounded implementation task in an existing repository. This skill is self-contained for ordinary C# behavior: inspect layout and the version contract here.

Do not use, and route to a specialist, when the primary outcome is:

- read-only review or diagnosis of existing code or a diff — use `mag-csharp-review`;
- creating or extending a solution/project, resolving package compatibility, or publishing/AOT/trimming — use `mag-dotnet-project`;
- task ownership, cancellation, bounded concurrency, or shutdown as the dominant concern — use `mag-dotnet-async-reliability`;
- a measured performance problem — use `mag-dotnet-performance`.

An ordinary feature that happens to contain an async method is still implementation; an unreliable worker lifecycle is async work. A question that only asks for an explanation does not authorize edits.

Do not silently broaden a behavior change into a refactor, modernization, dependency upgrade, or API redesign.

## Establish the repository contract

1. Read repository instructions and the relevant requirement or failing behavior.
2. Locate the solution and project, and read `global.json`, the `.csproj`, `Directory.Build.*`, `Directory.Packages.props`, `.editorconfig`, analyzer settings, and the test project.
3. Detect versions separately — they are independent facts:
   - **SDK** — `global.json` `sdk.version` governs tooling/MSBuild, not the target framework;
   - **compiler / language version** — `<LangVersion>` in the project or `Directory.Build.*`, else the TFM-derived default;
   - **target framework(s)** — `<TargetFramework>` / `<TargetFrameworks>` (e.g. `net8.0`, `net9.0`, `netstandard2.0`, `net48`);
   - **runtime** — the executable's TFM/`runtimeconfig`; a library targets a TFM, not a specific runtime;
   - **packages** — central versions in `Directory.Packages.props` or direct `PackageReference`; resolved versions come from restore/assets;
   - **analyzers and style** — `.editorconfig`, `AnalysisLevel`, and analyzer packages.
4. Trace the entry point, direct callers, downstream consumers, and the affected tests.
5. State the intended behavior, affected files, non-goals, and the verification plan. When an edit-producing request has no source file in scope, ask for it or synthesize a clearly labeled representative file and state the assumption.

The default C# language version follows the target framework, not a universal "latest". Do not assume C# 12/13 or .NET 8/9; read the project. For an uncertain requirement, ask the smallest question that changes the implementation.

## Implement

Prefer the smallest change that fits established boundaries. Preserve layering, dependency injection, naming, namespace, error, async, serialization, and test patterns.

Own these C# semantics rather than deferring them:

- **Nullability and validation.** Preserve the nullable contract at boundaries: do not widen a non-null return to nullable or drop validation callers rely on. Match `#nullable` / `<Nullable>`, nullable-warning, and warnings-as-errors policy. Distinguish nullable reference types (compile-time flow analysis) from `Nullable<T>` (a runtime value type).
- **Value/reference and equality.** Choose `struct`, `class`, `record`, or `record struct` for its semantic reason (value identity, copy, equality), not habit. Match the equality contract: `==`, `object.Equals`, `IEquatable<T>`, `GetHashCode`, and compiler-generated record equality. Never define `Equals` without a matching `GetHashCode`. Respect `readonly struct`, `ref struct`, and `Span<T>`/`ReadOnlySpan<T>` constraints — do not box or store a `ref struct` where the runtime forbids it.
- **Exceptions.** Throw the repository's exception type at the right layer. Catch only what you can handle meaningfully at that layer; preserve the original exception with `throw;` or an inner exception; use exception filters when a condition decides handling. Keep resources acquired before a throw released (see disposal).
- **Disposal and async disposal.** Make ownership visible: who creates an `IDisposable`/`IAsyncDisposable` and who must release it. Prefer `using` / `await using` scoped to the ownership boundary, so disposal also runs on exception and early-return paths. Transfer ownership only explicitly (a factory or a returned live resource) and document it.
- **Async propagation.** Propagate `Task`/`Task<T>`/`ValueTask` honestly: `await`, or return the task. Avoid `async void` except for event handlers. Honor the repository's `ConfigureAwait` precedent (library versus UI/ASP.NET). Propagate `CancellationToken` through awaited calls where the surrounding contract supports it; do not swallow or fabricate cancellation. Avoid sync-over-async (`.Result`, `.Wait()`, `GetAwaiter().GetResult()`) unless the boundary is a documented, deadlock-safe exception.

## Compatibility boundaries

Preserve source, binary, and wire compatibility for the public surface within scope: keep public signatures, persisted data, message/JSON schemas, and configuration backward compatible unless the request explicitly changes that contract. Renaming or removing a public member, changing a return type, or altering serialization is a breaking change and requires explicit authorization.

The detailed compatibility checklist (PublicAPI/ApiCompat baselines, generated code, multi-TFM surface audit) belongs to the review and refactor specialists; this skill preserves the basics and defers deep audit.

Do not modernize, re-architect, or add/upgrade dependencies unless the request asks for it.

## Tests and verification

Add or update tests at the behavior seam:

- unit tests for private invariants;
- integration or contract tests for public behavior;
- error, boundary, cancellation, and disposal cases;
- cases for the nullable and equality contract you changed.

Use the repository's configured test framework (xUnit, NUnit, MSTest) and commands; do not impose a different runner. Prefer the narrowest build/test target (a single project), then broaden only when risk or policy warrants it.

Before running `dotnet restore`/`build`/`test`, assess trust and authorization: restore downloads packages, and build/test executes analyzers, source generators, and test code. Match the repository's restore policy (locked/offline, package feeds). Report exact commands and actual results; never claim completion from an unrun check.

## Version-sensitive rules

When the change uses an unfamiliar or version-sensitive API, syntax, compiler option, or analyzer, verify it against current official Microsoft/.NET documentation for the effective versions (see `references/version-and-docs.md`). When the requested API does not exist on the detected TFM, do not emit non-compiling code: state the mismatch, propose a compatible alternative, and ask the smallest question. Build the smallest affected target soon after introducing the construct; treat compiler and analyzer diagnostics as evidence and investigate version/configuration mismatch rather than guessing syntax. If authoritative documentation is unavailable, reuse a verified repository precedent or report the uncertainty — never invent an API.

## Output

Report:

- the detected SDK, language version, TFM(s), runtime, package, and analyzer facts as separate items — state `not detected` when absent rather than assuming a default;
- changed behavior and non-goals, with every claim anchored to `path:line` or the exact contract it changes;
- files and contracts changed;
- tests added or updated;
- commands run and actual results;
- compatibility, resource, and remaining-risk notes, with a `not run / not verified` subsection naming every command not executed and every unconfirmed fact.
