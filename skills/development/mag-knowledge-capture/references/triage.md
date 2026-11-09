# Capture triage

Triage selects the few claims that will shorten future work. It is a curation decision, not a filter over text volume: a long transcript can yield one note, and a small diff can yield three.

## Candidate sources

Mine these, in proportion to the checkpoint:

- the verified change itself and its review or verification results;
- research findings and confirmed decisions, with the evidence that supports them;
- the debugging path: symptom, hypotheses that were eliminated, verified root cause, the fix and its check;
- setup and access work actually performed — what was required, what failed, what unblocked it;
- procedures that measurably sped up the work, at least once performed.

## Knowledge kinds and the bar for capture

| Kind | Captures | Bar |
|---|---|---|
| Domain model | Entities, invariants, business rules, terminology, lifecycle rules | An owner decision or a verified rule — not a guess about intent |
| Architecture and contracts | Component boundaries, interface and data contracts, sequencing, ownership, compatibility constraints | Stable enough to outlive this change — not internal style preference |
| Debugging | Verified symptom, root cause, fix, regression check; environment quirks that cost real time | Root cause verified — not the first plausible hypothesis |
| Access and resources | How to reach systems, required roles, credential location and rotation, rate limits, quirks | The route was actually used successfully |
| Environment and system setup | Toolchain and version requirements, environment variable names, provisioning steps, known incompatibilities | Verified by a working setup |
| Workflow and procedures | Repeatable procedures, verification recipes, release or incident steps | Performed at least once and reusable beyond this task |

## Exclusions, with reasons

- **Task history and events** — progress, plan status, assignments, approvals. They belong in the task record or the owning workflow, not in knowledge.
- **Transient hypotheses and unverified claims** — keep them with their uncertainty in the task record or chat. Capture only after verification; store an explicitly marked proposal only when explicitly requested.
- **Raw logs, transcripts and dumps** — mine them for conclusions; store the distilled claim plus a pointer to where the raw material lives, never the material itself.
- **Secrets** — never store credential, token or key values, credentialed URLs, or private personal data. Store where the secret lives and how it rotates. If reliable redaction is not possible, skip the item and say so.
- **One-off session state** — anything whose value dies with this task.

Repository or user policy that marks material private wins over any capture value.

## Evidence grades

- **verified** — checked against current source or a live system, with a citable source: file and revision, command output, owner decision.
- **recorded** — a stored claim from a provider, with its provenance kept and its currentness unverified.
- **reported** — a participant statement without independent verification; capture only with the uncertainty explicit, or as a marked proposal.

The grade travels with the note into its provenance fields.

## Volume discipline

Prefer skip-and-mention when in doubt between capturing and skipping. A chat mention costs nothing; a wrong stored note costs future trust and must later be reconciled by someone. Ten good checkpoint notes in a project is a healthy ceiling, not a target to reach.
