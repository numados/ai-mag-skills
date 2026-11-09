# Storage configuration and first-use setup

This reference owns destination configuration and setup for MAG knowledge and task memory. It is bundled in capture and storage so either can work alone. Configuration chooses a destination; it grants neither write access nor approval to persist particular content.

## Resolve without forking

Resolve the requested section and operation, not a generic “MCP present” flag:

1. An explicit destination for this request.
2. Project configuration: the applicable provider's project mapping or `<project-root>/.mag-storage.json`.
3. Global defaults: the provider's applicable default or `${XDG_CONFIG_HOME}/mag/storage.json`; when XDG_CONFIG_HOME is unset, use `~/.config/mag/storage.json`.
4. No applicable destination: start the setup dialogue below if persistence is requested.

A project root comes from explicit context or the repository root, not an arbitrary tool working directory. Use an explicitly chosen configuration path when supplied; do not scan the home directory for plausible vaults.

Local configuration overrides global defaults **as a destination unit**, not by merging paths or writer hints from unrelated stores. Resolve a generic configuration's relative `root` from that configuration file's directory. An absolute `root` is used as written. A missing or invalid local target is an error to correct, not permission to fall through to a global store.

Provider settings and a MAG file can describe the same store. Verify identity/namespace; if same-priority settings disagree, show the conflict and ask rather than choosing silently. An explicit destination disambiguates this request but does not migrate existing records or authorize ignoring an access refusal.

Resolve existing configuration and readiness for authorized memory reads as well as writes. A read-only lookup can resolve its store but cannot create configuration or start setup unless requested. If its destination is missing, ask where to read. Note-only formatting of supplied content/targets needs no backend discovery. Honor narrower no-probing or no-configuration-read constraints, and skip memory resolution for work that does not need memory.

## Generic configuration

An existing three-field project file remains valid:

```json
{
  "root": "../engineering-memory",
  "knowledgeRoot": "Knowledge",
  "taskRoot": "Tasks"
}
```

The same shape works at global scope. Section roots are relative subdirectories inside the resolved `root`, not traversal paths or symlinks escaping it. Preserve the destination's actual layout and case. Missing sections are not a reason to guess another store; ask before establishing a new section. For a newly approved generic store, `knowledge` and `tasks` are proposed defaults, created only as needed.

Optional routing hints may be added after their actual capabilities are discovered:

| Field | Meaning |
|---|---|
| `provider` | Chosen provider identity; verify against callable tools, not a guessed API. |
| `store` | Provider's actual vault/store/namespace selector. An opaque routing hint, not an invented argument name. |
| `writerSkill` | Available skill chosen to arrange/write the records; instructions, not an executable tool or permission. |

For provider-owned storage, `root` can be absent if the provider resolves the chosen namespace itself. Resolve `store` through its documented contract. A generic file route requires a verified filesystem root. A hint never establishes capabilities, overrides a server's format, or authorizes direct files behind its invariants.

Prefer the provider's native configuration when it already expresses the user's choice. Do not create a redundant MAG file to mirror it. Store no credentials or personal session content in either file. A global file may hold a private machine path; do not copy that path into published notes or commit it as a portable configuration.

## Setup dialogue

Enter this dialogue automatically when an authorized persistence request has no known destination. Also use it for an explicit configure/change-storage request. Starting a dialogue is not changing configuration.

1. **Discover before asking.** Inspect the actual MCP/tool catalog and available skill names/descriptions. Read a relevant writer skill only when it can help. Identify supported knowledge and task operations separately, native destination mappings, Markdown/file capabilities and bounded readiness evidence. A listed skill does not prove tools, access or successful execution. Reuse established capability/readiness evidence within its stated scope; a missing destination choice does not make known readiness unknown. For a supplied hypothetical catalog, reason from its stated facts without probing real tools. Readiness still grants neither destination selection nor write permission.
2. **Show the useful choices.** Report ready destinations, unavailable configured targets and genuinely missing capabilities. Explain whether a choice supports knowledge, progress or both. Do not send note content to candidate providers as a discovery probe.
3. **Ask the smallest choice.** Ask which destination and local/global/session scope the user wants. Offer verified MCP or writer-skill options first when suitable. If none exists, offer an explicitly chosen existing folder or a project-local `.mag/knowledge/` (and task section if needed) as proposals, not automatic fallbacks. Do not ask again for decisions already supplied.
4. **Preview the setup.** Show the exact configuration path, chosen store/namespace, section layout, writer route and configuration diff. Identify any needed directories. Existing notes/protocols remain untouched; migration is a separate operation.
5. **Obtain approval before mutation.** Apply only the approved configuration and necessary directories using supported tools. A provider's preview/confirmation flow still applies. Do not install a skill/server, authenticate, initialize a repository, alter remote configuration or migrate data without separate explicit approval.
6. **Verify and continue.** Read the resulting configuration, resolve the same destination, perform a permitted readiness/read check, then resume the original save within its own content permission. A configuration write is not proof of a note write. Keep a session-only choice in session if that is what the user chose.

If setup is declined, blocked or unanswered, keep the useful content in chat and report it unsaved. Do not repeatedly interrupt ordinary work. A concrete permitted route awaiting setup/write approval can be reported as proposed; unavailable or unverified compatibility stays unsaved.

## Writer handoff

For each operation prefer the store's ready domain API, then compatible authorized record tools, then compatible authorized files. A selected writer skill can guide either fallback using the tools it actually has. Pass the curated content, supported metadata, known identity, link base and constraints; let the writer arrange it under the resolved destination. Do not create a second mirror simply because the writer chooses its own filenames.

For generic Markdown, use the common note-format contract bundled by the caller. A provider owns its accepted arguments and schema: map the content through those, not around them. If required metadata/relationships cannot be represented, report the incompatibility before writing.

An access denial or write gate is not a missing destination: honor it, report the affected content unsaved or pending approval, and request a permission correction when appropriate. Do not start setup to evade it. For an unknown write outcome, establish persisted state by readback before retrying, switching writers or changing destinations. An unavailable configured target calls for correction of that target; choosing a replacement is an explicit user decision, not an automatic fallback.
