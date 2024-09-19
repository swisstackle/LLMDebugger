import ell
import subprocess
from generate_commands import generate_commands
from auto_pdb import AutoPdb

@ell.simple(model="gpt-4o-mini")
def assist_debugger(error_message: str, script_path: str) -> str:
    """
    Analyze the error message and automate pdb debugging by executing generated commands.
    """
    # Generate pdb commands using the LMP
    suggested_commands = generate_commands(error_message)
    
    # Debug: Log the raw suggested commands
    print("Suggested Commands from LLM:\n", suggested_commands)
    
    # Split commands into a list, filter out any empty lines or comments
    pdb_commands = []
    for line in suggested_commands.split('\n'):
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            pdb_commands.append(stripped)
    
    # Debug: Log the cleaned pdb commands
    print("Cleaned Pdb Commands:\n", pdb_commands)
    
    if not pdb_commands:
        return "No valid pdb commands generated."
    
    # Initialize AutoPdb with the generated commands
    def pdb_exec():
        AutoPdb(pdb_commands).run(f'exec(open("{script_path}").read())')
    
    # Execute the debugger
    pdb_exec()
    
    return "Debugger assistance completed."