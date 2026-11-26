---
name: Create and Validate
description: Add a SlopLang example program with an exact-output test, then run the full validation suite
---

# Create and Validate

Use this when you need to add a language-feature example, its regression test, and verification in one pass.

## Workflow

1. Load the `create-test-program` skill with the skill tool and follow it to add the example and exact-output test.
2. Load the `validate` skill with the skill tool and follow it to run the project checks.
3. Report the outcome: which checks passed or failed. If a check failed and you changed files to fix it, rerun the `validate` skill before reporting.

## Rules

- Do not duplicate the referenced skills' instructions here. If they change, this skill still applies as written.
- Follow `AGENTS.md` and `docs/spec.md` for project layout and language behavior, as those skills direct.
