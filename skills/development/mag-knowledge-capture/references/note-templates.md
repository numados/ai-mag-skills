# Knowledge content profiles

These profiles own knowledge-specific content and lifecycle fields. Apply the bundled [Obsidian note format](obsidian-note-format.md) for the common envelope, property types, filenames and links. Combine that envelope with the profile below for a new generic note. Preserve an established provider/vault schema; this is not a migration instruction. Keep one reusable topic per file.

## Knowledge-specific fields

```yaml
format: mag-knowledge-note-v1
kind: domain
status: active
```

- `kind` is one of `domain`, `architecture`, `debugging`, `access`, `environment`, `workflow`.
- The shared envelope's `sources` list cites evidence, not a conversation. Preserve an existing `source` text field rather than renaming it or maintaining a duplicate provenance field.
- `status` is `active`, or `superseded` with an added `superseded-by` text property pointing to the replacement, or `disputed` with the open conflict stated in the body. Preserve an existing replacement-pointer convention; a new generic note uses a quoted, verified vault-relative wikilink when the vault base is known. Superseded and disputed notes keep their content; they are resolved by an owner decision or newer verified evidence, never silently deleted.

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
