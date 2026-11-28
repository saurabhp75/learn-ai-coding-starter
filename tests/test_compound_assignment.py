import pytest

from sloperator.runner import run_source


def test_compound_assignment_adds_the_right_hand_expression_first():
    source = """slop n = 2✨
n += 3 * 4✨
hallucinate(n)✨
"""
    result = run_source(source)
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == "14\n"


def test_compound_assignment_joins_strings():
    source = """slop message = “hello”✨
message += “ world”✨
hallucinate(message)✨
"""
    result = run_source(source)
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == "hello world\n"


def test_compound_assignment_updates_the_nearest_shadowed_variable():
    source = """slop score = 1✨
{
    slop score = 2✨
    {
        score += 3✨
    }
    hallucinate(score)✨
}
hallucinate(score)✨
"""
    result = run_source(source)
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == "5\n1\n"


def test_right_hand_expression_is_evaluated_before_the_current_value_is_read():
    source = """slop n = 1✨
clanker bump() {
    n = 100✨
    ship 1✨
}
n += bump()✨
hallucinate(n)✨
"""
    result = run_source(source)
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == "101\n"


@pytest.mark.parametrize(
    ("source", "line", "message"),
    [
        ("missing += 1✨", 1, "undefined variable 'missing'"),
        (
            "loadbearing LIMIT = 10✨\nLIMIT += 1✨",
            2,
            "cannot assign to loadbearing 'LIMIT'",
        ),
        (
            "loadbearing LIMIT = 10✨\nLIMIT += “s”✨",
            2,
            "cannot assign to loadbearing 'LIMIT'",
        ),
        (
            "clanker f() {\n}\nf += 1✨",
            3,
            "cannot assign to immutable binding 'f'",
        ),
        (
            "slop x = 1✨\nx += “s”✨",
            2,
            "operands of '+=' must both be numbers or both be strings, got number and string",
        ),
        (
            "slop x = “s”✨\nx += 1✨",
            2,
            "operands of '+=' must both be numbers or both be strings, got string and number",
        ),
    ],
)
def test_compound_assignment_runtime_errors(source: str, line: int, message: str):
    result = run_source(source)
    assert result.stdout == ""
    assert result.stderr == f"SlopLang runtime error at line {line}: {message}\n"
    assert result.exit_code == 1
