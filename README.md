# Numados Skills

[![skills.sh](https://skills.sh/b/numados/skills)](https://skills.sh/numados/skills)

A maintained catalog of agent skills for communication, development, reasoning, Rust, and C#/.NET engineering.

## Install

Choose one installation channel. Installing through multiple channels can duplicate skills.

### Any supported agent

The standard [`skills`](https://github.com/vercel-labs/skills) CLI supports pi, Claude Code, Codex, Cursor, Gemini, Copilot, and other agents.

Interactive installation:

```bash
npx skills@latest add numados/skills
```

Non-interactive installation for pi only:

```bash
# Project scope
npx skills@latest add numados/skills -a pi -y

# Global scope
npx skills@latest add numados/skills -a pi -g -y
```

Non-interactive installation for all supported agents:

```bash
npx skills@latest add numados/skills -a '*' -g -y
```

Install one skill:

```bash
npx skills@latest add numados/skills -s mag-code-review -a pi -g -y
```

Update installed skills:

```bash
npx skills@latest update
```

### Migration from unprefixed names

The catalog uses the `mag-` prefix to avoid collisions with skills from other repositories. Existing installations keep the old directories; remove each old skill name you installed, then install the catalog again.

```bash
npx skills@latest remove rust-review --global --agent '*'
npx skills@latest add numados/skills -a pi -g -y
```

Pin an installation to a stable Git tag:

```bash
npx skills@latest add numados/skills#v0.1.0
```

### Claude Code plugin

This repository also contains Claude Code plugin manifests:

```bash
claude plugin marketplace add https://github.com/numados/skills.git
claude plugin install numados-skills@numados
```

Use one channel per installation target; do not install both the universal skills package and the Claude plugin into the same target.

## Local verification

```bash
./scripts/check-skills.sh
./scripts/list-skills.sh
npx skills@latest add ./ --list
```

## Catalog

### Communication

| Skill | Purpose |
|---|---|
| [`mag-ai-writing`](skills/communication/mag-ai-writing/SKILL.md) | Audit and improve prose for factual, evidentiary, structural, and stylistic quality. |
| [`mag-clear-report`](skills/communication/mag-clear-report/SKILL.md) | Produce a clear, structured report for a named reader. |
| [`mag-minto-pyramid`](skills/communication/mag-minto-pyramid/SKILL.md) | Structure answers with the conclusion first and grouped supporting points. |

### Development

| Skill | Purpose |
|---|---|
| [`mag-code-construction`](skills/development/mag-code-construction/SKILL.md) | Design and construct code that fits the project. |
| [`mag-code-design`](skills/development/mag-code-design/SKILL.md) | Design internal code structure and interfaces. |
| [`mag-code-review`](skills/development/mag-code-review/SKILL.md) | Review changes and verify review findings. |
| [`mag-discuss-changes`](skills/development/mag-discuss-changes/SKILL.md) | Explain changes interactively, one idea at a time. |
| [`mag-pr-replies`](skills/development/mag-pr-replies/SKILL.md) | Prepare evidence-based replies to review comments. |
| [`mag-task-execution`](skills/development/mag-task-execution/SKILL.md) | Execute an authorized development plan and verify it. |
| [`mag-task-gap-drill`](skills/development/mag-task-gap-drill/SKILL.md) | Investigate a consequential uncertainty in a task. |
| [`mag-task-history`](skills/development/mag-task-history/SKILL.md) | Recover task state, decisions, and remaining work. |
| [`mag-task-planning`](skills/development/mag-task-planning/SKILL.md) | Create an actionable implementation plan. |
| [`mag-task-research`](skills/development/mag-task-research/SKILL.md) | Research a development task before planning or implementation. |
| [`mag-tdd`](skills/development/mag-tdd/SKILL.md) | Develop behavior test-first with red-green-refactor cycles. |

### C# and .NET

| Skill | Purpose |
|---|---|
| [`mag-csharp-implementation`](skills/dotnet/mag-csharp-implementation/SKILL.md) | Implement authorized C# features and fixes within the repository contract. |
| [`mag-csharp-review`](skills/dotnet/mag-csharp-review/SKILL.md) | Review C# code and compatibility without editing. |
| [`mag-dotnet-project`](skills/dotnet/mag-dotnet-project/SKILL.md) | Create or extend .NET projects and diagnose toolchain/build compatibility. |
| [`mag-dotnet-async-reliability`](skills/dotnet/mag-dotnet-async-reliability/SKILL.md) | Design, review, or fix async lifecycles, concurrency, and shutdown. |
| [`mag-dotnet-performance`](skills/dotnet/mag-dotnet-performance/SKILL.md) | Diagnose .NET performance and verify measured optimizations. |
| [`mag-aspnet-core`](skills/dotnet/mag-aspnet-core/SKILL.md) | Design, review, or fix ASP.NET Core request, security, resilience, and observability behavior. |
| [`mag-ef-core`](skills/dotnet/mag-ef-core/SKILL.md) | Design, review, or fix EF Core query, persistence, transaction, and provider behavior. |
| [`mag-dotnet-testing-quality`](skills/dotnet/mag-dotnet-testing-quality/SKILL.md) | Design realistic .NET test seams, fixtures, runners, and quality gates. |
| [`mag-csharp-refactor`](skills/dotnet/mag-csharp-refactor/SKILL.md) | Refactor C# while preserving observable and compatibility contracts. |
| [`mag-csharp-explain`](skills/dotnet/mag-csharp-explain/SKILL.md) | Explain concrete C#/.NET code and runtime behavior. |

See the [bundle guide](skills/dotnet/README.md) for selection boundaries.

### Reasoning

| Skill | Purpose |
|---|---|
| [`mag-jev-assist`](skills/reasoning/mag-jev-assist/SKILL.md) | Use Jev for bounded classification and decision support. |

### Rust

| Skill | Purpose |
|---|---|
| [`mag-rust-async-reliability`](skills/rust/mag-rust-async-reliability/SKILL.md) | Design and review async and concurrent Rust systems. |
| [`mag-rust-explain`](skills/rust/mag-rust-explain/SKILL.md) | Explain concrete Rust code and its data flow. |
| [`mag-rust-implementation`](skills/rust/mag-rust-implementation/SKILL.md) | Implement authorized Rust features and fixes. |
| [`mag-rust-project`](skills/rust/mag-rust-project/SKILL.md) | Structure Rust packages, crates, and workspaces. |
| [`mag-rust-refactor`](skills/rust/mag-rust-refactor/SKILL.md) | Refactor Rust while preserving observable behavior. |
| [`mag-rust-review`](skills/rust/mag-rust-review/SKILL.md) | Perform a verified multi-category Rust review. |
| [`mag-rust-testing-quality`](skills/rust/mag-rust-testing-quality/SKILL.md) | Design Rust tests and quality gates. |
| [`mag-rust-unsafe-review`](skills/rust/mag-rust-unsafe-review/SKILL.md) | Review unsafe Rust and safety obligations. |

## Repository layout

```text
skills/
├── communication/<skill>/SKILL.md
├── development/<skill>/SKILL.md
├── dotnet/<skill>/SKILL.md
├── reasoning/<skill>/SKILL.md
└── rust/<skill>/SKILL.md
```

Each skill is a directory with a `SKILL.md` containing `name` and `description` frontmatter. Evaluation metadata and fixtures are kept under `evals/`, outside the installed skill directories.

## Versioning

`main` contains the latest development version. Stable snapshots are published as Git tags such as `v0.1.0`; use a tag when reproducible installations are required. Changes are documented in [`CHANGELOG.md`](CHANGELOG.md).
