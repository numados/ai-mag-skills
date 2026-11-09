<!-- Generated from skills/development/mag-obsidian-markdown/references/note-format.md. Do not edit this copy; run python3 scripts/sync-skill-resources.py in the catalog repository. No source checkout is needed at runtime. -->

# Shared Obsidian note format

This reference owns Markdown representation and common property types for MAG knowledge and task notes. Content owners define knowledge kinds, task identity, lifecycle, event order and approval. Storage providers own their accepted schema and placement. The default below applies to new generic notes, not migrations or server-owned records.

## Select the schema

Read a relevant neighboring note, a template or the provider contract when available. Preserve existing fields, identifiers, filenames, dates and unknown properties outside the requested edit.

- Existing provider or vault schema: keep it; apply compatible Markdown improvements only within scope.
- New generic MAG note: use the common envelope below plus the content owner's fields.
- Provider accepts structured arguments rather than a complete note: map supported metadata and body to those arguments. Do not insert raw YAML into a title/content field that expects something else.
- A required property or relationship cannot survive the mapping: disclose the gap and ask before persisting. Do not silently discard it or create a second file behind the provider.

Obsidian compatibility does not promise a particular index or plugin will ingest the note. Do not add Dataview queries, Bases, CSS, hooks or `.obsidian/` configuration unless requested.

## Common envelope

For a new generic note, include `format`, `title`, `tags`, and the actual creation time when known. Add only useful supported fields. Mutable notes get `updated` when created or changed; immutable events keep their original creation time.

| Property | Type | Use |
|---|---|---|
| `format` | text | Content schema identifier supplied by its owner. Use `mag-note-v1` only when no content schema exists. |
| `title` | text | Specific topic, conclusion or task/event title. |
| `summary` | text | Optional short retrieval hint; no unsupported claim. |
| `created`, `updated` | date & time | New generic notes use ISO 8601, with timezone when known, such as `2026-01-15T09:30:00Z`. Preserve existing date conventions. |
| `tags` | list of text | A few meaningful labels from the destination's taxonomy. Values omit the leading `#`. |
| `aliases` | list of text | Real alternative names, acronyms or useful language variants. Omit when none are useful. |
| `repositories` | list of text | Stable repository/project names when relevant, not machine-local paths. |
| `scope` | text | Applicability such as component, environment and version. Put complex boundaries in the body. |
| `sources` | list of text | Evidence references: source paths with revision/heading, URLs or identified owner decisions. |
| `related` | list of text | Quoted, verified internal links. Omit unresolved targets or label them as open in the body. |

Keep a property's type stable across the vault. Obsidian assigns the type by property name, not by note. Do not change a list into a scalar because it has one item. Existing `source` text is not silently replaced with `sources`, and an existing profile's `kind`, `status` or task pointers keep their meaning.

### YAML rules

- Place one frontmatter block at the very start of the file, between lines containing `---`. A returned note has no assistant preamble before it.
- Use a flat mapping with unique keys. No nested objects, duplicate keys, YAML anchors, custom tags or prose blobs in properties.
- Use YAML lists for `tags`, `aliases`, `sources`, `related` and other list-valued fields. Use current keys `tags`, `aliases`, `cssclasses`; the singular legacy spellings are deprecated.
- Quote every wikilink in properties: `related: ["[[Knowledge/charge-policy]]"]`.
- Quote text containing `: `, ` #`, YAML metacharacters, or text that resembles a boolean, null, number or date. For example, a textual task sequence stays `sequence: "0003"`.
- Keep booleans and numbers typed only when the schema calls for them. Omit unknown optional values instead of inventing dates, IDs, approvals or evidence.
- Preserve provider-required nulls or types rather than “repairing” them into this default.

Do not create parallel copies of the same fact in several properties. Keep atomic metadata in properties and the actual explanation, evidence qualifications and decision context in the body.

## Tags and aliases

Reuse existing labels before adding new ones. Prefer a small stable vocabulary over spelling variants or a tag for every sentence. Obsidian tags are case-insensitive; lowercase kebab-case and optional `topic/subtopic` hierarchies are MAG defaults only when no convention exists.

Tags cannot contain spaces and cannot be entirely numeric. Letters, digits, underscores, hyphens and slashes are suitable portable characters; a digit-first tag such as `3d-rendering` is valid. Avoid punctuation-heavy labels even though Obsidian accepts additional Unicode characters.

Aliases name the same subject, not adjacent topics or invented keywords. Link to the actual file and use an alias as display text: `[[Knowledge/application-programming-interface|API]]`, not an unverified `[[API]]` target.

## Internal links and identity

Know the vault root before claiming a wikilink resolves. A storage section or task directory is not necessarily that root.

- Note: `[[Knowledge/charge-policy]]`.
- Display text: `[[Knowledge/charge-policy|Charge policy]]`.
- Heading: `[[Tasks/FEE-7/plan#Verification]]`.
- Block: `[[Tasks/FEE-7/research#^rounding-evidence]]`.
- Same note: `[[#Verification]]`.

Wikilink folder paths start at the **vault root** and use forward slashes. Repeated filenames such as `plan.md`, `research.md` and `_task_index.md` need vault-relative paths. Use a bare basename only when its resolution is verified and unambiguous.

If the vault root is unknown, ask when it is needed for a required wikilink. Otherwise use a verified relative Markdown link between known files, or leave an unresolved relationship as plain text. Obsidian also supports Markdown links. URL-encode spaces and other special characters in Markdown destinations; resolve those paths from the containing file.

Protocol fields such as `latest_iteration` and `previous` are not ordinary links. Preserve their owner-defined path base and scalar type. Add a readable body link when useful; do not replace a task-relative pointer with a wikilink.

Verify the target file and exact heading or block ID. Block IDs contain Latin letters, digits and hyphens. A paragraph ID follows a space, such as `Evidence checked. ^rounding-evidence`. A structured block's ID goes on a separate line after a blank line.

Choose a stable, descriptive filename using the destination's convention. For new generic notes, kebab-case is a default. Avoid characters that interfere with links or portable filenames, including `#`, `|`, `^`, `:`, brackets and path separators inside a filename. Check for collisions rather than overwriting a different note. Renames or backlink repairs outside the requested scope need separate authorization.

## Body

Lead with the useful conclusion or current state. Use informative headings and short paragraphs that remain understandable without a chat transcript.

- Knowledge: state the reusable claim, applicability, evidence and material uncertainty. Do not import task-history sections merely to share a format.
- Progress: state what actually changed, checks and results, unresolved decisions, blockers and next action. Preserve the task protocol's required sections and immutable history.
- Cite decisive evidence beside the claim with a source path/revision, heading, command/result or URL. A chat recollection is not independent verification.
- Keep confirmed facts, inference, proposals and owner decisions distinguishable. A successful formatting or write check proves neither domain correctness nor plan approval.
- Keep credentials, personal session dumps and raw logs out of properties and body. Hidden comments are not a safe place for secrets or unresolved decisions.

Use standard Markdown where it suffices. Do not require decorative syntax:

| Feature | Syntax and boundary |
|---|---|
| Callout | `> [!warning] Scope limit`, followed by quoted body lines. `+` expands, `-` collapses. Keep essential state visible. |
| Embed | `![[Knowledge/charge-policy#Rule]]`. Use only a verified, permitted target. Prefer a link when duplication is unnecessary. |
| Table link | Escape its display separator: `[[Knowledge/charge-policy\|Policy]]`. |
| Task list | `- [ ]` and `- [x]`. A checked box is not proof that the check ran. |
| Code | Use a language-tagged fence. Choose a longer outer fence when returning Markdown containing fences. |
| Highlight/comment | `==text==` and `%%comment%%`. Do not hide material uncertainty in comments. |

Do not put Markdown inside HTML and assume Obsidian renders it. Use optional diagrams, math or attachments only when they serve the requested note.

## Verification

Before delivery:

1. Parse the frontmatter with an available YAML parser; check unique keys and expected scalar/list types. Some parsers accept duplicate keys silently, so inspect those separately. If no parser is available, do a bounded manual check and report that limit when material; do not install one without approval.
2. Compare with the source: no lost qualifier, invented evidence, exposed secret, implicit approval or changed task outcome.
3. Resolve added internal targets and headings/blocks under the correct vault or file base. Exclude code examples from live-link checks. An unresolved intentional reference is not a verified link.
4. Check fences, tables and callouts as source. Use an available renderer only when useful and permitted; do not require or claim an Obsidian GUI check without one.
5. For persistence, the writer reads back the actual saved representation and performs bounded rediscovery using the store's supported tools. A preview or returned payload is not a saved note. Search infrastructure is outside this format contract.

## Sources

Syntax is based on official Obsidian documentation:
[Properties](https://help.obsidian.md/properties),
[Internal links](https://help.obsidian.md/links),
[Aliases](https://help.obsidian.md/aliases),
[Tags](https://help.obsidian.md/tags),
[Callouts](https://help.obsidian.md/callouts),
[Embeds](https://help.obsidian.md/embeds), and
[Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown).

These describe syntax, not MAG lifecycle rules or a guarantee that a third-party search tool understands every property.
