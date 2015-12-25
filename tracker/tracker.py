from collections import namedtuple
import inspect

from .snapshot import Snapshot


Frame = namedtuple('Frame', ['file', 'line', 'context'])
Step = namedtuple('Step', ['name', 'value', 'stack'])

def tracked(*tracked, **kwargs):
    code_context = kwargs.pop('code_context', 1)

    def decorate(basetype):

        class Tracker(basetype):
            """
            Mimics the interface of the type it subclasses, and logs to self.__history
            when tracked attributes are modified using __setattr__ or __setitem__.
            """
            def __init__(self, *args, **kwargs):
                self._history = []
                self._tracked = tracked
                super(Tracker, self).__init__(*args, **kwargs)

            def __capture_state(self, name, value):
                """
                Capture the state of a name, value pair along with the code
                that caused the modification
                """
                stack = inspect.stack()
                frames = [
                    Frame(
                        file=frame[1],
                        line=frame[2],
                        context=code_context
                    ) for frame in reversed(stack)
                ]
                self._history.append(
                    Step(
                        name=name,
                        value=value,
                        stack=frames
                    )
                )

            def __setattr__(self, name, value):
                """
                Inject code to capture modifications of tracked attributes
                """
                if name in tracked:
                    self.__capture_state(name, value)
                return super(Tracker, self).__setattr__(name, value)

            def __setitem__(self, name, value):
                """
                Enable tracking modifications of objects that subclass `dict`
                """
                if name in tracked:
                    self.__capture_state(name, value)
                return super(Tracker, self).__setitem__(name, value)

            def replay(self, names=None):
                if not names:
                    names = self._tracked
                state = {}
                for step in self._history:
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
