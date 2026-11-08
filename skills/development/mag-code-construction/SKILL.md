---
name: mag-code-construction
description: Design or construct code in any language or framework, including features, methods, modules, interfaces, and integrations. Use when a task requires shaping new behavior or fitting code, its placement, and integration to a project. For refactoring-only or test-first work, prefer the relevant specialized skill when available.
---

# Code construction

1. Establish the requested behavior, constraints, and observable outcomes. Do not invent requirements; ask a focused question when a consequential choice cannot be resolved from the request or project evidence.
2. Inspect only the relevant existing code, project instructions, configuration, dependencies, and tests. Reuse verified context while it remains current; recheck facts affected by changes. Identify applicable language, runtime, framework, and dependency versions and follow established project conventions.
3. Choose the directory, module, and file based on existing responsibilities and dependencies. Trace the necessary callers, interfaces, registrations, configuration, and related tests so the change is reachable and consistent with existing contracts. If the appropriate placement or integration remains materially uncertain, ask rather than guess.
4. For unfamiliar or version-sensitive language, framework, or API behavior, first discover whether a suitable documentation tool or plugin is available and use it if appropriate. Otherwise consult available authoritative sources, including official online documentation when permitted. Confirm that the documentation applies to the project's version. If reliable confirmation is unavailable, state the uncertainty and its impact; ask when it blocks a safe choice.
5. Propose or implement, according to the user's request, the smallest cohesive solution that satisfies the behavior. Keep responsibilities clear, preserve relevant invariants and compatibility, handle meaningful failure cases, and avoid unrelated restructuring or speculative abstractions. A design-only request does not authorize code changes.
6. When implementing, update or add relevant tests at the project's existing test locations. Perform the narrowest useful verification permitted by the environment, then report the actual results and any unverified behavior; do not imply checks ran when they did not.

**New code vs existing code.** When adding new classes or components, consult the bundled [principles](references/principles.md) and [patterns](references/patterns.md) references where they pay off. When modifying existing code, follow the code being changed: do not reformat or restructure untouched code unless the user explicitly asks, and keep the diff confined to the authorized change.

Refactoring and TDD are separate practices, not mandatory steps of construction. When either is appropriate, read and apply a suitable available skill for that practice; otherwise use your own knowledge without claiming to have used a skill. Follow the user's requested method and current environment constraints.
