from app.AST import Stmt
from app.evaluator import Evaluator
from app.AST import *


class Interpreter():
    def __init__(self, stmts: list[Stmt]) -> None:
        self.stmts: list[Stmt] = stmts
        self.evaluator = Evaluator()

    def interpret(self) -> None:
        for stmt in self.stmts:
            self.exec(stmt)

    def exec(self, stmt: Stmt) -> None:
        if isinstance(stmt, PrintStmt):
            print(self.stringfy(stmt.expr))
        elif isinstance(stmt, ExprStmt):
            self.evaluator.evaluate(stmt.expr)

    def stringfy(self, expr: Expr) -> str:
        out = self.evaluator.evaluate(expr)
        out = self.evaluator.stringfy(out)

        return out
