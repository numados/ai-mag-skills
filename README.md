# Numados Skills

[GitHub repository](https://github.com/numados/ai-mag-skills)

A maintained catalog of agent skills for communication, development, reasoning, Rust, and C#/.NET engineering.

## Install

Choose one installation channel. Installing through multiple channels can duplicate skills.

### Any supported agent

The standard [`skills`](https://github.com/vercel-labs/skills) CLI supports pi, Claude Code, Codex, Cursor, Gemini, Copilot, and other agents.

Interactive installation:

```bash
npx skills@latest add numados/ai-mag-skills
```

Non-interactive installation targeting Pi:

```bash
# Project scope
npx skills@latest add numados/ai-mag-skills -a pi -y

# Global scope
npx skills@latest add numados/ai-mag-skills -a pi -g -y
```

The CLI uses `.agents/skills/` for project installation and `~/.agents/skills/` for global installation targeting Pi. Other agents that read these shared directories can discover the same skills. The `-a pi` flag does not isolate them from those agents.

Non-interactive installation for all supported agents:

```bash
npx skills@latest add numados/ai-mag-skills -a '*' -g -y
```

Install one skill:

```bash
npx skills@latest add numados/ai-mag-skills -s mag-code-review -a pi -g -y
```

Update installed skills:

```bash
npx skills@latest update
```

### Migration from unprefixed names

The catalog uses the `mag-` prefix to avoid collisions with skills from other repositories. A new name does not remove an old installation. Before removal, identify the old skills from this catalog and their installation scope. Do not remove same-named skills from other sources.

For an old global installation targeting Pi, remove each confirmed old name, then install this catalog:

```bash
npx skills@latest remove rust-review --global --agent pi
npx skills@latest add numados/ai-mag-skills -a pi -g -y
```

For a project installation, omit `--global` and `-g`. For a fixed catalog revision, see [Versioning](#versioning).

### Claude Code plugin

This repository also contains Claude Code plugin manifests:

```bash
claude plugin marketplace add https://github.com/numados/ai-mag-skills.git
claude plugin install numados-skills@numados
```

Use one channel per installation target; do not install both the universal skills package and the Claude plugin into the same target.

## First use

A skill supplies instructions and bundled references, not a new executable tool. After installation, start a new agent session or use the host's reload mechanism. Work from the repository or directory that contains the material for your task.

### Invoke a skill explicitly

In Pi, use `/reload` after installing into an active session, then enter:

```text
/skill:mag-code-review Review the current local diff. Do not modify files or post comments. Return only verified findings with file locations and impact.
```

For a standalone Claude Code skill, use `/mag-code-review`. For the Claude plugin channel above, use `/numados-skills:mag-code-review`. Append the same task description after the command. Command names and explicit-invocation syntax depend on the host; other supported agents can also select skills from a natural-language request.

This request asks for a read-only review with verified findings and important verification limits. The skill directs the agent to state when it finds no actionable issues. If you do not mean the current local diff, supply the intended base/head or files.

To check loading, inspect the host's tool trace for the requested `SKILL.md` read or its explicit skill-loading event. A mention of the skill name in the answer is not proof that it was loaded. If it is missing, check the installed skill name and scope, reload the session, and use the host's explicit invocation. If the host cannot discover skills, supply the installed `SKILL.md` path and ask the agent to read it before the task.

### Other example requests

Use these task descriptions with your host's skill invocation, or name the skill in a normal request:

| Skill | Example request | Expected result |
|---|---|---|
| `mag-task-research` | Investigate why invoice totals differ from the supplied example. Read the example and relevant code. Do not edit files or produce an implementation plan. | Evidence, current behavior, a supported solution direction, and open questions. |
| `mag-task-planning` | Plan the supplied invoice-rounding fix in this repository. Identify files, integration points, tests, and unresolved decisions. Do not implement it. | An actionable plan with scope, acceptance checks, and unresolved choices. |
| `mag-code-construction` | Implement the approved rounding plan above, including its tests. Stay within the approved files and behavior. Do not install dependencies, commit, or deploy. | The authorized changes and actual verification results, including checks that could not run. |

These are separate requests, not a mandatory pipeline. Start with the skill matching your goal. Installing a skill or obtaining a plan does not authorize implementation; approve the actual plan before using the implementation example. If the plan is not in the current conversation, supply it explicitly.

## Requirements and optional capabilities

Each skill can be installed on its own. Its required reference files and license are inside its directory. Names of other skills indicate optional alternatives or specialist guidance, not installation dependencies. No source checkout or resource-generation step is needed to use an installed skill.

| Capability | What must already be available |
|---|---|
| Installation through `skills` | Node.js and npm/npx. The CLI currently requires Node.js 22.20 or later. Git and network access are needed for GitHub sources. See the [CLI documentation](https://github.com/vercel-labs/skills). |
| Reading, editing, or verifying project code | The host agent's permitted file, shell, and documentation tools. Builds and tests need the target project's toolchain, such as .NET or Rust, when those checks are requested. |
| `mag-parallel-orchestration` | A native subagent launcher exposed by the host. Pi requires an installed subagent extension; the skill does not install one. See its [runtime guides](skills/development/mag-parallel-orchestration/SKILL.md). |
| `mag-jev-assist` | Externally configured Jev classifier access. Jev is an optional model for choosing among bounded alternatives, not a general reasoning replacement. This repository supplies instructions and a [Pi codemode adapter](skills/reasoning/mag-jev-assist/references/pi-codemode.md), not the classifier runtime, credentials, or provider setup. |
| Persistent task memory | An explicitly configured and authorized store. See the optional integration below. No particular MCP server is required. |

Installing these skills does not install compilers, MCP servers, agent extensions, model providers, or storage. It grants no access or write permission. Without optional capabilities, the agent uses ordinary reasoning, direct work, or chat output where suitable. It reports important capability limits. An unavailable capability is not permission to install or configure it.

## Optional knowledge and task memory

Research, planning and history work without persistent storage. Install `mag-task-storage` to add optional memory integration:

```bash
npx skills@latest add numados/ai-mag-skills -s mag-task-storage -a pi -g -y
```

The addon separates reusable knowledge from task state and history. It uses ready MCP domain operations first, supplies missing semantics through record tools, or uses compatible authorized files. It selects access per operation, not merely by MCP presence. An access denial never authorizes a filesystem bypass.

Use an explicit destination, project configuration, or global defaults. Generic stores use `.mag-storage.json` in the project or `${XDG_CONFIG_HOME:-~/.config}/mag/storage.json` globally; see [configuration and first-use setup](skills/development/mag-task-storage/references/storage-configuration.md). When a save needs a destination, the skill discovers suitable MCP operations and writer skills, asks for the destination and scope, and previews configuration before an approved change. Installing a skill grants no write permission and performs no setup, migration or server installation. Until a destination is chosen, useful content stays unsaved in chat. Knowledge changes need their own authorization, not just permission to log tasks.

Without the addon, current chat-default behavior is unchanged. A chat-only/read-only request still takes precedence when it is installed. Discovery and composition depend on the harness exposing the available skills; this package does not install an always-on hook. Explicitly supply the skill if the harness cannot discover it. The Claude plugin includes the addon in its full catalog; installation is not storage activation or permission. Execution and gap-drill use the addon for requested or otherwise authorized tracking handoffs, not to turn ordinary work or read-only questions into automatic logging.

`mag-knowledge-capture` adds capture at explicit checkpoints: it triages work products into reusable notes, reconciles them with existing knowledge, and uses the same setup/access contract. A first-use `.mag/knowledge/` folder is one proposal requiring approval, never a bypass of a denial, write gate or unavailable configured target. Capture owns curation; storage owns persistence routing for its workflows.

`mag-obsidian-markdown` prepares the shared representation for knowledge and task progress: flat typed YAML properties, tags and aliases, evidence references and unambiguous internal links. It does not search a vault or choose storage. Capture and storage bundle its format contract, so each skill still installs independently. Knowledge and progress keep their distinct lifecycle rules; MCP providers keep their accepted schemas and placement. Formatting alone never authorizes a write.

## Authoring and local verification

See the [skill authoring guide](docs/authoring.md) for the supported
frontmatter profile, progressive disclosure rules, and when to add
`references/`, `scripts/`, or `assets/`.

```bash
./scripts/check-skills.sh
./scripts/list-skills.sh
npx skills@latest add ./ --list | python3 scripts/check_discovery.py
```

## Catalog

### Communication

| Skill | Purpose |
|---|---|
| [`mag-ai-writing`](skills/communication/mag-ai-writing/SKILL.md) | Assess AI-like writing patterns and write or edit clear, natural prose without inferring authorship. |
| [`mag-clear-explainer`](skills/communication/mag-clear-explainer/SKILL.md) | Explain any topic in plain language at a B2/ELI12 level, choosing the structure that fits. |
| [`mag-clear-report`](skills/communication/mag-clear-report/SKILL.md) | Produce a clear, structured report for a named reader. |
| [`mag-minto-pyramid`](skills/communication/mag-minto-pyramid/SKILL.md) | Structure answers with the conclusion first and grouped supporting points. |

### Development

| Skill | Purpose |
|---|---|
| [`mag-branch`](skills/development/mag-branch/SKILL.md) | Produce a repository-aligned branch name and creation commands without changing Git state. |
| [`mag-code-construction`](skills/development/mag-code-construction/SKILL.md) | Design and construct code that fits the project. |
| [`mag-code-design`](skills/development/mag-code-design/SKILL.md) | Design internal code structure and interfaces. |
| [`mag-code-review`](skills/development/mag-code-review/SKILL.md) | Review changes and verify review findings. |
| [`mag-commit-message`](skills/development/mag-commit-message/SKILL.md) | Draft repository-aligned commit messages without touching Git state. |
| [`mag-discuss-changes`](skills/development/mag-discuss-changes/SKILL.md) | Explain changes interactively, one idea at a time. |
| [`mag-knowledge-capture`](skills/development/mag-knowledge-capture/SKILL.md) | Curate reusable knowledge at explicit checkpoints: triage candidates, reconcile with existing notes, and persist through available MCP operations, record tools, or authorized files. |
| [`mag-obsidian-markdown`](skills/development/mag-obsidian-markdown/SKILL.md) | Prepare Obsidian-compatible knowledge and progress notes with typed properties, evidence and unambiguous links; leave storage to the writer. |
| [`mag-parallel-orchestration`](skills/development/mag-parallel-orchestration/SKILL.md) | Coordinate native agents with integrated setup, model/effort discovery, and verified synthesis. |
| [`mag-pr-replies`](skills/development/mag-pr-replies/SKILL.md) | Prepare evidence-based replies to review comments. |
| [`mag-shift-left-testing`](skills/development/mag-shift-left-testing/SKILL.md) | Orchestrate cross-stack quality from requirements through CI: choose the earliest reliable verification seam per risk and hand per-stack work to specialized skills. |
| [`mag-task-execution`](skills/development/mag-task-execution/SKILL.md) | Execute an authorized development plan and verify it. |
| [`mag-task-gap-drill`](skills/development/mag-task-gap-drill/SKILL.md) | Investigate a consequential uncertainty in a task. |
| [`mag-task-history`](skills/development/mag-task-history/SKILL.md) | Recover task state, decisions, and remaining work. |
| [`mag-task-planning`](skills/development/mag-task-planning/SKILL.md) | Plan clean implementation and correct integration; preserve existing architecture unless redesign is explicitly requested. |
| [`mag-task-research`](skills/development/mag-task-research/SKILL.md) | Understand a problem and establish an evidence-based solution direction, without implementation planning. |
| [`mag-task-storage`](skills/development/mag-task-storage/SKILL.md) | Add optional reusable knowledge and task memory through available MCP capabilities or compatible files. |
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

Each skill is a directory with a `SKILL.md` containing required `name` and
`description` frontmatter. Optional portable metadata is documented in the
[authoring guide](docs/authoring.md). Evaluation metadata and fixtures are
kept under `evals/`, outside the installed skill directories.

### Maintaining bundled resources

Shared reference text has one editable owner, recorded in `scripts/sync-skill-resources.py`. Other skills receive committed local copies, marked as generated. The root `LICENSE` owns the license text included in every skill directory. Edit the owner. Then regenerate the copies and run the checks:

```bash
python3 scripts/sync-skill-resources.py
./scripts/check-skills.sh
```

Do not edit generated copies. `check-skills.sh` checks synchronization without rewriting files and runs resource regression tests. It rejects local reference links that leave the individual skill directory or point to missing files. This is a maintainer step, not an installation requirement. Local checks require Bash and Python 3.9 or later; the resource script uses only the Python standard library.

## License

[MIT](LICENSE). Each independently installable skill includes the same license notice. Third-party sources linked by the skills retain their own terms; a link does not relicense the source material.

## Versioning

`main` is the development branch. No Git release tags are currently published. To fix the catalog revision, install from a full commit SHA:

```bash
npx skills@latest add numados/ai-mag-skills#57bb6ca7a63431c192e026351315903faef18b5e
```

This example points to a published commit. It fixes the skill source revision, not the installer or host version. The plugin manifest's `0.1.0` version does not imply a published Git tag. Changes are documented in [`CHANGELOG.md`](CHANGELOG.md).
