---
name: mag-commit-message
description: Generate repository-aligned commit-message text from the intended changes, repository instructions, recent history, branch metadata, and optional linked work-item context. Use when the user asks to write, improve, or validate a commit message, or when an authorized implementation phase needs message text. Never stage files, create a commit, push, or modify repository state.
---

# Commit message

Generate the message only. Preserve the repository's own convention instead of assuming a forge, issue tracker, or commit format.

## Determine the message scope

1. Read repository instructions that govern commits.
2. Inspect status and staged changes first. If files are staged, describe only the staged diff unless the user explicitly requests another scope.
3. If nothing is staged, inspect the relevant unstaged diff and state that assumption only when it could surprise the user.
4. If staged and unstaged changes overlap or the intended scope is ambiguous, ask one precise question before generating a misleading message.
5. Read a small recent-history sample to match subject, scope, identifier placement, capitalization, and body style.

Detect unrelated changes. Recommend splitting them when one truthful subject cannot describe the diff; do not invent a broad message to hide multiple concerns.

## Work-item context

Treat branch names, supplied identifiers, and linked issue/work-item URLs as optional evidence. Do not assume Jira, Azure Boards, GitHub Issues, or any other system.

When a URL is supplied and an applicable read-only provider is already available, read the title or acceptance context only if it materially clarifies intent. Use that material as private input; do not copy its URL, PRD/process narrative, or review history into the commit message. Never install, authenticate, or configure a provider. Preserve a compact identifier only when repository instructions, branch conventions, or recent history show where and how it belongs; never invent brackets, prefixes, or a ticket number.

## Format precedence

Use this order:

1. explicit user instruction;
2. repository commit rules;
3. dominant recent-history convention;
4. Conventional Commits as a portable fallback.

For the fallback:

```text
type(optional-scope): Optional-Identifier Imperative summary

- Essential durable behavior or contract outcome
- Additional distinct outcome, when present
```

Choose a scope that names the changed topic, not the repository. Use `!` or a breaking-change body only when the diff proves a compatibility break. Keep the subject concise, but follow a repository-specific length limit when one exists.

## Body decision gate

A subject-only message is acceptable only when the selected diff has one atomic
outcome and the subject fully communicates that outcome without ambiguity.
Repository history containing subject-only commits is evidence of style, not a
reason to omit useful behavioral context.

Include a concise body when any of these apply:

- the diff has two or more meaningful behavioral, contract, data, or
  operational outcomes;
- the subject necessarily compresses distinct concerns such as propagation and
  validation, persistence and migration, or configuration and fallback
  behavior;
- an amend combines the existing commit with staged follow-up changes;
- a compatibility boundary or durable reason matters but does not fit cleanly
  in the subject.

Use one to three bullets. Each bullet must describe a durable outcome,
invariant, or externally relevant effect—not filenames, implementation steps,
test counts, or review history. Do not repeat the subject in the body.

For an amend, generate the message from the complete future commit (parent to
index), not only from the newly staged delta.

Common fallback types: `feat`, `fix`, `test`, `docs`, `refactor`, `perf`, `build`, `ops`, `chore`, `style`.

## Artifact hygiene

Describe only the resulting behavior, contract, configuration, test, documentation, or operational change and its durable reason. Exclude:

- AI/model/agent attribution or co-author metadata;
- prompts, conversations, sessions, or implementation-plan narration;
- PRD, issue, task, or review URLs and copied process text;
- reviewer recommendations or phrases such as “as requested” and “following review feedback”;
- validation theater, exhaustive file lists, and unrelated changes already visible in Git.

A repository-required work-item identifier may remain when it directly identifies the change. Keep unrelated concerns in separate messages/commits.

## Output

Return one paste-ready message in a fenced text block. Add prose only for a material ambiguity, an atomicity warning, or an assumption about unstaged scope. Do not execute Git mutations.

Before returning, verify that:

- every claim is supported by the selected diff;
- every meaningful outcome is represented by either the subject or body;
- the message explains intent rather than listing filenames;
- a required body was not omitted merely because recent history uses
  subject-only commits.
