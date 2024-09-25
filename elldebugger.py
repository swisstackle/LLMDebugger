import ell
from openai import Client
import os
import subprocess
import argparse
import glob
import shutil

# Initialize OpenAI client with environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not set. Please set the OPENAI_API_KEY environment variable.")

openai_client = Client(api_key=openai_api_key)
ell.init(default_openai_client=openai_client, store='./logdir', autocommit=True, verbose=True)

def detect_error(script_path: str) -> str:
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

# ... other existing functions ...

def collect_project_files(project_dir: str) -> list:
    """
    Collect all Python files within the project directory recursively.

    Args:
        project_dir (str): Root directory of the project.

    Returns:
        list: List of file paths.
    """
    pattern = os.path.join(glob.escape(project_dir), '**', '*.py')
    return glob.glob(pattern, recursive=True)


def insert_trace_code(original_script: str, script_path: str, project_files: list, report_path: str) -> None:
    """
    Insert the custom_trace function and sys.settrace calls into the original script.

    Args:
        original_script (str): Content of the original script.
        script_path (str): Path to the original script to modify.
        project_files (list): List of project file paths.
        report_path (str): Absolute path to the debug report file.
    """
    # Backup the original script
    backup_path = f"{script_path}.bak"
    shutil.copyfile(script_path, backup_path)

    # Convert project file paths to absolute paths in a Python list format
    # Escape backslashes in paths by replacing '\' with '\\'
    project_files_list = repr([os.path.abspath(path) for path in project_files])

    # Escape backslashes in report_path
    escaped_report_path = repr(report_path)

    custom_trace_code = f"""
import sys
import trace
import linecache
import os

project_files = {project_files_list}
report_path = {escaped_report_path}
global report_file
report_file = open(report_path, 'a')

def custom_trace(frame, event, arg):
    if event == 'line' and os.path.abspath(frame.f_code.co_filename) in project_files:
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        line = linecache.getline(filename, lineno).strip()
        local_vars = frame.f_locals
        report_file.write(f"Line {{lineno}}: {{line}}\\n")
        report_file.write(f"Variables: {{local_vars}}\\n")
        report_file.write("---\\n")
        
    return custom_trace
sys.settrace(custom_trace)
"""

    end_trace_code = """
sys.settrace(None)
report_file.close()
"""

    with open(script_path, 'w') as script_file:
        # Insert custom_trace at the beginning
        script_file.write(custom_trace_code)
        script_file.write(original_script)
        # Insert sys.settrace(None) at the end
        script_file.write(end_trace_code)

def main():
    parser = argparse.ArgumentParser(description="Debug a Python script.")
    parser.add_argument("script_path", help="Path to the script to debug.")
    parser.add_argument("--project_dir", default='.', help="Root directory of the project.")
    args = parser.parse_args()
    script_path = args.script_path
    project_dir = args.project_dir

    # Collect project files
    project_files = collect_project_files(project_dir)

    # Read the original script
    with open(script_path, 'r') as f:
        original_script = f.read()

    # Define the absolute path for debug_report.txt
    report_path = os.path.abspath('debug_report.txt')

    # Insert trace code into the original script
    insert_trace_code(original_script, script_path, project_files, report_path)

    try:
        # Execute the modified script
        error = detect_error(script_path)
        print(error)
    finally:
        # Restore the original script from backup
        shutil.move(f"{script_path}.bak", script_path)

if __name__ == "__main__":
    main()