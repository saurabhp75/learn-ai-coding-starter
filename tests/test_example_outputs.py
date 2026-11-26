from pathlib import Path

import pytest

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"

CASES = [
    ("equality.slop", "✅\n❌\n❌\n✅\n❌\n✅\n❌\n✅\n❌\n"),
]


@pytest.mark.parametrize(("filename", "expected"), CASES, ids=[case[0] for case in CASES])
def test_example_output(filename: str, expected: str):
    source = (EXAMPLES / filename).read_text(encoding="utf-8")
    result = run_source(source)
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == expected
