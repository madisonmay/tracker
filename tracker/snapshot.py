import textwrap


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
    def format_frame(cls, frame):
        return "%s:%d\n%s" % (
            frame.file, frame.line, Snapshot.format_code(frame.code, line_number=frame.line)
        )

    @classmethod
    def format_code(cls, code, line_number):
        lines = textwrap.dedent("".join(code)).split('\n')[:-1]
        context = len(lines) / 2
        line_numbers = range(line_number - context, line_number + context + 1)
        text = ""
        for i, line in enumerate(lines):
            text += " {numbers}{code}\n".format(
                numbers=str(line_numbers[i]).ljust(8),
                code=line
            )
        return text

    def __getitem__(self, name):
        return self.state.__getitem__(name)

    def __repr__(self):
        state = repr(self.state)
        return "\n%s\n" % self.state + "\n".join(
            [Snapshot.format_frame(frame) for frame in self.stack]
        )
