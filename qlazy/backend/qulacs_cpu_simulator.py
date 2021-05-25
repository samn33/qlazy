# -*- coding: utf-8 -*-
import sys
import random
from collections import Counter
import numpy as np
import cmath

from qlazy.error import *
from qlazy.config import *
from qlazy.util import *

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

def init(qubit_num=0, backend=None):

    qstate = QuantumState(qubit_num)
    return qstate

def run(qubit_num=0, cmem_num=0, qstate=None, qcirc=[], cmem=[], shots=1, backend=None):

    # number of measurement (measurement_cnt)
    # and its position of last measurement (end_of_measurements)
    measurement_cnt = 0
    end_of_measurements = -1
    for j, c in enumerate(qcirc):
        if c['kind'] == MEASURE:
            measurement_cnt += 1
            end_of_measurements = j
    
    # qcirc have only one measurement at the end, or not
    if measurement_cnt == 1 and end_of_measurements == len(qcirc) - 1:
        only_one_measurement_end = True
    else:
        only_one_measurement_end = False
    
    # run the quantum circuit
    freq = Counter()
    for cnt in range(shots):
        for i, c in enumerate(qcirc):
            
            if c['kind'] == MEASURE:
                md = __qulacs_measure(qstate, qubit_num, qid=c['qid'], shots=1)
    
                if c['cid'] != None:
                    for k,mval in enumerate(list(md['last'])):
                        cmem[c['cid'][k]] = int(mval)
                        
                if end_of_measurements == i:
                    freq += md['frequency']
    
            else:
                if c['ctrl'] == None or cmem[c['ctrl']] == 1:
                    __qulacs_operate_qgate(qstate, qubit_num, kind=c['kind'], qid=c['qid'],
                                           phase=c['phase'], phase1=c['phase1'], phase2=c['phase2'])
    
            # qcirc have only one measurement
            if only_one_measurement_end == True and i == len(qcirc) - 2:
                md = __qulacs_measure(qstate, qubit_num, qid=qcirc[-1]['qid'], shots=shots)
                freq = md['frequency']
                
                if qcirc[-1]['cid'] != None:
                    for k,mval in enumerate(list(md['last'])):
                        cmem[qcirc[-1]['cid'][k]] = int(mval)
                break
            
        if only_one_measurement_end == True and i == len(qcirc) - 2:
            break
        
        # reset classical memory and qubits, if not end of the shots
        if cnt < shots-1:
            cmem = [0] * len(cmem)
            qstate.set_zero_state()
    
    # if end_of_measurements > 0:
    if measurement_cnt > 0:
        measured_qid = qcirc[end_of_measurements]['qid']
        result = {'measured_qid': measured_qid, 'frequency': freq}
    else:
        result = None

    return result
        
def reset(qstate=None, backend=None):

    if qstate != None:
        qstate.set_zero_state()

    # return True

def free(qstate=None, backend=None):

    if qstate != None:
        del qstate

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

def __qulacs_measure(qstate, qubit_num, qid, shots=1):

    # error check
    # qubit_num = qstate.get_qubit_count()
    if max(qid) >= qubit_num:
        raise ValueError

    # list of binary vectors for len(qid) bit integers
    qid_sorted = sorted(qid)
    mbits_list = []
    for i in range(2**len(qid)):
        # ex)
        # qid = [5,0,2] -> qid_sorted = [0,2,5]
        # i = (0,1,2), idx = (2,0,1)
        # bits = [q0,q1,q2] -> mbits = [q1,q2,q0]
        bits = list(map(int, list(format(i, '0{}b'.format(len(qid))))))
        mbits = [0] * len(qid)
        for i, q in enumerate(qid):
            idx = qid_sorted.index(q)
            mbits[idx] = bits[i]
        mbits_list.append(mbits)

    # list of probabilities
    prob_list = []
    prob = 0.0
    for mbits in mbits_list:
        args = [2] * qubit_num
        for j, q in enumerate(qid):
            args[q] = mbits[j]
        prob += qstate.get_marginal_probability(args)
        prob_list.append(prob)
    if prob_list[-1] != 1.0:
        prob_list[-1] = 1.0

    # frequency
    mval_data = []
    if shots > 1:
        for i in range(shots - 1):
            rand = random.random()
            for mbits, prob in zip(mbits_list, prob_list):
                mval = ''.join(map(str, mbits))
                if rand <= prob:
                    mval_data.append(mval)
                    break

    # last quantum state
    circ = QuantumCircuit(qubit_num)
    for i, q in enumerate(qid):
        circ.add_gate(Measurement(q, i))
    circ.update_quantum_state(qstate)

    last = ''.join(map(str, [qstate.get_classical_value(i) for i in range(len(qid))]))
    mval_data.append(last)
    frequency = Counter(mval_data)

    measured_data = {'measured_qid': qid, 'frequency': frequency, 'last': last}
    
    return measured_data
