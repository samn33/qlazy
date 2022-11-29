# -*- coding: utf-8 -*-
""" Quantum State """
import ctypes
import random
import numpy as np

import qlazy.config as cfg
from qlazy.gpu import is_gpu_supported_lib
from qlazy.util import is_unitary_gate
from qlazy.QObject import QObject

class QState(ctypes.Structure, QObject):
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

        if self.qubit_num < ob.qubit_num:
            raise ValueError("total qubit number of the observable must be less than qstate's.")

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

    # operate gate

    def operate_gate(self, kind=None, qid=None, phase=0.0, **kwargs):
        """
        operate gate

        Parameters
        ----------
        kind : int
            kind of the gate
        qid : list
            quantum id list
        phase : float
            phase for rotation gate

        Returns
        -------
        self : instance of QState
            quantum state

        """
        if kind == cfg.RESET:
            qstate_reset(self, qid=qid)
        elif is_unitary_gate(kind):
            qstate_operate_qgate(self, kind=kind, qid=qid, phase=phase)
        else:
            raise ValueError("gate: {} is not supported.".format(cfg.GATE_STRING[kind]))
        return self

    # operate quantum circuit

    def operate_qcirc(self, qcirc, qctrl=None):
        """
        operate quantum circuit

        Parameters
        ----------
        qcirc : instance of QCirc
            quantum circuit
        qctrl : int
            control qubit id

        Returns
        -------
        self : instance of QState
            quantum state after executing the quantum circuit

        Notes
        -----
        The quantum circut must be unintary.

        """
        if qcirc.is_unitary() is False:
            raise ValueError("qcirc must be unitary quantum circuit.")
        if self.qubit_num < qcirc.qubit_num:
            raise ValueError("qubit number of quantum state must be equal or larger than the quantum circuit size.")

        if qctrl is None:
            qstate_operate_qcirc(self, cmem=None, qcirc=qcirc, shots=1, cid=None, out_state=True)
        else:
            qc_qctrl = qcirc.add_control(qctrl=qctrl)
            qstate_operate_qcirc(self, cmem=None, qcirc=qc_qctrl, shots=1, cid=None, out_state=True)

        return self

    def __del__(self):

        qstate_free(self)

# c-library for qstate
from qlazy.lib.qstate_c import (qstate_init, qstate_init_with_vector, qstate_reset,
                                qstate_print, qstate_copy, qstate_bloch,
                                qstate_inner_product, qstate_get_camp,
                                qstate_tensor_product, qstate_evolve, qstate_expect_value,
                                qstate_apply_matrix, qstate_operate_qgate, qstate_measure,
                                qstate_measure_stats, qstate_measure_bell_stats, qstate_operate_qcirc,
                                qstate_free)
