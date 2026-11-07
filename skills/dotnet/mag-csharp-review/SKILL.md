---
name: mag-csharp-review
description: Perform a read-only, evidence-driven review of C#/.NET code, a diff, commit range, project, or repository, reporting only reachable correctness, nullability, type/equality, resource, security, concurrency, performance, or maintainability issues with verification and location; use for review, not editing; route async-reliability or measured-performance reviews to their specialists when that concern is dominant.
---

# C# Review

## When to Use

Use for a read-only review of C# code, a local diff, commit or PR, a project (`.csproj`/`.sln`), a repository, or a pasted excerpt. Use it to verify whether a proposed review finding is valid, and to review .NET API or compatibility concerns.

A review, diagnosis, or design request is not permission to edit: do not modify code, format files, fix findings, generate API baselines, post comments, approve, merge, or change remote state. Do not turn style preferences or missing-test opinions into findings.

Route to `mag-dotnet-async-reliability` when async/concurrency design or shutdown is the dominant concern, and to `mag-dotnet-performance` when the request is measured performance diagnosis or optimization. These are optional specialists, not prerequisites; treat async or performance here only as review lenses.

## Establish scope and contract

1. Establish the exact target and revision: diff base/head, commit range, branch, files, or pasted code. Do not silently substitute a merge-base or `HEAD`. For pasted code there is no base: review the supplied scope without inventing change attribution. If the prompt references a snippet or diff that is not actually in scope, list it as missing context and review nothing rather than inventing it.
2. Read repository instructions (AGENTS, CONTRIBUTING, Directory.Build.props, `.editorconfig`, `.globalconfig`) and the relevant project files. The repository contract wins over generic API assumptions.
3. Detect the toolchain separately; do not collapse them into "the .NET version":
   - SDK: `global.json`, `dotnet --version`/`--list-sdks` (read-only commands are safe).
   - Language version: `<LangVersion>` (explicit or `latest`/`preview`) versus the TFM-defaulted version.
   - Target framework(s): `<TargetFramework>`/`<TargetFrameworks>` (e.g. `net8.0`, `net9.0`, `netstandard2.0`, `net48`); multi-targeting implies per-TFM surface review.
   - Runtime/deployment: `runtimeconfig.json`, `RuntimeIdentifier`, `SelfContained`, container/AOT/trimming properties when present.
   - Packages: `Directory.Packages.props`, `PackageReference`, `packages.lock.json`, `<RestorePackagesWithLockFile>`.
   - Analyzers/quality gates: `AnalysisLevel`, `EnableNETAnalyzers`, `TreatWarningsAsErrors`, `CodeAnalysisRuleSet`, `.editorconfig` severity.
4. Check version-sensitive claims against the detected version and, when reachable, current official Microsoft/.NET documentation. If a claim cannot be verified, report it as unverified rather than asserting it.

## Read-only discipline

Default to static reading. `dotnet --version`, `--list-sdks`, `--list-runtimes` only report state and are safe. Anything that restores, builds, tests, or otherwise writes (`dotnet restore`, `build`, `test`, `format`) may hit the network, execute the project, or create `obj/`, `bin/`, and lock files — treat it as an action requiring authorization, and say which check was not run. Package installs, `dotnet publicapi`-style baseline creation, and running analyzers are not implicit review authority. A snippet proves only what it contains; list missing context instead of guessing.

## Review lenses

Investigate the risk surface in this order and trace each suspicion through callers, guards, configuration, and consumers. Use [api-compatibility](references/api-compatibility.md) when a public surface, serialization contract, or multi-TFM question is in play.

- **Correctness and nullability:** nullable context per project, flow analysis, `null!`/`!` suppressions that contradict actual state, default value types, string and null comparisons, `Equals`/`==` semantics, operator overloads.
- **Types and equality:** struct vs class and record value semantics, `IEquatable<T>`, `GetHashCode`/`Equals` consistency, `==`/`!=` vs reference equality, init-only/`with`, implicit conversions, enum underlying values, readonly/ref structs.
- **Resources:** `IDisposable`/`IAsyncDisposable` ownership, `using`/`await using`, finalizers, unmanaged handles, stream/file/connection lifetimes, `HttpClient` reuse, async disposal on failure paths.
- **Security:** untrusted input and injection (SQL concatenation, command building), path traversal, secrets in source/config, deserialization settings (`TypeNameHandling`-style and binary formatter hazards), `System.Text.Json` defaults, HTML/URL encoding, weak RNG (`Random` vs `RandomNumberGenerator`) and crypto defaults, sensitive data in logs or exceptions.
- **Concurrency:** shared/static state without synchronization, lock scope and ordering, sync-over-async (`.Result`, `.Wait()`, `.GetAwaiter().GetResult()`) and deadlock/thread-pool starvation, `async void` outside event handlers, races, `volatile`/`Interlocked`/`ConcurrentDictionary` misuse.
- **Performance:** flag only reachable, material costs — hot-path allocations, deferred/multiple LINQ enumeration, string concatenation in loops, boxing, unbounded collections — and only when scale or evidence makes it consequential. Route measured optimization to `mag-dotnet-performance`.
- **Maintainability:** actionable only — a violated repository rule, or a concrete coupling/co-change consequence across named locations. Never report formatting or naming taste as a defect.
- **Design / anti-patterns:** flag a God Object, premature abstraction, pattern overuse, or a DRY violation only with a concrete co-change consequence, and only against the file's own maintainability standard (verification checklists: `skills/development/mag-code-design/references/principles.md`). In existing code, report only when the reviewed change activates or worsens it — follow the attribution rules under Findings.

## Verify each candidate

1. Name the violated contract or invariant and its evidence: a requirement, a documented repository rule, a framework/runtime contract, or established behavior. A reviewer preference is not a contract.
2. Trace a concrete trigger and inputs to the consequence through actual code, guards, configuration, state, and consumers. Confirm reachability.
3. Seek counter-evidence: tests on the path, validation, caller guarantees, analyzer coverage, and actual framework or serializer behavior for the detected version. A generic default is not proof of a guarantee.
4. Run only safe, authorized checks; a test proves only the scenario it exercises.
5. Classify each candidate as **confirmed**, **refuted**, **out of scope**, or **needs evidence**. Missing evidence is not a refutation: if a material risk remains plausible, name the specific missing fact and the smallest way to check it.

## Findings

A reportable finding needs: the smallest causal file/line or function/hunk anchor; the violated contract; a reachable trigger; the behavior and impact; and why any existing guard is insufficient. Classify as **Blocker** or **Issue**. Omit nits.

Distinguish attribution: for a diff/commit review, a problem is a change regression when the change introduces, exposes, widens, or worsens it; a pre-existing defect is reportable only when the change makes it newly reachable, and then call out both the activation and the underlying behavior. For a repository/file/paste snapshot review, a present reachable defect is reportable without change attribution — say when its history is unknown. For absence findings, cite the project file or contract and the concrete consequence rather than inventing a line number.

## Output

~~~markdown
# C# review — <scope>
Revision: <branch/commit/status>
Detected: SDK, LangVersion, TFM(s), runtime, key packages/analyzers — each as a separate item; state `not detected` when no project file is in scope instead of assuming a default
Verdict: SOUND | ISSUES | BLOCKERS

## Blockers
- path:line — problem; trigger and impact; fix direction.

## Issues
- path:line — problem; trigger and impact; fix direction.

## Done right
- concrete verified strengths, or "nothing notable in the reviewed scope".

## Not verified
- missing callers, unavailable build, unverified runtime assumptions, checks not run.
~~~

Report only verified, in-scope findings. If no confirmed findings remain, say so explicitly with the reviewed scope and its limits — a clean review never proves the absence of all defects. Never prescribe a fix unless asked; when asked, check it addresses the actual failure path and preserves relevant contracts.
