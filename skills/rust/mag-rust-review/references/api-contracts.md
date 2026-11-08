<!-- Generated from skills/rust/mag-rust-implementation/references/api-contracts.md. Do not edit this copy; run python3 scripts/sync-skill-resources.py in the catalog repository. No source checkout is needed at runtime. -->

# Rust API and ownership contracts

Load this reference when designing or reviewing public types, conversions, traits, resource lifetimes, or ownership-heavy data structures. These are decision rules, not a requirement to redesign every existing API.

## Encode the contract in types

- Use `Option<T>` for an absent value when no failure detail is needed.
- Use `Result<T, E>` when the caller needs to distinguish or report failure.
- Replace a sentinel with `Option` or a domain enum when the sentinel is not a valid value.
- Replace multiple flags with an enum or newtypes when the states have domain meaning. Keep a `bool` when the domain is permanently binary.
- Use private fields and validated constructors when an invariant must hold after construction.
- Use a builder only when construction has enough optional or ordered inputs to justify its extra state. Validate required invariants at `build()`.

Do not encode a wire-format assumption as a type invariant without validating the input at the boundary.

## Conversions

Use `From`/`Into` for infallible, lossless conversions. Use `TryFrom`/`TryInto` when validation can fail or information can be lost. Treat unchecked casts such as `as` as a deliberate numeric policy: check range, signedness, truncation, and overflow behavior first. Preserve the original error as `source()` when wrapping a parse or I/O failure.

Do not add a conversion only to make a call site compile. State whether it is lossless, fallible, lossy, or a representation change.

## Generics and dynamic dispatch

Prefer generics or `impl Trait` when the caller's concrete type, static bounds, or monomorphization is part of the contract. Use `dyn Trait` when heterogeneous values, runtime-selected implementations, or a measured code-size or compile-time trade-off requires it. Do not claim that either dispatch mode is faster without evidence.

Before exposing `dyn Trait`, check object safety: generic methods, methods returning `Self`, and unsuitable receivers can prevent the intended trait-object use. Before changing a public trait, check implementor compatibility, required methods, default methods, blanket implementations, and downstream semver impact.

## Errors, panics, and release

Choose structured error types for reusable library contracts. An application boundary may erase or render errors after the useful context has been preserved. Document surprising `# Panics`, `# Errors`, and `# Safety` conditions. Do not use `catch_unwind` as general error handling.

`Drop` cannot report failure. If release, flush, commit, or close can fail, provide an explicit fallible method and define what `Drop` does when the caller does not use it. Test both explicit release and drop fallback. Do not claim that a dropped value completed asynchronous cleanup.

## Ownership before borrowing

Start with an owned representation. Borrow only when the lifetime, reuse, or allocation contract justifies it. Consider `Cow`, `Arc`, or a stable owned buffer when they express the actual sharing or copy trade-off. Treat `Rc<RefCell<_>>` and `Arc<Mutex<_>>` as runtime checking or synchronization designs, not generic escapes from ownership questions.

A borrowed parser result cannot outlive the input it references. If a service stores the result while reusing or dropping the input buffer, choose ownership or stable shared storage instead of adding a lifetime that cannot be satisfied.

## Laws and compatibility

Check that `Eq` and `Hash` agree, and that `Ord` agrees with `PartialOrd`. Treat `Copy` as a promise that bitwise duplication is valid and cheap. A public parameter, return type, trait method, derive, error representation, or feature-gated public item is a compatibility surface. For a library, verify the declared MSRV and dependency lower bounds, not only the current lockfile.

Keep this reference conditional. A zero-copy parser, a boolean, a builder, a trait object, or interior mutability can be correct when its contract and evidence support it.
