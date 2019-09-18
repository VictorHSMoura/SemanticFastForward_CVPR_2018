class InputError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return str(self.msg)

class BuildError(Exception): # pragma: no cover
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return str(self.msg)