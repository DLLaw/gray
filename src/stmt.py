from expr import Expr


class Stmt:
    pass


class ExpressionStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression


class PrintStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression