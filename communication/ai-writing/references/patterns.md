# Pattern reference

Use this reference for a full assessment, a substantive rewrite, or when the
short workflow needs a more careful distinction. These are prompts for
editorial checking, not a detector and not a blacklist.

## Content and reasoning

- **Inflated significance or legacy:** ordinary facts followed by claims about
  a pivotal moment, broader movement, enduring legacy, universal debate, or
  evolving landscape. Keep a broader claim only when a supplied or verified
  source makes the connection specific.
- **Empty analysis:** clauses such as “highlighting its importance,”
  “demonstrating its impact,” “fostering connection,” or “underscoring the
  significance” that add no new fact. Delete them or state the concrete
  consequence.
- **Promotional framing:** “renowned,” “vibrant,” “groundbreaking,” “rich
  heritage,” “offers a diverse array,” and similar praise presented as fact.
  Replace it with observable facts or attribute the praise when appropriate.
- **Vague actors and relationships:** “experts say,” “observers note,”
  “widely regarded,” “associated with,” and “in connection with” when the
  specific person, source, action, or relationship is known.
- **Generic future/legacy endings:** “despite its success...” followed by
  unsourced challenges, forecasts, or hopeful conclusions added to complete a
  standard outline.
- **One-sided framing:** inspect omissions, unequal standards, and source
  quality as content problems. Do not attribute bias to AI from tone alone.

## Language

Check clusters and density, not isolated words:

- repeated fashionable abstractions such as “crucial,” “pivotal,” “robust,”
  “intricate,” “delve,” “showcase,” “tapestry,” “testament,” “underscore,”
  “foster,” “enhance,” “landscape,” or their local-language equivalents;
- indirect substitutes for simple verbs (`serves as`, `stands as`, `boasts`,
  `features`, `offers` instead of `is`, `has`, or a concrete action);
- repeated “not only ... but also ...”, “not just ... but ...”, or dramatic
  contrast where the contrast is not necessary;
- rule-of-three adjective or noun strings that make thin material look full;
- elegant variation or stiff synonyms that hide the same referent; prefer a
  precise repeated noun and a direct verb when clearer;
- excessive qualifiers or intensifiers only when they weaken or obscure a
  supported claim. Qualifiers are not AI evidence by themselves.

## Structure and presentation

- generic headings or section order that do not fit the material;
- redundant title, introduction, “in summary,” or conclusion;
- excessive bold inline headers, decorative emoji, or small tables that make
  copy-ready prose look like a chatbot handout;
- lists converted to prose when items are truly discrete, or prose forced into
  a list when relationships and sequence matter. Keep the structure that
  helps the destination reader;
- wrong heading case or invalid markup for the destination medium.

## Artifacts and references

Verify directly where possible:

- placeholders (`[Name]`, `URL`, `INSERT_SOURCE_URL`, `XX-XX`), exposed prompt
  text, assistant preambles, abrupt cut-offs, and unfinished delimiters;
- leaked citation/search internals such as `turn0search0`, `oaicite`,
  `contentReference`, `【...†source】`, or `[cite_start]`;
- Markdown pasted into wikitext, malformed JSON/Markdown/HTML, broken links,
  invalid DOI/ISBN, unrelated DOI metadata, unused named references, and
  tracking parameters in a destination where canonical URLs are expected.

A broken link or invalid identifier is a confirmed technical defect when
verified, but it is not proof of AI authorship. Never fabricate a replacement
source.

## Context and counterevidence

A sudden change from an author's established style, metadata history, or text
dating can be relevant context only when that evidence is available. It cannot
be inferred from the passage. Do not report perfect grammar, one em dash,
one transition word, curly quotes, formal prose, an ordinary list, or a single
awkward sentence as an AI sign. A person can explain or correct an unusual
choice; that is useful context, not proof either way.

## Editing priorities

1. Preserve facts, scope, uncertainty, voice, and required disclosure.
2. Remove unsupported inference and generic praise.
3. Replace vague claims with concrete actors, actions, dates, and relationships
   already supported by the supplied material.
4. Fit structure and tone to the recipient and destination.
5. Simplify without flattening personality or adding artificial mistakes.
6. Validate the final format and reread it independently of the original.
