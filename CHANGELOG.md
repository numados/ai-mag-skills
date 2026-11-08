# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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
