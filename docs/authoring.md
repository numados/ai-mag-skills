# Skill authoring guide

This repository follows the portable Agent Skills format. Every published skill
is an independently installable directory with a `SKILL.md` file.

## Directory layout

```text
skills/<category>/<skill-name>/
├── SKILL.md                 # Required metadata and instructions
├── LICENSE                  # Generated copy of the repository license
├── references/              # Optional detail loaded only when needed
├── scripts/                 # Optional deterministic helpers
└── assets/                  # Optional templates, fixtures, and static files
```

Do not add `scripts/` or `assets/` for symmetry. Add them only when the skill
has a concrete helper, template, fixture, or other reusable file that belongs
to the skill.

## Frontmatter

Required fields:

```yaml
---
name: mag-example
description: Explain what the skill does and when to use it.
---
```

`name` must be lowercase, use hyphens, and start with `mag-`. The description
is the discovery trigger: state the outcome, the situations that activate the
skill, and important boundaries.

Supported optional fields:

```yaml
license: Complete terms in LICENSE.txt
compatibility: Requires a host with filesystem access and optional MCP support.
metadata:
  stability: stable
  supported-harnesses: pi, claude-code, codex
```

Use `compatibility` only for real environment requirements. Use `metadata` for
small string-valued facts that are not already owned by the directory layout,
plugin manifest, or changelog. Keep metadata flat.

Do not add `category`, `version`, `author`, or `updated` to individual skills
unless the repository adopts an explicit owner for that data. Do not use
harness-specific `allowed-tools` in portable skills without a documented
compatibility policy.

The catalog validator intentionally supports a strict YAML subset. It rejects
unknown top-level fields, nested metadata, collections, non-string scalar
values, unquoted numeric, timestamp, boolean, or empty metadata values, empty
`metadata:`, tab indentation, duplicate keys, and malformed frontmatter.

A real client parses the same frontmatter with a full YAML parser, so the value
must also be valid and unambiguous YAML. Quote a value that contains `: `, that
contains ` #` (a YAML comment start), or that looks like a number, timestamp, or
boolean:

```yaml
compatibility: "Optional: requires a configured classifier provider."
description: 'Tracks upstream issue #123 without truncation.'
metadata:
  priority: '1'
```

Every limit applies to the parsed value. A clip-chomped block scalar (`>`) keeps
a trailing newline, so use `>-` when a description sits exactly at the limit.

## Body and progressive disclosure

Keep `SKILL.md` focused on the workflow the agent needs after activation:

- explain when the skill applies and when it does not;
- give actionable steps and the reason for important constraints;
- define the expected output and verification;
- link to a local reference only when the detail is needed for that path.

Put long version-specific guidance, large examples, and specialist reference
material in `references/`. Keep each reference self-contained and link to it
from `SKILL.md`. Do not make one skill depend on another skill's private files.

## Scripts and assets

Use `scripts/` for deterministic or repetitive operations that should not be
recreated by the model on every invocation. Scripts must have a clear input,
output, and failure behavior, and must not expand the skill's authorization.

Use `assets/` for files consumed by the skill's output or workflow, such as
templates, schemas, fixtures, sample documents, or static resources. Do not
copy general documentation into `assets/`; use `references/` instead.

## Verification

Add or update the skill's evals under `evals/<category>/<skill-name>/`. Keep
evaluation fixtures outside the installable skill directory. Run:

```bash
./scripts/check-skills.sh
```

The check validates frontmatter, the catalog, manifests, local references,
licenses, and evaluation metadata. Behavioral evaluation results are evidence
about a skill's behavior; structural validation alone is not a behavioral
quality guarantee.

Because a client that cannot parse the frontmatter skips the skill and still
exits successfully, verify discovery against a real client before publishing:

```bash
npx skills@latest add ./ --list | python3 scripts/check_discovery.py
```

That command fails when a published skill is missing from the client's listing
or when the client reports a skipped file. It needs network access, so CI runs
it separately from `./scripts/check-skills.sh`.
