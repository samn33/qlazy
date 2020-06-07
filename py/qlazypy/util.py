# -*- coding: utf-8 -*-
import math
from qlazypy.error import *
from qlazypy.config import *

def get_lib_ext():
    
    import platform
    if platform.system() == 'Darwin':
        return 'dylib'
    else:
        return 'so'

def qstate_check_args(qs, kind=None, qid=None, shots=None, angle=None,
                      phase=None, phase1=None, phase2=None):
    
    for q in qid:
        if (q >= qs.qubit_num) or (q < 0):
            raise QState_OutOfBound()
            
    qnum = get_qgate_qubit_num(kind)
    
    if qnum == 0:  # any qubit number
        # check qubit number
        if len(qid) > qs.qubit_num:
            raise QState_TooManyArguments()
        elif len(qid) < 1:
            raise QState_NeedMoreArguments()
        else:
            pass
            
        # check same qubit number
        if len(set(qid)) != len(qid):
            raise QState_SameQubitID()
            
    elif qnum == 1:
        # check qubit number
        if len(qid) > qnum:
            raise QState_TooManyArguments()
        elif len(qid) < qnum:
            raise QState_NeedMoreArguments()
        else:
            return True
            
    elif qnum == 2:
        # check qubit number
        if len(qid) > qnum:
            raise QState_TooManyArguments()
        elif len(qid) < qnum:
            raise QState_NeedMoreArguments()
        else:
            pass
    
        # check same qubit number
        if (qid[0]==qid[1]):
            raise QState_SameQubitID()
        else:
            return True
            
    elif qnum == 3:
        # check qubit number
        if len(qid) > qnum:
            raise QState_TooManyArguments()
        elif len(qid) < qnum:
            raise QState_NeedMoreArguments()
        else:
            pass
    
        # check same qubit id
        if (qid[0]==qid[1] or qid[1]==qid[2] or qid[2]==qid[0]):
            raise QState_SameQubitID()
        else:
            return True
    
def densop_check_args(de, kind=None, qid=None, shots=None, angle=None,
                      phase=None, phase1=None, phase2=None):

    qubit_num = int(math.log2(de.row))
        
    for q in qid:
        if (q >= qubit_num) or (q < 0):
            raise QState_OutOfBound()
            
    qnum = get_qgate_qubit_num(kind)

    if qnum == 0:  # any qubit number
        # check qubit number
        if len(qid) > qubit_num:
            raise QState_TooManyArguments()
        elif len(qid) < 1:
            raise QState_NeedMoreArguments()
        else:
            pass
            
        # check same qubit number
        if len(set(qid)) != len(qid):
            raise QState_SameQubitID()
            
    elif qnum == 1:
            # check qubit number
        if len(qid) > qnum:
            raise QState_TooManyArguments()
        elif len(qid) < qnum:
            raise QState_NeedMoreArguments()
        else:
            return True
            
    elif qnum == 2:
        # check qubit number
        if len(qid) > qnum:
            raise QState_TooManyArguments()
        elif len(qid) < qnum:
            raise QState_NeedMoreArguments()
        else:
            pass

        # check same qubit number
        if (qid[0]==qid[1]):
            raise QState_SameQubitID()
        else:
            return True
            
    elif qnum == 3:
        # check qubit number
        if len(qid) > qnum:
            raise QState_TooManyArguments()
        elif len(qid) < qnum:
            raise QState_NeedMoreArguments()
        else:
            pass

        # check same qubit id
        if (qid[0]==qid[1] or qid[1]==qid[2] or qid[2]==qid[0]):
            raise QState_SameQubitID()
        else:
            return True

def get_qgate_qubit_num(kind=None):

    if (kind==SHOW or kind==MEASURE or
        kind==MEASURE_X or kind==MEASURE_Y or kind==MEASURE_Z):  # 0 if any number
        return 0
    elif (kind==BLOCH or kind==PAULI_X or kind==PAULI_Y or kind==PAULI_Z or
          kind==ROOT_PAULI_X or kind==ROOT_PAULI_X_ or kind==HADAMARD or
          kind==PHASE_SHIFT_S or kind==PHASE_SHIFT_S_ or
          kind==PHASE_SHIFT_T or kind==PHASE_SHIFT_T_ or kind==PHASE_SHIFT or
          kind==ROTATION_X or kind==ROTATION_Y or kind==ROTATION_Z or
          kind==ROTATION_U1 or kind==ROTATION_U2 or kind==ROTATION_U3):
        return 1
    elif (kind==CONTROLLED_X or kind==CONTROLLED_Y or kind==CONTROLLED_Z or
          kind==CONTROLLED_XR or kind==CONTROLLED_XR_ or kind==CONTROLLED_H or
          kind==CONTROLLED_S or kind==CONTROLLED_S_ or kind==CONTROLLED_T or
          kind==CONTROLLED_T_ or kind==SWAP or kind==CONTROLLED_P or
          kind==CONTROLLED_RX or kind==CONTROLLED_RY or kind==CONTROLLED_RZ or
          kind==CONTROLLED_U1 or kind==CONTROLLED_U2 or kind==CONTROLLED_U3 or
          kind==MEASURE_BELL):
        return 2
    else:
        raise QState_UnknownQgateKind()
