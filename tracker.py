from collections import namedtuple
from operator import itemgetter
import textwrap
import inspect


Frame = namedtuple('Frame', ['file', 'line', 'code'])
Step = namedtuple('Step', ['name', 'value', 'stack'])


class Snapshot(object):

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
        print len(lines)
        context = len(lines) / 2
        line_numbers = range(line_number - context, line_number + context + 1)
        text = ""
        for i, line in enumerate(lines):
            text += "  " + str(line_numbers[i]).ljust(8) + line + "\n"
        return text

    def __repr__(self):
        state = repr(self.state)
        return "\n%s\n" % self.state + "\n".join(
            [Snapshot.format_frame(frame) for frame in self.stack]
        )
 
def tracked(*tracked, **kwargs):
    code_context = kwargs.pop('code_context', 1)

    def decorate(basetype):

        class Tracker(basetype):

            def __init__(self, *args, **kwargs):
                self.__history = []
                super(Tracker, self).__init__(*args, **kwargs)

            def __setattr__(self, name, value):
                if name in tracked:
                    stack = inspect.stack(context=code_context*2+1)
                    frames = [
                        Frame(
                            file=frame[1],
                            line=frame[2],
                            code=frame[4]
                        ) for frame in stack[1:]
                    ]
                    self.__history.append(
                        Step(
                            name=name,
                            value=value,
                            stack=frames
                        )
                    )
                return super(Tracker, self).__setattr__(name, value)

            def replay(self, names=tracked):
                state = {}
                for step in self.__history:
                    if step.name in names:
                        state[step.name] = step.value
                        yield Snapshot(
                            state=state, 
                            stack=step.stack,
                        )


        # preserve metadata
        Tracker.__module__ = basetype.__module__
        Tracker.__name__ = basetype.__name__

        return Tracker

    return decorate


if __name__ == "__main__":
    from pprint import pprint

    @tracked('x', 'y', code_context=1)
    class Namespace(object): pass

    data = Namespace()
    data.x = 5
    data.y = 10
    data.x += 1
    data.x += 1
    data.y += 1
    data.x += (
        1
    )
    for state in data.replay():
        print state

    # data = tracked(dict)('x', 'y')()
    # data.x = 5
    # data.x = 10
    # data.y = 1
    # print data.history('x')
    # print data.history('y')
