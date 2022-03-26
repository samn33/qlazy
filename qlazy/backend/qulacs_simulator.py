# -*- coding: utf-8 -*-
""" run function for qulacs's cpu/gpu simulator """

from collections import Counter
import cmath
import numpy as np

from qulacs import QuantumState
from qulacs import QuantumCircuit
from qulacs.gate import X, Y, Z
from qulacs.gate import H, S, Sdag, T, Tdag, sqrtX, sqrtXdag
from qulacs.gate import CNOT, CZ, SWAP
from qulacs.gate import RX, RY, RZ
from qulacs.gate import U1, U2, U3
from qulacs.gate import Measurement
from qulacs.gate import DenseMatrix
from qulacs.gate import to_matrix_gate

import qlazy.config as cfg
from qlazy.util import get_qgate_qubit_num, get_qgate_param_num
from qlazy.Result import Result

GateFunctionName = {
    # 1-qubit, 0-parameter gate
    cfg.PAULI_X: 'X',
    cfg.PAULI_Y: 'Y',
    cfg.PAULI_Z: 'Z',
    cfg.ROOT_PAULI_X:'sqrtX',
    cfg.ROOT_PAULI_X_:'sqrtXdag',
    cfg.HADAMARD:'H',
    cfg.PHASE_SHIFT_S:'S',
    cfg.PHASE_SHIFT_S_:'Sdag',
    cfg.PHASE_SHIFT_T:'T',
    cfg.PHASE_SHIFT_T_:'Tdag',
    cfg.IDENTITY:'Identity',
    # 1-qubit, 1-parameter gate
    cfg.ROTATION_X:'RX',
    cfg.ROTATION_Y:'RY',
    cfg.ROTATION_Z:'RZ',
    cfg.PHASE_SHIFT:'__get_P',
    cfg.ROTATION_U1:'U1',
    # 1-qubit, 2-parameter gate
    cfg.ROTATION_U2:'U2',
    # 1-qubit, 3-parameter gate
    cfg.ROTATION_U3:'U3',
    # 2-qubit, 0-parameters gate
    cfg.CONTROLLED_X:'CNOT',
    cfg.CONTROLLED_Y:'__get_CY',
    cfg.CONTROLLED_Z:'CZ',
    cfg.CONTROLLED_XR:'__get_CXR',
    cfg.CONTROLLED_XR_:'__get_CXR_dg',
    cfg.CONTROLLED_H:'__get_CH',
    cfg.CONTROLLED_S:'__get_CS',
    cfg.CONTROLLED_S_:'__get_CS_dg',
    cfg.CONTROLLED_T:'__get_CT',
    cfg.CONTROLLED_T_:'__get_CT_dg',
    cfg.CONTROLLED_P:'__get_CP',
    cfg.SWAP_QUBITS:'SWAP',
    # 2-qubit, 1-parameters gate
    cfg.CONTROLLED_RX:'__get_CRX',
    cfg.CONTROLLED_RY:'__get_CRY',
    cfg.CONTROLLED_RZ:'__get_CRZ',
    cfg.CONTROLLED_U1:'__get_CU1',
    # 2-qubit, 2-parameters gate
    cfg.CONTROLLED_U2:'__get_CU2',
    # 2-qubit, 3-parameters gate
    cfg.CONTROLLED_U3:'__get_CU3',
}

def run_cpu(qcirc=None, shots=1, cid=None, backend=None):
    """ run the quantum circuit (CPU) """

    return __run_all(qcirc=qcirc, shots=shots, cid=cid, backend=backend, proc='CPU')

def run_gpu(qcirc=None, shots=1, cid=None, backend=None):
    """ run the quantum circuit (GPU) """

    return __run_all(qcirc=qcirc, shots=shots, cid=cid, backend=backend, proc='GPU')

def __run_all(qcirc=None, shots=1, cid=None, backend=None, proc='CPU'):

    if qcirc is None:
        raise ValueError("quantum circuit must be specified.")

    qubit_num = qcirc.qubit_num
    cmem_num = qcirc.cmem_num

    if cid is None:
        cid = list(range(cmem_num))

    if cmem_num < len(cid):
        raise ValueError("length of cid must be less than classical resister size of qcirc")

    #
    # initialize
    #

    if proc == 'CPU':
        qstate = QuantumState(qubit_num)
    else:
        from qulacs import QuantumStateGpu
        qstate = QuantumStateGpu(qubit_num)
    cmem = [0] * cmem_num

    #
    # before measurement gate
    #

    while True:
        kind = qcirc.kind_first()
        if kind is None or kind is cfg.MEASURE or kind is cfg.RESET:
            break

        (kind, qid, para, c, ctrl) = qcirc.pop_gate()
        if ctrl is None or (ctrl is not None and cmem[ctrl] == 1):
            __qulacs_operate_qgate(qstate, qubit_num, kind=kind, qid=qid,
                                   phase=para[0], phase1=para[1], phase2=para[2])

    if kind is None:
        info = {'quantumstate': qstate, 'cmem': cmem}

        result = Result()
        result.qubit_num = qubit_num
        result.cmem_num = cmem_num
        result.cid = cid
        result.shots = shots
        result.frequency = None
        result.backend = backend
        result.info = info
        return result

    #
    # after measurement gate
    #

    frequency = Counter()
    qstate_tmp = None
    for _ in range(shots):

        qstate_tmp = qstate.copy()
        qcirc_tmp = qcirc.clone()

        while True:

            kind = qcirc_tmp.kind_first()
            if kind is None:
                break

            # elif kind == cfg.MEASURE:
            if kind == cfg.MEASURE:
                (kind, qid, para, c, ctrl) = qcirc_tmp.pop_gate()
                mval = __qulacs_measure(qstate_tmp, qubit_num, qid[0])
                if c is not None:
                    cmem[c] = mval

            elif kind == cfg.RESET:
                (kind, qid, para, c, ctrl) = qcirc_tmp.pop_gate()
                __qulacs_reset(qstate_tmp, qubit_num, qid[0])

            else:
                (kind, qid, para, c, ctrl) = qcirc_tmp.pop_gate()
                if (ctrl is None or (ctrl is not None and cmem[ctrl] == 1)):
                    __qulacs_operate_qgate(qstate_tmp, qubit_num, kind=kind, qid=qid,
                                           phase=para[0], phase1=para[1], phase2=para[2])

        if len(cmem) > 0:
            mval = ''.join(map(str, [cmem[i] for i in cid]))
            frequency[mval] += 1

    if qstate_tmp is not None:
        qstate.load(qstate_tmp.get_vector())

    if len(frequency) == 0:
        frequency = None

    info = {'quantumstate': qstate, 'cmem': cmem}

    result = Result()
    result.backend = backend
    result.qubit_num = qubit_num
    result.cmem_num = cmem_num
    result.cid = cid
    result.shots = shots
    result.frequency = frequency
    result.info = info

    return result

def __is_supported_qgate(kind):

    return kind in GateFunctionName.keys()

# not supported as pre-defined gates

def __get_P(q0, phase):

    exp = cmath.exp(1.j * phase)
    gate = DenseMatrix(q0, [[1., 0.], [0., exp]])
    return gate

def __get_CY(q0, q1):

    gate = to_matrix_gate(Y(q1))
    gate.add_control_qubit(q0, 1)
    return gate

def __get_CXR(q0, q1):

    gate = to_matrix_gate(sqrtX(q1))
    gate.add_control_qubit(q0, 1)
    return gate

def __get_CXR_dg(q0, q1):

    gate = to_matrix_gate(sqrtXdag(q1))
    gate.add_control_qubit(q0, 1)
    return gate

def __get_CH(q0, q1):

    gate = to_matrix_gate(H(q1))
    gate.add_control_qubit(q0, 1)
    return gate

def __get_CS(q0, q1):

    gate = to_matrix_gate(S(q1))
    gate.add_control_qubit(q0, 1)
    return gate

def __get_CS_dg(q0, q1):

    gate = to_matrix_gate(Sdag(q1))
    gate.add_control_qubit(q0, 1)
    return gate

def __get_CT(q0, q1):

    gate = to_matrix_gate(T(q1))
    gate.add_control_qubit(q0, 1)
    return gate

def __get_CT_dg(q0, q1):

    gate = to_matrix_gate(Tdag(q1))
    gate.add_control_qubit(q0, 1)
    return gate

def __get_CP(q0, q1, phase):

    exp = cmath.exp(1.j * phase)
    gate = DenseMatrix(q1, [[1., 0.], [0., exp]])
    gate.add_control_qubit(q0, 1)
    return gate

def __get_CRX(q0, q1, phase):

    gate = to_matrix_gate(RX(q1, phase))
    gate.add_control_qubit(q0, 1)
    return gate

def __get_CRY(q0, q1, phase):

    gate = to_matrix_gate(RY(q1, phase))
    gate.add_control_qubit(q0, 1)
    return gate

def __get_CRZ(q0, q1, phase):

    gate = to_matrix_gate(RZ(q1, phase))
    gate.add_control_qubit(q0, 1)
    return gate

def __get_CU1(q0, q1, phase):

    gate = to_matrix_gate(U1(q1, phase))
    gate.add_control_qubit(q0, 1)
    return gate

def __get_CU2(q0, q1, phase, phase1):

    gate = to_matrix_gate(U2(q1, phase, phase1))
    gate.add_control_qubit(q0, 1)
    return gate

def __get_CU3(q0, q1, phase, phase1, phase2):

    gate = to_matrix_gate(U3(q1, phase, phase1, phase2))
    gate.add_control_qubit(q0, 1)
    return gate

def __qulacs_operate_qgate(qstate, qubit_num, kind, qid, phase, phase1, phase2):

    if __is_supported_qgate(kind) is False:
        raise ValueError("not supported quantum gate")

    circ = QuantumCircuit(qubit_num)

    term_num = get_qgate_qubit_num(kind)
    para_num = get_qgate_param_num(kind)
    gate_function_name = GateFunctionName[kind]

    phase = phase * np.pi
    phase1 = phase1 * np.pi
    phase2 = phase2 * np.pi

    # the sign-definition of rotation gate on qulacs
    if (kind in (cfg.ROTATION_X, cfg.ROTATION_Y, cfg.ROTATION_Z,
                 cfg.CONTROLLED_RX, cfg.CONTROLLED_RY, cfg.CONTROLLED_RZ)):
        phase = -phase
    # the argument-order-definition of U2 gate on qulacs
    elif kind in (cfg.ROTATION_U2, cfg.CONTROLLED_U2):
        phase1, phase = phase, phase1
    # the argument-order-definition of U3 gate on qulacs
    elif kind in (cfg.ROTATION_U3, cfg.CONTROLLED_U3):
        phase2, phase = phase, phase2

    if term_num == 1 and para_num == 0:
        circ.add_gate(eval(gate_function_name)(qid[0]))
    elif term_num == 1 and para_num == 1:
        circ.add_gate(eval(gate_function_name)(qid[0], phase))
    elif term_num == 1 and para_num == 2:
        circ.add_gate(eval(gate_function_name)(qid[0], phase, phase1))
    elif term_num == 1 and para_num == 3:
        circ.add_gate(eval(gate_function_name)(qid[0], phase, phase1, phase2))
    elif term_num == 2 and para_num == 0:
        circ.add_gate(eval(gate_function_name)(qid[0], qid[1]))
    elif term_num == 2 and para_num == 1:
        circ.add_gate(eval(gate_function_name)(qid[0], qid[1], phase))
    elif term_num == 2 and para_num == 2:
        circ.add_gate(eval(gate_function_name)(qid[0], qid[1], phase, phase1))
    elif term_num == 2 and para_num == 3:
        circ.add_gate(eval(gate_function_name)(qid[0], qid[1], phase, phase1, phase2))
    else:
        raise ValueError("not supported terminal or parameter-number")

    circ.update_quantum_state(qstate)

def __qulacs_reset(qstate, qubit_num, q):

    # error check
    if q >= qubit_num:
        raise ValueError("reset qubit id is out of bound")

    circ = QuantumCircuit(qubit_num)
    circ.add_gate(Measurement(q, 0))
    circ.update_quantum_state(qstate)
    circ_flip = QuantumCircuit(qubit_num)
    if qstate.get_classical_value(0) == 1:
        circ_flip.add_gate(X(q))
        circ_flip.update_quantum_state(qstate)

def __qulacs_measure(qstate, qubit_num, q):

    # error check
    if q >= qubit_num:
        raise ValueError("measurement qubit id is out of bound")

    circ = QuantumCircuit(qubit_num)
    circ.add_gate(Measurement(q, 0))
    circ.update_quantum_state(qstate)
    mval = qstate.get_classical_value(0)

    return mval
