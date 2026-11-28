import pytest

from sloperator.errors import SlopSyntaxError
from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Assign, Binary, If, Literal


def parse_source(source: str):
    return parse(tokenize(source))


def test_compound_assignment_is_a_single_token():
    tokens = tokenize("x += 1✨")
    assert [token.type for token in tokens] == [
        TokenType.IDENTIFIER,
        TokenType.PLUS_EQUAL,
        TokenType.NUMBER,
        TokenType.SPARKLES,
        TokenType.EOF,
    ]
    assert tokens[1].lexeme == "+="


def test_plus_and_equal_are_separate_tokens_when_not_adjacent():
    assert [token.type for token in tokenize("+= + =")] == [
        TokenType.PLUS_EQUAL,
        TokenType.PLUS,
        TokenType.EQUAL,
        TokenType.EOF,
    ]


def test_compound_assignment_parses_as_a_statement():
    (statement,) = parse_source("n += 3 * 4✨")
    assert isinstance(statement, Assign)
    assert statement.name.lexeme == "n"
    assert statement.operator.type is TokenType.PLUS_EQUAL
    assert isinstance(statement.value, Binary)
    assert statement.value.operator.type is TokenType.STAR
    assert isinstance(statement.value.left, Literal) and statement.value.left.value == 3
    assert isinstance(statement.value.right, Literal) and statement.value.right.value == 4


def test_compound_assignment_accepts_a_string_value():
    (statement,) = parse_source("message += “hello”✨")
    assert isinstance(statement, Assign)
    assert statement.operator.type is TokenType.PLUS_EQUAL
    assert isinstance(statement.value, Literal) and statement.value.value == "hello"


def test_compound_assignment_parses_inside_a_block():
    (statement,) = parse_source("vibe ✅ { n += 1✨ }")
    assert isinstance(statement, If)
    (assignment,) = statement.then_branch.statements
    assert isinstance(assignment, Assign)
    assert assignment.operator.type is TokenType.PLUS_EQUAL


def test_compound_assignment_is_not_an_expression():
    with pytest.raises(SlopSyntaxError, match=r"expected '\)' after arguments, found '\+='"):
        parse_source("hallucinate(x += 1)✨")


def test_compound_assignment_requires_a_terminator():
    with pytest.raises(
        SlopSyntaxError, match=r"expected ✨ after assignment, but reached end of file"
    ):
        parse_source("x += 1")
