from enum import Enum, auto
from typing import Any
import sys


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
    def __init__(self, content: str) -> None:
        self.content: str = content
        self.tokens: list[Token] = list()
        self.line_number: int = 0
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
        self.line_number += 1
        char = 0
        while char < len(self.content):
            type: str = ''
            literal: Any = None
            err: Err = Err.NONE
            token_str: str = self.content[char]
            if token_str == '\n':
                char += 1
                self.line_number += 1
                continue
            if token_str.isspace():
                char += 1
                continue
            # handle operators
            if token_str == '=' and char + 1 < len(self.content):
                if self.content[char + 1] == '=':
                    char += 1
                    token_str += self.content[char]
            elif token_str == '!' and char + 1 < len(self.content):
                if self.content[char + 1] == '=':
                    char += 1
                    token_str += self.content[char]
            elif (token_str == '>' or token_str == '<') and char + 1 < len(self.content):
                if self.content[char + 1] == '=':
                    char += 1
                    token_str += self.content[char]
            # handle comments
            elif token_str == '/' and char + 1 < len(self.content) and self.content[char + 1] == '/':

                # // comment -> skip the rest of line
                if (i := self.content[char + 1:].find('\n')) >= 0:
                    char += i + 1
                    continue
                else:  # the file itself is a comment
                    break

            elif token_str == '"':
                if (ret := self.scan_string_literals(self.content[char+1:])):
                    type, literal = ret
                    token_str = f'"{literal}"'
                    char += len(literal) + 1
                else:
                    self.ret = 65
                    err = Err.UNTERMINATED_STRING
                    char = len(self.content)
            elif token_str.isdigit():
                type, token_str = self.scan_nums(self.content[char:])
                literal = float(token_str)
                char += len(token_str) - 1
            elif self.is_id_start(token_str):
                type, token_str = self.scan_id_keywords(self.content[char:])
                char += len(token_str) - 1
            elif token_str not in self.lexmes:
                self.ret = 65
                err = Err.UNEXPECTED_CHAR

            self.add_token(self.tokenize(
                token_str, self.line_number, type=type, literal=literal, err=err))
            char += 1

        self.add_token(Token('EOF', '', 'null', self.line_number + 1))

    def scan_string_literals(self, line: str) -> tuple[str, str] | None:
        end = -1
        for i, c in enumerate(line):
            if c == '\n':
                self.line_number += 1
            elif c == '"':
                end = i
                break
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

    def tokenize(self, lexme: str, line: int, type: str = '', literal: Any = None, err: Err = Err.NONE) -> Token:
        literal = literal if literal != None else 'null'
        if not type and lexme in self.lexmes:
            type = self.lexmes[lexme]
        return Token(type, lexme, literal, line, err=err)

    def add_token(self, token: Token) -> None:
        self.tokens.append(token)
