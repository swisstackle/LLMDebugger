import ell
@ell.simple(model="gpt-4o")
def generate_next_command(error_message: str, script_path: str, script: str, last_command_output: str) -> str:
    """
    Generate the next pdb command based on the latest output.
    """
    prompt = (
        f"Error Message:\n{error_message}\n\n"
        f"Script:\n{script}\n\n"
        f"Last Command Output:\n{last_command_output}\n\n"
        "Provide the next pdb command to debug the error. Only provide a single pdb command without explanations."
    )
    return prompt


def generate_commands(error_message: str, script_path: str, script: str) -> str:
    """
    Set breakpoints at every executable line and print all variables at each breakpoint.
    """
    pdb_commands = []
    lines = script.split('\n')
    for i, line in enumerate(lines, start=1):
        # Skip empty lines and comments
        if line.strip() and not line.strip().startswith('#'):
            # Set breakpoint
            pdb_commands.append(f"break {script_path}:{i}")
            # Define commands for the breakpoint
            pdb_commands.append("commands")
            pdb_commands.append("    p globals()")
            pdb_commands.append("    p locals()")
            pdb_commands.append("    continue")
            pdb_commands.append("end")
    return '\n'.join(pdb_commands)