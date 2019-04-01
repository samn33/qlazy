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

# MData

class MData_FailToGetFrq(Exception):
    def __str__(self):
        return "MData: fail to get frq"

class MData_FailToShow(Exception):
    def __str__(self):
        return "MData: fail to show"
