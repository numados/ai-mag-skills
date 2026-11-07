# Test platform detection: VSTest vs Microsoft.Testing.Platform

Load this reference when a prompt names a test runner, a `dotnet test` flag, a coverage collector, or a "tests not discovered / `--logger` ignored" problem. The central rule: **detect the platform before touching a run command**, because VSTest and Microsoft.Testing.Platform (MTP) are different runners with different flag handling, and mixing them silently drops behavior.

## Two runners, one command name

- **VSTest** is the long-standing runner; the default `dotnet test` mode before the .NET 10 SDK invokes the VSTest MSBuild target → `vstest.console`, and translates `dotnet test` options to vstest.console equivalents.
- **Microsoft.Testing.Platform (MTP)** is the newer runner. xUnit, NUnit, MSTest, and TUnit each have MTP support, but TUnit is built **on MTP, not VSTest**.

`dotnet test` has two modes:

- **VSTest mode** (default before the .NET 10 SDK) — VSTest semantics and flags apply.
- **MTP mode** (introduced with the .NET 10 SDK) — targets MTP-only test apps; selected via `global.json` `"runner": "Microsoft.Testing.Platform"` or the `DOTNET_TEST_RUNNER` environment variable (from .NET 11 Preview 6). Requires MTP 1.7.0+.

## MTP v1 legacy bridge (do not use on MTP v2)

Running MTP under VSTest mode was an MTP v1 bridge: it needed the `Microsoft.Testing.Platform.MSBuild` package and `TestingPlatformDotnetTestSupport=true` (default **false**). With MTP v2 on the .NET 10 SDK this bridge is unsupported — a project must select MTP mode (`global.json` `runner`) instead of enabling the legacy flag. When you see `TestingPlatformDotnetTestSupport` in an existing project, treat it as migration debt and say so. In historical v1-bridge output VSTest-specific options (e.g. `--logger`) were **silently ignored**, and MTP-specific args (e.g. `--report-trx`) had to follow an extra `--`.

## TUnit specifics

- TUnit is on MTP, discovers tests at compile time via a source generator (no reflection scan at startup), runs tests in parallel by default, and supports Native AOT.
- Run commands differ from the `dotnet test` habit: `dotnet run -c Release` (preferred), `dotnet test -c Release -- --report-trx --coverage` (flags **after** `--`), or `dotnet exec YourTestProject.dll` after build.
- Two hard incompatibilities: do **not** reference `Microsoft.NET.Test.Sdk` (breaks discovery), and do **not** use `coverlet.collector`/`coverlet.msbuild` (VSTest-based, incompatible). Detect these in the project file before advising a run command.
- `--report-trx` is **not** built into MTP: the test app must register the `Microsoft.Testing.Extensions.TrxReport` extension, otherwise the flag is unrecognized.

## MSTest/NUnit bridge and mixed solutions

- MSTest and NUnit reach MTP in two ways: MSTest 4.4+ has native MTP integration (no bridge), while earlier MSTest and current NUnit use the `Microsoft.Testing.Extensions.VSTestBridge` (`EnableMSTestRunner` / `EnableNUnitRunner`); a bridged project can support both VSTest and MTP. Detect the package version before assuming which path applies.
- Mixing VSTest and MTP projects in **one solution is unsupported/risky** (some projects VSTest, others MTP). When a solution spans both, call out the risk and keep run commands per-project, not per-solution.

## Coverage collectors follow the platform

- VSTest-based projects typically use coverlet collectors; MTP projects cannot use the VSTest collector/MSBuild packages, but coverage is still available: use `coverlet.MTP` (`dotnet test --coverlet`, writes `coverage.json`) or the runner's own mechanism (e.g. the `--coverage` flag and its registered extension). Match the collector to the detected platform rather than assuming one everywhere.
- Regardless of platform, coverage is an explored-paths signal, not correctness — a covered line with no assertion proves nothing.

## Detection workflow

1. Read the test project(s): the SDK, TFM, test packages (`Microsoft.NET.Test.Sdk`? `xunit`/`NUnit`/`MSTest`/`TUnit`? bridge packages?), and any `global.json` `runner` setting.
2. Identify the platform per project — do not assume the solution is homogeneous.
3. Map the requested command/flags to that platform's supported set; when a requested flag is VSTest-only but the platform is MTP, say the flag is ignored and give the MTP equivalent (or say it needs an extension).
4. Report version-sensitive facts as detected (package versions come from `Directory.Packages.props`/`PackageReference`, not from memory) and never claim a run succeeded from a command you did not execute.

## References

- [Unit testing with `dotnet test` (VSTest vs MTP modes, `runner`, `--report-trx`, bridges)](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test)
- [TUnit (MTP-based, source-generated discovery)](https://thomhurst.github.io/TUnit/)
- [TUnit installation (no `Microsoft.NET.Test.Sdk`, no coverlet)](https://thomhurst.github.io/TUnit/docs/getting-started/installation)
- [TUnit running your tests (run commands, flags after `--`)](https://thomhurst.github.io/TUnit/docs/getting-started/running-your-tests)
