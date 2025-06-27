from typing import Any
from app.AST import *
from app.env import Env


class Evaluator:
    def __init__(self) -> None:
        self.env = Env()
    # f(B(B(1+2)*B(5-3)))
    #  └──f(B(1+2)) * f(B(5-3))
    #           └── 3 * 2

    # f(!!12)
    #  └──!f(!12)
    #           └── !f(12)
    def evaluate(self, expression: Expr) -> Any:
        if isinstance(expression, Literal):
            return (expression.value)

        elif isinstance(expression, Binary):
            op: str = expression.op
            left = self.evaluate(expression.lexpr)
            right = self.evaluate(expression.rexpr)
            if op == '==':
                return left == right
            if op == '!=':
                return left != right
            if op == '+':
                if type(left) is type(right):
                    return left + right
                else:
                    raise RuntimeError(
                        'Operands must be two numbers or two strings.')
            if isinstance(left, float) and isinstance(right, float):
                if op == '-':
                    return left - right
                if op == '*':
                    return left * right
                if op == '/':
                    return left / right
                if op == '>':
                    return left > right
                if op == '<':
                    return left < right
                if op == '>=':
                    return left >= right
                if op == '<=':
                    return left <= right
            else:
                raise RuntimeError('Operands must be numbers.')
        elif isinstance(expression, Grouping):
            return self.evaluate(expression.expr)
        elif isinstance(expression, Unary):
            op = expression.op
            expr = self.evaluate(expression.expr)
            if op == '!':
                if isinstance(expr, float) and expr > 0:
                    return False
                if isinstance(expr, float) and expr == 0.0:
                    return True  # not sure about this behaviour yet
                return not (expr)
            elif op == '-':
                if isinstance(expr, float):
                    return -expr
                else:
                    raise RuntimeError('Operand must be a number.')
        elif isinstance(expression, Variable):
            return self.env.get(expression.name)
        elif isinstance(expression, Assign):
            name = expression.name
            value = self.evaluate(expression.expr)
            self.env.put(name, value)
            return value

    def stringfy(self, out: Any) -> str:
        if isinstance(out, float):
            if out.is_integer():
                out = str(int(out))
            else:
                out = str(out)
        elif isinstance(out, bool | None):
            if out is None:
                out = 'nil'
            else:
                out = 'true' if out else 'false'
        return out
