import sys

from expr import Binary, Grouping, Literal, Unary
from token_type import TokenType


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.had_error = False

    def parse(self):
        try:
            expression = self.expression()

            if not self.is_at_end():
                raise self.error(
                    self.peek(),
                    "Unexpected trailing token.",
                )

            return expression

        except ParseError:
            return None
        except RecursionError:
            self.error(self.peek(), "Expression is nested too much.")
            return None

    def expression(self):
        return self.logical_or()

    def logical_or(self):
        return self.binary_chain(
            self.logical_and,
            TokenType.OR,
        )

    def logical_and(self):
        return self.binary_chain(
            self.equality,
            TokenType.AND,
        )

    def equality(self):
        return self.binary_chain(
            self.comparison,
            TokenType.EQUAL_EQUAL,
            TokenType.BANG_EQUAL,
        )

    def comparison(self):
        return self.binary_chain(
            self.term,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        )

    def term(self):
        return self.binary_chain(
            self.factor,
            TokenType.PLUS,
            TokenType.MINUS,
        )

    def factor(self):
        return self.binary_chain(
            self.unary,
            TokenType.MUL,
            TokenType.DIV,
        )

    def binary_chain(self, operand_rule, *operator_types):
        expression = operand_rule()

        while self.match(*operator_types):
            operator = self.previous()
            right = operand_rule()
            expression = Binary(expression, operator, right)

        return expression

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)

        if self.match(TokenType.TRUE):
            return Literal(True)

        if self.match(TokenType.NULL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            opening = self.previous()
            expression = self.expression()

            self.consume(
                TokenType.RIGHT_PAREN,
                f"Expected ')' to close '(' from line {opening.line}.",
            )

            return Grouping(expression)

        raise self.error(
            self.peek(),
            "Expected an expression (literal, unary operator, or '(').",
        )

    def match(self, *token_types):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True

        return False

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()

        raise self.error(self.peek(), message)

    def check(self, token_type):
        return self.peek().type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1

        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def error(self, token, message):
        self.had_error = True

        if token.type == TokenType.EOF:
            location = "at end"
        else:
            location = f"at {token.lexeme!r}"

        print(
            f"[line {token.line}] Error {location}: {message}",
            file=sys.stderr,
        )

        return ParseError()
