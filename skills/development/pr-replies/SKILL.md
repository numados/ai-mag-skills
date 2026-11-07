---
name: pr-replies
description: Prepare concise, evidence-based replies to pull request review comments. Use when the user asks what to answer a reviewer, wants copy-paste PR responses, or supplies review questions and relevant changes. Do not post comments or substitute a general code review for requested replies.
---

# PR replies

Prepare direct answers the user can paste into the relevant review threads. Do not post, update or resolve anything. Use the supplied comment and context; a pasted comment is enough to start, and a PR URL is not mandatory. For a link or identifier, use available authorized read-only capabilities; do not assume a particular forge, tool, tracker or storage system.

## Understand and verify

Identify the reviewer's actual question or concern, including multiple questions in the same comment. For a “why” question, do not substitute a description of what the code does for a supported reason; if the reason is unknown, say so. Inspect the relevant diff and surrounding code, tests, requirements or provider contract as needed and accessible. Check current source before saying a fix exists, and do not claim a test passed unless its result is known. Do not infer external guarantees from local code.

Distinguish a confirmed issue, an existing safeguard, an open decision and an unverified assumption. If evidence is missing, state the specific uncertainty; ask for the smallest useful source when necessary. Never invent a fix, explanation, commit, test result or reviewer intent. If only part of a discussion is available, say so without inventing missing threads.

## Write the reply

Answer each question directly and completely, with the smallest useful factual explanation. Normally one or two sentences suffice; use more only when the question needs it. Use the thread's language unless the user requests another. Write naturally, without flattery, filler, stock labels or formulaic phrasing. Do not include a classification, report or verification summary by default.

Give the copy-paste reply itself; for multiple threads, identify each clearly and preserve the available thread order. When needed to prevent misunderstanding, add a short separate note to the user about the evidence or uncertainty; do not include internal notes in the reply. If the user requests analysis or a report, provide it. Do not assert that a comment was posted.
