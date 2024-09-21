import ast

def get_variable_names(script: str) -> list:
    """
    Parse the script and extract variable names from assignments.
    """
    class VariableVisitor(ast.NodeVisitor):
        def __init__(self):
            self.variables = set()

        def visit_Assign(self, node):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.variables.add(target.id)
                elif isinstance(target, ast.Tuple):
                    for elem in target.elts:
                        if isinstance(elem, ast.Name):
                            self.variables.add(elem.id)
            self.generic_visit(node)

        def visit_AugAssign(self, node):
            target = node.target
            if isinstance(target, ast.Name):
                self.variables.add(target.id)
            self.generic_visit(node)

        def visit_AnnAssign(self, node):
            target = node.target
            if isinstance(target, ast.Name):
                self.variables.add(target.id)
            self.generic_visit(node)

    tree = ast.parse(script)
    visitor = VariableVisitor()
    visitor.visit(tree)
    return list(visitor.variables)

def get_all_executable_lines(script: str) -> list:
    """
    Retrieve all executable lines in the script.
    """
    tree = ast.parse(script)
    executable_lines = set()
    for node in ast.walk(tree):
        if hasattr(node, 'lineno') and not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            executable_lines.add(node.lineno)
    return sorted(executable_lines)

def get_starting_line(tree: ast.AST) -> int:
    """
    Retrieve the first executable line in the script.
    """
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue  # Skip definitions
        if hasattr(node, 'lineno'):
            return node.lineno
    return 1  # Default to line 1 if not found

def generate_commands(error_message: str, script_path: str, script: str) -> str:
    """
    Set breakpoints at all executable lines and generate commands to step through lines and print variables.
    """
    pdb_commands = []
    variable_names = get_variable_names(script)

    # Determine all executable lines
    executable_lines = get_all_executable_lines(script)

    # Set a breakpoint at the starting line
    starting_line = get_starting_line(ast.parse(script))
    pdb_commands.append(f"break {script_path}:{starting_line}")
    pdb_commands.append(f"c")

    for line in executable_lines:
        # Step into the line first
        pdb_commands.append("step")
        pdb_commands.append("w")
        
        for var in variable_names:
            pdb_commands.append(f"p {var}")  # Print each variable

    return '\n'.join(pdb_commands)