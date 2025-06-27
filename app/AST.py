from dataclasses import dataclass
from typing import Any

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


class Stmt():
    pass


@dataclass
class PrintStmt(Stmt):
    expr: Expr


@dataclass
class ExprStmt(Stmt):
    expr: Expr


def print_ast(expr: Expr) -> str | None:
    if isinstance(expr, Literal):
        value: Any
        if expr.value is None:
            value = 'nil'
        elif isinstance(expr.value, bool):
            value = 'true' if expr.value else 'false'
        else:
            value = expr.value
        return str(value)
    if isinstance(expr, Grouping):
        return f"(group {print_ast(expr.expr)})"
    if isinstance(expr, Unary):
        return f"({expr.op} {print_ast(expr.expr)})"
    if isinstance(expr, Binary):
        return f"({expr.op} {print_ast(expr.lexpr)} {print_ast(expr.rexpr)})"
