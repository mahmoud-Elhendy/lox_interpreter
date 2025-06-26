from app.evaluator import Evaluator
from app.AST import *


class Interpreter():
    def exec(self, stmt: Stmt) -> None:
        if isinstance(stmt, PrintStmt):
            print(self.stringfy(stmt.expr))

    def stringfy(self, expr: Expr) -> str:
        evaluator = Evaluator()
        out = evaluator.evaluate(expr)
        out = evaluator.stringfy(out)

        return out
