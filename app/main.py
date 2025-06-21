import sys


class Token:
    def __init__(self, type: str, lexme: str, literal: str) -> None:
        self.type = type
        self.lexme = lexme
        self.literal = literal

    def __str__(self) -> str:
        return f'{self.type} {self.lexme} {self.literal}'


class Scanner:
    def __init__(self, content: list[str]) -> None:
        self.content: list[str] = content
        self.tokens: list[Token] = list()
        self.line: int = 0

    def scan(self) -> None:
        for line in self.content:
            self.line += 1
            for lexme in line:
                self.add_token(self.tokenize(lexme))

    def tokenize(self, lexme: str) -> Token:
        lexme_type = ''
        if lexme == '(':
            lexme_type = 'LEFT_PAREN'
        elif lexme == ')':
            lexme_type = 'RIGHT_PAREN'
        return Token(lexme_type, lexme, 'null')

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
            print(t)
        print("EOF  null")
    else:
        # Placeholder, replace this line when implementing the scanner
        print("EOF  null")


if __name__ == "__main__":
    main()
