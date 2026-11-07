---
name: mag-csharp-refactor
description: Refactor or modernize existing C# while preserving observable behavior, public/source/binary/wire contracts, evaluation order and short-circuiting, serialization, exceptions, disposal and async/ValueTask semantics, and measured performance, by freezing a baseline, grading each move by risk, and verifying bounded steps. Use for behavior-preserving restructuring only; a business-rule or behavior change is implementation, not refactor.
---

# C# Refactor

## When to Use

Use when the user asks to improve, modernize, simplify, restructure, or clean up existing C# while keeping behavior stable. "Refactor" here means: the same observable behavior with a different internal shape.

Do not use for a feature, bug fix, or business-rule change — that is `mag-csharp-implementation`. Do not silently change a public signature, persisted or wire format, exception type or timing, evaluation order, disposal path, async shape, or dependency set. For a mixed request, route by the dominant outcome: a behavior change that dominates goes wholly to implementation; when the structural cleanup dominates, the behavior change stays out of scope here — name it and hand it to implementation with its own authorization. Never fold one into the other.

A diagnosis, review, or "should I refactor?" question is read-only: assess and plan, but change nothing until an edit is authorized.

## Freeze the baseline

1. Read repository instructions and the relevant `.csproj`/`.sln`, and detect the contract as independent facts — **SDK**, **LangVersion**, **TFM(s)**, **runtime**, **packages**, **analyzers** — never as one "the .NET version".
2. Inspect the working tree and preserve unrelated work. Never reset, clean, checkout, or stash the whole tree to undo an agent edit; undo only your own changes from a saved patch or targeted edits.
3. Record current behavior: the tests that pass, the build configuration, and any relevant performance measurement. If nontrivial logic lacks characterization tests, propose them before changing code.
4. Decide whether restore/build/test are trusted and authorized. Restore downloads packages; build/test execute analyzers, source generators, and test code. Say which operation you need and what it does before running it, and never claim a result from an unrun check.

Behavior includes outputs, exceptions, side effects, evaluation order, deferred-vs-eager execution, serialization shape, resource lifetimes, cancellation, and timing-sensitive synchronization — not just the happy-path return value.

## Plan by risk

Classify every move and confirm the class before implementing:

- **Mechanical** — a local syntax or representation change, only after proving evaluation order, short-circuiting, exception, and disposal behavior are unchanged. Examples: `if` to switch expression, null-coalescing/pattern rewrites that preserve operand order, `new List<T>()` to `[]`, removing a now-unused private member.
- **Structural** — visibility, public signatures, namespace or project boundaries, serialization/DI/mapping attributes, test seams, or the public/source/binary/wire compatibility surface. Requires separate confirmation; apply the source, binary, and wire compatibility axes from `mag-csharp-review`'s `references/api-compatibility.md` as a lens.
- **Semantic-risk** — algorithm, data structure, eager↔lazy evaluation, equality contract, concurrency/`lock` scope, disposal, async/`ValueTask` shape, or allocation/performance. Requires a characterization test, an invariant proof, a measurement, or an explicit user decision — see `references/semantic-risks.md`.

The C# traps that turn a "mechanical-looking" edit into a semantic-risk change live in `references/semantic-risks.md`: deferred LINQ execution and multiple enumeration, operand evaluation order and `&&`/`||`/`??`/`?:`, `using`/`await using` disposal paths, `Task`↔`ValueTask` return-type changes, `record`/`struct`/`class` equality contracts, closure capture, and restructuring `lock`/`SemaphoreSlim` across `await`.

## Execute safely

1. Present the ordered plan: exact paths, risk class per move, acceptance checks, and non-goals. State explicitly when an axis has no justified change.
2. Implement one bounded, coherent step at a time; do not batch unrelated "obviously safe" edits into one diff.
3. Run the narrowest relevant tests after the execution boundary is trusted and authorized, then broaden to project/analysis checks the repository contract requires. Preserve build configuration (Debug vs Release) and compare against the frozen baseline.
4. On failure, diagnose and revert only your own edits from the saved patch. Do not destroy user work.
5. Performance claims must be measured or argued from generated behavior — a "same result, fewer allocations" claim needs a benchmark or a documented runtime guarantee, not vibes.
6. Request confirmation before any public API, serialization, dependency, TFM, persistence, or concurrency change, and before a semantic-risk move without a proving test.

## Output

Report:

- baseline and final verification (commands run, actual results, configuration);
- changed files and the risk class of each change;
- preserved contracts — public/source/binary/wire surface, evaluation order, serialization, exceptions, disposal, async/ValueTask semantics, and measured performance — each stated as preserved or explicitly changed with authorization;
- rejected candidates and why;
- remaining uncertainty, including any check not run and why.

If the honest outcome is "no justified change", say so with the scope that was examined — a refactor that would change behavior is not a refactor, and declining to make it is a valid result.
