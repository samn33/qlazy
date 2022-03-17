# -*- coding: utf-8 -*-
""" various kind of utilities """
import math
import numpy as np

import qlazy.config as cfg

def get_lib_ext():
    """ get library extension (for Mac OS)"""

    import platform
    if platform.system() == 'Darwin':
        return 'dylib'
    return 'so'

def qstate_check_args(qs, kind=None, qid=None):
    """ check arguments for qstate """

    for q in qid:
        if (q >= qs.qubit_num) or (q < 0):
            raise IndexError("index out of range.")

    qnum = get_qgate_qubit_num(kind)

    if qnum == 0:  # any qubit number
        # check qubit number
        if len(qid) > qs.qubit_num:
            raise IndexError("Too many arguments.")
        if len(qid) < 1:
            raise IndexError("Need more arguments.")
        # check same qubit number
        if len(set(qid)) != len(qid):
            raise IndexError("Same qubit ID.")

    elif qnum == 1:
        # check qubit number
        if len(qid) > qnum:
            raise IndexError("Too many arguments.")
        if len(qid) < qnum:
            raise IndexError("Need more arguments.")

    elif qnum == 2:
        # check qubit number
        if len(qid) > qnum:
            raise IndexError("Too many arguments.")
        if len(qid) < qnum:
            raise IndexError("Need more arguments.")
        # check same qubit number
        if qid[0] == qid[1]:
            raise IndexError("Same qubit ID.")

    elif qnum == 3:
        # check qubit number
        if len(qid) > qnum:
            raise IndexError("Too many arguments.")
        if len(qid) < qnum:
            raise IndexError("Need more arguments.")
        # check same qubit id
        if qid[0] == qid[1] or qid[1] == qid[2] or qid[2] == qid[0]:
            raise IndexError("Same qubit ID.")

    return True

def densop_check_args(de, kind=None, qid=None):
    """ check arguments for densop """

    qubit_num = int(math.log2(de.row))

    for q in qid:
        if (q >= qubit_num) or (q < 0):
            raise IndexError("index out of range.")

    qnum = get_qgate_qubit_num(kind)

    if qnum == 0:  # any qubit number
        # check qubit number
        if len(qid) > qubit_num:
            raise IndexError("Too many arguments.")
        if len(qid) < 1:
            raise IndexError("Need more arguments.")

        # check same qubit number
        if len(set(qid)) != len(qid):
            raise IndexError("Same qubit ID.")

    elif qnum == 1:
        # check qubit number
        if len(qid) > qnum:
            raise IndexError("Too many arguments.")
        if len(qid) < qnum:
            raise IndexError("Need more arguments.")

    elif qnum == 2:
        # check qubit number
        if len(qid) > qnum:
            raise IndexError("Too many arguments.")
        if len(qid) < qnum:
            raise IndexError("Need more arguments.")

        # check same qubit number
        if qid[0] == qid[1]:
            raise IndexError("Same qubit ID.")

    elif qnum == 3:
        # check qubit number
        if len(qid) > qnum:
            raise IndexError("Too many arguments.")
        if len(qid) < qnum:
            raise IndexError("Need more arguments.")

        # check same qubit id
        if qid[0] == qid[1] or qid[1] == qid[2] or qid[2] == qid[0]:
            raise IndexError("Same qubit ID.")

    return True

def get_qgate_qubit_num(kind=None):
    """ get qubit number for the quantum gate """

    if kind in (cfg.SHOW, cfg.MEASURE, cfg.MEASURE_X, cfg.MEASURE_Y,
                cfg.MEASURE_Z, cfg.RESET):  # 0 if any number
        return 0
    if ((kind in (cfg.BLOCH, cfg.PAULI_X, cfg.PAULI_Y, cfg.PAULI_Z, cfg.ROOT_PAULI_X,
                  cfg.ROOT_PAULI_X_, cfg.HADAMARD, cfg.PHASE_SHIFT_S, cfg.PHASE_SHIFT_S_,
                  cfg.PHASE_SHIFT_T, cfg.PHASE_SHIFT_T_, cfg.PHASE_SHIFT, cfg.ROTATION_X,
                  cfg.ROTATION_Y, cfg.ROTATION_Z, cfg.ROTATION_U1, cfg.ROTATION_U2,
                  cfg.ROTATION_U3))):
        return 1
    if (kind in (cfg.CONTROLLED_X, cfg.CONTROLLED_Y, cfg.CONTROLLED_Z, cfg.CONTROLLED_XR,
                 cfg.CONTROLLED_XR_, cfg.CONTROLLED_H, cfg.CONTROLLED_S, cfg.CONTROLLED_S_,
                 cfg.CONTROLLED_T, cfg.CONTROLLED_T_, cfg.SWAP_QUBITS, cfg.CONTROLLED_P,
                 cfg.CONTROLLED_RX, cfg.CONTROLLED_RY, cfg.CONTROLLED_RZ, cfg.CONTROLLED_U1,
                 cfg.CONTROLLED_U2, cfg.CONTROLLED_U3, cfg.MEASURE_BELL,
                 cfg.ROTATION_XX, cfg.ROTATION_YY, cfg.ROTATION_ZZ)):
        return 2

    raise ValueError("unknown quantum gate.")

def get_qgate_param_num(kind=None):
    """ get parameter number for the quantum gate """

    if (kind in (cfg.SHOW, cfg.BLOCH, cfg.MEASURE, cfg.MEASURE_X, cfg.MEASURE_Y,
                 cfg.MEASURE_Z, cfg.MEASURE_BELL, cfg.RESET, cfg.PAULI_X, cfg.PAULI_Y,
                 cfg.PAULI_Z, cfg.ROOT_PAULI_X, cfg.ROOT_PAULI_X_, cfg.HADAMARD,
                 cfg.PHASE_SHIFT_S, cfg.PHASE_SHIFT_S_, cfg.PHASE_SHIFT_T,
                 cfg.PHASE_SHIFT_T_, cfg.CONTROLLED_X, cfg.CONTROLLED_Y, cfg.CONTROLLED_Z,
                 cfg.CONTROLLED_XR, cfg.CONTROLLED_XR_, cfg.CONTROLLED_H,
                 cfg.CONTROLLED_S, cfg.CONTROLLED_S_, cfg.CONTROLLED_T, cfg.CONTROLLED_T_,
                 cfg.SWAP_QUBITS)):
        return 0
    if (kind in (cfg.PHASE_SHIFT, cfg.ROTATION_X, cfg.ROTATION_Y, cfg.ROTATION_Z,
                 cfg.ROTATION_U1, cfg.CONTROLLED_P, cfg.CONTROLLED_RX, cfg.CONTROLLED_RY,
                 cfg.CONTROLLED_RZ, cfg.CONTROLLED_U1,
                 cfg.ROTATION_XX, cfg.ROTATION_YY, cfg.ROTATION_ZZ)):
        return 1
    if kind in (cfg.ROTATION_U2, cfg.CONTROLLED_U2):
        return 2
    if kind in (cfg.ROTATION_U3, cfg.CONTROLLED_U3):
        return 3

    raise ValueError("unknown quantum gate.")

def is_clifford_gate(kind):
    """ is the gate clifford? """

    return kind in (cfg.PAULI_X, cfg.PAULI_Y, cfg.PAULI_Z, cfg.HADAMARD,
                    cfg.PHASE_SHIFT_S, cfg.PHASE_SHIFT_S_,
                    cfg.CONTROLLED_X, cfg.CONTROLLED_Y, cfg.CONTROLLED_Z)

def is_non_clifford_gate(kind):
    """ is the gate non-clifford? """

    return (is_clifford_gate(kind) is False and
            is_measurement_gate(kind) is False and
            is_reset_gate(kind) is False)

def is_measurement_gate(kind):
    """ is the gate measurement? """

    return kind in (cfg.MEASURE, cfg.MEASURE_X, cfg.MEASURE_Y,
                    cfg.MEASURE_Z, cfg.MEASURE_BELL)

def is_reset_gate(kind):
    """ is the gate reset? """

    return kind == cfg.RESET

def reverse_bit_order(vec_in):
    """ reverse bit order of the state vector """

    vec_out = [0] * len(vec_in)
    digits = float(np.log2(len(vec_in)))
    if not digits.is_integer():
        raise ValueError("length of vector must be power of two")

    for idx, val in enumerate(vec_in):
        idx_binstr = '{:0{digits}b}'.format(idx, digits=int(digits))
        idx_binstr_rev = ''.join(reversed(list(idx_binstr)))
        idx_rev = int(idx_binstr_rev, 2)
        vec_out[idx_rev] = val

    return vec_out
