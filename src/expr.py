import json
from gray_token import Token


class Expr:
    def __str__(self):
        raise NotImplementedError


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if self.value is None:
            return "null"

        if isinstance(self.value, bool):
            return "true" if self.value else "false"

        if isinstance(self.value, str):
            return json.dumps(self.value, ensure_ascii=False)

        return str(self.value)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"({self.operator.lexeme} {self.right})"


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"({self.operator.lexeme} {self.left} {self.right})"


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def __str__(self):
        return f"(group {self.expression})"


class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name.lexeme


class Assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"(= {self.name.lexeme} {self.value})"