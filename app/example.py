import re

# Tokenizer


def tokenize(source):
    token_spec = [
        ('NUMBER',  r'\d+(\.\d*)?'),
        ('PLUS',    r'\+'),
        ('MINUS',   r'-'),
        ('MUL',     r'\*'),
        ('DIV',     r'/'),
        ('LPAREN',  r'\('),
        ('RPAREN',  r'\)'),
        ('SKIP',    r'[ \t]+'),
    ]
    regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    for match in re.finditer(regex, source):
        kind = match.lastgroup
        if kind == 'SKIP':
            continue
        # print(kind, match.group())
        yield (kind, match.group())

# Parser

# expression → term ( ("+" | "-") term )* ;
# term       → factor ( ("*" | "/") factor )* ;
# factor     → NUMBER | "(" expression ")" ;


class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.current = 0

    def peek(self):
        return self.tokens[self.current] if self.current < len(self.tokens) else ('EOF', '')

    def advance(self):
        tok = self.peek()
        self.current += 1
        return tok

    def match(self, *expected):
        kind, _ = self.peek()
        if kind in expected:
            return self.advance()
        return None

    def parse(self):
        return self.expression()

    # -> float | tuple[Any, float, float] | tuple[Any, float | tup...:
    def expression(self):
        expr = self.term()
        while self.match('PLUS', 'MINUS'):
            op = self.tokens[self.current - 1][1]
            right = self.term()
            expr = (op, expr, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match('MUL', 'DIV'):
            op = self.tokens[self.current - 1][1]
            right = self.factor()
            expr = (op, expr, right)
        return expr

    def factor(self):
        if self.match('NUMBER'):
            return float(self.tokens[self.current - 1][1])
        if self.match('LPAREN'):
            expr = self.expression()
            self.match('RPAREN')  # consume closing )
            return expr
        raise SyntaxError("Expected number or (expr)")

# Evaluator


def evaluate(node):
    if isinstance(node, float):
        return node
    op, left, right = node
    if op == '+':
        return evaluate(left) + evaluate(right)
    if op == '-':
        return evaluate(left) - evaluate(right)
    if op == '*':
        return evaluate(left) * evaluate(right)
    if op == '/':
        return evaluate(left) / evaluate(right)


# Run
source = "abc1 + 2 * (3 + 4)"
tokens = tokenize(source)
print(tokens)
parser = Parser(tokens)
ast = parser.parse()
print("AST:", ast)
print("Result:", evaluate(ast))
