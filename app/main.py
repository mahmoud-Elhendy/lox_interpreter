from dataclasses import dataclass
from typing import Any
import sys

from enum import Enum, auto


class Err(Enum):
    NONE = auto()
    UNEXPECTED_CHAR = auto()
    UNTERMINATED_STRING = auto()


class Token:
    def __init__(self, type: str, lexme: str, literal: Any, line: int, err: Err = Err.NONE) -> None:
        self.type: str = type
        self.lexme: str = lexme
        self.literal: Any = literal
        self.line: int = line
        self.err: Err = err

    def __str__(self) -> str:
        return f'{self.type} {self.lexme} {self.literal}'

    def display(self) -> None:
        if self.err == Err.UNEXPECTED_CHAR:
            print(
                f'[line {self.line}] Error: Unexpected character: {self.lexme}', file=sys.stderr)
        elif self.err == Err.UNTERMINATED_STRING:
            print(
                f'[line {self.line}] Error: Unterminated string.', file=sys.stderr)
        else:
            print(self)


class Scanner:
    def __init__(self, content: list[str]) -> None:
        self.content: list[str] = content
        self.tokens: list[Token] = list()
        self.line: int = 0
        self.lexmes: dict[str, str] = {
            '(': 'LEFT_PAREN',
            ')': 'RIGHT_PAREN',
            '{': 'LEFT_BRACE',
            '}': 'RIGHT_BRACE',
            '*': 'STAR',
            '.': 'DOT',
            ',': 'COMMA',
            '+': 'PLUS',
            '-': 'MINUS',
            ';': 'SEMICOLON',
            '/': 'SLASH',
            '=': 'EQUAL',
            '!': 'BANG',
            "!=": "BANG_EQUAL",
            "==": "EQUAL_EQUAL",
            "<=": "LESS_EQUAL",
            ">=": "GREATER_EQUAL",
            "<": "LESS",
            ">": "GREATER",
            "and":    "AND",
            "class":  "CLASS",
            "else":   "ELSE",
            "false":  "FALSE",
            "for":    "FOR",
            "fun":    "FUN",
            "if":     "IF",
            "nil":    "NIL",
            "or":     "OR",
            "print":  "PRINT",
            "return": "RETURN",
            "super":  "SUPER",
            "this":   "THIS",
            "true":   "TRUE",
            "var":    "VAR",
            "while":  "WHILE"
        }
        self.ret: int = 0

    def scan(self) -> None:
        for line in self.content:
            self.line += 1
            char = 0
            while char < len(line):
                type: str = ''
                literal: Any = ''
                err: Err = Err.NONE
                token_str: str = line[char]
                if token_str.isspace():
                    char += 1
                    continue
                # handle operators
                if token_str == '=' and char + 1 < len(line):
                    if line[char + 1] == '=':
                        char += 1
                        token_str += line[char]
                elif token_str == '!' and char + 1 < len(line):
                    if line[char + 1] == '=':
                        char += 1
                        token_str += line[char]
                elif (token_str == '>' or token_str == '<') and char + 1 < len(line):
                    if line[char + 1] == '=':
                        char += 1
                        token_str += line[char]
                # handle comments
                elif token_str == '/' and char + 1 < len(line) and line[char + 1] == '/':
                    # // comment -> skip the rest of line
                    break
                elif token_str == '"':
                    if (ret := self.scan_string_literals(line[char+1:])):
                        type, literal = ret
                        token_str = f'"{literal}"'
                        char += len(literal) + 1
                    else:
                        self.ret = 65
                        err = Err.UNTERMINATED_STRING
                        char = len(line)  # end loop
                elif token_str.isdigit():
                    type, token_str = self.scan_nums(line[char:])
                    literal = float(token_str)
                    char += len(token_str) - 1
                elif self.is_id_start(token_str):
                    type, token_str = self.scan_id_keywords(line[char:])
                    char += len(token_str) - 1
                elif token_str not in self.lexmes:
                    self.ret = 65
                    err = Err.UNEXPECTED_CHAR

                self.add_token(self.tokenize(
                    token_str, self.line, type=type, literal=literal, err=err))
                char += 1
        self.add_token(Token('EOF', '', 'null', self.line + 1))

    def scan_string_literals(self, line: str) -> tuple[str, str] | None:
        end: int = line.find('"')
        if end != -1:
            return ('STRING', line[:end])
        else:
            return None

    def is_id_start(self, c: str) -> bool:
        if c.isalpha() or c == '_':
            return True
        return False

    def is_valid_id_char(self, c: str) -> bool:
        if c.isalpha() or c == '_' or c.isdigit():
            return True
        return False

    def scan_id_keywords(self, line: str) -> tuple[str, str]:
        end = 1
        type: str = 'IDENTIFIER'
        for c in line[1:]:
            if self.is_valid_id_char(c):
                end += 1
            else:
                break
        if line[0:end] in self.lexmes:
            type = self.lexmes[line[0:end]]
        return type, line[0:end]

    def scan_nums(self, line: str) -> tuple[str, str]:
        i = 1
        num: str = line[0]
        first_dot = True
        while i < len(line):
            if line[i].isdigit() or (line[i] == '.' and first_dot):
                if line[i] == '.':
                    first_dot = False
                num += line[i]
            else:
                break
            i += 1
        return 'NUMBER', num

    def tokenize(self, lexme: str, line: int, type: str = '', literal: Any = '', err: Err = Err.NONE) -> Token:
        literal = literal if literal != '' else 'null'
        if not type and lexme in self.lexmes:
            type = self.lexmes[lexme]
        return Token(type, lexme, literal, line, err=err)

    def add_token(self, token: Token) -> None:
        self.tokens.append(token)


def scan(file_contents: list[str]) -> Scanner:
    s = Scanner(file_contents)
    s.scan()
    return s

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


def print_ast(expr: Expr) -> str | None:
    if isinstance(expr, Literal):
        value: Any
        if isinstance(expr.value, bool):
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

    def parse(self) -> Expr:
        return self.expression()
# Evaluator


def evaluate(expression: Expr) -> Any:
    if isinstance(expression, Literal):
        return (expression.value)

    elif isinstance(expression, Binary):
        op: str = expression.op
        left: Expr = expression.lexpr
        right: Expr = expression.rexpr
        if op == '+':
            return evaluate(left) + evaluate(right)
        if op == '-':
            return evaluate(left) - evaluate(right)
        if op == '*':
            return evaluate(left) * evaluate(right)
        if op == '/':
            return evaluate(left) / evaluate(right)
    elif isinstance(expression, Grouping):
        return evaluate(expression.expr)
    elif isinstance(expression, Unary):
        op = expression.op
        expr = evaluate(expression.expr)
        if op == '!':
            if isinstance(expr, float) and expr > 0:
                return False
            if isinstance(expr, float) and expr == 0.0:
                return True  # not sure about this behaviour yet
            return not (expr)
        elif op == '-':
            if isinstance(expr, float):
                return -expr
# f(B(B(1+2)*B(5-3)))
#  └──f(B(1+2)) * f(B(5-3))
#           └── 3 * 2

# f(!!12)
#  └──!f(!12)
#           └── !f(12)


def main() -> None:

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command == "tokenize":
        with open(filename) as file:
            file_contents: list[str] = file.readlines()

        if file_contents:
            s = Scanner(file_contents)
            s.scan()
            for t in s.tokens:
                t.display()
            sys.exit(s.ret)
        else:
            # Placeholder, replace this line when implementing the scanner
            print("EOF  null")
    elif command == "parse":
        with open(filename) as file:
            file_contents: list[str] = file.readlines()

        if file_contents:
            s = Scanner(file_contents)
            s.scan()
            p = Parser(s.tokens)
            try:
                ast = p.parse()
            except SyntaxError as e:
                print(e, file=sys.stderr)
                sys.exit(65)
            out = print_ast(ast)
            print(out)
    elif command == "evaluate":
        with open(filename) as file:
            file_contents: list[str] = file.readlines()

        if file_contents:
            s = Scanner(file_contents)
            s.scan()
            p = Parser(s.tokens)
            try:
                ast: Expr = p.parse()
                out = evaluate(ast)
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
                print(out)
            except SyntaxError as e:
                print(e, file=sys.stderr)
                sys.exit(65)
    elif command == "test":
        e = evaluate(Binary(Literal(5.0), Literal(2.0), '-'))
        print(e)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
