# -*- coding: utf-8 -*-
import ctypes
from ctypes.util import find_library
import pathlib

from qlazy.Stabilizer import Stabilizer
from qlazy.error import *
from qlazy.config import *
from qlazy.util import *

lib= ctypes.CDLL(str(pathlib.Path(__file__).with_name('libqlz.'+get_lib_ext())))
libc = ctypes.CDLL(find_library("c"),mode=ctypes.RTLD_GLOBAL)

def stabilizer_init(gene_num=None, qubit_num=None, seed=None):

    lib.init_qlazy(ctypes.c_int(seed))
    
    stab = None
    c_stab = ctypes.c_void_p(stab)
        
    lib.stabilizer_init.restype = ctypes.c_int
    lib.stabilizer_init.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                    ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.stabilizer_init(ctypes.c_int(gene_num), ctypes.c_int(qubit_num),
                              ctypes.c_int(seed), c_stab)

    if ret == FALSE:
        raise Stabilizer_Error_Initialize()
        
    out = ctypes.cast(c_stab.value, ctypes.POINTER(Stabilizer))

    return out.contents

def stabilizer_copy(sb):

    try:
        stab = None
        c_stab = ctypes.c_void_p(stab)
            
        lib.stabilizer_copy.restype = ctypes.c_int
        lib.stabilizer_copy.argtypes = [ctypes.POINTER(Stabilizer),
                                        ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.stabilizer_copy(ctypes.byref(sb), c_stab)

        if ret == FALSE:
            raise Stabilizer_Error_Clone()

        out = ctypes.cast(c_stab.value, ctypes.POINTER(Stabilizer))

        return out.contents
        
    except Exception:
        raise Stabilizer_Error_Clone()

def stabilizer_set_pauli_fac(sb, gene_id, pauli_fac):

    lib.stabilizer_set_pauli_fac.restype = ctypes.c_int
    lib.stabilizer_set_pauli_fac.argtypes = [ctypes.POINTER(Stabilizer), ctypes.c_int,
                                             ctypes.c_int]
    ret = lib.stabilizer_set_pauli_fac(ctypes.byref(sb), ctypes.c_int(gene_id),
                                       ctypes.c_int(pauli_fac))

    if ret == FALSE:
        raise Stabilizer_Error_SetPauliFac()

    return ret
    
def stabilizer_get_pauli_fac(sb, gene_id):

    pauli_fac = REAL_PLUS
    c_pauli_fac = ctypes.c_int(pauli_fac)

    lib.stabilizer_get_pauli_fac.restype = ctypes.c_int
    lib.stabilizer_get_pauli_fac.argtypes = [ctypes.POINTER(Stabilizer), ctypes.c_int,
                                             ctypes.POINTER(ctypes.c_int)]
    ret = lib.stabilizer_get_pauli_fac(ctypes.byref(sb), ctypes.c_int(gene_id),
                                       ctypes.byref(c_pauli_fac))

    if ret == FALSE:
        raise Stabilizer_Error_GetPauliFac()

    pauli_fac = c_pauli_fac.value

    return pauli_fac

def stabilizer_set_pauli_op(sb, gene_id=None, qubit_id=None, pauli_op=None):

    lib.stabilizer_set_pauli_op.restype = ctypes.c_int
    lib.stabilizer_set_pauli_op.argtypes = [ctypes.POINTER(Stabilizer), ctypes.c_int,
                                            ctypes.c_int, ctypes.c_int]
    ret = lib.stabilizer_set_pauli_op(ctypes.byref(sb), ctypes.c_int(gene_id),
                                      ctypes.c_int(qubit_id), ctypes.c_int(pauli_op))

    if ret == FALSE:
        raise Stabilizer_Error_SetPauliOp()

    return ret

def stabilizer_get_pauli_op(sb, gene_id=None, qubit_id=None):

    pauli_op = IDENTITY
    c_pauli_op = ctypes.c_int(pauli_op)

    lib.stabilizer_get_pauli_op.restype = ctypes.c_int
    lib.stabilizer_get_pauli_op.argtypes = [ctypes.POINTER(Stabilizer), ctypes.c_int,
                                            ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    ret = lib.stabilizer_get_pauli_op(ctypes.byref(sb), ctypes.c_int(gene_id),
                                      ctypes.c_int(qubit_id), ctypes.byref(c_pauli_op))

    if ret == FALSE:
        raise Stabilizer_Error_GetPauliOp()

    pauli_op = c_pauli_op.value

    return pauli_op

def stabilizer_operate_qgate(sb, kind=None, q0=None, q1=None):

    lib.stabilizer_operate_qgate.restype = ctypes.c_int
    lib.stabilizer_operate_qgate.argtypes = [ctypes.POINTER(Stabilizer), ctypes.c_int,
                                             ctypes.c_int, ctypes.c_int]
    ret = lib.stabilizer_operate_qgate(ctypes.byref(sb), ctypes.c_int(kind),
                                       ctypes.c_int(q0), ctypes.c_int(q1))
    
    if ret == FALSE:
        raise Stabilizer_Error_OperateQgate()
    
def stabilizer_get_rank(sb):

    rank = 0
    c_rank = ctypes.c_int(rank)

    lib.stabilizer_get_rank.restype = ctypes.c_int
    lib.stabilizer_get_rank.argtypes = [ctypes.POINTER(Stabilizer),
                                        ctypes.POINTER(ctypes.c_int)]
    ret = lib.stabilizer_get_rank(ctypes.byref(sb), ctypes.byref(c_rank))
    
    if ret == FALSE:
        raise Stabilizer_Error_GetRank()

    rank = c_rank.value

    return rank
    
def stabilizer_measure(sb, q=None):

    prob = [0.0, 0.0]
    DoubleArray = ctypes.c_double * 2
    c_prob = DoubleArray(*prob)

    mval = 0
    c_mval = ctypes.c_int(mval)

    lib.stabilizer_measure.restype = ctypes.c_int
    lib.stabilizer_measure.argtypes = [ctypes.POINTER(Stabilizer), ctypes.c_int,
                                       DoubleArray, ctypes.POINTER(ctypes.c_int)]
    ret = lib.stabilizer_measure(ctypes.byref(sb), ctypes.c_int(q),
                                 c_prob, ctypes.byref(c_mval))
    
    if ret == FALSE:
        raise Stabilizer_Error_Measure()

    mval = c_mval.value

    return mval
    
def stabilizer_free(stab):

    lib.stabilizer_free.argtypes = [ctypes.POINTER(Stabilizer)]
    lib.stabilizer_free(ctypes.byref(stab))
