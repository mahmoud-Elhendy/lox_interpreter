from app.AST import *
from app.AST import Expr
from app.scanner import Token

# program        → declaration* EOF ;

# declaration    → varDecl | statement ;

# statement      → printStmt | exprStmt ;

# printStmt      → "print" expression ";" ;
# exprStmt       → expression ";" ;
# varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;

# expression     → assignment ;

# assignment     → IDENTIFIER "=" assignment
#                | equality ;

# equality       → comparison ( ( "!=" | "==" ) comparison )* ;
# comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
# term           → factor ( ( "-" | "+" ) factor )* ;
# factor         → unary ( ( "/" | "*" ) unary )* ;
# unary          → ( "!" | "-" ) unary
#                | primary ;

# primary        → NUMBER | STRING | "true" | "false" | "nil"
#                | "(" expression ")" | IDENTIFIER ;


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

    def decl(self) -> Stmt:
        if self.match('VAR'):
            return self.vardecl()
        else:
            return self.statment()

    def vardecl(self) -> Stmt:
        if token := self.match('IDENTIFIER'):
            expr = None
            if self.match('EQUAL'):
                expr = self.expression()
            self.consume('SEMICOLON', 'Missing ;')
            return Decl(token.lexme, expr)
        else:
            token = self.peek()
            raise SyntaxError(
                f'[line {token.line}]: Expected Identifier after var')

    def statment(self) -> Stmt:
        if self.match('PRINT'):
            return self.printstatment()
        else:
            return self.exprstatment()

    def exprstatment(self) -> Stmt:
        expr = self.expression()
        self.consume('SEMICOLON', 'Statment missing ;')
        return ExprStmt(expr)

    def printstatment(self) -> Stmt:
        expr = self.expression()
        self.consume('SEMICOLON', 'Statment missing ;')
        return PrintStmt(expr)

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr: Expr = self.equality()
        if self.match('EQUAL'):
            value: Expr = self.assignment()
            if isinstance(expr, Variable):
                return Assign(expr.name, value)
            else:
                raise SyntaxError("Invalid assignment target.")
        return expr

    def equality(self) -> Expr:
        expr: Expr = self.comparison()
        while (token := self.match("BANG_EQUAL", "EQUAL_EQUAL")):
            right: Expr = self.comparison()
            expr = Binary(expr, right, token.lexme)
        return expr

    def comparison(self) -> Expr:
        expr: Expr = self.term()
        while (token := self.match("LESS_EQUAL", "GREATER_EQUAL", "LESS", "GREATER")):
            right: Expr = self.term()
            expr = Binary(expr, right, token.lexme)
        return expr

    def term(self) -> Expr:
        expr: Expr = self.factor()
        while (token := self.match("PLUS", "MINUS")):
            right: Expr = self.factor()
            expr = Binary(expr, right, token.lexme)
        return expr

    def factor(self) -> Expr:
        expr: Expr = self.unary()
        while (token := self.match("SLASH", "STAR")):
            right: Expr = self.unary()
            expr = Binary(expr, right, token.lexme)
        return expr

    def unary(self) -> Expr:
        if token := self.match("BANG", "MINUS"):
            right: Expr = self.unary()
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
            self.consume('RIGHT_PAREN', 'Expected )')
            return Grouping(expr)
        elif token := self.match('IDENTIFIER'):
            return Variable(token.lexme)

        token = self.peek()
        raise SyntaxError(
            f"[line {token.line}] Error at '{token.lexme}': Expect expression.")

    def parse(self) -> list[Stmt]:
        statments: list[Stmt] = []
        while not self.at_end():
            statments.append(self.decl())
        return statments

    def parse_expr(self) -> Expr:
        return self.expression()
