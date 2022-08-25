# -*- coding: utf-8 -*-
""" run function for IBMQ """
from collections import Counter
import numpy as np

from qiskit import IBMQ, QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from qiskit.providers.ibmq import least_busy
from qiskit.circuit.library.standard_gates import SXdgGate

import qlazy.config as cfg
from qlazy.Result import Result

def run(qcirc=None, shots=1, cid=None, backend=None, out_state=False):
    """ run the quantum circuit """

    if qcirc is None:
        raise ValueError("quantum circuit must be specified.")

    qcirc_tmp = qcirc.clone()

    qubit_num = qcirc_tmp.qubit_num
    cmem_num = qcirc_tmp.cmem_num

    if cid is None:
        cid = list(range(cmem_num))

    if cmem_num < len(cid):
        raise ValueError("length of cid must be less than classical resister size of qcirc")

    qubit_reg = QuantumRegister(qubit_num)
    cmem_reg = [ClassicalRegister(1, name="c{}".format(i)) for i in range(cmem_num)]

    args = [qubit_reg] + cmem_reg
    qc = QuantumCircuit(*args)

    exist_measurement = False
    while True:
        kind = qcirc_tmp.kind_first()
        if kind is None:
            break

        (kind, qid, para, c, ctrl) = qcirc_tmp.pop_gate()

        if kind == cfg.MEASURE:
            exist_measurement = True
            if c is None:
                raise ValueError("cid (classical register ID) must be specified")
            qc.measure(qubit_reg[qid[0]], cmem_reg[c])

        elif kind == cfg.RESET:
            qc.reset(qubit_reg[qid[0]])

        else:
            __ibmq_add_qgate(qc, kind, qid, para[0] * np.pi, para[1] * np.pi, para[2] * np.pi,
                             ctrl, cmem_reg)

    # set backend
    if backend.device == 'aer_simulator':
        ibmq_backend = Aer.get_backend("aer_simulator")
    elif backend.device == 'aer_simulator_statevector':
        ibmq_backend = Aer.get_backend("aer_simulator_statevector")
    elif backend.device == 'aer_simulator_matrix_product_state':
        ibmq_backend = Aer.get_backend("aer_simulator_matrix_product_state")
    else:
        provider = IBMQ.load_account()
        if backend.device == 'least_busy':
            ibmq_backend = least_busy(provider.backends(simulator=False, operational=True))
        else:
            ibmq_backend_system_names = [b.name() for b in
                                         provider.backends(simulator=False, operational=True)]
            if backend.device in ibmq_backend_system_names:
                ibmq_backend = provider.get_backend(backend.device)
            else:
                raise ValueError("unknown device")

    # execute the circuit
    if exist_measurement is True:

        res = execute(qc, ibmq_backend, shots=shots).result()
        frq = res.get_counts(qc)

        frequency = Counter()
        for k, v in frq.items():
            bits_list = list(k.replace(' ', ''))
            bits_list.reverse()
            measured_bits_list = [bits_list[c] for c in cid]
            measured_bits = ''.join(measured_bits_list)
            if measured_bits != '':
                frequency[measured_bits] += v
            else:
                frequency = None
                break

    else:  # no measurement gates included
        cid = []
        frequency = None
        res = None

    info = {'quantum_circuit':qc, 'ibmq':res}

    result = Result()
    result.backend = backend
    result.qubit_num = qubit_num
    result.cmem_num = cmem_num
    result.cid = cid
    result.shots = shots
    result.frequency = frequency
    result.info = info

    return result

def __ibmq_add_qgate(qc, kind, qid, phase, phase1, phase2, ctrl, cmem_reg):

    # 1-qubit, 0-parameter gate
    if kind == cfg.PAULI_X:
        if ctrl is None:
            qc.x(qid[0])
        else:
            qc.x(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.PAULI_Y:
        if ctrl is None:
            qc.y(qid[0])
        else:
            qc.y(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.PAULI_Z:
        if ctrl is None:
            qc.z(qid[0])
        else:
            qc.z(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.ROOT_PAULI_X:
        if ctrl is None:
            qc.sx(qid[0])
        else:
            qc.sx(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.ROOT_PAULI_X_:
        if ctrl is None:
            qc.sxdg(qid[0])
        else:
            qc.sxdg(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.HADAMARD:
        if ctrl is None:
            qc.h(qid[0])
        else:
            qc.h(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.PHASE_SHIFT_S:
        if ctrl is None:
            qc.s(qid[0])
        else:
            qc.s(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.PHASE_SHIFT_S_:
        if ctrl is None:
            qc.sdg(qid[0])
        else:
            qc.sdg(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.PHASE_SHIFT_T:
        if ctrl is None:
            qc.t(qid[0])
        else:
            qc.t(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.PHASE_SHIFT_T_:
        if ctrl is None:
            qc.tdg(qid[0])
        else:
            qc.tdg(qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.IDENTITY:
        if ctrl is None:
            qc.i(qid[0])
        else:
            qc.i(qid[0]).c_if(cmem_reg[ctrl], 1)

    # 1-qubit, 1-parameter gate
    elif kind == cfg.ROTATION_X:
        if ctrl is None:
            qc.rx(phase, qid[0])
        else:
            qc.rx(phase, qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.ROTATION_Y:
        if ctrl is None:
            qc.ry(phase, qid[0])
        else:
            qc.ry(phase, qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.ROTATION_Z:
        if ctrl is None:
            qc.rz(phase, qid[0])
        else:
            qc.rz(phase, qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.PHASE_SHIFT:
        if ctrl is None:
            qc.p(phase, qid[0])
        else:
            qc.p(phase, qid[0]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.ROTATION_U1:
        if ctrl is None:
            qc.p(phase, qid[0])
        else:
            qc.p(phase, qid[0]).c_if(cmem_reg[ctrl], 1)

    # 1-qubit, 2-parameter gate
    elif kind == cfg.ROTATION_U2:
        if ctrl is None:
            qc.u(0.5 * np.pi, phase1, phase, qid[0])
        else:
            qc.u(0.5 * np.pi, phase1, phase, qid[0]).c_if(cmem_reg[ctrl], 1)

    # 1-qubit, 3-parameter gate
    elif kind == cfg.ROTATION_U3:
        if ctrl is None:
            qc.u(phase2, phase1, phase, qid[0])
        else:
            qc.u(phase2, phase1, phase, qid[0]).c_if(cmem_reg[ctrl], 1)

    # 2-qubit, 0-parameters gate
    elif kind == cfg.CONTROLLED_X:
        if ctrl is None:
            qc.cx(qid[0], qid[1])
        else:
            qc.cx(qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.CONTROLLED_Y:
        if ctrl is None:
            qc.cy(qid[0], qid[1])
        else:
            qc.cy(qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.CONTROLLED_Z:
        if ctrl is None:
            qc.cz(qid[0], qid[1])
        else:
            qc.cz(qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.CONTROLLED_XR:
        if ctrl is None:
            qc.csx(qid[0], qid[1])
        else:
            qc.csx(qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.CONTROLLED_XR_:
        q_csxdg = QuantumRegister(2)
        qc_csxdg = QuantumCircuit(q_csxdg)
        csxdg_gate = SXdgGate().control(1)
        qc_csxdg.append(csxdg_gate, q_csxdg)
        if ctrl is None:
            qc.append(qc_csxdg, qargs=[qid[0], qid[1]])
        else:
            qc.append(qc_csxdg, qargs=[qid[0], qid[1]]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.CONTROLLED_H:
        if ctrl is None:
            qc.ch(qid[0], qid[1])
        else:
            qc.ch(qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.CONTROLLED_S:
        if ctrl is None:
            qc.cp(0.5 * np.pi, qid[0], qid[1])
        else:
            qc.cp(0.5 * np.pi, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.CONTROLLED_S_:
        if ctrl is None:
            qc.cp(-0.5 * np.pi, qid[0], qid[1])
        else:
            qc.cp(-0.5 * np.pi, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.CONTROLLED_T:
        if ctrl is None:
            qc.cp(0.25 * np.pi, qid[0], qid[1])
        else:
            qc.cp(0.25 * np.pi, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.CONTROLLED_T_:
        if ctrl is None:
            qc.cp(-0.25 * np.pi, qid[0], qid[1])
        else:
            qc.cp(-0.25 * np.pi, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.CONTROLLED_P:
        if ctrl is None:
            qc.cp(phase, qid[0], qid[1])
        else:
            qc.cp(phase, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.SWAP_QUBITS:
        if ctrl is None:
            qc.swap(qid[0], qid[1])
        else:
            qc.swap(qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    # 2-qubit, 1-parameters gate
    elif kind == cfg.CONTROLLED_RX:
        if ctrl is None:
            qc.crx(phase, qid[0], qid[1])
        else:
            qc.crx(phase, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.CONTROLLED_RY:
        if ctrl is None:
            qc.cry(phase, qid[0], qid[1])
        else:
            qc.cry(phase, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.CONTROLLED_RZ:
        if ctrl is None:
            qc.crz(phase, qid[0], qid[1])
        else:
            qc.crz(phase, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    elif kind == cfg.CONTROLLED_U1:
        if ctrl is None:
            qc.cp(phase, qid[0], qid[1])
        else:
            qc.cp(phase, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    # 2-qubit, 2-parameters gate
    elif kind == cfg.CONTROLLED_U2:
        if ctrl is None:
            qc.cu(0.5 * np.pi, phase1, phase, 0, qid[0], qid[1])
        else:
            qc.cu(0.5 * np.pi, phase1, phase, 0, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    # 2-qubit, 3-parameters gate
    elif kind == cfg.CONTROLLED_U3:
        if ctrl is None:
            qc.cu(phase2, phase1, phase, 0, qid[0], qid[1])
        else:
            qc.cu(phase2, phase1, phase, 0, qid[0], qid[1]).c_if(cmem_reg[ctrl], 1)

    else:
        raise ValueError("unknown gate")
