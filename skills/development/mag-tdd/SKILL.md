---
name: mag-tdd
description: Develop a requested behavior test-first using short red-green-refactor cycles, or organize tests around observable behavior in an existing codebase. Use when the user requests TDD, test-first development, or asks to add tests to existing code. Distinguish characterization tests from test-first development; do not treat every coding task as a TDD request.
---

# Test-driven development

Use tests to guide a requested behavior and provide evidence about it. Respect the user's scope and the project's existing test practices. Do not claim a cycle or check occurred unless it actually ran.

## Find the test location and contract

- Read the requirement and only the relevant code, callers, existing tests, test configuration, and project instructions; reuse previously verified context while current. Identify observable behavior, meaningful examples and error cases; ask when a material expected behavior is ambiguous.
- Find the appropriate existing test project, directory and file by following nearby tests for the same component and repository conventions. Check the framework, naming, fixtures, setup and test-discovery rules. Add to an appropriate file or create a neighboring file where it fits. If no precedent exists, choose a simple structure supported by the project's tools; discuss a material architectural choice such as a new test project before making it.
- Prefer testing through a stable, relevant interface at the smallest boundary that can expose the behavior; use integration tests where interaction with a real provider is part of the contract. Cover technical contracts and failures as well as business rules. Do not introduce a complex test framework, shared helper, or dependency without a demonstrated need and required permission.

## New behavior: test first

For each small behavior slice:

1. Write a focused test that expresses the expected observable result. Run the targeted test and inspect the failure. The expected failure should show that the missing or incorrect behavior causes it, not that the environment or test setup is broken. A compilation failure for a not-yet-created interface can be an intermediate step; implement enough of the interface and then establish a meaningful behavioral failure before claiming RED.
2. Make the smallest complete production change that satisfies that behavior. Run the targeted test and relevant existing tests; investigate failures rather than masking them.
3. Consider whether the changed code or tests need a small clarity improvement. Refactor only if useful and within scope, then rerun affected tests. Do not expand this into unrelated restructuring.
4. Repeat for remaining behavior and edge cases. Ensure the test runner discovers the new tests. Run the related suite, and broader checks when project policy or risk warrants them.

If a meaningful failing test cannot be observed or tests cannot run, explain the exact limitation. Do not claim a verified RED, GREEN, or completed TDD cycle. An environmental failure requires diagnosis, not a production fix guessed from the failure.

## Existing behavior

A characterization test records existing behavior and may pass immediately; it is not evidence of a test-first RED. Check its assertions, discovery and the behavior it actually observes. Where useful and safe, assess whether it would detect a meaningful regression using a permitted, reversible technique; deliberately breaking production code is not a required step. Do not change production behavior merely to label the test TDD.

## Report

Summarize changed tests and their location, actual commands and outcomes, meaningful RED/GREEN evidence when observed, and any unrun checks or remaining uncertainty. Use an available dedicated skill for a separate practice when applicable; otherwise proceed with the agent's own knowledge without claiming that skill was used.
