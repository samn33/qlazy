# -*- coding: utf-8 -*-
import warnings

from qlazy.config import *
from qlazy.util import *
from qlazy.error import *
from qlazy.Backend import *

class QComp:
    """ Quantum Computer.

    Attributes
    ----------
    qubit_num : int
        size of qubits
    cmem_num : int
        size of classical memory
    cmem : list
        classical memory
    qcirc : dict
        quantum circuit
    qstate : instance of quantum state
        quantum state (depend on backend)

    """
    def __init__(self, qubit_num, cmem_num=0, backend=None):

        self.qubit_num = qubit_num
        self.cmem_num = cmem_num
        self.cmem = [0] * cmem_num
        self.qcirc = []

        if backend is None:
            self.backend = Backend()
        else:
            self.backend = backend

        # qlazy
        if self.backend.name == 'qlazy':

            # qstate simulator
            if self.backend.device == 'qstate_simulator':
                from qlazy.backend.qlazy_qstate_simulator import init, run, reset, free
                self.__init = init
                self.__run = run
                self.__reset = reset
                self.__free = free
        
            # stabilizer simulator
            elif self.backend.device == 'stabilizer_simulator':
                from qlazy.backend.qlazy_stabilizer_simulator import init, run, reset, free
                self.__init = init
                self.__run = run
                self.__reset = reset
                self.__free = free
                
            else:
                raise Backend_Error_DeviceNotSupported()
            
        # qulacs
        elif self.backend.name == 'qulacs':

            # cpu_simulator
            if self.backend.device == 'cpu_simulator':
                from qlazy.backend.qulacs_cpu_simulator import init, run, reset, free
                self.__init = init
                self.__run = run
                self.__reset = reset
                self.__free = free
        
            # gpu_simulator
            elif self.backend.device == 'gpu_simulator':
                from qlazy.backend.qulacs_gpu_simulator import init, run, reset, free
                self.__init = init
                self.__run = run
                self.__reset = reset
                self.__free = free
                
            else:
                raise Backend_Error_DeviceNotSupported()
        
        # ibmq
        elif self.backend.name == 'ibmq':
            
            from qlazy.backend.ibmq import init, run, reset, free
            self.__init = init
            self.__run = run
            self.__reset = reset
            self.__free = free

        # 
        # note: followings are not supported in the near future
        #
        
        # qlazy qstate simulator
        elif self.backend.name == 'qlazy_qstate_simulator':
            from qlazy.backend.qlazy_qstate_simulator import init, run, reset, free
            self.__init = init
            self.__run = run
            self.__reset = reset
            self.__free = free
            warnings.warn("You should use name='qlazy',device='qstate_simulator', because name='qlazy_qstate_simulator' will be not supported in the near future")
        
        # qlazy stabilizer simulator
        elif self.backend.name == 'qlazy_stabilizer_simulator':
            from qlazy.backend.qlazy_stabilizer_simulator import init, run, reset, free
            self.__init = init
            self.__run = run
            self.__reset = reset
            self.__free = free
            warnings.warn("You should use name='qlazy',device='stabilizer_simulator', because name='qlazy_stabilizer_simulator' will be not supported in the near future")
        
        # qulacs
        elif self.backend.name == 'qulacs_simulator':
            from qlazy.backend.qulacs_cpu_simulator import init, run, reset, free
            self.__init = init
            self.__run = run
            self.__reset = reset
            self.__free = free
            warnings.warn("You should use name='qulacs',device='cpu_simulator', because name='qulacs_simulator' will be not supported in the near future")
        
        # qulacs-gpu
        elif self.backend.name == 'qulacs_gpu_simulator':
            from qlazy.backend.qulacs_gpu_simulator import init, run, reset, free
            self.__init = init
            self.__run = run
            self.__reset = reset
            self.__free = free
            warnings.warn("You should use name='qulacs',device='gpu_simulator', because name='qulacs_gpu_simulator' will be not supported in the near future")
        
        else:
            raise Backend_Error_NameNotSupported()

        self.qstate = self.__init(qubit_num=qubit_num, backend=self.backend)
            
    def reset(self, reset_qubits=True, reset_cmem=True, reset_qcirc=True):
        """
        reset quantum state, quantum circuit, and classical memory

        Parameters
        ----------
        reset_qubits : bool, default True
            reset quantum state or not.
        reset_cmem : bool, default True
            reset classical memory or not.
        reset_qcirc : bool, default True
            reset quantum circuit or not.

        Returns
        -------
        None

        """
        if reset_qubits == True:
            if self.qstate != None:
                self.__reset(qstate=self.qstate, backend=self.backend)
        else:
            if self.backend.name == 'ibmq':
                raise ValueError("reset_qubits must be True (can't maintain quantum state, when you reset QComp)")

        if reset_cmem == True:
            self.cmem = [0] * self.cmem_num

        if reset_qcirc == True:
            self.qcirc = []

    def free(self):
        """
        free quantum state, quantum circuit, and classical memory

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        if self.qstate != None:
            self.__free(qstate=self.qstate, backend=self.backend)

        del self.cmem
        del self.qcirc

    def run(self, shots=DEF_SHOTS, reset_qubits=True, reset_cmem=True, reset_qcirc=True):
        """
        run the quantum circuit.

        Parameters
        ----------
        shots : int, default 1
            number of measurements.
        reset_qubits : bool, default True
            reset quantum state or not.
        reset_cmem : bool, default True
            reset classical memory or not.
        reset_qcirc : bool, default True
            reset quantum circuit or not.

        Returns
        -------
        result : dict
            measurement result.

        Examples
        --------
        >>> # simple example
        >>> qc = QComp(2).h(0).cx(0,1).measure(qid=[0,1])  # add quantum gates, set circuit
        >>> result = qc.run(shots=10)  # run the circuit, get measured result
        >>> print(result)
        {'measured_qid': [0,1], 'frequency': Counter({'00': 5, '11': 5})}
        >>> ...
        >>> # control qubits by measured results
        >>> qc = QComp(qubit_num=2, cmem_num=2)  # set quantum and classical register 
        >>> qc.h(0).cx(0,1).measure(qid=[0],cid=[0]).x(0, ctrl=0).x(1, ctrl=0).measure(qid=[0,1])
	>>> result = qc.run(shots=10)
	>>> print(result)
        {'measured_qid': [0, 1], 'frequency': Counter({'00': 10})}

        """
        result = self.__run(qubit_num=self.qubit_num, cmem_num=self.cmem_num,
                            qstate=self.qstate, qcirc=self.qcirc, cmem=self.cmem, shots=shots,
                            backend=self.backend)
        self.reset(reset_qubits=reset_qubits, reset_cmem=reset_cmem, reset_qcirc=reset_qcirc)
        return result

    def measure(self, qid, cid=None, ctrl=None):
        """
        add measurement gate (Z-basis).

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.
        cid : list of int
            classical register id list to store measured result.
        ctrl : int
            address of classical memory to control gate operation

        Returns
        -------
        self : instance of QComp

        Notes
        -----
        'cid' must be 'None' or same length as 'qid'

        """
        self.__add_quantum_gate(kind=MEASURE, qid=qid, cid=cid, ctrl=ctrl)
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
        self : instance of QComp.

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
        self : instance of QComp

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
        self : instance of QComp.

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
        self : instance of QComp.

        """
        self.__add_quantum_gate(kind=HADAMARD, qid=[q0])
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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QState

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QState

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

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
        self : instance of QComp.

        """
        self.cx(q2,q1,ctrl=ctrl).ccx(q0,q1,q2,ctrl=ctrl).cx(q2,q1,ctrl=ctrl)
        return self

    def __add_quantum_gate(self, kind=None, qid=None, cid=None,
                           phase=DEF_PHASE, phase1=DEF_PHASE, phase2=DEF_PHASE,
                           ctrl=None):

        if cid != None and len(qid) != len(cid):
            raise QComp_Error_NumberOfClassicalReg()
            
        # non-clifford operation is not allowed for stabilizer calculation
        if (is_clifford_gate(kind) is False
            and is_measurement_gate(kind) is False
            and self.backend.name == 'qlazy_stabilizer_simulator'):
            raise QComp_Error_QgateNotSupported()
        
        else:
            self.qcirc.append({'kind': kind, 'qid': qid, 'cid': cid,
                               'phase': phase, 'phase1': phase1, 'phase2': phase2,
                               'ctrl': ctrl})
