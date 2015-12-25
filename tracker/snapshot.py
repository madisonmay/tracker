import textwrap
from itertools import izip_longest

from .tracker import __file__ as SOURCE_FILE

class Snapshot(object):
    """
    Represents the state of all tracked variables at a given point in time
    Also stores a record of the code that produced the last modification
    """
    def __init__(self, state=None, stack=None, context=1):
        self.state = state
        self.stack = stack
        self._context = context

    @classmethod
    def valid_frame(cls, frame):
        # exclude frames from tracker source
        if SOURCE_FILE.startswith(frame.file):
            return False
        return True

    @classmethod
    def format_frame(cls, frame):
        code = Snapshot.format_code(
            filename=frame.file, line_number=frame.line, context=frame.context
        )
        return "%s:%d\n%s" % (frame.file, frame.line, code)

    @classmethod
    def format_code(cls, filename, line_number, context):
        code_start = line_number - context - 1
        code_end = line_number + context
        code = open(filename).readlines()[code_start:code_end]
        lines = textwrap.dedent("".join(code)).split('\n')[:-1]
        line_numbers = range(code_start + 1, code_end + 1)
        text = ""
        for line_number, code_line in izip_longest(line_numbers, code):
            text += "  {line_number}{code}".format(
                line_number=str(line_number).ljust(8),
                code=(code_line or "\n")
            )
        return text

    def __getitem__(self, name):
        return self.state.__getitem__(name)

    def __repr__(self):
        state = repr(self.state)
        divider = '-' * 80 
        frames = "\n".join(
            [
                Snapshot.format_frame(frame) for frame in self.stack
                if Snapshot.valid_frame(frame)
            ]
        )
        return "\n{state}\n{divider}\n{frames}".format(
            state=state, divider=divider, frames=frames
        )
