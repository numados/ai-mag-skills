# Other native harnesses

Use only the section matching the actual client. Verify current documentation, installed version and callable launch schema. These are setup/discovery instructions, not tested universal adapters. If a feature is unverified or unavailable, disclose that limit and use a permitted native default or sequential work; do not start another harness CLI to compensate.

## Codex

Sources: [subagents](https://developers.openai.com/codex/subagents), [configuration reference](https://developers.openai.com/codex/config-reference), [app-server model catalog](https://developers.openai.com/codex/app-server).

Current documentation describes standalone custom-agent TOML files in project `.codex/agents/` and user `~/.codex/agents/`, with `CODEX_HOME` potentially changing the user root. Required fields are `name`, `description`, `developer_instructions`:

```toml
name = "evidence_reader"
description = "Gather file-backed evidence without changing files."
developer_instructions = "Read assigned sources. Return references and unknowns; do not edit."
```

This is an illustrative new definition, not permission enforcement. Custom agents inherit parent permissions/provider; a read-only prompt is not a sandbox. Resolve actual tool/permission constraints at the parent before delegation.

After discovering support and obtaining approval, concrete `model` and `model_reasoning_effort` belong in that native file. Do not write Claude's `model: inherit` or `effort` syntax into TOML. Current custom-file values override previously resolved spawn/default/parent values; a spawn argument does not necessarily beat a named definition. Model changes and omitted effort can resolve differently depending on which layer selected the model: inspect actual precedence and choose supported values together.

Where already exposed, app-server `model/list` advertises model IDs, supported reasoning efforts and defaults. Do not start app-server, authenticate or infer access merely to imitate a protocol example. A turn-level effort field is not proof the native spawn operation has the same argument.

Codex session `--profile` configuration is not a named worker role. Avoid creating or migrating session profiles when native custom agents suffice. Check custom-agent discovery and visibility after a save; skill/MCP refresh operations do not prove agent refresh. Do not invent reload commands, enable subagent flags or promise old releases accept the current schema.

## Antigravity

Sources: [custom subagents](https://antigravity.google/docs/subagents/), [discovery](https://antigravity.google/docs/customization-discovery/), [model selection](https://antigravity.google/docs/models/), [effort](https://antigravity.google/docs/cli/commands/effort/).

Current docs describe project `.agents/agents/<name>.md` or `<name>/agent.md` and user `~/.gemini/config/agents/`. Resolve the actual workspace/user scope and name precedence. YAML requires `name` and `description`; the body supplies instructions. For a worker-only definition, current documented fields include `mainAgent: false` and `subagent: true`.

The documented subagent `model` is a tier: `inherit`, `flash` or `pro`. A tier is not a fixed Gemini model ID or permission to write arbitrary catalog display names. Check the active account and installed client's options before proposing choices.

Per-subagent effort and its inheritance are **not established by the cited schema**. Session effort controls do not prove a worker effort field or its effective value. Leave effort unknown unless the installed schema and authoritative version-appropriate evidence establish it; do not invent an agent `effort` key or alter session/global settings to simulate one.

Current docs describe native `invoke_subagent`, separate context and asynchronous operation. Inspect its real schema and tool names before dispatch; guessed tool names can break execution. Workspace `branch` options may create worktrees and need separate permission. Use the installed discovery interface to check new definitions (current docs mention reopening `/agents`); do not assume active workers reload changed definitions.

## Unrecognized or limited clients

Inspect the exposed capabilities and relevant non-secret configuration before asking. Distinguish lack of visibility from proven absence. If models cannot be enumerated, offer only verified options and ask for the smallest missing input. An inherited/default worker may be enough if its actual semantics and data permissions fit.

Do not create guessed configuration files, invent native tool names, promise parent model/effort inheritance, or install tooling to make the runtime match another harness. Missing persistence does not require a new registry: keep supported choices session-only or work sequentially.
