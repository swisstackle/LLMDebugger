
# Automated LLM based PDB Debugger Assistant

## Description

This repository's goal is to teach LLM's how to debug Python code. It does so by generating pdb commands based on the code structure and error message and then feeding the results to an LLM to generate a report.
Currently, it only generates and executes the commands but does not feed the results to an LLM yet.



## Features

- **Automatic Breakpoint Setting**: Identifies executable lines and sets breakpoints.
- **Variable Monitoring**: Automatically prints the values of variables at each step.

## Dependencies

- `ast`: Standard library for parsing Python code.
- `pdb`: Standard library for debugging.
- `openai`: API for generating commands.
- `ell-ai`: LLM Library for nested prompt engineering.



## Usage

1. **Prepare Your Script**
   
   Ensure your Python script is ready and contains the code you want to debug. For example, `testscript.py`:
   
   ```python
   def divide(a, b):
       return a / b
   
   result = divide(10, 0)  # This will cause a ZeroDivisionError
   print(result)
   ```

2. **Run the Ell Debugger**
   
   Use the `elldebugger.py` to analyze the error and automate the debugging process.
   
   ```bash
   python elldebugger.py testscript.py
   ```

## Project Structure

- `generate_commands.py`: Parses scripts and generates `pdb` commands.
- `auto_pdb.py`: Extends `pdb.Pdb` to execute commands and capture output.
- `debugger_assistant.py`: Main interface to analyze errors and automate debugging.
- `testscript.py`: Example script to demonstrate debugging.
- `test_generate_commands.py`: Tests for the command generation functionality.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
