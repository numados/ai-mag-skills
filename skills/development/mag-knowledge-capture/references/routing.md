# Storage routing per operation

Routing is decided **per operation** — search, read, write — not per session. A connected server may cover reads but not writes, or one vault but not another. Inspect the actual callable tool catalog, including MCP discovery interfaces, rather than assuming from a server or package name; cache successful discovery for the session and re-check after reconnect, configuration change or a relevant failure.

## Route precedence

For each operation, take the first available row:

| Route | Condition | Use |
|---|---|---|
| 1. Domain operations | The store's own knowledge API is callable, such as knowledge-mcp `knowledge_search`, `knowledge_read`, `knowledge_write` | Use it; the server owns format, validation, search and confirmation |
| 2. Generic record tools | No domain operation, but authorized list/search/read and conditional create/update primitives over the store | After fallback verification, supply missing semantics through the primitives; a discovered compatible writer skill can guide the operation |
| 3. Compatible files | No operations, but the destination is an authorized file store with a compatible layout | Only after the fallback verification below: direct bounded file reads and writes for that operation only, keeping the established layout |
| 4. Unsaved proposal | No permitted route for this operation | Keep the curated note in chat, marked unsaved, with the reason |

An MCP connection proves neither a function nor access to this store. A capability for one operation does not extend to another: partial capability routes partially. When the catalog serves search and read but not write, use the domain operations for exactly those and route the write independently through this table — a covered read is not evidence that the write, its namespace or its format is covered too.

Routes 2 and 3 are fallbacks for a missing capability, never alternatives to a refused one. Before using either, verify that it addresses the same store and namespace the provider owns, and that the write preserves what the provider owns: record format, identifiers, links and metadata, validation and index invariants, and the conditional-write and concurrency guarantees the store relies on. If that cannot be verified, or the verification fails, the operation has no permitted route: keep the note unsaved rather than writing through an unproven substitute.

## Denials and unknown outcomes

- An access denial ends that operation. It is not permission for route 2, route 3, another vault, or files that happen to be locally writable. Report the item unsaved with the denial, and ask for the needed permission or a correction.
- A write gate, confirmation requirement or preview protocol is followed as it is. A technical `confirm` flag transports an obtained approval; it is not the approval itself.
- An unknown write outcome — timeout, lost response — requires readback before any retry. Do not replay the mutation, and do not start a second writer to make sure.
- Never write files behind a server that owns the store's invariants, validation or index; a direct write cannot preserve what it cannot see.

## Destination resolution

Read [storage configuration and setup](storage-configuration.md), the single owner of explicit/project/global precedence, configuration fields, writer discovery and first-use setup. Its bundled copy keeps this skill independently installable. Configuration selects the destination but every operation still passes through the permission and compatibility routes above.

## First-use proposal

When no store resolves, start the shared setup dialogue. If no ready destination or chosen writer exists, `.mag/knowledge/` can be proposed for one-topic-per-file notes. No directory, note or persistent configuration exists before approval. A session-only choice expires with the session; a local/global choice persists only through an approved configuration change. Do not create an index, database or conversation mirror as part of capture. A refused write, invalid configured target or unknown outcome never triggers this proposal as a bypass.

## Writes and verification

Use conditional or exclusive-creation operations where supported; check the state you read before updating it, and preserve concurrent changes rather than overwriting them. After an executed write, read the note back and confirm bounded rediscovery with the note's distinctive terms. For an interrupted multi-note update, establish which notes actually persisted and reconcile within existing permission before another write. A preview is not a write; a confirmed write is not a verified one until read back.
