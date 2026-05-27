__all__ = ['SubJobState']

import enum as _enum

class SubJobState(_enum.Enum):
    """ Represents the state of a job """

    INIT = _enum.auto()
    """ Job is initializing """

    RUNNING = _enum.auto()
    """ Job is running """

    FINISHED = _enum.auto()
    """ Job has completed """

    CANCELLED = _enum.auto()
    """ Job was cancelled """

    ERROR = _enum.auto()
    """ Job encountered an error """