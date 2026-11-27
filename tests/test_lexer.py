import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import Token, TokenType, tokenize
from sloperator.runner import run_source


def types(source: str) -> list[TokenType]:
    return [token.type for token in tokenize(source)]


def test_keywords_operators_and_emoji():
    assert types("slop x = ✅ && !❌✨") == [
        TokenType.SLOP,
        TokenType.IDENTIFIER,
        TokenType.EQUAL,
        TokenType.TRUE,
        TokenType.AND,
        TokenType.BANG,
        TokenType.FALSE,
        TokenType.SPARKLES,
        TokenType.EOF,
    ]


def test_two_character_operators_are_greedy():
    assert types("== != <= >= ||") == [
        TokenType.EQUAL_EQUAL,
        TokenType.BANG_EQUAL,
        TokenType.LESS_EQUAL,
        TokenType.GREATER_EQUAL,
        TokenType.OR,
        TokenType.EOF,
    ]


def test_variation_selector_after_emoji_is_absorbed():
    tokens = tokenize("✅️✨️")
    assert [t.type for t in tokens] == [TokenType.TRUE, TokenType.SPARKLES, TokenType.EOF]
    assert tokens[0].lexeme == "✅️"


def test_number_literal_is_an_int():
    assert tokenize("9001")[0] == Token(TokenType.NUMBER, "9001", 9001, 1)


def test_identifier_may_contain_digits_after_the_first_character():
    # Digits were rejected after the first character, so `score2` tokenized as
    # `score` followed by the number `2` and failed to parse.
    assert tokenize("score2")[0] == Token(TokenType.IDENTIFIER, "score2", None, 1)


def test_identifier_cannot_start_with_a_digit():
    assert types("2score") == [TokenType.NUMBER, TokenType.IDENTIFIER, TokenType.EOF]


def test_identifiers_with_digits_run_end_to_end():
    result = run_source("slop score2 = 40✨\nscore2 = score2 + 2✨\nhallucinate(score2)✨")
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == "42\n"


def test_function_and_parameter_names_may_contain_digits():
    result = run_source("clanker add2(a1, b2) {\n    ship a1 + b2✨\n}\nhallucinate(add2(40, 2))✨")
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == "42\n"


def test_hallucinate_is_an_identifier_not_a_keyword():
    assert tokenize("hallucinate")[0].type is TokenType.IDENTIFIER


def test_loadbearing_is_a_keyword():
    assert tokenize("loadbearing")[0].type is TokenType.LOADBEARING


def test_string_may_contain_em_dash_and_opening_quote():
    assert tokenize("“x — “y”")[0].literal == "x — “y"


def test_string_escapes_are_decoded():
    assert tokenize("“a\\tb\\nc\\\\d\\”e”")[0].literal == "a\tb\nc\\d”e"


@pytest.mark.parametrize(
    ("source", "line", "message"),
    [
        ('"hi"', 1, "straight quotes are not supported, use “ and ” for strings"),
        ("x;", 1, "semicolons are not supported, end statements with ✨"),
        ("\n// nope", 2, "comments start with an em dash (—), not //"),
        ("– nope", 1, "'–' is an en dash, comments start with an em dash (—)"),
        ("x”", 1, "unexpected closing quote ” without an opening “"),
        ("“abc", 1, "unterminated string"),
        ("“abc\n”", 1, "unterminated string"),
        ("“a\\q”", 1, "unknown escape sequence '\\q'"),
        ("“a\\", 1, "unterminated string"),
        ("a & b", 1, "unexpected character '&', did you mean '&&'?"),
        ("a | b", 1, "unexpected character '|', did you mean '||'?"),
        ("x$", 1, "unexpected character '$'"),
    ],
)
def test_lexical_errors(source: str, line: int, message: str):
    with pytest.raises(LexicalError) as info:
        tokenize(source)
    assert info.value.line == line
    assert info.value.message == message
    assert str(info.value) == f"SlopLang lexical error at line {line}: {message}"


def test_error_after_comment_reports_the_following_line():
    # A comment used to consume its trailing newline without counting it,
    # so everything after a comment was reported one line early.
    with pytest.raises(LexicalError) as info:
        tokenize("— a comment\n@")
    assert info.value.line == 2
    assert info.value.message == "unexpected character '@'"


def test_tokens_after_comment_are_on_the_following_line():
    tokens = tokenize("— a comment\n✨")
    assert [(token.type, token.line) for token in tokens] == [
        (TokenType.SPARKLES, 2),
        (TokenType.EOF, 2),
    ]
