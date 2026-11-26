# AGENTS.md

Sloperator is a Python 3.13 interpreter for SlopLang, managed with `uv`.

## Project layout

- `sloperator.py` — CLI entrypoint; `--check` parses without executing
- `sloperator/lexer/`, `sloperator/parser/`, `sloperator/evaluator/` — pipeline stages
- `sloperator/runner.py` — wires the stages together; `run_source` is used by tests
- `tests/` — pytest suite
- `examples/` — `.slop` programs, all executed by the tests
- `playground/` — web playground
- `docs/spec.md` — language specification

## Validation

Run from the repo root:

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

Use `uv run ruff format` to fix formatting.

## Regression tests

Add a regression test whenever you fix a bug or change behavior. Put it in the matching `tests/test_*.py` file (`test_lexer`, `test_parser`, `test_evaluator`, `test_cli`, or `test_errors`); end-to-end cases can use `run_source`. Run comparison tests with `uv run pytest tests/test_comparisons.py`. If you add an example, `tests/test_examples.py` already runs every `examples/*.slop`, and it must exit cleanly with output.

## Language behavior

See [docs/spec.md](docs/spec.md) for the source of truth on SlopLang behavior, and update it when behavior changes.
