import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEST_DIR = Path(__file__).resolve().parent

# name, source input, expected AST or error
# --- start AI code ---
# Ran all of these tests manually and had ChatGPT add them to this file
TESTS = [
    (
        "precedence",
        "1 + 2 * 3",
        "(+ 1 (* 2 3))",
    ),
    (
        "grouping",
        "(1 + 2) * 3",
        "(* (group (+ 1 2)) 3)",
    ),
    (
        "nested_grouping",
        "((1 + 2))",
        "(group (group (+ 1 2)))",
    ),
    (
        "subtraction_associativity",
        "10 - 3 - 2",
        "(- (- 10 3) 2)",
    ),
    (
        "division_associativity",
        "20 / 2 / 5",
        "(/ (/ 20 2) 5)",
    ),
    (
        "unary_and_decimal",
        "- -3.5",
        "(- (- 3.5))",
    ),
    (
        "logical_precedence",
        "true or false and !false",
        "(or true (and false (! false)))",
    ),
    (
        "comparisons_and_equality",
        "1 < 2 == 3 <= 4",
        "(== (< 1 2) (<= 3 4))",
    ),
    (
        "remaining_comparisons",
        "3 > 2 != 4 >= 5",
        "(!= (> 3 2) (>= 4 5))",
    ),
    (
        "strings_and_null",
        '("hello" == "hello") and (null != "")',
        '(and (group (== "hello" "hello")) (group (!= null "")))',
    ),
    (
        "escaped_string",
        r'"First\nSecond"',
        r'"First\nSecond"',
    ),
    (
        "missing_closing_parenthesis",
        "(1 + 2",
        "Expected ')'",
    ),
    (
        "missing_operand",
        "1 +",
        "Expected an expression",
    ),
    (
        "unexpected_token",
        "let",
        "Expected an expression",
    ),
    (
        "trailing_token",
        "1 2",
        "Unexpected trailing token",
    ),
    (
        "extra_closing_parenthesis",
        "1)",
        "Unexpected trailing token",
    ),
    (
        "missing_left_operand",
        "* 2",
        "Expected an expression",
    ),
    (
        "empty_input",
        "",
        "Expected an expression",
    ),
    (
        "lexical_error",
        "@",
        "That character isn't valid",
    ),
]
# --- end AI code ---
# Cases at and after this index should throw errors
FIRST_ERROR = 11


def run_gray(arguments, input_text=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "src" / "gray.py"), *arguments],
        input=input_text,
        capture_output=True,
        text=True,
        cwd=ROOT,
        timeout=10,
    )


def main():
    failures = 0

    for index, (name, source, expected) in enumerate(TESTS):
        path = TEST_DIR / f"{name}.gray"
        path.write_text(source, encoding="utf-8")

        result = run_gray([str(path)])
        actual_ast = result.stdout.strip()
        actual_error = result.stderr.strip()
        expects_error = index >= FIRST_ERROR

        if expects_error:
            passed = (
                result.returncode == 65
                and actual_ast == ""
                and expected in actual_error
                and "[line 1]" in actual_error
                and "Traceback" not in actual_error
            )
        else:
            passed = (
                result.returncode == 0
                and actual_error == ""
                and actual_ast == expected
            )

        print(f"Test: {name}")
        print(f"Source: {source!r}")
        print(f"Expected: {expected}")
        print(f"Actual AST: {actual_ast or '(none)'}")
        print(f"Actual errors: {actual_error or '(none)'}")
        print(f"Exit code: {result.returncode}")
        print(f"Result: {'PASS' if passed else 'FAIL'}")
        print()

        if not passed:
            failures += 1

    # Test recovery after error
    interactive_input = "1 +\n4 + 5\n@\n6 * 7\n"
    result = run_gray([], interactive_input)

    expected_stdout = (
        "> > (+ 4 5)\n"
        "> > (* 6 7)\n"
        "> \nExiting REPL...\n"
    )

    interactive_passed = (
        result.returncode == 0
        and result.stdout == expected_stdout
        and result.stderr.count("[line 1]") == 2
        and "Expected an expression" in result.stderr
        and "That character isn't valid" in result.stderr
        and "Traceback" not in result.stderr
    )

    print("Test interactive_recovery")
    print(f"Source: {interactive_input!r}")
    print("Expected two errors, valid ASTs afterward, then EOF exit")
    print(f"Actual stdout:\n{result.stdout}")
    print(f"Actual stderr:\n{result.stderr}")
    print(f"Result: {'PASS' if interactive_passed else 'FAIL'}")

    if not interactive_passed:
        failures += 1

    total = len(TESTS) + 1
    print(f"\n{total - failures}/{total} tests passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())