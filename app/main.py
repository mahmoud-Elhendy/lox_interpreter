import sys


class Token:
    def __init__(self, type: str, lexme: str, literal: str, line: int, err: bool = False) -> None:
        self.type: str = type
        self.lexme: str = lexme
        self.literal: str = literal
        self.line: int = line
        self.err: bool = err

    def __str__(self) -> str:
        return f'{self.type} {self.lexme} {self.literal}'

    def display(self):
        if self.err:
            print(
                f'[Line {self.line}] Error: Unexpected character: {self.lexme}', file=sys.stderr)
        else:
            print(self)


class Scanner:
    def __init__(self, content: list[str]) -> None:
        self.content: list[str] = content
        self.tokens: list[Token] = list()
        self.line: int = 0
        self.lexmes: dict[str, str] = {
            '(': 'LEFT_PAREN', ')': 'RIGHT_PAREN', '{': 'LEFT_BRACE', '}': 'RIGHT_BRACE', '*': 'STAR', '.': 'DOT', ',': 'COMMA', '+': 'PLUS', '-': 'MINUS', ';': 'SEMICOLON', '/': 'SLASH'}
        self.ret: int = 0

    def scan(self) -> None:
        for line in self.content:
            self.line += 1
            for lexme in line:
                self.add_token(self.tokenize(lexme, self.line))
        self.add_token(Token('EOF', '', 'null', self.line + 1))

    def tokenize(self, lexme: str, line: int) -> Token:
        if lexme in self.lexmes:
            return Token(self.lexmes[lexme], lexme, 'null', line)
        else:
            self.ret = 65
            return Token('', lexme, '', line, err=True)

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
