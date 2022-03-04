# -*- coding: utf-8 -*-
""" Result of quantum circuit execution """

from collections import Counter

from qlazy.Backend import Backend

class Result:
    """ Result of quantum circuit execution

    Attributes
    ----------
    cid : list
        classical register id list to get frequencys.
    freqency : instance of Counter
        frequencies of measured value.
    elapsed_time : float
        elapsed time to ececute the quantum circuit.
    backend : instance of Backend
        backend device of quantum computing
    info : dict
        result informations relating to the backend device

    """
    # def __init__(self, cid=None, frequency=None, elapsed_time=None,
    #              backend=None, info=None):
    # 
    #     self.__cid = cid
    #     self.__frequency = frequency
    #     self.__elapsed_time = elapsed_time
    #     self.__backend = backend
    #     self.__info = info

    def __init__(self):

        self.__cid = None
        self.__frequency = None
        self.__elapsed_time = None
        self.__backend = None
        self.__info = None

    @property
    def cid(self):
        pass

    @cid.setter
    def cid(self, cid):
        if isinstance(cid, list) is not True:
            raise TypeError("type of cid must be list.")
        self.__cid = cid

    @cid.getter
    def cid(self):
        return self.__cid

    @property
    def frequency(self):
        pass

    @frequency.setter
    def frequency(self, frequency):
        if isinstance(frequency, Counter) is not True and frequency is not None:
            raise TypeError("type of frequency must be Counter.")
        self.__frequency = frequency

    @frequency.getter
    def frequency(self):
        return self.__frequency

    @property
    def elapsed_time(self):
        pass

    @elapsed_time.setter
    def elapsed_time(self, elapsed_time):
        if isinstance(elapsed_time, float) is not True:
            raise TypeError("type of elaased_time must be float.")
        self.__elapsed_time = elapsed_time

    @elapsed_time.getter
    def elapsed_time(self):
        return self.__elapsed_time

    @property
    def backend(self):
        pass

    @backend.setter
    def backend(self, backend):
        if isinstance(backend, Backend) is not True:
            raise TypeError("type of backend must be Backend.")
        self.__backend = backend

    @backend.getter
    def backend(self):
        return self.__backend

    @property
    def info(self):
        pass

    @info.setter
    def info(self, info):
        if isinstance(info, dict) is not True:
            raise TypeError("type of info must be dict.")
        self.__info = info

    @info.getter
    def info(self):
        return self.__info
