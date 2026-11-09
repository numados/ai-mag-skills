# Optional knowledge-mcp adapter

Load this only when the provider's actual tools are discovered in the callable catalog. It is an adapter to one server, not a dependency of this skill on any other skill. Verify the callable schema and response on this installation; versions differ, and a product name is not an API.

## Operations

- `knowledge_status`: readiness, configuration sources, vault and project routing, and the technical write gate. Resolve the configured vault; a missing vault is unavailable, not permission to create a replacement elsewhere.
- `knowledge_search`, `knowledge_read`: search candidates for reconciliation, then bounded metadata, outline, section or body reads. Read only the best candidates and the needed sections.
- `knowledge_write`: create, update, retire or supersede notes. The current interface is two-phase — a call without `confirm: true` returns a preview and persists nothing; review the preview against the curated candidate; obtain the needed approval; then call with confirmation. A preview is not a write, and `confirm` transports an obtained approval, it is not the approval itself.

The server's own note formats, tags, identifiers and supersede mechanism are authoritative. Do not impose the generic note templates on it, and do not rewrite its metadata conventions.

## Verification

After a confirmed write, read the note back with `knowledge_read` and check the intended content, status and links, then confirm bounded rediscovery with `knowledge_search` using the note's distinctive terms. Server-returned validation may satisfy the checks its contract explicitly establishes; perform the missing authorized reads yourself. For an unknown outcome, read back before any retry.

## Partial availability

Do not require every tool for a partial flow: search and read may exist while writes do not, or one vault may be configured while another is not. Use the available domain operations for what they cover, and follow the main routing for the rest — generic record tools, compatible authorized files, or an unsaved proposal — with the standing limits: no files behind this server's invariants, and no fallback after a denial or gate. Do not call the server's task operations for a knowledge-only capture; those belong to the task workflow that composed the checkpoint.
