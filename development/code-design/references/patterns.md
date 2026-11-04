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

For any candidate, describe the specific problem, alternatives, applicability, participants, interaction, benefits, and consequences. Check whether the selected language and existing project design already provide a simpler equivalent. Do not introduce extensibility, runtime switching, global state, asynchronous delivery, or new dependencies solely because a pattern allows them.
