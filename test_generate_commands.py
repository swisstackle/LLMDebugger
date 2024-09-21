import unittest
from generate_commands import get_starting_line
import ast

class TestGetStartingLine(unittest.TestCase):
    def setUp(self):
        self.parse_and_test = lambda script, expected: self.assertEqual(
            get_starting_line(ast.parse(script)), expected
        )

    def test_empty_script(self):
        script = ""
        self.parse_and_test(script, 1)

    def test_only_definitions(self):
        script = """
def foo():
    pass

class Bar:
    def method(self):
        pass
"""
        self.parse_and_test(script, 1)

    def test_starting_executable_line(self):
        script = """
x = 10
def foo():
    pass
"""
        self.parse_and_test(script, 2)

    def test_non_executable_start(self):
        script = """
# This is a comment
x = 10
"""
        self.parse_and_test(script, 3)

    def test_start_with_import(self):
        script = """
import os
x = 10
"""
        self.parse_and_test(script, 2)

if __name__ == '__main__':
    unittest.main()