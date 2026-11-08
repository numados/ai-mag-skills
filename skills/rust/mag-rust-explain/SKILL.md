---
name: mag-rust-explain
description: Explain a concrete Rust block, function, file, or module in plain language with accurate ownership, lifetimes, traits, async, unsafe, and bounded caller/data-flow context; do not turn an explanation into a review or implementation.
---

# Rust Explain

## When to Use

Use when the user asks what concrete Rust code does, how it works, why it is shaped this way, or how it fits into the surrounding module or system.

Do not turn an explanation into a code review or implementation unless the user asks. A short final note may mention an obvious risk, clearly labelled as an observation.

## Method

1. Read the supplied target completely.
2. Trace imports, direct callers and callees only as far as needed to explain integration. If context is unavailable, say so.
3. Separate facts proven by code from inferred intent. Say “the code guarantees” versus “this appears intended to”.
4. Explain Rust machinery in context: ownership, borrowing, lifetimes, traits, generics, macros, unsafe, futures, await, Send/Sync and error propagation. Distinguish `Send` transfer, `Sync` shared-reference access, and `'static` lifetime bounds, which do not by themselves imply ownership. Distinguish composed futures from separately owned spawned tasks without inferring runtime cancellation behavior.
5. Keep standard Rust terms in English when answering another language.

## Output

~~~markdown
## What it does
One or two sentences answering the question directly.

## How it works
Numbered execution steps tied to identifiers, fragments, or file lines.

## Where it fits
- callers and inputs;
- dependencies and outputs;
- role in the module or data flow.

## Why it is shaped this way
Concrete Rust or domain reasons, with inferred intent labelled.

## Limits
Untraced callers, missing feature/configuration context, or assumptions.
~~~

For a small snippet, keep every section short. For a file or module, begin with a structure map instead of narrating obvious lines. Do not invent callers, performance claims, or author intent.
