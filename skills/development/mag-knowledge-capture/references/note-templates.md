# Note templates

Defaults for generic Markdown stores and the `.mag/knowledge/` default. When the destination has an established format, metadata or naming convention, follow it instead; these templates fill the gap only. One topic per file; derive the filename from the topic, kebab-case, and keep it stable.

## Shared frontmatter

```yaml
format: mag-knowledge-note-v1
kind: domain
title: Charges are per started hour
scope: billing service, staging and production
status: active
updated: 2026-01-15T00:00:00Z
source: src/billing.py@41af2c3 verified by regression test
```

- `kind` is one of `domain`, `architecture`, `debugging`, `access`, `environment`, `workflow`.
- `source` cites evidence — file and revision, command output, owner decision — not a conversation.
- `status` is `active`, or `superseded` with an added `superseded-by: <file>` line, or `disputed` with the open conflict stated in the body. Superseded and disputed notes keep their content; they are resolved by an owner decision or newer verified evidence, never silently deleted.

## Bodies per kind

Keep each note to what a future task actually needs.

- **domain**: the rule or invariant in one or two sentences; the entities and terms it binds; boundary conditions; who owns the rule.
- **architecture**: the boundary or contract; consumers and providers; sequencing and format constraints; compatibility limits; where the contract is enforced (type, test, review).
- **debugging**: the observable symptom; the verified root cause with its evidence; the fix; the check that catches a regression; the environments where the cause applies.
- **access**: what the resource is; how to reach it — host, port, protocol, jump hosts; the required role or permission; where credentials live and how they rotate — never the credential value; quirks such as rate limits, timeouts or maintenance windows.
- **environment**: prerequisites and versions; environment variables by name, never by value; setup steps actually performed; known incompatibilities and their symptoms; the check that shows the setup works.
- **workflow**: when to use the procedure; the steps in order with decision points; the verification at the end; what breaks when a step is skipped.

## Provenance on change

When extending or superseding, append a dated provenance line with its evidence instead of rewriting the previous history. Do not copy secrets, tokens, or private conversation content into any field, including `source`.
