# Task records

A task record answers what was requested, what is known or decided, what was done and checked, what is blocked and what comes next. It is not the whole conversation and is separate from reusable knowledge.

## Recover

Use a ready domain task-status/recovery operation first. Otherwise locate the task in the resolved namespace and read its current index, latest meaningful event and only the linked research, plan, findings or earlier events needed now. Check source when current behavior matters.

If the index or latest event is missing, stale or contradictory, disclose the gap and inspect bounded linked records or recent event names to recover what is evidenced. Do not repair during a read-only request, infer approval from a filename or claim that history proves present behavior.

## Record a meaningful step

Use a ready domain task operation, providing the actual outcome, not a manufactured file layout or sequence. Through lower-level record tools/files, preserve the existing protocol and record the equivalent of:

- **Current index:** stable task identity and repository/project association, current stage/outcome, phase if applicable, latest event, short current state, next action, blocker and links to existing detail.
- **Current artifacts:** compact research, current proposed/approved plan, and findings only when relevant. Preserve evidence versus inference, scope authority and explicit approval state. Include analysed source revision or an honest currentness limit where useful.
- **Append-only events:** one per meaningful research pass, plan revision, implementation phase or review/correction cycle. Record intent, verified state, actual changes, decision changes and their authority, checks/results or unrun checks, blockers, next action and previous-event/detail links.

Correct conclusions with a later event, not an edited old event. Events must retain enough material decision/change context to understand revisions even after current artifacts change; this is not a guarantee of full historical snapshots. An unapproved plan stays proposed. Completion requires evidence for the requested checks, not merely a successful record write.

## Default only for a new generic store

Knowledge and task progress use the bundled [Obsidian note format](obsidian-note-format.md) for their representation, but retain different content and lifecycle rules. For new generic task files, combine its common envelope with the task fields below. Preserve existing/server-owned schemas and events; do not retroactively add properties or convert history merely to share a format.

Use this layout only when no provider or existing record protocol owns it:

```text
<taskRoot>/<task-id>/
  _task_index.md
  research.md
  plan.md
  remarks.md             # only when findings exist
  iterations/
    0001-research.md
    0002-planning.md
```

The index adds these task fields to the shared envelope:

```yaml
format: mag-task-index-v1
task_id: <store-wide-id>
stage: research
status: active
current_phase: null
latest_iteration: iterations/0001-research.md
```

Its body contains current state, next action, blocker and existing artifact links. Include the repository/project association through the shared envelope. Resolve `latest_iteration` and each event's `previous` from the task directory; they remain plain protocol paths. Resolve ordinary Markdown links from their containing file, and wikilinks from the actual vault root. Repeated task filenames require unambiguous vault-relative wikilinks, not an assumed `[[plan]]` target. `stage` describes the work; `status` is its outcome (`active`, `ready`, `blocked`, `done`), not permission to execute a plan.

Each new event uses the common envelope plus `format: mag-task-event-v1`, the same `task_id`, a quoted zero-padded text `sequence`, `stage`, `status` and `previous` pointer (null for the first), plus the event content above. Its creation timestamp is immutable; a later correction is another event, not an `updated` rewrite. Use exclusive creation and the existing ordering; do not overwrite a colliding event. A domain server may own a different format and sequencing; do not add these tags to its records.

## Persist and verify

For primitive/file writes, first establish non-conflicting ownership or supported conditional operations. Update needed current artifacts, create the event, then update the index to reference records that exist. This order is not a transaction: if any part fails, read back and report/reconcile partial state before another write. Check the old index before replacing it; never overwrite a concurrent writer. If safe coordination is unavailable, stop the affected write.

Read back changed records, verify parseable metadata, matching identity, latest/previous/detail links and bounded rediscovery by task ID within its namespace. With domain APIs, rely only on verification their actual contract/results establish, and perform the missing authorized reads. Report partial writes and unsupported checks rather than claiming a complete handoff.
