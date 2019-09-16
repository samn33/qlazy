# -*- coding: utf-8 -*-

# QState

class QState_FailToInitialize(Exception):
    def __str__(self):
        return "QState: fail to initialize"

class QState_FailToGetCmp(Exception):
    def __str__(self):
        return "QState: fail to get cmp"

class QState_FailToShow(Exception):
    def __str__(self):
        return "QState: fail to show"

class QState_FailToClone(Exception):
    def __str__(self):
        return "QState: fail to clone"

class QState_FailToInnerProduct(Exception):
    def __str__(self):
        return "QState: fail to inner product"

class QState_FailToTensorProduct(Exception):
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

class QState_FailToOperateQgate(Exception):
    def __str__(self):
        return "QState: fail to operate qgate"

class QState_FailToEvolve(Exception):
    def __str__(self):
        return "QState: fail to evolve"

class QState_FailToExpect(Exception):
    def __str__(self):
        return "QState: fail to expect"

class QState_FailToApply(Exception):
    def __str__(self):
        return "QState: fail to apply"

class QState_FailToBloch(Exception):
    def __str__(self):
        return "QState: fail to bloch"

class QState_FailToOperate(Exception):
    def __str__(self):
        return "QState: fail to operate"

# MData

class MData_FailToGetFrq(Exception):
    def __str__(self):
        return "MData: fail to get frq"

class MData_FailToShow(Exception):
    def __str__(self):
        return "MData: fail to show"

# Observable

class Observable_FailToInitialize(Exception):
    def __str__(self):
        return "Observable: fail to initialize"

# DensOp

class DensOp_FailToInitialize(Exception):
    def __str__(self):
        return "DensOp: fail to initialize"

class DensOp_FailToShow(Exception):
    def __str__(self):
        return "DensOp: fail to show"

class DensOp_FailToClone(Exception):
    def __str__(self):
        return "DensOp: fail to clone"

class DensOp_FailToGetElm(Exception):
    def __str__(self):
        return "DensOp: fail to get_elm"

class DensOp_FailToTrace(Exception):
    def __str__(self):
        return "DensOp: fail to trace"

class DensOp_FailToSqTrace(Exception):
    def __str__(self):
        return "DensOp: fail to square trace"

class DensOp_FailToPaTrace(Exception):
    def __str__(self):
        return "DensOp: fail to partial trace"

class DensOp_FailToApply(Exception):
    def __str__(self):
        return "DensOp: fail to apply"

class DensOp_FailToMeasure(Exception):
    def __str__(self):
        return "DensOp: fail to measure"

class DensOp_FailToAdd(Exception):
    def __str__(self):
        return "DensOp: fail to add"

class DensOp_FailToMul(Exception):
    def __str__(self):
        return "DensOp: fail to mul"

