# expression     → literal
#                | unary
#                | binary
#                | grouping ;

# literal        → NUMBER | STRING | "true" | "false" | "nil" ;
# grouping       → "(" expression ")" ;
# unary          → ( "-" | "!" ) expression ;
# binary         → expression operator expression ;
# operator       → "==" | "!=" | "<" | "<=" | ">" | ">="
#                | "+"  | "-"  | "*" | "/" ;

# Note: Literal is an expression but op not expression

from dataclasses import dataclass
from typing import Any


class Expr:
    pass


@dataclass
class Literal(Expr):
    value: Any


@dataclass
class Grouping(Expr):
    expr: Expr


@dataclass
class Unary(Expr):
    op: str
    expr: Expr


@dataclass
class Binary(Expr):
    lexpr: Expr
    rexpr: Expr
    op: str


def print_ast(expr: Expr) -> str | None:
    if isinstance(expr, Literal):
        return str(expr.value)
    if isinstance(expr, Grouping):
        return f"(group {print_ast(expr.expr)})"
    if isinstance(expr, Unary):
        return f"({expr.op} {print_ast(expr.expr)})"
    if isinstance(expr, Binary):
        return f"({expr.op} {print_ast(expr.lexpr)} {print_ast(expr.rexpr)})"
