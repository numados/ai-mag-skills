---
name: mag-knowledge-capture
description: Curate and persist reusable engineering knowledge during or after work. Apply when asked to capture, distill, or record what was learned — domain rules, architecture contracts, debugging root causes, access and resource discoveries, environment setup, or procedures — or at an explicit checkpoint composed by an outcome-owning skill. Triage candidates against task history, hypotheses, raw logs and secrets; search before writing; classify new, duplicate, incomplete, stale or contradictory; route each write through available knowledge MCP operations, authorized record tools, or compatible files; report captured, proposed, skipped, disputed and unsaved items. Not an always-on hook, a log archive, or permission to write.
compatibility: Reading and chat-only capture need no store; persisting notes needs an authorized knowledge destination such as MCP operations, record tools, or compatible files.
---

# Knowledge capture

Turn verified work products into a small set of maintained notes that make the next task faster. The skill decides **what is worth keeping** and **where it can go**. It does not archive conversations or logs, and its presence is not permission to write.

## Scope and invocation

- Trigger on an explicit capture request, or on a checkpoint step that an outcome-owning workflow (research, planning, execution, review, gap drill) composes into its instructions. There is no always-on hook: without an explicit request or a composed checkpoint step, do the ordinary work and do not run a capture pass.
- Do not use this skill for implementing or fixing code — the owning workflow stays in charge; for recovering or logging task state (`mag-task-history`, the task side of `mag-task-storage`); for authoring the project's own documentation when that documentation is the requested product; or for a pure knowledge lookup with nothing to capture.
- A chat-only, read-only or output-constrained request takes precedence: triage and reconcile through reads only, and keep every result in chat, reported unsaved — the constraint permits no route.
- When `mag-task-storage` is also present, the split is deterministic: every supplied, configured or provider-resolved destination routes through its access routing, honoring its denial, gate and unknown-outcome rules; this skill owns the capture triage and reconciliation. Use the bundled storage-configuration contract for local/global resolution and setup; `.mag/knowledge/` is only one first-use proposal when no destination resolves. A proposal is a chat question, not a write, and never overrides storage policy. Do not create a second store or fork records because two skills are installed.

## Capture pass

1. **Establish the checkpoint.** Identify the work products to mine — the change and its verification results, findings and confirmed decisions, the debugging path, setup and access work actually performed — plus the constraints, and whether knowledge writes are authorized at all. Authorization to do the work is not authorization to persist knowledge.
2. **Triage.** Read [triage](references/triage.md). Select candidates of these kinds: domain model, architecture and contracts, debugging, access and resources, environment and system setup, workflow and procedures. Exclude task history, transient hypotheses, raw logs and secrets. Grade the evidence and redact before anything leaves the session.
3. **Resolve and reconcile.** Read [storage configuration and setup](references/storage-configuration.md) to resolve the destination before searching; when persistence needs an unknown destination, start its setup dialogue. Keep candidates unsaved while that choice is unresolved. Read [reconciliation](references/reconciliation.md). For each candidate with a resolved store, search it first, then classify its relationship to existing notes — new, duplicate, incomplete, stale, contradictory — and choose create, extend, supersede, link, dispute or skip. No classification, no write.
4. **Prepare and persist per operation.** Apply the bundled [Obsidian note format](references/obsidian-note-format.md) to generic notes; `mag-obsidian-markdown`, when available, can prepare the same representation. Read [routing](references/routing.md) and use the destination and writer capabilities established during resolution. For each write, use ready knowledge MCP domain operations first; otherwise authorized generic record tools; otherwise a compatible authorized filesystem destination; otherwise keep the curated note in chat as unsaved. Honor access denials and unknown write outcomes; never bypass a write gate. For the knowledge-mcp provider, follow its [adapter](references/knowledge-mcp.md), including its two-phase preview and confirmation.
5. **Verify and report.** Read back each persisted note and confirm bounded rediscovery. Do not claim checks the provider did not perform.

[Knowledge content profiles](references/note-templates.md) own knowledge-specific fields and bodies; the shared format owns common properties and links. Hand supported metadata and content to the writer; an MCP may arrange the records itself. Preserve its accepted schema and report required fields that cannot be mapped rather than silently dropping them or writing behind the server.

## Report

Return one line per candidate and a short total, using exactly these decisions:

| Decision | Meaning |
|---|---|
| captured | Persisted and verified: note reference and the check performed. |
| proposed | A permitted, compatible route exists and the write is pending: a provider preview or write gate awaiting approval, or the first-use default awaiting the user's confirmation. |
| skipped | Not reusable knowledge, with the reason: task history, hypothesis, raw log, secret, or duplicate. |
| disputed | Contradicts a stored note and needs an owner decision; both versions are kept visible. |
| unsaved | Worth keeping, but no permitted or compatible route exists — denied, unavailable, or compatibility unverified — or the write was explicitly refused; the note stays in chat with the reason. |

State the destination for each persisted item, and never present a proposed note as saved. Do not include credentials, tokens or private session dumps in the report.

## Fallback boundary

When no destination resolves, enter the setup dialogue in [storage configuration](references/storage-configuration.md). A **first-use-confirmed `.mag/knowledge/` proposal** remains an option, not an automatically created default. Discover available writers, let the user choose the destination and local/global/session scope, and preview configuration before an approved change. Without a choice, keep the note unsaved in chat. A denial, write gate, invalid configured target or unknown write outcome does not authorize a replacement store.
