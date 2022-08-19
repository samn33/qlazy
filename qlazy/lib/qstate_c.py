# -*- coding: utf-8 -*-
""" wrapper functions for QState """
import ctypes
from ctypes.util import find_library
import pathlib
from collections import Counter
import numpy as np

import qlazy.config as cfg
from qlazy.util import get_lib_ext, qstate_check_args
from qlazy.QState import QState
from qlazy.MData import MData
from qlazy.ObservableBase import ObservableBase
from qlazy.QCirc import QCirc
from qlazy.CMem import CMem

lib = ctypes.CDLL(str(pathlib.Path(__file__).with_name('libqlz.'+get_lib_ext())))
libc = ctypes.CDLL(find_library("c"), mode=ctypes.RTLD_GLOBAL)

def qstate_init(qubit_num=None, seed=None, use_gpu=False):
    """ initialize QState object """

    libc.srand(ctypes.c_int(seed))

    qstate = None
    c_qstate = ctypes.c_void_p(qstate)

    lib.qstate_init.restype = ctypes.c_bool
    lib.qstate_init.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_void_p), ctypes.c_bool]
    ret = lib.qstate_init(ctypes.c_int(qubit_num), c_qstate, ctypes.c_bool(use_gpu))

    if ret is False:
        raise ValueError("can't initialize QState object.")

    return c_qstate

def qstate_init_with_vector(vector=None, seed=None, use_gpu=False):
    """ initialize QState object with vector """

    libc.srand(ctypes.c_int(seed))

    qstate = None
    c_qstate = ctypes.c_void_p(qstate)

    dim = len(vector)
    vec_real = [0.0 for _ in range(dim)]
    vec_imag = [0.0 for _ in range(dim)]
    for i in range(dim):
        vec_real[i] = vector[i].real
        vec_imag[i] = vector[i].imag

    DoubleArray = ctypes.c_double * dim
    c_vec_real = DoubleArray(*vec_real)
    c_vec_imag = DoubleArray(*vec_imag)

    lib.qstate_init_with_vector.restype = ctypes.c_bool
    lib.qstate_init_with_vector.argtypes = [DoubleArray, DoubleArray, ctypes.c_int,
                                            ctypes.POINTER(ctypes.c_void_p), ctypes.c_bool]
    ret = lib.qstate_init_with_vector(c_vec_real, c_vec_imag, ctypes.c_int(dim),
                                      c_qstate, ctypes.c_bool(use_gpu))

    if ret is False:
        raise ValueError("can't initialize QState object.")

    return c_qstate


def qstate_reset(qs, qid=None):
    """ reset quantum state vector """

    if qid is None or qid == []:
        qid = list(range(qs.qubit_num))

    qstate_check_args(qs, kind=cfg.SHOW, qid=qid)

    try:
        qubit_num = len(qid)
        qubit_id = [0 for _ in range(qubit_num)]
        for i, q in enumerate(qid):
            qubit_id[i] = q

        IntArray = ctypes.c_int * qubit_num
        qid_array = IntArray(*qubit_id)

        lib.qstate_reset.restype = ctypes.c_bool
        lib.qstate_reset.argtypes = [ctypes.POINTER(QState), ctypes.c_int, IntArray]
        ret = lib.qstate_reset(ctypes.byref(qs), ctypes.c_int(qubit_num), qid_array)

        if ret is False:
            raise ValueError("can't reset quantum state vector.")

    except Exception:
        raise ValueError("can't reset quantum state vector.")


def qstate_print(qs, qid=None, nonzero=False):
    """ print quantum state vector """

    if qid is None or qid == []:
        qid = list(range(qs.qubit_num))

    qstate_check_args(qs, kind=cfg.SHOW, qid=qid)

    try:
        qubit_num = len(qid)
        qubit_id = [0 for _ in range(qubit_num)]
        for i, q in enumerate(qid):
            qubit_id[i] = q

        IntArray = ctypes.c_int * qubit_num
        qid_array = IntArray(*qubit_id)

        lib.qstate_print.restype = ctypes.c_bool
        lib.qstate_print.argtypes = [ctypes.POINTER(QState), ctypes.c_int, IntArray, ctypes.c_bool]
        ret = lib.qstate_print(ctypes.byref(qs), ctypes.c_int(qubit_num),
                               qid_array, ctypes.c_bool(nonzero))

        if ret is False:
            raise ValueError("can't print quantum state vector.")

    except Exception:
        raise ValueError("can't print quantum state vector.")


def qstate_copy(qs):
    """ copy the quantum state vector """

    try:
        qstate = None
        c_qstate = ctypes.c_void_p(qstate)

        lib.qstate_copy.restype = ctypes.c_bool
        lib.qstate_copy.argtypes = [ctypes.POINTER(QState),
                                    ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.qstate_copy(ctypes.byref(qs), c_qstate)

        if ret is False:
            raise ValueError("can't copy quantum state vector.")

        return c_qstate

    except Exception:
        raise ValueError("can't copy quantum state vector.")


def qstate_bloch(qs, q=0):
    """ get bloch angle from quantum state vector """

    # error check
    qstate_check_args(qs, kind=cfg.BLOCH, qid=[q])

    try:
        theta = 0.0
        phi = 0.0
        c_theta = ctypes.c_double(theta)
        c_phi = ctypes.c_double(phi)

        lib.qstate_bloch.restype = ctypes.c_bool
        lib.qstate_bloch.argtypes = [ctypes.POINTER(QState), ctypes.c_int,
                                     ctypes.POINTER(ctypes.c_double),
                                     ctypes.POINTER(ctypes.c_double)]
        ret = lib.qstate_bloch(ctypes.byref(qs), ctypes.c_int(q),
                               ctypes.byref(c_theta), ctypes.byref(c_phi))

        if ret is False:
            raise ValueError("can't get bloch angle.")

        theta = c_theta.value
        phi = c_phi.value

        return theta, phi

    except Exception:
        raise ValueError("can't get bloch angle.")


def qstate_inner_product(qs_0, qs_1):
    """ get inner product of 2 quantum state vectors """

    try:
        real = 0.0
        imag = 0.0
        c_real = ctypes.c_double(real)
        c_imag = ctypes.c_double(imag)

        lib.qstate_inner_product.restype = ctypes.c_bool
        lib.qstate_inner_product.argtypes = [ctypes.POINTER(QState),
                                             ctypes.POINTER(QState),
                                             ctypes.POINTER(ctypes.c_double),
                                             ctypes.POINTER(ctypes.c_double)]
        ret = lib.qstate_inner_product(ctypes.byref(qs_0), ctypes.byref(qs_1),
                                       ctypes.byref(c_real), ctypes.byref(c_imag))

        if ret is False:
            raise ValueError("can't get inner product of 2 quantum state vectors.")

        real = c_real.value
        imag = c_imag.value

        return complex(real, imag)

    except Exception:
        raise ValueError("can't get inner product of 2 quantum state vectors.")


def qstate_get_camp(qs, qid=None):
    """ get elements of the quantum state vector """

    if qid is None or qid == []:
        qid = list(range(qs.qubit_num))

    # error check
    if len(qid) > qs.qubit_num:
        raise IndexError("too many arguments.")
    for q in qid:
        if q >= qs.qubit_num:
            raise IndexError("out of range.")
        if q < 0:
            raise IndexError("out of range.")

    try:
        qubit_num = len(qid)
        qubit_id = [0 for _ in range(qubit_num)]
        for i, q in enumerate(qid):
            qubit_id[i] = q
        IntArray = ctypes.c_int * qubit_num
        qid_array = IntArray(*qubit_id)

        camp = None
        c_camp = ctypes.c_void_p(camp)
        lib.qstate_get_camp.restype = ctypes.c_bool
        lib.qstate_get_camp.argtypes = [ctypes.POINTER(QState), ctypes.c_int, IntArray,
                                        ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.qstate_get_camp(ctypes.byref(qs), ctypes.c_int(qubit_num),
                                  qid_array, c_camp)

        if ret is False:
            raise ValueError("can't get element of the quantum state vector.")

        o = ctypes.cast(c_camp.value, ctypes.POINTER(ctypes.c_double))

        state_num = (1 << len(qid))
        out = [0] * state_num
        for i in range(state_num):
            out[i] = complex(o[2*i], o[2*i+1])

        libc.free.argtypes = [ctypes.POINTER(ctypes.c_double)]
        libc.free(o)

    except Exception:
        raise ValueError("can't get element of the quantum state vector.")

    return np.array(out)


def qstate_tensor_product(qs, qstate):
    """ get tensor product of 2 quantum state vectors """

    try:
        qstate_out = None
        c_qstate_out = ctypes.c_void_p(qstate_out)

        lib.qstate_tensor_product.restype = ctypes.c_bool
        lib.qstate_tensor_product.argtypes = [ctypes.POINTER(QState),
                                              ctypes.POINTER(QState),
                                              ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.qstate_tensor_product(ctypes.byref(qs), ctypes.byref(qstate),
                                        c_qstate_out)

        if ret is False:
            raise ValueError("can't get tensor product of the 2 quantum state vectors.")

        return c_qstate_out

    except Exception:
        raise ValueError("can't get tensor product of the 2 quantum state vectors.")


def qstate_evolve(qs, observable=None, time=0.0, iteration=0):
    """ time evolution of the quantum state vectors """

    if iteration < 1:
        raise ValueError("iteration must be positive integer.")

    if observable is None:
        raise ValueError("observable must be set.")

    try:
        lib.qstate_evolve.restype = ctypes.c_bool
        lib.qstate_evolve.argtypes = [ctypes.POINTER(QState), ctypes.POINTER(ObservableBase),
                                      ctypes.c_double, ctypes.c_int]
        ret = lib.qstate_evolve(ctypes.byref(qs), ctypes.byref(observable),
                                ctypes.c_double(time), ctypes.c_int(iteration))

        if ret is False:
            raise ValueError("can't get the quantum state vectors after time evolution.")

    except Exception:
        raise ValueError("can't get the quantum state vectors after time evolution.")


def qstate_expect_value(qs, observable=None):
    """ get expectation value of the observable
        under the quantum state vector """

    if observable is None:
        raise ValueError("observable must be set.")

    try:
        val = 0.0
        c_val = ctypes.c_double(val)
        lib.qstate_expect_value.restype = ctypes.c_bool
        lib.qstate_expect_value.argtypes = [ctypes.POINTER(QState),
                                            ctypes.POINTER(ObservableBase),
                                            ctypes.POINTER(ctypes.c_double)]
        ret = lib.qstate_expect_value(ctypes.byref(qs),
                                      ctypes.byref(observable),
                                      ctypes.byref(c_val))

        if ret is False:
            raise ValueError("can't get expect value of the observable"
                             " under the quantum state vector.")

        val = c_val.value

        return complex(val, 0.0)

    except Exception:
        raise ValueError("can't get expect value of the observable"
                         " under the quantum state vector.")

    # return out


def qstate_apply_matrix(qs, matrix=None, qid=None):
    """ apply matrix to the quantum state """

    if matrix is None:
        raise ValueError("matrix must be set.")

    if qid is None or qid == []:
        qid = list(range(qs.qubit_num))

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

        lib.qstate_apply_matrix.restype = ctypes.c_bool
        lib.qstate_apply_matrix.argtypes = [ctypes.POINTER(QState),
                                            ctypes.c_int, IntArray,
                                            DoubleArray, DoubleArray,
                                            ctypes.c_int, ctypes.c_int]
        ret = lib.qstate_apply_matrix(ctypes.byref(qs),
                                      ctypes.c_int(qubit_num), qid_array,
                                      c_mat_real, c_mat_imag,
                                      ctypes.c_int(row), ctypes.c_int(col))

        if ret is False:
            raise ValueError("can't apply the matrix to the quantum state vector.")

    except Exception:
        raise ValueError("can't apply the matrix to the quantum state vector.")


def qstate_operate_qgate(qs, kind=None, qid=None, phase=cfg.DEF_PHASE,
                         phase1=cfg.DEF_PHASE, phase2=cfg.DEF_PHASE):
    """ operate quantum gate to the quantum state """

    # error check
    qstate_check_args(qs, kind=kind, qid=qid)

    qubit_id = [-1 for _ in range(2)]
    for i, q in enumerate(qid):
        qubit_id[i] = q
    IntArray = ctypes.c_int * 2
    qid_array = IntArray(*qubit_id)

    lib.qstate_operate_qgate.restype = ctypes.c_bool
    lib.qstate_operate_qgate.argtypes = [ctypes.POINTER(QState), ctypes.c_int,
                                         ctypes.c_double, ctypes.c_double,
                                         ctypes.c_double, IntArray]
    ret = lib.qstate_operate_qgate(ctypes.byref(qs), ctypes.c_int(kind),
                                   ctypes.c_double(phase), ctypes.c_double(phase1),
                                   ctypes.c_double(phase2), qid_array)

    if ret is False:
        raise ValueError("can't operate quantum gate to the quantum state vector.")

def qstate_measure(qs, qid=None):
    """ measurement of the qubits """

    # qnum, mnum
    qnum = qs.qubit_num
    if qid is None or qid == []:
        qid = list(range(qnum))
    mnum = len(qid)

    # qid_array
    qubit_id = [0 for _ in range(qnum)]
    for i, q in enumerate(qid):
        qubit_id[i] = q
    IntArray = ctypes.c_int * qnum
    qid_array = IntArray(*qubit_id)

    # mstr_all_array, mstr_qid_array
    mstr = "0" * qnum
    mstr_array = ctypes.create_string_buffer(mstr.encode())



    mchar_bytes = bytearray([0x00 for _ in range(qnum)])
    CharArray = ctypes.c_char * qnum
    mchar_array = CharArray(*mchar_bytes)
    
    lib.qstate_measure.restype = ctypes.c_bool
    lib.qstate_measure.argtypes = [ctypes.POINTER(QState), ctypes.c_int,
                                   IntArray, ctypes.c_char_p, ctypes.c_bool]
    ret = lib.qstate_measure(ctypes.byref(qs), ctypes.c_int(mnum),
                             qid_array, mchar_array, True)

    if ret is False:
        raise ValueError("can't measure the qubits.")

    measured_str = mstr_array.value.decode()
    measured_str = "".join(map(str, [int.from_bytes(c, byteorder='big') for c in mchar_array]))

    return measured_str

def qstate_measure_stats(qs, qid=None, shots=cfg.DEF_SHOTS, angle=0.0, phase=0.0):
    """ measurement of the qubits and get stats """

    if qid is None or qid == []:
        qid = list(range(qs.qubit_num))

    # error check
    qstate_check_args(qs, kind=cfg.MEASURE, qid=qid)

    # operate
    qubit_num = len(qid)
    qubit_id = [0 for _ in range(qubit_num)]
    for i, q in enumerate(qid):
        qubit_id[i] = q
    IntArray = ctypes.c_int * qubit_num
    qid_array = IntArray(*qubit_id)

    mdata = None
    c_mdata = ctypes.c_void_p(mdata)

    lib.qstate_measure_stats.restype = ctypes.c_bool
    lib.qstate_measure_stats.argtypes = [ctypes.POINTER(QState), ctypes.c_int,
                                         ctypes.c_double, ctypes.c_double,
                                         ctypes.c_int, IntArray,
                                         ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.qstate_measure_stats(ctypes.byref(qs), ctypes.c_int(shots),
                                   ctypes.c_double(angle), ctypes.c_double(phase),
                                   ctypes.c_int(qubit_num), qid_array, c_mdata)

    if ret is False:
        raise ValueError("can't measure the qubits.")

    out = ctypes.cast(c_mdata.value, ctypes.POINTER(MData))

    return out.contents

def qstate_measure_bell_stats(qs, qid=None, shots=cfg.DEF_SHOTS):
    """ bell measurement of the qubits and get stats """

    if qid is None or qid == []:
        qid = list(range(2))

    # error check
    qstate_check_args(qs, kind=cfg.MEASURE_BELL, qid=qid)

    # operate
    qubit_num = 2
    qubit_id = [0 for _ in range(qubit_num)]
    for i in range(qubit_num):
        qubit_id[i] = qid[i]
    IntArray = ctypes.c_int * qubit_num
    qid_array = IntArray(*qubit_id)

    mdata = None
    c_mdata = ctypes.c_void_p(mdata)

    lib.qstate_measure_bell_stats.restype = ctypes.c_bool
    lib.qstate_measure_bell_stats.argtypes = [ctypes.POINTER(QState), ctypes.c_int,
                                              ctypes.c_int, IntArray,
                                              ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.qstate_measure_bell_stats(ctypes.byref(qs), ctypes.c_int(shots),
                                        ctypes.c_int(qubit_num), qid_array, c_mdata)

    if ret is False:
        raise ValueError("can't measure the qubits.")

    out = ctypes.cast(c_mdata.value, ctypes.POINTER(MData))

    return out.contents

def qstate_operate_qcirc(qstate, cmem, qcirc, shots, cid, out_state):
    """ operate quantum circuit """

    if cmem is not None:
        cmem_num = cmem.cmem_num
    else:
        cmem_num = 0

    buf_size = cmem_num * shots
    mchar_array = bytearray([0x00 for _ in range(buf_size)])
    CharArray = ctypes.c_char * buf_size
    mchar_shots = CharArray(*mchar_array)

    lib.qstate_operate_qcirc.restype = ctypes.c_bool
    lib.qstate_operate_qcirc.argtypes = [ctypes.POINTER(QState),
                                         ctypes.POINTER(CMem), ctypes.POINTER(QCirc),
                                         ctypes.c_int, CharArray, ctypes.c_bool]

    if cmem is not None:
        ret = lib.qstate_operate_qcirc(ctypes.byref(qstate),
                                       ctypes.byref(cmem), ctypes.byref(qcirc),
                                       ctypes.c_int(shots), mchar_shots, ctypes.c_bool(out_state))
        frequency = Counter()
        for i in range(0, len(mchar_shots), cmem_num):
            cmem_list = mchar_shots[i:i+cmem_num]
            cmem_list_part = [cmem_list[c] for c in cid]
            mchar = "".join(map(str, cmem_list_part))
            frequency[mchar] += 1

    else: # unitary only
        c_cmem = ctypes.POINTER(CMem)()
        ret = lib.qstate_operate_qcirc(ctypes.byref(qstate), c_cmem, ctypes.byref(qcirc),
                                       ctypes.c_int(shots), mchar_shots, ctypes.c_bool(out_state))

        frequency = None

    return frequency

def qstate_free(qs):
    """ free memory of the QState object """

    lib.qstate_free.argtypes = [ctypes.POINTER(QState)]
    lib.qstate_free(ctypes.byref(qs))
