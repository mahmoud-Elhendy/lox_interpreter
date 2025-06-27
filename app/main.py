import sys

from app.scanner import Scanner
from app.RDParser import Parser
from app.evaluator import Evaluator
from app.interpreter import Interpreter
from app.AST import *


def main() -> None:

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command == "tokenize":
        with open(filename, encoding="utf-8") as file:
            file_contents = file.read()

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
        with open(filename, encoding="utf-8") as file:
            file_contents = file.read()

        if file_contents:
            s = Scanner(file_contents)
            s.scan()
            p = Parser(s.tokens)
            try:
                ast = p.parse_expr()
                out = print_ast(ast)
                print(out)
            except SyntaxError as e:
                print(e, file=sys.stderr)
                sys.exit(65)

    elif command == "evaluate":
        with open(filename, encoding="utf-8") as file:
            file_contents = file.read()

        if file_contents:
            s = Scanner(file_contents)
            s.scan()
            p = Parser(s.tokens)
            try:
                ast: Expr = p.parse_expr()
                evaluator = Evaluator()
                out = evaluator.evaluate(ast)
                out = evaluator.stringfy(out)
                print(out)
            except SyntaxError as e:
                print(e, file=sys.stderr)
                sys.exit(65)
            except RuntimeError as e:
                print(e, file=sys.stderr)
                sys.exit(70)
    elif command == "run":
        with open(filename, encoding="utf-8") as file:
            file_contents: str = file.read()

        if file_contents:
            s = Scanner(file_contents)
            s.scan()
            p = Parser(s.tokens)
            try:
                stms: list[Stmt] = p.parse()
            except SyntaxError as e:
                print(e, file=sys.stderr)
                sys.exit(65)
            print(stms)
            interpreter = Interpreter(stms)
            try:
                interpreter.interpret()
            except RuntimeError as e:
                print(e, file=sys.stderr)
                sys.exit(70)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
