__all__ = [ 'TimeDeltaUtil' ]

import datetime as _dt

from io import\
    StringIO as _StringIO

class TimeDeltaUtil:
    """ Utility for time-delta-related operations """

    @classmethod
    def make_str(cls, timedelta:_dt.timedelta):
        """
        Creates a string representation of a time delta

        :param timedelta: time delta
        :return: Created string
        """
        # Compute hours, minutes, seconds
        _span = timedelta.seconds
        seconds = (_span % 60) + timedelta.microseconds / 1000000
        _span //= 60
        minutes = _span % 60
        hours = _span // 60
        # Create text
        with _StringIO() as _strio:
            _empty = True
            # days
            if timedelta.days > 0:
                _strio.write(f"{timedelta.days} day{('s' if (timedelta.days != 1) else '')}")
                _empty = False
            # hours
            if hours > 0:
                if not _empty: _strio.write("; ")
                _strio.write(f"{hours} hour{('s' if (hours != 1) else '')}")
                _empty = False
            # minutes
            if minutes > 0:
                if not _empty: _strio.write("; ")
                _strio.write(f"{minutes} minute{('s' if (minutes != 1) else '')}")
                _empty = False
            # seconds
            if seconds > 0.0:
                if not _empty: _strio.write("; ")
                _strio.write(f"{seconds} second{('s' if (hours != 1) else '')}")
                _empty = False
            # Success!!!
            return _strio.getvalue()