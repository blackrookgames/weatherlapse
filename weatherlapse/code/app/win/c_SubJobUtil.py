__all__ = ['SubJobUtil']

import multiprocessing as _mp

import code.engine.help as _help

from .c_SubJob_OQEntry import\
    _OQEntry,\
    _OQEntryData_Init,\
    _OQEntryData_Running,\
    _OQEntryData_Finished,\
    _OQEntryData_Cancelled,\
    _OQEntryData_Error

class SubJobUtil:
    """ Utility for job-related operations """

    #region RunInfo

    class RunInfo:
        """ Represents information about job progress """

        #region init

        def __init__(self):
            """ Initializer for RunInfo """
            self.__main_desc:str = ""
            self.__main_prog:_help.ProgTrck = _help.ProgTrck()
            self.__sub_desc:str = ""
            self.__sub_prog:_help.ProgTrck = _help.ProgTrck()

        #endregion

        #region properties

        @property
        def main_desc(self): return self.__main_desc
        @main_desc.setter
        def main_desc(self, value:str): self.__main_desc = value

        @property
        def main_prog(self): return self.__main_prog

        @property
        def sub_desc(self): return self.__sub_desc
        @sub_desc.setter
        def sub_desc(self, value:str): self.__sub_desc = value

        @property
        def sub_prog(self): return self.__sub_prog

        #endregion

    #endregion

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
        Indicate that the job is still initializing

        :param oqueue: Output queue
        """
        oqueue.put(_OQEntry(_OQEntryData_Init()).pickle())
    
    @classmethod
    def output_running(cls, oqueue:_mp.Queue,\
            main_desc:str = "",\
            main_prog:float = 0,\
            sub_desc:str = "",\
            sub_prog:float = 0):
        """
        Indicate that the job is currently running

        :param oqueue: Output queue
        :param main_desc: Main progress description
        :param main_prog: Main progress (in percent)
        :param sub_desc: Sub progress description
        :param sub_prog: Sub progress (in percent)
        """
        oqueue.put(_OQEntry(_OQEntryData_Running(main_desc, main_prog, sub_desc, sub_prog)).pickle())
    
    @classmethod
    def output_running2(cls, oqueue:_mp.Queue, info:'SubJobUtil.RunInfo'):
        """
        Indicate that the job is currently running

        :param oqueue: Output queue
        :param info: Information about job progress
        """
        oqueue.put(_OQEntry(_OQEntryData_Running(\
            info.main_desc,\
            info.main_prog.percent(),\
            info.sub_desc,\
            info.sub_prog.percent())\
            ).pickle())

    @classmethod
    def output_finished(cls, oqueue:_mp.Queue, output:bytes = b""):
        """
        Indicate that the job has completed

        :param oqueue: Output queue
        :param output: Output
        """
        oqueue.put(_OQEntry(_OQEntryData_Finished(output)).pickle())

    @classmethod
    def output_cancelled(cls, oqueue:_mp.Queue):
        """
        Indicate that the job has been cancelled

        :param oqueue: Output queue
        """
        oqueue.put(_OQEntry(_OQEntryData_Cancelled()).pickle())

    @classmethod
    def output_error(cls, oqueue:_mp.Queue, message):
        """
        Indicate that the job has encountered an error

        :param oqueue: Output queue
        :param message: Error message
        """
        oqueue.put(_OQEntry(_OQEntryData_Error(str(message))))