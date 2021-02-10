# -*- coding: utf-8 -*-
from collections import Counter

from qlazypy.error import *
from qlazypy.config import *
from qlazypy.lib.qstate_c import *
from qlazypy.lib.stabilizer_c import *

def run_qlazy_qstate_simulator(qstate, qcirc, cmem, shots=DEF_SHOTS):

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

def run_qlazy_stabilizer_simulator(stab, qcirc, cmem, shots=DEF_SHOTS):

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
                    mval = stabilizer_measure(stab, q=q)
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
                        raise ValuError
                            
                    stabilizer_operate_qgate(stab, kind=c['kind'], q0=q0, q1=q1)

            # qcirc have only one measurement at the end
            # if only_one_measurement_end == True and i == len(qcirc) - 2:
            if only_one_measurement_end == True and (i == len(qcirc) - 2 or i == len(qcirc) - 1):
                for i in range(shots):
                    if i < shots-1:
                        stab_tmp = stab.clone()
                    else:
                        stab_tmp = stab
                        
                    mval_list = []
                    for q in qcirc[-1]['qid']:
                        mval = stabilizer_measure(stab_tmp, q=q)
                        mval_list.append(mval)
                    mval_list_str = "".join(map(str, mval_list))
                    freq += Counter([mval_list_str])

                    if qcirc[-1]['cid'] != None:
                        for k,mval in enumerate(mval_list):
                            cmem[qcirc[-1]['cid'][k]] = mval

                    if i < shots-1:
                        stab_tmp.free()
                break
            
        if only_one_measurement_end == True:
            break

        # reset classical memory and qubits, if not end of the shots
        if cnt < shots-1:
            cmem = [0] * len(cmem)
            stab.set_all('Z')

    # if end_of_measurements > 0:
    if measurement_cnt > 0:
        measured_qid = qcirc[end_of_measurements]['qid']
        result = {'measured_qid': measured_qid, 'frequency': freq}
    else:
        result = None
        
    return result
