# -*- coding: utf-8 -*-
""" wrapper functions for QState """
import ctypes
from ctypes.util import find_library
from collections import Counter
import pathlib

import qlazy.config as cfg
from qlazy.util import get_lib_ext
from qlazy.Stabilizer import Stabilizer
from qlazy.QCirc import QCirc
from qlazy.CMem import CMem

lib = ctypes.CDLL(str(pathlib.Path(__file__).with_name('libqlz.'+get_lib_ext())))
libc = ctypes.CDLL(find_library("c"), mode=ctypes.RTLD_GLOBAL)

def stabilizer_init(gene_num=None, qubit_num=None, seed=None):
    """ initialize Stabilizer object """

    libc.srand(ctypes.c_int(seed))

    stab = None
    c_stab = ctypes.c_void_p(stab)

    lib.stabilizer_init.restype = ctypes.c_bool
    lib.stabilizer_init.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                    ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.stabilizer_init(ctypes.c_int(gene_num), ctypes.c_int(qubit_num),
                              ctypes.c_int(seed), c_stab)

    if ret is False:
        raise ValueError("can't initialize Stabilizer object.")

    return c_stab

def stabilizer_copy(sb):
    """ copy the stabilizer state """

    try:
        stab = None
        c_stab = ctypes.c_void_p(stab)

        lib.stabilizer_copy.restype = ctypes.c_bool
        lib.stabilizer_copy.argtypes = [ctypes.POINTER(Stabilizer),
                                        ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.stabilizer_copy(ctypes.byref(sb), c_stab)

        if ret is False:
            raise ValueError("can't copy the Stabilizer object.")

        return c_stab

    except Exception:
        raise ValueError("can't copy the Stabilizer object.")

def stabilizer_set_pauli_fac(sb, gene_id, pauli_fac):
    """ set pauli factor to the stabilizer state """

    lib.stabilizer_set_pauli_fac.restype = ctypes.c_bool
    lib.stabilizer_set_pauli_fac.argtypes = [ctypes.POINTER(Stabilizer), ctypes.c_int,
                                             ctypes.c_int]
    ret = lib.stabilizer_set_pauli_fac(ctypes.byref(sb), ctypes.c_int(gene_id),
                                       ctypes.c_int(pauli_fac))

    if ret is False:
        raise ValueError("can't set pauli factor to the Stabilizer object.")

    return ret

def stabilizer_get_pauli_fac(sb, gene_id):
    """ get pauli factor from the stabilizer state """

    pauli_fac = cfg.REAL_PLUS
    c_pauli_fac = ctypes.c_int(pauli_fac)

    lib.stabilizer_get_pauli_fac.restype = ctypes.c_bool
    lib.stabilizer_get_pauli_fac.argtypes = [ctypes.POINTER(Stabilizer), ctypes.c_int,
                                             ctypes.POINTER(ctypes.c_int)]
    ret = lib.stabilizer_get_pauli_fac(ctypes.byref(sb), ctypes.c_int(gene_id),
                                       ctypes.byref(c_pauli_fac))

    if ret is False:
        raise ValueError("can't get pauli factor from the Stabilizer object.")

    pauli_fac = c_pauli_fac.value

    return pauli_fac

def stabilizer_set_pauli_op(sb, gene_id=None, qubit_id=None, pauli_op=None):
    """ set pauli operator to the stabilizer state """

    lib.stabilizer_set_pauli_op.restype = ctypes.c_bool
    lib.stabilizer_set_pauli_op.argtypes = [ctypes.POINTER(Stabilizer), ctypes.c_int,
                                            ctypes.c_int, ctypes.c_int]
    ret = lib.stabilizer_set_pauli_op(ctypes.byref(sb), ctypes.c_int(gene_id),
                                      ctypes.c_int(qubit_id), ctypes.c_int(pauli_op))

    if ret is False:
        raise ValueError("can't set pauli operator to the Stabilizer object.")

    return ret

def stabilizer_get_pauli_op(sb, gene_id=None, qubit_id=None):
    """ get pauli operator from the stabilizer state """

    pauli_op = cfg.IDENTITY
    c_pauli_op = ctypes.c_int(pauli_op)

    lib.stabilizer_get_pauli_op.restype = ctypes.c_bool
    lib.stabilizer_get_pauli_op.argtypes = [ctypes.POINTER(Stabilizer), ctypes.c_int,
                                            ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    ret = lib.stabilizer_get_pauli_op(ctypes.byref(sb), ctypes.c_int(gene_id),
                                      ctypes.c_int(qubit_id), ctypes.byref(c_pauli_op))

    if ret is False:
        raise ValueError("can't get pauli operator from the Stabilizer object.")

    pauli_op = c_pauli_op.value

    return pauli_op

def stabilizer_operate_qgate(sb, kind=None, q0=None, q1=None):
    """ operate quantum gate to the stabilizer state """

    lib.stabilizer_operate_qgate.restype = ctypes.c_bool
    lib.stabilizer_operate_qgate.argtypes = [ctypes.POINTER(Stabilizer), ctypes.c_int,
                                             ctypes.c_int, ctypes.c_int]
    ret = lib.stabilizer_operate_qgate(ctypes.byref(sb), ctypes.c_int(kind),
                                       ctypes.c_int(q0), ctypes.c_int(q1))

    if ret is False:
        raise ValueError("can't operate quantum gate to the Stabilizer object.")

def stabilizer_get_rank(sb):
    """ get rank of the stabilizer state """

    rank = 0
    c_rank = ctypes.c_int(rank)

    lib.stabilizer_get_rank.restype = ctypes.c_bool
    lib.stabilizer_get_rank.argtypes = [ctypes.POINTER(Stabilizer),
                                        ctypes.POINTER(ctypes.c_int)]
    ret = lib.stabilizer_get_rank(ctypes.byref(sb), ctypes.byref(c_rank))

    if ret is False:
        raise ValueError("can't get rank of the Stabilizer object.")

    rank = c_rank.value

    return rank

def stabilizer_measure(sb, q=None):
    """ measure the stabilizer state """

    prob = [0.0, 0.0]
    DoubleArray = ctypes.c_double * 2
    c_prob = DoubleArray(*prob)

    mval = 0
    c_mval = ctypes.c_int(mval)

    lib.stabilizer_measure.restype = ctypes.c_bool
    lib.stabilizer_measure.argtypes = [ctypes.POINTER(Stabilizer), ctypes.c_int,
                                       DoubleArray, ctypes.POINTER(ctypes.c_int)]
    ret = lib.stabilizer_measure(ctypes.byref(sb), ctypes.c_int(q),
                                 c_prob, ctypes.byref(c_mval))

    if ret is False:
        raise ValueError("can't measure the Stabilizer object.")

    mval = c_mval.value

    return mval

def stabilizer_operate_qcirc(sb, cmem, qcirc, shots, cid):
    """ operate quantum circuit to the stabilizer state """

    lib.stabilizer_operate_qcirc.restype = ctypes.c_bool
    lib.stabilizer_operate_qcirc.argtypes = [ctypes.POINTER(Stabilizer),
                                             ctypes.POINTER(CMem), ctypes.POINTER(QCirc)]

    if cmem is not None:

        cmem_num = cmem.cmem_num
        frequency = Counter()
        for n in range(shots):

            if n < shots - 1:
                sb_tmp = sb.clone()
                cmem_tmp = cmem.clone()
                ret = lib.stabilizer_operate_qcirc(ctypes.byref(sb_tmp),
                                                   ctypes.byref(cmem_tmp), ctypes.byref(qcirc))
                bit_array = ctypes.cast(cmem_tmp.bit_array, ctypes.POINTER(ctypes.c_ubyte*cmem_num))
            else:
                ret = lib.stabilizer_operate_qcirc(ctypes.byref(sb),
                                                   ctypes.byref(cmem), ctypes.byref(qcirc))
                bit_array = ctypes.cast(cmem.bit_array, ctypes.POINTER(ctypes.c_ubyte*cmem_num))

            if ret is False:
                raise ValueError("can't operate quantum circuit to the Stabilizer object.")

            cmem_list = [bit_array.contents[i] for i in range(cmem_num)]
            mval = "".join(map(str, [cmem_list[c] for c in cid]))

            frequency[mval] += 1

        return frequency

    c_cmem = ctypes.POINTER(CMem)()
    ret = lib.stabilizer_operate_qcirc(ctypes.byref(sb), c_cmem, ctypes.byref(qcirc))

    if ret is False:
        raise ValueError("can't operate quantum circuit to the Stabilizer object.")

    return None

def stabilizer_free(stab):
    """ free memory of Stabilizer object """

    lib.stabilizer_free.argtypes = [ctypes.POINTER(Stabilizer)]
    lib.stabilizer_free(ctypes.byref(stab))
