# -*- coding: utf-8 -*-
""" run function for qlazy's qstate simulator """

from qlazy.QState import QState
from qlazy.QCirc import QCirc
from qlazy.CMem import CMem
from qlazy.Result import Result
from qlazy.lib.qstate_c import qstate_operate_qcirc

def run_cpu(qcirc=None, shots=1, cid=None, backend=None, out_state=False):
    """ run the quantum circuit (with CPU) """

    return __run_all(qcirc=qcirc, shots=shots, cid=cid, backend=backend, use_gpu=False,
                     out_state=out_state)

def run_gpu(qcirc=None, shots=1, cid=None, backend=None, out_state=False):
    """ run the quantum circuit (with GPU) """

    return __run_all(qcirc=qcirc, shots=shots, cid=cid, backend=backend, use_gpu=True,
                     out_state=out_state)

def __run_all(qcirc=None, shots=1, cid=None, backend=None, use_gpu=False, out_state=False):
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

    qstate = QState(qubit_num=qubit_num, use_gpu=use_gpu)

    frequency = qstate_operate_qcirc(qstate, cmem, qcirc, shots, cid, out_state)

    result = Result()
    result.backend = backend
    result.qubit_num = qubit_num
    result.cmem_num = cmem_num
    result.cid = cid
    result.shots = shots
    result.frequency = frequency
    if out_state is True:
        result.qstate = qstate
        result.cmem = cmem
    else:
        result.qstate = None
        result.cmem = None
    result.info = None

    return result
