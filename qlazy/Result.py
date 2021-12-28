# -*- coding: utf-8 -*-
from collections import Counter

from qlazy.config import *
from qlazy.error import *

class Result:
    """ Result data of running quantum computer

    Attributes
    ----------
    cid : list
        classical register id list to get frequencys.
    freqency : Counter
        frequencies of measured value.

    """
    def __init__(self, cid=None, frequency=None):

        self.cid = cid
        self.frequency = frequency
