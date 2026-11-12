---
name: mag-branch
description: Create a git branch for a task following the Numados convention — base off the repo's default branch (master/main), and name bugfix/ or feature/ branches by tracker (Jira key only; Azure DevOps number plus kebab-case description). Use when the user asks to create, start, or check out a branch for a bug fix or feature, or provides a task/work item and a branch type. Reports the commands only; never creates, pushes, or mutates without authorization.
---

# Branch for a task

Produce one branch name and the exact commands to create it. Branch creation is
an approval-required operation — never run `git switch`, `git checkout`, or
`git push` yourself; report the commands and wait for authorization.

The new branch must be its own reference. Create it from the base branch with
`git switch -c <name> <base>` or `git checkout -b <name> <base>` so it has its
own ref and upstream later; never check out or move the base branch itself.

## 1. Determine the base branch

Default to the repository's integration branch (`master` or `main`) — use
whichever the repo actually uses, not a guess.

Establish it read-only:

1. Read the remote default: `git symbolic-ref refs/remotes/origin/HEAD`.
2. Otherwise, find the local branch that tracks `origin/master` or `origin/main`.
3. Otherwise, repository instructions naming the integration branch.

If both `master` and `main` exist or the default is ambiguous, ask which base to
use. Only branch from the current `HEAD` when the user explicitly asks.

## 2. Identify the tracker and task number

- **Jira** — a key such as `PROJ-123`.
- **Azure DevOps** — a numeric work item such as `181874`.

Take the tracker from the task reference the user gives, repository
instructions, or an explicit statement. Use the task number exactly as
supplied — never reformat, pad, or invent it.

## 3. Name the branch

| Type | Jira | Azure DevOps |
|------|------|--------------|
| Bug fix | `bugfix/<TASK>` | `bugfix/<TASK>-<short-description>` |
| Feature | `feature/<TASK>` | `feature/<TASK>-<short-description>` |

- `<TASK>` — the work-item identifier, unmodified.
- `<short-description>` — 2–5 lowercase hyphen-separated words naming the
  change's topic (not the repository), e.g. `editable-instrument-type`.
- Jira branches carry only the key — no description suffix.
- Azure DevOps branches always carry the kebab-case description suffix.

If the type is neither a clear bug fix nor a clear feature, ask rather than
guessing.

## 4. Output

Report, without executing:

1. the base branch and how it was determined;
2. the tracker, task number, and type;
3. the proposed branch name;
4. the exact creation command, e.g.:

```bash
git switch -c bugfix/181874-editable-instrument-type origin/master
```

Use `git checkout -b <name> <base>` when `git switch` is unavailable or the
base is a local branch.

Ask for authorization before creating or pushing the branch.
