# -*- coding: utf-8 -*-
import ctypes
from ctypes.util import find_library
import pathlib
from collections import Counter

from qlazy.config import *
from qlazy.error import *
from qlazy.util import *

class MData(ctypes.Structure):

    _fields_ = [
        ('qubit_num', ctypes.c_int),
        ('shot_num', ctypes.c_int),
        ('angle', ctypes.c_double),
        ('phase', ctypes.c_double),
        ('qubit_id', ctypes.POINTER(ctypes.c_int)),
        ('freq', ctypes.POINTER(ctypes.c_int)),
        ('last_val', ctypes.c_int),
    ]

    def __new__(cls, qubit_num=None, shots=1, angle=0.0, phase=0.0, qid=[], **kwargs):
        """
        Parameters
        ----------
        None

        Returns
        -------
        md : instance (QCirc)

        """
        obj = mdata_init(qubit_num, shots, angle, phase, qid)
        md = ctypes.cast(obj.value, ctypes.POINTER(cls)).contents
        return md

    def __str__(self):

        s = ""
        s += "measured direction (theta, phi): {0:}*PI, {1:}*PI\n".format(self.angle, self.phase)
        s += "measured qubit id: {}\n".format([self.qubit_id[i] for i in range(self.qubit_num)])
        s += "frequency: {}\n".format(self.frequency)
        s += "last state: {}".format(self.last)
        return s
    
    def show(self):

        mdata_print(self)

    @property
    def last(self):
        """ last measured value (binary string) """
        mval = self.last_val
        digits = self.qubit_num
        return '{:0{digits}b}'.format(mval, digits=digits)
            
    @property
    def lst(self):
        """ last measured value (integer) """
        return self.last_val
            
    @property
    def frequency(self):
        """ frequencies of measured value (Counter) """
        state_num = 2**self.qubit_num
        frq = [self.freq[i] for i in range(state_num)]
        digits = self.qubit_num
        res = {"{:0{digits}b}".format(k, digits=digits):v
               for k,v in enumerate(frq) if v > 0}
        return Counter(res)
            
    @property
    def frq(self):
        """ frequencies of measured value (list) """
        state_num = 2**self.qubit_num
        freq_list = [0] * state_num
        for k, v in self.frequency.items():
            i = int(k, 2)
            freq_list[i] = v
        return freq_list

    @property
    def state_num(self):
        return 2**self.qubit_num
        
    def __del__(self):

        mdata_free(self)
        
# c-library for qstate
from qlazy.lib.mdata_c import *
