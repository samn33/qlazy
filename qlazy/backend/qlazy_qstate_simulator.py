# -*- coding: utf-8 -*-
""" run function for qlazy's qstate simulator """

from qlazy.QState import QState
from qlazy.CMem import CMem
from qlazy.Result import Result
from qlazy.lib.qstate_c import qstate_operate_qcirc

def run(qcirc=None, shots=1, cid=None, backend=None):
    """ run the quantum circuit """

    if qcirc is None:
        raise ValueError("quantum circuit must be specified.")

    qubit_num = qcirc.qubit_num
    cmem_num = qcirc.cmem_num
    qstate = QState(qubit_num=qubit_num)
    if cmem_num > 0:
        cmem = CMem(cmem_num)
    else:
        cmem = None

    if cid is None:
        cid = list(range(cmem_num))

    if cmem_num < len(cid):
        raise ValueError("length of cid must be less than classical resister size of qcirc")

    qcirc_unitary, qcirc_non_unitary = qcirc.split_unitary_non_unitary()

    frequency = qstate_operate_qcirc(qstate, cmem, qcirc_unitary, 1, cid)
    frequency = qstate_operate_qcirc(qstate, cmem, qcirc_non_unitary, shots, cid)

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
