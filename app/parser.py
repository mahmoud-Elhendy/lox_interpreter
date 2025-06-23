from AST import Expr
from main import Token
from AST import *

# expression     → equality ;
# equality       → comparison ( ( "!=" | "==" ) comparison )* ;
# comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
# term           → factor ( ( "-" | "+" ) factor )* ;
# factor         → unary ( ( "/" | "*" ) unary )* ;
# unary          → ( "!" | "-" ) unary
#                | primary ;
# primary        → NUMBER | STRING | "true" | "false" | "nil"
#                | "(" expression ")" ;


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens
        self.current = 0

    def peek(self) -> Token:
        return self.tokens[self.current]

    def advance(self) -> Token:
        tok = self.peek()
        self.current += 1
        return tok

    def expression(self) -> Expr:
        return self.term()

    def match(self, *types: str) -> Token | None:
        kind = self.peek().type
        if kind in types:
            return self.advance()
        return None

    def term(self) -> Expr:
        expr: Expr = self.primary()
        while (token := self.match("PLUS", "MINUS")):
            right = self.primary()
            expr = Binary(expr, right, token.lexme)
        return expr

    def primary(self) -> Expr:
        if token := self.match('TRUE', 'FALSE', 'NIL'):
            return Literal(token.lexme)
        elif token := self.match('NUMBER', 'STRING'):
            return Literal(token.literal)
        elif self.match('LEFT_PAREN'):
            expr: Expr = self.expression()
            return Grouping(expr)
        raise SyntaxError("Expected literal or (expr)")

    def parse(self) -> Expr:
        return self.expression()
