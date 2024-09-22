import unittest
from generate_commands import get_starting_line, get_all_executable_lines
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
        script = """def foo():
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

class TestGetAllExecutableLines(unittest.TestCase):
    def setUp(self):
        self.parse_and_test = lambda script, expected: self.assertEqual(
            get_all_executable_lines(script), expected
        )

    def test_empty_script(self):
        script = ""
        self.parse_and_test(script, [])

    def test_only_definitions(self):
        script = """def foo():
    pass

class Bar:
    def method(self):
        pass
"""
        self.parse_and_test(script, [])

    def test_variable_assignments(self):
        script = """x = 10
y = 20
z = x + y
"""
        self.parse_and_test(script, [1, 2, 3])

    def test_control_structures(self):
        script = """for i in range(5):
    print(i)

if True:
    print("True branch")
else:
    print("False branch")
"""
        self.parse_and_test(script, [1,2, 4, 5, 6, 7])

    def test_import_statements(self):
        script = """import os
import sys

def foo():
    pass
"""
        self.parse_and_test(script, [1, 2, 5])

    def test_expressions_and_function_calls(self):
        script = """print("Hello, World!")
result = sum([1, 2, 3])
foo()
"""
        self.parse_and_test(script, [1, 2, 3])

    def test_multiline_expressions(self):
        script = """total = (
    1 +
    2 +
    3
)
print(total)
"""
        self.parse_and_test(script, [1, 2, 3, 4, 6])

    def test_decorators(self):
        script = """@decorator
def foo():
    pass

@decorator
class Bar:
    pass
"""
        self.parse_and_test(script, [])

    def test_try_except_finally(self):
        script = """try:
    x = 1
except Exception as e:
    print(e)
finally:
    print("Done")
"""
        self.parse_and_test(script, [1, 2, 3, 4, 6])

    def test_with_statement(self):
        script = """with open('file.txt') as f:
    content = f.read()
print(content)
"""
        self.parse_and_test(script, [1, 2, 3])

    def test_complex_multiline_function(self):
        script = """def complex_function(x, y):
    if x > y:
        return x
    else:
        return y

result = complex_function(10, 20)
print(result)
"""
        self.parse_and_test(script, [1,2, 3, 4, 5, 7, 8])

    def test_nested_control_structures(self):
        script = """for i in range(3):
    if i % 2 == 0:
        print(f"{i} is even")
    else:
        print(f"{i} is odd")
"""
        self.parse_and_test(script, [1, 2, 3, 5])

    def test_function_with_pass(self):
        script = """def foo():
    pass

foo()
"""
        self.parse_and_test(script, [2, 4])

    def test_class_with_methods(self):
        script = """class MyClass:
    def method_one(self):
        print("Method One")

    def method_two(self):
        print("Method Two")

obj = MyClass()
obj.method_one()
obj.method_two()
"""
        self.parse_and_test(script, [2, 3, 5,6, 8, 9, 10])

    def test_lambda_expressions(self):
        script = """add = lambda x, y: x + y
result = add(5, 3)
print(result)
"""
        self.parse_and_test(script, [1, 2, 3])

    def test_inline_comments(self):
        script = """x = 10  # Initialize x
y = 20  # Initialize y
z = x + y  # Sum of x and y
print(z)  # Output the result
"""
        self.parse_and_test(script, [1, 2, 3, 4])

    def test_docstrings(self):
        script = """def foo():
    \"\"\"This is a docstring.\"\"\"
    x = 10

foo()
"""
        self.parse_and_test(script, [3, 5])

    def test_multiline_comments(self):
        script = """# This is a comment
# spanning multiple lines
x = 10  # Initialize x
"""
        self.parse_and_test(script, [3])

    def test_complex_expression(self):
        script = """result = (lambda x: x * x)(5)
print(result)
"""
        self.parse_and_test(script, [1, 2])

    def test_try_without_except_finally(self):
        script = """try:
    x = 10
finally:
    print("Cleanup")
"""
        self.parse_and_test(script, [1, 2, 4])

    def test_with_multiple_context_managers(self):
        script = """with open('file1.txt') as f1, open('file2.txt') as f2:
    data1 = f1.read()
    data2 = f2.read()
    print(data1, data2)
"""
        self.parse_and_test(script, [1, 2, 3, 4])

    def test_commented_executable_lines(self):
        script = """x = 10
# y = 20
z = x + 30  # This adds 30 to x
# print(z)
"""
        self.parse_and_test(script, [1, 3])

if __name__ == '__main__':
    unittest.main()