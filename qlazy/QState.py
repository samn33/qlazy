# -*- coding: utf-8 -*-
import random
import numpy as np
from collections import Counter

from qlazy.config import *
from qlazy.error import *
from qlazy.MData import *
from qlazy.Observable import *
from qlazy.lib.qstate_mcx import *

MDATA_TABLE = {}

class QState(ctypes.Structure):
    """ Quantum State

    Attributes
    ----------
    qubit_num : int
        qubit number of the quantum state (= log(state_num)).
    state_num : int
        dimension of the quantum state vector (= 2**qubit_num).
    amp : list of complex
        elements of the quantum state vector.

    """

    _fields_ = [
        ('qubit_num', ctypes.c_int),
        ('state_num', ctypes.c_int),
        ('camp', ctypes.c_void_p),
        ('camp_tmp', ctypes.c_void_p),
        ('gbank', ctypes.c_void_p),
    ]

    def __new__(cls, qubit_num=None, vector=None, seed=None):
        """
        Parameters
        ----------
        qubit_num : int
            qubit number of the quantum state.
        vector : list
            elements of the quantum state vector.
        seed : int, default - set randomly
            seed for random generation for meaurement.

        Notes
        -----
        You must specify either 'qubit_num' or 'vector', not both.

        """
        if seed is None:
            seed = random.randint(0,1000000)

        if qubit_num is not None:
            if qubit_num > MAX_QUBIT_NUM:
                print("qubit number must be {0:d} or less.".format(MAX_QUBIT_NUM))
                raise QState_Error_Initialize()

            return qstate_init(qubit_num, seed)

        else:
            return qstate_init_with_vector(vector, seed)
            
    def __str__(self):

        return str(self.get_amp())

    def reset(self, qid=[]):
        """
        reset to |00..0> state.

        Parameters
        ----------
        qid : list, default - qubit id's list for all of the qubits
            qubit id's list to reset.

        Notes
        -----
        If 'qid' is set, specified qubits are reset after
        measurement. So if the specified qubits are entangled with the
        remaining qubits, output quantum state is probabilistic. If no
        qubits are set, all qubits are zero reset.

        """
        qstate_reset(self, qid=qid)
        
    @classmethod
    def add_method(cls, method):
        """
        add method (custum gate).

        Parameters
        ----------
        method : func
            method (custum gate) to add.

        Examples
        --------
        >>> def bell(self, q0, q1):
        >>>     self.h(q0).cx(q0,q1)
        >>> ...
        >>> QState.add_method(bell)
        >>> qs = QState(qubit_num=2)
        >>> qs.bell(0,1)
        >>> ...
        
        """
        setattr(cls, method.__name__, method)
        
    @classmethod
    def add_methods(cls, *methods):
        """
        add methods (custum gates).

        Parameters
        ----------
        methods : func, func, ...
            arguments of methods (custum gates) to add.

        Examples
        --------
        >>> def bell(self, q0, q1):
        >>>     self.h(q0).cx(q0,q1)
        >>>     return self
        >>> ...
        >>> def flip(self, q0, q1):
        >>>     self.x(q0).x(q1)
        >>>     return self
        >>> ...
        >>> QState.add_methods(bell, flip, ...)
        >>> qs = QState(2)
        >>> qs.bell(0,1)
        >>> qs.flip(0,1)
        >>> ...
        
        """
        for method in methods:
            if callable(method):
                setattr(cls, method.__name__, method)
            else:
                raise QState_Error_AddMethods()
            
    @classmethod
    def create_register(cls, num):
        """
        create registers (qubit id's) and initialize zero.

        Parameters
        ----------
        num : int
            qubit number you want to use.

        Examples
        --------
        >>> qid = QState.create_register(3)
        >>> print(qid)
        [0,0,0]
        
        """
        qid = [0]*num
        return qid

    @classmethod
    def init_register(cls, *args):
        """
        initialize registers (qubit id's).

        Parameters
        ----------
        args : list, list,...
            arguments of qubit registers.

        Returns
        -------
        idx : int
            total qubit number.

        Examples
        --------
        >>> qid_0 = QState.create_register(3)
        >>> qid_1 = QState.create_register(2)
        >>> print(qid_0, qid_1)
        [0,0,0] [0,0]
        >>> qnum = QState.init_register(qid_0, qid_1)
        >>> print(qnum, qid_0, qid_1)
        5 [0,1,2] [3,4]
        """
        idx = 0
        for i in range(len(args)):
            for j in range(len(args[i])):
                args[i][j] = idx
                idx += 1
        return idx
    
    @classmethod
    def free_all(cls, *qstates):
        """
        free memory of the all quantum states.

        Parameters
        ----------
        qstates : instance of QState,instance of QState,...
            set of QState instances

        Returns
        -------
        None

        """
        for qs in qstates:
            if type(qs) is list or type(qs) is tuple:
                cls.free_all(*qs)
            elif type(qs) is QState:
                qs.free()
            else:
                raise QState_Error_FreeAll()

    @property
    def amp(self, qid=None):
        """ elements of quantum state vector. """
        return self.get_amp()
        
    def get_amp(self, qid=None):
        """
        get the elements of quantum state vector.

        Parameters
        ----------
        qid : list of int, default - list of all of the qubit id
            qubit id's list.

        Returns
        -------
        ret : list of complex
            elements of the quantum state vector.

        Notes
        -----
        If 'qid' is set, specified qubit state are got after remaining
        qubits are measured. So if the specified qubits are entangled
        with the remaining qubits, output quantum state is
        probabilistic. If no qubits are specified, you get all
        elements of the quantum state.

        """
        ret =  qstate_get_camp(self, qid)
        return ret

    def partial(self, qid=None):
        """
        get the partial quantum state.

        Parameters
        ----------
        qid : list of int, default - list of all of the qubit id
            qubit id's list to get as a partial quantum
            system.

        Returns
        -------
        qs : instance of QState
            partial quantum state.

        Notes
        -----
        If 'qid' is set, specified partial quantum system are got
        after remaining system are measured. So if the specified
        quantum system are entangled with the remaining system, output
        quantum state is probabilistic. If no qubits are specified,
        you get the copy of original quantum state.

        """
        vec = self.get_amp(qid)
        qs = QState(vector=vec)
        return qs
        
    def show(self, qid=None, nonzero=False):
        """
        show the quantum state 
        (elements of the state vector and probabilities).

        Parameters
        ----------
        qid : list of int, default - list of all of the qubit id
            qubit id's list to show.
        nonzero : bool, default False
            if True, only non-zero amplitudes are printed.

        Returns
        -------
        None

        Notes
        -----
        If 'qid' is set, it shows the elements of quantum state vector
        for partial quantum system specified by 'qid'. If the
        specified quantum system are entangled with the remaining
        system, output is probabilistic. If no qubits are specified,
        it shows the whole quantum state. This method does not change
        the original quantum state.

        Examples
        --------
        >>> qs = QState(2).h(0).cx(0,1)
        >>> qs.show()
        c[00] = +0.7071+0.0000*i : 0.5000 |++++++
        c[01] = +0.0000+0.0000*i : 0.0000 |
        c[10] = +0.0000+0.0000*i : 0.0000 |
        c[11] = +0.7071+0.0000*i : 0.5000 |++++++
        ...
        >>> qs.show(qid=[0])
        c[0] = +1.0000+0.0000*i : 1.0000 |+++++++++++
        c[1] = +0.0000+0.0000*i : 0.0000 |
        ...
        >>> qs.show(nonzero=True)
        c[00] = +0.7071+0.0000*i : 0.5000 |++++++
        c[11] = +0.7071+0.0000*i : 0.5000 |++++++

        """
        qstate_print(self, qid, nonzero)

    def clone(self):
        """
        get the copy of the quantum state.

        Parameters
        ----------
        None

        Returns
        -------
        qstate : instance of QState
            copy of the original quantum state.

        """
        qstate = qstate_copy(self)
        return qstate

    def bloch(self, q=0):
        """
        get bloch angles.

        Parameters
        ----------
        q : int
            qubit id

        Returns
        -------
        theta : float
            bloch angle with Z-axis
        phi : float
            bloch angle with X-axis

        Notes
        -----
        the unit of angle is PI radian. for example, 0.5 means 0.5*PI
        (radian).

        """
        theta, phi = qstate_bloch(self, q=0)
        return theta, phi

    def inpro(self, qstate, qid=[]):
        """
        get the inner product with quantum state.

        Parameters
        ----------
        qstate : instance of QState
            one of the two quantum state.
        qid : list of int, default - list of all of the qubit id
            qubit id's list.

        Returns
        -------
        inp : complex
            inner produt (<self|qstate>).

        Notes
        -----
        If 'qid' is set, you can get the inner product for partial
        quantum state. If the specified quantum system are entangled
        with the remaining system, output value is probabilistic,
        while original quantum states do not change.

        """
        if qid == []:
            inp = qstate_inner_product(self, qstate)
        else:
            qs_0 = self.partial(qid=qid)
            qs_1 = qstate.partial(qid=qid)
            inp = qstate_inner_product(qs_0, qs_1)
            qs_0.free()
            qs_1.free()
        return inp
        
    def tenspro(self, qstate):
        """
        get the tensor product with quantum state.

        Parameters
        ----------
        qstate : instance of QState
            quantum state to get the tensor product.

        Returns
        -------
        qstate_out : instance of QState
            tensor produt of 'self' and 'qstate'.

        """
        qstate_out = qstate_tensor_product(self, qstate)
        return qstate_out

    def fidelity(self, qstate, qid=[]):
        """
        get the fidelity with quantum state.

        Parameters
        ----------
        qstate : instance of QState
            one of the two quantum state.
        qid : list of int
            qubit id's list.

        Returns
        -------
        fid : float
            fidelity of two quantum states. absolute value of the
            inner product of two quantum states.

        Notes
        -----
        If 'qid' is set, you can get the fidelity for partial quantum
        state. If the specified quantum system are entangled with the
        remaining system, output value is probabilistic, while
        original quantum states do not change.

        """
        return abs(self.inpro(qstate, qid=qid))

    def composite(self, num=1):
        """
        get the composite state of same quantum states.

        Parameters
        ----------
        num : int
            number of quantum states.

        Returns
        -------
        qs : instance of QState
            composite quantum state.

        """
        if num <= 1:
            return self
        else:
            qs = self.clone()
            for i in range(num-1):
                qs_tmp = qs.tenspro(self)
                qs.free()
                qs = qs_tmp.clone()
                qs_tmp.free()
            return qs
        
    def evolve(self, observable=None, time=0.0, iter=0):
        """
        evolve the quantum state.

        Parameters
        ----------
        observable : instance of Observable
            Hamiltonian of the system.
        time : float
            period of time.
        iter : int
            number of iteration.

        Returns
        -------
        self : instance of QState

        Notes
        -----
        The 'iter' value should be sufficiently larger than the
        'time' value. This method change the original state.

        See Also
        --------
        Obserbable class (Observable.py)

        """
        qstate_evolve(self, observable=observable, time=time, iter=iter)
        return self
    
    def expect(self, observable=None):
        """
        get the expectation value for observable under the quantum state.

        Parameters
        ----------
        observable : instance of Observable
            obserbable of the system.

        Returns
        -------
        expect : float
            expect value.

        See Also
        --------
        Obserbable class (Observable.py)

        """
        expect = qstate_expect_value(self, observable=observable)
        return expect
    
    def apply(self, matrix=None, qid=None):
        """
        apply matrix.

        Parameters
        ----------
        matrix : list of list
            matrix to apply.

        Returns
        -------
        self : instance of QState

        Notes
        -----
        If 'qid' isn't set, dimension of the matrix must be equal to
        the 2 power of qubit number of the system. If 'qid' is set,
        dimension of the matrix must be equal to the 2 power of 'qid'
        length.

        """
        qstate_apply_matrix(self, matrix=matrix, qid=qid)
        return self

    def __schmidt_decomp(self, qid_0=[], qid_1=[]):

        vec = self.get_amp(qid=qid_0+qid_1)

        row = 2**len(qid_0)
        col = 2**len(qid_1)
        mat = np.zeros((row, col), dtype=np.complex)
        for idx,comp in enumerate(vec):
            mat[idx//col][idx%col] = comp
    
        U,D,V = np.linalg.svd(mat, full_matrices=False)
        coef = np.array([d for d in D if d > EPS])
        
        vec_0 = [v for i,v in enumerate(U.T) if i < len(coef)]
        vec_1 = [v for i,v in enumerate(V) if i < len(coef)]
    
        return (coef, vec_0, vec_1)

    def schmidt_decomp(self, qid_0=[], qid_1=[]):
        """
        schmidt decomposition.

        Parameters
        ----------
        qid_0 : list
            subsystem to decomposite.
        qid_1 : list
            another subsystem to decomposite.

        Returns
        -------
        coef : numpy.ndarray
            schmidt coefficients.
        qs_0 : list of QState instances
            decomposite quantum state related to 'qid_0'.
        qs_1 : list of QState instances
            decomposite quantum state related to 'qid_1'.

        """
        coef, vec_0, vec_1 = self.__schmidt_decomp(qid_0=qid_0, qid_1=qid_1)
        qs_0 = [QState(vector=v) for i,v in enumerate(vec_0) if i < len(coef)]
        qs_1 = [QState(vector=v) for i,v in enumerate(vec_1) if i < len(coef)]
    
        return (coef, qs_0, qs_1)

    def schmidt_coef(self, qid_0=[], qid_1=[]):
        """
        get schmidt coefficients.

        Parameters
        ----------
        qid_0 : list
            subsystem to decomposite.
        qid_1 : list
            another subsystem to decomposite.

        Returns
        -------
        coef : numpy.ndarray
            schmidt coefficients.

        """
        coef, vec_0, vec_1 = self.__schmidt_decomp(qid_0=qid_0, qid_1=qid_1)
        return coef

    # 1-qubit gate

    def x(self, q0):
        """
        operate X gate.

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=PAULI_X, phase=DEF_PHASE, qid=[q0])
        return self

    def y(self, q0):
        """
        operate Y gate.

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=PAULI_Y, phase=DEF_PHASE, qid=[q0])
        return self

    def z(self, q0):
        """
        operate Z gate.

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=PAULI_Z, phase=DEF_PHASE, qid=[q0])
        return self

    def xr(self, q0):
        """
        operate root X gate.

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=ROOT_PAULI_X, phase=DEF_PHASE, qid=[q0])
        return self

    def xr_dg(self, q0):
        """
        operate root X dagger gate 
        (hermmitian conjugate of root X gate).

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=ROOT_PAULI_X_, phase=DEF_PHASE, qid=[q0])
        return self

    def h(self, q0):
        """
        operate H gate (hadamard gate).

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=HADAMARD, phase=DEF_PHASE, qid=[q0])
        return self

    def s(self, q0):
        """
        operate S gate.

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=PHASE_SHIFT_S, phase=DEF_PHASE, qid=[q0])
        return self

    def s_dg(self, q0):
        """
        operate S dagger gate (hermitian conjugate of S gate).

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=PHASE_SHIFT_S_, phase=DEF_PHASE, qid=[q0])
        return self

    def t(self, q0):
        """
        operate T gate.

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=PHASE_SHIFT_T, phase=DEF_PHASE, qid=[q0])
        return self

    def t_dg(self, q0):
        """
        operate T dagger gate (hermitian conjugate of T gate).

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=PHASE_SHIFT_T_, phase=DEF_PHASE, qid=[q0])
        return self

    def rx(self, q0, phase=DEF_PHASE):
        """
        operate RX gate (rotation around X-axis).

        Parameters
        ----------
        q0 : int
            qubit id.
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=ROTATION_X, phase=phase, qid=[q0])
        return self

    def ry(self, q0, phase=DEF_PHASE):
        """
        operate RY gate (rotation around Y-axis).

        Parameters
        ----------
        q0 : int
            qubit id.
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=ROTATION_Y, phase=phase, qid=[q0])
        return self

    def rz(self, q0, phase=DEF_PHASE):
        """
        operate RZ gate (rotation around Z-axis).

        Parameters
        ----------
        q0 : int
            qubit id.
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=ROTATION_Z, phase=phase, qid=[q0])
        return self

    def p(self, q0, phase=DEF_PHASE):
        """
        operate P gate (phase shift gate).

        Parameters
        ----------
        q0 : int
            qubit id.
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QState

        Notes
        -----
        matrix expression is following...
        | 1.0 0.0             |
        | 0.0 exp(i*phase*PI) |

        """
        qstate_operate_qgate(self, kind=PHASE_SHIFT, phase=phase, qid=[q0])
        return self

    def u1(self, q0, alpha=DEF_PHASE):
        """
        operate U1 gate (by IBM).

        Parameters
        ----------
        q0 : int
            qubit id.
        alpha : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QState

        Notes
        -----
        this opration is equal to P gate (phase shift gate)

        """
        qstate_operate_qgate(self, kind=ROTATION_U1, phase=alpha, qid=[q0])
        return self

    def u2(self, q0, alpha=DEF_PHASE, beta=DEF_PHASE):
        """
        operate U2 gate (by IBM).

        Parameters
        ----------
        q0 : int
            qubit id.
        alpha : float
            rotation angle (unit of angle is pi radian).
        beta : float
            rotation angle (unit of angle is pi radian).

        Returns
        -------
        self : instance of QState

        Notes
        -----
        matrix experssion is following...
        | 1/sqrt(2)              -exp(i*alpha*PI)/sqrt(2)       |
        | exp(i*beta*PI)/sqrt(2) exp(i*(alpha+beta)*PI)/sqrt(2) |

        """
        qstate_operate_qgate(self, kind=ROTATION_U2, phase=alpha, phase1=beta, qid=[q0])
        return self

    def u3(self, q0, alpha=DEF_PHASE, beta=DEF_PHASE, gamma=DEF_PHASE):
        """
        operate U3 gate (by IBM).

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

        Returns
        -------
        self : instance of QState

        Notes
        -----
        matrix expression is following...
        | cos(gamma/2)                -exp(i*alpha*PI)*sin(gamma/2)       |
        | exp(i*beta*PI)*sin(gamma/2) exp(i*(alpha+beta)*PI)*cos(gamma/2) |


        """
        qstate_operate_qgate(self, kind=ROTATION_U3, phase=alpha, phase1=beta,
                             phase2=gamma, qid=[q0])
        return self

    # 2-qubit gate

    def cx(self, q0, q1):
        """
        operate CX gate (controlled X gate, controlled NOT gate, CNOT gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_X, phase=DEF_PHASE, qid=[q0,q1])
        return self

    def cy(self, q0, q1):
        """
        operate CY gate (controlled X gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_Y, phase=DEF_PHASE, qid=[q0,q1])
        return self

    def cz(self, q0, q1):
        """
        operate CZ gate (controlled Z gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_Z, phase=DEF_PHASE, qid=[q0,q1])
        return self

    def cxr(self, q0, q1):
        """
        operate CXR gate (controlled root X gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_XR, phase=DEF_PHASE, qid=[q0,q1])
        return self

    def cxr_dg(self, q0, q1):
        """
        operate CXR dagger gate (controlled XR dagger gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_XR_, phase=DEF_PHASE, qid=[q0,q1])
        return self

    def ch(self, q0, q1):
        """
        operate CH gate (controlled H gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_H, phase=DEF_PHASE, qid=[q0,q1])
        return self

    def cs(self, q0, q1):
        """
        operate CS gate (controlled S gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_S, phase=DEF_PHASE, qid=[q0,q1])
        return self

    def cs_dg(self, q0, q1):
        """
        operate CS dagger gate (controlled S dagger gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_S_, phase=DEF_PHASE, qid=[q0,q1])
        return self

    def ct(self, q0, q1):
        """
        operate CT gate (controlled T gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_T, phase=DEF_PHASE, qid=[q0,q1])
        return self

    def ct_dg(self, q0, q1):
        """
        operate CT dagger gate (controlled T dagger gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_T_, phase=DEF_PHASE, qid=[q0,q1])
        return self

    def sw(self, q0, q1):
        """
        swap gate

        Parameters
        ----------
        q0 : int
            qubit id
        q1 : int
            qubit id

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=SWAP_QUBITS, phase=DEF_PHASE, qid=[q0,q1])
        return self

    def cp(self, q0, q1, phase=DEF_PHASE):
        """
        operate CP gate (controlled P gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_P, phase=phase, qid=[q0,q1])
        return self

    def crx(self, q0, q1, phase=DEF_PHASE):
        """
        operate CRX gate (controlled RX gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_RX, phase=phase, qid=[q0,q1])
        return self

    def cry(self, q0, q1, phase=DEF_PHASE):
        """
        operate CRY gate (controlled RY gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_RY, phase=phase, qid=[q0,q1])
        return self

    def crz(self, q0, q1, phase=DEF_PHASE):
        """
        operate CRZ gate (controlled RZ gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_RZ, phase=phase, qid=[q0,q1])
        return self

    def cu1(self, q0, q1, alpha=DEF_PHASE):
        """
        operate CU1 gate (controlled U1 gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        alpha : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_U1, phase=alpha, qid=[q0,q1])
        return self

    def cu2(self, q0, q1, alpha=DEF_PHASE, beta=DEF_PHASE):
        """
        operate CU2 gate (controlled U2 gate).

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

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_U2, phase=alpha, phase1=beta,
                             qid=[q0,q1])
        return self

    def cu3(self, q0, q1, alpha=DEF_PHASE, beta=DEF_PHASE, gamma=DEF_PHASE):
        """
        operate CU3 gate (controlled U3 gate).

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

        Returns
        -------
        self : instance of QState

        """
        qstate_operate_qgate(self, kind=CONTROLLED_U3, phase=alpha, phase1=beta,
                             phase2=gamma, qid=[q0,q1])
        return self

    # 3-qubit gate
    
    def ccx(self, q0, q1, q2):
        """
        operate CCX gate (toffoli gate, controlled controlled X gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (control qubit).
        q2 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QState

        """
        self.cxr(q1,q2).cx(q0,q1).cxr_dg(q1,q2).cx(q0,q1).cxr(q0,q2)
        return self

    def csw(self, q0, q1, q2):
        """
        operate CSW gate (fredkin gate, controlled swap gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (swap qubit).
        q2 : int
            qubit id (swap qubit).

        Returns
        -------
        self : instance of QState

        """
        self.cx(q2,q1).ccx(q0,q1,q2).cx(q2,q1)
        return self

    # other gate

    def mcx(self,qid=[]):
        """
        operate MCX gate (multi-controlled X gate).
    
        Parameters
        ----------
        qid : list of int
            qubit id list [control, control, ... , control, target]
    
        Returns
        -------
        self : instance of QState
    
        """
        qstate_mcx(self, qid)
        return self
    
    # measurement
    
    def m(self, qid=None, shots=DEF_SHOTS, angle=0.0, phase=0.0, tag=None):
        """
        measurement in any direction (default: Z-axis).

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.
        shots : int, default 1
            number of measurements.
        angle : float, default 0.0
            direction of measurement (angle with Z-axis).
        phase : float, default 0.0
            direction of measurement (phase around Z-axis).
        tag : str
            tag of measurement data.

        Returns
        -------
        md : instance of MData
            measurement data.

        Examples
        --------
        >>> qs = QState(2).h(0).cx(0,1)
        >>> md = qs.m()
        >>> md.show(shots=100)
        direction of measurement: z-axis
        frq[00] = 52
        frq[11] = 48
        last state => 11

        See Also
        --------
        MData class (MData.py)

        """
        md = qstate_measure(self, MDATA_TABLE, qid=qid, shots=shots,
                              angle=angle, phase=phase, tag=tag)
        return md
        
    def mx(self, qid=None, shots=DEF_SHOTS, tag=None):
        """
        X-axis measurement.

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.
        shots : int, default 1
            number of measurements.
        tag : str
            tag of measurement data.

        Returns
        -------
        md : instance of MData
            measurement data.

        See Also
        --------
        MData class (MData.py)

        """
        md = qstate_measure(self, MDATA_TABLE, qid=qid, shots=shots,
                              angle=0.5, phase=0.0, tag=tag)
        return md
        
    def my(self, qid=None, shots=DEF_SHOTS, tag=None):
        """
        Y-axis measurement.

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.
        shots : int, default 1
            number of measurements.
        tag : str
            tag of measurement data.

        Returns
        -------
        md : instance of MData
            measurement data.

        See Also
        --------
        MData class (MData.py)

        """
        md =  qstate_measure(self, MDATA_TABLE, qid=qid, shots=shots,
                              angle=0.5, phase=0.5, tag=tag)
        return md
        
    def mz(self, qid=None, shots=DEF_SHOTS, tag=None):
        """
        Z-axis measurement.

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.
        shots : int, default 1
            number of measurements.
        tag : str
            tag of measurement data.

        Returns
        -------
        md : instance of MData
            measurement data.

        See Also
        --------
        MData class (MData.py)

        """
        md =  qstate_measure(self, MDATA_TABLE, qid=qid, shots=shots,
                              angle=0.0, phase=0.0, tag=tag)
        return md

    def mb(self, qid=None, shots=DEF_SHOTS, tag=None):
        return qstate_measure_bell(self, MDATA_TABLE, qid=qid, shots=shots, tag=tag)
        
    def m_value(self, tag=None, angle=0.0, phase=0.0, binary=False):
        """
        get measurement value.

        Parameters
        ----------
        tag : str
            tag of measurement data.
        angle : float, default 0.0
            direction of measurement (angle with Z-axis).
        phase : float, default 0.0
            direction of measurement (phase around Z-axis).
        binary : bool
            format of measurement value.

        Returns
        -------
        mval : str (binary:True) or int (binary:False)
            measurement value (if shots>1, last measured value).
            - binary=True -> '00','01','10','11' for 2 qubits measurement
            - binary=False -> 0,1,2,3 for 2 qubits measurement

        Examples
        --------
        >>> qs = QState(2).h(0).cx(0,1)
        >>> qs.m(shots=100)
        >>> print(qs.m_value(binary=True))
        00

        """
        if tag is None: tag = DEF_TAG
        tag_long = repr(self) + '.' + tag
        mval = MDATA_TABLE[tag_long].measured_value(angle=angle, phase=phase)
        if binary == True:
            digits = len(MDATA_TABLE[tag_long].qid)
            mval = '{:0{digits}b}'.format(mval, digits=digits)
        return mval

    def m_bit(self, q, tag=None, angle=0.0, phase=0.0, boolean=False):
        """
        get measured bit value.

        Parameters
        ----------
        q : int
        tag : str
            tag of measurement data.
        angle : float, default 0.0
            direction of measurement (angle with Z-axis).
        phase : float, default 0.0
            direction of measurement (phase around Z-axis).
        boolean : bool
            format of measured bit.

        Returns
        -------
        mbit : bool (boolean:True) or int (boolean:False)
            measured bit value (if shots>1, last measured bit value).
            - boolean=True -> False,True
            - boolean=False -> 0,1

        Examples
        --------
        >>> qs = QState(2).h(0).cx(0,1)
        >>> qs.m(shots=100)
        >>> print(qs.m_bit(boolean=True))
        True

        """
        if tag is None: tag = DEF_TAG
        tag_long = repr(self) + '.' + tag
        mbit =  MDATA_TABLE[tag_long].measured_bit(q, angle=angle, phase=phase)
        if boolean == True:
            mbit = bool(mbit)
        return mbit
        
    def m_freq(self, tag=None, angle=0.0, phase=0.0):
        """
        get measurement value.

        Parameters
        ----------
        tag : str
            tag of measurement data.
        angle : float, default 0.0
            direction of measurement (angle with Z-axis).
        phase : float, default 0.0
            direction of measurement (phase around Z-axis).

        Returns
        -------
        mfrq : instance of Counter from collection (Python standard library)
            measurement frequency.

        Examples
        --------
        >>> qs = QState(2).h(0).cx(0,1)
        >>> qs.m(shots=100)
        >>> print(qs.m_freq())
        Counter({'11': 53, '00': 47})

        """
        if tag is None: tag = DEF_TAG
        tag_long = repr(self) + '.' + tag
        mfrq = MDATA_TABLE[tag_long].measured_freq(angle=angle, phase=phase)
        return mfrq

    def free(self):
        """
        free memory of quantum state.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        qstate_free(self)
        

# c-library for qstate
from qlazy.lib.qstate_c import *
