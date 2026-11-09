# Worked examples

The fixture dates and repository names below illustrate formatting, not current facts. The vault root contains `Knowledge/` and `Tasks/`. Referenced notes must exist before these examples become live records.

## Knowledge note

A content workflow selected the claim, checked the evidence and chose its knowledge schema. The format adds typed retrieval properties without copying the task history.

````markdown
---
format: mag-knowledge-note-v1
kind: domain
title: "Charges use each started hour"
summary: "Positive durations round up before multiplication by the hourly rate."
tags:
  - billing/rounding
aliases:
  - Started-hour billing
scope: "Billing service, policy revision 41af2c3"
created: 2026-01-15T09:30:00Z
updated: 2026-01-15T09:30:00Z
status: active
sources:
  - "src/billing.py@41af2c3, charge function"
  - "tests/test_billing.py@41af2c3, 90-minute regression"
related:
  - "[[Tasks/FEE-7/research]]"
---

# Charges use each started hour

A positive duration rounds up to whole hours before multiplication by the rate.

## Applicability

This note describes the verified billing implementation at revision `41af2c3`.
It does not establish a tax policy or authorize a rate change.

## Evidence

The `charge` function and its 90-minute regression agree at that revision.
See [[Tasks/FEE-7/research|the originating research]] for task context.
````

## Task event

The task protocol, not the formatter, selected the event identity and sequence. Its `previous` pointer stays task-relative; the body uses a vault-relative wikilink. A later correction creates another event rather than editing this one.

````markdown
---
format: mag-task-event-v1
title: "FEE-7: rounding regression verified"
tags:
  - billing/rounding
task_id: billing/FEE-7
sequence: "0003"
stage: implementation
status: ready
created: 2026-01-15T10:00:00Z
previous: iterations/0002-planning.md
related:
  - "[[Tasks/FEE-7/plan]]"
---

# FEE-7: rounding regression verified

## Intent

Verify the approved started-hour change.

## Verified state

The 90-minute case passes at revision `41af2c3`.

## Changes

Updated the rounding implementation and its regression test.

## Verification

`python -m unittest tests.test_billing` passed. No deployment check ran.

## Handoff

Ready for review, not deployed. Next: review [[Tasks/FEE-7/plan#Verification]].

## Detail

Previous event: [[Tasks/FEE-7/iterations/0002-planning]].
````

## Existing provider schema

If a server owns `numados-task-iteration-v1`, its `iteration`, `stage`, `previous` and date types stay unchanged. Submit its accepted event arguments and format only the supported Markdown body. Do not replace its format with `mag-task-event-v1`, allocate its sequence, or add unsupported fields.

If an existing vault uses a relative Markdown link whose destination is `../plan.md`, preserve that valid link. Wikilinks are useful, not a reason to migrate compatible notes.
