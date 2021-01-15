# -*- coding: utf-8 -*-
import numpy as np

def CreateRegister(*args):
    """
    create multi-dimensional register id and initialize zero.

    Arguments
    ----------
    args : (int, int, ...)
        size of register id.

    Returns
    -------
    reg : list (multi-dimensional)
        register id list.

    Examples
    --------
    >>> reg = CreateRegister(2)
    >>> print(reg)
    [0,0]
    >>> reg = CreateRegister(2,3)
    >>> print(reg)
    [[0,0,0],[0,0,0]]
        
    """
    global COUNT
    COUNT = 0
    reg = np.zeros(args, dtype=int).tolist()
    return reg

def InitRegister(*args):
    """
    initialize register id

    Arguments
    ---------
    args : list, list,...
        arguments of register id

    Returns
    -------
    total_num : int
       total number of registers

    Examples
    --------
    >>> reg_0 = QState.create_register(3)
    >>> reg_1 = QState.create_register(2,4)
    >>> print(reg_0, reg_1)
    [0,0,0] [[0,0,0,0],[0,0,0,0]]
    >>> reg_num = InitRegister(reg_0, reg_1)
    >>> print(reg_num, reg_0, reg_1)
    11 [0,1,2] [[3,4,5,6],[7,8,9,10]]
    """
    global COUNT
    for x in args:
        if type(x) is list:
            for i,v in enumerate(x):
                if type(v) is int:
                    x[i] = COUNT
                    COUNT += 1
                else:
                    num = InitRegister(v)
    return COUNT
