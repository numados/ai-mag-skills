# Claude Code native agents

Load only for Claude Code. Check the installed version, exposed Agent schema, current definitions and applicable managed restrictions before applying the [subagent documentation](https://code.claude.com/docs/en/sub-agents) or [model configuration](https://code.claude.com/docs/en/model-config). Current documentation can describe features newer than the installed client.

## Definitions and discovery

Current documented locations are project `.claude/agents/<name>.md` and user `~/.claude/agents/<name>.md`. Definitions use YAML frontmatter and a system-prompt body; `name` and `description` are required. Verify scope/name precedence, including managed and session definitions, before reusing or creating a name.

Example of a minimal inherited-model reader:

```markdown
---
name: evidence-reader
description: Gather file-backed evidence without changing files.
tools: Read, Grep, Glob
model: inherit
---
Read assigned sources. Return references and unresolved questions.
```

Use only tools present in the active client. Omitting a tool restriction inherits a tool pool; it is not a read-only default. Choose model aliases or exact IDs from the current permitted catalog, not this example. The definition owns any concrete model/effort settings.

Verify discovery after an approved save. Current docs describe watching existing agent directories, with exceptions such as a newly created directory requiring restart. Do not promise hot reload on every installed version, invent a reload command or start a worker as an unapproved probe.

## Effective model and effort

- Definition `model` currently accepts documented aliases, full IDs or `inherit`; the Agent invocation override has a narrower alias-only contract in current docs. Inspect the actual schema rather than pass a definition value verbatim as an invocation argument.
- Ordinary current model resolution is invocation override → definition → subagent environment default → parent. This is version-sensitive: older clients and enforced environment/organization policy can change it. Do not modify global environment or managed settings to defeat a restriction.
- Native policy/fallback can substitute another model. Distinguish configured/requested from observed model; do not claim a strict user pin was honored when the runtime substituted it.
- Current docs allow definition `effort`, subject to parser/model support. Invocation-level subagent `effort` requires **v2.1.292 or later** and an actual exposed schema field. A session `--effort` option alone does not establish that field.
- Effort can be constrained by environment/policy, invocation and definition settings. Without its own setting, same-model workers can use session effort; different-model workers do not universally inherit it. Supported levels and caps depend on the model/client. Report an unknown effective default rather than inventing one.

Show the actual options during setup. A single permitted Claude model can cover several roles; neither multiple providers nor a fixed Haiku/Sonnet/Opus assignment is required. Do not map economy/quality to a model family without suitable evidence or the user's choice.

Use the active native task interface to inspect effective model/effort when it exposes them. Source/version evidence supports configuration advice, not a claim this account successfully executed the route.
