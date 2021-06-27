# -*- coding: utf-8 -*-
import ctypes
from ctypes.util import find_library
import numpy as np
import pathlib

from qlazy.config import *
from qlazy.error import *
from qlazy.util import *
from qlazy.MData import *
from qlazy.QCirc import QCirc
from qlazy.lib.mdata_c import *

lib= ctypes.CDLL(str(pathlib.Path(__file__).with_name('libqlz.'+get_lib_ext())))
libc = ctypes.CDLL(find_library("c"),mode=ctypes.RTLD_GLOBAL)

def qcirc_init():

    qcirc = None
    c_qcirc = ctypes.c_void_p(qcirc)

    lib.qcirc_init.restype = ctypes.c_int
    lib.qcirc_init.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.qcirc_init(c_qcirc)

    if ret == FALSE:
        raise QCirc_Error_Initialize()

    out = ctypes.cast(c_qcirc.value, ctypes.POINTER(QCirc))
        
    return out.contents

def qcirc_append_gate(qcirc, kind, qid, para, c, ctrl):

    if para == None: para = [0.0, 0.0, 0.0]
    if c == None: c = -1
    if ctrl == None: ctrl = -1
    
    qid_num = len(qid)
    para_num = len(para)
    IntArray = ctypes.c_int * qid_num
    DoubleArray = ctypes.c_double * para_num
    c_qid = IntArray(*qid)
    c_para = DoubleArray(*para)
    
    lib.qcirc_append_gate.restype = ctypes.c_int
    lib.qcirc_append_gate.argtypes = [ctypes.POINTER(QCirc), ctypes.c_int, IntArray, DoubleArray,
                                      ctypes.c_int, ctypes.c_int]
    ret = lib.qcirc_append_gate(ctypes.byref(qcirc), ctypes.c_int(kind), c_qid, c_para,
                                ctypes.c_int(c), ctypes.c_int(ctrl))

    if ret == FALSE:
        raise QCirc_Error_AppendGate()
    
def qcirc_free(qcirc):

    lib.qcirc_free.argtypes = [ctypes.POINTER(QCirc)]
    lib.qcirc_free(ctypes.byref(qcirc))
