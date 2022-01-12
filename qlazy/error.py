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

# MData

class MData_Error_GetFrq(Exception):
    def __str__(self):
        return "MData: fail to get frq"

class MData_Error_Show(Exception):
    def __str__(self):
        return "MData: fail to show"

class MData_Error_GetMeasuredData(Exception):
    def __str__(self):
        return "MData: fail to get measured data (probably not measured yet)"

# Observable

class Observable_Error_Initialize(Exception):
    def __str__(self):
        return "Observable: fail to initialize"

# DensOp

class DensOp_Error_Initialize(Exception):
    def __str__(self):
        return "DensOp: fail to initialize"

class DensOp_Error_Show(Exception):
    def __str__(self):
        return "DensOp: fail to show"

class DensOp_Error_Clone(Exception):
    def __str__(self):
        return "DensOp: fail to clone"

class DensOp_Error_Add(Exception):
    def __str__(self):
        return "DensOp: fail to add"

class DensOp_Error_Mul(Exception):
    def __str__(self):
        return "DensOp: fail to mul"

class DensOp_Error_GetElm(Exception):
    def __str__(self):
        return "DensOp: fail to get_elm"

class DensOp_Error_Trace(Exception):
    def __str__(self):
        return "DensOp: fail to trace"

class DensOp_Error_SqTrace(Exception):
    def __str__(self):
        return "DensOp: fail to square trace"

class DensOp_Error_PaTrace(Exception):
    def __str__(self):
        return "DensOp: fail to partial trace"

class DensOp_Error_Apply(Exception):
    def __str__(self):
        return "DensOp: fail to apply"

class DensOp_Error_Probability(Exception):
    def __str__(self):
        return "DensOp: fail to probability"

class DensOp_Error_Instrument(Exception):
    def __str__(self):
        return "DensOp: fail to instrument"

class DensOp_Error_Fidelity(Exception):
    def __str__(self):
        return "DensOp: fail to get fidelity"

class DensOp_Error_Distance(Exception):
    def __str__(self):
        return "DensOp: fail to get distance"

class DensOp_Error_Spectrum(Exception):
    def __str__(self):
        return "DensOp: fail to get spectrum"

class DensOp_Error_Entropy(Exception):
    def __str__(self):
        return "DensOp: fail to get entropy"

class DensOp_Error_OperateQGate(Exception):
    def __str__(self):
        return "DensOp: fail to operate qgate"

class DensOp_Error_TensorProduct(Exception):
    def __str__(self):
        return "DensOp: fail to tensor product"
    
class DensOp_Error_Reset(Exception):
    def __str__(self):
        return "DensOp: fail to reset"
    
class DensOp_Error_FreeAll(Exception):
    def __str__(self):
        return "DensOp: fail to free all"

class DensOp_Error_AddMethods(Exception):
    def __str__(self):
        return "DensOp: fail to add methods"

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

# # QComp
# 
# class QComp_Error_QgateNotSupported(Exception):
#     def __str__(self):
#         return "QComp: qgate is not supported"
# 
# class QComp_Error_BackendNotSupported(Exception):
#     def __str__(self):
#         return "QComp: backend is not supported"
# 
# class QComp_Error_NumberOfClassicalReg(Exception):
#     def __str__(self):
#         return "QComp: number of classical register must be equal to corresponding quantum register"
# 
# class QComp_Error_FreeAll(Exception):
#     def __str__(self):
#         return "QComp: fail to free all"
    
# Backend

class Backend_Error_NameNotSupported(Exception):
    def __str__(self):
        return "Backend: name is not supported"

class Backend_Error_DeviceNotSupported(Exception):
    def __str__(self):
        return "Backend: device is not supported"

class Backend_Error_NameNotSpecified(Exception):
    def __str__(self):
        return "Backend: name is not specified"

# QCirc

class QCirc_Error_Initialize(Exception):
    def __str__(self):
        return "QCirc: fail to initialize"

class QCirc_Error_Copy(Exception):
    def __str__(self):
        return "QCirc: fail to copy"

class QCirc_Error_Merge(Exception):
    def __str__(self):
        return "QCirc: fail to merge"

class QCirc_Error_AppendGate(Exception):
    def __str__(self):
        return "QCirc: fail to append gate"

class QCirc_Error_KindFirst(Exception):
    def __str__(self):
        return "QCirc: fail to kind first"

class QCirc_Error_PopGate(Exception):
    def __str__(self):
        return "QCirc: fail to pop gate"

# CMem

class CMem_Error_Initialize(Exception):
    def __str__(self):
        return "CMem: fail to initialize"

class CMem_Error_Clone(Exception):
    def __str__(self):
        return "CMem: fail to clone"

