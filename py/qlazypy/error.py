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
