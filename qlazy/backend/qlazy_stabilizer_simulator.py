# -*- coding: utf-8 -*-
from collections import Counter

from qlazy.error import *
from qlazy.config import *
from qlazy.util import *
from qlazy.Stabilizer import *
from qlazy.lib.stabilizer_c import *

def init(qubit_num=0, backend=None):

    qstate = Stabilizer(qubit_num)
    qstate.set_all('Z')
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
            # if c['kind'] == MEASURE:
            if c['kind'] == MEASURE and len(qcirc) > 1:
                mval_list = []
                for q in c['qid']:
                    mval = stabilizer_measure(qstate, q=q)
                    mval_list.append(mval)
                mval_list_str = "".join(map(str, mval_list))
                f = Counter([mval_list_str])

                if c['cid'] != None:
                    for k,mval in enumerate(mval_list):
                        cmem[c['cid'][k]] = mval
                        
                if end_of_measurements == i:
                        freq += f
            # else:
            elif c['kind'] != MEASURE:
                if c['ctrl'] == None or cmem[c['ctrl']] == 1:
                    if len(c['qid']) == 1:
                        q0 = c['qid'][0]
                        q1 = 0
                    elif len(c['qid']) == 2:
                        q0 = c['qid'][0]
                        q1 = c['qid'][1]
                    else:
                        raise ValueError
                            
                    stabilizer_operate_qgate(qstate, kind=c['kind'], q0=q0, q1=q1)

            # qcirc have only one measurement at the end
            # if only_one_measurement_end == True and i == len(qcirc) - 2:
            if only_one_measurement_end == True and (i == len(qcirc) - 2 or i == len(qcirc) - 1):
                for i in range(shots):
                    if i < shots-1:
                        qstate_tmp = qstate.clone()
                    else:
                        qstate_tmp = qstate
                        
                    mval_list = []
                    for q in qcirc[-1]['qid']:
                        mval = stabilizer_measure(qstate_tmp, q=q)
                        mval_list.append(mval)
                    mval_list_str = "".join(map(str, mval_list))
                    freq += Counter([mval_list_str])

                    if qcirc[-1]['cid'] != None:
                        for k,mval in enumerate(mval_list):
                            cmem[qcirc[-1]['cid'][k]] = mval

                    if i < shots-1:
                        qstate_tmp.free()
                break
            
        if only_one_measurement_end == True:
            break

        # reset classical memory and qubits, if not end of the shots
        if cnt < shots-1:
            cmem = [0] * len(cmem)
            qstate.set_all('Z')

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
        qstate.set_all('Z')

    # return True

def free(qstate=None, backend=None):

    if qstate != None:
        qstate.free()
