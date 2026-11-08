# C# and .NET skills

Ten independent skills for C# implementation, review, project compatibility, async reliability, measured performance, ASP.NET Core, EF Core, testing quality, refactoring, and explanation.

## Choose the primary skill

Select by the requested outcome, not by the presence of a C# file. Use one primary skill; add a specialist lens only when it helps.

| Skill | Primary outcome | Boundary |
|---|---|---|
| [mag-csharp-implementation](mag-csharp-implementation/SKILL.md) | Implement an authorized feature or bug fix | Not review-only, project-only, lifecycle-first, or performance-first work |
| [mag-csharp-review](mag-csharp-review/SKILL.md) | Report verified issues in existing code or a change | Read-only; no automatic fixes |
| [mag-dotnet-project](mag-dotnet-project/SKILL.md) | Create/extend project structure, resolve compatibility, or diagnose a build | Not application behavior, a broad upgrade, registry publication, or deployment |
| [mag-dotnet-async-reliability](mag-dotnet-async-reliability/SKILL.md) | Design, review, or fix task ownership, cancellation, bounded concurrency, and shutdown | Preserve the requested mode; diagnosis/review does not authorize edits |
| [mag-dotnet-performance](mag-dotnet-performance/SKILL.md) | Diagnose a performance problem and verify an authorized optimization | No speculative micro-optimization or unsupported speedup claims |
| [mag-aspnet-core](mag-aspnet-core/SKILL.md) | Design, review, or fix ASP.NET Core request, security, resilience, and observability behavior | Not generic C# or EF Core data-access work |
| [mag-ef-core](mag-ef-core/SKILL.md) | Design, review, or fix EF Core query, persistence, transaction, and provider behavior | Not generic SQL or ASP.NET request-pipeline work |
| [mag-dotnet-testing-quality](mag-dotnet-testing-quality/SKILL.md) | Design realistic .NET test seams, fixtures, runners, and quality gates | Not a generic test-first workflow or a mandated test framework |
| [mag-csharp-refactor](mag-csharp-refactor/SKILL.md) | Refactor C# while preserving observable and compatibility contracts | Not behavior-changing implementation or a review-only report |
| [mag-csharp-explain](mag-csharp-explain/SKILL.md) | Explain concrete C#/.NET code and runtime behavior | Not implementation, refactoring, or review |

For mixed requests, preserve explicit read-only, output, and file boundaries. An ordinary feature containing an async method remains implementation work; an unreliable worker lifecycle is async work. A broad code review remains review work; a latency investigation is performance work. Questions that only ask for an explanation do not authorize implementation.

## Shared contract

- Establish the repository and version facts relevant to the requested outcome. These can include the SDK, language version, target frameworks, runtime, packages, analyzers, and CI. Do not assume the newest release or require an unrelated environment inventory.
- Preserve source, binary, wire, resource-lifetime, and behavioral contracts within the authorized scope.
- Load a skill's references only for the problem at hand. No skill requires another skill, tracker, harness, or storage backend.
- Treat restore, build, tests, profiling, and publishing as operations with effects. Respect repository trust, user authority, and dependency-installation boundaries.
- Report commands actually run, observed results, missing evidence, and remaining risks.

Behavioral evaluations and routing comparisons are separate evidence gates; structural validity alone does not demonstrate reliability. ASP.NET Core, EF Core, testing, refactoring, and explanation are focused specialists, not replacements for the generic task, TDD, or code-review workflows.
