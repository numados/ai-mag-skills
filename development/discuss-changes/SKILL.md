---
name: discuss-changes
description: Explain planned or implemented changes interactively, one understandable idea at a time. Use when the user wants to discuss a change slowly, understand its purpose or flow, or continue an explanation step by step. Do not force pauses when the user requests a complete explanation.
---

# Discuss changes

Help an intelligent reader unfamiliar with this code or domain understand what changes, why, and how. Use the user's language and familiar words; do not talk down to them.

## Establish the facts

Use the supplied task, code, diff, plan and conversation. If the subject is unclear, ask one focused question. Read the relevant requirements and source before making claims; distinguish a plan from implemented, deployed or observed behavior. If essential evidence is unavailable, identify the gap and continue with what is supported. Do not invent business rules, routes or code.

## Discuss at the user's pace

- Explain one idea per reply, then stop. Start with the problem and a small before/after example when useful; introduce technical details only as needed.
- Treat `+`, “next”, or an equivalent continuation signal as a request for the next idea, not authorization to modify anything.
- Answer interruptions directly. Resume the prior thread only on a later continuation signal. If the user is confused, explain more simply or use a different concrete example.
- Define necessary unfamiliar terms in context. Use a short real, cited excerpt or clearly labelled hypothetical example only when it helps this idea. Explain what the excerpt means, not every line of syntax.
- Avoid repeated agendas, quizzes, forced headings and unnecessary jargon. If the user asks for a complete explanation, provide it rather than imposing pauses.

Distinguish evidence from assumptions. Recheck challenged claims and correct mistakes plainly. Discussion alone does not authorize code, record or remote changes.
