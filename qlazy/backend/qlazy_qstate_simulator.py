# -*- coding: utf-8 -*-
from collections import Counter

from qlazy.error import *
from qlazy.config import *
from qlazy.util import *
from qlazy.QState import *
from qlazy.Result import *
from qlazy.lib.qstate_c import *

def run(qcirc=[], shots=1, cid=[], backend=None):

    qcc = QCirc()
    for i, gate in enumerate(qcirc):
        kind = gate['kind']
        qids = gate['qid']
        cids = gate['cid']
        phase = gate['phase']
        phase1 = gate['phase1']
        phase2 = gate['phase2']
        ctrl = gate['ctrl']
        para = [phase, phase1, phase2]
        if is_measurement_gate(kind) == True:
            for i, q in enumerate(qids):
                qids = [q]
                if cids is not None:
                    c = cids[i]
                else:
                    c = None
                qcc.append_gate(kind, qids, para, c, ctrl)
        elif is_reset_gate(kind) == True:
            for q in qids:
                qids = [q]
                c = None
                qcc.append_gate(kind, qids, para, c, ctrl)
        else:
            c = None
            qcc.append_gate(kind, qids, para, c, ctrl)

    qubit_num = qcc.qubit_num
    cmem_num = qcc.cmem_num
    qstate = QState(qubit_num=qubit_num)
    cmem = [0] * cmem_num

    if cmem_num < len(cid):
        raise ValueError("length of cid must be less than classical resister size of qcirc")

    if cid == []:
        cid = [i for i in range(cmem_num)]

    frequency = qstate_operate_qcirc(qstate, cmem, qcc, shots, cid)

    info = {'qstate': qstate, 'cmem': cmem}

    result = Result(cid=cid, frequency=frequency, backend=backend, info=info)

    return result
