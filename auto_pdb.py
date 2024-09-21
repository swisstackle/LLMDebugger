import pdb
import sys

class AutoPdb(pdb.Pdb):
    def __init__(self, commands, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate the command queue with the generated commands
        self.cmdqueue = list(commands.split('\n')) + self.cmdqueue
        self.output = []
        self._stdout = sys.stdout
        sys.stdout = self  # Redirect stdout to capture outputs

    def write(self, data):
        self.output.append(data)

    def flush(self):
        """Handle flush calls."""
        pass  # No action needed as data is being captured

    def get_output(self):
        sys.stdout = self._stdout  # Restore original stdout
        return "\n".join(self.output)

    def run_path(self, path):
        with open(path, "rb") as fp:
            code = compile(fp.read(), path, 'exec')
            self.run(code)