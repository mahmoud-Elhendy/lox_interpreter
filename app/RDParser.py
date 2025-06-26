from app.AST import *
from app.scanner import Token

# statment       → printStmt
# printStmt      → "print" expression ";"
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

    def match(self, *types: str) -> Token | None:
        kind = self.peek().type
        if kind in types:
            return self.advance()
        return None

    def check(self, type: str) -> bool:
        kind = self.peek().type
        if kind == type:
            return True
        return False

    def consume(self, type: str, expected: str) -> None:
        if self.check(type):
            self.advance()
        else:
            raise SyntaxError(expected)

    def at_end(self) -> bool:
        return self.peek().type == 'EOF'

    def statment(self) -> Stmt:
        if self.match('PRINT'):
            return self.printstatment()
        raise SyntaxError('Unsupported statment')  # TODO fix

    def printstatment(self) -> Stmt:
        expr = self.expression()
        self.consume('SEMICOLON', 'Statment missing ;')
        return PrintStmt(expr)

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()
        while (token := self.match("BANG_EQUAL", "EQUAL_EQUAL")):
            right = self.comparison()
            expr = Binary(expr, right, token.lexme)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()
        while (token := self.match("LESS_EQUAL", "GREATER_EQUAL", "LESS", "GREATER")):
            right = self.term()
            expr = Binary(expr, right, token.lexme)
        return expr

    def term(self) -> Expr:
        expr: Expr = self.factor()
        while (token := self.match("PLUS", "MINUS")):
            right = self.factor()
            expr = Binary(expr, right, token.lexme)
        return expr

    def factor(self) -> Expr:
        expr: Expr = self.unary()
        while (token := self.match("SLASH", "STAR")):
            right = self.unary()
            expr = Binary(expr, right, token.lexme)
        return expr

    def unary(self) -> Expr:
        if token := self.match("BANG", "MINUS"):
            right = self.unary()
            return Unary(token.lexme, right)
        return self.primary()

    def primary(self) -> Expr:
        if token := self.match('TRUE'):
            return Literal(True)
        elif token := self.match('FALSE'):
            return Literal(False)
        elif token := self.match('NIL'):
            return Literal(None)
        elif token := self.match('NUMBER', 'STRING'):
            return Literal(token.literal)
        elif self.match('LEFT_PAREN'):
            expr: Expr = self.expression()
            self.match('RIGHT_PAREN')
            return Grouping(expr)
        token = self.peek()
        raise SyntaxError(
            f"[line {token.line}] Error at '{token.lexme}': Expect expression.")

    def parse(self) -> list[Stmt]:
        statments: list[Stmt] = []
        while not self.at_end():
            statments.append(self.statment())
        return statments

    def parse_expr(self) -> Expr:
        return self.expression()
