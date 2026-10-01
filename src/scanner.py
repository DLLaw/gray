import math
import sys

from gray_token import Token
from token_type import TokenType


class Scanner:
    keywords = {
        "and": TokenType.AND,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "fn": TokenType.FN,
        "for": TokenType.FOR,
        "if": TokenType.IF,
        "let": TokenType.LET,
        "null": TokenType.NULL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "true": TokenType.TRUE,
        "while": TokenType.WHILE,
    }

    single_character_tokens = {
        "(": TokenType.LEFT_PAREN,
        ")": TokenType.RIGHT_PAREN,
        "{": TokenType.LEFT_BRACE,
        "}": TokenType.RIGHT_BRACE,
        ",": TokenType.COMMA,
        ".": TokenType.DOT,
        "-": TokenType.MINUS,
        "+": TokenType.PLUS,
        ";": TokenType.SEMICOLON,
        "/": TokenType.SLASH,
        "*": TokenType.STAR,
    }

    paired_tokens = {
        "!": (TokenType.BANG, TokenType.BANG_EQUAL),
        "=": (TokenType.EQUAL, TokenType.EQUAL_EQUAL),
        "<": (TokenType.LESS, TokenType.LESS_EQUAL),
        ">": (TokenType.GREATER, TokenType.GREATER_EQUAL),
    }

    escape_sequences = {
        "n": "\n",
        "t": "\t",
        "r": "\r",
        '"': '"',
        "\\": "\\",
    }

    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.start_line = 1
        self.had_error = False

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.start_line = self.line
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        character = self.advance()

        if character in self.single_character_tokens:
            self.add_token(self.single_character_tokens[character])

        elif character in self.paired_tokens:
            single, paired = self.paired_tokens[character]
            self.add_token(paired if self.match("=") else single)

        elif character == "#":
            while not self.is_at_end() and self.peek() not in ("\r", "\n"):
                self.advance()

        elif character in (" ", "\t"):
            pass

        elif character == "\r":
            self.match("\n")
            self.line += 1

        elif character == "\n":
            self.line += 1

        elif character == '"':
            self.string()

        elif self.is_digit(character):
            self.number()

        elif self.is_alpha(character):
            self.identifier()

        else:
            self.error(
                self.start_line,
                f"That character isn't valid: {character!r}.",
            )

    def string(self):
        characters = []
        valid = True

        while not self.is_at_end():
            #line breaks aren't allowed inside strings.
            if self.peek() in ("\r", "\n"):
                self.error(self.start_line, "You never closed the string.")
                return

            character = self.advance()

            if character == '"':
                if valid:
                    self.add_token(TokenType.STRING, "".join(characters))
                return

            if character == "\\":
                if self.is_at_end() or self.peek() in ("\r", "\n"):
                    self.error(self.start_line, "You never closed the string.")
                    return

                escape = self.advance()

                if escape in self.escape_sequences:
                    characters.append(self.escape_sequences[escape])
                else:
                    self.error(
                        self.start_line,
                        f"Not a valid escape sequence: '\\{escape}'.",
                    )
                    valid = False
            else:
                characters.append(character)

        self.error(self.start_line, "You never closed the string.")

    # --- start AI code ---
    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        text = self.source[self.start:self.current]
        value = float(text) if "." in text else int(text)

        self.add_token(TokenType.NUMBER, value)
    # --- end AI code ---

    def identifier(self):
        while self.is_alpha(self.peek()) or self.is_digit(self.peek()):
            self.advance()

        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    def advance(self):
        character = self.source[self.current]
        self.current += 1
        return character

    def match(self, expected):
        if self.is_at_end() or self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def is_at_end(self):
        return self.current >= len(self.source)

    def add_token(self, token_type, literal=None):
        lexeme = self.source[self.start:self.current]
        self.tokens.append(
            Token(token_type, lexeme, literal, self.start_line)
        )

    def error(self, line, message):
        self.had_error = True
        print(f"[line {line}] Error: {message}", file=sys.stderr)

    @staticmethod
    def is_digit(character):
        return "0" <= character <= "9"

    @staticmethod
    def is_alpha(character):
        return (
            "a" <= character <= "z"
            or "A" <= character <= "Z"
            or character == "_"
        )