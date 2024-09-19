import ell
from openai import Client
import os
import subprocess
from debugger_assistant import assist_debugger
# Initialize OpenAI client with environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not set. Please set the OPENAI_API_KEY environment variable.")

openai_client = Client(api_key=openai_api_key)
ell.init(default_openai_client=openai_client, store='./logdir', autocommit=True, verbose=True)

@ell.simple(model="gpt-4o-mini")
def detect_error(script_path: str) -> str:
    """Monitor the execution of a Python script and capture error messages."""
    try:
        # Execute the script
        result = subprocess.run(
            ["python", script_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return "No errors detected."
    except subprocess.CalledProcessError as e:
        return e.stderr  # Return the error message

@ell.simple(model="gpt-4o-mini")
def assist_debugger_main(error_message: str, script_path: str) -> str:
    """Invoke the automated debugger assistant."""
    return assist_debugger(error_message, script_path)

def main():
    script_path = "testscript.py"
    
    # Detect errors in the script
    error = detect_error(script_path)
    
    assist_debugger_main(error, script_path)

if __name__ == "__main__":
    main()