# -*- coding: utf-8 -*-
import ctypes
from ctypes.util import find_library
import pathlib

from qlazy.config import *
from qlazy.error import *
from qlazy.util import *
from qlazy.MData import *

lib= ctypes.CDLL(str(pathlib.Path(__file__).with_name('libqlz.'+get_lib_ext())))
libc = ctypes.CDLL(find_library("c"),mode=ctypes.RTLD_GLOBAL)

class MDataC(ctypes.Structure):

    _fields_ = [
        ('qubit_num', ctypes.c_int),
        ('state_num', ctypes.c_int),
        ('shot_num', ctypes.c_int),
        ('angle', ctypes.c_double),
        ('phase', ctypes.c_double),
        ('qubit_id', ctypes.c_int*MAX_QUBIT_NUM),
        ('freq', ctypes.POINTER(ctypes.c_int)),
        ('last', ctypes.c_int),
    ]

    def show(self):

        mdata_print(self)
        
    @property
    def frq(self):

        try:
            freq = ctypes.cast(self.freq, ctypes.POINTER(ctypes.c_int*self.state_num))
            freq_list = [freq.contents[i] for i in range(self.state_num)]
        except Exception:
            raise MData_Error_GetFrq()
        
        return np.array(freq_list)

    @property
    def lst(self):

        return self.last
            
    def free(self):

        mdata_free(self)

def mdata_print(md):

    lib.mdata_print.restype = ctypes.c_int
    lib.mdata_print.argtypes = [ctypes.POINTER(MDataC)]
    ret = lib.mdata_print(ctypes.byref(md))

    if ret == FALSE:
        raise MData_Error_Show()


def mdata_free(md):

    lib.mdata_free.argtypes = [ctypes.POINTER(MDataC)]
    lib.mdata_free(ctypes.byref(md))
