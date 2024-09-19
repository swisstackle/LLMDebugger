import ell

@ell.simple(model="gpt-4o-mini")
def generate_commands(error_message: str) -> str:
    """
    You are an expert Python debugger. Given an error message, generate a sequence of pdb commands to debug the issue.
    Commands should be in the order they need to be executed, one per line, without any explanations or comments.
    """
    return f"Given the error message:\n{error_message}\n\nPlease provide only the pdb commands needed to debug this error, one command per line."