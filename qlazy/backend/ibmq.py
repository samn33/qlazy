# -*- coding: utf-8 -*-
import sys
import random
from collections import Counter
import numpy as np
import cmath

from qlazy.error import *
from qlazy.config import *
from qlazy.util import *

from qiskit import IBMQ, QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from qiskit.qasm import pi
from qiskit.providers.ibmq import least_busy
from qiskit.circuit.library.standard_gates import SXdgGate

def init(qubit_num=0, backend=None):

    qstate = [0.+0.j] * (2**qubit_num)
    qstate[0] = 1.+0.j
    return qstate

def run(qubit_num=0, cmem_num=0, qstate=None, qcirc=[], cmem=[], shots=1, backend=None):

    if cmem == []:
        cmem_num = qubit_num
        cmem = [0] * cmem_num
        
    qubit_reg = QuantumRegister(qubit_num)
    cmem_reg = [ClassicalRegister(1, name="cmem_reg_{}".format(i)) for i in range(cmem_num)]

    args = [qubit_reg] + cmem_reg
    qc = QuantumCircuit(*args)

    measured_qid = []
    measured_cid = []

    for crc in qcirc:
        kind = crc['kind']
        qid = crc['qid']
        cid = crc['cid']
        phase = crc['phase'] * np.pi
        phase1 = crc['phase1'] * np.pi
        phase2 = crc['phase2'] * np.pi
        ctrl = crc['ctrl']

        term_num = get_qgate_qubit_num(kind)
        para_num = get_qgate_param_num(kind)

        if kind == MEASURE:
            if cid == None:
                cid = qid[:]
            if len(qid) != len(cid):
                raise ValueError("cid length is not equal to qid's ")
            qc.measure(qid, cid)
            measured_qid[:] = qid[:]
            measured_cid[:] = cid[:]

        else:
            __ibmq_add_qgate(qc, kind, qid, phase, phase1, phase2, ctrl, cmem_reg)

    # set backend
    if backend.device == 'qasm_simulator':
        ibmq_backend = Aer.get_backend("qasm_simulator")
    else:
        provider = IBMQ.load_account()
        if backend.device == 'least_busy':
            ibmq_backend = least_busy(provider.backends(simulator=False, operational=True))
        else:
            ibmq_backend_system_names = [b.name() for b in provider.backends(simulator=False, operational=True)]
            if backend.device in ibmq_backend_system_names:
                ibmq_backend = provider.get_backend(backend.device)
            else:
                raise ValueError("unknown device")

    # execute the circuit
    res = execute(qc, ibmq_backend, shots=shots).result()
    frq = res.get_counts(qc)

    # execute the circuit (for state vector)
    ibmq_sv_backend = Aer.get_backend("statevector_simulator")
    res_sv = execute(qc, ibmq_sv_backend).result()
    qstate[:] = reverse_bit_order(res_sv.get_statevector(qc))
    
    # if nothing are measured
    if measured_qid == None:
        return None

    # else if something are measured
    lut = {}
    for q,c in zip(measured_qid, measured_cid):
        lut[q] = c

    frequency = Counter()
    for k,v in frq.items():
        bits_list = list(k.replace(' ', ''))
        bits_list.reverse()
        measured_bits_list = []
        for q in measured_qid:
            measured_bits_list.append(bits_list[lut[q]])
        measured_bits = ''.join(measured_bits_list)
        frequency[measured_bits] += v

    result = {'measured_qid': measured_qid, 'frequency': frequency}
    return result
        
def reset(qstate=None, backend=None):

    pass

def free(qstate=None, backend=None):

    pass

def __ibmq_add_qgate(qc, kind, qid, phase, phase1, phase2, ctrl, cmem_reg):

    # 1-qubit, 0-parameter gate
    if kind == PAULI_X:
        if ctrl == None: qc.x(qid[0])
        else: qc.x(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == PAULI_Y:
        if ctrl == None: qc.y(qid[0])
        else: qc.y(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == PAULI_Z:
        if ctrl == None: qc.z(qid[0])
        else: qc.z(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == ROOT_PAULI_X:
        if ctrl == None: qc.sx(qid[0])
        else: qc.sx(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == ROOT_PAULI_X_:
        if ctrl == None: qc.sxdg(qid[0])
        else: qc.sxdg(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == HADAMARD:
        if ctrl == None: qc.h(qid[0])
        else: qc.h(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == PHASE_SHIFT_S:
        if ctrl == None: qc.s(qid[0])
        else: qc.s(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == PHASE_SHIFT_S_:
        if ctrl == None: qc.sdg(qid[0])
        else: qc.sdg(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == PHASE_SHIFT_T:
        if ctrl == None: qc.t(qid[0])
        else: qc.t(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == PHASE_SHIFT_T_:
        if ctrl == None: qc.tdg(qid[0])
        else: qc.tdg(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == IDENTITY:
        if ctrl == None: qc.i(qid[0])
        else: qc.i(qid[0]).c_if(cmem_reg[ctrl], 1)
        
    # 1-qubit, 1-parameter gate
    elif kind == ROTATION_X:
        if ctrl == None: qc.rx(phase, qid[0])
        else: qc.rx(phase, qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == ROTATION_Y:
        if ctrl == None: qc.ry(phase, qid[0])
        else: qc.ry(phase, qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == ROTATION_Z:
        if ctrl == None: qc.rz(phase, qid[0])
        else: qc.rz(phase, qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == PHASE_SHIFT:
        if ctrl == None: qc.p(phase, qid[0])
        else: qc.p(phase, qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == ROTATION_U1:
        if ctrl == None: qc.p(phase, qid[0])
        else: qc.p(phase, qid[0]).c_if(cmem_reg[ctrl], 1)
        
    # 1-qubit, 2-parameter gate
    elif kind == ROTATION_U2:
        if ctrl == None: qc.u(0.5 * np.pi, phase1, phase, qid[0])
        else: qc.u(0.5 * np.pi, phase1, phase, qid[0]).c_if(cmem_reg[ctrl], 1)
        
    # 1-qubit, 3-parameter gate
    elif kind == ROTATION_U3:
        if ctrl == None: qc.u(phase2, phase1, phase, qid[0])
        else: qc.u(phase2, phase1, phase, qid[0]).c_if(cmem_reg[ctrl], 1)

    # 2-qubit, 0-parameters gate
    elif kind == CONTROLLED_X:
        if ctrl == None: qc.cx(qid[0], qid[1])
        else: qc.cx(qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == CONTROLLED_Y:
        if ctrl == None: qc.cy(qid[0], qid[1])
        else: qc.cy(qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == CONTROLLED_Z:
        if ctrl == None: qc.cz(qid[0], qid[1])
        else: qc.cz(qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == CONTROLLED_XR:
        if ctrl == None: qc.csx(qid[0], qid[1])
        else: qc.csx(qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == CONTROLLED_XR_:
        q_csxdg = QuantumRegister(2)
        qc_csxdg = QuantumCircuit(q_csxdg)
        csxdg_gate = SXdgGate().control(1)
        qc_csxdg.append(csxdg_gate, q_csxdg)
        if ctrl == None: qc.append(qc_csxdg, qargs=[qid[0], qid[1]])
        else: qc.append(qc_csxdg, qargs=[qid[0], qid[1]]).c_if(cmem_reg[ctrl], 1)

    elif kind == CONTROLLED_H:
        if ctrl == None: qc.ch(qid[0], qid[1])
        else: qc.ch(qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == CONTROLLED_S:
        if ctrl == None: qc.cp(0.5 * np.pi, qid[0], qid[1])
        else: qc.cp(0.5 * np.pi, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == CONTROLLED_S_:
        if ctrl == None: qc.cp(-0.5 * np.pi, qid[0], qid[1])
        else: qc.cp(-0.5 * np.pi, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == CONTROLLED_T:
        if ctrl == None: qc.cp(0.25 * np.pi, qid[0], qid[1])
        else: qc.cp(0.25 * np.pi, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == CONTROLLED_T_:
        if ctrl == None: qc.cp(-0.25 * np.pi, qid[0], qid[1])
        else: qc.cp(-0.25 * np.pi, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == CONTROLLED_P:
        if ctrl == None: qc.cp(phase, qid[0], qid[1])
        else: qc.cp(phase, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == SWAP_QUBITS:
        if ctrl == None: qc.swap(qid[0], qid[1])
        else: qc.swap(qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    # 2-qubit, 1-parameters gate
    elif kind == CONTROLLED_RX:
        if ctrl == None: qc.crx(phase, qid[0], qid[1])
        else: qc.crx(phase, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == CONTROLLED_RY:
        if ctrl == None: qc.cry(phase, qid[0], qid[1])
        else: qc.cry(phase, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == CONTROLLED_RZ:
        if ctrl == None: qc.crz(phase, qid[0], qid[1])
        else: qc.crz(phase, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == CONTROLLED_U1:
        if ctrl == None: qc.cp(phase, qid[0], qid[1])
        else: qc.cp(phase, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    # 2-qubit, 2-parameters gate
    elif kind == CONTROLLED_U2:
        if ctrl == None: qc.cu(0.5 * np.pi, phase1, phase, 0, qid[0], qid[1])
        else: qc.cu(0.5 * np.pi, phase1, phase, 0, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    # 2-qubit, 3-parameters gate
    elif kind == CONTROLLED_U3:
        if ctrl == None: qc.cu(phase2, phase1, phase, 0, qid[0], qid[1])
        else: qc.cu(phase2, phase1, phase, 0, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    else:
        raise ValueError("unknown gate")
