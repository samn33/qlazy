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

    return c_qcirc

def qcirc_copy(qc):

    qcirc = None
    c_qcirc = ctypes.c_void_p(qcirc)
            
    lib.qcirc_copy.restype = ctypes.c_int
    lib.qcirc_copy.argtypes = [ctypes.POINTER(QCirc),
                               ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.qcirc_copy(ctypes.byref(qc), c_qcirc)

    if ret == FALSE:
        raise QCirc_Error_Copy()

    return c_qcirc

def qcirc_merge(qc_L, qc_R):

    qcirc = None
    c_qcirc = ctypes.c_void_p(qcirc)
            
    lib.qcirc_merge.restype = ctypes.c_int
    lib.qcirc_merge.argtypes = [ctypes.POINTER(QCirc), ctypes.POINTER(QCirc),
                               ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.qcirc_merge(ctypes.byref(qc_L), ctypes.byref(qc_R), c_qcirc)

    if ret == FALSE:
        raise QCirc_Error_Merge()

    return c_qcirc

def qcirc_is_equal(qc_L, qc_R):

    ans = True
    c_ans = ctypes.c_bool(ans)
            
    lib.qcirc_is_equal.restype = ctypes.c_int
    lib.qcirc_is_equal.argtypes = [ctypes.POINTER(QCirc), ctypes.POINTER(QCirc),
                                   ctypes.POINTER(ctypes.c_bool)]
    ret = lib.qcirc_is_equal(ctypes.byref(qc_L), ctypes.byref(qc_R), ctypes.byref(c_ans))

    if ret == FALSE:
        raise QCirc_Error_Merge()

    ans = c_ans.value
    return ans

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
    
def qcirc_kind_first(qc):

    kind = 0
    c_kind = ctypes.c_int(kind)
            
    lib.qcirc_kind_first.restype = ctypes.c_int
    lib.qcirc_kind_first.argtypes = [ctypes.POINTER(QCirc), ctypes.POINTER(ctypes.c_int)]
    ret = lib.qcirc_kind_first(ctypes.byref(qc), ctypes.byref(c_kind))

    if ret == FALSE:
        raise QState_Error_KindFirst()

    kind = c_kind.value

    if kind == NOT_A_GATE:
        kind = None
    
    return kind

def qcirc_pop_gate(qc):

    kind = 0
    c_kind = ctypes.c_int(kind)
    qid = [0] * 2
    IntArray = ctypes.c_int * 2
    c_qid = IntArray(*qid)
    para = [0.0] * 3
    DoubleArray = ctypes.c_double * 3
    c_para = DoubleArray(*para)
    c = -1
    c_c = ctypes.c_int(c)
    ctrl = -1
    c_ctrl = ctypes.c_int(ctrl)
            
    lib.qcirc_pop_gate.restype = ctypes.c_int
    lib.qcirc_pop_gate.argtypes = [ctypes.POINTER(QCirc), ctypes.POINTER(ctypes.c_int),
                                     ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double),
                                     ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
                                     
    ret = lib.qcirc_pop_gate(ctypes.byref(qc), ctypes.byref(c_kind), c_qid, c_para,
                             ctypes.byref(c_c), ctypes.byref(c_ctrl))

    if ret == FALSE:
        raise QState_Error_PopGate()

    kind = c_kind.value
    qid = [c_qid[i] for i in range(2)]
    para = [c_para[i] for i in range(3)]
    c = c_c.value
    ctrl = c_ctrl.value

    if c == -1: c = None
    if ctrl == -1: ctrl = None

    return (kind, qid, para, c, ctrl)
    
def qcirc_free(qcirc):

    lib.qcirc_free.argtypes = [ctypes.POINTER(QCirc)]
    lib.qcirc_free(ctypes.byref(qcirc))
