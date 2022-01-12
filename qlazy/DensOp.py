# -*- coding: utf-8 -*-
import random
import math
import numpy as np
import warnings
import ctypes

from qlazy.config import *
from qlazy.error import *
from qlazy.QState import *
from qlazy.lib.densop_mcx import *

class DensOp(ctypes.Structure):
    """ Density Operator

    Attributes
    ----------
    row : int
        dimension of density operator (= 2**qubit_num).
    col : int
        dimension of density operator (= 2**qubit_num).
    element : list of list of complex
        matrix elements of density operator.

    """

    _fields_ = [
        ('row', ctypes.c_int),
        ('col', ctypes.c_int),
        ('buf_id', ctypes.c_int),
        ('elm', ctypes.c_void_p),
        ('buffer_0', ctypes.c_void_p),
        ('buffer_1', ctypes.c_void_p),
        ('gbank', ctypes.c_void_p),
    ]
    
    def __new__(cls, qubit_num=0, qstate=[], prob=[], matrix=None, **kwargs):
        """
        Parameters
        ----------
        qubit_num : int
            qubit number of the density operator.
        qstate : list of instance of QState
            quantum states of the mixed state.
        prob : list of float
            probability of each quantum state.
        matrix : list of list of comprex
            matrix elements of the density operator.

        Examles
        -------
        >>> import numpy as np
        >>> qs_0 = QState(2)
        >>> qs_1 = QState(2).h(0).cx(0,1)
        >>> de_A = DensOp(qubit_num=5)  # = |00..0><00..0|
        >>> de_B = DensOp(qstate=[qs_0,qs_1], prob=[0.2,0.8])
        >>> de_C = DensOp(matrix=np.array([[0.7,0.0],[0.0,0.3]]))

        Notes
        -----
        You must set either 'qubit_num' or 'qstate' or 'matrix'.
        If 'prob' isn't set, equal probabilities are set.

        """
        if qstate != [] and prob == []:
            mixed_num = len(qstate)
            prob = [1.0/mixed_num for _ in range(mixed_num)]
        
        if qubit_num != 0:
            qstate = [QState(qubit_num=qubit_num)]
            prob = [1.0]
            obj = densop_init(qstate, prob)
        
        elif qstate != [] and prob != []:
            obj = densop_init(qstate, prob)

        else:
            obj = densop_init_with_matrix(matrix)

        self = ctypes.cast(obj.value, ctypes.POINTER(cls)).contents
        return self
    
    def __str__(self):

        return str(self.get_elm())

    def reset(self, qid=[]):
        """
        reset to |0><0| state.

        Parameters
        ----------
        qid : list
            qubit id's list to reset.

        Returns
        -------
        densop : instance of DensOp
            reset density operator.

        Notes
        -----
        If 'qid' is not set, whole system is reset.

        """
        densop_reset(self, qid=qid)
        return self
        
    @classmethod
    def mix(cls, densop=[], prob=[]):
        """
        linear sum of the density operators.

        Parameters
        ----------
        densop : list of instances of DensOp
            densitiy operators.
        prob : list of float
            probabilities (coefficients of the linear sum).

        """
        N = len(densop)
        
        if sum(prob) != 1.0:
            s = sum(prob)
            prob = [p/s for p in prob]
         
        de_out = densop[0].clone()
        de_out.mul(factor=prob[0])
        for i in range(1,len(densop)):
            de_tmp = densop[i].clone()
            de_tmp.mul(factor=prob[i])
            de_out.add(densop=de_tmp)

        return de_out

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
        >>> DensOp.add_method(bell)
        >>> qs = DensOp(qubit_num=2)
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
        >>> DensOp.add_methods(bell, flip, ...)
        >>> de = DensOp(qubit=2)
        >>> de.bell(0,1)
        >>> de.flip(0,1)
        >>> ...
        
        """
        for method in methods:
            if callable(method):
                setattr(cls, method.__name__, method)
            else:
                raise DensOp_Error_AddMethods()
            
    @classmethod
    def create_register(cls, num):
        """
        create registers (qubit id's list) and initialize zero.

        Parameters
        ----------
        num : int
            qubit number you want to use.

        Returns
        -------
        qid : list of int
            qubit id's list.

        Examples
        --------
        >>> qid = DensOp.create_register(3)
        >>> print(qid)
        [0,0,0]
        
        """
        qid = [0]*num
        return qid

    @classmethod
    def init_register(cls, *args):
        """
        initialize registers (qubit id's list).

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
        >>> qid_0 = DensOp.create_register(3)
        >>> qid_1 = DensOp.create_register(2)
        >>> print(qid_0, qid_1)
        [0,0,0] [0,0]
        >>> qnum = DensOp.init_register(qid_0, qid_1)
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
    def free_all(cls, *densops):
        """
        free memory of the all density operators.

        Parameters
        ----------
        densops : instance of DensOp,instance of DensOp,...
            set of DensOp instances

        Returns
        -------
        None

        """
        warnings.warn("No need to call 'free_all' method because free automatically, or you can use class method 'del_all' to free memory explicitly.")

    @classmethod
    def del_all(cls, *densops):
        """
        free memory of the all density operators.

        Parameters
        ----------
        densops : instance of DensOp,instance of DensOp,...
            set of DensOp instances

        Returns
        -------
        None

        """
        for de in densops:
            if type(de) is list or type(de) is tuple:
                cls.del_all(*de)
            elif type(de) is DensOp:
                del de
            else:
                raise DensOp_Error_FreeAll()

    @property
    def element(self):
        """ matrix elements of density operator. """
        return self.get_elm()
    
    def get_elm(self, qid=[]):
        """
        get the matrix elements of density operator.

        Parameters
        ----------
        qid : list of int, default - list of all of the qubit id
            qubit id's list.

        Returns
        -------
        elm : list of complex
            elements of the density matrix.

        Notes
        -----
        If 'qid' is set, matrix elements of specified density operator
        are got after partial trace for remaining qubits. If no qubits
        are specified, you get all matrix elements of the density
        operator.

        """
        de_part = self.partial(qid=qid)
        elm = densop_get_elm(de_part)
        return elm
    
    def show(self, qid=[], nonzero=False):
        """
        show the elements of density operator.

        Parameters
        ----------
        qid : list of int, default - list of all of the qubit id
            qubit id's list to show.
        nonzero : bool, default False
            if True, only non-zero elements are printed.

        Returns
        -------
        None

        Notes
        -----
        If 'qid' is set, it shows the matrix elements of density
        operator for partial quantum system specified by 'qid'. If
        'qid' isn't set, it shows the matrix elements of whole quantum
        system.

        Examples
        --------
        >>> de = DensOp(qubit_num=1)
        >>> ...
        >>> de.show()
        elm[0][0] = +0.5000+0.0000*i : 0.2500 |++++
        elm[0][1] = +0.0000+0.0000*i : 0.0000 |
        elm[1][0] = +0.0000+0.0000*i : 0.0000 |
        elm[1][1] = +0.5000+0.0000*i : 0.2500 |++++
        ...
        >>> de.show(nonzero=True)
        elm[0][0] = +0.5000+0.0000*i : 0.2500 |++++
        elm[1][1] = +0.5000+0.0000*i : 0.2500 |++++

        """
        de_part = self.partial(qid=qid)
        densop_print(de_part, nonzero)

    def clone(self):
        """
        get the copy of density operator.

        Parameters
        ----------
        None

        Returns
        -------
        densop : instance of DensOp
            copy of the original density operator.

        """
        obj = densop_copy(self)
        de = ctypes.cast(obj.value, ctypes.POINTER(self.__class__)).contents
        return de
    
    def add(self, densop=None):
        """
        add the density operator.

        Parameters
        ----------
        densop : instance of DensOp
            density operator to add.

        Returns
        -------
        self : instance of DensOp

        Notes
        -----
        This method change the original density operator.

        """
        densop_add(self, densop=densop)
        return self

    def mul(self, factor=1.0):
        """
        multiply the density operator by factor.

        Parameters
        ----------
        factor : float, default 1.0
            number to multiply.

        Returns
        -------
        self : instance of DensOp

        Notes
        -----
        This method change the original density operator.

        """
        densop_mul(self, factor=factor)
        return self

    def trace(self):
        """
        get the trace of density operator.

        Parameters
        ----------
        None

        Returns
        -------
        trace : float
            trace of the density operator.

        """
        trace = densop_trace(self)
        return trace
        
    def sqtrace(self):
        """
        get the square trace of density operator.

        Parameters
        ----------
        None

        Returns
        -------
        sqtrace : float
            square trace of the density operator.

        """
        sqtrace = densop_sqtrace(self)
        return sqtrace
        
    def patrace(self, qid=[]):
        """
        get the partial trace of density operator.

        Parameters
        ----------
        qid : list of int
            qubit id's list to show.

        Returns
        -------
        densop : instance of DensOp
            density operator after partial trace.

        """
        obj = densop_patrace(self, qid=qid)
        de = ctypes.cast(obj.value, ctypes.POINTER(self.__class__)).contents
        return de

    def partial(self, qid=[]):
        """
        get the density operator for partial system.

        Parameters
        ----------
        qid : list of int
            qubit id's list to show.

        Returns
        -------
        densop : instance of DensOp
            density operator for partial system 
            (= partial trace for remaining system).

        """
        if qid is None or qid == []:
            return self.clone()
        else:
            qubit_num = int(math.log2(self.row))
            qid_remained = []
            for x in range(qubit_num):
                if not x in qid:
                    qid_remained.append(x)
            de_remained = self.patrace(qid=qid_remained)
            return de_remained
        
    def tenspro(self, densop):
        """
        get the tensor product with density operator.

        Parameters
        ----------
        densop : instance of DensOp
            density operator to get the tensor product..

        Returns
        -------
        densop_out : instance of DensOp
            tensor produt of 'self' and 'densop'.

        """
        obj = densop_tensor_product(self, densop)
        de = ctypes.cast(obj.value, ctypes.POINTER(self.__class__)).contents
        return de

    def composite(self, num=0):
        """
        get the composite density operator of same density operators.

        Parameters
        ----------
        num : int
            number of density operators..

        Returns
        -------
        de : instance of DensOp
            composite density operator.

        """
        if num <= 1:
            return self
        else:
            de = self.clone()
            for i in range(num-1):
                de_tmp = de.tenspro(self)
                de = de_tmp.clone()
            return de
        
    def join(self, de_list):
        """
        get tensor product state (density operator) of the density operators' list.

        Parameters
        ----------
        de_list : list (DensOp)
            list of density operators.

        Returns
        -------
        de_out : instance of DensOp
            tensor product state (density operator).

        """
        de_out = self.clone()
        for de in de_list:
            de_tmp = de_out.clone()
            de_out = de_tmp.tenspro(de)
        return de_out

    def expect(self, matrix=None):
        """
        get the expectation value of matrix under this density operator.

        Parameters
        ----------
        matrix : list of list of complex
            matrix expression of hermitian operator.

        Returns
        -------
        value : float
            expectation value.

        Notes
        -----
        'matrix' must be hermitian, and its dimension is equal to
        the dimension of density operator.

        """
        densop = self.clone()
        densop_apply_matrix(densop, matrix=matrix, dire='left')
        value = densop.trace()
        return value
        
    def apply(self, matrix=None, qid=[], dire='both'):
        """
        apply the matrix to density operator.
        (= [matrix] * [self] * [dagger of matrix])

        Parameters
        ----------
        matrix : list of list
            matrix to apply.

        Returns
        -------
        None

        Notes
        -----
        If 'qid' isn't set, dimension of the matrix must be equal to
        dimension of the density operator. If 'qid' is set, dimension
        of the matrix must be equal to the 2 power of 'qid' length.

        """
        densop_apply_matrix(self, matrix=matrix, qid=qid, dire=dire)
        return self

    def probability(self, kraus=[], povm=[], qid=[]):
        """
        get the probabilities for measuring operators. 
        (Kraus or POVM operators).

        Parameters
        ----------
        kraus : list of list of comprex
            Kraus operators.
        povm : list of list of comprex
            POVM operators.
        qid : list
            qubit id's list to measure.

        Returns
        -------
        prob : list of float
            probabilities for measuring operators.

        Notes
        -----
        Either 'kraus' or 'povm' must be set. If 'qid' is not set, all
        of the qubits are measured, the dimention of Kraus or POVM
        operator must be equal to the dimension of density
        operator. If 'qid' is set, the part of qubits are measured,
        the dimension of Kraus or POVM operator must be equal to the 2
        power of 'qid' length. This method does not change the
        original density operator.

        """
        if kraus != []:
            N = len(kraus)
            prob = [0.0]*N
            for i in range(N):
                 prob[i] = densop_probability(self, matrix=kraus[i], qid=qid,
                                             matrix_type='kraus')
                 if abs(prob[i]) < EPS:
                     prob[i] = 0.0
        elif povm != []:
            N = len(povm)
            prob = [0.0]*N
            for i in range(N):
                prob[i] = densop_probability(self, matrix=povm[i], qid=qid,
                                             matrix_type='povm')
                if abs(prob[i]) < EPS:
                    prob[i] = 0.0
        else:
            raise DensOp_Error_Probability()
                
        return prob

    def instrument(self, kraus=[], qid=[], measured_value=None):
        """
        instrument to the density operator

        Parameters
        ----------
        kraus : list of list of comprex
            Kraus operators.
        qid : list
            qubit id's list to measure.
        measured_value : int
            index of measurement 
            (in the case of selective measurement).

        Returns
        -------
        self : instance of DensOp

        Notes
        -----
        If 'measured_value' is set, selective measurement of the index
        corresponding to 'measured_value' is done (but not
        normalize). If 'measured_value' is not set, non-selective
        measurement is done (only operator sum for the Kraus operators
        are executed). This method does change the original density
        operator.

        """
        if qid is None or qid == []:
            qnum = int(math.log2(self.row))
            qid = [i for i in range(qnum)]

        if kraus == []:
            raise DensOp_Error_Instrument()
        else:
            N = len(kraus)

        if measured_value is None:  # non-selective measurement
            
            densop_ori = self.clone()
            for i in range(N):
                if i == 0:
                    self.apply(matrix=kraus[i], qid=qid, dire='both')
                else:
                    densop_tmp = densop_ori.clone()
                    densop_tmp.apply(matrix=kraus[i], qid=qid, dire='both')
                    self.add(densop=densop_tmp)
                
        else:  # selective measurement

            if (measured_value < 0 or measured_value >= N):
                raise DensOp_Error_Instrument()
            self.apply(matrix=kraus[measured_value],qid=qid)
            #prob = self.trace()
            #self.mul(factor=1.0/prob)

        return self

    def bit_flip(self, q, prob=0.0):
        """
        execute the quantum channel of bit flip.

        Parameters
        ----------
        q : int
            qubit id to execute.
        prob : float
            probabillity of the quantum channel.

        Returns
        -------
        self : instance of DensOp

        """
        Sigma_0 = np.eye(2)
        Sigma_1 = np.array([[0,1],[1,0]])
        Sigma_2 = np.array([[0,-1j],[1j,0]])
        Sigma_3 = np.array([[1,0],[0,-1]])

        para_a = math.sqrt(1-prob)
        para_b = math.sqrt(prob)
        kraus = [para_a*Sigma_0, para_b*Sigma_1]
        self.instrument(qid=[q], kraus=kraus)
        return self
    
    def phase_flip(self, q, prob=0.0):
        """
        execute the quantum channel of phase flip.

        Parameters
        ----------
        q : int
            qubit id to execute.
        prob : float
            probability of the quantum channel.

        Returns
        -------
        self : instance of DensOp

        """
        Sigma_0 = np.eye(2)
        Sigma_1 = np.array([[0,1],[1,0]])
        Sigma_2 = np.array([[0,-1j],[1j,0]])
        Sigma_3 = np.array([[1,0],[0,-1]])

        para_a = math.sqrt(1-prob)
        para_b = math.sqrt(prob)
        kraus = [para_a*Sigma_0, para_b*Sigma_3]
        self.instrument(qid=[q], kraus=kraus)
        return self
    
    def bit_phase_flip(self, q, prob=0.0):
        """
        execute the quantum channel of bit and phase flip.

        Parameters
        ----------
        q : int
            qubit id to execute.
        prob : float
            probability of the quantum channel.

        Returns
        -------
        self : instance of DensOp

        """
        Sigma_0 = np.eye(2)
        Sigma_1 = np.array([[0,1],[1,0]])
        Sigma_2 = np.array([[0,-1j],[1j,0]])
        Sigma_3 = np.array([[1,0],[0,-1]])

        para_a = math.sqrt(1-prob)
        para_b = math.sqrt(prob)
        kraus = [para_a*Sigma_0, para_b*Sigma_2]
        self.instrument(qid=[q], kraus=kraus)
        return self
    
    def depolarize(self, q, prob=0.0):
        """
        execute the quantum channel of depolarize.

        Parameters
        ----------
        q : int
            qubit id to execute.
        prob : float
            probability of the quantum channel.

        Returns
        -------
        self : instance of DensOp

        """
        Sigma_0 = np.eye(2)
        Sigma_1 = np.array([[0,1],[1,0]])
        Sigma_2 = np.array([[0,-1j],[1j,0]])
        Sigma_3 = np.array([[1,0],[0,-1]])

        para_a = math.sqrt(1-0.75*prob)
        para_b = math.sqrt(0.25*prob)
        para_c = math.sqrt(0.25*prob)
        para_d = math.sqrt(0.25*prob)
        kraus = [para_a*Sigma_0, para_b*Sigma_1, para_c*Sigma_2, para_d*Sigma_3]
        self.instrument(qid=[q], kraus=kraus)
        return self
    
    def amp_dump(self, q, prob=0.0):
        """
        execute the quantum channel of amplitude dumping.

        Parameters
        ----------
        q : int
            qubit id to execute.
        prob : float
            probability of the quantum channel.

        Returns
        -------
        self : instance of DensOp

        """
        transmit = math.sqrt(1.0-prob)
        reflect = math.sqrt(prob)
        kraus = [np.array([[1,0],[0,transmit]]), np.array([[0,reflect],[0,0]])]
        self.instrument(qid=[q], kraus=kraus)
        return self
    
    def phase_dump(self, q, prob=0.0):
        """
        execute the quantum channel of phase dumping.

        Parameters
        ----------
        q : int
            qubit id to execute.
        prob : float
            probability of the quantum channel.

        Returns
        -------
        self : instance of DensOp

        """
        transmit = math.sqrt(1.0-prob)
        reflect = math.sqrt(prob)
        kraus = [np.array([[1,0],[0,transmit]]), np.array([[0,0],[0,reflect]])]
        self.instrument(qid=[q], kraus=kraus)
        return self
    
    def __mat_sqrt(self,mat):  # mat is hermite

        eigenvals, unitary = np.linalg.eigh(mat)
        unitary_dg = np.conjugate(unitary.T)
        mat_diag = np.sqrt(np.abs(np.diag(eigenvals)))
        mat_sq = np.dot(np.dot(unitary,mat_diag),unitary_dg)

        return mat_sq

    def __mat_norm(self,mat):

        mat2 = np.dot(np.conjugate(mat.T),mat)  # mat2 is hermite
        mat2_sqrt = self.__mat_sqrt(mat2)
        norm = np.trace(mat2_sqrt).real

        return norm 

    def fidelity(self, densop=None, qid=[]):
        """
        get the fidelity with density operator.

        Parameters
        ----------
        densop : instance of DensOp
            density operators to get fidelity.
        qid : list of int, default - all of the qubit id's list
            qubit id's list.

        Returns
        -------
        fid : float
            fidelity of two density operators.

        """
        mat1 = self.get_elm(qid=qid)
        mat2 = densop.get_elm(qid=qid)

        if mat1.shape != mat2.shape:
            raise DensOp_Error_Fidelity()

        mat1_sqrt = self.__mat_sqrt(mat1)
        mat2_sqrt = self.__mat_sqrt(mat2)

        fid = self.__mat_norm(np.dot(mat1_sqrt,mat2_sqrt))
            
        return fid

    def distance(self, densop=None, qid=[]):
        """
        get the trace distance with the density operator.

        Parameters
        ----------
        densop : instance of DensOp
            density operator to get the trace distance.

        qid : list of int, default - all of the qubit id's list
            qubit id's list.

        Returns
        -------
        dis : float
            trace distance.

        """
        mat1 = self.get_elm(qid=qid)
        mat2 = densop.get_elm(qid=qid)

        if mat1.shape != mat2.shape:
            raise DensOp_Error_Distance()

        dis = 0.5 * self.__mat_norm(mat1-mat2)
            
        return dis

    def __mat_spectrum(self, mat):  # mat is hermite

        eigenvals, unitary = np.linalg.eigh(mat)
        unitary_T = unitary.T
        return eigenvals,unitary_T

    def spectrum(self):
        """
        get the spectrum.

        Parameters
        ----------
        None

        Returns
        -------
        qstate : list of QState
            list of the quantum state basis.
        prob : list of float
            list of coefficients for each quantum states basis.

        """
        mat = self.get_elm()
        eigvals,eigvecs = self.__mat_spectrum(mat)
        prob = [eigvals[i] for i in range(len(eigvals)) if abs(eigvals[i]) > EPS]
        vecs = [eigvecs[i] for i in range(len(eigvals)) if abs(eigvals[i]) > EPS]
        qstate = [QState(vector=vecs[i]) for i in range(len(prob))]

        #return prob,qstate
        return qstate,prob

    def __von_neumann_entropy(self):  # von neumann entropy

        mat = self.get_elm()
        eigvals = np.linalg.eigvalsh(mat)
        diag = [-eigvals[i]*np.log2(eigvals[i])
                for i in range(len(eigvals)) if abs(eigvals[i]) > EPS]
        ent = np.sum(diag)
        return ent
    
    def entropy(self, qid=[]):
        """
        get the von neumann entropy (or entanglement entropy).

        Parameters
        ----------
        qid : list of int, default - list all of the qubit id
            qubit id's list (sub-system) to calculate the entropy.

        Returns
        -------
        ent : float
            von neumann entropy.

        """
        qubit_num = int(math.log2(self.row))
        
        if qid == []:
            ent = self.__von_neumann_entropy()
        else:
            if (min(qid) < 0 or max(qid) >= qubit_num or len(qid)!=len(set(qid))):
                raise DensOp_Error_Entropy()
            if len(qid) == qubit_num:
                ent = self.__von_neumann_entropy()
            else:
                de_part = self.partial(qid=qid)
                ent = de_part.__von_neumann_entropy()
                
        return ent

    def cond_entropy(self, qid_0=[], qid_1=[]):
        """
        get the conditional entropy.

        Parameters
        ----------
        qid_0 : list of int
            qubit id's list (sub-system) to calculate the entropy.
        qid_1 : list of int
            qubit id's list (sub-system) to calculate the entropy.

        Returns
        -------
        ent : float
            conditianal entropy (S(qid_0|qid_1)).
        
        """
        qubit_num = int(math.log2(self.row))
        
        if (qid_0 == [] or qid_1 == []
            or min(qid_0) < 0 or max(qid_0) >= qubit_num
            or min(qid_1) < 0 or max(qid_1) >= qubit_num
            or len(qid_0) != len(set(qid_0))
            or len(qid_1) != len(set(qid_1))):
            raise DensOp_Error_Entropy()
        else:
            qid_merge = qid_0 + qid_1
            qid_whole = set(qid_merge)
            ent = self.entropy(qid_whole) - self.entropy(qid_1)
            
        return ent

    def mutual_info(self, qid_0=[], qid_1=[]):  # mutual information
        """
        get the mutual information.

        Parameters
        ----------
        qid_0 : list of int
            qubit id's list (sub-system) to calculate the mutual information.
        qid_1 : list of int
            qubit id's list (sub-system) to calculate the mutual information.

        Returns
        -------
        ent : float
            mutual information (S(qid_0:qid_1)).
        
        """
        qubit_num = int(math.log2(self.row))
        
        if (qid_0 == [] or qid_1 == []
            or min(qid_0) < 0 or max(qid_0) >= qubit_num
            or min(qid_1) < 0 or max(qid_1) >= qubit_num
            or len(qid_0) != len(set(qid_0))
            or len(qid_1) != len(set(qid_1))):
            raise DensOp_Error_Entropy()
        else:
            ent = self.entropy(qid_0) - self.cond_entropy(qid_0,qid_1)
            
        return ent

    def relative_entropy(self, densop=None):  # relative entropy
        """
        get the relative entropy.

        Parameters
        ----------
        densop : instance of DensOp
            density operator to get the relative entropy.

        Returns
        -------
        ent : float
            relative entropy.
        
        """
        if self.row != densop.row:
            raise DensOp_Error_Entropy()
        
        mat_A = self.get_elm()
        mat_B = densop.get_elm()

        eigvals_A,eigvecs_A = self.__mat_spectrum(mat_A)
        eigvals_B,eigvecs_B = self.__mat_spectrum(mat_B)

        P = np.dot(np.conjugate(eigvecs_A.T),eigvecs_B)
        P = np.conjugate(P)*P
        
        diag_A = [eigvals_A[i]*np.log2(eigvals_A[i])
                for i in range(len(eigvals_A)) if abs(eigvals_A[i]) > EPS]
        relent_A = np.sum(diag_A)

        relent_B = 0.0
        for i in range(len(eigvals_A)):
            if eigvals_A[i] < EPS:
                continue
            for j in range(len(eigvals_B)):
                relent_B += abs(P[i][j]) * eigvals_A[i] *np.log2(eigvals_B[j])
        
        relent = relent_A - relent_B
        return relent

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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=PAULI_X, phase=DEF_PHASE, qid=[q0])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=PAULI_Y, phase=DEF_PHASE, qid=[q0])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=PAULI_Z, phase=DEF_PHASE, qid=[q0])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self,kind=ROOT_PAULI_X, phase=DEF_PHASE, qid=[q0])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=ROOT_PAULI_X_, phase=DEF_PHASE, qid=[q0])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=HADAMARD, phase=DEF_PHASE, qid=[q0])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=PHASE_SHIFT_S, phase=DEF_PHASE, qid=[q0])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=PHASE_SHIFT_S_, phase=DEF_PHASE, qid=[q0])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=PHASE_SHIFT_T, phase=DEF_PHASE, qid=[q0])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=PHASE_SHIFT_T_, phase=DEF_PHASE, qid=[q0])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=ROTATION_X, phase=phase, qid=[q0])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=ROTATION_Y, phase=phase, qid=[q0])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=ROTATION_Z, phase=phase, qid=[q0])
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
        self : instance of DensOp

        Notes
        -----
        matrix expression is following...
        | 1.0 0.0             |
        | 0.0 exp(i*phase*PI) |

        """
        densop_operate_qgate(self, kind=PHASE_SHIFT, phase=phase, qid=[q0])
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
        self : instance of DensOp

        Notes
        -----
        this opration is equal to P gate (phase shift gate)

        """
        densop_operate_qgate(self, kind=ROTATION_U1, phase=alpha, qid=[q0])
        return self

    def u2(self, q0, alpha=DEF_PHASE, beta=DEF_PHASE):
        """
        operate U2 gate (by IBM).

        Parameters
        ----------
        q0 : int
            qubit id.
        alpha : float
            rotation angle (unit of angle is PI radian).
        beta : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of DensOp

        Notes
        -----
        matrix experssion is following...
        | 1/sqrt(2)              -exp(i*alpha*PI)/sqrt(2)       |
        | exp(i*beta*PI)/sqrt(2) exp(i*(alpha+beta)*PI)/sqrt(2) |

        """
        densop_operate_qgate(self, kind=ROTATION_U2, phase=alpha, phase1=beta, qid=[q0])
        return self

    def u3(self, q0, alpha=DEF_PHASE, beta=DEF_PHASE, gamma=DEF_PHASE):
        densop_operate_qgate(self, kind=ROTATION_U3, phase=alpha, phase1=beta,
                             phase2=gamma, qid=[q0])
        """
        operate U3 gate (by IBM).

        Parameters
        ----------
        q0 : int
            qubit id.
        alpha : float
            rotation angle (unit of angle is PI radian).
        beta : float
            rotation angle (unit of angle is PI radian).
        gamma : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of DensOp

        Notes
        -----
        matrix expression is following...
        | cos(gamma/2)                -exp(i*alpha*PI)*sin(gamma/2)       |
        | exp(i*beta*PI)*sin(gamma/2) exp(i*(alpha+beta)*PI)*cos(gamma/2) |


        """
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_X, phase=DEF_PHASE, qid=[q0,q1])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_Y, phase=DEF_PHASE, qid=[q0,q1])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_Z, phase=DEF_PHASE, qid=[q0,q1])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_XR, phase=DEF_PHASE, qid=[q0,q1])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_XR_, phase=DEF_PHASE, qid=[q0,q1])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_H, phase=DEF_PHASE, qid=[q0,q1])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_S, phase=DEF_PHASE, qid=[q0,q1])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_S_, phase=DEF_PHASE, qid=[q0,q1])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_T, phase=DEF_PHASE, qid=[q0,q1])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_T_, phase=DEF_PHASE, qid=[q0,q1])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=SWAP_QUBITS, phase=DEF_PHASE, qid=[q0,q1])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_P, phase=phase, qid=[q0,q1])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_RX, phase=phase, qid=[q0,q1])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_RY, phase=phase, qid=[q0,q1])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_RZ, phase=phase, qid=[q0,q1])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_U1, phase=alpha, qid=[q0,q1])
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_U2, phase=alpha, phase1=beta,
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
        self : instance of DensOp

        """
        densop_operate_qgate(self, kind=CONTROLLED_U3, phase=alpha, phase1=beta,
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
        self : instance of DensOp

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
        self : instance of DensOp

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
        self : instance of DensOp
        
        """
        densop_mcx(self, qid)
        return self

    def operate(self, pp=None, ctrl=None):
        """
        operate unitary operator to density operator.

        Parameters
        ----------
        pp : instance of PauliProduct
            pauli product to operate
        ctrl : int
            contoroll qubit id for controlled pauli product

        Returns
        -------
        self : instance of DensOp
            density operator after operation

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

    def free(self):
        """
        free memory of quantum state.

        Parameters
        ----------
        None

        Returns
        -------
        None
        self : instance of DensOp

        """
        # densop_free(self)
        warnings.warn("No need to call 'free' method because free automatically, or you can use 'del' to free memory explicitly.")

    def __del__(self):

        densop_free(self)
    
# c-library for densop
from qlazy.lib.densop_c import *
