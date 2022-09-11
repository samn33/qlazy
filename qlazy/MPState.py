# -*- coding: utf-8 -*-
""" Matrix Product State """

import random
import numpy as np
from collections import Counter
import copy

import tensornetwork as tn
from tensornetwork import FiniteMPS

import qlazy.config as cfg

def gray_code(n):
    """ gray code generator (for mcx method) """

    for k in range(2**n):
        yield k^(k>>1)

class MDataMPState:
    """ Measured Data for MPState

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


class MPState(FiniteMPS):
    """ Matrix Product State

    Attributes
    ----------
    qubit_num : int
        number of qubits (number of nodes)
    bond_dimensions : list (int)
        list of bond dimensions
    max_truncation_err : float
        maximum of truncation error
    tensors : list (np.ndarray)
        list of 3-rank tensors for the matrix product
    
    """
    def __init__(self, qubit_num=0, bits_str=None, tensors=None, max_truncation_err=cfg.EPS,
                 **kwargs):
        """
        Parameters
        ----------
        qubit_num : int
            qubit number of the quantum state.
        bits_str : str
            string of initial quantum state.
            ex) set '0011' if initial quantum state is |0011>
        tensors : list (numpy.ndarray)
            list of 3-rank tensors for the matrix product
        max_truncation_err : float
            maximum of truncation error

        Notes
        -----
        You must specify either 'qubit_num' or 'tensors', not both.

        """
        if qubit_num == 0 and tensors is None:
            raise ValueError("qubit_num or tensors must be specified.")

        if qubit_num == 0:
            qubit_num = len(tensors)

        if bits_str is None:
            bits_str = '0' * qubit_num
        bits_list = list(map(int, list(bits_str)))
        if len(bits_list) != qubit_num:
            raise ValueError("length of bits_str must be equal to the qubit_num.")

        if tensors is None:
            bond_dim = 1
            if qubit_num == 1:
                tensors = [np.zeros((1, 2, 1), dtype=complex)]
            else:
                tensors = [np.zeros((1, 2, bond_dim), dtype=complex)] + [
                    np.zeros((bond_dim, 2, bond_dim), dtype=complex) for _ in range(qubit_num - 2)
                ] + [np.zeros((bond_dim, 2, 1), dtype=complex)]
            for i, t in enumerate(tensors):
                t[0, bits_list[i], 0] = 1

        center_position = 0
        canonicalize = True
        super().__init__(tensors=tensors, center_position=center_position, canonicalize=canonicalize)

        self.__qubit_num = qubit_num
        self.__max_truncation_err = max_truncation_err

    @property
    def qubit_num(self):
        return self.__qubit_num

    @property
    def max_truncation_err(self):
        return self.__max_truncation_err

    def __str__(self):

        s = ""
        s += "== attributes ==\n"
        s += "qubit_num           = {}\n".format(self.qubit_num)
        s += "bond_dimensions     = {}\n".format(self.bond_dimensions)
        s += "max_truncation_err  = {}\n".format(self.max_truncation_err)

        for n, tensor in enumerate(self.tensors):
            s += "\n== qubit id = {} (row:{}, column:{}) ==\n".format(n, tensor.shape[0], tensor.shape[2])
            for i in range(tensor.shape[1]):
                s += "- matrix for |{}>:\n".format(i)
                mat = []
                for j in range(tensor.shape[0]):
                    row = [tensor[j][i][k] for k in range(tensor.shape[2])]
                    mat.append(row)
                s += "{}\n".format(np.array(mat))

        return s
            
    @classmethod
    def del_all(cls, *mpstates):
        """
        free memory of the all matrix product states.

        Parameters
        ----------
        mpstates : instance of MPState,instance of MPState,...
            set of MPState instances

        Returns
        -------
        None

        """
        for mps in mpstates:
            if isinstance(mps, (list, tuple)):
                cls.del_all(*mps)
            elif isinstance(mps, cls):
                del mps
            else:
                raise ValueError("can't free mpstate.")

    def clone(self):
        """
        get the copy of the matrix product state.

        Parameters
        ----------
        None

        Returns
        -------
        mps : instance of MPState
            copy of the original matrix product state.

        """
        mps = copy.deepcopy(self)
        return mps

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
        >>> mps = MPState(qubit_num=2).h(0).cx(0,1)
        >>> mps.show()
        c[00] = +0.7071+0.0000*i : 0.5000 |++++++
        c[01] = +0.0000+0.0000*i : 0.0000 |
        c[10] = +0.0000+0.0000*i : 0.0000 |
        c[11] = +0.7071+0.0000*i : 0.5000 |++++++
        ...
        >>> mps.show(qid=[0])
        c[0] = +1.0000+0.0000*i : 1.0000 |+++++++++++
        c[1] = +0.0000+0.0000*i : 0.0000 |
        ...
        >>> mps.show(nonzero=True)
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
        if qid is None or qid == []:

            mps = self.clone()
            mps.canonicalize(normalize=True)
            [mps.position(site=i, max_truncation_err=cfg.EPS) for i in range(self.qubit_num)]
            
            node_list = []
            for tensor in mps.tensors:
                node_list.append(tn.Node(tensor))

            for i in range(len(node_list) - 1):
                node_L = node_list[i]
                node_R = node_list[i + 1]
                node_L[2] ^ node_R[0]

            result = None
            for i in range(len(node_list)):
                if result is None:
                    result = node_list[i]
                else:
                    result = result @ node_list[i]

            statevec = result.tensor.flatten()
            norm = np.vdot(statevec, statevec)
            statevec = statevec / np.sqrt(norm)

        else:

            mps = self.__reset_others(qid=qid)
            mps.canonicalize(normalize=True)
            [mps.position(site=i, max_truncation_err=cfg.EPS) for i in range(self.qubit_num)]

            vec = []
            for i in range(2**len(qid)):
                bits_list = [0] * self.qubit_num
                bits_list_part = list("{:0{digits}b}".format(i, 'b', digits=len(qid)))
                for j, q in enumerate(qid):
                    bits_list[q] = bits_list_part[j]
                mps_ref = self.__class__(qubit_num=self.__qubit_num,
                                         bits_str="".join(map(str, bits_list)))
                vec.append(mps_ref.inpro(mps, qid=qid))
                statevec = np.array(vec)
        
        return statevec

    def __inner_product(self, mps):

        self.canonicalize(normalize=True)
        mps.canonicalize(normalize=True)

        node_list_A = [tn.Node(np.conj(tensor), f'A{i}') for i, tensor in enumerate(self.tensors)]
        node_list_B = [tn.Node(tensor, f'B{i}') for i, tensor in enumerate(mps.tensors)]
        node_list_A[0][0] ^ node_list_B[0][0]
        node_list_A[-1][2] ^ node_list_B[-1][2]
        [node_list_A[k][2] ^ node_list_A[k + 1][0] for k in range(self.__qubit_num - 1)]
        [node_list_B[k][2] ^ node_list_B[k + 1][0] for k in range(self.__qubit_num - 1)]
        [node_list_A[k][1] ^ node_list_B[k][1] for k in range(self.__qubit_num)]
        result = node_list_A[0] @ node_list_B[0]
        for i in range(1, self.__qubit_num):
            result = result @ node_list_A[i] @ node_list_B[i]
        tensor = result.tensor
        inp = complex(tensor.real, tensor.imag)

        return inp

    def __reset_others(self, qid=[]):

        if max(qid) > self.__qubit_num - 1:
            raise ValueError("maximum of qid must be smaller than qubit_num - 1.")
        elif min(qid) < 0:
            raise ValueError("minimum of qid must be larger than zero.")
        elif len(set(qid)) != len(qid):
            raise ValueError("duplicate qid.")

        mps = self.clone()
        if len(qid) != self.__qubit_num:
            qid_others = [q for q in range(self.__qubit_num) if q not in qid]
            mps.reset(qid=qid_others)
        return mps
        
    def inpro(self, mps, qid=None):
        """
        get the inner product with matrix product state.

        Parameters
        ----------
        mps : instance of MPState
            one of the two matrix product state.
        qid : list of int, default - list of all of the qubit id
            qubit id's list.

        Returns
        -------
        inp : complex
            inner produt (<self|mps>).

        Notes
        -----
        If 'qid' is set, you can get the inner product for partial
        quantum state. If the specified quantum system are entangled
        with the remaining system, output value is probabilistic,
        while original quantum states do not change.

        """
        if qid == [] or qid is None:
            inp = self.__inner_product(mps)
        else:
            mps_0 = self.__reset_others(qid=qid)
            mps_1 = mps.__reset_others(qid=qid)
            inp = mps_0.__inner_product(mps_1)
        return inp

    def fidelity(self, mps, qid=None):
        """
        get fidelity with the matrix product state.

        Parameters
        ----------
        mps : instance of MPState
            one of the two matrix product states.
        qid : list of int
            qubit id's list.

        Returns
        -------
        fid : float
            fidelity of the two matrix product states. absolute value of the
            inner product of two matrix product states.

        Notes
        -----
        If 'qid' is set, you can get the fidelity for partial quantum
        state. If the specified quantum system are entangled with the
        remaining system, output value is probabilistic, while
        original quantum states do not change.

        """
        return abs(self.inpro(mps, qid=qid))

    def __get_gate_array(self, gate_str, para=0.0):

        phase = para * np.pi
        
        if gate_str == 'x':
            gate_array = np.zeros((2, 2), dtype=complex)
            gate_array[0][1], gate_array[1][0] = 1.+0.j, 1.+0.j
        elif gate_str == 'y':
            gate_array = np.zeros((2, 2), dtype=complex)
            gate_array[0][1], gate_array[1][0] = -1.j, 1.j
        elif gate_str == 'z':
            gate_array = np.diag([1.+0.j, -1.+0.j])
        elif gate_str == 'xr':
            gate_array = np.zeros((2, 2), dtype=complex)
            gate_array[0][0] = (1.+1.j) / 2.0
            gate_array[0][1] = (1.-1.j) / 2.0
            gate_array[1][0] = (1.-1.j) / 2.0
            gate_array[1][1] = (1.+1.j) / 2.0
        elif gate_str == 'xr_dg':
            gate_array = np.zeros((2, 2), dtype=complex)
            gate_array[0][0] = (1.-1.j) / 2.0
            gate_array[0][1] = (1.+1.j) / 2.0
            gate_array[1][0] = (1.+1.j) / 2.0
            gate_array[1][1] = (1.-1.j) / 2.0
        elif gate_str == 'h':
            gate_array = np.array([[1.+0.j, 1.+0.j], [1.+0.j, -1.+0.j]]) / np.sqrt(2.0)
        elif gate_str == 's':
            gate_array = np.zeros((2, 2), dtype=complex)
            gate_array[0][0], gate_array[1][1] = 1.+0.j, 1.j
        elif gate_str == 's_dg':
            gate_array = np.zeros((2, 2), dtype=complex)
            gate_array[0][0], gate_array[1][1] = 1.+0.j, -1.j
        elif gate_str == 't':
            gate_array = np.zeros((2, 2), dtype=complex)
            gate_array[0][0], gate_array[1][1] = 1.+0.j, (1.+1.j)/np.sqrt(2.0)
        elif gate_str == 't_dg':
            gate_array = np.zeros((2, 2), dtype=complex)
            gate_array[0][0], gate_array[1][1] = 1.+0.j, (1.-1.j)/np.sqrt(2.0)
        elif gate_str == 'p':
            gate_array = np.zeros((2, 2), dtype=complex)
            gate_array[0][0] = 1.+0.j
            gate_array[1][1] = np.exp(phase * 1.j)
        elif gate_str == 'rx':
            gate_array = np.zeros((2, 2), dtype=complex)
            gate_array[0][0] = np.cos(phase / 2.0)
            gate_array[0][1] = -1.j * np.sin(phase / 2.0)
            gate_array[1][0] = -1.j * np.sin(phase / 2.0)
            gate_array[1][1] = np.cos(phase / 2.0)
        elif gate_str == 'ry':
            gate_array = np.zeros((2, 2), dtype=complex)
            gate_array[0][0] = np.cos(phase / 2.0)
            gate_array[0][1] = -np.sin(phase / 2.0)
            gate_array[1][0] = np.sin(phase / 2.0)
            gate_array[1][1] = np.cos(phase / 2.0)
        elif gate_str == 'rz':
            gate_array = np.zeros((2, 2), dtype=complex)
            gate_array[0][0] = np.exp(-1.j * phase / 2.0)
            gate_array[0][1] = 0.+0.j
            gate_array[1][0] = 0.+0.j
            gate_array[1][1] = np.exp(1.j * phase / 2.0)
        elif gate_str == 'cx':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = 1.+0.j
            gate_array[0][1][0][1] = 1.+0.j
            gate_array[1][0][1][1] = 1.+0.j
            gate_array[1][1][1][0] = 1.+0.j
        elif gate_str == 'cy':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = 1.+0.j
            gate_array[0][1][0][1] = 1.+0.j
            gate_array[1][0][1][1] = -1.j
            gate_array[1][1][1][0] = 1.j
        elif gate_str == 'cz':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = 1.+0.j
            gate_array[0][1][0][1] = 1.+0.j
            gate_array[1][0][1][0] = 1.+0.j
            gate_array[1][1][1][1] = -1.+0.j
        elif gate_str == 'cxr':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = 1.+0.j
            gate_array[0][1][0][1] = 1.+0.j
            gate_array[1][0][1][0] = (1.+1.j) / 2.0
            gate_array[1][0][1][1] = (1.-1.j) / 2.0
            gate_array[1][1][1][0] = (1.-1.j) / 2.0
            gate_array[1][1][1][1] = (1.+1.j) / 2.0
        elif gate_str == 'cxr_dg':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = 1.+0.j
            gate_array[0][1][0][1] = 1.+0.j
            gate_array[1][0][1][0] = (1.-1.j) / 2.0
            gate_array[1][0][1][1] = (1.+1.j) / 2.0
            gate_array[1][1][1][0] = (1.+1.j) / 2.0
            gate_array[1][1][1][1] = (1.-1.j) / 2.0
        elif gate_str == 'ch':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = 1.+0.j
            gate_array[0][1][0][1] = 1.+0.j
            gate_array[1][0][1][0] = (1.+0.j)/np.sqrt(2.0)
            gate_array[1][0][1][1] = (1.+0.j)/np.sqrt(2.0)
            gate_array[1][1][1][0] = (1.+0.j)/np.sqrt(2.0)
            gate_array[1][1][1][1] = (-1.+0.j)/np.sqrt(2.0)
        elif gate_str == 'cs':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = 1.+0.j
            gate_array[0][1][0][1] = 1.+0.j
            gate_array[1][0][1][0] = 1.+0.j
            gate_array[1][1][1][1] = 1.j
        elif gate_str == 'cs_dg':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = 1.+0.j
            gate_array[0][1][0][1] = 1.+0.j
            gate_array[1][0][1][0] = 1.+0.j
            gate_array[1][1][1][1] = -1.j
        elif gate_str == 'ct':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = 1.+0.j
            gate_array[0][1][0][1] = 1.+0.j
            gate_array[1][0][1][0] = 1.+0.j
            gate_array[1][1][1][1] = (1.+1.j)/np.sqrt(2.0)
        elif gate_str == 'ct_dg':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = 1.+0.j
            gate_array[0][1][0][1] = 1.+0.j
            gate_array[1][0][1][0] = 1.+0.j
            gate_array[1][1][1][1] = (1.-1.j)/np.sqrt(2.0)
        elif gate_str == 'cp':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = 1.+0.j
            gate_array[0][1][0][1] = 1.+0.j
            gate_array[1][0][1][0] = 1.+0.j
            gate_array[1][1][1][1] = np.exp(1.j * phase)
        elif gate_str == 'crx':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = 1.+0.j
            gate_array[0][1][0][1] = 1.+0.j
            gate_array[1][0][1][0] = np.cos(phase / 2.0)
            gate_array[1][0][1][1] = -1.j * np.sin(phase / 2.0)
            gate_array[1][1][1][0] = -1.j * np.sin(phase / 2.0)
            gate_array[1][1][1][1] = np.cos(phase / 2.0)
        elif gate_str == 'cry':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = 1.+0.j
            gate_array[0][1][0][1] = 1.+0.j
            gate_array[1][0][1][0] = np.cos(phase / 2.0)
            gate_array[1][0][1][1] = -np.sin(phase / 2.0)
            gate_array[1][1][1][0] = np.sin(phase / 2.0)
            gate_array[1][1][1][1] = np.cos(phase / 2.0)
        elif gate_str == 'crz':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = 1.+0.j
            gate_array[0][1][0][1] = 1.+0.j
            gate_array[1][0][1][0] = np.exp(-1.j * phase / 2.0)
            gate_array[1][1][1][1] = np.exp(1.j * phase / 2.0)
        elif gate_str == 'sw':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = 1.+0.j
            gate_array[0][1][1][0] = 1.+0.j
            gate_array[1][0][0][1] = 1.+0.j
            gate_array[1][1][1][1] = 1.+0.j
        elif gate_str == 'rxx':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = np.cos(phase / 2.0)
            gate_array[0][1][0][1] = np.cos(phase / 2.0)
            gate_array[1][0][1][0] = np.cos(phase / 2.0)
            gate_array[1][1][1][1] = np.cos(phase / 2.0)
            gate_array[0][0][1][1] = -1.j * np.sin(phase / 2.0)
            gate_array[0][1][1][0] = -1.j * np.sin(phase / 2.0)
            gate_array[1][0][0][1] = -1.j * np.sin(phase / 2.0)
            gate_array[1][1][0][0] = -1.j * np.sin(phase / 2.0)
        elif gate_str == 'ryy':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = np.cos(phase / 2.0)
            gate_array[0][1][0][1] = np.cos(phase / 2.0)
            gate_array[1][0][1][0] = np.cos(phase / 2.0)
            gate_array[1][1][1][1] = np.cos(phase / 2.0)
            gate_array[0][0][1][1] = 1.j * np.sin(phase / 2.0)
            gate_array[0][1][1][0] = -1.j * np.sin(phase / 2.0)
            gate_array[1][0][0][1] = -1.j * np.sin(phase / 2.0)
            gate_array[1][1][0][0] = 1.j * np.sin(phase / 2.0)
        elif gate_str == 'rzz':
            gate_array = np.zeros((2, 2, 2, 2), dtype=complex)
            gate_array[0][0][0][0] = np.exp(-1.j * phase / 2.0)
            gate_array[0][1][0][1] = np.exp(1.j * phase / 2.0)
            gate_array[1][0][1][0] = np.exp(1.j * phase / 2.0)
            gate_array[1][1][1][1] = np.exp(-1.j * phase / 2.0)

        return gate_array

    def operate_1qubit_gate(self, gate_str, q, para=0.0):
        """
        operate 1-qubit gate.

        Parameters
        ----------
        gate_str : str
            gate stiring (ex. 'x','y','z','h','s', ..)
        q0 : int
            qubit id.
        para : float
            angle for rotation gate (unit of angle is PI radian).

        Returns
        -------
        self : instance of MPState

        """
        if gate_str == 'i':
            return self
        gate_array = self.__get_gate_array(gate_str, para)
        self.apply_one_site_gate(gate=gate_array, site=q)
        return self
        
    def operate_2qubit_gate(self, gate_str, q0, q1, para=0.0):
        """
        operate 2-qubit gate.

        Parameters
        ----------
        gate_str : str
            gate stiring (ex. 'cx','cy','cz','ch','crz', ..)
        q0 : int
            qubit id.
        q1 : int
            qubit id.
        para : float
            angle for rotation gate (unit of angle is PI radian).

        Returns
        -------
        self : instance of MPState

        """
        if q0 == q1:
            raise ValueError("q0 is equal to q1, they must be different value.")

        gate_array = self.__get_gate_array(gate_str, para)
        swap_gate = self.__get_gate_array('sw')

        if q0 < q1:
            path = [q for q in range(q0, q1 + 1)]
            pos = 0
        elif q0 > q1:
            path = [q for q in range(q1, q0 + 1)]
            pos = -1

        for i in range(len(path) - 2, pos, -1):
            self.position(site=path[i])
            self.apply_two_site_gate(gate=swap_gate, site1=path[i], site2=path[i + 1],
                                     max_truncation_err=self.__max_truncation_err)
        self.position(site=path[0])
        self.apply_two_site_gate(gate=gate_array, site1=path[0], site2=path[1],
                                 max_truncation_err=self.__max_truncation_err)
        for i in range(pos + 1, len(path) - 1):
            self.position(site=path[i])
            self.apply_two_site_gate(gate=swap_gate, site1=path[i], site2=path[i + 1],
                                     max_truncation_err=self.__max_truncation_err)

        return self

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
        self : instance of MPState

        """
        self.operate_1qubit_gate('x', q0)
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
        self : instance of MPState

        """
        self.operate_1qubit_gate('y', q0)
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
        self : instance of MPState

        """
        self.operate_1qubit_gate('z', q0)
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
        self : instance of MPState

        """
        self.operate_1qubit_gate('xr', q0)
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
        self : instance of MPState

        """
        self.operate_1qubit_gate('xr_dg', q0)
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
        self : instance of MPState

        """
        self.operate_1qubit_gate('h', q0)
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
        self : instance of MPState

        """
        self.operate_1qubit_gate('s', q0)
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
        self : instance of MPState

        """
        self.operate_1qubit_gate('s_dg', q0)
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
        self : instance of MPState

        """
        self.operate_1qubit_gate('t', q0)
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
        self : instance of MPState

        """
        self.operate_1qubit_gate('t_dg', q0)
        return self

    def rx(self, q0, phase=0.0):
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
        self.operate_1qubit_gate('rx', q0, para=phase)
        return self

    def ry(self, q0, phase=0.0):
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
        self.operate_1qubit_gate('ry', q0, para=phase)
        return self

    def rz(self, q0, phase=0.0):
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
        self.operate_1qubit_gate('rz', q0, para=phase)
        return self

    def p(self, q0, phase=0.0):
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
        self.operate_1qubit_gate('p', q0, para=phase)
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
        self.operate_2qubit_gate('cx', q0, q1)
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
        self.operate_2qubit_gate('cy', q0, q1)
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
        self.operate_2qubit_gate('cz', q0, q1)
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
        self.operate_2qubit_gate('cxr', q0, q1)
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
        self.operate_2qubit_gate('cxr_dg', q0, q1)
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
        self.operate_2qubit_gate('ch', q0, q1)
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
        self.operate_2qubit_gate('cs', q0, q1)
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
        self.operate_2qubit_gate('cs_dg', q0, q1)
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
        self.operate_2qubit_gate('ct', q0, q1)
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
        self.operate_2qubit_gate('ct_dg', q0, q1)
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
        self.operate_2qubit_gate('sw', q0, q1)
        return self

    def cp(self, q0, q1, phase=0.0):
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
        self.operate_2qubit_gate('cp', q0, q1, para=phase)
        return self

    def crx(self, q0, q1, phase=0.0):
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
        self.operate_2qubit_gate('crx', q0, q1, para=phase)
        return self

    def cry(self, q0, q1, phase=0.0):
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
        self.operate_2qubit_gate('cry', q0, q1, para=phase)
        return self

    def crz(self, q0, q1, phase=0.0):
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
        self.operate_2qubit_gate('crz', q0, q1, para=phase)
        return self

    def rxx(self, q0, q1, phase=0.0):
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
        self.operate_2qubit_gate('rxx', q0, q1, para=phase)
        return self

    def ryy(self, q0, q1, phase=0.0):
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
        self.operate_2qubit_gate('ryy', q0, q1, para=phase)
        return self

    def rzz(self, q0, q1, phase=0.0):
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
        self.operate_2qubit_gate('rzz', q0, q1, para=phase)
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
        if qid is None:
            raise ValueError("qid must be set.")

        # controled and target register
        qid_ctr = qid[:-1]
        qid_tar = qid[-1]

        # hadamard
        self.h(qid_tar)

        # controlled-RZ(psi), psi=pi/(2**(bitnum-1))
        bitnum = len(qid_ctr)
        psi = 1.0/(2**(bitnum-1)) # unit=pi(radian)
        gray_pre = 0
        for gray in gray_code(bitnum):
            if gray == 0:
                continue
            msb = len(str(bin(gray)))-3
            chb = len(str(bin(gray^gray_pre)))-3
            if gray != 1:
                if chb == msb:
                    chb -= 1
                self.cx(qid_ctr[chb], qid_ctr[msb])
            self.cp(qid_ctr[msb], qid_tar, phase=psi)
            psi = -psi
            gray_pre = gray

        # hadamard
        self.h(qid_tar)

        return self
    
    def __probability(self, q):

        z_gate = self.__get_gate_array('z')
        expect_value = self.measure_local_operator([z_gate], [q])[0]
        prob_1 = (1.0 - expect_value.real) / 2.0
        prob_0 = 1.0 - prob_1
        return (prob_0, prob_1)
        
    def m(self, qid=None, shots=1):
        """
        measurement in Z-direction

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.
        shots : int, default 1
            number of measurements.

        Returns
        -------
        md : instance of MDataMPState
            measurement data.

        See Also
        --------
        MDataMPState class

        """
        if qid is None or qid == []:
            qid = list(range(self.__qubit_num))
        
        if shots > 1:
            md = self.__m_many_shots(qid=qid, shots=shots-1) # get stats by measurements (self not change)
            md_one_shot = self.__m_many_shots(qid=qid, shots=1) # mps changes by measurement
            mstr = md_one_shot.last
            md.frequency[mstr] += 1
            md.last = mstr
        else:
            md = self.__m_many_shots(qid=qid, shots=1)
        return md
        
    def __m_many_shots(self, qid=None, shots=1):
        """ mps is change if shots = 1 (projection), not change otherwise """

        proj_gate = [np.array([[1.+0.j, 0.+0.j],
                               [0.+0.j, 0.+0.j]]),
                     np.array([[0.+0.j, 0.+0.j],
                               [0.+0.j, 1.+0.j]])]

        if qid is None or qid == []:
            qid = list(range(self.__qubit_num))

        self.canonicalize(normalize=True)
        if shots > 1:
            [self.position(site=i, max_truncation_err=cfg.EPS) for i in range(self.__qubit_num)]

        frequency = Counter()
        prob_total_dict = {}

        for i in range(shots):
            
            if shots == 1:
                mps = self
            else:
                mps = self.clone()

            prob_total = 1.0
            measured_str = ""
            for q in qid:
                mps.position(q)
                prob = mps.__probability(q=q)
        
                if prob[0] == 1.0:
                    measured_value = 0
                    measured_str += str(measured_value)
                    continue
                elif prob[1] == 1.0:
                    measured_value = 1
                    measured_str += str(measured_value)
                    continue
                    
                if random.random() < prob[0]:
                    measured_value = 0
                    measured_str += str(measured_value)
                    prob_total = prob_total * prob[0]
                else:
                    measured_value = 1
                    measured_str += str(measured_value)
                    prob_total = prob_total * prob[1]
                mps.apply_one_site_gate(gate=proj_gate[measured_value], site=q)
        
            frequency[measured_str] += 1
            last = measured_str
        
            prob_total_dict[measured_str] = prob_total
            if abs(sum(prob_total_dict.values()) - 1.0) < cfg.EPS:
                shots = shots - i - 1
                break

        if i != shots - 1:
            mstr_list = list(prob_total_dict.keys())
            prob_list = list(prob_total_dict.values())
            for i in range(1, len(prob_list)):
                prob_list[i] += prob_list[i - 1]
            prob_list[-1] = 1.0
        
            for i in range(shots):
                r = random.random()
                for j, p in enumerate(prob_list):
                    if r <= p:
                        frequency[mstr_list[j]] += 1
                        break
        
        md = MDataMPState(frequency=frequency, last=last, qid=qid, qubit_num=len(qid))
        return md

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
        >>> mps = MPState(qubit_num=2).h(0).cx(0,1)
        >>> mps.show()
        >>> print(mps.measure(qid=[0,1]))
        >>> mps.show()
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
        md = self.m(qid=qid, shots=1)
        mval = md.last
        return mval
        
    def reset(self, qid=None):
        """
        reset to |00..0> state.

        Parameters
        ----------
        qid : list, default - qubit id's list for all of the qubits
            qubit id's list to reset.

        Returns
        -------
        self : instance of MPState
            matrix product state.

        Notes
        -----
        If 'qid' is set, specified qubits are reset after
        measurement. So if the specified qubits are entangled with the
        remaining qubits, output quantum state is probabilistic. If no
        qubits are set, all qubits are zero reset.

        """
        if qid is None or qid == []:
            qid = list(range(self.__qubit_num))

        proj_gate = [np.array([[1.+0.j, 0.+0.j],
                               [0.+0.j, 0.+0.j]]),
                     np.array([[0.+0.j, 0.+0.j],
                               [0.+0.j, 1.+0.j]])]

        self.canonicalize(normalize=True)

        for q in qid:
            self.position(q)
            prob = self.__probability(q=q)
            if abs(prob[0] - 1.0) < cfg.EPS:
                measured_value = 0
                continue
            elif abs(prob[1] - 1.0) < cfg.EPS:
                measured_value = 1
                self.x(q)
                continue

            if random.random() < prob[0]:
                measured_value = 0
                self.apply_one_site_gate(gate=proj_gate[measured_value], site=q)
                self.canonicalize(normalize=True)
            else:
                measured_value = 1
                self.apply_one_site_gate(gate=proj_gate[measured_value], site=q)
                self.canonicalize(normalize=True)
                self.x(q)

        return self

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

        See Also
        --------
        PauliProduct class (PauliProduct.py)

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

    def expect(self, observable=None):
        """
        get the expectation value for observable under the matrix product state.

        Parameters
        ----------
        observable : instance of Observable
            obserbable of the system.

        Returns
        -------
        expect : complex
            expect value.

        See Also
        --------
        Obserbable class (Observable.py)

        """
        ob = observable.clone()
        if ob.recalc_weight() is False:
            raise ValueError("Observable is not hermitian.")

        expect_value = 0.0
        weighted_pp_list = ob.weighted_pp_list
        for wpp in weighted_pp_list:
            mps = self.clone()
            weight = wpp['weight']
            qid = wpp['pp'].qid
            pauli_list = [pauli_str.lower() for pauli_str in wpp['pp'].pauli_list]
            [mps.operate_1qubit_gate(s, q) for s, q in zip(pauli_list, qid)]
            expect_value += (weight * self.inpro(mps))

        return expect_value
