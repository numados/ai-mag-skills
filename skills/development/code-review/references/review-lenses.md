# Review lenses

Apply only lenses relevant to the actual change or claim. They are prompts for investigation, not findings by themselves.

- **Contracts and compatibility:** Check callers and implementers, serialization, persistence, migrations, defaults, old data, rolling-version compatibility, and public interfaces where changed. Trace the actual supported versions and configurations.
- **State and failures:** Follow validation, mutation, durable or external effects, failure, cancellation and recovery. A lost response can mean an effect happened; retry safety depends on actual idempotency and recovery guarantees.
- **Concurrency and security:** Trace ownership, authorization, trust boundaries, timing, race windows and observable consequences. Confirm the environment and an attack or interleaving is reachable; do not include exploit details beyond what the reader needs.
- **Performance:** Identify input scale, resource bounds and changed hot paths before predicting a material regression. A theoretical complexity change alone is not proof of production impact.
- **Tests:** Check discovery, assertions, representative edge cases, and whether an existing test actually exercises the suspected path. Missing tests matter when they leave meaningful changed behavior unprotected; they do not by themselves establish a runtime defect.
- **Design and maintainability:** Check whether a changed rule, format, mapping or invariant has an established owner and whether repeated copies encode the same knowledge rather than coincidental similarity. Identify every relevant location and a concrete co-change or divergence consequence. Check responsibility, dispatch, substitutability, interface use and dependency direction against actual contracts and repository rules. Avoid proposing speculative abstraction or unrelated refactoring.

Use proportionate, safe checks and stop when the candidate is confirmed, refuted or bounded by a specific missing fact. If inspecting a separate component or repository requires authorization, disclose the gap instead of assuming its behavior.
