# -*- coding: utf-8 -*-

# QState

class QState_Error_Initialize(Exception):
    def __str__(self):
        return "QState: fail to initialize"

class QState_Error_GetCmp(Exception):
    def __str__(self):
        return "QState: fail to get cmp"

class QState_Error_Show(Exception):
    def __str__(self):
        return "QState: fail to show"

class QState_Error_Clone(Exception):
    def __str__(self):
        return "QState: fail to clone"

class QState_Error_InnerProduct(Exception):
    def __str__(self):
        return "QState: fail to inner product"

class QState_Error_TensorProduct(Exception):
    def __str__(self):
        return "QState: fail to tensor product"

class QState_OutOfBound(Exception):
    def __str__(self):
        return "QState: out of bound"

class QState_TooManyArguments(Exception):
    def __str__(self):
        return "QState: too many arguments"

class QState_NeedMoreArguments(Exception):
    def __str__(self):
        return "QState: need more arguments"

class QState_SameQubitID(Exception):
    def __str__(self):
        return "QState: same qubit id"
    
class QState_UnknownQgateKind(Exception):
    def __str__(self):
        return "QState: unknown qgate kind"

class QState_Error_OperateQgate(Exception):
    def __str__(self):
        return "QState: fail to operate qgate"

class QState_Error_Evolve(Exception):
    def __str__(self):
        return "QState: fail to evolve"

class QState_Error_Expect(Exception):
    def __str__(self):
        return "QState: fail to expect"

class QState_Error_Apply(Exception):
    def __str__(self):
        return "QState: fail to apply"

class QState_Error_Bloch(Exception):
    def __str__(self):
        return "QState: fail to bloch"

class QState_Error_Reset(Exception):
    def __str__(self):
        return "QState: fail to reset"

class QState_Error_FreeAll(Exception):
    def __str__(self):
        return "QState: fail to free all"

class QState_Error_AddMethods(Exception):
    def __str__(self):
        return "QState: fail to add methods"

class QState_Error_OperateQcirc(Exception):
    def __str__(self):
        return "QState: fail to operate qcirc"

# Stabilizer

class Stabilizer_Error_Initialize(Exception):
    def __str__(self):
        return "Stabilizer: fail to initialize"

class Stabilizer_Error_Clone(Exception):
    def __str__(self):
        return "Stabilizer: fail to clone"

class Stabilizer_Error_AddMethos(Exception):
    def __str__(self):
        return "Stabilizer: fail to add methods"

class Stabilizer_Error_SetPauliFac(Exception):
    def __str__(self):
        return "Stabilizer: fail to set pauli factor."

class Stabilizer_Error_GetPauliFac(Exception):
    def __str__(self):
        return "Stabilizer: fail to get pauli factor."

class Stabilizer_Error_SetPauliOp(Exception):
    def __str__(self):
        return "Stabilizer: fail to set pauli op."

class Stabilizer_Error_GetPauliOp(Exception):
    def __str__(self):
        return "Stabilizer: fail to get pauli op."

class Stabilizer_Error_GetRank(Exception):
    def __str__(self):
        return "Stabilizer: fail to get rank."

class Stabilizer_Error_OperateQgate(Exception):
    def __str__(self):
        return "Stabilizer: fail to operate qgate."

class Stabilizer_Error_GetRank(Exception):
    def __str__(self):
        return "Stabilizer: fail to get rank."

class Stabilizer_Error_Measure(Exception):
    def __str__(self):
        return "Stabilizer: fail to measure qubits."

class Stabilizer_Error_FreeAll(Exception):
    def __str__(self):
        return "Stabilizer: fail to free all"

class Stabilizer_Error_OperateQcirc(Exception):
    def __str__(self):
        return "Stabilizer: fail to operate qcirc"
