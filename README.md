# Numados Skills

[![skills.sh](https://skills.sh/b/numados/skills)](https://skills.sh/numados/skills)

A maintained catalog of agent skills for communication, development, reasoning, and Rust engineering.

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
npx skills@latest add numados/skills -s code-review -a pi -g -y
```

Update installed skills:

```bash
npx skills@latest update
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
| [`ai-writing`](skills/communication/ai-writing/SKILL.md) | Audit and improve prose for factual, evidentiary, structural, and stylistic quality. |
| [`clear-report`](skills/communication/clear-report/SKILL.md) | Produce a clear, structured report for a named reader. |
| [`minto-pyramid`](skills/communication/minto-pyramid/SKILL.md) | Structure answers with the conclusion first and grouped supporting points. |

### Development

| Skill | Purpose |
|---|---|
| [`code-construction`](skills/development/code-construction/SKILL.md) | Design and construct code that fits the project. |
| [`code-design`](skills/development/code-design/SKILL.md) | Design internal code structure and interfaces. |
| [`code-review`](skills/development/code-review/SKILL.md) | Review changes and verify review findings. |
| [`discuss-changes`](skills/development/discuss-changes/SKILL.md) | Explain changes interactively, one idea at a time. |
| [`pr-replies`](skills/development/pr-replies/SKILL.md) | Prepare evidence-based replies to review comments. |
| [`task-execution`](skills/development/task-execution/SKILL.md) | Execute an authorized development plan and verify it. |
| [`task-gap-drill`](skills/development/task-gap-drill/SKILL.md) | Investigate a consequential uncertainty in a task. |
| [`task-history`](skills/development/task-history/SKILL.md) | Recover task state, decisions, and remaining work. |
| [`task-planning`](skills/development/task-planning/SKILL.md) | Create an actionable implementation plan. |
| [`task-research`](skills/development/task-research/SKILL.md) | Research a development task before planning or implementation. |
| [`tdd`](skills/development/tdd/SKILL.md) | Develop behavior test-first with red-green-refactor cycles. |

### Reasoning

| Skill | Purpose |
|---|---|
| [`jev-assist`](skills/reasoning/jev-assist/SKILL.md) | Use Jev for bounded classification and decision support. |

### Rust

| Skill | Purpose |
|---|---|
| [`rust-async-reliability`](skills/rust/rust-async-reliability/SKILL.md) | Design and review async and concurrent Rust systems. |
| [`rust-explain`](skills/rust/rust-explain/SKILL.md) | Explain concrete Rust code and its data flow. |
| [`rust-implementation`](skills/rust/rust-implementation/SKILL.md) | Implement authorized Rust features and fixes. |
| [`rust-project`](skills/rust/rust-project/SKILL.md) | Structure Rust packages, crates, and workspaces. |
| [`rust-refactor`](skills/rust/rust-refactor/SKILL.md) | Refactor Rust while preserving observable behavior. |
| [`rust-review`](skills/rust/rust-review/SKILL.md) | Perform a verified multi-category Rust review. |
| [`rust-testing-quality`](skills/rust/rust-testing-quality/SKILL.md) | Design Rust tests and quality gates. |
| [`rust-unsafe-review`](skills/rust/rust-unsafe-review/SKILL.md) | Review unsafe Rust and safety obligations. |

## Repository layout

```text
skills/
├── communication/<skill>/SKILL.md
├── development/<skill>/SKILL.md
├── reasoning/<skill>/SKILL.md
└── rust/<skill>/SKILL.md
```

Each skill is a directory with a `SKILL.md` containing `name` and `description` frontmatter. Evaluation metadata and fixtures are kept under `evals/`, outside the installed skill directories.

## Versioning

`main` contains the latest development version. Stable snapshots are published as Git tags such as `v0.1.0`; use a tag when reproducible installations are required. Changes are documented in [`CHANGELOG.md`](CHANGELOG.md).
