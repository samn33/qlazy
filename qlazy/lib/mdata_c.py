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

def mdata_init(qubit_num=None, shots=1, angle=0.0, phase=0.0, qid=None):

    if qid is None or qid == []:
        qid = [i for i in range(qubit_num)]
        
    IntArray = ctypes.c_int * MAX_QUBIT_NUM
    qid_array = IntArray(*qubit_id)
    
    mdata = None
    c_mdata = ctypes.c_void_p(mdata)

    lib.mdata_init.restype = ctypes.c_int
    lib.mdata_init.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double,
                               IntArray, ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.mdata_init(ctypes.c_int(qubit_num), ctypes.c_int(shots),
                         ctypes.c_double(angle), ctypes.c_double(phase), qid_array, c_mdata)

    if ret == FALSE:
        raise MData_Error_Initialize()

    return c_mdata


def mdata_print(md):

    lib.mdata_print.restype = ctypes.c_int
    lib.mdata_print.argtypes = [ctypes.POINTER(MData)]
    ret = lib.mdata_print(ctypes.byref(md))

    if ret == FALSE:
        raise MData_Error_Show()

def mdata_free(md):

    lib.mdata_free.argtypes = [ctypes.POINTER(MData)]
    lib.mdata_free(ctypes.byref(md))
