# -*- coding: utf-8 -*-
""" wrapper functions for DensOp """
import ctypes
from ctypes.util import find_library
import pathlib
import math
import numpy as np

import qlazy.config as cfg
from qlazy.util import get_lib_ext, densop_check_args
from qlazy.QState import QState
from qlazy.DensOp import DensOp

lib = ctypes.CDLL(str(pathlib.Path(__file__).with_name('libqlz.'+get_lib_ext())))
libc = ctypes.CDLL(find_library("c"), mode=ctypes.RTLD_GLOBAL)

def densop_init(qstate=None, prob=None):
    """ initialize DensOp object """

    if qstate is None:
        qstate = []
    if prob is None:
        prob = []

    num = len(qstate)

    densop = None
    c_densop = ctypes.c_void_p(densop)

    DoubleArray = ctypes.c_double * num
    prob_array = DoubleArray(*prob)

    QStateArray = QState * num
    qstate_array = QStateArray(*qstate)

    lib.densop_init.restype = ctypes.c_bool
    lib.densop_init.argtypes = [ctypes.POINTER(QState),
                                ctypes.POINTER(ctypes.c_double),
                                ctypes.c_int,
                                ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.densop_init(qstate_array, prob_array,
                          ctypes.c_int(num), c_densop)

    if ret is False:
        raise ValueError("can't initialize DensOp object.")

    return c_densop

def densop_init_with_matrix(matrix=None):
    """ initialize DensOp object with matrix """

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

    lib.densop_init_with_matrix.restype = ctypes.c_bool
    lib.densop_init_with_matrix.argtypes = [DoubleArray, DoubleArray,
                                            ctypes.c_int, ctypes.c_int,
                                            ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.densop_init_with_matrix(c_mat_real, c_mat_imag,
                                      ctypes.c_int(row), ctypes.c_int(col),
                                      c_densop)

    if ret is False:
        raise ValueError("can't initialize densop with matrix.")

    return c_densop


def densop_get_elm(de):
    """ get elements of density operator """

    try:
        elm = None
        c_elm = ctypes.c_void_p(elm)

        lib.densop_get_elm.restype = ctypes.c_bool
        lib.densop_get_elm.argtypes = [ctypes.POINTER(DensOp),
                                       ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.densop_get_elm(ctypes.byref(de), c_elm)

        if ret is False:
            raise ValueError("can't get densop elements.")

        o = ctypes.cast(c_elm.value, ctypes.POINTER(ctypes.c_double))

        size = de.row * de.col
        out = [0] * size
        for i in range(size):
            out[i] = complex(round(o[2*i], 8), round(o[2*i+1], 8))

        libc.free.argtypes = [ctypes.POINTER(ctypes.c_double)]
        libc.free(o)

        return np.array(out).reshape([de.row, de.col])

    except Exception:
        raise ValueError("can't get densop elements.")

def densop_reset(de, qid=None):
    """ reset density operator """

    if qid is None or qid == []:
        qnum = int(math.log2(de.row))
        qid = list(range(qnum))

    try:
        qubit_num = len(qid)
        qubit_id = [0 for _ in range(qubit_num)]
        for i, q in enumerate(qid):
            qubit_id[i] = q

        IntArray = ctypes.c_int * qubit_num
        qid_array = IntArray(*qubit_id)

        lib.densop_reset.restype = ctypes.c_bool
        lib.densop_reset.argtypes = [ctypes.POINTER(DensOp), ctypes.c_int, IntArray]
        ret = lib.densop_reset(ctypes.byref(de), ctypes.c_int(qubit_num), qid_array)

        if ret is False:
            raise ValueError("can't reset.")

    except Exception:
        raise ValueError("can't reset.")

def densop_print(de, nonzero=False):
    """ print density operator """

    try:
        lib.densop_print.restype = ctypes.c_bool
        lib.densop_print.argtypes = [ctypes.POINTER(DensOp), ctypes.c_bool]
        ret = lib.densop_print(ctypes.byref(de), ctypes.c_bool(nonzero))

        if ret is False:
            raise ValueError("can't print densop.")

    except Exception:
        raise ValueError("can't print densop.")

def densop_copy(de):
    """ copy density operator """

    try:
        densop = None
        c_densop = ctypes.c_void_p(densop)

        lib.densop_copy.restype = ctypes.c_bool
        lib.densop_copy.argtypes = [ctypes.POINTER(DensOp),
                                    ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.densop_copy(ctypes.byref(de), c_densop)

        if ret is False:
            raise ValueError("can't copy densop.")

        return c_densop

    except Exception:
        raise ValueError("can't copy densop.")

def densop_add(de, densop=None):
    """ add density operator """

    try:
        lib.densop_add.restype = ctypes.c_bool
        lib.densop_add.argtypes = [ctypes.POINTER(DensOp), ctypes.POINTER(DensOp)]
        ret = lib.densop_add(ctypes.byref(de), ctypes.byref(densop))

        if ret is False:
            raise ValueError("can't add densop.")

    except Exception:
        raise ValueError("can't add densop.")

def densop_mul(de, factor=0.0):
    """ mul density operator """

    try:
        lib.densop_mul.restype = ctypes.c_bool
        lib.densop_mul.argtypes = [ctypes.POINTER(DensOp), ctypes.c_double]
        ret = lib.densop_mul(ctypes.byref(de), ctypes.c_double(factor))

        if ret is False:
            raise ValueError("can't mul densop.")

    except Exception:
        raise ValueError("can't mul densop.")

def densop_trace(de):
    """ trace of density operator """

    try:
        real = 0.0
        imag = 0.0
        c_real = ctypes.c_double(real)
        c_imag = ctypes.c_double(imag)

        lib.densop_trace.restype = ctypes.c_bool
        lib.densop_trace.argtypes = [ctypes.POINTER(DensOp),
                                     ctypes.POINTER(ctypes.c_double),
                                     ctypes.POINTER(ctypes.c_double)]
        ret = lib.densop_trace(ctypes.byref(de), ctypes.byref(c_real),
                               ctypes.byref(c_imag))

        if ret is False:
            raise ValueError("can't get trace of densop.")

        real = round(c_real.value, 8)
        imag = round(c_imag.value, 8)

        if abs(imag) > cfg.EPS:
            raise ValueError("can't get trace of densop.")

        return real

    except Exception:
        raise ValueError("can't get trace of densop.")

def densop_sqtrace(de):
    """ square trace of density operator """

    try:
        real = 0.0
        imag = 0.0
        c_real = ctypes.c_double(real)
        c_imag = ctypes.c_double(imag)

        lib.densop_sqtrace.restype = ctypes.c_bool
        lib.densop_sqtrace.argtypes = [ctypes.POINTER(DensOp),
                                       ctypes.POINTER(ctypes.c_double),
                                       ctypes.POINTER(ctypes.c_double)]
        ret = lib.densop_sqtrace(ctypes.byref(de), ctypes.byref(c_real),
                                 ctypes.byref(c_imag))

        if ret is False:
            raise ValueError("can't get square trace of densop.")

        real = round(c_real.value, 8)
        imag = round(c_imag.value, 8)

        if abs(imag) > cfg.EPS:
            raise ValueError("can't get square trace of densop.")

        return real

    except Exception:
        raise ValueError("can't get square trace of densop.")

def densop_patrace(de, qid=None):
    """ partial trace of density operator """

    try:
        if qid is None:
            raise ValueError("qid must be set.")

        densop = None
        c_densop = ctypes.c_void_p(densop)

        qubit_num = len(qid)
        qubit_id = [0 for _ in range(qubit_num)]
        for i, q in enumerate(qid):
            qubit_id[i] = q
        IntArray = ctypes.c_int * qubit_num
        qid_array = IntArray(*qubit_id)

        lib.densop_patrace.restype = ctypes.c_bool
        lib.densop_patrace.argtypes = [ctypes.POINTER(DensOp),
                                       ctypes.c_int, IntArray,
                                       ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.densop_patrace(ctypes.byref(de), ctypes.c_int(qubit_num),
                                 qid_array, c_densop)

        if ret is False:
            raise ValueError("can't get partial trace of densop.")

        return c_densop

    except Exception:
        raise ValueError("can't get partial trace of densop.")

def densop_tensor_product(de_0, de_1):
    """ tensor product of density operator """

    try:
        densop_out = None
        c_densop_out = ctypes.c_void_p(densop_out)

        lib.densop_tensor_product.restype = ctypes.c_bool
        lib.densop_tensor_product.argtypes = [ctypes.POINTER(DensOp),
                                              ctypes.POINTER(DensOp),
                                              ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.densop_tensor_product(ctypes.byref(de_0), ctypes. byref(de_1),
                                        c_densop_out)

        if ret is False:
            raise ValueError("can't get tensor product.")

        return c_densop_out

    except Exception:
        raise ValueError("can't get tensor product.")

def densop_apply_matrix(de, matrix=None, qid=None, dire='both'):
    """ operate matrix to the density operator """

    if matrix is None:
        raise ValueError("matrix must be set.")

    if qid is None or qid == []:
        qnum = int(math.log2(de.row))
        qid = list(range(qnum))

    if dire == 'left':
        adire = cfg.LEFT
    elif dire == 'right':
        adire = cfg.RIGHT
    elif dire == 'both':
        adire = cfg.BOTH
    else:
        raise ValueError("unknown dire string (set 'left', 'right' or 'both').")

    try:
        qubit_num = len(qid)
        qubit_id = [0 for _ in range(qubit_num)]
        for i, q in enumerate(qid):
            qubit_id[i] = q
        IntArray = ctypes.c_int * qubit_num
        qid_array = IntArray(*qubit_id)

        row = len(matrix) # dimension of the unitary matrix
        col = row
        size = row * col

        # set array of matrix
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

        lib.densop_apply_matrix.restype = ctypes.c_bool
        lib.densop_apply_matrix.argtypes = [ctypes.POINTER(DensOp),
                                            ctypes.c_int, IntArray,
                                            ctypes.c_int,
                                            DoubleArray, DoubleArray,
                                            ctypes.c_int, ctypes.c_int]
        ret = lib.densop_apply_matrix(ctypes.byref(de),
                                      ctypes.c_int(qubit_num), qid_array,
                                      ctypes.c_int(adire), c_mat_real, c_mat_imag,
                                      ctypes.c_int(row), ctypes.c_int(col))

        if ret is False:
            raise ValueError("can't apply matrix.")

    except Exception:
        raise ValueError("can't apply matrix.")

def densop_probability(de, matrix=None, qid=None, matrix_type=None):
    """ probability of the observable (matrix repr.) for the density operator """

    if matrix is None:
        raise ValueError("matrix must be set.")
    if (matrix.shape[0] > de.row or matrix.shape[1] > de.col):
        raise ValueError("matrix size is too large.")

    if qid is None or qid == []:
        qnum = int(math.log2(de.row))
        qid = list(range(qnum))

    if matrix_type == 'kraus':
        mtype = cfg.KRAUS
    elif matrix_type == 'povm':
        mtype = cfg.POVM
    else:
        raise ValueError("matrix_type is unknown (set 'kraus' or 'povm')")

    try:
        qubit_num = len(qid)
        qubit_id = [0 for _ in range(qubit_num)]
        for i, q in enumerate(qid):
            qubit_id[i] = q
        IntArray = ctypes.c_int * qubit_num
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

        lib.densop_probability.restype = ctypes.c_bool
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

        if ret is False:
            raise ValueError("can't calculate probability.")

        prob = round(c_prob.value, 8)

        return prob

    except Exception:
        raise ValueError("can't calculate probability.")

def densop_operate_qgate(de, kind=None, qid=None, phase=cfg.DEF_PHASE,
                         phase1=cfg.DEF_PHASE, phase2=cfg.DEF_PHASE):
    """ operate quantum gate to the density operator """

    # error check
    densop_check_args(de, kind=kind, qid=qid)

    qubit_id = [0 for _ in range(2)]
    for i, q in enumerate(qid):
        qubit_id[i] = q
    IntArray = ctypes.c_int * 2
    qid_array = IntArray(*qubit_id)

    lib.densop_operate_qgate.restype = ctypes.c_bool
    lib.densop_operate_qgate.argtypes = [ctypes.POINTER(DensOp), ctypes.c_int,
                                         ctypes.c_double, ctypes.c_double,
                                         ctypes.c_double, IntArray]
    ret = lib.densop_operate_qgate(ctypes.byref(de), ctypes.c_int(kind),
                                   ctypes.c_double(phase), ctypes.c_double(phase1),
                                   ctypes.c_double(phase2), qid_array)

    if ret is False:
        raise ValueError("can't operate the quantum gate.")

def densop_free(de):
    """ free memory of the density operator """

    lib.densop_free.argtypes = [ctypes.POINTER(DensOp)]
    lib.densop_free(ctypes.byref(de))
