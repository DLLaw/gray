from expr import Expr


class Stmt:
    pass


class ExpressionStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression


class PrintStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

class LetStmt(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer


class BlockStmt(Stmt):
    def __init__(self, statements):
        self.statements = statements