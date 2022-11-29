# -*- coding: utf-8 -*-
""" Stabilizer State """
import ctypes
import random
from collections import Counter

import qlazy.config as cfg
from qlazy.util import is_clifford_gate, get_qgate_qubit_num
from qlazy.QObject import QObject

class MDataStabilizer:
    """ Measured Data for Stabilizer

    Attributes
    ----------
    frequency : Counter
        frequencies of measured value.
    last : str
        last measured value.
    qid : list of int
        qubit id's list.
    qubit_num : int
        qubit number of the quantum state (= log(state_num)).

    """

    def __init__(self, frequency=None, last=None, qid=None, qubit_num=0):

        self.frequency = frequency
        self.last = last
        self.qid = qid
        self.qubit_num = qubit_num

class Stabilizer(ctypes.Structure, QObject):
    """ Stabilizer State

    Attributes
    ----------
    qubit_num : int
        number of qubits.
    gene_num : int
        number of generators.
    """

    _fields_ = [
        ('gene_num', ctypes.c_int),
        ('qubit_num', ctypes.c_int),
        ('pauli_factor', ctypes.c_void_p),
        ('check_matrix', ctypes.c_void_p),
    ]

    def __new__(cls, qubit_num=None, gene_num=None, pp_list=None, seed=None, **kwargs):
        """
        Parameters
        ----------
        gene_num : int
            number of generators.
        qubit_num : int
            number of qubit.

        Notes
        -----
        You must specify 'qubit_num'. If 'gene_num' is not specified,
        'gene_num' is equal to 'qubit_num.'

        """
        if seed is None:
            seed = random.randint(0, 1000000)

        if pp_list is not None:
            gene_num = len(pp_list)
            qubit_num = 0
            for pp in pp_list:
                qubit_num = max([qubit_num] + pp.qid)
            qubit_num += 1
            obj = stabilizer_init(gene_num, qubit_num, seed)
            sb = ctypes.cast(obj.value, ctypes.POINTER(cls)).contents
            for i, pp in enumerate(pp_list):
                for j, q in enumerate(pp.qid):
                    sb.set_pauli_op(i, q, pp.pauli_list[j])

        else:
            if qubit_num is None:
                raise ValueError("qubit number must be set.")
            if gene_num is None:
                gene_num = qubit_num
            if qubit_num < 1 or gene_num < 1:
                raise ValueError("qubit_num and gene_num must be positive integer.")
            obj = stabilizer_init(gene_num, qubit_num, seed)
            sb = ctypes.cast(obj.value, ctypes.POINTER(cls)).contents

        return sb

    def __str__(self):

        return self.get_str()

    @classmethod
    def add_method(cls, method):
        """
        add method (custum gate).

        Parameters
        ----------
        method : func
            method (custum gate) to add.

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

        """
        for method in methods:
            if callable(method):
                setattr(cls, method.__name__, method)
            else:
                raise ValueError("can't add method.")

    def get_str(self):
        """ get string of the stabilzer """

        str_out = ""
        for i in range(self.gene_num):
            pauli_fac_complex = self.get_pauli_fac(i)

            gene_str = ""
            for j in range(self.qubit_num):
                s = self.get_pauli_op(i, j)
                gene_str += s

            if pauli_fac_complex == 1+0j:
                pauli_fac_str = "  "
            elif pauli_fac_complex == 1j:
                pauli_fac_str = " i"
            elif pauli_fac_complex == -1+0j:
                pauli_fac_str = " -"
            elif pauli_fac_complex == -1j:
                pauli_fac_str = "-i"
            else:
                raise ValueError("can't get string.")

            str_out += "{0:}{1:}\n".format(pauli_fac_str, gene_str)

        return str_out

    def show(self):
        """
        show the generators of stabilizer.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        digits = len(str(self.gene_num - 1))
        s = self.get_str()
        gene_list = s.rstrip().split('\n')
        for i, gene_str in enumerate(gene_list):
            print("g[{0:{digits}d}]:{1:}".format(i, gene_str, digits=digits))

    def clone(self):
        """
        get the copy of the quantum state.

        Parameters
        ----------
        None

        Returns
        -------
        stab : instance of Stabilizer
            copy of the original stabilizer.

        """
        obj = stabilizer_copy(self)
        sb = ctypes.cast(obj.value, ctypes.POINTER(self.__class__)).contents
        return sb

    def get_rank(self):
        """ get rank of the stabilizer """

        rank = stabilizer_get_rank(self)
        return rank

    def set_all(self, pauli_op_str):
        """
        set all of the qubits same pauli operators.

        Parameters
        ----------
        pauli_op_str : str
            string of pauli operator ('X','Y','Z').

        Returns
        -------
        self : instance of Stabilizer

        Examples
        --------
        >>> sb = Stabilizer(qubit_num=3)
        >>> sb.set_all('Z')
        >>> sb.show()
        g[0]:  ZII
        g[1]:  IZI
        g[2]:  IIZ

        """
        self.reset()
        length = min(self.gene_num, self.qubit_num)
        [self.set_pauli_op(i, i, pauli_op_str) for i in range(length)]
        return self

    def set_pauli_fac(self, gene_id, pauli_fac_str):
        """
        set pauli factor of generator ('+1','-1','+i','-i').

        Parameters
        ----------
        gene_id : int
            generator id to set.

        Returns
        -------
        self : instance of Stabilizer

        """
        if pauli_fac_str in ("+1", "1"):
            pauli_fac = cfg.REAL_PLUS
        elif pauli_fac_str == "+i":
            pauli_fac = cfg.IMAG_PLUS
        elif pauli_fac_str == "-1":
            pauli_fac = cfg.REAL_MINUS
        elif pauli_fac_str == "-i":
            pauli_fac = cfg.IMAG_MINUS
        else:
            raise ValueError("can't set pauli factor.")

        stabilizer_set_pauli_fac(self, gene_id, pauli_fac)

        return self

    def get_pauli_fac(self, gene_id):
        """
        get pauli factor of generator ('+1','-1','+i','-i').

        Parameters
        ----------
        gene_id : int
            generator id to get.

        Returns
        -------
        pauli_fac_complex : complex
            complex facto of the generator (1+0j, 1j, -1+0j, -1j)

        """
        pauli_fac = stabilizer_get_pauli_fac(self, gene_id)

        if pauli_fac == cfg.REAL_PLUS:
            pauli_fac_complex = 1+0j
        elif pauli_fac == cfg.IMAG_PLUS:
            pauli_fac_complex = 1j
        elif pauli_fac == cfg.REAL_MINUS:
            pauli_fac_complex = -1+0j
        elif pauli_fac == cfg.IMAG_MINUS:
            pauli_fac_complex = -1j
        else:
            raise ValueError("can't get pauli factor.")

        return pauli_fac_complex

    def set_pauli_op(self, gene_id, qubit_id, pauli_op_str):
        """
        set pauli operator ('I','X','Y','Z').

        Parameters
        ----------
        gene_id : int
            generator id to set.
        qubit_id : int
            qubit id to set.

        Returns
        -------
        self : instance of Stabilizer

        """
        if pauli_op_str == 'X':
            pauli_op = cfg.PAULI_X
        elif pauli_op_str == 'Y':
            pauli_op = cfg.PAULI_Y
        elif pauli_op_str == 'Z':
            pauli_op = cfg.PAULI_Z
        elif pauli_op_str == 'I':
            pauli_op = cfg.IDENTITY
        else:
            raise ValueError("can't set pauli operator.")

        stabilizer_set_pauli_op(self, gene_id, qubit_id, pauli_op)

        return self

    def get_pauli_op(self, gene_id, qubit_id):
        """
        get pauli operator ('I','X','Y','Z').

        Parameters
        ----------
        gene_id : int
            generator id to get.
        qubit_id : int
            qubit id to get.

        Returns
        -------
        pauli_op_str : str
            pauli operator ('I','X','Y','Z')

        """
        pauli_op = stabilizer_get_pauli_op(self, gene_id, qubit_id)

        if pauli_op == cfg.PAULI_X:
            pauli_op_str = 'X'
        elif pauli_op == cfg.PAULI_Y:
            pauli_op_str = 'Y'
        elif pauli_op == cfg.PAULI_Z:
            pauli_op_str = 'Z'
        elif pauli_op == cfg.IDENTITY:
            pauli_op_str = 'I'
        else:
            raise ValueError("can't get pauli operator.")

        return pauli_op_str

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
        >>> sb = Stabilizer(qubit_num=2).set_all('Z').h(0).cx(0,1)
        >>> sb.show()
        >>> print(sb.measure(qid=[0,1]))
        >>> sb.show()
        g[0]:  XX
        g[1]:  ZZ
        00
        g[0]:  ZI
        g[1]:  ZZ

        """
        mval = self.m(qid=qid, shots=1).last
        return mval

    def m(self, qid=None, shots=cfg.DEF_SHOTS):
        """
        measurement in Z-direction.

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.
        shots : int, default 1
            number of measurements.

        Returns
        -------
        md : instance of MDataStabilizer
            measurement data.

        Examples
        --------
        >>> sb = Stabilizer(qubit_num=2).set_all('Z').h(0).cx(0,1)
        >>> md = qs.m(qid=[0,1], shots=100)
        >>> print(md.freauency)
        >>> print(md.last)
        Counter({'00':55,'11':45})
        11

        See Also
        --------
        MDataStabilizer class

        """
        md = self.mz(qid=qid, shots=shots)
        return md

    def mx(self, qid=None, shots=cfg.DEF_SHOTS):
        """
        measurement in X-direction.

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.
        shots : int, default 1
            number of measurements.

        Returns
        -------
        md : instance of MDataStabilizer
            measurement data.

        """
        [self.h(q) for q in qid]
        md = self.mz(qid=qid, shots=shots)
        [self.h(q) for q in qid]
        return md

    def my(self, qid=None, shots=cfg.DEF_SHOTS):
        """
        measurement in Y-direction.

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.
        shots : int, default 1
            number of measurements.

        Returns
        -------
        md : instance of MDataStabilizer
            measurement data.

        """

        [self.s_dg(q).h(q) for q in qid]
        md = self.mz(qid=qid, shots=shots)
        [self.h(q).s(q) for q in qid]
        return md

    def mz(self, qid=None, shots=cfg.DEF_SHOTS):
        """
        measurement in Z-direction.

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.
        shots : int, default 1
            number of measurements.

        Returns
        -------
        md : instance of MDataStabilizer
            measurement data.

        Examples
        --------
        >>> sb = Stabilizer(2).set_all('Z').h(0).cx(0,1)
        >>> md = qs.mz(qid=[0,1], shots=100)
        >>> print(md.freauency)
        >>> print(md.last)
        Counter({'00':55,'11':45})
        11

        See Also
        --------
        MDataStabilizer class

        """
        frequency = Counter()

        # 1st to last-1 measurement
        for _ in range(shots-1):
            st = self.clone()
            mval_str = ''
            for q in qid:
                mval = stabilizer_measure(st, q)
                mval_str += str(mval)
            frequency += {mval_str:1}

        # last measurement
        mval_str = ''
        for q in qid:
            m = stabilizer_measure(self, q)
            mval_str += str(m)
        frequency += {mval_str:1}
        last = mval_str

        md = MDataStabilizer(frequency=frequency, last=last, qid=qid,
                             qubit_num=self.qubit_num)

        return md

    @classmethod
    def del_all(cls, *stabs):
        """
        free memory of the all stabilizer.

        Parameters
        ----------
        stabs : instance of Stabilizer,instance of Stabilizer,...
            set of Stabilizer instances

        Returns
        -------
        None

        """
        for sb in stabs:
            if isinstance(sb, (list, tuple)):
                cls.del_all(*sb)
            elif isinstance(sb, cls):
                del sb
            else:
                raise ValueError("can't free stabilizer.")

    def operate(self, pp=None, ctrl=None, qctrl=None):
        """
        operate unitary operator to stabilizer.

        Parameters
        ----------
        pp : instance of PauliProduct
            pauli product to operate
        ctrl : int
            contoroll qubit id for controlled pauli product
            (this option will be removed near future)
        qctrl : int
            contoroll qubit id for controlled pauli product

        Returns
        -------
        self : instance of Stabilizer
            stabilizer after operation

        """
        pauli_list = pp.pauli_list
        qid = pp.qid
        factor = pp.factor

        if ctrl is None:
            ctrl = qctrl

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

    # operate gate

    def operate_gate(self, kind=None, qid=None, **kwargs):
        """
        operate gate

        Parameters
        ----------
        kind : int
            kind of the gate
        qid : list
            quantum id list

        Returns
        -------
        self : instance of QState
            quantum state

        """
        if kind == cfg.RESET:
            if qid is not None:
                raise ValueError("qid is not supported.")
            for i in range(self.gene_num):
                for j in range(self.qubit_num):
                    self.set_pauli_op(i, j, 'I')
                self.set_pauli_fac(i, '+1')
        elif kind == cfg.CONTROLLED_Y:
            q0, q1 = qid[0], qid[1]
            self.cz(q0, q1).cx(q0, q1).s(q0)
        elif is_clifford_gate(kind):
            if get_qgate_qubit_num(kind) == 1:
                q0 = qid[0]
                stabilizer_operate_qgate(self, kind, q0, 0)
            elif get_qgate_qubit_num(kind) == 2:
                q0, q1 = qid[0], qid[1]
                stabilizer_operate_qgate(self, kind, q0, q1)
            else:
                raise ValueError("length of qid must be 1 or 2.")
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
        qs : instance of QState
            quantum state after executing the quantum circuit

        Notes
        -----
        The quantum circut must be clifford.

        """
        if qcirc.is_clifford() is False:
            raise ValueError("qcirc must be clifford quantum circuit.")
        if self.qubit_num < qcirc.qubit_num:
            raise ValueError("qubit number of quantum state must be equal or larger than the quantum circuit size.")

        if qctrl is None:
            stabilizer_operate_qcirc(self, cmem=None, qcirc=qcirc, shots=1, cid=None)
        else:
            qc_qctrl = qcirc.add_control(qctrl=qctrl)
            stabilizer_operate_qcirc(self, cmem=None, qcirc=qc_qctrl, shots=1, cid=None)

        return self

    def __del__(self):

        stabilizer_free(self)

# c-library for stabilizer
from qlazy.lib.stabilizer_c import (stabilizer_init, stabilizer_copy,
                                    stabilizer_set_pauli_fac, stabilizer_get_pauli_fac,
                                    stabilizer_set_pauli_op, stabilizer_get_pauli_op,
                                    stabilizer_operate_qgate, stabilizer_get_rank,
                                    stabilizer_measure, stabilizer_operate_qcirc,
                                    stabilizer_free)
