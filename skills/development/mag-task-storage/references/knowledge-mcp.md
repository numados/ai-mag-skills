# Optional knowledge-mcp adapter

Load only when these actual provider tools are discovered. This is an adapter to the server, not a dependency on any Numados skill. Verify the callable schema and response on this installation; versions can differ.

## Resolution and operations

- `knowledge_status`: read readiness, configuration sources, vault/project routing and technical write gate. Resolve the configured vault instead of guessing a path. A missing vault is unavailable, not permission to create a replacement.
- `knowledge_search`, `knowledge_read`: search candidates, then bounded metadata/outline/section/body reads.
- `knowledge_write`: create/update/retire/supersede notes. The current interface previews without `confirm: true`, then executes and validates with confirmation. Follow its approval process; a preview is not persistence.
- `knowledge_task`: use `status` for recovery; `init`, `iteration`, `update` for authorized task records. The server owns event numbering, previous links and index projection. It does not replace writing a detailed research/plan note when needed; use `knowledge_write` for those artifacts, then the task operation to record/link the handoff. Do not call the task API for a knowledge-only request.

Prepare compatible Obsidian Markdown for supported content/body fields and submit metadata only through actual accepted arguments. The server controls placement and serialization. Verify that required scope, evidence and relationships survive its preview/readback; an unsupported mapping needs clarification, not silent loss or a second file writer. Do not require all tools for a supported partial operation. For missing functions, follow the main access contract with the provider's actual primitives or compatible files. Honor each write preview/confirmation process and permission; `confirm` transports obtained approval, not permission on its own.

## Provider-owned task protocol

The known task API uses `_task_index.md`, current `research.md` / `plan.md` / optional `remarks.md`, and immutable `iterations/` notes. Its `numados-task-*-v1` tags are server data formats, not a requirement to install Numados. Keep them unchanged; do not replace them with the generic MAG defaults.

For the known schema, `status` is the event outcome (`active|ready|blocked|done`); `taskStatus` sets lifecycle (`brainstorm|planning|implementing|reviewing|blocked|done`). Map a MAG research pass to the server's `brainstorm` stage. Supply `taskRoot` only from an established destination/configuration. A proposed plan is still proposed regardless of lifecycle.

Direct-file fallback must preserve the actual provider protocol, not just these filenames. Inspect accessible existing records and the provider's current format/validation contract first. If those do not establish safe compatibility (including metadata, numbering and indexing requirements), report the missing capability and stop the write. Do not claim generic MAG records can be adopted by this server without a verified contract or an authorized migration.

Known configuration sources are repository `.knowledge-mcp.json` and the central configuration selected by `KNOWLEDGE_MCP_CONFIG` or `~/.config/knowledge-mcp/config.json`. They can map a project to a vault, knowledge root and task root. Read only the needed routing values; do not expose credentials or machine-private configuration. Configuration compatibility does not prove format or write-policy compatibility.
