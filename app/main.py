import sys

from enum import Enum, auto


class Err(Enum):
    NONE = auto()
    UNEXPECTED_CHAR = auto()
    UNTERMINATED_STRING = auto()


class Token:
    def __init__(self, type: str, lexme: str, literal: str, line: int, err: Err = Err.NONE) -> None:
        self.type: str = type
        self.lexme: str = lexme
        self.literal: str = literal
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
            ">": "GREATER"}
        self.ret: int = 0

    def scan(self) -> None:
        for line in self.content:
            self.line += 1
            char = 0
            while char < len(line):
                type: str = ''
                literal: str = ''
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
                    literal = str(float(token_str))
                    char += len(token_str) - 1
                elif self.is_id_start(token_str):
                    type, token_str = self.scan_id(line[char:])
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

    def scan_id(self, line: str) -> tuple[str, str]:
        end = 1
        for c in line[1:]:
            if self.is_valid_id_char(c):
                end += 1
            else:
                break
        return 'IDENTIFIER', line[0:end]

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

    def tokenize(self, lexme: str, line: int, type: str = '', literal: str = '', err: Err = Err.NONE) -> Token:
        literal = literal if literal else 'null'
        if not type and lexme in self.lexmes:
            type = self.lexmes[lexme]
        return Token(type, lexme, literal, line, err=err)

    def add_token(self, token: Token) -> None:
        self.tokens.append(token)


def main():

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.readlines()

    if file_contents:
        s = Scanner(file_contents)
        s.scan()
        for t in s.tokens:
            t.display()
        sys.exit(s.ret)
    else:
        # Placeholder, replace this line when implementing the scanner
        print("EOF  null")


if __name__ == "__main__":
    main()
