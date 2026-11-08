# Pi native agents

Load only for Pi. Subagents are extension-provided; two Pi installations may expose different APIs. Use the installed package's `docs/models.md`, `docs/codemode.md` and its launcher documentation/schema. The [Pi project](https://pi.dev/) is the starting point, not proof a particular extension is installed.

## Identify the launcher

- An `Agent`-style tool may expose named agent types, `model`, `thinking`, copied-context and background controls. Inspect its current declaration and profile loader. Do not assume these fields or their precedence exist on a `subagent` tool.
- Pi's packaged `examples/extensions/subagent/` is another implementation: named Markdown/YAML definitions, user agents in `~/.pi/agent/agents/`, project agents in `.pi/agents/`. Its `agentScope` controls project discovery; the example defaults to user agents. Verify the actual agent directory and trusted project scope rather than writing an undiscoverable project file or changing trust settings.
- In that example, definitions parse `name`, `description`, `tools` and optional `model`; omitted model inherits the dispatching session's model and thinking. A pinned model does **not** forward the parent's thinking. Its profile loader does not parse a `thinking` field. Adding one is not effective effort configuration.
- A different installed launcher can support profile thinking or explicit invocation overrides. Verify the reader and precedence first. Use only user-approved values actually supported by that model/launcher. If persistent per-agent effort is unsupported, say so and use a permitted native default or a supported session-only choice; do not change global thinking settings to simulate per-worker support.

For the packaged example only, a minimal inherited-model reader definition is:

```markdown
---
name: evidence-reader
description: Gather evidence from assigned files without editing.
tools: read
---
Read the supplied paths. Return references and unresolved questions.
```

This is not installed by the skill. Choose actual allowed tools and a unique name for the verified launcher before previewing a write. A configured definition is not proof of visibility, model access or successful execution.

## Discover candidates without inference

Prefer the active catalog or model picker. In Pi codemode, when the installed API supports it:

```js
const candidates = await models.getAvailableOfType("chat");
return candidates.map(m => ({ provider: m.provider, id: m.id, name: m.name }));
```

These are catalog candidates with credential evidence, not permission to transmit source or proof of health. Apply session scoping, provider/data restrictions and supported thinking levels before proposing assignments. Do not dump `auth.json` or raw model files containing keys/credential commands. Catalog prices or model metadata may be incomplete.

Use native completion/notification semantics from the actual launcher. For background tools that notify completion, do other work and collect the result on completion; do not busy-poll. A worker's result/error envelope must be checked, including partial changes.

## Optional Jev through codemode

Follow the core skill's Jev permission and bounded-choice rules. If the installed API exposes `models.getAvailableOfType("classifier")`, use its metadata to identify permitted Jev candidates; do not assume a fixed provider or model ID. Classifier availability is separate from the chat-model picker.

After permission and filtering, `models.classify(selectedJev, { state, questions })` can answer a typed choice. Supply only minimal permitted task metadata and **already eligible** route identifiers, with a none/unclear alternative. Do not send the repository merely to route work. Check `stopReason === "stop"`, answer type, and membership in the supplied choices; catch thrown errors too. Provider results can return `error` or `aborted` without throwing. Probabilities are not permission or a reliability guarantee.

This is a conditional use of the installed API, not a bundled classifier integration. If discovery, permission or the interface is missing, use ordinary reasoning. Do not install/configure a provider as an automatic fallback.
