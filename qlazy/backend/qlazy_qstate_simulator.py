# -*- coding: utf-8 -*-
from collections import Counter

from qlazy.error import *
from qlazy.config import *
from qlazy.util import *
from qlazy.QState import *
from qlazy.Result import *
from qlazy.lib.qstate_c import *

import sys

def init(qubit_num=0, backend=None):

    qstate = QState(qubit_num)
    return qstate

def run(qubit_num=0, cmem_num=0, qstate=None, qcirc=[], cmem=[], shots=1, cid=[], backend=None):

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

    frequency = qstate_operate_qcirc(qstate, cmem, qcc, shots, cid)

    if frequency is not None:
        result = Result(cid=cid, frequency=frequency)
    else:
        result = None
        
    return result
    
def clear(qstate=None, backend=None):

    if qstate != None:
        qstate.reset()

def free(qstate=None, backend=None):

    if qstate != None:
        del qstate
