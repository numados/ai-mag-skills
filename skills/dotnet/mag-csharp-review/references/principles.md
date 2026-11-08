<!-- Generated from skills/development/mag-code-design/references/principles.md. Do not edit this copy; run python3 scripts/sync-skill-resources.py in the catalog repository. No source checkout is needed at runtime. -->

# Design principles — verification checklists

Use these to verify new code and design reviews. Each principle lists a checkable question, the signal that it is violated, and when the rule legitimately bends. When modifying existing code, verify against that code's own conventions and keep the diff minimal — no drive-by SOLID or DRY rewrites unless the user asks.

## SOLID

### SRP — Single Responsibility

- **Check:** Does this class or method have more than one reason to change? If two independent requirement changes would both force edits here, it has more than one responsibility.
- **Violation signal:** One class or method changes when any of several independent things change; a constructor with many dependencies; a single method that also owns unrelated concerns.
- **Bends when:** predicted variation is near zero — a small stable tool may stay monolithic. SRP means one reason to change; the fix is giving each responsibility its own home (class, module, or method), and an interface is needed only when callers must substitute or vary an implementation — not one interface per responsibility.

### OCP — Open/Closed

- **Check:** Can new behavior be added by adding code to an existing extension point instead of editing an already-tested class?
- **Violation signal:** Every new requirement forces editing a deployed class; a switch or type-based conditional that must grow a case per variant.
- **Bends when:** a bug fix (always an edit — write a failing test, then the smallest fix); a client-unaware change; protect only predicted variation (too few and too many extension points both fail). Prefer interface inheritance over implementation inheritance as the extension point.

### LSP — Liskov Substitution

- **Check:** Can a subtype be substituted for its base type everywhere the base is used, without breaking the base contract?
- **Violation signal:** A strengthened precondition; a weakened postcondition; a broken invariant; a new exception type that the base contract does not allow; variance misuse — variance is a generic-interface/delegate concept (`in`/`out`), not a method-override freedom: overrides keep parameter types exactly and may only narrow outputs via covariant returns (C# 9+).
- **Bends when:** it does not bend — treat a violation as debt to fix by redesigning the hierarchy (do not model an Ostrich as a flying Bird; move guarded fields behind protected setters).

### ISP — Interface Segregation

- **Check:** Does every implementer actually need every member, and does every client actually use every member?
- **Violation signal:** Pass-through or no-op decorators; one broad interface forcing implementers to stub members they do not support.
- **Bends when:** a cross-cutting decorator that legitimately applies to every method (logging, transactions); segregation raises constructor arity (a cost to weigh); merge members that are truly identical rather than splitting them.

### DIP / D — Dependency Inversion (also called Dependency Injection)

- **Check (inversion):** Do high-level modules depend on abstractions, not concrete details? Constructing a low-level value or DTO inside a method is normal; constructing a *service dependency* inside high-level policy is the violation.
- **Check (injection):** Does the class declare its dependencies (typically via constructor) instead of constructing or fetching them?
- **Violation signal (inversion):** high-level policy reaching into concrete details; a Service Locator.
- **Violation signal (injection):** hidden construction of service dependencies; injecting the container; an interface constructor plus a default constructor that `new`s implementations ("illegitimate injection"). An interface living in the same assembly as its implementation ("Entourage") is a coupling smell to weigh, not an automatic violation.
- **Bends when:** a Service Locator as a last resort for a framework with no injection hook; only the composition root may know DI; the mechanism choice (Poor Man's DI vs conventions) is a trade-off, not a violation.

Treat the "D" as one principle with two faces: depend on abstractions, and declare those dependencies instead of building them.

## DRY — Don't Repeat Yourself

- **Check:** Does the same creation, validation, or algorithm logic exist in more than one place, so a change must be applied at every site?
- **Violation signal:** Duplicated creation code, duplicated code fragments or similar algorithmic sequences, or copied pattern implementations; a fix must then be applied in several places, and inconsistent edits produce subtle bugs.
- **Bends when:** code that looks alike but changes for different reasons is not duplication; refactor on the third occurrence rather than the first. Duplication kinds: **accidental** — the same logic copied to several sites that must change together, consolidate it; **essential** — two different concerns that merely look similar, leave them separate.

## Boundary principles

- **KISS** — prefer the simplest solution that meets the need; a pattern that does not pay for itself is complexity, not virtue.
- **YAGNI** — do not build for variation that is not yet predicted or requested; add abstraction when growth proves it necessary, not in advance.
