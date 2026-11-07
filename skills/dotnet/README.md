# C# and .NET skills

Five independent skills for C# implementation, read-only review, .NET project compatibility, async reliability, and measured performance.

## Choose the primary skill

Select by the requested outcome, not by the presence of a C# file. Use one primary skill; add a specialist lens only when it helps.

| Skill | Primary outcome | Boundary |
|---|---|---|
| [mag-csharp-implementation](mag-csharp-implementation/SKILL.md) | Implement an authorized feature or bug fix | Not review-only, project-only, lifecycle-first, or performance-first work |
| [mag-csharp-review](mag-csharp-review/SKILL.md) | Report verified issues in existing code or a change | Read-only; no automatic fixes |
| [mag-dotnet-project](mag-dotnet-project/SKILL.md) | Create/extend project structure, resolve compatibility, or diagnose a build | Not application behavior, a broad upgrade, registry publication, or deployment |
| [mag-dotnet-async-reliability](mag-dotnet-async-reliability/SKILL.md) | Design, review, or fix task ownership, cancellation, bounded concurrency, and shutdown | Preserve the requested mode; diagnosis/review does not authorize edits |
| [mag-dotnet-performance](mag-dotnet-performance/SKILL.md) | Diagnose a performance problem and verify an authorized optimization | No speculative micro-optimization or unsupported speedup claims |

For mixed requests, preserve explicit read-only, output, and file boundaries. An ordinary feature containing an async method remains implementation work; an unreliable worker lifecycle is async work. A broad code review remains review work; a latency investigation is performance work. Questions that only ask for an explanation do not authorize implementation.

## Shared contract

- Detect the repository's SDK, language version, target frameworks, runtime, package graph, analyzers, and CI rather than assuming a current release.
- Preserve source, binary, wire, resource-lifetime, and behavioral contracts within the authorized scope.
- Load a skill's references only for the problem at hand. No skill requires another skill, tracker, harness, or storage backend.
- Treat restore, build, tests, profiling, and publishing as operations with effects. Respect repository trust, user authority, and dependency-installation boundaries.
- Report commands actually run, observed results, missing evidence, and remaining risks.

These are Phase 1 drafts. Behavioral evaluations and routing comparisons are separate follow-up work; structural validity alone does not demonstrate reliability. ASP.NET Core, EF Core, Aspire, testing, refactoring, and explanation specialists are not part of this phase.
