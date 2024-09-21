import unittest
from generate_commands import get_starting_line
import ast

class TestGetStartingLine(unittest.TestCase):

    def test_empty_script(self):
        script = ""
        tree = ast.parse(script)
        self.assertEqual(get_starting_line(tree), 1)

    def test_only_definitions(self):
        script = """
def foo():
    pass

class Bar:
    def method(self):
        pass
"""
        tree = ast.parse(script)
        self.assertEqual(get_starting_line(tree), 1)  # Now it should return 1

    def test_starting_executable_line(self):
        script = """
x = 10
def foo():
    pass
"""
        tree = ast.parse(script)
        self.assertEqual(get_starting_line(tree), 2)

    def test_non_executable_start(self):
        script = """
# This is a comment
x = 10
"""
        tree = ast.parse(script)
        self.assertEqual(get_starting_line(tree), 3)

    def test_start_with_import(self):
        script = """
import os
x = 10
"""
        tree = ast.parse(script)
        self.assertEqual(get_starting_line(tree), 2)

if __name__ == '__main__':
    unittest.main()