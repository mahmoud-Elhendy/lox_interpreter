# test_my_math.py
import unittest
from RDParser import *
from main import Token
from AST import *


class TestParser(unittest.TestCase):
    def test_number(self) -> None:
        p = Parser(
            [Token('NUMBER', '12', '12.0', 1), Token('EOF', '', 'null', 1)])
        ret = print_ast(p.parse())
        assert (ret == '12.0')

    def test_bool(self) -> None:
        p = Parser(
            [Token('TRUE', 'true', 'null', 1), Token('EOF', '', 'null', 1)])
        ret = print_ast(p.parse())
        assert (ret == 'true')

    def test_nil(self) -> None:
        p = Parser(
            [Token('NIL', 'nil', 'null', 1), Token('EOF', '', 'null', 1)])
        ret = print_ast(p.parse())
        assert (ret == 'nil')

    def test_expr(self) -> None:
        p = Parser(
            [Token('NUMBER', '1', '1.0', 1), Token('PLUS', '+', 'null', 1), Token('NUMBER', '2', '2.0', 1), Token('EOF', '', 'null', 1)])
        ret = print_ast(p.parse())
        assert (ret == '(+ 1.0 2.0)')


if __name__ == '__main__':
    unittest.main()
