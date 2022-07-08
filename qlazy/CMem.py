# -*- coding: utf-8 -*-
""" Classical Memory """
import ctypes

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

    def __str__(self):

        return str(self.get_bits())

    @property
    def bits(self):
        """ bit list of classical memory. """
        return self.get_bits()

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

    def get_bits(self):
        """
        get bit list of the classical memory.

        Parameters
        ----------
        None

        Returns
        -------
        bits : numpy.ndarray (int)
            bits array of the classical memory

        """
        bits = cmem_get_bits(self)
        return bits

    def set_bits(self, bits):
        """
        set bit list to the classical memory.

        Parameters
        ----------
        bits : list
            bits array of the classical memory

        Returns
        -------
        None

        """
        cmem_set_bits(self, bits)

    def __del__(self):

        cmem_free(self)

# c-library for qstate
from qlazy.lib.cmem_c import (cmem_init, cmem_copy, cmem_get_bits, cmem_set_bits,
                              cmem_free)
