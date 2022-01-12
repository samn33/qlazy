# -*- coding: utf-8 -*-
import ctypes
from collections import Counter
from ctypes.util import find_library
import warnings
import ctypes

from qlazy.config import *
from qlazy.error import *

class CMem(ctypes.Structure):
    """ Classical Memory

    Attributes
    ----------
    cmem_num : int
        number of the classical register (classical memory size).
    bit_array : list (int)
        bit array of classical memory.

    """
    _fields_ = [
        ('cmem_num', ctypes.c_int),
        ('bit_array', ctypes.c_void_p),
    ]

    def __new__(cls, cmem_num, **kwargs):
        """
        Parameters
        ----------
        cmem_num : int
            number of the classical register.

        Returns
        -------
        cmem : instance (CMem)

        """
        obj = cmem_init(cmem_num)
        cmem = ctypes.cast(obj.value, ctypes.POINTER(cls)).contents
        return cmem
            
    def clone(self):
        """
        get the copy of the classical memory.

        Parameters
        ----------
        None

        Returns
        -------
        cmem : instance of CMem
            copy of the original classical memory.

        """
        obj = cmem_copy(self)
        cmem = ctypes.cast(obj.value, ctypes.POINTER(self.__class__)).contents
        return cmem

    def __del__(self):
        
        cmem_free(self)
        
# c-library for qstate
from qlazy.lib.cmem_c import *
