from sloperator.runner import run_source


def test_comparison_binds_tighter_than_equality():
    result = run_source("hallucinate(1 < 2 == ✅)✨")
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == "✅\n"
