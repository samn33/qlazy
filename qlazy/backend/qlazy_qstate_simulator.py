# -*- coding: utf-8 -*-
from collections import Counter

from qlazy.error import *
from qlazy.config import *
from qlazy.util import *
from qlazy.QState import *
from qlazy.lib.qstate_c import *

def init(qubit_num=0, backend=None):

    qstate = QState(qubit_num)
    return qstate

def run(qubit_num=0, cmem_num=0, qstate=None, qcirc=[], cmem=[], shots=1, backend=None):

    # number of measurement (measurement_cnt)
    # and its position of last measurement (end_of_measurements)
    measurement_cnt = 0
    end_of_measurements = -1
    for j, c in enumerate(qcirc):
        if c['kind'] == MEASURE:
            measurement_cnt += 1
            end_of_measurements = j

    # qcirc have only one measurement at the end, or not
    if measurement_cnt == 1 and end_of_measurements == len(qcirc) - 1:
        only_one_measurement_end = True
    else:
        only_one_measurement_end = False

    # run the quantum circuit
    freq = Counter()
    for cnt in range(shots):
        for i, c in enumerate(qcirc):
            
            if c['kind'] == MEASURE:
                md = qstate_measure(qstate, {}, qid=c['qid'], shots=1, angle=0.0, phase=0.0, tag=None)

                if c['cid'] != None:
                    for k,mval in enumerate(list(md.last)):
                        cmem[c['cid'][k]] = int(mval)
                        
                if end_of_measurements == i:
                    freq += md.frequency

            else:
                if c['ctrl'] == None or cmem[c['ctrl']] == 1:
                    qstate_operate_qgate(qstate, kind=c['kind'], qid=c['qid'],
                                         phase=c['phase'], phase1=c['phase1'], phase2=c['phase2'])

            # qcirc have only one measurement
            if only_one_measurement_end == True and i == len(qcirc) - 2:
                md = qstate_measure(qstate, {}, qid=qcirc[-1]['qid'], shots=shots, angle=0.0, phase=0.0, tag=None)
                freq = md.frequency
                
                if qcirc[-1]['cid'] != None:
                    for k,mval in enumerate(list(md.last)):
                        cmem[qcirc[-1]['cid'][k]] = int(mval)
                break

        if only_one_measurement_end == True and i == len(qcirc) - 2:
            break
            
        # reset classical memory and qubits, if not end of the shots
        if cnt < shots-1:
            cmem = [0] * len(cmem)
            qstate.reset()

    # if end_of_measurements > 0:
    if measurement_cnt > 0:
        measured_qid = qcirc[end_of_measurements]['qid']
        result = {'measured_qid': measured_qid, 'frequency': freq}
    else:
        result = None
        
    return result

def reset(qstate=None, backend=None):

    if qstate != None:
        qstate.reset()

    # return True

def free(qstate=None, backend=None):

    if qstate != None:
        qstate.free()

