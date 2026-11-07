# Pattern refactoring — moving legacy code toward patterns

Use this together with the main SKILL when a refactor targets a design pattern or removes an anti-pattern. Read in order: diff discipline first, then the safe-move loop, then the recipes.

## Diff discipline (binding)

Refactor only what the request authorizes. Follow the surrounding style of the code being changed; do not reformat or restructure beyond the authorized change. Keep the diff confined to the change and preserve observable behavior — this is refactor, not redesign.

## Safe-move discipline

1. **Assess before touching.** Inventory the coupling, duplicated logic, rigidity, and inflexible creation, and their severity, before editing anything.
2. **Set an explicit goal per change.** State which maintainability or extensibility improvement each move targets, so pattern selection follows need, not fashion.
3. **Pin current behavior first.** When existing tests do not already pin today's behavior, add characterization-style checks — or an equivalent safety net such as an invariant argument, a measurement, or an explicit recorded risk decision — before the first change.
4. **Refactor for clarity before patterns.** Extract methods, split large classes, and loosen coupling first — patterns assume a clean modular base, and inserting them into tangled code raises defect risk.
5. **Introduce the pattern incrementally.** Small, behavior-preserving steps, verifying after each; never a large rewrite.
6. **Verify and record.** Run the tests after each step and note the before/after design and its rationale.

## Incremental moves (recipes)

- **Replace a conditional with polymorphism.** Create the new subclasses as standalone classes first — do not touch the original yet. Link them under an abstract base, move the shared members up and remove the type-aware switch, then replace the constructor with a factory. Verify after each smaller step rather than all at once.
- **Replace a constructor with a factory, then a factory class.** Do it in two steps: the static factory method is directly testable but consumers still cannot substitute it through dependency injection; the factory class behind an interface is injectable.
- **Replace inheritance with delegation** on refused bequest — a subclass that no-ops most of what it inherits. Split the base; the former subclass becomes an injected collaborator, with a null object for the "no reward" case.
- **Treat clarity refactors as a stepping stone, not the destination.** Splitting a monolith into private delegating methods improves readability but does not buy adaptability; only moving each responsibility behind its own interface does.

## Anti-patterns and their removal

| Anti-pattern | Signal | Move toward |
|---|---|---|
| God Object | One class owns many unrelated concerns and changes for unrelated reasons | Extract focused classes; delegate through interfaces |
| Golden hammer | A favorite pattern applied everywhere regardless of fit | Apply a pattern only where it answers a concrete challenge; return to simpler code |
| Premature abstraction | Interfaces or extension points that are never used; patterns before the problem manifests | Implement the simple solution; add the abstraction when growth proves it |
| Service Locator | A class fetches an ambient static container; its dependencies are invisible | Constructor injection at the composition root; the locator only as a last resort |
| Illegitimate injection | An interface constructor plus a default constructor that `new`s implementations | Remove the default constructor; supply mocks through the real constructor |
