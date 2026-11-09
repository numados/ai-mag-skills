---
name: mag-obsidian-markdown
description: Prepare or edit Obsidian-compatible Markdown notes with flat typed properties, useful tags and aliases, unambiguous internal links, and source-backed content. Use for Obsidian note authoring or conversion, frontmatter and wikilink repairs, or when a knowledge-capture or task-progress workflow delegates note formatting. Not a vault search, storage setup, task tracker, or automatic conversion of every Markdown file.
---

# Obsidian Markdown

Produce a readable note whose metadata and links other tools can interpret. Knowledge and task progress share a representation, not a lifecycle: the caller decides what belongs in the note, what is verified, and whether it can be saved.

No Obsidian application, plugin, MCP, or other skill is required. This skill owns formatting, not destination selection, knowledge triage, task sequencing, or permission to write.

## Prepare the note

1. **Resolve the output.** Identify the requested content, audience, note type, edit scope and output form. For a file-backed edit, read the file and relevant destination conventions first. Chat-only or output-only means return the Markdown without saving, discovering storage backends/configuration or starting setup. Read supplied sources and link targets only as permitted.
2. **Read the contract.** Apply [note format](references/note-format.md) for properties, links, readable structure and checks. Use the destination's existing schema when one exists; the common envelope fills gaps for new generic notes. Do not migrate a vault or add a second metadata schema to a provider-owned record.
3. **Keep the caller's meaning.** Preserve evidence, applicability, uncertainty, decisions and approval state. A progress observation is not automatically reusable knowledge; a formatted plan is not approved. Ask only when a missing fact can change meaning or a destination-specific choice.
4. **Build a small, connected note.** Use a specific title, stable property types and useful search terms. Link verified related notes with unambiguous targets. Do not create a web of speculative links or require every optional property and syntax feature.
5. **Deliver or hand off.** Return just the requested Markdown for output-only work. For authorized persistence, give the writer the note content, metadata, known identity and link context. The storage workflow selects the writer and handles confirmation, concurrency and readback; the writer can be the same agent using authorized file tools, not necessarily another skill or server. Formatting alone grants no storage access.
6. **Verify proportionately.** Check metadata, content and links using the contract. Report an unresolved target or unavailable parser/render check honestly. Claim a saved note only after the writer establishes it.

[Worked examples](references/examples.md) show a knowledge note and a task event with the same envelope. Their content and lifecycle fields are examples, not a replacement for the caller's schema.

## Composition with MAG

When available, `mag-knowledge-capture` owns candidate selection and reconciliation; `mag-task-storage` owns destination setup, access and task-record protocols. They can pass either knowledge or progress content to this skill. Their bundled format reference also supports standalone installations.

Use only the formatting needed by the request. A pure vault lookup stays with its reader; an ordinary README or source-code edit does not activate this skill merely because it contains Markdown or the word “task.”

## Result

Return the requested note or bounded edit. Add only material verification limits and, when persistence was requested, the actual saved/proposed/unsaved state supplied by the writer. Do not append storage setup or a formatting audit to a note-only answer.
