__all__ = ['SubProcessState']

import enum as _enum

class SubProcessState(_enum.Enum):
    """ Represents the state of a process """

    INIT = _enum.auto()
    """ Process is initializing """

    RUNNING = _enum.auto()
    """ Process is running """

    FINISHED = _enum.auto()
    """ Process has completed """

    CANCELLED = _enum.auto()
    """ Process was cancelled """

    ERROR = _enum.auto()
    """ Process encountered an error """