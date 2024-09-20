import pdb

class AutoPdb(pdb.Pdb):
    def __init__(self, commands, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate the command queue with the commands
        self.cmdqueue = list(commands) + self.cmdqueue