# -*- coding: utf-8 -*-
""" Result of quantum circuit execution """

class Result:
    """ Result of quantum circuit execution

    Attributes
    ----------
    cid : list
        classical register id list to get frequencys.
    freqency : instance of Counter
        frequencies of measured value.
    backend : instance of Backend
        backend device of quantum computing
    info : dict
        result informations relating to the backend device

    """
    def __init__(self, cid=None, frequency=None, backend=None, info=None):

        self.cid = cid
        self.frequency = frequency
        self.backend = backend
        self.info = info
