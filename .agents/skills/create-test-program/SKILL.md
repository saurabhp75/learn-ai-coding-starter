---
name: Create Test Program
description: Add a SlopLang example program and an exact-output test for a language feature
---

# Create Test Program

Use this when adding or changing a SlopLang language feature and you need an executable example plus an exact-output regression test.

## Workflow

1. Read `docs/spec.md` for the feature and its edge cases. The spec is the source of truth; do not infer behavior from the implementation alone.
2. Check `examples/` for a similar program. Add a small, deterministic `examples/<feature>.slop` that demonstrates the feature and prints its result with `hallucinate`. Every `examples/*.slop` is executed by `tests/test_examples.py`, so it must exit 0, write no stderr, and print at least one line.
3. Add an exact-output case to `tests/test_example_outputs.py`. If that file does not exist, create it from this template:

```python
from pathlib import Path

import pytest

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"

CASES = [
    ("<feature>.slop", "expected output\n"),
]


@pytest.mark.parametrize(("filename", "expected"), CASES, ids=[case[0] for case in CASES])
def test_example_output(filename: str, expected: str):
    source = (EXAMPLES / filename).read_text(encoding="utf-8")
    result = run_source(source)
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == expected
```

   Add one `(filename, expected)` row per example. Include trailing newlines exactly as printed, and preserve SlopLang's Unicode output (`✅`, `❌`, smart quotes) verbatim.
4. Run the focused test and the project validation:

```bash
uv run pytest tests/test_example_outputs.py
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

Use `uv run ruff format` to fix formatting before rerunning the check.
