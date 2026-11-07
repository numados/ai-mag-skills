# Version and project contracts

Read when a project decision turns on SDK, language, target framework, runtime, package, or analyzer versioning. The point of this reference is that these facts are independent and must be detected separately.

## The six facts are independent

| Fact | Where it lives | Detect with |
|---|---|---|
| SDK (toolchain) | `global.json` `sdk.version`, `rollForward` | `dotnet --version`, `dotnet --list-sdks` |
| Compiler / LangVersion | `<LangVersion>`, or the TFM default | project file; `#error version` (CS8304) |
| Target framework (TFM) | `<TargetFramework>` / `<TargetFrameworks>` | project file |
| Runtime / deployment model | `SelfContained`, `RuntimeIdentifier`, `PublishSingleFile`, `PublishTrimmed`, `PublishAot` | project file + publish profile |
| Package versions | `PackageReference`, `PackageVersion`, lock file | project, `Directory.Packages.props`, `packages.lock.json` |
| Analyzer level | `AnalysisLevel`, `AnalysisMode`, `EnableNETAnalyzers`, analyzer packages | project, `Directory.Build.props`, `.editorconfig` |

A TFM selects the default C# language version and the reference-assembly API surface, but it does not pin the SDK, the runtime on the target machine, or package versions. Keep them separate in any report.

## SDK vs global.json

`global.json` selects the SDK (the CLI/toolchain) and is independent of the TFM. `rollForward` governs how far the resolver may move from the requested `version`: `patch`, `feature`, `minor`, `major`, `latestFeature`, `latestMinor`, `latestMajor`, or `disable`. `allowPrerelease` controls preview SDKs.

Resolve SDK availability from `dotnet --list-sdks`; do not assume an SDK is installed just because a TFM exists.

## LangVersion

`<LangVersion>` pins the language version. The default follows the TFM (for example, net8.0 defaults to C# 12 and net9.0 to C# 13); pin it only to diverge from that default. `latest` follows whatever compiler is installed, so builds vary by machine; prefer an explicit value or the TFM default.

Use `#error version` in a scratch file to make the compiler report the active language version (CS8304).

## TFM and multi-targeting

Single: `<TargetFramework>net8.0</TargetFramework>`. Multi: `<TargetFrameworks>net8.0;net9.0</TargetFrameworks>`. OS-specific TFMs such as `net8.0-windows` add platform APIs and usually need a `TargetPlatformMinVersion`. `netstandard2.x` is a compatibility contract, not a runtime.

Multi-targeting multiplies restore, build, test, and analyzer passes. Prefer it only when there is a real consumer on each TFM. When behavior differs per TFM, guard with preprocessor symbols such as `#if NET8_0_OR_GREATER` rather than inventing new ones.

## Runtime / deployment model

Framework-dependent (the default) requires the runtime on the target machine. Self-contained (`SelfContained=true`) bundles the runtime and implies a runtime identifier (RID). `PublishSingleFile`, `PublishReadyToRun`, `PublishTrimmed`, and `PublishAot` are publish-time deployment shapes layered on top, each with its own constraints (see `aot-trimming.md`).

## Nullable and ImplicitUsings

`<Nullable>enable</Nullable>` enables the nullable annotation and warning context project-wide; `#nullable enable` scopes it to a file. This is an analyzer/compiler contract, not a runtime fact, so respect the repo's existing setting and `.editorconfig` severity rather than switching it.

`<ImplicitUsings>enable</ImplicitUsings>` injects common global usings and varies with the SDK and TFM; do not assume which namespaces are imported when the project disables or customizes it.

## Package versions and central package management

Direct versions live on `PackageReference Version`. Central Package Management uses `Directory.Packages.props` with `ManagePackageVersionsCentrally=true`; projects then reference packages without a version and the version is resolved from a `<PackageVersion>` entry. `CentralPackageTransitivePinningEnabled` pins transitive versions. Lock files (`RestorePackagesWithLockFile`, `packages.lock.json`) and `NuGet.config` (sources, credentials, `globalPackagesFolder`) shape restore.

A package's supported TFMs and its resolved version come from NuGet metadata and the restore/lock graph, not from a remembered table.

## Analyzers

`EnableNETAnalyzers` and `AnalysisLevel` select the built-in analyzer set and level; `AnalysisMode` (`Default`, `Recommended`, `All`, or `Minimum`) widens or narrows it. A separate analyzer package (for example `Microsoft.CodeAnalysis.NetAnalyzers`) can pin an analyzer version independently of the SDK. `.editorconfig` sets severity and style per rule.

## Inheritance

`Directory.Build.props` and `Directory.Build.targets` apply to every project under their directory (props import early, targets import late); when several exist, the file nearest the project wins. `Directory.Packages.props` is NuGet's version-inheritance counterpart. Read these before editing a single project so edits do not fight inherited values.

## Official references

- Configure language version: https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/configure-language-version
- global.json: https://learn.microsoft.com/en-us/dotnet/core/tools/global-json
- dotnet sln / .slnx: https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-sln
- MSBuild properties for Microsoft.NET.Sdk: https://learn.microsoft.com/en-us/dotnet/core/project-sdk/msbuild-props
- Central Package Management: https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management
- Target frameworks: https://learn.microsoft.com/en-us/dotnet/standard/frameworks
