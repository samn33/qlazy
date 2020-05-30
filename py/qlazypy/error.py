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
