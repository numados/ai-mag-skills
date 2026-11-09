# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Rust skills: add book-informed references with single owners and generated distribution copies — `api-contracts.md` (implementation; copies in project/review/refactor), `lifecycle.md` (async-reliability; copy in implementation), and `concurrency-model.md` (async-reliability; copies in unsafe-review/review/testing-quality). Core skills gained conditional decision rules for conversions, fallible release versus `Drop`, feature unification, wake/cancellation contracts, capacity ownership, publication/CAS/wait-predicate analysis, and Send/Sync/'static distinctions.
- Correct `mag-rust-project` lockfile guidance: the lockfile records one resolved dependency graph; reproduction also depends on toolchain, target, features, command, environment and services.
- Route unsafe review by requested outcome rather than any occurrence of unsafe code; explanation-only unsafe requests stay with `mag-rust-explain`.

### Fixed

- Rust eval fixtures that did not contain the behavior their prompts referenced (`mag-rust-async-reliability` worker, `mag-rust-explain` async shutdown), plus an implementation routing label and new domain-type, unsafe-guard, and feature-unification eval cases with fixtures.
- Eval validation now rejects non-boolean `should_trigger` values and files where the label is present on only some entries.

- CI discovery smoke test: parse only the client's listing section, so the non-agent intro banner (`┌  skills`) is no longer reported as a skill with no `SKILL.md`; pin the `skills` CLI, run `npx --yes`, and print the listing before judging it; report an unparseable listing as a client-format change rather than one failure per entry, and match skip notices case-insensitively.

- `mag-obsidian-markdown`: shared Obsidian-compatible representation for knowledge and progress notes, with flat typed properties, evidence references and unambiguous links; independently usable without Obsidian, a storage server or sibling skills.
- Shared local/global storage configuration and first-use setup for capture and task storage, including MCP/writer-skill discovery, approved configuration previews and provider-schema-preserving handoffs. Common format and configuration references have one editable owner and generated standalone distribution copies.
### Added

- `mag-clear-explainer`: plain-language explanations at a B2/ELI12 reading level, with topic-fitted structure, English correction before the answer, evidence-grounded code and change walkthroughs, and an explicit boundary against implementation and review.
- `scripts/check_discovery.py` and a CI gate that fails when a client skips a skill or lists a different set than the repository publishes.
- `mag-knowledge-capture`: proactive reusable-knowledge capture at explicit checkpoints — candidate triage across domain, architecture, debugging, access, environment and workflow kinds; search-before-write reconciliation (new, duplicate, incomplete, stale, contradictory); per-operation storage routing with MCP domain operations first, denial and unknown-outcome handling, an optional knowledge-mcp two-phase adapter, and a first-use-confirmed `.mag/knowledge/` default when no store is resolvable.
- `docs/authoring.md` with the supported frontmatter profile, progressive-disclosure rules, and when to add `references/`, `scripts/`, or `assets/`.
- Optional `license`, `compatibility`, and flat `metadata` frontmatter in the catalog validator, with the specification's length limits and YAML-ambiguity rejection.
- One-line `compatibility` metadata for `mag-jev-assist`, `mag-task-storage`, and `mag-parallel-orchestration`.

- `mag-commit-message`: repository-aligned commit-message drafting with scope detection, format precedence, a body decision gate, and artifact hygiene; it never stages, commits, or pushes.
- MIT license, included in each independently installable skill directory.
- First-use examples, invocation guidance, and runtime requirements in the README.
- Bundled shared references with a single editable owner, deterministic synchronization, and isolation regression checks.
- `mag-task-storage`: optional reusable knowledge and task memory, capability-driven MCP/record/file access, provider-format preservation and conditional research/planning/history integration.
- `mag-parallel-orchestration`: native-agent coordination with integrated capability-driven setup, project-local routing preferences, optional Jev assistance, and explicit-user-direction-only external agent execution; synthetic behavioral and routing evaluation inputs.
- Five Phase 2 C#/.NET skills: `mag-aspnet-core` (request pipeline, auth/resource authorization, DI lifetimes, caching tenancy, HTTP resilience, observability), `mag-dotnet-testing-quality` (test seams, WebApplicationFactory/Testcontainers, TimeProvider, VSTest vs MTP/TUnit detection), `mag-csharp-refactor` (behavior-preserving refactoring with compatibility contracts), `mag-csharp-explain` (code explanation without editing), and `mag-ef-core` (translation, tracking, pooling, transactions, concurrency, migrations, provider realism).
- Behavioral evaluation sets and fixtures for all ten .NET skills (six cases each), a private final holdout panel, and an expanded 30-case routing set with two independent classifier results.
- Controlled paired baseline evidence (with-skill vs no-skill) with frozen assertions and independent grading, plus static review viewers.

### Changed

- Correct repository URLs and installation sources, remove the unavailable skills.sh catalog link, and replace the nonexistent release-tag example with a published commit.
- Clarify shared installation directories, migration scope, AI-writing assessment boundaries, and outcome-specific .NET environment checks.
- Make construction and C# reference paths local to each skill instead of requiring neighboring skills or a source checkout.
- Clarify `mag-task-research` as problem understanding, evidence gathering and justified solution direction, not implementation planning. Extend `mag-task-planning` with proportionate architecture/code design, available-skill composition and version-applicable technology verification; add focused regression scenarios and synthetic file-backed fixtures.
- Prefix all public skill identities with `mag-` to avoid collisions after installation.
- Document migration from unprefixed skill names.

## [0.1.0] - 2026-11-07

### Added

- Standard `skills/<category>/<name>/SKILL.md` catalog layout.
- Universal installation instructions for pi and other supported agents.
- Claude Code plugin and marketplace manifests.
- Local validation scripts and GitHub Actions checks.
