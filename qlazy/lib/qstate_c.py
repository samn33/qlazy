# -*- coding: utf-8 -*-
import ctypes
from ctypes.util import find_library
import numpy as np
import pathlib
from collections import Counter 

from qlazy.config import *
from qlazy.error import *
from qlazy.util import *
from qlazy.QState import QState
from qlazy.MData import *
from qlazy.Observable import Observable
from qlazy.QCirc import QCirc
from qlazy.CMem import CMem
from qlazy.lib.mdata_c import *

lib= ctypes.CDLL(str(pathlib.Path(__file__).with_name('libqlz.'+get_lib_ext())))
libc = ctypes.CDLL(find_library("c"),mode=ctypes.RTLD_GLOBAL)

def qstate_init(qubit_num=None, seed=None):

    lib.init_qlazy(ctypes.c_int(seed))
        
    qstate = None
    c_qstate = ctypes.c_void_p(qstate)

    lib.qstate_init.restype = ctypes.c_int
    lib.qstate_init.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.qstate_init(ctypes.c_int(qubit_num), c_qstate)

    if ret == FALSE:
        raise QState_Error_Initialize()

    return c_qstate

def qstate_init_with_vector(vector=None, seed=None):
        
    lib.init_qlazy(ctypes.c_int(seed))
        
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
    
    lib.qstate_init_with_vector.restype = ctypes.c_int
    lib.qstate_init_with_vector.argtypes = [DoubleArray, DoubleArray, ctypes.c_int,
                                            ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.qstate_init_with_vector(c_vec_real, c_vec_imag, ctypes.c_int(dim),
                                      c_qstate)
    
    if ret == FALSE:
        raise QState_Error_Initialize()
    
    return c_qstate


def qstate_reset(qs, qid=None):
    
    if qid is None or qid == []:
        qid = [i for i in range(qs.qubit_num)]
    
    qstate_check_args(qs, kind=SHOW, shots=None, angle=None, qid=qid)
    
    try:
        qubit_num = len(qid)
        qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
        for i in range(len(qid)):
            qubit_id[i] = qid[i]
    
        IntArray = ctypes.c_int * MAX_QUBIT_NUM
        qid_array = IntArray(*qubit_id)
            
        lib.qstate_reset.restype = ctypes.c_int
        lib.qstate_reset.argtypes = [ctypes.POINTER(QState),ctypes.c_int, IntArray]
        ret = lib.qstate_reset(ctypes.byref(qs),ctypes.c_int(qubit_num), qid_array)
    
        if ret == FALSE:
            raise QState_Error_Reset()
    
    except Exception:
        raise QState_Error_Reset()

    
def qstate_print(qs, qid=None, nonzero=False):

    if qid is None or qid == []:
        qid = [i for i in range(qs.qubit_num)]

    qstate_check_args(qs, kind=SHOW, shots=None, angle=None, qid=qid)
        
    try:
        qubit_num = len(qid)
        qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
        for i in range(len(qid)):
            qubit_id[i] = qid[i]

        IntArray = ctypes.c_int * MAX_QUBIT_NUM
        qid_array = IntArray(*qubit_id)

        
            
        lib.qstate_print.restype = ctypes.c_int
        lib.qstate_print.argtypes = [ctypes.POINTER(QState),ctypes.c_int, IntArray, ctypes.c_bool]
        ret = lib.qstate_print(ctypes.byref(qs),ctypes.c_int(qubit_num), qid_array, ctypes.c_bool(nonzero))

        if ret == FALSE:
            raise QState_Error_Show()

    except Exception:
        raise QState_Error_Show()


def qstate_copy(qs):

    try:
        qstate = None
        c_qstate = ctypes.c_void_p(qstate)
            
        lib.qstate_copy.restype = ctypes.c_int
        lib.qstate_copy.argtypes = [ctypes.POINTER(QState),
                                    ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.qstate_copy(ctypes.byref(qs), c_qstate)

        if ret == FALSE:
            raise QState_Error_Clone()

        return c_qstate
        
    except Exception:
        raise QState_Error_Clone()


def qstate_bloch(qs, q=0):

    # error check
    qstate_check_args(qs, kind=BLOCH, shots=None, angle=None, qid=[q])

    try:
        theta = 0.0
        phi = 0.0
        c_theta = ctypes.c_double(theta)
        c_phi = ctypes.c_double(phi)
            
        lib.qstate_bloch.restype = ctypes.c_int
        lib.qstate_bloch.argtypes = [ctypes.POINTER(QState),ctypes.c_int,
                                     ctypes.POINTER(ctypes.c_double),
                                     ctypes.POINTER(ctypes.c_double)]
        ret = lib.qstate_bloch(ctypes.byref(qs),ctypes.c_int(q),
                               ctypes.byref(c_theta), ctypes.byref(c_phi))

        if ret == FALSE:
            raise QState_Error_Bloch()

        theta = c_theta.value
        phi = c_phi.value

        return theta,phi

    except Exception:
        raise QState_Error_Bloch()


def qstate_inner_product(qs_0, qs_1):

    try:
        real = 0.0
        imag = 0.0
        c_real = ctypes.c_double(real)
        c_imag = ctypes.c_double(imag)
            
        lib.qstate_inner_product.restype = ctypes.c_int
        lib.qstate_inner_product.argtypes = [ctypes.POINTER(QState),
                                             ctypes.POINTER(QState),
                                             ctypes.POINTER(ctypes.c_double),
                                             ctypes.POINTER(ctypes.c_double)]
        ret = lib.qstate_inner_product(ctypes.byref(qs_0),ctypes.byref(qs_1),
                                       ctypes.byref(c_real), ctypes.byref(c_imag))

        if ret == FALSE:
            raise QState_Error_InnerProduct()

        real = c_real.value
        imag = c_imag.value

        return complex(real, imag)
        
    except Exception:
        raise QState_Error_InnerProduct()

    
def qstate_get_camp(qs, qid=None):

    if qid is None or qid == []:
        qid = [i for i in range(qs.qubit_num)]

    # error check
    if len(qid) > qs.qubit_num:
        raise QState_TooManyArguments()
    for i in range(len(qid)):
        if qid[i] >= qs.qubit_num:
            raise QState_OutOfBound()
        if qid[i] < 0:
            raise QState_OutOfBound()

    try:
        qubit_num = len(qid)
        qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
        for i in range(len(qid)):
            qubit_id[i] = qid[i]
        IntArray = ctypes.c_int * MAX_QUBIT_NUM
        qid_array = IntArray(*qubit_id)

        camp = None
        c_camp = ctypes.c_void_p(camp)
        lib.qstate_get_camp.restype = ctypes.c_int
        lib.qstate_get_camp.argtypes = [ctypes.POINTER(QState),ctypes.c_int, IntArray,
                                        ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.qstate_get_camp(ctypes.byref(qs),ctypes.c_int(qubit_num),
                                  qid_array, c_camp)

        if ret == FALSE:
            raise QState_Error_GetAmp()
                
        o = ctypes.cast(c_camp.value, ctypes.POINTER(ctypes.c_double))
            
        state_num = (1 << len(qid))
        out = [0] * state_num
        for i in range(state_num):
            out[i] = complex(o[2*i],o[2*i+1])

        libc.free.argtypes = [ctypes.POINTER(ctypes.c_double)]
        libc.free(o)

    except Exception:
        raise QState_Error_GetCmp()

    return np.array(out)


def qstate_tensor_product(qs, qstate):

    try:
        qstate_out = None
        c_qstate_out = ctypes.c_void_p(qstate_out)

        lib.qstate_tensor_product.restype = ctypes.c_int
        lib.qstate_tensor_product.argtypes = [ctypes.POINTER(QState),
                                              ctypes.POINTER(QState),
                                              ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.qstate_tensor_product(ctypes.byref(qs),ctypes.byref(qstate),
                                        c_qstate_out)

        if ret == FALSE:
            raise QState_Error_TensorProduct()

        return c_qstate_out

    except Exception:
        raise QState_Error_TensorProduct()


def qstate_evolve(qs, observable=None, time=0.0, iter=0):

    if iter < 1:
        raise QState_Error_Evolve()
        
    if observable is None:
        raise QState_Error_Evolve()
        
    try:
        lib.qstate_evolve.restype = ctypes.c_int
        lib.qstate_evolve.argtypes = [ctypes.POINTER(QState),ctypes.POINTER(Observable),
                                      ctypes.c_double, ctypes.c_int]
        ret = lib.qstate_evolve(ctypes.byref(qs), ctypes.byref(observable),
                                ctypes.c_double(time), ctypes.c_int(iter))

        if ret == FALSE:
            raise QState_Error_Evolve()
            
    except Exception:
        raise QState_Error_Evolve()


def qstate_expect_value(qs, observable=None):

    if observable is None:
        raise QState_Error_Expect()
        
    try:
        val = 0.0
        c_val = ctypes.c_double(val)
        lib.qstate_expect_value.restype = ctypes.c_int
        lib.qstate_expect_value.argtypes = [ctypes.POINTER(QState),
                                            ctypes.POINTER(Observable),
                                            ctypes.POINTER(ctypes.c_double)]
        ret = lib.qstate_expect_value(ctypes.byref(qs),
                                      ctypes.byref(observable),
                                      ctypes.byref(c_val))
            
        if ret == FALSE:
            raise QState_Error_Expect()

        val = c_val.value
            
        return complex(val,0.0)
            
    except Exception:
        raise QState_Error_Expect()

    return out


def qstate_apply_matrix(qs, matrix=None, qid=None):

    if matrix is None:
        raise QState_Error_Apply()
        
    if qid is None or qid == []:
        qid = [i for i in range(qs.qubit_num)]

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
            
        lib.qstate_apply_matrix.restype = ctypes.c_int
        lib.qstate_apply_matrix.argtypes = [ctypes.POINTER(QState),
                                            ctypes.c_int, IntArray,
                                            DoubleArray, DoubleArray,
                                            ctypes.c_int, ctypes.c_int]
        ret = lib.qstate_apply_matrix(ctypes.byref(qs),
                                      ctypes.c_int(qubit_num), qid_array,
                                      c_mat_real, c_mat_imag,
                                      ctypes.c_int(row), ctypes.c_int(col))

        if ret == FALSE:
            raise QState_Error_Apply()

    except Exception:
        raise QState_Error_Apply()

    
def qstate_operate_qgate(qs, kind=None, qid=None,
                         phase=DEF_PHASE, phase1=DEF_PHASE, phase2=DEF_PHASE):

    # error check
    qstate_check_args(qs, kind=kind, qid=qid, shots=None, angle=None,
                      phase=phase, phase1=phase1, phase2=phase2)

    qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
    for i in range(len(qid)):
        qubit_id[i] = qid[i]
    IntArray = ctypes.c_int * MAX_QUBIT_NUM
    qid_array = IntArray(*qubit_id)

    lib.qstate_operate_qgate.restype = ctypes.c_int
    lib.qstate_operate_qgate.argtypes = [ctypes.POINTER(QState), ctypes.c_int,
                                         ctypes.c_double, ctypes.c_double,
                                         ctypes.c_double, IntArray]
    ret = lib.qstate_operate_qgate(ctypes.byref(qs), ctypes.c_int(kind),
                                   ctypes.c_double(phase), ctypes.c_double(phase1),
                                   ctypes.c_double(phase2), qid_array)

    if ret == FALSE:
        raise QState_Error_OperateQgate()

def qstate_measure(qs, qid=None, angle=0.0, phase=0.0):

    if qid is None or qid == []:
        qid = [i for i in range(qs.qubit_num)]

    # operate
    qubit_num = len(qid)
    qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
    for i in range(len(qid)):
        qubit_id[i] = qid[i]
    IntArray = ctypes.c_int * MAX_QUBIT_NUM
    qid_array = IntArray(*qubit_id)

    mval = 0
    c_mval = ctypes.c_int(mval)

    lib.qstate_measure.restype = ctypes.c_int
    lib.qstate_measure.argtypes = [ctypes.POINTER(QState),
                                   ctypes.c_double, ctypes.c_double,
                                   ctypes.c_int, IntArray, ctypes.POINTER(ctypes.c_int)]
    ret = lib.qstate_measure(ctypes.byref(qs),
                             ctypes.c_double(angle), ctypes.c_double(phase),
                             ctypes.c_int(qubit_num), qid_array, ctypes.byref(c_mval))

    if ret == FALSE:
        raise QState_Error_Measure()

    mval = c_mval.value
    digits = len(qid)
    mval = '{:0{digits}b}'.format(mval, digits=digits)

    return mval

def qstate_measure_stats(qs, qid=None, shots=DEF_SHOTS, angle=0.0, phase=0.0):

    if qid is None or qid == []:
        qid = [i for i in range(qs.qubit_num)]

    # error check
    qstate_check_args(qs, kind=MEASURE, qid=qid, shots=shots, angle=angle, phase=phase)

    # operate
    qubit_num = len(qid)
    qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
    for i in range(len(qid)):
        qubit_id[i] = qid[i]
    IntArray = ctypes.c_int * MAX_QUBIT_NUM
    qid_array = IntArray(*qubit_id)

    mdata = None
    c_mdata = ctypes.c_void_p(mdata)

    lib.qstate_measure_stats.restype = ctypes.c_int
    lib.qstate_measure_stats.argtypes = [ctypes.POINTER(QState), ctypes.c_int,
                                         ctypes.c_double, ctypes.c_double,
                                         ctypes.c_int, IntArray,
                                         ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.qstate_measure_stats(ctypes.byref(qs), ctypes.c_int(shots),
                                   ctypes.c_double(angle), ctypes.c_double(phase),
                                   ctypes.c_int(qubit_num), qid_array, c_mdata)

    if ret == FALSE:
        raise QState_Error_Measure()

    out = ctypes.cast(c_mdata.value, ctypes.POINTER(MDataC))
        
    state_num = out.contents.state_num
    last_state = out.contents.last
    freq = ctypes.cast(out.contents.freq, ctypes.POINTER(ctypes.c_int*state_num))
    freq_list = [freq.contents[i] for i in range(state_num)]
    md = MData(freq_list=freq_list, last_state=last_state, qid=qid,
               qubit_num=qubit_num, state_num=state_num, angle=angle, phase=phase,
               is_bell=False)
    out.contents.free()

    return md

def qstate_measure_bell_stats(qs, qid=None, shots=DEF_SHOTS):

    if qid is None or qid == []:
        qid = [i for i in range(2)]
            
    # error check
    qstate_check_args(qs, kind=MEASURE_BELL, qid=qid, shots=shots, angle=None, phase=None)

    # operate
    state_num = 4
    qubit_num = 2
    qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
    for i in range(qubit_num):
        qubit_id[i] = qid[i]
    IntArray = ctypes.c_int * MAX_QUBIT_NUM
    qid_array = IntArray(*qubit_id)
        
    mdata = None
    c_mdata = ctypes.c_void_p(mdata)

    lib.qstate_measure_bell_stats.restype = ctypes.c_int
    lib.qstate_measure_bell_stats.argtypes = [ctypes.POINTER(QState), ctypes.c_int,
                                              ctypes.c_int, IntArray,
                                              ctypes.POINTER(ctypes.c_void_p)]

    ret = lib.qstate_measure_bell_stats(ctypes.byref(qs), ctypes.c_int(shots),
                                        ctypes.c_int(qubit_num), qid_array, c_mdata)

    if ret == FALSE:
        raise QState_Error_Measure()

    out = ctypes.cast(c_mdata.value, ctypes.POINTER(MDataC))
        
    last_state = out.contents.last
    freq = ctypes.cast(out.contents.freq, ctypes.POINTER(ctypes.c_int*state_num))
    freq_list = [freq.contents[i] for i in range(state_num)]
    md = MData(freq_list=freq_list, last_state=last_state, qid=qid,
               qubit_num=qubit_num, state_num=state_num, angle=0.0, phase=0.0,
               is_bell=True)
    out.contents.free()

    return md

def qstate_operate_qcirc(qstate, cmem, qcirc, shots, cid):

    lib.qstate_operate_qcirc.restype = ctypes.c_int
    lib.qstate_operate_qcirc.argtypes = [ctypes.POINTER(QState), ctypes.POINTER(CMem), ctypes.POINTER(QCirc)]

    if cmem is not None:

        cmem_num = cmem.cmem_num
        frequency = Counter()
        for n in range(shots):
            
            if n < shots - 1:
                qstate_tmp = qstate.clone()
                cmem_tmp = cmem.clone()
                ret = lib.qstate_operate_qcirc(ctypes.byref(qstate_tmp), ctypes.byref(cmem_tmp), ctypes.byref(qcirc))
                bit_array = ctypes.cast(cmem_tmp.bit_array, ctypes.POINTER(ctypes.c_int*cmem_num))
            else:
                ret = lib.qstate_operate_qcirc(ctypes.byref(qstate), ctypes.byref(cmem), ctypes.byref(qcirc))
                bit_array = ctypes.cast(cmem.bit_array, ctypes.POINTER(ctypes.c_int*cmem_num))

            if ret == FALSE:
                raise QState_Error_OperateQcirc()
        
            cmem_list = [bit_array.contents[i] for i in range(cmem_num)]
            cmem_list_part = [cmem_list[c] for c in cid]
            mval = "".join(map(str, cmem_list_part))

            frequency[mval] += 1

        return frequency

    else:

        c_cmem = ctypes.POINTER(CMem)()
        ret = lib.qstate_operate_qcirc(ctypes.byref(qstate), c_cmem, ctypes.byref(qcirc))

        if ret == FALSE:
            raise QState_Error_OperateQcirc()

        return None

def qstate_free(qs):

    lib.qstate_free.argtypes = [ctypes.POINTER(QState)]
    lib.qstate_free(ctypes.byref(qs))

def __gray_code(qs, n):

    for k in range(2**n):
        yield k^(k>>1)

def qstate_mcx(qs,qid=[]):

    # controled and target register
    qid_ctr = qid[:-1]
    qid_tar = qid[-1]
        
    # hadamard
    qs.h(qid_tar)

    # controlled-RZ(psi), psi=pi/(2**(bitnum-1))
    bitnum = len(qid_ctr)
    psi = 1.0/(2**(bitnum-1)) # unit=pi(radian)
    gray_pre = 0
    for gray in __gray_code(qs,bitnum):
        if gray == 0:
            continue
        msb = len(str(bin(gray)))-3
        chb = len(str(bin(gray^gray_pre)))-3
        if gray != 1:
            if chb == msb:
                chb -= 1
            qs.cx(qid_ctr[chb],qid_ctr[msb])
        qs.cp(qid_ctr[msb],qid_tar,phase=psi)
        psi = -psi
        gray_pre = gray
    
    # hadamard
    qs.h(qid_tar)
