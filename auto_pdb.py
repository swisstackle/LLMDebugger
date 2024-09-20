import pdb
import sys
from io import StringIO

class AutoPdb(pdb.Pdb):
    def __init__(self, commands, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate the command queue with the commands
        self.cmdqueue = list(commands) + self.cmdqueue
        self.output = []
        self._stdout = sys.stdout
        sys.stdout = self  # Redirect stdout to capture outputs

    def do_print(self, arg):
        try:
            value = eval(arg, self.curframe.f_globals, self.curframe.f_locals)
            self.output.append(f"{arg} = {value}")
            self._stdout.write(f"{arg} = {value}\n")
        except Exception as e:
            self.output.append(f"Error evaluating {arg}: {e}")
            self._stdout.write(f"Error evaluating {arg}: {e}\n")

    def do_quit(self, arg):
        self.set_quit()

    def write(self, data):
        self.output.append(data)

    def get_output(self):
        sys.stdout = self._stdout  # Restore original stdout
        return "\n".join(self.output)

    def run_path(self, path):
        with open(path, "rb") as fp:
            code = compile(fp.read(), path, 'exec')
            self.run(code)