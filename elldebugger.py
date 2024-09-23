import ell
from openai import Client
import os
import subprocess
from debugger_assistant import assist_debugger
import argparse


# Initialize OpenAI client with environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not set. Please set the OPENAI_API_KEY environment variable.")

openai_client = Client(api_key=openai_api_key)
ell.init(default_openai_client=openai_client, store='./logdir', autocommit=True, verbose=True)

def detect_error(script_path: str) -> str:
    """Monitor the execution of a Python script and capture error messages."""
    try:
        # Execute the script
        subprocess.run(
            ["python", script_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return "No errors detected."
    except subprocess.CalledProcessError as e:
        return e.stderr  # Return the error message

def main():
    parser = argparse.ArgumentParser(description="Debug a Python script.")
    parser.add_argument("script_path", help="Path to the script to debug.")
    args = parser.parse_args()
    script_path = args.script_path
    # We will create a line numbered version of the script to pass to the LLM
    with open(script_path, 'r') as f:
        script = f.read()
    lines = script.split('\n')
    numbered_script = "\n".join([f"{i+1}: {line}" for i, line in enumerate(lines)])
    print(numbered_script + "\n")
    # Detect errors in the script
    error = detect_error(script_path)
    
    assist_debugger(error, script_path, script)

if __name__ == "__main__":
    main()