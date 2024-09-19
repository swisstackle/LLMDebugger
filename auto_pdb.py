import pdb

class AutoPdb(pdb.Pdb):
    def __init__(self, commands, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = commands
        self.current_command = 0

    def interaction(self, frame, traceback):
        while self.current_command < len(self.commands):
            cmd = self.commands[self.current_command].strip()
            print(f">>> {cmd}")  # Log the command being executed
            self.current_command += 1
            # Use try-except to handle any unexpected pdb command errors
            try:
                self.onecmd(cmd)
            except Exception as e:
                print(f"Error executing command '{cmd}': {e}")
        # After executing all commands, continue execution
        self.set_continue()

    def set_continue(self):
        self.do_continue('')  # Continue execution after all commands