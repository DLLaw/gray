import operator
import sys

from expr import Binary, Grouping, Literal, Unary


class Evaluator:
    def __init__(self):
        self.had_error = False

    def evaluate(self, expression):
        self.had_error = False
        try:
            return self.calculate(expression)
        except (RuntimeError, ArithmeticError) as error:
            self.had_error = True
            print(f"Runtime error: {error}", file=sys.stderr)
            return None

    def calculate(self, expression):
        if isinstance(expression, Literal):
            return expression.value

        if isinstance(expression, Grouping):
            return self.calculate(expression.expression)

        if isinstance(expression, Unary):
            value = self.calculate(expression.right)
            if expression.operator.lexeme == "!":
                return not self.truthy(value)
            if not self.is_number(value):
                self.error(expression.operator, "Expected a number.")
            return -value

        if isinstance(expression, Binary):
            token = expression.operator
            symbol = token.lexeme
            left = self.calculate(expression.left)

            if symbol == "or":
                return left if self.truthy(left) else self.calculate(expression.right)
            if symbol == "and":
                return self.calculate(expression.right) if self.truthy(left) else left

            right = self.calculate(expression.right)

            if symbol in ("==", "!="):
                same_type = type(left) is type(right)
                both_numbers = self.is_number(left) and self.is_number(right)
                equal = (same_type or both_numbers) and left == right
                return equal if symbol == "==" else not equal

            if symbol == "+" and isinstance(left, str) and isinstance(right, str):
                return left + right

            if not (self.is_number(left) and self.is_number(right)):
                self.error(token, "Expected two numbers.")

            if symbol == "/" and right == 0:
                self.error(token, "Cannot divide by zero.")

            operations = {
                "+": operator.add,
                "-": operator.sub,
                "*": operator.mul,
                "/": operator.truediv,
                "<": operator.lt,
                "<=": operator.le,
                ">": operator.gt,
                ">=": operator.ge,
            }
            if symbol not in operations:
                self.error(token, "Unsupported operator.")
            return operations[symbol](left, right)

        raise RuntimeError("Unknown expression.")

    @staticmethod
    def is_number(value):
        return type(value) in (int, float)

    @staticmethod
    def truthy(value):
        return value is not None and value is not False

    @staticmethod
    def error(token, message):
        raise RuntimeError(f"[line {token.line}] at {token.lexeme!r}: {message}")

    @staticmethod
    def stringify(value):
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)