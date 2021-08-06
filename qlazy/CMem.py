# -*- coding: utf-8 -*-
import ctypes
from collections import Counter
from ctypes.util import find_library
import warnings

from qlazy.config import *
from qlazy.error import *

class CMem(ctypes.Structure):
    """ Classical Memory

    Attributes
    ----------
    cmem_num : int
        number of the classical register.
    bit_array : list (int)
        bit array of classical memory.

    """
    _fields_ = [
        ('cmem_num', ctypes.c_int),
        ('bit_array', ctypes.c_void_p),
    ]

    def __new__(cls, cmem_num):
        """
        Parameters
        ----------
        cmem_num : int
            number of the classical register.

        Returns
        -------
        cmem : instance (CMem)

        """
        cmem = cmem_init(cmem_num)
        return cmem
            
    def free(self):
        """
        free memory of classical memory.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        # cmem_free(self)
        warnings.warn("No need to call 'free' method because free automatically, or you can use 'del' to free memory explicitly.")
        
    def __del__(self):
        
        cmem_free(self)
        
# c-library for qstate
from qlazy.lib.cmem_c import *
