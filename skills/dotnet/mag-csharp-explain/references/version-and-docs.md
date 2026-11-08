<!-- Generated from skills/dotnet/mag-csharp-implementation/references/version-and-docs.md. Do not edit this copy; run python3 scripts/sync-skill-resources.py in the catalog repository. No source checkout is needed at runtime. -->

# Version detection and documentation routing

Load this reference only when the code under discussion uses an unfamiliar or version-sensitive API, syntax, compiler option, or analyzer, or when the effective versions are unclear.

## Detecting versions separately

Six independent facts describe a repository's .NET contract. Record each from repository files, not from memory:

| Fact | Primary source | Note |
|---|---|---|
| SDK | `global.json` `sdk.version` | Governs tooling/MSBuild; does not determine the target framework |
| Compiler / language version | `<LangVersion>` in `.csproj` or `Directory.Build.*` | Default follows the target framework; `latest` is discouraged for reproducible builds |
| Target framework(s) | `<TargetFramework>` / `<TargetFrameworks>` | e.g. `net8.0`, `net9.0`, `netstandard2.0`, `net48` |
| Runtime | executable's TFM / `runtimeconfig.json` | A library targets a TFM, not a specific runtime |
| Packages | `Directory.Packages.props` central versions or `PackageReference`; resolved versions from restore/assets or lock files | Central package management versus direct references |
| Analyzers and style | `.editorconfig`, `AnalysisLevel`, analyzer packages | Determines which diagnostics are warnings versus errors on your code |

Check order: repository source and generated types first; then resolved package metadata; then current official documentation for the exact effective versions.

## When to consult official documentation

Before using an unfamiliar or version-sensitive construct, confirm its syntax, signature, availability, nullability, and runtime behavior for the effective TFM and language version. During authorized implementation, build the smallest affected target soon after introducing the construct and treat compiler/analyzer diagnostics as evidence. A read-only explanation or review does not authorize restore, build, or test execution.

## Focused official references

- Configure language version — https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/configure-language-version
- Target frameworks in SDK-style projects — https://learn.microsoft.com/en-us/dotnet/standard/frameworks
- global.json overview — https://learn.microsoft.com/en-us/dotnet/core/tools/global-json
- Nullable reference types — https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references
- Value types — https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types
- Records — https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/record
- Equality operators — https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/equality-operators
- Exception-handling statements — https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/exception-handling-statements
- Implement a Dispose method — https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose
- Implement a DisposeAsync method — https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-disposeasync
- Asynchronous programming — https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/

## When documentation is unreachable

Report the inaccessible verification instead of asserting the fact. Reuse a verified repository precedent when one exists; otherwise state the uncertainty explicitly.
