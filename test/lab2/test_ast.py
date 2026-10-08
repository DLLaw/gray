import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from expr import Binary, Grouping, Literal, Unary
from gray_token import Token
from token_type import TokenType


def operator(token_type, lexeme):
    return Token(token_type, lexeme, None, 1)


def main():
    tests = [
        (
            "Nested arithmetic, unary minus, and grouping",
            Binary(
                Unary(operator(TokenType.MINUS, "-"), Literal(123)),
                operator(TokenType.STAR, "*"),
                Grouping(Literal(45.67)),
            ),
            "(* (- 123) (group 45.67))",
        ),
        (
            "Addition, subtraction, and division",
            Binary(
                Binary(
                    Literal(10),
                    operator(TokenType.PLUS, "+"),
                    Literal(2),
                ),
                operator(TokenType.SLASH, "/"),
                Grouping(
                    Binary(
                        Literal(8),
                        operator(TokenType.MINUS, "-"),
                        Literal(4),
                    )
                ),
            ),
            "(/ (+ 10 2) (group (- 8 4)))",
        ),
        (
            "Logical operators, negation, and booleans",
            Binary(
                Unary(operator(TokenType.BANG, "!"), Literal(False)),
                operator(TokenType.AND, "and"),
                Grouping(
                    Binary(
                        Literal(True),
                        operator(TokenType.OR, "or"),
                        Literal(False),
                    )
                ),
            ),
            "(and (! false) (group (or true false)))",
        ),
        (
            "String equality",
            Binary(
                Literal("hello"),
                operator(TokenType.EQUAL_EQUAL, "=="),
                Literal("hello"),
            ),
            '(== "hello" "hello")',
        ),
        (
            "Null and inequality",
            Binary(
                Literal(None),
                operator(TokenType.BANG_EQUAL, "!="),
                Literal(""),
            ),
            '(!= null "")',
        ),
        (
            "Less than",
            Binary(
                Literal(1),
                operator(TokenType.LESS, "<"),
                Literal(2),
            ),
            "(< 1 2)",
        ),
        (
            "Less than or equal",
            Binary(
                Literal(2),
                operator(TokenType.LESS_EQUAL, "<="),
                Literal(2),
            ),
            "(<= 2 2)",
        ),
        (
            "Greater than",
            Binary(
                Literal(3),
                operator(TokenType.GREATER, ">"),
                Literal(2),
            ),
            "(> 3 2)",
        ),
        (
            "Greater than or equal",
            Binary(
                Literal(3),
                operator(TokenType.GREATER_EQUAL, ">="),
                Literal(3),
            ),
            "(>= 3 3)",
        ),
        (
            "String escapes",
            Literal('First\n"second"\\third'),
            r'"First\n\"second\"\\third"',
        ),
        (
            "Nested grouping and zero",
            Grouping(Grouping(Literal(0))),
            "(group (group 0))",
        ),
    ]

# --- start AI code ---
    failures = 0

    for number, (purpose, expression, expected) in enumerate(tests, 1):
        actual = str(expression)
        matches = actual == expected

        print(f"Test {number}: {purpose}")
        print(f"Expected: {expected}")
        print(f"Actual:   {actual}")
        print(f"Result:   {'PASS' if matches else 'FAIL'}")
        print()

        if not matches:
            failures += 1

    print(f"{len(tests) - failures}/{len(tests)} tests passed.")
    return 1 if failures else 0
# --- end AI code ---

if __name__ == "__main__":
    sys.exit(main())