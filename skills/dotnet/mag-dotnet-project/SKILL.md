---
name: mag-dotnet-project
description: Create, extend, or diagnose .NET solutions and projects (.sln/.slnx/.csproj) by detecting the SDK, compiler/LangVersion, target framework, runtime model, package, and analyzer versions as separate facts, honoring global.json, Directory.Build.props/targets, central package management, NuGet config, nullable, and multi-targeting, and gating AOT/trimming, local container publishing, and binlog-based build diagnosis. Use for project structure, compatibility or package-surface checks, and build-failure diagnosis; use the C# implementation or review skills instead when writing code logic or doing a read-only code audit is the primary request.
---

# .NET Project

## When to Use

Use when creating a .NET solution or project, adding a project/target/test project, deciding where code or tests belong, checking a package or target-framework compatibility question, choosing SDK/global.json/language settings, or diagnosing a build failure.

Route instead when the primary request is writing or changing C# logic (implementation), auditing code for correctness (review), async/concurrency design, measured performance, or EF Core / ASP.NET Core / Aspire work. This skill is self-contained: it inspects the project contract itself rather than requiring another skill.

Scope governs mode. A review, diagnosis, or design question is read-only: report and recommend, do not edit. Only create or edit project files when the user authorized that structural change.

## Establish the project contract

1. Read repository guidance (CONTRIBUTING, AGENTS, .editorconfig, CI) and locate the nearest `.sln`/`.slnx`, `.csproj`/`.fsproj`, `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props`, and `NuGet.config`.
2. Record the target type: application, library, test project, tool, source generator, or multi-targeted library. Note the SDK attribute (`Microsoft.NET.Sdk`, `.Sdk.Web`, `.Sdk.Worker`, `.Sdk.Razor`, ...).
3. Record the declared contract before assuming anything: target framework(s), LangVersion, nullable, implicit usings, analyzers, package versions, and any inherited settings from `Directory.Build.*` files.
4. Inspect analogous projects in the repo before choosing a location or convention. Preserve existing structure; do not introduce a solution folder, new project, shared project, or multi-targeting only because it is fashionable.

## Separate the version facts

Detect and report these independently; none implies the others:

- **SDK version** — `dotnet --version`, `dotnet --list-sdks`; also `global.json` `sdk.version`/`rollForward`. The SDK is the toolchain, not the target.
- **Compiler / LangVersion** — the `<LangVersion>` property or the TFM's default language version. `latest` varies by machine and is unreliable.
- **Target framework (TFM)** — `<TargetFramework>` vs `<TargetFrameworks>`; `netstandard2.x`, `net8.0`, `net9.0`, OS-specific variants. A TFM selects the default language version and the reference-assembly API surface.
- **Runtime model** — framework-dependent vs self-contained (`SelfContained`), `RuntimeIdentifier(s)`, and single-file/ReadyToRun/AOT/trimming toggles. This is deployment shape, not the TFM.
- **Package versions** — `PackageReference Version`, central `PackageVersion` entries, transitive pinning, and lock files. `NuGet.config` decides sources and credentials.
- **Analyzer version/level** — `AnalysisLevel`, `AnalysisMode`, `EnableNETAnalyzers`, and analyzer `PackageReference`s; `.editorconfig` sets severity and style.

Read `references/version-contracts.md` when any of these is version-sensitive, or when global.json, `Directory.Build.*`, central package management, `NuGet.config`, nullable, or multi-targeting details matter.

## Structure decisions

- A library keeps public API in the project's root namespace and concept folders; an executable stays a thin argument/IO/error boundary. Unit tests live in a separate test project that references the library, or beside private logic when the repo already does that.
- Prefer a solution to group related projects; add projects with `dotnet sln <file> add`. Choose `.sln` vs `.slnx` from the installed SDK (below).
- Multi-target only when there is a real consumer on each TFM; otherwise a single `TargetFramework` is simpler and cheaper to verify.
- Keep dependency direction acyclic and public exports deliberate.

### .sln vs .slnx

Choose the solution format from the installed SDK, not from habit:

- `.sln` is the long-standing format and is the `dotnet new sln` default through .NET 9; `.slnx` is the newer XML format. `dotnet new sln` output and `dotnet sln migrate` availability depend on the SDK version, so check `dotnet --version`/`--list-sdks` first.
- Only emit or rely on `.slnx` when the selected SDK (and any IDE/toolchain the repo uses) is known to support it. Do not assume `dotnet new sln` produces `.slnx`, and do not migrate an existing `.sln` to `.slnx` without authorization.
- Report what the toolchain supports rather than asserting a default.

## Package and project surface checks

- Verify a package's supported TFMs and versions against the project's TFM and the repo's resolved restore graph before adding or bumping it. Prefer the lock file or the repository's own restore output over an assumption.
- Under central package management, add or change a version in `Directory.Packages.props`, not inline on a `PackageReference`.
- Keep API compatibility detail (ApiCompat/PublicAPI baselines, source/binary/wire compatibility) with the review skill; here check only that the project and package surface is coherent.

## AOT and trimming

Treat trimming (ILLink, IL2xxx) and Native AOT (IL3xxx) as distinct. `PublishTrimmed` is size reduction for self-contained apps; `PublishAot` compiles IL to native code and forbids JIT and reflection emit. Both produce static-analysis warnings that must be root-caused, not mass-suppressed. See `references/aot-trimming.md`.

## Container publishing

Keep image creation local and reversible. `dotnet publish /t:PublishContainer` builds without Docker and pushes to the local container runtime by default; prefer an explicit local archive path (tarball) for a reversible artifact, and never add a registry push or deployment step unless the user asked for it. See `references/publishing-containers.md`.

## Build diagnosis with a binlog

1. Reproduce with `dotnet build`/`msbuild -bl` (or `-bl:<name>.binlog`) to capture a structured binary log; add `-v:diag` only when text-level detail is needed.
2. Open the binlog locally (MSBuild Structured Log Viewer or the `msbuild` structured-log tooling); inspect the failing target/task, properties, items, and imported files.
3. A binlog records full command lines, environment, and imported file contents, so it can contain secrets (tokens, passwords, keys). Keep it local, redact before sharing, and never auto-upload it to a remote service.
4. Report the failing target/task and the smallest repro; do not claim a fix until a build that failed now passes.

## Do not

- Install SDKs, workloads, or global/local tools; commit, stage, switch branches, or delete files; run product builds beyond what diagnosis requires; publish, push, or deploy.
- Set `LangVersion` to `latest`; mass-suppress trim/AOT warnings; enable trimming, AOT, or containers merely to modernize.
- Add EF Core, ASP.NET Core, Aspire, or upgrade-specialist guidance here.

## Decision output

Return:

1. Detected contract: SDK, LangVersion, TFM(s), runtime model, package and analyzer facts, and inherited settings.
2. Recommended structure or fix, and the repository precedent that supports it.
3. Compatibility consequences (packages, TFMs, analyzers, nullability, publishing).
4. Exact commands to verify, and actual results when run.
5. Unknowns requiring source, toolchain, or documentation lookup.

State an unverified version claim as unverified instead of asserting it.
