# -*- coding: utf-8 -*-
""" run function for AWS """
from collections import Counter
import numpy as np

from braket.aws import AwsDevice
from braket.devices import LocalSimulator
from braket.circuits import Circuit

import qlazy.config as cfg
from qlazy.Result import Result

def __braket_add_qgate(qc_braket, kind, q0, q1, angle, product):
    """ add gate to braket circuit """

    # 1-qubit, 0-parameter gate
    if kind == cfg.PAULI_X:
        qc_braket.x(q0)

    elif kind == cfg.PAULI_Z:
        qc_braket.z(q0)

    elif kind == cfg.HADAMARD:
        qc_braket.h(q0)

    elif kind == cfg.PHASE_SHIFT_S:
        qc_braket.s(q0)

    elif kind == cfg.PHASE_SHIFT_S_:
        qc_braket.si(q0)

    elif kind == cfg.PHASE_SHIFT_T:
        qc_braket.t(q0)

    elif kind == cfg.PHASE_SHIFT_T_:
        qc_braket.ti(q0)

    # 1-qubit, 1-parameter gate
    elif kind == cfg.ROTATION_X:
        qc_braket.rx(q0, angle=angle)

    elif kind == cfg.ROTATION_Z:
        qc_braket.rz(q0, angle=angle)

    # 2-qubit, 0-parameters gate
    elif kind == cfg.CONTROLLED_X:
        qc_braket.cnot(q0, q1)

    elif kind == cfg.CONTROLLED_Z:
        if product == 'braket_ionq':
            qc_braket.h(q1).cnot(q0, q1).h(q1)
        else:
            qc_braket.cz(q0, q1)

    elif kind == cfg.CONTROLLED_H:
        pi_2 = 0.5 * np.pi
        pi_4 = 0.25 * np.pi
        qc_braket.ry(1, angle=-pi_4).cnot(0, 1).rz(1, angle=-pi_2)
        qc_braket.cnot(0, 1).rz(1, angle=pi_2).ry(1, angle=pi_4)
        if product == 'braket_ionq':
            qc_braket.rz(0, angle=pi_2)
        else:
            qc_braket.phaseshift(0, angle=pi_2)

    # 2-qubit, 1-parameters gate
    elif kind == cfg.CONTROLLED_RZ:
        qc_braket.rz(q1, angle=angle/2).cnot(q0, q1).rz(q1, angle=-angle/2).cnot(q0, q1)

    else:
        raise ValueError("unknown gate")

def __convert_to_braket_circuit(qc_qlazy, product):
    """ convert qlazy circuit to braket circuit """

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
        # not allowed operating unitary gate on measured qubit (braket limitation?)
        elif measured_info[qid[0]] != -1  or measured_info[qid[1]] != -1:
            raise ValueError("not allowed operating unitary gate on measured qubit.")
        elif ctrl is not None:
            raise ValueError("not allowed operating unitary gate on measured qubit.")
        # ex) mesure(qid=[0,1,2], cid=[2,1,0]) -> measured_flg = [2, 1, 0, -1, -1,...]

    # qlazy gate -> braket gate
    qc_braket = Circuit()
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
        __braket_add_qgate(qc_braket, kind, q0, q1, angle, product)

    return qc_braket, measured_info

def run(qcirc=None, shots=1, cid=None, backend=None, out_state=False):
    """ run the quantum circuit on braket_sv """

    if qcirc is None:
        raise ValueError("quantum circuit must be specified.")

    qubit_num = qcirc.qubit_num
    cmem_num = qcirc.cmem_num

    qc, measured_info = __convert_to_braket_circuit(qcirc, backend.product)

    if backend.product == 'braket_local':
        if backend.device == 'braket_sv':
            device = LocalSimulator(backend="braket_sv")
        else:
            raise ValueError("device:'{}' is unknown for product:'{}'."
                             .format(backend.device, backend.product))
        task = device.run(qc, shots=shots)

    elif backend.product == 'braket_aws':
        if backend.device == 'sv1':
            device = AwsDevice("arn:aws:braket:::device/quantum-simulator/amazon/sv1")
            s3_folder = (backend.config_braket['backet_name'], "sv1")
        elif backend.device == 'tn1':
            device = AwsDevice("arn:aws:braket:::device/quantum-simulator/amazon/tn1")
            s3_folder = (backend.config_braket['backet_name'], "tn1")
        elif backend.device == 'dm1':
            device = AwsDevice("arn:aws:braket:::device/quantum-simulator/amazon/dm1")
            s3_folder = (backend.config_braket['backet_name'], "dm1")
        else:
            raise ValueError("device:'{}' is unknown for product:'{}'."
                             .format(backend.device, backend.product))

        if backend.config_braket['poll_timeout_seconds'] is None:
            task = device.run(qc, s3_folder, shots=shots)
        else:
            task = device.run(qc, s3_folder, shots=shots,
                              poll_timeout_seconds=backend.config_braket['poll_timeout_seconds'])

    elif backend.product == 'braket_ionq':
        if backend.device == 'ionq':
            device = AwsDevice("arn:aws:braket:::device/qpu/ionq/ionQdevice")
            s3_folder = (backend.config_braket['backet_name'], "ionq")
        else:
            raise ValueError("device:'{}' is unknown for product:'{}'."
                             .format(backend.device, backend.product))

        if backend.config_braket['poll_timeout_seconds'] is None:
            task = device.run(qc, s3_folder, shots=shots)
        else:
            task = device.run(qc, s3_folder, shots=shots,
                              poll_timeout_seconds=backend.config_braket['poll_timeout_seconds'])

    elif backend.product == 'braket_rigetti':
        if backend.device == 'aspen_11':
            device = AwsDevice("arn:aws:braket:::device/qpu/rigetti/Aspen-11")
            s3_folder = (backend.config_braket['backet_name'], "aspen_11")
        elif backend.device == 'aspen_m_1':
            device = AwsDevice("arn:aws:braket:us-west-1::device/qpu/rigetti/Aspen-M-1")
            s3_folder = (backend.config_braket['backet_name'], "aspen_m_1")
        else:
            raise ValueError("device:'{}' is unknown for product:'{}'."
                             .format(backend.device, backend.product))

        if backend.config_braket['poll_timeout_seconds'] is None:
            task = device.run(qc, s3_folder, shots=shots)
        else:
            task = device.run(qc, s3_folder, shots=shots,
                              poll_timeout_seconds=backend.config_braket['poll_timeout_seconds'])

    elif backend.product == 'braket_oqc':
        if backend.device == 'lucy':
            device = AwsDevice("arn:aws:braket:eu-west-2::device/qpu/oqc/Lucy")
            s3_folder = (backend.config_braket['backet_name'], "lucy")
        else:
            raise ValueError("device:'{}' is unknown for product:'{}'."
                             .format(backend.device, backend.product))

        if backend.config_braket['poll_timeout_seconds'] is None:
            task = device.run(qc, s3_folder, shots=shots)
        else:
            task = device.run(qc, s3_folder, shots=shots,
                              poll_timeout_seconds=backend.config_braket['poll_timeout_seconds'])

    result = task.result()
    frequency_org = result.measurement_counts

    # redefine the measured info
    # ex) mesure(qid=[0,1,2], cid=[2,1,0]) -> measured_info = [2, 1, 0, -1, -1,...]
    #     cid = [1,2] -> measured_info = [1, 0, -1, -1,...]
    #     cid = [2,0] -> measured_info = [0, -1, 1, -1, -1,...]
    #     cid = None -> cid = [0,1,2] -> measured_info = [2, 1, 0, -1, -1,...]

    if cid is None:
        cid = list(range(cmem_num))

    if cmem_num < len(cid):
        raise ValueError("length of cid must be less than classical resister size of qcirc")

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
            mlist_new = ['0'] * len(cid)
            for i, m in enumerate(measured_info):
                if m >= 0:
                    mlist_new[m] = mlist[i]
            mstr_new = "".join(mlist_new)
            frequency[mstr_new] += freq

    info = {'braket': result}

    result = Result()
    result.backend = backend
    result.qubit_num = qubit_num
    result.cmem_num = cmem_num
    result.cid = cid
    result.shots = shots
    result.frequency = frequency
    result.info = info

    return result
