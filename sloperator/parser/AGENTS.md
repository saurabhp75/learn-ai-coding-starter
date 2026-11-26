# Parser Conventions

Apply these in `sloperator/parser/parser.py`.

## One method per grammar rule

Name each parser method after the grammar rule it implements (`logic_or`, `logic_and`, `equality`, `comparison`, `term`, `factor`, `unary`, `call`, `primary`, ...), and keep that rule's logic in its method. Do not fold two rules into one method or invent ad-hoc helper names for a separate rule. If a rule must be split for line length, keep the split clearly subordinate (for example `factor` / `factor_tail`) rather than creating a second conceptual rule.

## Syntax errors describe the token that was found

Every syntax error must report what was found: `expected X, found '<lexeme>'`, or `..., but reached end of file` at EOF. Raise errors through `Parser.error` / `Parser.expect` so this suffix stays consistent; do not raise `SlopSyntaxError` directly with only an "expected ..." message. When changing parser messages, update `tests/test_parser.py` and `tests/test_errors.py`.
