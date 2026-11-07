# API compatibility

Apply this reference when a review touches a public surface, a serialization or wire contract, or a multi-targeted project. It describes how to reason about source, binary, and wire compatibility and how to use PublicAPI/ApiCompat-style evidence — not a list of automatic defects.

## Three compatibility axes

Keep the three axes distinct; a change can break one without the others.

- **Source compatibility** — existing caller code still compiles after the change. Broken by renames, removed members or types, changed parameter names (named arguments), changed types, added abstract members on inheritable types, removed optional/`ref`/`in`/`out` modifiers, and overloads that capture previously-resolving call sites.
- **Binary compatibility** — already-compiled assemblies still load and run without recompilation. Broken by removing or renaming types/members, changing signatures or return types, changing enum underlying types, sealing an unsealed type, removing virtual, adding instance fields to structs without nonpublic fields, or changing the assembly name/public key. It survives many source-level changes (renaming a parameter body, adding members, changing a method body).
- **Behavioral (and wire) compatibility** — observable behavior, and serialized data or protocol shape that persists or crosses processes. Broken by changing a public constant or enum member value, changing property/getter behavior, changing serialization formats or member names that appear in output, changing `GetHashCode` behavior for persisted keys, or firing an event that never fired before. A DTO field rename or a serialized property-name-policy change can break consumers of persisted or cross-service data even when source and binary compatibility are preserved.

For serialization/deserialization and wire contracts, treat the serialized shape (JSON/XML/binary member names, enum values, format) as its own public surface distinct from the CLR surface.

## Version-sensitive checks

- A rule may depend on the C# language version. For example, adding a default instance interface member is generally source-compatible, but is a source-breaking change for `ref struct` implementers (C# 13 and later), which must provide explicit implementations.
- Distinguish compile-time (reference) assemblies from runtime assemblies in multi-targeted packages; a public surface must be present and consistent across every shipped TFM.

## PublicAPI analyzer evidence

The `Microsoft.CodeAnalysis.PublicApiAnalyzers` package tracks the declared public API in `PublicAPI.Shipped.txt` and `PublicAPI.Unshipped.txt`. It flags added public symbols (RS0016) and removed or renamed symbols (RS0017, entries marked `*REMOVED*`), plus invalid or duplicate declarations (RS0024/RS0025). Treat those files and their warnings as repository-level evidence that a surface change is intended and reviewed, not as proof of compatibility. Review the declaration text itself for removals, signature changes, and accidental additions; do not generate or edit baselines as part of a review.

## ApiCompat / package validation evidence

- Package validation (`EnablePackageValidation=true`) runs after `Pack` and uses three validators: the **baseline** validator (against a previously released stable package), the **compatible runtime** validator (runtime assemblies consistent with compile-time assemblies), and the **compatible framework** validator (code compiled against one TFM runs against all others in a multi-targeting package).
- The same machinery is available through the `Microsoft.DotNet.ApiCompat.Tool` global tool and `Microsoft.DotNet.ApiCompat` for assembly-level validation. Check which of these the repository actually uses before citing it; a project without them has no enforced surface contract.

## Generated code and multi-TFM surface

- Review generated public symbols (source generators, build-time code) through their generated output and the declared PublicAPI files; never edit generated files or generated baselines as part of a review.
- For multi-targeting, compare the public surface per TFM: a member present on one target but missing on another is a compatibility hole for consumers of that target, and a `#if`-guarded surface may not match the declared baseline.
- When a change adds or alters a `#if` guard, attribute, or generator input that changes emitted surface, treat the emitted change as part of the reviewed diff even if the generator output is not committed.

## References

- [.NET compatibility overview](https://learn.microsoft.com/en-us/dotnet/core/compatibility/)
- [Library change rules](https://learn.microsoft.com/en-us/dotnet/core/compatibility/library-change-rules)
- [.NET package validation](https://learn.microsoft.com/en-us/dotnet/fundamentals/package-validation/overview)
- [Breaking changes and .NET libraries](https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/breaking-changes)
- [PublicApiAnalyzers (Microsoft.CodeAnalysis.PublicApiAnalyzers)](https://github.com/dotnet/roslyn-analyzers/tree/main/src/PublicApiAnalyzers)
