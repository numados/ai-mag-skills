# Reconciliation with existing knowledge

Reconciliation prevents duplicate truth. Every candidate is compared with the store before any write; a candidate without a classification has no write.

## Search before write

For each candidate, search the resolved knowledge store first:

- Use the provider's own search operation when available; otherwise bounded filename and text searches rooted in the resolved store.
- Search by the claim's distinctive terms, not the conversation's wording. Two or three bounded queries per candidate; a missing hit bounds effort, it does not prove absence.
- Read the best candidates' scope, status and provenance before classifying. Do not classify from a title.

## Classification and action

| Relationship | Test | Action |
|---|---|---|
| new | No stored note makes this claim within this scope | Create the note |
| duplicate | A stored note already makes the same claim for the same scope | Skip creation; optionally refresh verification provenance or add a link — never a second copy |
| incomplete | A stored note covers part; the candidate adds verified detail | Extend the existing note in place, preserving its format and provenance |
| stale | A stored note is superseded by verified evidence within the same scope | Update or supersede through the provider's mechanism, citing the evidence; keep provenance and history |
| contradictory | Evidence conflicts with a stored claim, and scope and provenance cannot resolve it | Mark disputed: present both versions with evidence, ask the owner; do not silently rewrite |

- **Scope before substance.** An apparent contradiction is often two scopes — a different environment, version or component. Check the stored note's applicability fields first; a genuine scope difference means two notes, not a conflict.
- **Supersede needs verified evidence**, not merely a newer opinion. Same-scope replacement without verification is a dispute, not a refresh.
- **Use the destination's established supersede or retire mechanism.** Do not delete history. A generic store without such a mechanism keeps the old note with a superseded status and a link, per the note templates.
- **Unresolvable identity** — two stored notes could both be "the" note for a candidate — is a question for the owner, not a fork of truth.

## During read-only requests

Classification and dispute findings may be reported from reads alone. A read-only or chat-only request never performs the resulting write; the actions above execute only within established write authorization.
