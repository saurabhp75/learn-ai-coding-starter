# AGENTS.md

Sloperator is a Python 3.13 tree-walking interpreter for SlopLang. `docs/spec.md` is the language source of truth; the README only links to it. Update the spec when language behavior changes.

## Commands

Run a program, or check syntax without executing:

```bash
uv run sloperator.py examples/fib.slop
uv run sloperator.py --check examples/fib.slop
```

Validate with all four checks (fix formatting first with `uv run ruff format`):

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

A single test: `uv run pytest tests/test_evaluator.py::test_name`. The repo's `validate` skill runs only pytest, format check, and lint; `ty check` also passes but is easy to forget.

Playground: `uv run playground/server.py` serves <http://localhost:8080>. It runs submissions as subprocesses and appends JSON results to repo-root `logs/runs.log`.

## Pipeline

`sloperator.py` → `sloperator/runner.py` → lexer (`scanner.py`) → parser (`parser.py`) → evaluator (`interpreter.py`). Tests use `run_source` from `runner.py`.

- `run_program` raises Python's recursion limit to 20,000; the interpreter separately caps SlopLang call depth at 500 and reports `stack overflow`.
- Errors are `SlopError` subclasses printed as `SlopLang <kind> error at line N: message`. Exit codes: 0 success, 1 language error, 2 usage/read failure. Output before a runtime error stays on stdout; never leak a Python traceback.
- `hallucinate` is a global `Builtin` bound by the interpreter, not a lexer keyword. Only `slop`, `loadbearing`, `clanker`, `vibe`, `nah`, `ralph`, and `ship` are keywords.

## Source Gotchas

- `.slop` files and test source strings need `“ ”` strings, `—` comments, `✨` terminators, and `✅`/`❌` booleans.
- Straight quotes, `;`, and the en dash `–` are deliberate lexical errors with guidance messages. Do not "correct" them in tests or examples.
- `tests/test_examples.py` runs every `examples/*.slop` and requires zero stderr, exit code 0, and non-empty stdout. New examples must print something.

## Repo-Specific Tooling

- `.ignore` lists `uv.lock` so search tools skip it while Git still tracks it; do not move it to `.gitignore`.
- Playground logs live in root `logs/` and are ignored by both Git and the OpenCode watcher.
- `.opencode/plugins/run-slop.ts` provides the `run_slop` tool; `.opencode/agents/review.md` is a read-only reviewer.
