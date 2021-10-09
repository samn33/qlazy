# -*- coding: utf-8 -*-
import ctypes
from ctypes.util import find_library
import math
import numpy as np
import pathlib

from qlazy.config import *
from qlazy.error import *
from qlazy.util import *
from qlazy.QState import QState
from qlazy.DensOp import DensOp

lib= ctypes.CDLL(str(pathlib.Path(__file__).with_name('libqlz.'+get_lib_ext())))
libc = ctypes.CDLL(find_library("c"),mode=ctypes.RTLD_GLOBAL)

def densop_init(qstate=[], prob=[]):
        
    num = len(qstate)

    densop = None
    c_densop = ctypes.c_void_p(densop)

    DoubleArray = ctypes.c_double * num
    prob_array = DoubleArray(*prob)

    QStateArray = QState * num
    qstate_array = QStateArray(*qstate)

    lib.densop_init.restype = ctypes.c_int
    lib.densop_init.argtypes = [ctypes.POINTER(QState),
                                ctypes.POINTER(ctypes.c_double),
                                ctypes.c_int,
                                ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.densop_init(qstate_array, prob_array,
                          ctypes.c_int(num), c_densop)

    if ret == FALSE:
        raise DensOp_Error_Initialize()
            
    # out = ctypes.cast(c_densop.value, ctypes.POINTER(DensOp))
    # return out.contents
    return c_densop

def densop_init_with_matrix(matrix=None):

    densop = None
    c_densop = ctypes.c_void_p(densop)

    row = len(matrix)
    col = row
    size = row * col

    mat_complex = list(matrix.flatten())
    mat_real = [0.0 for _ in range(size)]
    mat_imag = [0.0 for _ in range(size)]
    for i in range(size):
        mat_real[i] = mat_complex[i].real
        mat_imag[i] = mat_complex[i].imag
                
    DoubleArray = ctypes.c_double * size
    c_mat_real = DoubleArray(*mat_real)
    c_mat_imag = DoubleArray(*mat_imag)
            
    lib.densop_init_with_matrix.restype = ctypes.c_int
    lib.densop_init_with_matrix.argtypes = [DoubleArray, DoubleArray,
                                            ctypes.c_int, ctypes.c_int,
                                            ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.densop_init_with_matrix(c_mat_real, c_mat_imag,
                                      ctypes.c_int(row), ctypes.c_int(col),
                                      c_densop)
        
    if ret == FALSE:
        raise DensOp_Error_Initialize()
            
    # out = ctypes.cast(c_densop.value, ctypes.POINTER(DensOp))
    # return out.contents
    return c_densop


def densop_get_elm(de):

    try:
        elm = None
        c_elm = ctypes.c_void_p(elm)

        lib.densop_get_elm.restype = ctypes.c_int
        lib.densop_get_elm.argtypes = [ctypes.POINTER(DensOp),
                                           ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.densop_get_elm(ctypes.byref(de), c_elm)

        if ret == FALSE:
            raise DensOp_Error_GetElm()
            
        o = ctypes.cast(c_elm.value, ctypes.POINTER(ctypes.c_double))

        size = de.row * de.col
        out = [0] * size
        for i in range(size):
            out[i] = complex(round(o[2*i],8),round(o[2*i+1],8))

        libc.free.argtypes = [ctypes.POINTER(ctypes.c_double)]
        libc.free(o)

        return np.array(out).reshape([de.row, de.col])

    except Exception:
        raise DensOp_Error_GetElm()

def densop_reset(de, qid=None):

    if qid is None or qid == []:
        qnum = int(math.log2(de.row))
        qid = [i for i in range(qnum)]

    try:
        qubit_num = len(qid)
        qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
        for i in range(len(qid)):
            qubit_id[i] = qid[i]

        IntArray = ctypes.c_int * MAX_QUBIT_NUM
        qid_array = IntArray(*qubit_id)
            
        lib.densop_reset.restype = ctypes.c_int
        lib.densop_reset.argtypes = [ctypes.POINTER(DensOp),ctypes.c_int, IntArray]
        ret = lib.densop_reset(ctypes.byref(de),ctypes.c_int(qubit_num), qid_array)

        if ret == FALSE:
            raise DensOp_Error_Reset()

    except Exception:
        raise DensOp_Error_Reset()

def densop_print(de, nonzero=False):

    try:
        lib.densop_print.restype = ctypes.c_int
        lib.densop_print.argtypes = [ctypes.POINTER(DensOp), ctypes.c_bool]
        ret = lib.densop_print(ctypes.byref(de), ctypes.c_bool(nonzero))

        if ret == FALSE:
            raise DensOp_Error_Show()

    except Exception:
        raise DensOp_Error_Show()

def densop_copy(de):

    try:
        densop = None
        c_densop = ctypes.c_void_p(densop)
            
        lib.densop_copy.restype = ctypes.c_int
        lib.densop_copy.argtypes = [ctypes.POINTER(DensOp),
                                    ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.densop_copy(ctypes.byref(de), c_densop)

        if ret == FALSE:
            raise DensOp_Error_Clone()

        # out = ctypes.cast(c_densop.value, ctypes.POINTER(DensOp))
        # return out.contents
        return c_densop
        
    except Exception:
        raise DensOp_Error_Clone()

def densop_add(de, densop=None):

    try:
        lib.densop_add.restype = ctypes.c_int
        lib.densop_add.argtypes = [ctypes.POINTER(DensOp), ctypes.POINTER(DensOp)]
        ret = lib.densop_add(ctypes.byref(de), ctypes.byref(densop))

        if ret == FALSE:
            raise DensOp_Error_Add()
        
    except Exception:
        raise DensOp_Error_Add()

    
def densop_mul(de, factor=0.0):

    try:
        lib.densop_mul.restype = ctypes.c_int
        lib.densop_mul.argtypes = [ctypes.POINTER(DensOp), ctypes.c_double]
        ret = lib.densop_mul(ctypes.byref(de), ctypes.c_double(factor))

        if ret == FALSE:
            raise DensOp_Error_Mul()

    except Exception:
        raise DensOp_Error_Mul()

def densop_trace(de):

    try:
        real = 0.0
        imag = 0.0
        c_real = ctypes.c_double(real)
        c_imag = ctypes.c_double(imag)
            
        lib.densop_trace.restype = ctypes.c_int
        lib.densop_trace.argtypes = [ctypes.POINTER(DensOp),
                                     ctypes.POINTER(ctypes.c_double),
                                     ctypes.POINTER(ctypes.c_double)]
        ret = lib.densop_trace(ctypes.byref(de), ctypes.byref(c_real),
                               ctypes.byref(c_imag))

        if ret == FALSE:
            raise DensOp_Error_Trace()

        real = round(c_real.value, 8)
        imag = round(c_imag.value, 8)

        if abs(imag) > EPS:
            raise DensOp_Error_Trace()
                
        return real
        
    except Exception:
        raise DensOp_Error_Trace()

def densop_sqtrace(de):

    try:
        real = 0.0
        imag = 0.0
        c_real = ctypes.c_double(real)
        c_imag = ctypes.c_double(imag)
            
        lib.densop_sqtrace.restype = ctypes.c_int
        lib.densop_sqtrace.argtypes = [ctypes.POINTER(DensOp),
                                       ctypes.POINTER(ctypes.c_double),
                                       ctypes.POINTER(ctypes.c_double)]
        ret = lib.densop_sqtrace(ctypes.byref(de), ctypes.byref(c_real),
                                 ctypes.byref(c_imag))

        if ret == FALSE:
            raise DensOp_Error_SqTrace()

        real = round(c_real.value, 8)
        imag = round(c_imag.value, 8)

        if abs(imag) > EPS:
            raise DensOp_Error_Trace()
                
        return real

    except Exception:
        raise DensOp_Error_SqTrace()

def densop_patrace(de, qid=None):

    try:
        if qid == None:
            raise DensOp_Error_PaTrace()
            
        densop = None
        c_densop = ctypes.c_void_p(densop)
            
        qubit_num = len(qid)
        qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
        for i in range(len(qid)):
            qubit_id[i] = qid[i]
        IntArray = ctypes.c_int * MAX_QUBIT_NUM
        qid_array = IntArray(*qubit_id)

        lib.densop_patrace.restype = ctypes.c_int
        lib.densop_patrace.argtypes = [ctypes.POINTER(DensOp),
                                       ctypes.c_int,IntArray,
                                       ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.densop_patrace(ctypes.byref(de), ctypes.c_int(qubit_num),
                                 qid_array, c_densop)

        if ret == FALSE:
            raise DensOp_Error_PaTrace()
            
        # out = ctypes.cast(c_densop.value, ctypes.POINTER(DensOp))
        # return out.contents
        return c_densop

    except Exception:
        raise DensOp_Error_PaTrace()

def densop_tensor_product(de_0, de_1):

    try:
        densop_out = None
        c_densop_out = ctypes.c_void_p(densop_out)

        lib.densop_tensor_product.restype = ctypes.c_int
        lib.densop_tensor_product.argtypes = [ctypes.POINTER(DensOp),
                                              ctypes.POINTER(DensOp),
                                              ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.densop_tensor_product(ctypes.byref(de_0),ctypes.byref(de_1),
                                        c_densop_out)

        if ret == FALSE:
            raise DensOp_Error_TensorProduct()

        # out = ctypes.cast(c_densop_out.value, ctypes.POINTER(DensOp))
        # return out.contents
        return c_densop_out

    except Exception:
        raise DensOp_Error_TensorProduct()
    
def densop_apply_matrix(de, matrix=None, qid=[], dire='both'):

    if matrix is None:
        raise DensOp_Error_Apply()
    # if (matrix.shape[0] > de.row or matrix.shape[1] > de.col):
    #     raise DensOp_Error_Apply()
        
    if qid is None or qid == []:
        qnum = int(math.log2(de.row))
        qid = [i for i in range(qnum)]

    if dire == 'left':
        adire = LEFT
    elif dire == 'right':
        adire = RIGHT
    elif dire == 'both':
        adire = BOTH
    else:
        raise DensOp_Error_Apply()

    try:
        qubit_num = len(qid)
        qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
        for i in range(len(qid)):
            qubit_id[i] = qid[i]
        IntArray = ctypes.c_int * MAX_QUBIT_NUM
        qid_array = IntArray(*qubit_id)

        row = len(matrix) # dimension of the unitary matrix
        col = row
        size = row * col

        # set array of matrix
        # mat_complex = list(matrix.flatten())
        mat_complex = []
        for mat_row in matrix:
            for mat_elm in mat_row:
                mat_complex.append(mat_elm)
        
        mat_real = [0.0 for _ in range(size)]
        mat_imag = [0.0 for _ in range(size)]
        for i in range(size):
            mat_real[i] = mat_complex[i].real
            mat_imag[i] = mat_complex[i].imag
                
        DoubleArray = ctypes.c_double * size
        c_mat_real = DoubleArray(*mat_real)
        c_mat_imag = DoubleArray(*mat_imag)
            
        lib.densop_apply_matrix.restype = ctypes.c_int
        lib.densop_apply_matrix.argtypes = [ctypes.POINTER(DensOp),
                                            ctypes.c_int, IntArray,
                                            ctypes.c_int,
                                            DoubleArray, DoubleArray,
                                            ctypes.c_int, ctypes.c_int]
        ret = lib.densop_apply_matrix(ctypes.byref(de),
                                      ctypes.c_int(qubit_num), qid_array,
                                      ctypes.c_int(adire), c_mat_real, c_mat_imag,
                                      ctypes.c_int(row), ctypes.c_int(col))

        if ret == FALSE:
            raise DensOp_Error_Apply()

    except Exception:
        raise DensOp_Error_Apply()

def densop_probability(de, matrix=None, qid=[], matrix_type=None):

    if matrix is None:
        raise DensOp_Error_Probability()
    if (matrix.shape[0] > de.row or matrix.shape[1] > de.col):
        raise DensOp_Error_Probability()
        
    if qid is None or qid == []:
        qnum = int(math.log2(de.row))
        qid = [i for i in range(qnum)]

    if matrix_type == 'kraus':
        mtype = KRAUS
    elif matrix_type == 'povm':
        mtype = POVM
    else:
        raise DensOp_Error_Probability()
            
    try:
        qubit_num = len(qid)
        qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
        for i in range(len(qid)):
            qubit_id[i] = qid[i]
        IntArray = ctypes.c_int * MAX_QUBIT_NUM
        qid_array = IntArray(*qubit_id)

        row = len(matrix) # dimension of the unitary matrix
        col = row
        size = row * col

        # set array of matrix
        mat_complex = list(matrix.flatten())
        mat_real = [0.0 for _ in range(size)]
        mat_imag = [0.0 for _ in range(size)]
        for i in range(size):
            mat_real[i] = mat_complex[i].real
            mat_imag[i] = mat_complex[i].imag
                
        DoubleArray = ctypes.c_double * size
        c_mat_real = DoubleArray(*mat_real)
        c_mat_imag = DoubleArray(*mat_imag)
            
        prob = 0.0
        c_prob = ctypes.c_double(prob)

        lib.densop_probability.restype = ctypes.c_int
        lib.densop_probability.argtypes = [ctypes.POINTER(DensOp),
                                           ctypes.c_int, IntArray,
                                           ctypes.c_int, DoubleArray, DoubleArray,
                                           ctypes.c_int, ctypes.c_int,
                                           ctypes.POINTER(ctypes.c_double)]
        ret = lib.densop_probability(ctypes.byref(de),
                                     ctypes.c_int(qubit_num), qid_array,
                                     ctypes.c_int(mtype), c_mat_real, c_mat_imag,
                                     ctypes.c_int(row), ctypes.c_int(col),
                                     ctypes.byref(c_prob))

        if ret == FALSE:
            raise DensOp_Error_Probability()

        prob = round(c_prob.value, 8)
            
        return prob

    except Exception:
        raise DensOp_Error_Probability()

def densop_operate_qgate(de, kind=None, qid=None,
                         phase=DEF_PHASE, phase1=DEF_PHASE, phase2=DEF_PHASE):

    # error check
    densop_check_args(de, kind=kind, qid=qid, shots=None, angle=None,
                      phase=phase, phase1=phase1, phase2=phase2)

    qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
    for i in range(len(qid)):
        qubit_id[i] = qid[i]
    IntArray = ctypes.c_int * MAX_QUBIT_NUM
    qid_array = IntArray(*qubit_id)

    lib.densop_operate_qgate.restype = ctypes.c_int
    lib.densop_operate_qgate.argtypes = [ctypes.POINTER(DensOp), ctypes.c_int,
                                         ctypes.c_double, ctypes.c_double,
                                         ctypes.c_double, IntArray]
    ret = lib.densop_operate_qgate(ctypes.byref(de), ctypes.c_int(kind),
                                   ctypes.c_double(phase), ctypes.c_double(phase1),
                                   ctypes.c_double(phase2), qid_array)

    if ret == FALSE:
        raise DensOp_Error_OperateQGate()

def densop_free(de):

    lib.densop_free.argtypes = [ctypes.POINTER(DensOp)]
    lib.densop_free(ctypes.byref(de))
