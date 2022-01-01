# -*- coding: utf-8 -*-
import sys
import random
from collections import Counter
import numpy as np
import cmath

from qlazy.error import *
from qlazy.config import *
from qlazy.util import *
from qlazy.Result import *

from qulacs import QuantumState
from qulacs import QuantumCircuit
from qulacs.gate import Identity, X, Y, Z
from qulacs.gate import H, S, Sdag, T, Tdag, sqrtX, sqrtXdag, sqrtY, sqrtYdag
from qulacs.gate import CNOT, CZ, SWAP
from qulacs.gate import RX, RY, RZ
from qulacs.gate import U1, U2, U3
from qulacs.gate import Measurement
from qulacs.gate import DenseMatrix
from qulacs.gate import to_matrix_gate

GateFunctionName = {
    # 1-qubit, 0-parameter gate
    PAULI_X: 'X',
    PAULI_Y: 'Y',
    PAULI_Z: 'Z',
    ROOT_PAULI_X:'sqrtX',
    ROOT_PAULI_X_:'sqrtXdag',
    HADAMARD:'H',
    PHASE_SHIFT_S:'S',
    PHASE_SHIFT_S_:'Sdag',
    PHASE_SHIFT_T:'T',
    PHASE_SHIFT_T_:'Tdag',
    IDENTITY:'Identity',
    # 1-qubit, 1-parameter gate
    ROTATION_X:'RX',
    ROTATION_Y:'RY',
    ROTATION_Z:'RZ',
    PHASE_SHIFT:'__get_P',
    ROTATION_U1:'U1',
    # 1-qubit, 2-parameter gate
    ROTATION_U2:'U2',
    # 1-qubit, 3-parameter gate
    ROTATION_U3:'U3',
    # 2-qubit, 0-parameters gate
    CONTROLLED_X:'CNOT',
    CONTROLLED_Y:'__get_CY',
    CONTROLLED_Z:'CZ',
    CONTROLLED_XR:'__get_CXR',
    CONTROLLED_XR_:'__get_CXR_dg',
    CONTROLLED_H:'__get_CH',
    CONTROLLED_S:'__get_CS',
    CONTROLLED_S_:'__get_CS_dg',
    CONTROLLED_T:'__get_CT',
    CONTROLLED_T_:'__get_CT_dg',
    CONTROLLED_P:'__get_CP',
    SWAP_QUBITS:'SWAP',
    # 2-qubit, 1-parameters gate
    CONTROLLED_RX:'__get_CRX',
    CONTROLLED_RY:'__get_CRY',
    CONTROLLED_RZ:'__get_CRZ',
    CONTROLLED_U1:'__get_CU1',
    # 2-qubit, 2-parameters gate
    CONTROLLED_U2:'__get_CU2',
    # 2-qubit, 3-parameters gate
    CONTROLLED_U3:'__get_CU3',
}

def run_cpu(qcirc=[], shots=1, cid=[], backend=None):

    return __run_all(qcirc=qcirc, shots=shots, cid=cid, backend=backend, proc='CPU')

def run_gpu(qcirc=[], shots=1, cid=[], backend=None):

    return __run_all(qcirc=qcirc, shots=shots, cid=cid, backend=backend, proc='GPU')

def __run_all(qcirc=[], shots=1, cid=[], backend=None, proc='CPU'):

    #
    # get qubit_num and cmem_num
    #

    qubit_num = 0
    cmem_num = 0
    for c in qcirc:
        if (c['qid'] is not None) and (c['qid'] != []):
            qubit_num = max(qubit_num, max(c['qid']) + 1)
        if (c['cid'] is not None) and (c['cid'] != []):
            cmem_num = max(cmem_num, max(c['cid']) + 1)

    if cmem_num < len(cid):
        raise ValueError("length of cid must be less than classical resister size of qcirc")

    if cid == []:
        cid = [i for i in range(cmem_num)]

    #
    # initialize
    #

    if proc == 'CPU':
        qstate = QuantumState(qubit_num)
    else:
        qstate = QuantumStateGpu(qubit_num)
    cmem = [0] * cmem_num

    #
    # before measurement gate
    #

    exist_measurement = False
    for pos, c in enumerate(qcirc):

        if (c['ctrl'] == None or (c['ctrl'] != None and cmem[c['ctrl']] == 1)):

            if c['kind'] == MEASURE:
                exist_measurement = True
                break
            elif c['kind'] == RESET:
                __qulacs_reset(qstate, qubit_num, qid=c['qid'])
            else:
                __qulacs_operate_qgate(qstate, qubit_num, kind=c['kind'], qid=c['qid'],
                                       phase=c['phase'], phase1=c['phase1'], phase2=c['phase2'])

    if exist_measurement == False:
        info = {'quantumstate': qstate, 'cmem': cmem}
        result = Result(cid=cid, frequency=None, backend=backend, info=info)
        return result
    
    #
    # after measurement gate
    #

    frequency = Counter()
    qstate_tmp = None
    for cnt in range(shots):

        qstate_tmp = qstate.copy()

        for c in qcirc[pos:]:

            if (c['ctrl'] == None or (c['ctrl'] != None and cmem[c['ctrl']] == 1)):

                if c['kind'] == MEASURE:
                    m_list = __qulacs_measure(qstate_tmp, qubit_num, qid=c['qid'])

                    if len(cmem) > 0 and c['cid'] != None:
                        for k, m in enumerate(m_list):
                            cmem[c['cid'][k]] = m
                        
                elif c['kind'] == RESET:
                    __qulacs_reset(qstate_tmp, qubit_num, qid=c['qid'])
                
                else:
                    __qulacs_operate_qgate(qstate_tmp, qubit_num, kind=c['kind'], qid=c['qid'],
                                           phase=c['phase'], phase1=c['phase1'], phase2=c['phase2'])

        if len(cmem) > 0:
            mval = ''.join(map(str, [cmem[i] for i in cid]))
            frequency[mval] += 1
    
    if qstate_tmp is not None:
        qstate.load(qstate_tmp.get_vector())

    if len(frequency) == 0:
        frequency = None

    info = {'quantumstate': qstate, 'cmem': cmem}
    result = Result(cid=cid, frequency=frequency, backend=backend, info=info)
    
    return result
        
def __is_supported_qgate(kind):

    if kind in GateFunctionName.keys():
        return True
    else:
        return False

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

    if __is_supported_qgate(kind) == False:
        raise ValueError("not supported quantum gate")

    circ = QuantumCircuit(qubit_num)

    term_num = get_qgate_qubit_num(kind)
    para_num = get_qgate_param_num(kind)
    gate_function_name = GateFunctionName[kind]

    phase = phase * np.pi
    phase1 = phase1 * np.pi
    phase2 = phase2 * np.pi

    # the sign-definition of rotation gate on qulacs 
    if (kind == ROTATION_X or kind == ROTATION_Y or kind == ROTATION_Z or
        kind == CONTROLLED_RX or kind == CONTROLLED_RY or kind == CONTROLLED_RZ):
        phase = -phase
    # the argument-order-definition of U2 gate on qulacs 
    elif kind == ROTATION_U2 or kind == CONTROLLED_U2:
        phase1, phase = phase, phase1
    # the argument-order-definition of U3 gate on qulacs 
    elif kind == ROTATION_U3 or kind == CONTROLLED_U3:
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

def __qulacs_reset(qstate, qubit_num, qid):

    # error check
    # qubit_num = qstate.get_qubit_count()
    if max(qid) >= qubit_num:
        raise ValueError

    # last quantum state
    circ = QuantumCircuit(qubit_num)
    for i, q in enumerate(qid):
        circ.add_gate(Measurement(q, i))
    circ.update_quantum_state(qstate)

    circ_flip = QuantumCircuit(qubit_num)
    for i, q in enumerate(qid):
        if qstate.get_classical_value(i) == 1:
            circ_flip.add_gate(X(q))
    circ_flip.update_quantum_state(qstate)

def __qulacs_measure(qstate, qubit_num, qid):

    # error check
    if max(qid) >= qubit_num:
        raise ValueError

    # measurement
    circ = QuantumCircuit(qubit_num)
    for i, q in enumerate(qid):
        circ.add_gate(Measurement(q, i))
    circ.update_quantum_state(qstate)
    mval_list = [qstate.get_classical_value(i) for i in range(len(qid))]

    return mval_list
