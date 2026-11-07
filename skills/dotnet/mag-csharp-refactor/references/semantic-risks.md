# Semantic-risk traps in C# refactoring

Load this reference when a candidate refactor touches deferred execution, evaluation order, disposal, async/ValueTask shape, equality, closure capture, or locking. Each trap is a stable C# semantic (not version-gated) that a behavior-preserving refactor must re-prove before the edit is classified "mechanical".

## Deferred execution and multiple enumeration

- A LINQ query is a *description*, not a result: it runs on each enumeration and reads captured variables at enumeration time, not at definition time. Re-enumerating a query against a changing source can yield different elements or re-run side effects.
- Materializing with `ToList`/`ToArray` changes *when* work runs and *how many times*. Converting an eager collection to a lazy query, or the reverse, is therefore a semantic-risk change, not a syntax change.
- Extracting a query into a method or field can change its capture scope and enumeration count. A refactor that enumerates a sequence more than once (or zero times) after the change is not behavior-preserving.

## Evaluation order and short-circuiting

- C# evaluates operands left-to-right. `&&`, `||`, and `??` skip the right operand when the left one decides the result; `?:` evaluates only the selected branch; `??=` assigns only when the left side is null.
- Reordering operands, extracting a subexpression into a local that always runs, or inverting a boolean expression can change which side effects and exceptions are observed and in what order. Preserve operand order and short-circuit paths exactly, or prove the skipped side is pure and non-throwing.

## Disposal paths

- `using` and `await using` guarantee disposal on exception and early-return paths. Converting a `using` block to a manual `Dispose()`/`DisposeAsync()` call, moving a resource across a method boundary, or widening/lengthening a resource's lifetime can leak or double-dispose.
- `IDisposable` and `IAsyncDisposable` are different contracts: `using` normally requires `IDisposable` and `await using` `IAsyncDisposable`, but C# also accepts a pattern-based shape — a public `Dispose()`/`DisposeAsync()` method without the interface (common for `ref struct` types). Converting one to the other without the interface or the matching pattern does not compile, and adding the interface changes the type's contract. Do not "upgrade" `using` to `await using` unless the type actually supports async disposal and the call site is asynchronous.
- Keep ownership visible: note who creates a resource and who releases it. A refactor that silently transfers or duplicates ownership is a resource-lifetime change.

## Async and ValueTask shape

- `Task` can be awaited any number of times; `ValueTask` must be consumed exactly once. Changing a return type from `Task`/`Task<T>` to `ValueTask`/`ValueTask<T>` (or the reverse) changes the consumer contract and can introduce double-consumption faults if the caller stored or re-awaited it.
- `async` vs "return the task" changes exception timing: in an `async` method every exception — including one thrown before the first `await` — is captured in the returned `Task`; a non-async task-returning method can throw synchronously before it returns anything. Converting between the two changes whether the caller observes a fault by inspecting the task or via an immediate throw, so a surrounding `try/catch` can start or stop catching it. `async void`, `ConfigureAwait`, and continuation context shift where a fault surfaces as well.
- Moving code across an `await`, or moving a `lock`/`SemaphoreSlim` hold across an `await`, can change continuation context, hold duration, and deadlock exposure.

## Equality contracts

- `record` and `record struct` get compiler-generated value equality (`Equals`, `GetHashCode`, `==`); `class` gets reference equality by default; `struct` gets field-wise `Equals` unless overridden. Changing between these kinds changes the equality contract for any code that compares, hashes, caches, or stores instances.
- Never change `Equals` without a matching `GetHashCode`, and never persist a hash code or use it across processes, app domains, platforms, or runtime versions — .NET hash codes are deliberately randomized per process and are stable only for the lifetime of one process run. Hash-based collections (`Dictionary`, `HashSet`) are fine within a run; persistence, caching keyed by hash across restarts, or network transfer of a hash code is not. A "cleanup" that changes equality semantics or hashing changes observable behavior.

## Closure capture

- A lambda or local function captures variables, not values. In a `foreach` loop the iteration variable is fresh per iteration (since C# 5), but a `for` loop's initializer variable is one shared variable captured by every iteration — extracting the body into a lambda can change what each invocation observes. Moving a lambda in or out of a loop can change captured behavior either way.

## Concurrency and shared state

- Widening or narrowing a `lock` scope, switching `lock` to `SemaphoreSlim`/`Monitor`, or reordering reads and writes around a guard can change serialization, visibility, and deadlock potential. These are concurrency-semantic changes, not formatting.

## References

- [Introduction to LINQ queries (deferred vs immediate execution)](https://learn.microsoft.com/en-us/dotnet/csharp/linq/get-started/introduction-to-linq-queries)
- [Boolean logical operators (&&, ||, short-circuit)](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/boolean-logical-operators)
- [C# operators (evaluation order, ?:, ??, ??=)](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/)
- [Implement a Dispose method](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)
- [Implement a DisposeAsync method](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-disposeasync)
- [Asynchronous programming (async/await control flow)](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)
- [ValueTask (single consumption)](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.valuetask)
- [Records](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/record)
- [Equality operators](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/equality-operators)
