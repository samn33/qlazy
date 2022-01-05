# -*- coding: utf-8 -*-
import ctypes
from collections import Counter
from ctypes.util import find_library
import warnings
import ctypes

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
        obj = qcirc_init()
        qcirc = ctypes.cast(obj.value, ctypes.POINTER(cls)).contents
        return qcirc
            
    def clone(self):
        """
        Parameters
        ----------
        None

        Returns
        -------
        qcirc : instance of QCirc
            quantum circuit

        """
        obj = qcirc_copy(self)
        qcirc = ctypes.cast(obj.value, ctypes.POINTER(self.__class__)).contents
        return qcirc

    def kind_first(self):
        """
        Parameters
        ----------
        None

        Returns
        -------
        kind : int
            kind of first quantum gate of quantum circuit

        Note
        ----
        return None if none of gates included

        """
        kind = qcirc_kind_first(self)
        return kind

    def pop_gate(self):
        """
        Parameters
        ----------
        None

        Returns
        -------
        gate : tupple of (int, [int,int], [float,float,float], int, int)
            tupple of (kind, qid, para, c, ctrl)
            - kind ... kind of gate
            - qid ... qubit id list
            - para ... parameters for rotation
            - c ... classical register ID to store measured data (only for measurement gate)
            - ctrl ... classical register id to controll the gate

        Note
        ----
        return NOT_A_GATE if none of gates included

        """
        (kind, qid, para, c, ctrl) = qcirc_pop_gate(self)
        return (kind, qid, para, c, ctrl)

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

    def split_unitary_non_unitary(self):
        """
        Parameters
        ----------
        None

        Returns
        -------
        qc_pair : tupple of (QCirc, Qcirc)
            former part includes only unitary gates and later part includes non-unitary gate (measure or reset) first
        """
        qc_unitary = QCirc()
        qc_non_unitary = self.clone()
        while True:
            kind_ori = qc_non_unitary.kind_first()
            if kind_ori is None or kind_ori is MEASURE or kind_ori is RESET:
                break
            else:
                (kind, qid, para, c, ctrl) = qc_non_unitary.pop_gate()
                qc_unitary.append_gate(kind, qid, para, c, ctrl)

        qc_pair = (qc_unitary, qc_non_unitary)
        return qc_pair

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
        warnings.warn("No need to call 'free' method because free automatically, or you can use 'del' to free memory explicitly.")
        
    def __del__(self):
        
        qcirc_free(self)
        
# c-library for qstate
from qlazy.lib.qcirc_c import *
