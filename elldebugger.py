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
def assist_debugger_main(error_message: str, script_path: str, numbered_script: str) -> str:
    """Invoke the automated debugger assistant."""
    return assist_debugger(error_message, script_path, numbered_script)

def main():
    script_path = "testscript.py"
    # We will create a line numbered version of the script to pass to the LLM
    script = open(script_path, 'r').read()
    lines = script.split('\n')
    numbered_script = "\n".join([f"{i+1}: {line}" for i, line in enumerate(lines)])
    print(numbered_script + "\n")
    # Detect errors in the script
    error = detect_error(script_path)
    
    assist_debugger_main(error, script_path, numbered_script)

if __name__ == "__main__":
    main()