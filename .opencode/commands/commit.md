---
description: Review the diff, commit all changes with the given message, then rebase onto origin/main
---

Review the pending changes, commit them, and sync with `main`.

Message: $ARGUMENTS

## Steps

1. Inspect `git status --short` and `git diff HEAD`. Read any untracked files listed by `git status` as well.
2. Review the changes for problems before staging: leftover debug code, stray files, unrelated edits, secrets or `.env` files. If something looks accidental or out of scope, stop and ask instead of committing it.
3. If there are no changes, say so and stop.
4. If $ARGUMENTS is empty, propose a concise commit message based on the diff and ask for confirmation instead of inventing one.
5. Stage and commit everything: `git add -A` then `git commit -m "$ARGUMENTS"`. Pass the message as a single quoted argument so it is not split by the shell.
6. Run `git pull --rebase origin main`. If the rebase hits conflicts, do not force or abort silently: list the conflicted files, explain the conflicting hunks, and ask how to resolve them.
7. Report the new commit (`git log --oneline -1`) and the final `git status --short`.

Do not push. Only fetch and rebase as specified.
