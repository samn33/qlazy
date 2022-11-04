# -*- coding: utf-8 -*-
""" functions to create and initialize registers """
from collections import UserList
import numpy as np

class Register(UserList):

    def __init__(self, shape=None):

        super().__init__(list(np.zeros(shape, dtype=int).tolist()))
        self.shape = shape
        self.start = 0
        self.num = np.prod(shape)
        
    def set_number(self, start):

        self.data = []
        self.start = start
        end = start + self.num
        reg_arr = np.array(list(range(start, end)))
        reg_arr = reg_arr.reshape(self.shape).tolist()
        [self.append(r) for r in reg_arr] 

        return end
        
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
    reg = Register(shape=args)
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
    >>> reg_0 = CreateRegister(3)
    >>> reg_1 = CreateRegister(2,4)
    >>> print(reg_0, reg_1)
    [0,0,0] [[0,0,0,0],[0,0,0,0]]
    >>> reg_num = InitRegister(reg_0, reg_1)
    >>> print(reg_num, reg_0, reg_1)
    11 [0,1,2] [[3,4,5,6],[7,8,9,10]]

    """
    cnt = 0
    for reg in args:
        cnt = reg.set_number(cnt)
    return cnt
