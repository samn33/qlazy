# -*- coding: utf-8 -*-
from collections import Counter

from qlazy.error import *
from qlazy.config import *
from qlazy.util import *
from qlazy.QState import *
from qlazy.Result import *
from qlazy.lib.qstate_c import *

def run(qcirc=None, shots=1, cid=[], backend=None):

    if qcirc is None:
        raise ValueError("quantum circuit must be specified.")
    
    qubit_num = qcirc.qubit_num
    cmem_num = qcirc.cmem_num
    qstate = QState(qubit_num=qubit_num)
    if cmem_num > 0:
        cmem = CMem(cmem_num)
    else:
        cmem = None

    if cmem_num < len(cid):
        raise ValueError("length of cid must be less than classical resister size of qcirc")

    if cid == []:
        cid = [i for i in range(cmem_num)]

    qcirc_unitary, qcirc_non_unitary = qcirc.split_unitary_non_unitary()

    frequency = qstate_operate_qcirc(qstate, cmem, qcirc_unitary, 1, cid)
    frequency = qstate_operate_qcirc(qstate, cmem, qcirc_non_unitary, shots, cid)

    info = {'qstate': qstate, 'cmem': cmem}

    result = Result(cid=cid, frequency=frequency, backend=backend, info=info)

    return result
