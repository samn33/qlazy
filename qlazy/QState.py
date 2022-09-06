# -*- coding: utf-8 -*-
""" Quantum State """
import ctypes
import random
import numpy as np

import qlazy.config as cfg
from qlazy.lib.qstate_mcx import qstate_mcx
from qlazy.gpu import is_gpu_supported_lib

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

    if is_gpu_supported_lib() is True:
        _fields_ = [
            ('qubit_num', ctypes.c_int),
            ('state_num', ctypes.c_int),
            ('buf_id', ctypes.c_int),
            ('camp', ctypes.c_void_p),
            ('buffer_0', ctypes.c_void_p),
            ('buffer_1', ctypes.c_void_p),
            ('prob_array', ctypes.c_void_p),
            ('prob_updated', ctypes.c_bool),
            ('d_buf_id', ctypes.c_int),
            ('d_camp', ctypes.c_void_p),
            ('d_buffer_0', ctypes.c_void_p),
            ('d_buffer_1', ctypes.c_void_p),
            ('d_prob_array', ctypes.c_void_p),
            ('d_prob_updated', ctypes.c_bool),
            ('gbank', ctypes.c_void_p),
            ('use_gpu', ctypes.c_bool),
        ]
    else:
        _fields_ = [
            ('qubit_num', ctypes.c_int),
            ('state_num', ctypes.c_int),
            ('buf_id', ctypes.c_int),
            ('camp', ctypes.c_void_p),
            ('buffer_0', ctypes.c_void_p),
            ('buffer_1', ctypes.c_void_p),
            ('prob_array', ctypes.c_void_p),
            ('prob_updated', ctypes.c_bool),
            ('gbank', ctypes.c_void_p),
            ('use_gpu', ctypes.c_bool),
        ]

    def __new__(cls, qubit_num=0, vector=None, seed=None, use_gpu=False, **kwargs):
        """
        Parameters
        ----------
        qubit_num : int
            qubit number of the quantum state.
        vector : list
            elements of the quantum state vector.
        seed : int, default - set randomly
            seed for random generation for meaurement.
        use_gpu : bool
            calcurate with GPU(cuda) or not.

        Notes
        -----
        You must specify either 'qubit_num' or 'vector', not both.

        """
        if seed is None:
            seed = random.randint(0, 1000000)

        # if qubit_num is not None:
        if qubit_num > 0:
            if qubit_num > cfg.MAX_QUBIT_NUM:
                raise ValueError("qubit number must be {0:d} or less.".format(cfg.MAX_QUBIT_NUM))
            obj = qstate_init(qubit_num, seed, use_gpu)
        elif qubit_num == 0:
            obj = qstate_init_with_vector(vector, seed, use_gpu)
        else:
            raise ValueError("qubit number must be positive.")

        self = ctypes.cast(obj.value, ctypes.POINTER(cls)).contents
        return self

    def __str__(self):

        return str(self.get_amp())

    def reset(self, qid=None):
        """
        reset to |00..0> state.

        Parameters
        ----------
        qid : list, default - qubit id's list for all of the qubits
            qubit id's list to reset.

        Returns
        -------
        self : instance of QState
            quantum state.

        Notes
        -----
        If 'qid' is set, specified qubits are reset after
        measurement. So if the specified qubits are entangled with the
        remaining qubits, output quantum state is probabilistic. If no
        qubits are set, all qubits are zero reset.

        """
        qstate_reset(self, qid=qid)
        return self

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
        >>>     return self
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
                raise ValueError("can't add method.")

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
        for i, arg in enumerate(args):
            for j in range(len(arg)):
                args[i][j] = idx
                idx += 1
        return idx

    @classmethod
    def del_all(cls, *qstates):
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
            if isinstance(qs, (list, tuple)):
                cls.del_all(*qs)
            elif isinstance(qs, cls):
                del qs
            else:
                raise ValueError("can't free qstate.")

    @property
    def amp(self):
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
        ret : numpy.ndarray (complex)
            elements of the quantum state vector.

        Notes
        -----
        If 'qid' is set, specified qubit state are got after remaining
        qubits are measured. So if the specified qubits are entangled
        with the remaining qubits, output quantum state is
        probabilistic. If no qubits are specified, you get all
        elements of the quantum state.

        """
        ret = qstate_get_camp(self, qid)
        return ret

    def get_prob(self, qid=None):
        """
        get the probability list of quantum state vector.

        Parameters
        ----------
        qid : list of int, default - list of all of the qubit id
            qubit id's list.

        Returns
        -------
        prob : dict
            key - bits string
            value - probability
            ex) {'00': 0.52, '11': 0.48}

        """
        amp = qstate_get_camp(self, qid)
        if qid is None:
            digits = self.qubit_num
        else:
            digits = len(qid)
        prob = {"{:0{digits}b}".format(i, digits=digits): abs(c) * abs(c)
                for i, c in enumerate(amp) if abs(c) > cfg.EPS}
        return prob

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
        qs = self.__class__(vector=vec)
        return qs

    def show(self, qid=None, nonzero=False, preal=0):
        """
        show the quantum state
        (elements of the state vector and probabilities).

        Parameters
        ----------
        qid : list of int, default - list of all of the qubit id
            qubit id's list to show.
        nonzero : bool, default False
            if True, only non-zero amplitudes are printed.
        preal : int, default 0
            state id to make positive real amplitude.
            (if -1 is set, do not go out the global phase factor)

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
        # qstate_print(self, qid, nonzero)

        if qid is None or len(qid) == 0:
            digits = self.qubit_num
        else:
            digits = len(qid)

        vec = self.get_amp(qid=qid)

        if preal >= 0:
            exp_i_phase = 1.+0.j
            if abs(vec[preal].imag) > cfg.EPS:
                exp_i_phase = vec[preal] / abs(vec[preal])
            elif vec[preal].real < 0.0:
                exp_i_phase = -exp_i_phase
            vec = vec / exp_i_phase

        for i, v in enumerate(vec):
            bits = "{:0{digits}b}".format(i, digits=digits)
            absval2 = abs(v) * abs(v)
            if absval2 < cfg.EPS:
                bar_len = 0
            else:
                bar_len = int(absval2 / 0.1 + 1.5)
            bar_str = "|" + "+" * bar_len
            if nonzero is True and absval2 < cfg.EPS:
                continue
            else:
                print("c[{}] = {:+.4f}{:+.4f}*i : {:.4f} {}"
                      .format(bits, v.real, v.imag, abs(v)**2, bar_str))

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
        obj = qstate_copy(self)
        qs = ctypes.cast(obj.value, ctypes.POINTER(self.__class__)).contents
        return qs

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
        theta, phi = qstate_bloch(self, q=q)
        return theta, phi

    def inpro(self, qstate, qid=None):
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
        if qid == [] or qid is None:
            inp = qstate_inner_product(self, qstate)
        else:
            qs_0 = self.partial(qid=qid)
            qs_1 = qstate.partial(qid=qid)
            inp = qstate_inner_product(qs_0, qs_1)
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
        obj = qstate_tensor_product(self, qstate)
        qs = ctypes.cast(obj.value, ctypes.POINTER(self.__class__)).contents
        return qs

    def fidelity(self, qstate, qid=None):
        """
        get fidelity with the quantum state.

        Parameters
        ----------
        qstate : instance of QState
            one of the two quantum states.
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

        qs = self.clone()
        for _ in range(num-1):
            qs_tmp = qs.tenspro(self)
            qs = qs_tmp.clone()
        return qs

    def join(self, qs_list):
        """
        get tensor product state of the quantum states' list.

        Parameters
        ----------
        qs_list : list (QState)
            list of quantum states.

        Returns
        -------
        qs_out : instance of QState
            tensor product state.

        """
        qs_out = self.clone()
        for qs in qs_list:
            qs_tmp = qs_out.clone()
            qs_out = qs_tmp.tenspro(qs)
        return qs_out

    def evolve(self, observable=None, time=0.0, iteration=0):
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
        ob = observable.clone()
        if ob.recalc_weight() is False:
            raise ValueError("Observable is not hermitian.")

        qstate_evolve(self, observable=ob.base, time=time, iteration=iteration)
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
        ob = observable.clone()
        if ob.recalc_weight() is False:
            raise ValueError("Observable is not hermitian.")

        expect = qstate_expect_value(self, observable=ob.base)
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

    def __schmidt_decomp(self, qid_0=None, qid_1=None):

        if qid_0 is None:
            qid_0 = []
        if qid_1 is None:
            qid_1 = []

        vec = self.get_amp(qid=qid_0+qid_1)

        row = 2**len(qid_0)
        col = 2**len(qid_1)
        mat = np.zeros((row, col), dtype=complex)
        for idx, comp in enumerate(vec):
            mat[idx//col][idx%col] = comp

        U, D, V = np.linalg.svd(mat, full_matrices=False)
        coef = np.array([d for d in D if d > cfg.EPS])

        vec_0 = [v for i, v in enumerate(U.T) if i < len(coef)]
        vec_1 = [v for i, v in enumerate(V) if i < len(coef)]

        return (coef, vec_0, vec_1)

    def schmidt_decomp(self, qid_0=None, qid_1=None):
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
        qs_0 = [self.__class__(vector=v) for i, v in enumerate(vec_0) if i < len(coef)]
        qs_1 = [self.__class__(vector=v) for i, v in enumerate(vec_1) if i < len(coef)]

        return (coef, qs_0, qs_1)

    def schmidt_coef(self, qid_0=None, qid_1=None):
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
        coef = self.__schmidt_decomp(qid_0=qid_0, qid_1=qid_1)[0]
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
        qstate_operate_qgate(self, kind=cfg.PAULI_X, phase=cfg.DEF_PHASE, qid=[q0])
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
        qstate_operate_qgate(self, kind=cfg.PAULI_Y, phase=cfg.DEF_PHASE, qid=[q0])
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
        qstate_operate_qgate(self, kind=cfg.PAULI_Z, phase=cfg.DEF_PHASE, qid=[q0])
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
        qstate_operate_qgate(self, kind=cfg.ROOT_PAULI_X, phase=cfg.DEF_PHASE, qid=[q0])
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
        qstate_operate_qgate(self, kind=cfg.ROOT_PAULI_X_, phase=cfg.DEF_PHASE, qid=[q0])
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
        qstate_operate_qgate(self, kind=cfg.HADAMARD, phase=cfg.DEF_PHASE, qid=[q0])
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
        qstate_operate_qgate(self, kind=cfg.PHASE_SHIFT_S, phase=cfg.DEF_PHASE, qid=[q0])
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
        qstate_operate_qgate(self, kind=cfg.PHASE_SHIFT_S_, phase=cfg.DEF_PHASE, qid=[q0])
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
        qstate_operate_qgate(self, kind=cfg.PHASE_SHIFT_T, phase=cfg.DEF_PHASE, qid=[q0])
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
        qstate_operate_qgate(self, kind=cfg.PHASE_SHIFT_T_, phase=cfg.DEF_PHASE, qid=[q0])
        return self

    def rx(self, q0, phase=cfg.DEF_PHASE):
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
        qstate_operate_qgate(self, kind=cfg.ROTATION_X, phase=phase, qid=[q0])
        return self

    def ry(self, q0, phase=cfg.DEF_PHASE):
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
        qstate_operate_qgate(self, kind=cfg.ROTATION_Y, phase=phase, qid=[q0])
        return self

    def rz(self, q0, phase=cfg.DEF_PHASE):
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
        qstate_operate_qgate(self, kind=cfg.ROTATION_Z, phase=phase, qid=[q0])
        return self

    def p(self, q0, phase=cfg.DEF_PHASE):
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
        qstate_operate_qgate(self, kind=cfg.PHASE_SHIFT, phase=phase, qid=[q0])
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
        qstate_operate_qgate(self, kind=cfg.CONTROLLED_X, phase=cfg.DEF_PHASE, qid=[q0, q1])
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
        qstate_operate_qgate(self, kind=cfg.CONTROLLED_Y, phase=cfg.DEF_PHASE, qid=[q0, q1])
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
        qstate_operate_qgate(self, kind=cfg.CONTROLLED_Z, phase=cfg.DEF_PHASE, qid=[q0, q1])
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
        qstate_operate_qgate(self, kind=cfg.CONTROLLED_XR, phase=cfg.DEF_PHASE, qid=[q0, q1])
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
        qstate_operate_qgate(self, kind=cfg.CONTROLLED_XR_, phase=cfg.DEF_PHASE, qid=[q0, q1])
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
        qstate_operate_qgate(self, kind=cfg.CONTROLLED_H, phase=cfg.DEF_PHASE, qid=[q0, q1])
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
        qstate_operate_qgate(self, kind=cfg.CONTROLLED_S, phase=cfg.DEF_PHASE, qid=[q0, q1])
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
        qstate_operate_qgate(self, kind=cfg.CONTROLLED_S_, phase=cfg.DEF_PHASE, qid=[q0, q1])
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
        qstate_operate_qgate(self, kind=cfg.CONTROLLED_T, phase=cfg.DEF_PHASE, qid=[q0, q1])
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
        qstate_operate_qgate(self, kind=cfg.CONTROLLED_T_, phase=cfg.DEF_PHASE, qid=[q0, q1])
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
        qstate_operate_qgate(self, kind=cfg.SWAP_QUBITS, phase=cfg.DEF_PHASE, qid=[q0, q1])
        return self

    def cp(self, q0, q1, phase=cfg.DEF_PHASE):
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
        qstate_operate_qgate(self, kind=cfg.CONTROLLED_P, phase=phase, qid=[q0, q1])
        return self

    def crx(self, q0, q1, phase=cfg.DEF_PHASE):
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
        qstate_operate_qgate(self, kind=cfg.CONTROLLED_RX, phase=phase, qid=[q0, q1])
        return self

    def cry(self, q0, q1, phase=cfg.DEF_PHASE):
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
        qstate_operate_qgate(self, kind=cfg.CONTROLLED_RY, phase=phase, qid=[q0, q1])
        return self

    def crz(self, q0, q1, phase=cfg.DEF_PHASE):
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
        qstate_operate_qgate(self, kind=cfg.CONTROLLED_RZ, phase=phase, qid=[q0, q1])
        return self

    def rxx(self, q0, q1, phase=cfg.DEF_PHASE):
        """
        operate Rxx gate.

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
        qstate_operate_qgate(self, kind=cfg.ROTATION_XX, phase=phase, qid=[q0, q1])
        return self

    def ryy(self, q0, q1, phase=cfg.DEF_PHASE):
        """
        operate Ryy gate.

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
        qstate_operate_qgate(self, kind=cfg.ROTATION_YY, phase=phase, qid=[q0, q1])
        return self

    def rzz(self, q0, q1, phase=cfg.DEF_PHASE):
        """
        operate Rxx gate.

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
        qstate_operate_qgate(self, kind=cfg.ROTATION_ZZ, phase=phase, qid=[q0, q1])
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
        self.cxr(q1, q2).cx(q0, q1).cxr_dg(q1, q2).cx(q0, q1).cxr(q0, q2)
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
        self.cx(q2, q1).ccx(q0, q1, q2).cx(q2, q1)
        return self

    # other gate

    def mcx(self, qid=None):
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

    def measure(self, qid=None):
        """
        one shot measurement in Z-direction.

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.

        Returns
        -------
        mval : str
            measurement value.

        Examples
        --------
        >>> qs = QState(qubit_num=2).h(0).cx(0,1)
        >>> qs.show()
        >>> print(qs.measure(qid=[0,1]))
        >>> qs.show()
        c[00] = +0.7071+0.0000*i : 0.5000 |++++++
        c[01] = +0.0000+0.0000*i : 0.0000 |
        c[10] = +0.0000+0.0000*i : 0.0000 |
        c[11] = +0.7071+0.0000*i : 0.5000 |++++++
        00
        c[00] = +1.0000+0.0000*i : 1.0000 |+++++++++++
        c[01] = +0.0000+0.0000*i : 0.0000 |
        c[10] = +0.0000+0.0000*i : 0.0000 |
        c[11] = +0.0000+0.0000*i : 0.0000 |

        """
        mval = qstate_measure(self, qid=qid)
        return mval

    def m(self, qid=None, shots=cfg.DEF_SHOTS, angle=0.0, phase=0.0):
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
        md = qstate_measure_stats(self, qid=qid, shots=shots,
                                  angle=angle, phase=phase)
        return md

    def mx(self, qid=None, shots=cfg.DEF_SHOTS):
        """
        X-axis measurement.

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.
        shots : int, default 1
            number of measurements.

        Returns
        -------
        md : instance of MData
            measurement data.

        See Also
        --------
        MData class (MData.py)

        """
        md = qstate_measure_stats(self, qid=qid, shots=shots,
                                  angle=0.5, phase=0.0)
        return md

    def my(self, qid=None, shots=cfg.DEF_SHOTS):
        """
        Y-axis measurement.

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.
        shots : int, default 1
            number of measurements.

        Returns
        -------
        md : instance of MData
            measurement data.

        See Also
        --------
        MData class (MData.py)

        """
        md = qstate_measure_stats(self, qid=qid, shots=shots,
                                  angle=0.5, phase=0.5)
        return md

    def mz(self, qid=None, shots=cfg.DEF_SHOTS):
        """
        Z-axis measurement.

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.
        shots : int, default 1
            number of measurements.

        Returns
        -------
        md : instance of MData
            measurement data.

        See Also
        --------
        MData class (MData.py)

        """
        md = qstate_measure_stats(self, qid=qid, shots=shots,
                                  angle=0.0, phase=0.0)
        return md

    def mb(self, qid=None, shots=cfg.DEF_SHOTS):
        """ bell measurement """
        return qstate_measure_bell_stats(self, qid=qid, shots=shots)

    def operate(self, pp=None, ctrl=None):
        """
        operate unitary operator to quantum state.

        Parameters
        ----------
        pp : instance of PauliProduct
            pauli product to operate
        ctrl : int
            contoroll qubit id for controlled pauli product

        Returns
        -------
        self : instance of QState
            quantum state after operation

        """
        pauli_list = pp.pauli_list
        qid = pp.qid
        factor = pp.factor

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

            if factor == -1.+0.j:
                self.z(ctrl)
            elif factor == 0.+1.j:
                self.s(ctrl)
            elif factor == 0.-1.j:
                self.s_dg(ctrl)

        return self

    def __del__(self):

        qstate_free(self)

# c-library for qstate
from qlazy.lib.qstate_c import (qstate_init, qstate_init_with_vector, qstate_reset,
                                qstate_print, qstate_copy, qstate_bloch,
                                qstate_inner_product, qstate_get_camp,
                                qstate_tensor_product, qstate_evolve, qstate_expect_value,
                                qstate_apply_matrix, qstate_operate_qgate, qstate_measure,
                                qstate_measure_stats, qstate_measure_bell_stats, qstate_free)
