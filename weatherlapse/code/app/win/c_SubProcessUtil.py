__all__ = ['SubProcessUtil']

import multiprocessing as _mp

import code.engine.help as _help

from .c_SubProcessState import SubProcessState as _SubProcessState

class SubProcessUtil:
    """ Utility for process-related operations """
    
    @classmethod
    def user_cancelled(cls, iqueue:_mp.Queue):
        """
        Reads the queue to determine if the user wants to cancel

        :param iqueue: Input queue
        :return: Whether or not the user wants to cancel
        """
        cancelled = False
        # Read entire queue
        while not iqueue.empty():
            if iqueue.get_nowait() == 'CANCEL':
                cancelled = True
        # Return
        return cancelled

    @classmethod
    def output_init(cls, oqueue:_mp.Queue):
        """
        Indicate that the process is still initializing

        :param oqueue: Output queue
        """
        oqueue.put(str(_SubProcessState.INIT.value))

    @classmethod
    def output_running(cls, oqueue:_mp.Queue, progress:float = 0, message:str = ""):
        """
        Indicate that the process is currently running

        :param oqueue: Output queue
        :param progress: Progress indicater (in percent)
        :param message: Message about current progress
        """
        oqueue.put(f"{_SubProcessState.RUNNING.value} {progress} {_help.StrUtil.from_argv(message)}")

    @classmethod
    def output_finished(cls, oqueue:_mp.Queue, *output):
        """
        Indicate that the process has completed

        :param oqueue: Output queue
        :param output: Output
        """
        oqueue.put(f"{_SubProcessState.FINISHED.value} {_help.StrUtil.from_argv(*output)}")

    @classmethod
    def output_cancelled(cls, oqueue:_mp.Queue):
        """
        Indicate that the process has been cancelled

        :param oqueue: Output queue
        """
        oqueue.put(str(_SubProcessState.CANCELLED.value))

    @classmethod
    def output_error(cls, oqueue:_mp.Queue, message):
        """
        Indicate that the process has encountered an error

        :param oqueue: Output queue
        :param message: Error message
        """
        oqueue.put(f"{_SubProcessState.ERROR.value} {_help.StrUtil.from_argv(message)}")