# Access and capability routing

## Resolve one store

Use an explicit user-supplied destination first, then the applicable provider's project mapping/configuration, or an existing project `.mag-storage.json`. A filename match or a writable directory alone is not an authorized destination. If explicit and configured locations conflict, explain the conflict; do not silently fork the record.

The optional project configuration for generic record/file stores is:

```json
{
  "root": "../engineering-memory",
  "knowledgeRoot": "knowledge",
  "taskRoot": "tasks"
}
```

Resolve `root` relative to this configuration file (or use its explicit absolute path); resolve the two section roots inside it. They are relative subdirectories, not traversal paths or symlinks escaping the resolved store. Preserve an established layout. For a new, explicitly chosen store without a layout, these two subdirectories are defaults, created only as needed and with write permission. Reading a configuration is not permission to create or edit it. Missing configuration is not permission to choose a repository-local fallback. Knowledge and task access can be configured independently by a provider; an unavailable section need not block a permitted operation on the other.

Resolve the task's store-wide identity and repository/project association. Do not pick a bare ticket match shared by several namespaces. Derive a stable slug from a task without an ID only when creating its authorized record; validate it as a path component, and check existing records before creating another. Ask when identity or destination remains materially ambiguous.

## Discover capabilities per operation

Inspect the harness's actual callable tool catalog, including a supported discovery interface for hidden MCP tools. Read applicable schemas and make a bounded read-only readiness check when needed. A skill file, installed server package or MCP connection alone proves neither a function nor access to this store. Cache successful discovery for the session; reconsider after reconnect, changed configuration or a relevant failure.

Route knowledge search/read/write and task recover/record independently:

| Available capability for this operation | Route |
|---|---|
| Ready domain operation, such as a task-state or knowledge-note API | Use it; let the server own its format, event sequencing, validation and supported search. |
| No suitable domain operation, but authorized generic record/list/search/read/write primitives | Supply only the missing knowledge or task semantics through those primitives in the same store. |
| Missing operation and direct access to compatible, authorized store files | Use the files for that operation only. |
| No permitted compatible route | Report unavailable/unsaved state; retain the useful chat result. |

Prefer a provider's own search over an independent index of the same store. Without it, use bounded filename/text searches rooted in the resolved files. Generic search capability does not imply a task-recording API. Likewise, task recording does not prove knowledge-writing support. Discover the primitives' conditional-write and consistency guarantees rather than assuming them.

## Preserve one source of truth

Before using another route, establish that it addresses the same data, namespace and record format. Preserve provider-owned schemas, IDs, metadata, event order and link conventions. Do not create a second local history because the MCP is missing a function, or assume a generic MAG index is accepted by a newly connected provider. If format compatibility is unproven, stop the affected write and ask or inspect the provider contract; migration needs separate authorization.

Fallback fills a missing capability. It does not bypass an access denial, write gate, confirmation requirement or other policy, even when files are locally writable. A failed readiness check is not by itself evidence that bypass is permitted. For an availability failure, use another route only after verifying permissions, compatibility and the outcome of any in-flight write. An unknown commit outcome requires readback before another mutation. If the server enforces invariants or indexes that a direct write cannot preserve, do not write files behind it.

## Writes and partial failure

Use established user/workflow permission scoped to the destination and operation; ask when it is missing. A configured write gate is a technical capability, not blanket approval. Research/planning may write their authorized memory records, not product files or trackers. Do not commit, push, publish, delete or rewrite repository history as part of storage.

Use conditional updates or exclusive creation where supported. Before updating a projection, compare the version/state read; preserve concurrent changes. If overlapping writers cannot be excluded or coordinated, stop rather than claiming race-free persistence. Do not allocate event IDs client-side when a domain API owns them.

After an interrupted multi-record update, identify which records actually persisted. Report a stale projection or partial event explicitly, reconcile only within existing write permission, and retain earlier events. A task is not saved in full merely because one file was written.
