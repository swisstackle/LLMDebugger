import ell
from generate_commands import generate_commands
from auto_pdb import AutoPdb

@ell.simple(model="gpt-4o-mini")
def assist_debugger(error_message: str, script_path: str, script: str) -> str:
    """
    Analyze the error message and automate pdb debugging by executing generated commands.
    """
    # Generate pdb commands using the updated generate_commands function
    pdb_commands = generate_commands(error_message, script_path, script)
    
    # Debug: Log the generated pdb commands
    print("Generated Pdb Commands:\n", pdb_commands)
    
    # Initialize AutoPdb with the generated commands
    pdb = AutoPdb(pdb_commands)
    pdb.run_path(script_path)
    output = pdb.get_output()
    
    # Optionally, you can process the output or log it
    print("Debugger Output:\n", output)
    
    return "Debugger assistance completed."