<!-- Generated from skills/development/mag-code-construction/references/technology-evidence.md. Do not edit this copy; run python3 scripts/sync-skill-resources.py in the catalog repository. No source checkout is needed at runtime. -->

# Repository-specific technology evidence

Use this check when an unfamiliar or version-sensitive fact can change the solution. It is part of the requested planning, implementation, explanation or review, not a mandatory extra stage.

1. Establish the relevant project contract from source, configuration, resolved dependencies and existing tests. Distinguish installed tooling from the framework or library version the project actually targets.
2. Identify the consequential question: API availability, package compatibility, provider behavior, configuration or lifecycle. Keep stable correctness and safety constraints in the design; verify changing details instead of treating a skill's examples as a compatibility table.
3. Discover a suitable callable documentation capability, such as Context7 or an equivalent tool. Inspect its schema and library/version coverage; availability alone does not make its result applicable or authoritative. Use it when it can answer the question for this project.
4. If that capability is absent, fails or lacks the required coverage, use permitted web search or direct retrieval of official version-appropriate documentation, package metadata or source. Follow search results to the underlying evidence. Do not send private code or credentials in public queries, or install a provider to complete the lookup.
5. Choose the simplest supported solution that fits the repository and authorized outcome. A newer example, a missing search result or lack of an exact-TFM asset is not proof of incompatibility: check compatible assets, dependencies and applicable contracts. Do not silently upgrade dependencies or invent a fallback.
6. Record only findings that change the decision, with their source and applicability. Reuse verified evidence while current. If confirmation is unavailable, state the uncertainty and block only affected choices; during authorized implementation, verify the selected approach at the smallest useful executable boundary.
