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


@ell.simple(model="gpt-4o")
def generate_commands(error_message: str, script_path: str, script : str) -> str:
    """
    You are an expert Python debugger. Given the following error message, provide a list of pdb commands needed to automatically debug the issue.
    - Each command should be on a new line.
    - Do not include any explanations, comments, or markdown formatting.
    - Only provide valid pdb commands such as 'break', 'continue', 'next', 'step', 'print <variable>', etc.
    - The allowed commands are 'break', 's', 'p', 'w', 'quit', 'c', 'n', 's', 'q', 'commands', 'end' 
    - At each step, please use the 'print' command to print all variables and their values.
    - Make sure to use the 'commands' command to define commands for each breakpoint and the 'end' command to end the breakpoint command definition.
    - DO NOT use 'print' command in the breakpoint commands. Use 'p'!!! I general try to use the abbreviationse
    - For 'break' command, use 'break {{script_path}}:<line_number>' to set a breakpoint at the specified line number.
    - <important> Make sure to double check in the end if the breakpoints are set correctly so that all variables will be able to be able to be printed out. Think STEP BY STEP TO DO THAT BY ITERATING THROUGH THE SCRIPT LOGIC OF \n {{script}} \n and think about where the variables are printed and where the logic is to be able to print them out.
    """
    prompt = (
        f"Error Message:\n{error_message}\n\n"
        "Provide only the pdb commands, one per line, to debug this error automatically. "
    )
    return f"Given the error message:\n{error_message} and the script: \n{script}\n\nPlease provide only the pdb commands needed to debug this error, one command per line."