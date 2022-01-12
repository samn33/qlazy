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

    def __new__(cls, **kwargs):
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

    def __str__(self):

        return self.to_string()
    
    def to_string(self):
        """
        get string of quantum circuit description.

        Parameters
        ----------
        None

        Returns
        -------
        qcirc_str : str

        """
        qc = self.clone()
        qcirc_str = ""
        while True:
            kind = qc.kind_first()
            if kind is None:
                break
            else:
                (kind, qid, para, c, ctrl) = qc.pop_gate()
                term_num = get_qgate_qubit_num(kind)
                if (kind == MEASURE) or (kind == RESET):
                    term_num = 1
                para_num = get_qgate_param_num(kind)

                gate_str = GATE_STRING[kind]
                qid_str = " ".join(map(str, [qid[i] for i in range(term_num)]))
                qid_str.strip()

                if para_num == 0:
                    para_str = ""
                else:
                    para_str = ",".join(map(str, [para[i] for i in range(para_num)]))
                    para_str = "(" + para_str+ ")"
                
                if c is None:
                    c_str = ""
                else:
                    c_str = "-> {}".format(c)

                if ctrl is None:
                    ctrl_str = ""
                else:
                    ctrl_str = ", ctrl = {}".format(ctrl)
                    
                qcirc_str += "{0:}{2:} {1:} {3:}{4:}\n".format(gate_str, qid_str, para_str, c_str, ctrl_str)
                
        return qcirc_str.strip()
        
    def __add__(self, qc):
        """
        Parameters
        ----------
        qc : instance of QCirc
            quantum circuit (merged)

        Returns
        -------
        qcirc : instance of QCirc
            quantum circuit (result)

        """
        qcirc = self.merge(qc)
        return qcirc

    def __iadd__(self, qc):
        """
        Parameters
        ----------
        qc : instance of QCirc
            quantum circuit (merged)

        Returns
        -------
        qcirc : instance of QCirc
            quantum circuit (result)

        """
        qcirc = self.merge(qc)
        return qcirc

    def __eq__(self, qc):
        """
        Parameters
        ----------
        qc : instance of QCirc
            quantum circuit (merged)

        Returns
        -------
        ans : bool
            equal or not

        """
        ans = self.is_equal(qc)
        return ans

    def __ne__(self, qc):
        """
        Parameters
        ----------
        qc : instance of QCirc
            quantum circuit (merged)

        Returns
        -------
        ans : bool
            equal or not

        """
        ans = not self.is_equal(qc)
        return ans

    def clone(self):
        """
        clone quantum circuit.

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

    def merge(self, qc):
        """
        merge quantum circuit.

        Parameters
        ----------
        qc : instance of QCirc
            quantum circuit (merged)

        Returns
        -------
        qcirc : instance of QCirc
            quantum circuit (result)

        """
        obj = qcirc_merge(self, qc)
        qcirc = ctypes.cast(obj.value, ctypes.POINTER(self.__class__)).contents
        return qcirc

    def is_equal(self, qc):
        """
        eaual or not.

        Parameters
        ----------
        qc : instance of QCirc
            quantum circuit (merged)

        Returns
        -------
        qcirc : instance of QCirc
            quantum circuit (result)

        """
        ans = qcirc_is_equal(self, qc)
        return ans

    def kind_first(self):
        """
        get kind of first gate of the circuit.

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
        pop first gate of the circuit.

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

        """
        (kind, qid, para, c, ctrl) = qcirc_pop_gate(self)
        return (kind, qid, para, c, ctrl)

    def append_gate(self, kind, qid, para=None, c=None, ctrl=None):
        """
        append gate to the end of the circuit.

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
        split two part of the gate.

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

    def __del__(self):
        
        qcirc_free(self)

    def measure(self, qid, cid):
        """
        add measurement gate (Z-basis).

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.
        cid : list of int
            classical register id list to store measured result.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=MEASURE, qid=qid, cid=cid, ctrl=None)
        return self

    def reset(self, qid):
        """
        add reset gate.

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.
        cid : list of int
            classical register id list to store measured result.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        Notes
        -----
        'cid' must be 'None' or same length as 'qid'

        """
        self.__add_quantum_gate(kind=RESET, qid=qid, cid=None, ctrl=None)
        return self

    # add 1-qubit gate
    
    def x(self, q0, ctrl=None):
        """
        add X gate.

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=PAULI_X, qid=[q0], ctrl=ctrl)
        return self

    def y(self, q0, ctrl=None):
        """
        add Y gate.

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=PAULI_Y, qid=[q0], ctrl=ctrl)
        return self

    def z(self, q0, ctrl=None):
        """
        add Z gate.

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=PAULI_Z, qid=[q0], ctrl=ctrl)
        return self

    def h(self, q0, ctrl=None):
        """
        add H gate (hadamard gate).

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=HADAMARD, qid=[q0], ctrl=ctrl)
        return self
        
    def xr(self, q0, ctrl=None):
        """
        add root X gate.

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=ROOT_PAULI_X, qid=[q0], ctrl=ctrl)
        return self

    def xr_dg(self, q0, ctrl=None):
        """
        add root X dagger gate 
        (hermmitian conjugate of root X gate).

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=ROOT_PAULI_X_, qid=[q0], ctrl=ctrl)
        return self

    def s(self, q0, ctrl=None):
        """
        add S gate.

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=PHASE_SHIFT_S, qid=[q0], ctrl=ctrl)
        return self

    def s_dg(self, q0, ctrl=None):
        """
        add S dagger gate (hermitian conjugate of S gate).

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=PHASE_SHIFT_S_, qid=[q0], ctrl=ctrl)
        return self

    def t(self, q0, ctrl=None):
        """
        add T gate.

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=PHASE_SHIFT_T, qid=[q0], ctrl=ctrl)
        return self

    def t_dg(self, q0, ctrl=None):
        """
        add T dagger gate (hermitian conjugate of T gate).

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=PHASE_SHIFT_T_, qid=[q0], ctrl=ctrl)
        return self

    def rx(self, q0, phase=DEF_PHASE, ctrl=None):
        """
        add RX gate (rotation around X-axis).

        Parameters
        ----------
        q0 : int
            qubit id.
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=ROTATION_X, qid=[q0], phase=phase, ctrl=ctrl)
        return self

    def ry(self, q0, phase=DEF_PHASE, ctrl=None):
        """
        add RY gate (rotation around Y-axis).

        Parameters
        ----------
        q0 : int
            qubit id.
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=ROTATION_Y, qid=[q0], phase=phase, ctrl=ctrl)
        return self

    def rz(self, q0, phase=DEF_PHASE, ctrl=None):
        """
        add RZ gate (rotation around Z-axis).

        Parameters
        ----------
        q0 : int
            qubit id.
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=ROTATION_Z, qid=[q0], phase=phase, ctrl=ctrl)
        return self

    def p(self, q0, phase=DEF_PHASE, ctrl=None):
        """
        add P gate (phase shift gate).

        Parameters
        ----------
        q0 : int
            qubit id.
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        Notes
        -----
        matrix expression is following...
        | 1.0 0.0             |
        | 0.0 exp(i*phase*PI) |

        """
        self.__add_quantum_gate(kind=PHASE_SHIFT, qid=[q0], phase=phase, ctrl=ctrl)
        return self

    def u1(self, q0, alpha=DEF_PHASE, ctrl=None):
        """
        add U1 gate (by IBM).

        Parameters
        ----------
        q0 : int
            qubit id.
        alpha : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        Notes
        -----
        this opration is equal to P gate (phase shift gate)

        """
        self.__add_quantum_gate(kind=ROTATION_U1, qid=[q0], phase=alpha, ctrl=ctrl)
        return self

    def u2(self, q0, alpha=DEF_PHASE, beta=DEF_PHASE, ctrl=None):
        """
        add U2 gate (by IBM).

        Parameters
        ----------
        q0 : int
            qubit id.
        alpha : float
            rotation angle (unit of angle is pi radian).
        beta : float
            rotation angle (unit of angle is pi radian).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        Notes
        -----
        matrix experssion is following...
        | 1/sqrt(2)              -exp(i*alpha*PI)/sqrt(2)       |
        | exp(i*beta*PI)/sqrt(2) exp(i*(alpha+beta)*PI)/sqrt(2) |

        """
        self.__add_quantum_gate(kind=ROTATION_U2, qid=[q0], phase=alpha, phase1=beta, ctrl=ctrl)
        return self

    def u3(self, q0, alpha=DEF_PHASE, beta=DEF_PHASE, gamma=DEF_PHASE, ctrl=None):
        """
        add U3 gate (by IBM).

        Parameters
        ----------
        q0 : int
            qubit id.
        alpha : float
            rotation angle (unit of angle is pi radian).
        beta : float
            rotation angle (unit of angle is pi radian).
        gamma : float
            rotation angle (unit of angle is pi radian).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        Notes
        -----
        matrix expression is following...
        | cos(gamma/2)                -exp(i*alpha*PI)*sin(gamma/2)       |
        | exp(i*beta*PI)*sin(gamma/2) exp(i*(alpha+beta)*PI)*cos(gamma/2) |


        """
        self.__add_quantum_gate(kind=ROTATION_U3, qid=[q0], phase=alpha, phase1=beta,
                                phase2=gamma, ctrl=ctrl)
        return self

    # add 2-qubit gate
    
    def cx(self, q0, q1, ctrl=None):
        """
        add CX gate (controlled X gate, controlled NOT gate, CNOT gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_X, qid=[q0,q1], ctrl=ctrl)
        return self

    def cy(self, q0, q1, ctrl=None):
        """
        operate CY gate (controlled X gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_Z, qid=[q0,q1], ctrl=ctrl)
        self.__add_quantum_gate(kind=CONTROLLED_X, qid=[q0,q1], ctrl=ctrl)
        self.__add_quantum_gate(kind=PHASE_SHIFT_S, qid=[q0], ctrl=ctrl)
        return self

    def cz(self, q0, q1, ctrl=None):
        """
        add CZ gate (controlled Z gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_Z, qid=[q0,q1], ctrl=ctrl)
        return self

    def cxr(self, q0, q1, ctrl=None):
        """
        add CXR gate (controlled root X gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_XR, qid=[q0,q1], ctrl=ctrl)
        return self

    def cxr_dg(self, q0, q1, ctrl=None):
        """
        add CXR dagger gate (controlled XR dagger gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_XR_, qid=[q0,q1], ctrl=ctrl)
        return self

    def ch(self, q0, q1, ctrl=None):
        """
        add CH gate (controlled H gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_H, qid=[q0,q1], ctrl=ctrl)
        return self

    def cs(self, q0, q1, ctrl=None):
        """
        add CS gate (controlled S gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_S, qid=[q0,q1], ctrl=ctrl)
        return self

    def cs_dg(self, q0, q1, ctrl=None):
        """
        add CS dagger gate (controlled S dagger gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_S_, qid=[q0,q1], ctrl=ctrl)
        return self

    def ct(self, q0, q1, ctrl=None):
        """
        add CT gate (controlled T gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_T, qid=[q0,q1], ctrl=ctrl)
        return self

    def ct_dg(self, q0, q1, ctrl=None):
        """
        add CT dagger gate (controlled T dagger gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_T_, qid=[q0,q1], ctrl=ctrl)
        return self

    def sw(self, q0, q1, ctrl=None):
        """
        add swap gate

        Parameters
        ----------
        q0 : int
            qubit id
        q1 : int
            qubit id
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=SWAP_QUBITS, qid=[q0,q1], ctrl=ctrl)
        return self

    def cp(self, q0, q1, phase=DEF_PHASE, ctrl=None):
        """
        add CP gate (controlled P gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_P, qid=[q0,q1], phase=phase, ctrl=ctrl)
        return self

    def crx(self, q0, q1, phase=DEF_PHASE, ctrl=None):
        """
        add CRX gate (controlled RX gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_RX, qid=[q0,q1], phase=phase, ctrl=ctrl)
        return self

    def cry(self, q0, q1, phase=DEF_PHASE, ctrl=None):
        """
        add CRY gate (controlled RY gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_RY, qid=[q0,q1], phase=phase, ctrl=ctrl)
        return self

    def crz(self, q0, q1, phase=DEF_PHASE, ctrl=None):
        """
        add CRZ gate (controlled RZ gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_RZ, qid=[q0,q1], phase=phase, ctrl=ctrl)
        return self

    def cu1(self, q0, q1, alpha=DEF_PHASE, ctrl=None):
        """
        add CU1 gate (controlled U1 gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        alpha : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_U1, qid=[q0,q1], phase=alpha, ctrl=ctrl)
        return self

    def cu2(self, q0, q1, alpha=DEF_PHASE, beta=DEF_PHASE, ctrl=None):
        """
        add CU2 gate (controlled U2 gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        alpha : float
            rotation angle (unit of angle is PI radian).
        beta : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_U2, qid=[q0,q1], phase=alpha, phase1=beta, ctrl=ctrl)
        return self

    def cu3(self, q0, q1, alpha=DEF_PHASE, beta=DEF_PHASE, gamma=DEF_PHASE, ctrl=None):
        """
        add CU3 gate (controlled U3 gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        alpha : float
            rotation angle (unit of angle is PI radian).
        beta : float
            rotation angle (unit of angle is PI radian).
        gamma : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.__add_quantum_gate(kind=CONTROLLED_U3, qid=[q0,q1], phase=alpha, phase1=beta,
                                phase2=gamma, ctrl=ctrl)
        return self

    # 3-qubit gate
    
    def ccx(self, q0, q1, q2, ctrl=None):
        """
        add CCX gate (toffoli gate, controlled controlled X gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (control qubit).
        q2 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.cxr(q1,q2,ctrl=ctrl).cx(q0,q1,ctrl=ctrl).cxr_dg(q1,q2,ctrl=ctrl)
        self.cx(q0,q1,ctrl=ctrl).cxr(q0,q2,ctrl=ctrl)
        return self

    def csw(self, q0, q1, q2, ctrl=None):
        """
        add CSW gate (fredkin gate, controlled swap gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (swap qubit).
        q2 : int
            qubit id (swap qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.cx(q2,q1,ctrl=ctrl).ccx(q0,q1,q2,ctrl=ctrl).cx(q2,q1,ctrl=ctrl)
        return self

    def operate(self, pp=None, ctrl=None):
        """
        add unitary operator.

        Parameters
        ----------
        pp : instance of PauliProduct
            pauli product to operate
        ctrl : int
            contoroll qubit id for controlled pauli product

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        pauli_list = pp.pauli_list
        qid = pp.qid
    
        if ctrl is None:
            for q, pauli in zip(qid, pauli_list):
                if pauli == 'X':
                    self.x(q)
                elif pauli == 'Y':
                    self.y(q)
                elif pauli == 'Z':
                    self.z(q)
                else:
                    continue
        else:
            if ctrl in qid:
                raise ValueError("controll and target qubit id conflict")
        
            for q, pauli in zip(qid, pauli_list):
                if pauli == 'X':
                    self.cx(ctrl, q)
                elif pauli == 'Y':
                    self.cy(ctrl, q)
                elif pauli == 'Z':
                    self.cz(ctrl, q)
                else:
                    continue
    
        return self

    def __add_quantum_gate(self, kind=None, qid=None, cid=None,
                           phase=DEF_PHASE, phase1=DEF_PHASE, phase2=DEF_PHASE,
                           ctrl=None):

        if qid is None:
            raise ValueError("qid must be specified")
            
        para = [phase, phase1, phase2]
        if is_measurement_gate(kind) == True:
            if cid is None:
                raise ValueError("cid must be specified")
            for q, c in zip(qid, cid):
                qid = [q]
                self.append_gate(kind, qid, para, c, ctrl)
        elif is_reset_gate(kind) == True:
            for q in qid:
                qid = [q]
                c = None
                self.append_gate(kind, qid, para, c, ctrl)
        else:
            c = None
            self.append_gate(kind, qid, para, c, ctrl)
        
# c-library for qstate
from qlazy.lib.qcirc_c import *
