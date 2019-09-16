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
    
    def __new__(cls, qstate=[], prob=[]):

        return cls.densop_init(qstate, prob)

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
            densop[i].mul(factor=prob[i])
            de_out.add(densop=densop[i])

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

    def apply(self, matrix=None, id=None):

        self.densop_apply_matrix(matrix=matrix, id=id)
        return self

    def measure(self, kraus=[], povm=[], id=[]):

        if kraus != []:
            N = len(kraus)
            prob = [0.0]*N
            for i in range(N):
                prob[i] = self.densop_measure_kraus(matrix=kraus[i], id=id)
                if abs(prob[i]) < MIN_DOUBLE:
                    prob[i] = 0.0
        elif povm != []:
            N = len(povm)
            prob = [0.0]*N
            for i in range(N):
                prob[i] = self.densop_measure_povm(matrix=povm[i], id=id)
                if abs(prob[i]) < MIN_DOUBLE:
                    prob[i] = 0.0
        else:
            raise DensOp_FailToMeasure()
                
        return prob

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

    def densop_apply_matrix(self, matrix=None, id=None):

        if matrix is None:
            raise DensOp_FailToApply()
        if (matrix.shape[0] > self.row or matrix.shape[1] > self.col):
            raise DensOp_FailToApply()
        
        if id is None or id == []:
            qnum = int(math.log2(self.row))
            id = [i for i in range(qnum)]
            
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
                                                DoubleArray, DoubleArray,
                                                ctypes.c_int, ctypes.c_int]
            ret = lib.densop_apply_matrix(ctypes.byref(self),
                                          ctypes.c_int(qubit_num), id_array,
                                          c_mat_real, c_mat_imag,
                                          ctypes.c_int(row), ctypes.c_int(col))

            if ret == FALSE:
                raise DensOp_FailToApply()

        except Exception:
            raise DensOp_FailToApply()

    def densop_measure_kraus(self, matrix=None, id=None):

        if matrix is None:
            raise DensOp_FailToMeasure()
        if (matrix.shape[0] > self.row or matrix.shape[1] > self.col):
            raise DensOp_FailToMeasure()
        
        if id is None or id == []:
            qnum = int(math.log2(self.row))
            id = [i for i in range(qnum)]
            
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

            lib.densop_measure_kraus.restype = ctypes.c_int
            lib.densop_measure_kraus.argtypes = [ctypes.POINTER(DensOp),
                                                 ctypes.c_int, IntArray,
                                                 DoubleArray, DoubleArray,
                                                 ctypes.c_int, ctypes.c_int,
                                                 ctypes.POINTER(ctypes.c_double)]
            ret = lib.densop_measure_kraus(ctypes.byref(self),
                                           ctypes.c_int(qubit_num), id_array,
                                           c_mat_real, c_mat_imag,
                                           ctypes.c_int(row), ctypes.c_int(col),
                                           ctypes.byref(c_prob))

            if ret == FALSE:
                raise DensOp_FailToMeasure()

            prob = round(c_prob.value, 8)
            
            return prob

        except Exception:
            raise DensOp_FailToMeasure()

    def densop_measure_povm(self, matrix=None, id=None):

        if matrix is None:
            raise DensOp_FailToMeasure()
        if (matrix.shape[0] > self.row or matrix.shape[1] > self.col):
            raise DensOp_FailToMeasure()
        
        if id is None or id == []:
            qnum = int(math.log2(self.row))
            id = [i for i in range(qnum)]
            
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

            lib.densop_measure_povm.restype = ctypes.c_int
            lib.densop_measure_povm.argtypes = [ctypes.POINTER(DensOp),
                                                ctypes.c_int, IntArray,
                                                DoubleArray, DoubleArray,
                                                ctypes.c_int, ctypes.c_int,
                                                ctypes.POINTER(ctypes.c_double)]
            ret = lib.densop_measure_povm(ctypes.byref(self),
                                          ctypes.c_int(qubit_num), id_array,
                                          c_mat_real, c_mat_imag,
                                          ctypes.c_int(row), ctypes.c_int(col),
                                          ctypes.byref(c_prob))

            if ret == FALSE:
                raise DensOp_FailToMeasure()

            prob = round(c_prob.value, 8)
            
            return prob

        except Exception:
            raise DensOp_FailToMeasure()


    def densop_free(self):

        lib.densop_free.argtypes = [ctypes.POINTER(DensOp)]
        lib.densop_free(ctypes.byref(self))
