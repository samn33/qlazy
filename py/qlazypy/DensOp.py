# -*- coding: utf-8 -*-
import ctypes
import random
import math
import numpy as np
from ctypes.util import find_library
from qlazypy.error import *
from qlazypy.config import *
from qlazypy.QState import *
from qlazypy.MData import *
from qlazypy.Observable import *

lib = ctypes.CDLL('libQlazy.so',mode=ctypes.RTLD_GLOBAL)
libc = ctypes.CDLL(find_library("c"),mode=ctypes.RTLD_GLOBAL)

class DensOp(ctypes.Structure):

    _fields_ = [
        ('row', ctypes.c_int),
        ('col', ctypes.c_int),
        ('elm', ctypes.c_void_p),
    ]
    
    def __new__(cls, qstate=[], prob=[], matrix=None):

        if qstate != [] and prob != []:
            return cls.densop_init(qstate, prob)
        else:
            return cls.densop_init_with_matrix(matrix)
    
    def __str__(self):

        return str(self.get_elm())

    @classmethod
    def mix(cls, densop=[], prob=[]):

        N = len(densop)
        
        if sum(prob) != 1.0:
            s = sum(prob)
            for i in range(N):
                prob[i] = prob[i] / s
        
        de_out = densop[0].clone()
        de_out.mul(factor=prob[0])
        for i in range(1,len(densop)):
            de_tmp = densop[i].clone()
            de_tmp.mul(factor=prob[i])
            de_out.add(densop=de_tmp)
            de_tmp.free()

        return de_out

    @property
    def element(self):

        return self.get_elm()
    
    def get_elm(self, id=[]):

        de_part = self.partial(id=id)
        elm = de_part.densop_get_elm()
        return elm
    
    def partial(self, id=[]):

        if id is None or id == []:
            return self.clone()
        else:
            qubit_num = int(math.log2(self.row))
            id_remained = []
            for x in range(qubit_num):
                if not x in id:
                    id_remained.append(x)
            de_remained = self.patrace(id=id_remained)
            return de_remained
        
    def show(self, id=[]):

        de_part = self.partial(id=id)
        de_part.densop_print()
        de_part.free()

    def clone(self):

        return self.densop_copy()
    
    def add(self, densop=None):

        self.densop_add(densop=densop)
        return self

    def mul(self, factor=0.0):

        self.densop_mul(factor=factor)
        return self

    def trace(self):

        return self.densop_trace()
        
    def sqtrace(self):

        return self.densop_sqtrace()
        
    def patrace(self, id=[]):

        return self.densop_patrace(id=id)

    def tenspro(self, densop):

        return self.densop_tensor_product(densop)

    def expect(self, matrix=None):

        densop = self.clone()
        densop.densop_apply_matrix(matrix=matrix,dir='left')
        value = densop.trace()
        densop.free()
        return value
        
    def apply(self, matrix=None, id=[], dir='both'):

        self.densop_apply_matrix(matrix=matrix, id=id, dir=dir)
        return self

    def probability(self, kraus=[], povm=[], id=[]):

        if kraus != []:
            N = len(kraus)
            prob = [0.0]*N
            for i in range(N):
                prob[i] = self.densop_probability(matrix=kraus[i], id=id,
                                                  matrix_type='kraus')
                if abs(prob[i]) < MIN_DOUBLE:
                    prob[i] = 0.0
        elif povm != []:
            N = len(povm)
            prob = [0.0]*N
            for i in range(N):
                prob[i] = self.densop_probability(matrix=povm[i], id=id,
                                                  matrix_type='povm')
                if abs(prob[i]) < MIN_DOUBLE:
                    prob[i] = 0.0
        else:
            raise DensOp_FailToProbability()
                
        return prob

    def instrument(self, kraus=[], id=[], measured_value=None):

        if id is None or id == []:
            qnum = int(math.log2(self.row))
            id = [i for i in range(qnum)]

        if kraus == []:
            raise DensOp_FailToInstrument()
        else:
            N = len(kraus)

        if measured_value is None:  # non-selective measurement
            
            densop_ori = self.clone()
            for i in range(N):
                if i == 0:
                    self.apply(matrix=kraus[i], id=id, dir='both')
                else:
                    densop_tmp = densop_ori.clone()
                    densop_tmp.apply(matrix=kraus[i], id=id, dir='both')
                    self.add(densop=densop_tmp)
                    densop_tmp.free()
            densop_ori.free()
                
        else:  # selective measurement

            if (measured_value < 0 or measured_value >= N):
                raise DensOp_FailToInstrument()
            self.apply(matrix=kraus[measured_value],id=id)
            #prob = self.trace()
            #self.mul(factor=1.0/prob)

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

    def fidelity(self, densop=None):

        mat1 = self.get_elm()
        mat2 = densop.get_elm()

        if mat1.shape != mat2.shape:
            raise DensOp_FailToFidelity()

        mat1_sqrt = self.__mat_sqrt(mat1)
        mat2_sqrt = self.__mat_sqrt(mat2)

        fid = self.__mat_norm(np.dot(mat1_sqrt,mat2_sqrt))
            
        return fid

    def distance(self, densop=None):  # trace distance

        mat1 = self.get_elm()
        mat2 = densop.get_elm()

        if mat1.shape != mat2.shape:
            raise DensOp_FailToDistance()

        dis = 0.5 * self.__mat_norm(mat1-mat2)
            
        return dis

    def __mat_spectrum(self, mat):  # mat is hermite

        eigenvals, unitary = np.linalg.eigh(mat)
        unitary_T = unitary.T
        return eigenvals,unitary_T

    def spectrum(self):

        mat = self.get_elm()
        eigvals,eigvecs = self.__mat_spectrum(mat)
        prob = [eigvals[i] for i in range(len(eigvals)) if abs(eigvals[i]) > MIN_DOUBLE]
        vecs = [eigvecs[i] for i in range(len(eigvals)) if abs(eigvals[i]) > MIN_DOUBLE]
        qstate = [QState(vector=vecs[i]) for i in range(len(prob))]

        return prob,qstate

    def __von_neumann_entropy(self):  # von neumann entropy

        mat = self.get_elm()
        eigvals = np.linalg.eigvalsh(mat)
        diag = [-eigvals[i]*np.log2(eigvals[i])
                for i in range(len(eigvals)) if abs(eigvals[i]) > MIN_DOUBLE]
        ent = np.sum(diag)
        return ent
    
    def entropy(self, id=[]):  # von neumann / entanglement entropy

        qubit_num = int(math.log2(self.row))
        
        if id == []:
            ent = self.__von_neumann_entropy()
        else:
            if (min(id) < 0 or max(id) >= qubit_num or len(id)!=len(set(id))):
                raise DensOp_FailToEntropy()
            if len(id) == qubit_num:
                ent = self.__von_neumann_entropy()
            else:
                de_part = self.partial(id=id)
                ent = de_part.__von_neumann_entropy()
                de_part.free()
                
        return ent

    def cond_entropy(self, id_0=[], id_1=[]):  # conditional entropy

        qubit_num = int(math.log2(self.row))
        
        if (id_0 == [] or id_1 == []
            or min(id_0) < 0 or max(id_0) >= qubit_num
            or min(id_1) < 0 or max(id_1) >= qubit_num
            or len(id_0) != len(set(id_0))
            or len(id_1) != len(set(id_1))):
            raise DensOp_FailToEntropy()
        else:
            id_merge = id_0 + id_1
            id_whole = set(id_merge)
            ent = self.entropy(id_whole) - self.entropy(id_1)
            
        return ent

    def mutual_info(self, id_0=[], id_1=[]):  # mutual information

        qubit_num = int(math.log2(self.row))
        
        if (id_0 == [] or id_1 == []
            or min(id_0) < 0 or max(id_0) >= qubit_num
            or min(id_1) < 0 or max(id_1) >= qubit_num
            or len(id_0) != len(set(id_0))
            or len(id_1) != len(set(id_1))):
            raise DensOp_FailToEntropy()
        else:
            ent = self.entropy(id_0) - self.cond_entropy(id_0,id_1)
            
        return ent

    def relative_entropy(self, densop=None):  # relative entropy

        if self.row != densop.row:
            raise DensOp_FailToEntropy()
        
        mat_A = self.get_elm()
        mat_B = densop.get_elm()

        eigvals_A,eigvecs_A = self.__mat_spectrum(mat_A)
        eigvals_B,eigvecs_B = self.__mat_spectrum(mat_A)

        P = np.dot(np.conjugate(eigvecs_A.T),eigvecs_B)
        P = np.conjugate(P)*P
        
        diag_A = [eigvals_A[i]*np.log2(eigvals_A[i])
                for i in range(len(eigvals_A)) if abs(eigvals_A[i]) > MIN_DOUBLE]
        relent_A = np.sum(diag_A)

        relent_B = 0.0
        for i in range(len(eigvals_A)):
            if eigvals_A[i] < MIN_DOUBLE:
                continue
            for j in range(len(eigvals_B)):
                relent_B += abs(P[i][j]) * np.log2(eigvals_B[j])
        
        relent = relent_A - relent_B
        return relent

    # 1-qubit gate

    def x(self, q0):
        self.densop_operate_qgate(kind=PAULI_X, phase=DEF_PHASE, id=[q0])
        return self

    def y(self, q0):
        self.densop_operate_qgate(kind=PAULI_Y, phase=DEF_PHASE, id=[q0])
        return self

    def z(self, q0):
        self.densop_operate_qgate(kind=PAULI_Z, phase=DEF_PHASE, id=[q0])
        return self

    def xr(self, q0):
        self.densop_operate_qgate(kind=ROOT_PAULI_X, phase=DEF_PHASE, id=[q0])
        return self

    def xr_dg(self, q0):
        self.densop_operate_qgate(kind=ROOT_PAULI_X_, phase=DEF_PHASE, id=[q0])
        return self

    def h(self, q0):
        self.densop_operate_qgate(kind=HADAMARD, phase=DEF_PHASE, id=[q0])
        return self

    def s(self, q0):
        self.densop_operate_qgate(kind=PHASE_SHIFT_S, phase=DEF_PHASE, id=[q0])
        return self

    def s_dg(self, q0):
        self.densop_operate_qgate(kind=PHASE_SHIFT_S_, phase=DEF_PHASE, id=[q0])
        return self

    def t(self, q0):
        self.densop_operate_qgate(kind=PHASE_SHIFT_T, phase=DEF_PHASE, id=[q0])
        return self

    def t_dg(self, q0):
        self.densop_operate_qgate(kind=PHASE_SHIFT_T_, phase=DEF_PHASE, id=[q0])
        return self

    def rx(self, q0, phase=DEF_PHASE):
        self.densop_operate_qgate(kind=ROTATION_Y, phase=phase, id=[q0])
        return self

    def ry(self, q0, phase=DEF_PHASE):
        self.densop_operate_qgate(kind=ROTATION_Y, phase=phase, id=[q0])
        return self

    def rz(self, q0, phase=DEF_PHASE):
        self.densop_operate_qgate(kind=ROTATION_Z, phase=phase, id=[q0])
        return self

    def p(self, q0, phase=DEF_PHASE):
        self.densop_operate_qgate(kind=PHASE_SHIFT, phase=phase, id=[q0])
        return self

    def u1(self, q0, alpha=DEF_PHASE):
        self.densop_operate_qgate(kind=ROTATION_U1, phase=alpha, id=[q0])
        return self

    def u2(self, q0, alpha=DEF_PHASE, beta=DEF_PHASE):
        self.densop_operate_qgate(kind=ROTATION_U2, phase=alpha, phase1=beta, id=[q0])
        return self

    def u3(self, q0, alpha=DEF_PHASE, beta=DEF_PHASE, gamma=DEF_PHASE):
        self.densop_operate_qgate(kind=ROTATION_U3, phase=alpha, phase1=beta,
                                  phase2=gamma, id=[q0])
        return self

    # 2-qubit gate

    def cx(self, q0, q1):
        self.densop_operate_qgate(kind=CONTROLLED_X, phase=DEF_PHASE, id=[q0,q1])
        return self

    def cy(self, q0, q1):
        self.densop_operate_qgate(kind=CONTROLLED_Y, phase=DEF_PHASE, id=[q0,q1])
        return self

    def cz(self, q0, q1):
        self.densop_operate_qgate(kind=CONTROLLED_Z, phase=DEF_PHASE, id=[q0,q1])
        return self

    def cxr(self, q0, q1):
        self.densop_operate_qgate(kind=CONTROLLED_XR, phase=DEF_PHASE, id=[q0,q1])
        return self

    def cxr_dg(self, q0, q1):
        self.densop_operate_qgate(kind=CONTROLLED_XR_, phase=DEF_PHASE, id=[q0,q1])
        return self

    def ch(self, q0, q1):
        self.densop_operate_qgate(kind=CONTROLLED_H, phase=DEF_PHASE, id=[q0,q1])
        return self

    def cs(self, q0, q1):
        self.densop_operate_qgate(kind=CONTROLLED_S, phase=DEF_PHASE, id=[q0,q1])
        return self

    def cs_dg(self, q0, q1):
        self.densop_operate_qgate(kind=CONTROLLED_S_, phase=DEF_PHASE, id=[q0,q1])
        return self

    def ct(self, q0, q1):
        self.densop_operate_qgate(kind=CONTROLLED_T, phase=DEF_PHASE, id=[q0,q1])
        return self

    def ct_dg(self, q0, q1):
        self.densop_operate_qgate(kind=CONTROLLED_T_, phase=DEF_PHASE, id=[q0,q1])
        return self

    def sw(self, q0, q1):
        self.densop_operate_qgate(kind=SWAP, phase=DEF_PHASE, id=[q0,q1])
        return self

    def cp(self, q0, q1, phase=DEF_PHASE):
        self.densop_operate_qgate(kind=CONTROLLED_P, phase=phase, id=[q0,q1])
        return self

    def crx(self, q0, q1, phase=DEF_PHASE):
        self.densop_operate_qgate(kind=CONTROLLED_RX, phase=phase, id=[q0,q1])
        return self

    def cry(self, q0, q1, phase=DEF_PHASE):
        self.densop_operate_qgate(kind=CONTROLLED_RY, phase=phase, id=[q0,q1])
        return self

    def crz(self, q0, q1, phase=DEF_PHASE):
        self.densop_operate_qgate(kind=CONTROLLED_RZ, phase=phase, id=[q0,q1])
        return self

    def cu1(self, q0, q1, alpha=DEF_PHASE):
        self.densop_operate_qgate(kind=CONTROLLED_U1, phase=alpha, id=[q0,q1])
        return self

    def cu2(self, q0, q1, alpha=DEF_PHASE, beta=DEF_PHASE):
        self.densop_operate_qgate(kind=CONTROLLED_U2, phase=alpha, phase1=beta,
                                  id=[q0,q1])
        return self

    def cu3(self, q0, q1, alpha=DEF_PHASE, beta=DEF_PHASE, gamma=DEF_PHASE):
        self.densop_operate_qgate(kind=CONTROLLED_U3, phase=alpha, phase1=beta,
                                  phase2=gamma, id=[q0,q1])
        return self

    # 3-qubit gate
    
    def ccx(self, q0, q1, q2):
        self.cxr(q1,q2).cx(q0,q1).cxr_dg(q1,q2).cx(q0,q1).cxr(q0,q2)
        return self

    def csw(self, q0, q1, q2):
        self.cx(q2,q1).ccx(q0,q1,q2).cx(q2,q1)
        return self
    
    def free(self):

        return self.densop_free()
    
    #
    # ctypes
    #

    @classmethod
    def densop_init(cls, qstate=[], prob=[]):
        
        num = len(qstate)

        densop = None
        c_densop = ctypes.c_void_p(densop)

        DoubleArray = ctypes.c_double * num
        prob_array = DoubleArray(*prob)

        QStateArray = QState * num
        qstate_array = QStateArray(*qstate)

        lib.densop_init.restype = ctypes.c_int
        lib.densop_init.argtypes = [ctypes.POINTER(QState),
                                    ctypes.POINTER(ctypes.c_double),
                                    ctypes.c_int,
                                    ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.densop_init(qstate_array, prob_array,
                              ctypes.c_int(num), c_densop)

        if ret == FALSE:
            raise DensOp_FailToInitialize()
            
        out = ctypes.cast(c_densop.value, ctypes.POINTER(DensOp))
        
        return out.contents

    @classmethod
    def densop_init_with_matrix(cls, matrix=None):

        densop = None
        c_densop = ctypes.c_void_p(densop)

        row = len(matrix)
        col = row
        size = row * col

        mat_complex = list(matrix.flatten())
        mat_real = [0.0 for _ in range(size)]
        mat_imag = [0.0 for _ in range(size)]
        for i in range(size):
            mat_real[i] = mat_complex[i].real
            mat_imag[i] = mat_complex[i].imag
                
        DoubleArray = ctypes.c_double * size
        c_mat_real = DoubleArray(*mat_real)
        c_mat_imag = DoubleArray(*mat_imag)
            
        lib.densop_init_with_matrix.restype = ctypes.c_int
        lib.densop_init_with_matrix.argtypes = [DoubleArray, DoubleArray,
                                                ctypes.c_int, ctypes.c_int,
                                                ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.densop_init_with_matrix(c_mat_real, c_mat_imag,
                                          ctypes.c_int(row), ctypes.c_int(col),
                                          c_densop)
        
        if ret == FALSE:
            raise DensOp_FailToInitialize()
            
        out = ctypes.cast(c_densop.value, ctypes.POINTER(DensOp))
        
        return out.contents
        
    def densop_get_elm(self):

        try:
            elm = None
            c_elm = ctypes.c_void_p(elm)

            lib.densop_get_elm.restype = ctypes.c_int
            lib.densop_get_elm.argtypes = [ctypes.POINTER(DensOp),
                                           ctypes.POINTER(ctypes.c_void_p)]
            ret = lib.densop_get_elm(ctypes.byref(self), c_elm)

            if ret == FALSE:
                raise DensOp_FailToGetElm()
            
            o = ctypes.cast(c_elm.value, ctypes.POINTER(ctypes.c_double))

            size = self.row * self.col
            out = [0] * size
            for i in range(size):
                out[i] = complex(round(o[2*i],8),round(o[2*i+1],8))

            libc.free.argtypes = [ctypes.POINTER(ctypes.c_double)]
            libc.free(o)

            return np.array(out).reshape([self.row,self.col])

        except Exception:
            raise DensOp_FailToGetElm()

    def densop_print(self):

        try:

            lib.densop_print.restype = ctypes.c_int
            lib.densop_print.argtypes = [ctypes.POINTER(DensOp)]
            ret = lib.densop_print(ctypes.byref(self))

            if ret == FALSE:
                raise DensOp_FailToShow()

        except Exception:
            raise DensOp_FailToShow()

    def densop_copy(self):

        try:
            densop = None
            c_densop = ctypes.c_void_p(densop)
            
            lib.densop_copy.restype = ctypes.c_int
            lib.densop_copy.argtypes = [ctypes.POINTER(DensOp),
                                        ctypes.POINTER(ctypes.c_void_p)]
            ret = lib.densop_copy(ctypes.byref(self), c_densop)

            if ret == FALSE:
                raise DensOp_FailToClone()

            out = ctypes.cast(c_densop.value, ctypes.POINTER(DensOp))

            return out.contents
        
        except Exception:
            raise DensOp_FailToClone()

    def densop_add(self, densop=None):

        try:
            lib.densop_add.restype = ctypes.c_int
            lib.densop_add.argtypes = [ctypes.POINTER(DensOp), ctypes.POINTER(DensOp)]
            ret = lib.densop_add(ctypes.byref(self), ctypes.byref(densop))

            if ret == FALSE:
                raise DensOp_FailToAdd()
        
        except Exception:
            raise DensOp_FailToAdd()

    def densop_mul(self, factor=0.0):

        try:
            
            lib.densop_mul.restype = ctypes.c_int
            lib.densop_mul.argtypes = [ctypes.POINTER(DensOp), ctypes.c_double]
            ret = lib.densop_mul(ctypes.byref(self), ctypes.c_double(factor))

            if ret == FALSE:
                raise DensOp_FailToMul()

        except Exception:
            raise DensOp_FailToMul()

    def densop_trace(self):

        try:
        
            real = 0.0
            imag = 0.0
            c_real = ctypes.c_double(real)
            c_imag = ctypes.c_double(imag)
            
            lib.densop_trace.restype = ctypes.c_int
            lib.densop_trace.argtypes = [ctypes.POINTER(DensOp),
                                         ctypes.POINTER(ctypes.c_double),
                                         ctypes.POINTER(ctypes.c_double)]
            ret = lib.densop_trace(ctypes.byref(self), ctypes.byref(c_real),
                                   ctypes.byref(c_imag))

            if ret == FALSE:
                raise DensOp_FailToTrace()

            real = round(c_real.value, 8)
            imag = round(c_imag.value, 8)

            if abs(imag) > MIN_DOUBLE:
                raise DensOp_FailToTrace()
                
            return real
        
        except Exception:
            raise DensOp_FailToTrace()

    def densop_sqtrace(self):

        try:
            real = 0.0
            imag = 0.0
            c_real = ctypes.c_double(real)
            c_imag = ctypes.c_double(imag)
            
            lib.densop_sqtrace.restype = ctypes.c_int
            lib.densop_sqtrace.argtypes = [ctypes.POINTER(DensOp),
                                           ctypes.POINTER(ctypes.c_double),
                                           ctypes.POINTER(ctypes.c_double)]
            ret = lib.densop_sqtrace(ctypes.byref(self), ctypes.byref(c_real),
                                     ctypes.byref(c_imag))

            if ret == FALSE:
                raise DensOp_FailToSqTrace()

            real = round(c_real.value, 8)
            imag = round(c_imag.value, 8)

            if abs(imag) > MIN_DOUBLE:
                raise DensOp_FailToTrace()
                
            return real
        
        except Exception:
            raise DensOp_FailToSqTrace()

    def densop_patrace(self, id=None):

        try:
            if id == None:
                raise DensOp_FailToPaTrace()
            
            densop = None
            c_densop = ctypes.c_void_p(densop)
            
            qubit_num = len(id)
            qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
            for i in range(len(id)):
                qubit_id[i] = id[i]
            IntArray = ctypes.c_int * MAX_QUBIT_NUM
            id_array = IntArray(*qubit_id)

            lib.densop_patrace.restype = ctypes.c_int
            lib.densop_patrace.argtypes = [ctypes.POINTER(DensOp),
                                           ctypes.c_int,IntArray,
                                           ctypes.POINTER(ctypes.c_void_p)]
            ret = lib.densop_patrace(ctypes.byref(self), ctypes.c_int(qubit_num),
                                     id_array, c_densop)

            if ret == FALSE:
                raise DensOp_FailToPaTrace()
            
            out = ctypes.cast(c_densop.value, ctypes.POINTER(DensOp))
        
            return out.contents

        except Exception:
            raise DensOp_FailToPaTrace()

    def densop_tensor_product(self, densop):

        try:
            densop_out = None
            c_densop_out = ctypes.c_void_p(densop_out)

            lib.densop_tensor_product.restype = ctypes.c_int
            lib.densop_tensor_product.argtypes = [ctypes.POINTER(DensOp),
                                                  ctypes.POINTER(DensOp),
                                                  ctypes.POINTER(ctypes.c_void_p)]
            ret = lib.densop_tensor_product(ctypes.byref(self),ctypes.byref(densop),
                                            c_densop_out)

            if ret == FALSE:
                raise DensOp_FailToTensorProduct()

            out = ctypes.cast(c_densop_out.value, ctypes.POINTER(DensOp))

            return out.contents

        except Exception:
            raise DensOp_FailToTensorProduct()

    def densop_apply_matrix(self, matrix=None, id=[], dir='both'):

        if matrix is None:
            raise DensOp_FailToApply()
        if (matrix.shape[0] > self.row or matrix.shape[1] > self.col):
            raise DensOp_FailToApply()
        
        if id is None or id == []:
            qnum = int(math.log2(self.row))
            id = [i for i in range(qnum)]

        if dir == 'left':
            adir = LEFT
        elif dir == 'right':
            adir = RIGHT
        elif dir == 'both':
            adir = BOTH
        else:
            raise DensOp_FailToApply()

        try:
            qubit_num = len(id)
            qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
            for i in range(len(id)):
                qubit_id[i] = id[i]
            IntArray = ctypes.c_int * MAX_QUBIT_NUM
            id_array = IntArray(*qubit_id)

            row = len(matrix) # dimension of the unitary matrix
            col = row
            size = row * col

            # set array of matrix
            mat_complex = list(matrix.flatten())
            mat_real = [0.0 for _ in range(size)]
            mat_imag = [0.0 for _ in range(size)]
            for i in range(size):
                mat_real[i] = mat_complex[i].real
                mat_imag[i] = mat_complex[i].imag
                
            DoubleArray = ctypes.c_double * size
            c_mat_real = DoubleArray(*mat_real)
            c_mat_imag = DoubleArray(*mat_imag)
            
            lib.densop_apply_matrix.restype = ctypes.c_int
            lib.densop_apply_matrix.argtypes = [ctypes.POINTER(DensOp),
                                                ctypes.c_int, IntArray,
                                                ctypes.c_int,
                                                DoubleArray, DoubleArray,
                                                ctypes.c_int, ctypes.c_int]
            ret = lib.densop_apply_matrix(ctypes.byref(self),
                                          ctypes.c_int(qubit_num), id_array,
                                          ctypes.c_int(adir), c_mat_real, c_mat_imag,
                                          ctypes.c_int(row), ctypes.c_int(col))

            if ret == FALSE:
                raise DensOp_FailToApply()

        except Exception:
            raise DensOp_FailToApply()
        

    def densop_probability(self, matrix=None, id=[], matrix_type=None):

        if matrix is None:
            raise DensOp_FailToProbability()
        if (matrix.shape[0] > self.row or matrix.shape[1] > self.col):
            raise DensOp_FailToProbability()
        
        if id is None or id == []:
            qnum = int(math.log2(self.row))
            id = [i for i in range(qnum)]

        if matrix_type == 'kraus':
            mtype = KRAUS
        elif matrix_type == 'povm':
            mtype = POVM
        else:
            raise DensOp_FailToProbability()
            
        try:
            qubit_num = len(id)
            qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
            for i in range(len(id)):
                qubit_id[i] = id[i]
            IntArray = ctypes.c_int * MAX_QUBIT_NUM
            id_array = IntArray(*qubit_id)

            row = len(matrix) # dimension of the unitary matrix
            col = row
            size = row * col

            # set array of matrix
            mat_complex = list(matrix.flatten())
            mat_real = [0.0 for _ in range(size)]
            mat_imag = [0.0 for _ in range(size)]
            for i in range(size):
                mat_real[i] = mat_complex[i].real
                mat_imag[i] = mat_complex[i].imag
                
            DoubleArray = ctypes.c_double * size
            c_mat_real = DoubleArray(*mat_real)
            c_mat_imag = DoubleArray(*mat_imag)
            
            prob = 0.0
            c_prob = ctypes.c_double(prob)

            lib.densop_probability.restype = ctypes.c_int
            lib.densop_probability.argtypes = [ctypes.POINTER(DensOp),
                                               ctypes.c_int, IntArray,
                                               ctypes.c_int, DoubleArray, DoubleArray,
                                               ctypes.c_int, ctypes.c_int,
                                               ctypes.POINTER(ctypes.c_double)]
            ret = lib.densop_probability(ctypes.byref(self),
                                         ctypes.c_int(qubit_num), id_array,
                                         ctypes.c_int(mtype), c_mat_real, c_mat_imag,
                                         ctypes.c_int(row), ctypes.c_int(col),
                                         ctypes.byref(c_prob))

            if ret == FALSE:
                raise DensOp_FailToProbability()

            prob = round(c_prob.value, 8)
            
            return prob

        except Exception:
            raise DensOp_FailToProbability()

    def densop_free(self):

        lib.densop_free.argtypes = [ctypes.POINTER(DensOp)]
        lib.densop_free(ctypes.byref(self))

    def densop_operate_qgate(self, kind=None, id=None,
                             phase=DEF_PHASE, phase1=DEF_PHASE, phase2=DEF_PHASE):

        # error check
        self.__check_args(kind=kind, id=id, shots=None, angle=None,
                          phase=phase, phase1=phase1, phase2=phase2)

        qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
        for i in range(len(id)):
            qubit_id[i] = id[i]
        IntArray = ctypes.c_int * MAX_QUBIT_NUM
        id_array = IntArray(*qubit_id)

        lib.densop_operate_qgate.restype = ctypes.c_int
        lib.densop_operate_qgate.argtypes = [ctypes.POINTER(DensOp), ctypes.c_int,
                                             ctypes.c_double, ctypes.c_double,
                                             ctypes.c_double, IntArray]
        ret = lib.densop_operate_qgate(ctypes.byref(self), ctypes.c_int(kind),
                                       ctypes.c_double(phase), ctypes.c_double(phase1),
                                       ctypes.c_double(phase2), id_array)

        if ret == FALSE:
            raise DensOp_FailToOperateQGate()

    def __check_args(self, kind=None, id=None, shots=None, angle=None,
                     phase=None, phase1=None, phase2=None):

        qubit_num = int(math.log2(self.row))
        
        for q in id:
            if (q >= qubit_num) or (q < 0):
                raise QState_OutOfBound()
            
        qnum = self.__get_qgate_qubit_num(kind)

        if qnum == 0:  # any qubit number
            # check qubit number
            if len(id) > qubit_num:
                raise QState_TooManyArguments()
            elif len(id) < 1:
                raise QState_NeedMoreArguments()
            else:
                pass
            
            # check same qubit number
            if len(set(id)) != len(id):
                raise QState_SameQubitID()
            
        elif qnum == 1:
            # check qubit number
            if len(id) > qnum:
                raise QState_TooManyArguments()
            elif len(id) < qnum:
                raise QState_NeedMoreArguments()
            else:
                return True
            
        elif qnum == 2:
            # check qubit number
            if len(id) > qnum:
                raise QState_TooManyArguments()
            elif len(id) < qnum:
                raise QState_NeedMoreArguments()
            else:
                pass

            # check same qubit number
            if (id[0]==id[1]):
                raise QState_SameQubitID()
            else:
                return True
            
        elif qnum == 3:
            # check qubit number
            if len(id) > qnum:
                raise QState_TooManyArguments()
            elif len(id) < qnum:
                raise QState_NeedMoreArguments()
            else:
                pass

            # check same qubit id
            if (id[0]==id[1] or id[1]==id[2] or id[2]==id[0]):
                raise QState_SameQubitID()
            else:
                return True
        
    def __get_qgate_qubit_num(self, kind=None):

        if (kind==SHOW or kind==MEASURE or
            kind==MEASURE_X or kind==MEASURE_Y or kind==MEASURE_Z):  # 0 if any number
            return 0
        elif (kind==BLOCH or kind==PAULI_X or kind==PAULI_Y or kind==PAULI_Z or
              kind==ROOT_PAULI_X or kind==ROOT_PAULI_X_ or kind==HADAMARD or
              kind==PHASE_SHIFT_S or kind==PHASE_SHIFT_S_ or
              kind==PHASE_SHIFT_T or kind==PHASE_SHIFT_T_ or kind==PHASE_SHIFT or
              kind==ROTATION_X or kind==ROTATION_Y or kind==ROTATION_Z or
              kind==ROTATION_U1 or kind==ROTATION_U2 or kind==ROTATION_U3):
             return 1
        elif (kind==CONTROLLED_X or kind==CONTROLLED_Y or kind==CONTROLLED_Z or
              kind==CONTROLLED_XR or kind==CONTROLLED_XR_ or kind==CONTROLLED_H or
              kind==CONTROLLED_S or kind==CONTROLLED_S_ or kind==CONTROLLED_T or
              kind==CONTROLLED_T_ or kind==SWAP or kind==CONTROLLED_P or
              kind==CONTROLLED_RX or kind==CONTROLLED_RY or kind==CONTROLLED_RZ or
              kind==CONTROLLED_U1 or kind==CONTROLLED_U2 or kind==CONTROLLED_U3 or
              kind==MEASURE_BELL):
            return 2
        else:
            raise QState_UnknownQgateKind()
