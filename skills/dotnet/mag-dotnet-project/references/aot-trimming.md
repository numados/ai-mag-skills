# AOT and trimming

Read when enabling `PublishTrimmed` or `PublishAot`, or triaging IL2xxx / IL3xxx warnings. Trimming and Native AOT are related but distinct; conflating them leads to the wrong fix.

## Trimming vs Native AOT

- **Trimming** (`PublishTrimmed=true`) removes unused code from self-contained deployments to cut size. The trimmer (ILLink) analyzes the whole application at build time. The app still runs with a JIT, so reflection works at runtime for anything the trimmer proved reachable.
- **Native AOT** (`PublishAot=true`) compiles IL to native code up front and produces a self-contained binary with no JIT. Runtime code generation (`System.Reflection.Emit`, `MakeGenericType` on unknown types, loading new assemblies) has no JIT to fall back to, so it fails at runtime.

Native AOT implies trimming-style analysis plus its own stricter checks. An app that trims cleanly is not automatically AOT-compatible.

## Warning ranges and root cause

- **IL2xxx** — trimmer (ILLink) analysis. Root causes: reflection the analyzer cannot see through, dynamic assembly loading, or `RequiresUnreferencedCode`. Examples: IL2026 (a member marked `RequiresUnreferencedCode`), IL2070 (a `DynamicallyAccessedMembers` requirement not satisfied).
- **IL3xxx** — Native AOT analysis. Root causes: APIs marked `RequiresDynamicCode` or patterns that need runtime code generation. Example: IL3050 (a member marked `RequiresDynamicCode`).

Read a warning as three questions: which member is reached, which annotation it violates, and whether that code path is actually exercised. Trim warnings are usually fixable with annotations or removing reflection; AOT warnings usually require removing the dynamic-code pattern.

## Fix order (never start at suppression)

1. Remove the reflection or dynamic-code pattern (source generation, compile-time generics, direct calls).
2. If types are known at compile time, annotate with `DynamicallyAccessedMembers` so the analyzer can preserve them.
3. If truly dynamic, mark the boundary `RequiresUnreferencedCode` (trim) or `RequiresDynamicCode` (AOT) so callers inherit the warning.
4. Only as a last resort, suppress a specific code at the narrowest scope with `UnconditionalSuppressMessage` (category `Trimming` or `Aot`) and a `Justification` that names the preserved or guarded path.

Do not recommend global `NoWarn`, `SuppressTrimAnalysisWarnings`, or any "suppress all" setting as a fix; that hides future regressions. A suppressed warning still requires testing the trimmed/AOT build because behavior can change at runtime.

## Source generation and reflection limits

- Reflection-based serializers (for example legacy `Newtonsoft.Json` default usage, `BinaryFormatter`) are trim/AOT-incompatible; use source-generated serialization such as `System.Text.Json` source generation or the configuration-binding source generator.
- `System.Reflection.Emit`, `Assembly.LoadFrom`-style plugin systems, and runtime `MakeGenericType` are incompatible with AOT and hostile to trimming because the compiler cannot see that code.
- `DynamicallyAccessedMembers`, `DynamicDependency`, and `RequiresUnreferencedCode` describe reachability to the analyzer; they are evidence, not a substitute for testing the published artifact.

## Verification

`dotnet publish` runs the analysis (and `dotnet build` does too when trimming is set in the project file). A clean build is necessary but not sufficient: run the published, trimmed or AOT binary against realistic inputs and confirm no reflection or dynamic-code path throws. Report whether that runtime verification was performed.

## Official references

- Trimming options: https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/trimming-options
- Fixing trim warnings: https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/fixing-warnings
- Known trimming incompatibilities: https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/incompatibilities
- Native AOT overview: https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/
- Introduction to AOT warnings: https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/fixing-warnings
