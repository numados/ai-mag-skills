# Pattern selection

Use these as candidate shapes, not a recipe or a complete catalog. Confirm the problem and compare with direct code first. Names help communication; language features may express the same idea without a class hierarchy. The same need can have more than one suitable solution.

| Need in this context | Candidate | What it changes | Cost or question |
|---|---|---|---|
| Select among genuinely different algorithms | Strategy, or a function value | Isolates interchangeable behavior | Are multiple variants real? Can a simple function suffice? |
| Behavior changes with an object's lifecycle state | State | Associates behavior and transitions with states | Are transitions and invalid states clearer than a simple state machine? |
| Create objects while hiding a meaningful creation decision | Factory method or factory function | Centralizes creation and choice | Is construction actually complex or variable? |
| Assemble an object with many optional or ordered steps | Builder | Separates incremental assembly from the result | Would named arguments or a validated constructor be simpler? |
| Make incompatible existing interfaces cooperate | Adapter | Translates an existing contract into one the caller uses | Can translation preserve semantics and failures? |
| Offer a simpler entry point to a complex subsystem | Facade | Groups a useful set of interactions | Is the facade adding value rather than just forwarding? |
| Add responsibilities around existing behavior | Decorator | Composes wrappers behind a compatible contract | Does ordering or failure handling change behavior? |
| Notify multiple independent consumers of events | Observer | Separates event production from interested consumers | Who owns subscriptions, ordering, failures and lifecycle? |
| Represent an operation for delayed execution, queuing or undo | Command | Makes the operation and its data explicit | Is storing or scheduling a command necessary; what about retries and side effects? |
| Guarantee a single shared instance | Singleton | Provides a global access point and one instance | Is "exactly one" truly required? Global state hides dependencies and couples tests |
| Create families of related, compatible products | Abstract factory | Keeps a product family consistent behind one interface | Is there a family of variants, or just one product? Each new product adds a method to every factory |
| Clone an existing instance instead of reconstructing | Prototype, or a record `with` copy | Reuses a configured instance as the template | Is construction actually costly? Shallow-vs-deep copy semantics add subtle risk |
| Let an abstraction and its implementation vary independently | Bridge | Splits abstraction from implementation into two hierarchies | Are there two real variation axes? One axis does not justify the extra hierarchy |
| Treat a part and a whole uniformly | Composite | Lets one client drive an interface across a tree | Does the child-management API belong on the shared interface, or only on the composite? |
| Share common state across many similar objects | Flyweight | Splits intrinsic from extrinsic state to save memory | Is the object count large enough? The state split and its bugs are subtle |
| Control access to another object | Proxy | Places a surrogate for lazy init, access control, or remoteness | Does the proxy honor the subject's exact contract, or does it become an LSP violation? |
| Pass a request along handlers until one handles it | Chain of responsibility | Lets handlers be added or reordered without touching the sender | Is any handler guaranteed to handle it? Ordering and fall-through are implicit |
| Evaluate sentences of a small grammar | Interpreter | Defines a grammar and its interpreter | Do regex, parser libraries, or LINQ expression trees already cover it? |
| Walk a collection without exposing its structure | Iterator, or `IEnumerable`/LINQ | Encapsulates traversal order | Does the language already provide the traversal? Hand-rolling one is rarely needed |
| Centralize many-to-many communication | Mediator | Routes colleagues through one object | Is the interaction genuinely many-to-many, or will the mediator become a God Object? |
| Capture and restore an object's internal state | Memento | Externalizes state for undo or snapshots | What is the memory cost, and does a wide memento leak internal state? |
| Fix an algorithm's skeleton with variable steps | Template method | Puts the sequence in a base class with overridable steps | Do subclasses couple to a fragile base? Would strategy or delegation serve better? |
| Add operations to a stable object structure | Visitor | Centralizes operations via double dispatch | Will the element hierarchy change? Pattern matching or switch expressions may suffice |
| Remove null-checking noise | Null object | Provides a do-nothing implementation clients dereference safely | Does an `IsNull` branch recreate the null checks? Weigh against nullable reference types |

For any candidate, describe the specific problem, alternatives, applicability, participants, interaction, benefits, and consequences. Check whether the selected language and existing project design already provide a simpler equivalent. Do not introduce extensibility, runtime switching, global state, asynchronous delivery, or new dependencies solely because a pattern allows them.

## When a pattern is harmful

A pattern is not a virtue by itself. Treat these as signals the pattern is hurting rather than helping:

- **Pattern for its own sake** — a pattern chosen to look compliant rather than to answer a concrete problem.
- **Golden-hammer reuse** — one favorite pattern applied everywhere, whether or not it fits.
- **Breaking encapsulation** — the pattern exposes or bypasses state that should stay hidden.
- **Ignoring the simpler solution** — a plain conditional, function, or existing language feature would do.
- **Indirection without a real variation axis** — an abstraction or extension point for variation that never arrives.

This catalog guides new designs. When editing existing code, follow the existing structure instead of introducing patterns unless asked.
