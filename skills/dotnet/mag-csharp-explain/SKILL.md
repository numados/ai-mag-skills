---
name: mag-csharp-explain
description: Explain concrete C# or .NET code — a block, method, type, file, or module — and its runtime behavior in plain language, with accurate value/reference, nullable, equality, generics, LINQ deferred execution, async/await, disposal, and cancellation mechanics plus bounded caller/data-flow context. Use for explanation only; never turn an explanation into a review or implementation, and never edit code.
---

# C# Explain

## When to Use

Use when the user asks what concrete C#/.NET code does, how it works, why it is shaped this way, or how it fits into the surrounding module, project, or data flow. The deliverable is an explanation grounded in the code, not a change.

Do not use it as a silent step inside another task. An explanation request does not authorize editing, fixing, reviewing, or refactoring the code. For a mixed request, route by the dominant outcome — if it is primarily "list what is wrong", it belongs to `mag-csharp-review`; if it is primarily a change, to `mag-csharp-implementation` or `mag-csharp-refactor`. When the explanation is the dominant ask and a change is mentioned as a follow-up, deliver the explanation first and treat the change as a separate request needing its own authorization.

A short, clearly labelled closing note may mention an obvious risk or behavior worth knowing, but only as an observation, and only when it does not drift into prescribing a fix or scoring the code.

## Method

1. Read the supplied target completely. For a file or module, begin with a structure map (public surface, main paths, state) instead of narrating every line.
2. Trace imports, direct callers, and callees only as far as needed to explain integration. When surrounding context is not supplied, say so rather than inventing it.
3. Separate facts proven by code from inferred intent. Say "the code guarantees…" versus "this appears intended to…". Never invent callers, author intent, or performance claims the code or measurements do not support.
4. Explain the C#/.NET machinery that actually applies, in context — do not recite the language reference:

   - **Value vs reference and equality** — `class` vs `struct` vs `record` vs `record struct`; reference equality vs `Equals`/`IEquatable<T>`/`GetHashCode`/`==`; `ref struct` (span) constraints; boxing; `readonly`.
   - **Nullability** — nullable reference types as compile-time flow analysis vs `Nullable<T>` as a runtime value type; the project's `#nullable`/`<Nullable>` context.
   - **Generics and variance** — constraints, `in`/`out`, how the runtime reifies closed constructed types.
   - **LINQ deferred vs immediate execution** — a query is a description, re-enumerated on each iteration and reading captured variables at enumeration time; `ToList`/`ToArray`/`Count`/`First` materialize or trigger execution. State exactly *when* a query runs and how many times it is enumerated.
   - **async/await** — what `await` unwraps and what it does not; where a continuation resumes (`SynchronizationContext`/`TaskScheduler`/`ConfigureAwait`); `async void` as an event-handler-only shape; `Task` vs `ValueTask` single-consumption semantics.
   - **Disposal** — `using` vs `await using`, `IDisposable` vs `IAsyncDisposable`, ownership transfer, and the fact that `using` guarantees release on exception and early-return paths.
   - **Cancellation and exceptions** — `CancellationToken` propagation, `OperationCanceledException`, how an unobserved `Task` fault is (or is not) surfaced, exception filters, `throw;` re-throw semantics.
5. Keep standard C#/.NET terms in English when answering in another language; translate only the surrounding prose.

## Version-sensitive facts

When the code uses an API, syntax, or compiler feature whose availability depends on the target framework (TFM) or language version, name that floor instead of assuming the newest release. Examples: `TimeProvider`/`ITimer` is in-box from .NET 8; `Task.WhenEach` is .NET 9+; a record, pattern, or `allows ref struct` syntax is gated by the language version. If the project's TFM is not visible, state that the fact is conditional and say what a confirming project file would establish.

For an unfamiliar or version-sensitive construct, verify it against current official Microsoft/.NET documentation for the effective TFM and language version (see `mag-csharp-implementation`'s `references/version-and-docs.md` for the official routing). When documentation is unreachable, report the uncertainty — never assert an API signature or behavior from memory.

## Output

~~~markdown
## What it does
One or two sentences answering the question directly.

## How it works
Numbered execution steps tied to identifiers, fragments, or file lines; note where a query is deferred, where an await resumes, and where a resource is released.

## Where it fits
- callers and inputs;
- dependencies and outputs;
- role in the module, project, or data flow.

## Why it is shaped this way
Concrete C#/.NET or domain reasons, with inferred intent clearly labelled as inference.

## Limits
Untraced callers, missing project/configuration context, and assumptions not proven by the supplied code.
~~~

For a small snippet keep every section short. For a file or module lead with the structure map. Do not invent callers, performance claims, or intent, and do not end with a fix unless the user separately asked for one.
