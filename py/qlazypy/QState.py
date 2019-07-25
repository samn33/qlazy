# -*- coding: utf-8 -*-
import ctypes
import random
import numpy as np
from qlazypy.error import *
from qlazypy.config import *
from qlazypy.Observable import *

lib = ctypes.CDLL('libQlazy.so',mode=ctypes.RTLD_GLOBAL)
try:
    libc = ctypes.CDLL('libc.so.6',mode=ctypes.RTLD_GLOBAL)
except:
    libc = ctypes.CDLL('libc.so',mode=ctypes.RTLD_GLOBAL)

class QState(ctypes.Structure):

    _fields_ = [
        ('qubit_num', ctypes.c_int),
        ('state_num', ctypes.c_int),
        ('camp', ctypes.c_void_p),
        ('gbank', ctypes.c_void_p),
    ]
    
    def __new__(cls, qubit_num, seed=None):

        if qubit_num > MAX_QUBIT_NUM:
            print("qubit number must be {0:d} or less.".format(MAX_QUBIT_NUM))
            raise QState_FailToInitialize()

        if seed is None:
            seed = random.randint(0,1000000)

        lib.init_qlazy(ctypes.c_int(seed))
        
        qstate = None
        c_qstate = ctypes.c_void_p(qstate)

        lib.qstate_init.restype = ctypes.c_int
        lib.qstate_init.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.qstate_init(ctypes.c_int(qubit_num), c_qstate)

        if ret == FALSE:
            raise QState_FailToInitialize()

        out = ctypes.cast(c_qstate.value, ctypes.POINTER(QState))
        
        return out.contents

    def show(self, id=None):

        if id is None or id == []:
            id = [i for i in range(self.qubit_num)]

        # error check
        if len(id) > self.qubit_num:
            raise QState_TooManyArguments()
        for i in range(len(id)):
            if id[i] >= self.qubit_num:
                raise QState_OutOfBound()
            if id[i] < 0:
                raise QState_OutOfBound()

        try:
            qubit_num = len(id)
            qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
            for i in range(len(id)):
                qubit_id[i] = id[i]
            IntArray = ctypes.c_int * MAX_QUBIT_NUM
            id_array = IntArray(*qubit_id)
            
            lib.qstate_print.restype = ctypes.c_int
            lib.qstate_print.argtypes = [ctypes.POINTER(QState),ctypes.c_int, IntArray]
            ret = lib.qstate_print(ctypes.byref(self),ctypes.c_int(qubit_num), id_array)

            if ret == FALSE:
                raise QState_FailToShow()

        except Exception:
            raise QState_FailToShow()

    def clone(self):

        try:
            qstate = None
            c_qstate = ctypes.c_void_p(qstate)
            
            lib.qstate_copy.restype = ctypes.c_int
            lib.qstate_copy.argtypes = [ctypes.POINTER(QState),
                                        ctypes.POINTER(ctypes.c_void_p)]
            ret = lib.qstate_copy(ctypes.byref(self), c_qstate)

            if ret == FALSE:
                raise QState_FailToClone()

            out = ctypes.cast(c_qstate.value, ctypes.POINTER(QState))

            return out.contents
        
        except Exception:
            raise QState_FailToClone()

    def bloch(self, qid=0):

        # error check
        if qid < 0 or qid >= self.qubit_num:
            raise QState_OutOfBound()

        try:
            theta = 0.0
            phi = 0.0
            c_theta = ctypes.c_double(theta)
            c_phi = ctypes.c_double(phi)
            
            lib.qstate_bloch.restype = ctypes.c_int
            lib.qstate_bloch.argtypes = [ctypes.POINTER(QState),ctypes.c_int,
                                         ctypes.POINTER(ctypes.c_double),
                                         ctypes.POINTER(ctypes.c_double)]
            ret = lib.qstate_bloch(ctypes.byref(self),ctypes.c_int(qid),
                                   ctypes.byref(c_theta), ctypes.byref(c_phi))

            if ret == FALSE:
                raise QState_FailToBloch()

            theta = c_theta.value
            phi = c_phi.value

            return theta,phi

        except Exception:
            raise QState_FailToBloch()

    def inpro(self, qstate):

        try:
            
            real = 0.0
            imag = 0.0
            c_real = ctypes.c_double(real)
            c_imag = ctypes.c_double(imag)
            
            lib.qstate_inner_product.restype = ctypes.c_int
            lib.qstate_inner_product.argtypes = [ctypes.POINTER(QState),
                                                 ctypes.POINTER(QState),
                                                 ctypes.POINTER(ctypes.c_double),
                                                 ctypes.POINTER(ctypes.c_double)]
            ret = lib.qstate_inner_product(ctypes.byref(self),ctypes.byref(qstate),
                                           ctypes.byref(c_real), ctypes.byref(c_imag))

            if ret == FALSE:
                raise QState_FailToInnerProduct()

            real = c_real.value
            imag = c_imag.value

            return complex(real, imag)
        
        except Exception:
            raise QState_FailToInnerProduct()
        
    def tenspro(self, qstate):

        try:
            qstate_out = None
            c_qstate_out = ctypes.c_void_p(qstate_out)

            lib.qstate_tensor_product.restype = ctypes.c_int
            lib.qstate_tensor_product.argtypes = [ctypes.POINTER(QState),
                                                  ctypes.POINTER(QState),
                                                  ctypes.POINTER(ctypes.c_void_p)]
            ret = lib.qstate_tensor_product(ctypes.byref(self),ctypes.byref(qstate),
                                            c_qstate_out)

            if ret == FALSE:
                raise QState_FailToTensorProduct()

            out = ctypes.cast(c_qstate_out.value, ctypes.POINTER(QState))

            return out.contents

        except Exception:
            raise QState_FailToTensorProduct()
        
    def evolve(self, observable=None, time=0.0, iter=0):

        if iter < 1:
            raise QState_FailToEvolve()
        
        if observable is None:
            raise QState_FailToEvolve()
        
        try:
            lib.qstate_evolve.restype = ctypes.c_int
            lib.qstate_evolve.argtypes = [ctypes.POINTER(QState),ctypes.POINTER(Observable),
                                          ctypes.c_double, ctypes.c_int]
            ret = lib.qstate_evolve(ctypes.byref(self), ctypes.byref(observable),
                                    ctypes.c_double(time), ctypes.c_int(iter))

            if ret == FALSE:
                raise QState_FailToEvolve()
            
        except Exception:
            raise QState_FailToEvolve()

    def expect(self, observable=None):

        if observable is None:
            raise QState_FailToExpect()
        
        try:
            val = 0.0
            c_val = ctypes.c_double(val)
            lib.qstate_expect_value.restype = ctypes.c_int
            lib.qstate_expect_value.argtypes = [ctypes.POINTER(QState),
                                                ctypes.POINTER(Observable),
                                                ctypes.POINTER(ctypes.c_double)]
            ret = lib.qstate_expect_value(ctypes.byref(self),
                                          ctypes.byref(observable),
                                          ctypes.byref(c_val))
            
            if ret == FALSE:
                raise QState_FailToExpect()

            val = c_val.value
            
            return complex(val,0.0)
            
        except Exception:
            raise QState_FailToExpect()

        return out

    def apply(self, matrix=None):

        if matrix is None:
            raise QState_FailToApply()
        
        try:
            dim = len(matrix) # dimension of the unitary matrix
            size = 2*dim*dim   # array size

            # set array of matrix
            mat_complex = list(matrix.flatten())
            mat = [0.0 for _ in range(size)]
            for i in range(dim*dim):
                mat[2*i] = mat_complex[i].real
                mat[2*i+1] = mat_complex[i].imag
                
            DoubleArray = ctypes.c_double * size
            c_matrix = DoubleArray(*mat)
            
            lib.qstate_apply_matrix.restype = ctypes.c_int
            lib.qstate_apply_matrix.argtypes = [ctypes.POINTER(QState),
                                                DoubleArray, ctypes.c_int]
            ret = lib.qstate_apply_matrix(ctypes.byref(self),
                                          c_matrix, ctypes.c_int(dim))

            if ret == FALSE:
                raise QState_FailToApply()

            return self

        except Exception:
            raise QState_FailToApply()

    @property
    def amp(self, id=None):

        return self.get_amp()
        
    def get_amp(self, id=None):

        if id is None or id == []:
            id = [i for i in range(self.qubit_num)]

        # error check
        if len(id) > self.qubit_num:
            raise QState_TooManyArguments()
        for i in range(len(id)):
            if id[i] >= self.qubit_num:
                raise QState_OutOfBound()
            if id[i] < 0:
                raise QState_OutOfBound()

        try:
            qubit_num = len(id)
            qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
            for i in range(len(id)):
                qubit_id[i] = id[i]
            IntArray = ctypes.c_int * MAX_QUBIT_NUM
            id_array = IntArray(*qubit_id)

            camp = None
            c_camp = ctypes.c_void_p(camp)
            lib.qstate_get_camp.restype = ctypes.c_int
            lib.qstate_get_camp.argtypes = [ctypes.POINTER(QState),ctypes.c_int, IntArray,
                                            ctypes.POINTER(ctypes.c_void_p)]
            ret = lib.qstate_get_camp(ctypes.byref(self),ctypes.c_int(qubit_num),
                                      id_array, c_camp)

            if ret == FALSE:
                raise QState_FailToGetAmp()
                
            o = ctypes.cast(c_camp.value, ctypes.POINTER(ctypes.c_double))
            
            state_num = (1 << len(id))
            out = [0] * state_num
            for i in range(state_num):
                out[i] = complex(o[2*i],o[2*i+1])

            libc.free.argtypes = [ctypes.POINTER(ctypes.c_double)]
            libc.free(o)

        except Exception:
            raise QState_FailToGetCmp()

        return np.array(out)
        
    def x(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=PAULI_X, phase=DEF_PHASE, id=id)
        return self

    def y(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=PAULI_Y, phase=DEF_PHASE, id=id)
        return self

    def z(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=PAULI_Z, phase=DEF_PHASE, id=id)
        return self

    def xr(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=ROOT_PAULI_X, phase=DEF_PHASE, id=id)
        return self

    def xr_dg(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()

        # operate
        id = [q0]
        self.__operate_qgate(kind=ROOT_PAULI_X_, phase=DEF_PHASE, id=id)
        return self

    def h(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()

        # operate
        id = [q0]
        self.__operate_qgate(kind=HADAMARD, phase=DEF_PHASE, id=id)
        return self

    def s(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=PHASE_SHIFT_S, phase=DEF_PHASE, id=id)
        return self

    def s_dg(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=PHASE_SHIFT_S_, phase=DEF_PHASE, id=id)
        return self

    def t(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=PHASE_SHIFT_T, phase=DEF_PHASE, id=id)
        return self

    def t_dg(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=PHASE_SHIFT_T_, phase=DEF_PHASE, id=id)
        return self

    def rx(self, q0, phase=DEF_PHASE):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=ROTATION_Y, phase=phase, id=id)
        return self

    def ry(self, q0, phase=DEF_PHASE):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=ROTATION_Y, phase=phase, id=id)
        return self

    def rz(self, q0, phase=DEF_PHASE):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=ROTATION_Z, phase=phase, id=id)
        return self

    def p(self, q0, phase=DEF_PHASE):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=PHASE_SHIFT, phase=phase, id=id)
        return self

    def cx(self, q0, q1):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()
            
        # operate
        id = [q0,q1]
        self.__operate_qgate(kind=CONTROLLED_X, phase=DEF_PHASE, id=id)
        return self

    def cy(self, q0, q1):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()
            
        # operate
        id = [q0,q1]
        self.__operate_qgate(kind=CONTROLLED_Y, phase=DEF_PHASE, id=id)
        return self

    def cz(self, q0, q1):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()

        # operate
        id = [q0,q1]
        self.__operate_qgate(kind=CONTROLLED_Z, phase=DEF_PHASE, id=id)
        return self

    def cxr(self, q0, q1):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()

        # operate
        id = [q0,q1]
        self.__operate_qgate(kind=CONTROLLED_XR, phase=DEF_PHASE, id=id)
        return self

    def cxr_dg(self, q0, q1):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()

        # operate
        id = [q0,q1]
        self.__operate_qgate(kind=CONTROLLED_XR_, phase=DEF_PHASE, id=id)
        return self

    def ch(self, q0, q1):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()

        # operate
        id = [q0,q1]
        self.__operate_qgate(kind=CONTROLLED_H, phase=DEF_PHASE, id=id)
        return self

    def cs(self, q0, q1):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()

        # operate
        id = [q0,q1]
        self.__operate_qgate(kind=CONTROLLED_S, phase=DEF_PHASE, id=id)
        return self

    def cs_dg(self, q0, q1):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()

        # operate
        id = [q0,q1]
        self.__operate_qgate(kind=CONTROLLED_S_, phase=DEF_PHASE, id=id)
        return self

    def ct(self, q0, q1):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()

        # operate
        id = [q0,q1]
        self.__operate_qgate(kind=CONTROLLED_T, phase=DEF_PHASE, id=id)
        return self

    def ct_dg(self, q0, q1):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()

        # operate
        id = [q0,q1]
        self.__operate_qgate(kind=CONTROLLED_T_, phase=DEF_PHASE, id=id)
        return self

    def cp(self, q0, q1, phase=DEF_PHASE):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()

        # operate
        id = [q0,q1]
        self.__operate_qgate(kind=CONTROLLED_P, phase=phase, id=id)
        return self

    def crx(self, q0, q1, phase=DEF_PHASE):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()

        # operate
        id = [q0,q1]
        self.__operate_qgate(kind=CONTROLLED_RX, phase=phase, id=id)
        return self

    def cry(self, q0, q1, phase=DEF_PHASE):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()

        # operate
        id = [q0,q1]
        self.__operate_qgate(kind=CONTROLLED_RY, phase=phase, id=id)
        return self

    def crz(self, q0, q1, phase=DEF_PHASE):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()

        # operate
        id = [q0,q1]
        self.__operate_qgate(kind=CONTROLLED_RZ, phase=phase, id=id)
        return self

    def ccx(self, q0, q1, q2):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q2 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()
        if q1 == q2:
            raise QState_SameQubitID()
        if q2 == q0:
            raise QState_SameQubitID()

        # operate
        id = [q0,q1,q2]
        self.__operate_qgate(kind=TOFFOLI, phase=DEF_PHASE, id=id)
        return self

    def m(self, id=None, shots=DEF_SHOTS, angle=0.0, phase=0.0):
        if id is None or id == []:
            id = [i for i in range(self.qubit_num)]
            
        # error check
        if len(id) > self.qubit_num:
            raise QState_TooManyArguments()
        for i in range(len(id)):
            if id[i] >= self.qubit_num:
                raise QState_OutOfBound()
            if id[i] < 0:
                raise QState_OutOfBound()

        # operate
        qubit_num = len(id)
        qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
        for i in range(len(id)):
            qubit_id[i] = id[i]
        IntArray = ctypes.c_int * MAX_QUBIT_NUM
        id_array = IntArray(*qubit_id)

        mdata = None
        c_mdata = ctypes.c_void_p(mdata)
        
        lib.qstate_measure.restype = ctypes.c_int
        lib.qstate_measure.argtypes = [ctypes.POINTER(QState), ctypes.c_int,
                                       ctypes.c_double, ctypes.c_double,
                                       ctypes.c_int, IntArray,
                                       ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.qstate_measure(ctypes.byref(self), ctypes.c_int(shots),
                                 ctypes.c_double(angle), ctypes.c_double(phase),
                                 ctypes.c_int(qubit_num), id_array, c_mdata)

        if ret == FALSE:
            raise QState_FailToMeasure()

        out = ctypes.cast(c_mdata.value, ctypes.POINTER(MData))
        
        state_num = out.contents.state_num
        last_state = out.contents.last
        freq = ctypes.cast(out.contents.freq, ctypes.POINTER(ctypes.c_int*state_num))
        freq_list = [freq.contents[i] for i in range(state_num)]
        mdpy = MDataPy(freq_list=freq_list, last_state=last_state, qubit_num=qubit_num,
                       state_num=state_num, angle=angle, phase=phase)
        out.contents.free()

        return mdpy

    def mx(self, id=None, shots=DEF_SHOTS):
        return self.m(id=id, shots=shots, angle=0.5, phase=0.0)
        
    def my(self, id=None, shots=DEF_SHOTS):
        return self.m(id=id, shots=shots, angle=0.5, phase=0.5)
        
    def mz(self, id=None, shots=DEF_SHOTS):
        return self.m(id=id, shots=shots, angle=0.0, phase=0.0)
        
    def mb(self, id=None, shots=DEF_SHOTS):
        # error check
        if id is None or id == []:
            raise QState_NeedMoreArguments()
        if len(id) < 2:
            raise QState_NeedMoreArguments()
        if len(id) > 2:
            raise QState_TooManyArguments()
        for i in range(len(id)):
            if id[i] >= self.qubit_num:
                raise QState_OutOfBound()
            if id[i] < 0:
                raise QState_OutOfBound()

        # operate
        state_num = 4
        qubit_num = 2
        qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
        for i in range(qubit_num):
            qubit_id[i] = id[i]
        IntArray = ctypes.c_int * MAX_QUBIT_NUM
        id_array = IntArray(*qubit_id)
        
        mdata = None
        c_mdata = ctypes.c_void_p(mdata)

        lib.qstate_measure_bell.restype = ctypes.c_int
        lib.qstate_measure_bell.argtypes = [ctypes.POINTER(QState), ctypes.c_int,
                                            ctypes.c_int, IntArray,
                                            ctypes.POINTER(ctypes.c_void_p)]

        ret = lib.qstate_measure_bell(ctypes.byref(self), ctypes.c_int(shots),
                                      ctypes.c_int(qubit_num), id_array, c_mdata)

        if ret == FALSE:
            raise QState_FailToMeasure()

        out = ctypes.cast(c_mdata.value, ctypes.POINTER(MData))
        
        last_state = out.contents.last
        freq = ctypes.cast(out.contents.freq, ctypes.POINTER(ctypes.c_int*state_num))
        freq_list = [freq.contents[i] for i in range(state_num)]
        mdpy = MDataPy(freq_list=freq_list, last_state=last_state, qubit_num=qubit_num,
                       state_num=state_num, angle=0.0, phase=0.0)
        out.contents.free()

        return mdpy

    def free(self):

        lib.qstate_free.argtypes = [ctypes.POINTER(QState)]
        lib.qstate_free(ctypes.byref(self))
 
    def __operate_qgate(self, kind=None, phase=None, id=None):

        qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
        for i in range(len(id)):
            qubit_id[i] = id[i]
        IntArray = ctypes.c_int * MAX_QUBIT_NUM
        id_array = IntArray(*qubit_id)

        lib.qstate_operate_qgate.restype = ctypes.c_int
        lib.qstate_operate_qgate.argtypes = [ctypes.POINTER(QState), ctypes.c_int,
                                             ctypes.c_double, IntArray]
        ret = lib.qstate_operate_qgate_param(ctypes.byref(self), ctypes.c_int(kind),
                                             ctypes.c_double(phase), id_array)

        if ret == FALSE:
            raise QState_FailToOperateQgate()
            

class MData(ctypes.Structure):

    _fields_ = [
        ('qubit_num', ctypes.c_int),
        ('state_num', ctypes.c_int),
        ('shot_num', ctypes.c_int),
        ('angle', ctypes.c_double),
        ('phase', ctypes.c_double),
        ('qubit_id', ctypes.c_int*MAX_QUBIT_NUM),
        ('freq', ctypes.POINTER(ctypes.c_int)),
        ('last', ctypes.c_int),
    ]

    def show(self):

        lib.mdata_print.restype = ctypes.c_int
        lib.mdata_print.argtypes = [ctypes.POINTER(MData)]
        ret = lib.mdata_print(ctypes.byref(self))

        if ret == FALSE:
            raise MData_FailToShow()

    @property
    def frq(self):

        try:
            freq = ctypes.cast(self.freq, ctypes.POINTER(ctypes.c_int*self.state_num))
            freq_list = [freq.contents[i] for i in range(self.state_num)]
        except Exception:
            raise MData_FailToGetFrq()
        
        return np.array(freq_list)

    @property
    def lst(self):

        return self.last
            
    def free(self):

        lib.mdata_free.argtypes = [ctypes.POINTER(MData)]
        lib.mdata_free(ctypes.byref(self))

class MDataPy:

    def __init__(self, freq_list=None, last_state=0, state_num=0, qubit_num=0,
                 angle=0.0, phase=0.0):
        self.freq_list = freq_list
        self.last_state = last_state
        self.qubit_num = qubit_num
        self.state_num = state_num
        self.angle = angle
        self.phase = phase

    @property
    def frq(self):
        return self.freq_list

    @property
    def lst(self):
        return self.last_state

    def show(self):
        if self.angle == 0.5 and self.phase == 0.0:
            print("direction of measurement: x-axis")
            self.__show_any()
        elif self.angle == 0.5 and self.phase == 0.5:
            print("direction of measurement: y-axis")
            self.__show_any()
        elif self.angle == 0.0 and self.phase == 0.0:
            print("direction of measurement: z-axis")
            self.__show_z()
        else:
            print("direction of measurement: theta={0:f}*PI, phi={1:f}*PI".
                  format(self.angle, self.phase))
            self.__show_any()

    def __show_z(self):
        
        for i in range(self.state_num):
            if self.freq_list[i] != 0:
                state_string = format(i,'b').zfill(self.qubit_num)
                print("frq[{0:}] = {1:d}".
                      format(state_string, self.freq_list[i]))
                
        state_string = format(self.last_state,'b').zfill(self.qubit_num)
        print("last state =>", state_string)

    def __show_any(self):
        
        for i in range(self.state_num):
            if self.freq_list[i] != 0:
                state_string = format(i,'b').zfill(self.qubit_num)\
                                            .replace('0','u').replace('1','d')
                print("frq[{0:}] = {1:d}".
                      format(state_string, self.freq_list[i]))
                
        state_string = format(self.last_state,'b').zfill(self.qubit_num)\
                                                  .replace('0','u').replace('1','d')
        print("last state =>", state_string)
