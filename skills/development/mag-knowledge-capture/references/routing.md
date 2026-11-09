# Storage routing per operation

Routing is decided **per operation** — search, read, write — not per session. A connected server may cover reads but not writes, or one vault but not another. Inspect the actual callable tool catalog, including MCP discovery interfaces, rather than assuming from a server or package name; cache successful discovery for the session and re-check after reconnect, configuration change or a relevant failure.

## Route precedence

For each operation, take the first available row:

| Route | Condition | Use |
|---|---|---|
| 1. Domain operations | The store's own knowledge API is callable, such as knowledge-mcp `knowledge_search`, `knowledge_read`, `knowledge_write` | Use it; the server owns format, validation, search and confirmation |
| 2. Generic record tools | No domain operation, but authorized list/search/read and conditional create/update primitives over the store | Only after the fallback verification below: supply the missing note semantics through the primitives, preserving the store's existing format, identifiers and links |
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

1. An explicit destination supplied by the user.
2. A configured store: provider configuration, a project `.mag-storage.json`, or knowledge-mcp vault routing. Reading a configuration is not permission to write it or to choose a repository-local alternative when it is absent.
3. The bounded default below, only when nothing above resolves.

The optional project `.mag-storage.json` is resolved on this skill's own terms, without depending on another skill's contract:

```json
{
  "root": "../engineering-memory",
  "knowledgeRoot": "knowledge",
  "taskRoot": "tasks"
}
```

Resolve `root` relative to the configuration file itself; an explicit absolute path is used as written. Resolve `knowledgeRoot` — the knowledge section root — inside the resolved `root`. `taskRoot` is the optional task section root, documented for completeness; this skill does not address task records. Section roots are relative subdirectories, not traversal paths or symlinks escaping the resolved store — a configuration that asks for either is not a usable destination. Preserve the layout the store already has instead of introducing a new one. The file's presence is routing information, not write authorization: every write still passes through the per-operation routes above.

## First-use-confirmed `.mag/knowledge/` default

This default is a deliberate policy of this skill, not a general permission: capture without any store loses verified knowledge when the session ends, and a minimal project-local default preserves it with the least ceremony — but only when **all** of these hold:

- No knowledge store is resolvable: MCP is genuinely absent or unreachable *without* a permission failure. A denial, gate or unknown outcome means stop that operation, never fall back to files.
- No destination was supplied or configured, and no other skill's contract already owns persistence for this request.
- At first use in a project, propose `.mag/knowledge/` in the project root, explain this policy and the one-note-per-topic layout, and obtain explicit user confirmation before creating the directory or any note.
- After confirmation, create only the needed note files. One topic per file, no index, no database, no mirror of the conversation.
- Reconfirm at the start of a new session unless the user has made the choice persistent. Repository policy that forbids the location wins; if forbidden, stay unsaved.

The default never overrides an established destination, and is never used to route around a refused write. Report its use explicitly: destination plus decision per note.

## Writes and verification

Use conditional or exclusive-creation operations where supported; check the state you read before updating it, and preserve concurrent changes rather than overwriting them. After an executed write, read the note back and confirm bounded rediscovery with the note's distinctive terms. For an interrupted multi-note update, establish which notes actually persisted and reconcile within existing permission before another write. A preview is not a write; a confirmed write is not a verified one until read back.
