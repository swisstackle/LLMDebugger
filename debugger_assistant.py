import ell
import subprocess
from generate_commands import generate_commands
from auto_pdb import AutoPdb
import re
import runpy  # Add this import

@ell.simple(model="gpt-4o-mini")
def assist_debugger(error_message: str, script_path: str, script : str) -> str:
    """
    Analyze the error message and automate pdb debugging by executing generated commands.
    """
    # Generate pdb commands using the LMP
    suggested_commands = generate_commands(error_message, script_path, script)
    
    # Debug: Log the raw suggested commands
    print("Suggested Commands from LLM:\n", suggested_commands)
    
    # Define allowed pdb commands
    allowed_commands = {'break', 'continue', 'next', 'step','where', 'quit', 'w', 'c', 'n', 's', 'q', 'commands', 'end', 'p'}
    
    # Regular expression to validate commands
    cmd_pattern = re.compile(r'^(break\b.*|continue\b|next\b|step\b|print\b.+|where\b|quit\b)$')
    
    # Split commands into a list and validate each command
    pdb_commands = []
    for line in suggested_commands.split('\n'):
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            parts = stripped.split(maxsplit=1)
            if parts[0] in allowed_commands:
                pdb_commands.append(stripped)
            elif parts[0] == 'b' and len(parts) > 1:  # Special case for 'break'
                pdb_commands.append(stripped)
            else:
                print(f"Invalid pdb command skipped: '{stripped}'")
    
    # Debug: Log the cleaned pdb commands
    print("Cleaned Pdb Commands:\n", pdb_commands)
    
    if not pdb_commands:
        return "No valid pdb commands generated."
    
    # Initialize AutoPdb with the generated commands
    def pdb_exec():
        import runpy
        def run_script():
            print(f"Attempting to run script: {script_path}")
            runpy.run_path(script_path)
        
        # Create a new dictionary with necessary globals
        globals_dict = {'run_script': run_script, '__name__': '__main__'}
        
        AutoPdb(pdb_commands).run('run_script()', globals=globals_dict)

    pdb_exec()
    
    return "Debugger assistance completed."