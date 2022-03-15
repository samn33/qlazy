# -*- coding: utf-8 -*-
""" run function for AWS """
from collections import Counter
import numpy as np

# import boto3
# from braket.aws import AwsDevice
from braket.devices import LocalSimulator
from braket.circuits import Circuit

import qlazy.config as cfg
from qlazy.Result import Result

def __aws_add_qgate(qc_aws, kind, q0, q1, angle):
    """ add gate to aws circuit """

    # 1-qubit, 0-parameter gate
    if kind == cfg.PAULI_X:
        qc_aws.x(q0)

    elif kind == cfg.PAULI_Z:
        qc_aws.z(q0)

    elif kind == cfg.HADAMARD:
        qc_aws.h(q0)

    elif kind == cfg.PHASE_SHIFT_S:
        qc_aws.s(q0)

    elif kind == cfg.PHASE_SHIFT_S_:
        qc_aws.si(q0)

    elif kind == cfg.PHASE_SHIFT_T:
        qc_aws.t(q0)

    elif kind == cfg.PHASE_SHIFT_T_:
        qc_aws.ti(q0)

    # 1-qubit, 1-parameter gate
    elif kind == cfg.ROTATION_X:
        qc_aws.rx(q0, angle=angle)

    elif kind == cfg.ROTATION_Z:
        qc_aws.rz(q0, angle=angle)

    # 2-qubit, 0-parameters gate
    elif kind == cfg.CONTROLLED_X:
        qc_aws.cnot(q0, q1)

    elif kind == cfg.CONTROLLED_Z:
        qc_aws.cz(q0, q1)

    elif kind == cfg.CONTROLLED_H:
        pi_2 = 0.5 * np.pi
        pi_4 = 0.25 * np.pi
        qc_aws.ry(1, angle=-pi_4).cnot(0, 1).rz(1, angle=-pi_2)
        qc_aws.cnot(0, 1).rz(1, angle=pi_2).ry(1, angle=pi_4)
        qc_aws.phaseshift(0, angle=pi_2)

    # 2-qubit, 1-parameters gate
    elif kind == cfg.CONTROLLED_RZ:
        qc_aws.rz(q1, angle=angle/2).cnot(q0, q1).rz(q1, angle=-angle/2).cnot(q0, q1)

    else:
        raise ValueError("unknown gate")

def __convert_to_aws_circuit(qc_qlazy):
    """ convert qlazy circuit to aws circuit """

    # not supported if any unitary gate exist after non-unitary gate (measure,rest)
    qubit_num = qc_qlazy.qubit_num
    measured_info = [-1] * qubit_num # all -1 means no qubits have measured
    qc_qlazy_tmp = qc_qlazy.clone()
    while True:
        kind = qc_qlazy_tmp.kind_first()
        if kind is None:
            break

        (kind, qid, para, c, ctrl) = qc_qlazy_tmp.pop_gate()

        # qid[0]th-qubit has measured and store c-th classical register
        if kind in (cfg.MEASURE, cfg.RESET):
            measured_info[qid[0]] = c
        # not allowed operating unitary gate on measured qubit (aws braket limitation?)
        elif measured_info[qid[0]] != -1  or measured_info[qid[1]] != -1:
            raise ValueError("not allowed operating unitary gate on measured qubit.")
        elif ctrl is not None:
            raise ValueError("not allowed operating unitary gate on measured qubit.")
        # ex) mesure(qid=[0,1,2], cid=[2,1,0]) -> measured_flg = [2, 1, 0, -1, -1,...]

    # qlazy gate -> aws gate
    qc_aws = Circuit()
    qc_qlazy_tmp = qc_qlazy.clone()
    while True:
        kind = qc_qlazy_tmp.kind_first()
        if kind is None:
            break

        (kind, qid, para, c, ctrl) = qc_qlazy_tmp.pop_gate()

        if kind in (cfg.MEASURE, cfg.RESET):
            continue

        angle = para[0] * np.pi
        q0, q1 = qid[0], qid[1]
        __aws_add_qgate(qc_aws, kind, q0, q1, angle)

    return qc_aws, measured_info

def run_braket_sv(qcirc=None, shots=1, cid=None, backend=None):
    """ run the quantum circuit on braket_sv """

    if qcirc is None:
        raise ValueError("quantum circuit must be specified.")

    qubit_num = qcirc.qubit_num
    cmem_num = qcirc.cmem_num

    if cid is None:
        cid = list(range(cmem_num))

    if cmem_num < len(cid):
        raise ValueError("length of cid must be less than classical resister size of qcirc")

    qc, measured_info = __convert_to_aws_circuit(qcirc)

    device = LocalSimulator(backend="braket_sv")
    task = device.run(qc, shots=shots)
    result = task.result()
    frequency_org = result.measurement_counts

    # redefine the measured info
    # ex) mesure(qid=[0,1,2], cid=[2,1,0]) -> measured_info = [2, 1, 0, -1, -1,...]
    #     cid = [1,2] -> measured_info = [1, 0, -1, -1,...]
    #     cid = [2,0] -> measured_info = [0, -1, 1, -1, -1,...]
    #     cid = None -> cid = [0,1,2,...] -> measured_info = [2, 1, 0, -1, -1,...]
    for i, m in enumerate(measured_info):
        if m == -1:
            continue

        if m in cid:
            measured_info[i] = cid.index(m)
        else:
            measured_info[i] = -1

    # marginal frequency
    if set(measured_info) == {-1}:  # no qubits is measured
        frequency = None
    else:
        frequency = Counter()
        for mstr, freq in frequency_org.items():
            mlist = list(mstr)
            mlist_new = [-1] * len(cid)
            for i, m in enumerate(measured_info):
                mlist_new[m] = mlist[i]
            mstr_new = "".join(mlist_new)
            frequency[mstr_new] += freq

    info = {'response':result}

    result = Result()
    result.backend = backend
    result.qubit_num = qubit_num
    result.cmem_num = cmem_num
    result.cid = cid
    result.shots = shots
    result.frequency = frequency
    result.info = info

    return result
