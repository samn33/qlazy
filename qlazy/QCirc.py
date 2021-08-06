# -*- coding: utf-8 -*-
import ctypes
from collections import Counter
from ctypes.util import find_library
import warnings

from qlazy.config import *
from qlazy.error import *

class QCirc(ctypes.Structure):
    """ Quantum Circuit

    Attributes
    ----------
    qubit_num : int
        qubit number of the quantum state (= log(state_num)).
    cmem_num : int
        number of the classical register.
    gate_num : int
        number of gates in the quantum circuit.
    first: object
        first gate of the quantum circuit.
    last: object
        last gate of the quantum circuit.

    """
    _fields_ = [
        ('qubit_num', ctypes.c_int),
        ('cmem_num', ctypes.c_int),
        ('gate_num', ctypes.c_int),
        ('first', ctypes.c_void_p),
        ('last', ctypes.c_void_p),
    ]

    def __new__(cls):
        """
        Parameters
        ----------
        None

        Returns
        -------
        qcirc : instance (QCirc)

        """
        qcirc = qcirc_init()
        return qcirc
            
    def append_gate(self, kind, qid, para=None, c=None, ctrl=None):
        """
        Parameters
        ----------
        kind : int
            kind of gate
        qid : list (int)
            list of qubit id
        para : list (float), default None
            list of parameters
        c : int, default None
            classical register id to store measured data
        ctrl : int, default None
            classical register id to controll the gate

        Returns
        -------
        None

        """
        qcirc_append_gate(self, kind, qid, para, c, ctrl)

    def free(self):
        """
        free memory of quantum circuit.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        # qcirc_free(self)
        warnings.warn("No need to call 'free' method because free automatically, or you can use 'del' to free memory explicitly.")
        
    def __del__(self):
        
        qcirc_free(self)
        
# c-library for qstate
from qlazy.lib.qcirc_c import *
