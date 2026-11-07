# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Five Phase 2 C#/.NET skills: `mag-aspnet-core` (request pipeline, auth/resource authorization, DI lifetimes, caching tenancy, HTTP resilience, observability), `mag-dotnet-testing-quality` (test seams, WebApplicationFactory/Testcontainers, TimeProvider, VSTest vs MTP/TUnit detection), `mag-csharp-refactor` (behavior-preserving refactoring with compatibility contracts), `mag-csharp-explain` (code explanation without editing), and `mag-ef-core` (translation, tracking, pooling, transactions, concurrency, migrations, provider realism).
- Behavioral evaluation sets and fixtures for all ten .NET skills (six cases each), a private final holdout panel, and an expanded 30-case routing set with two independent classifier results.
- Controlled paired baseline evidence (with-skill vs no-skill) with frozen assertions and independent grading, plus static review viewers.

### Changed

- Prefix all public skill identities with `mag-` to avoid collisions after installation.
- Document migration from unprefixed skill names.

## [0.1.0] - 2026-11-07

### Added

- Standard `skills/<category>/<name>/SKILL.md` catalog layout.
- Universal installation instructions for pi and other supported agents.
- Claude Code plugin and marketplace manifests.
- Local validation scripts and GitHub Actions checks.
