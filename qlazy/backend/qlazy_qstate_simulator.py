# -*- coding: utf-8 -*-
""" run function for qlazy's qstate simulator """

from qlazy.QState import QState
from qlazy.QCirc import QCirc
from qlazy.CMem import CMem
from qlazy.Result import Result
from qlazy.lib.qstate_c import qstate_operate_qcirc

def run_cpu(qcirc=None, shots=1, cid=None, backend=None):
    """ run the quantum circuit (with CPU) """

    return __run_all(qcirc=qcirc, shots=shots, cid=cid, backend=backend, use_gpu=False)

def run_gpu(qcirc=None, shots=1, cid=None, backend=None):
    """ run the quantum circuit (with GPU) """

    return __run_all(qcirc=qcirc, shots=shots, cid=cid, backend=backend, use_gpu=True)

def __run_all(qcirc=None, shots=1, cid=None, backend=None, use_gpu=False):
    """ run the quantum circuit """

    if qcirc is None:
        raise ValueError("quantum circuit must be specified.")

    qubit_num = qcirc.qubit_num
    cmem_num = qcirc.cmem_num

    if cmem_num > 0:
        cmem = CMem(cmem_num)
    else:
        cmem = None

    if cid is None:
        cid = list(range(cmem_num))

    if cmem_num < len(cid):
        raise ValueError("length of cid must be less than classical resister size of qcirc")

    # qcirc_unitary, qcirc_non_unitary = qcirc.split_unitary_non_unitary()

    qstate = QState(qubit_num=qubit_num, use_gpu=use_gpu)

    frequency = qstate_operate_qcirc(qstate, cmem, qcirc, shots, cid)

    # frequency = qstate_operate_qcirc(qstate, cmem, qcirc_unitary, 1, cid)
    # if qcirc_non_unitary.kind_first() is not None:
    #     frequency = qstate_operate_qcirc(qstate, cmem, qcirc_non_unitary, shots, cid)

    info = {'qstate': qstate, 'cmem': cmem}

    result = Result()
    result.backend = backend
    result.qubit_num = qubit_num
    result.cmem_num = cmem_num
    result.cid = cid
    result.shots = shots
    result.frequency = frequency
    result.info = info

    return result
