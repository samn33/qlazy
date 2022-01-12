# -*- coding: utf-8 -*-
from collections import Counter

from qlazy.config import *
from qlazy.error import *

class Result:
    """ Result of quantum circuit execution

    Attributes
    ----------
    cid : list
        classical register id list to get frequencys.
    freqency : Counter
        frequencies of measured value.
    backend : instance of Backend
        backend device of quantum computing
    info : dict
        result information relating to the backend device

    """
    def __init__(self, cid=None, frequency=None, backend=None, info=None):

        self.cid = cid
        self.frequency = frequency
        self.backend = backend
        self.info = info
