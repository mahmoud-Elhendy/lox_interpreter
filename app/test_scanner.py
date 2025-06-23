# test_my_math.py
import unittest
from main import Scanner


class TestScanner(unittest.TestCase):
    def test_scan_number1(self) -> None:
        content = ['4322()']
        s = Scanner(content=content)
        ret = s.scan_nums(content[0][0:])
        self.assertEqual(ret, ('NUMBER', '4322'))

    def test_scan_number2(self) -> None:
        content = ['43.22()']
        s = Scanner(content=content)
        ret = s.scan_nums(content[0][0:])
        self.assertEqual(ret, ('NUMBER', '43.22'))

    def test_scan_number3(self) -> None:
        content = ['432.2.2()']
        s = Scanner(content=content)
        ret = s.scan_nums(content[0][0:])
        self.assertEqual(ret, ('NUMBER', '432.2'))

    def test_scan_number4(self) -> None:
        content = ['43a2.2.2()']
        s = Scanner(content=content)
        ret = s.scan_nums(content[0][0:])
        self.assertEqual(ret, ('NUMBER', '43'))

    def test_scan_number5(self) -> None:
        content = ['4abc']
        s = Scanner(content=content)
        ret = s.scan_nums(content[0][0:])
        self.assertEqual(ret, ('NUMBER', '4'))


if __name__ == '__main__':
    unittest.main()
