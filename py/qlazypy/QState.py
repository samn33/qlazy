# -*- coding: utf-8 -*-
import ctypes
import random
import numpy as np
from ctypes.util import find_library
from qlazypy.error import *
from qlazypy.config import *
from qlazypy.MData import *
from qlazypy.Observable import *

lib = ctypes.CDLL('libQlazy.so',mode=ctypes.RTLD_GLOBAL)
libc = ctypes.CDLL(find_library("c"),mode=ctypes.RTLD_GLOBAL)

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

        return cls.qstate_init(qubit_num, seed)
    
    @property
    def amp(self, id=None):
        return self.get_amp()
        
    def get_amp(self, id=None):
        return self.qstate_get_camp(id)

    def show(self, id=None):
        self.qstate_print(id)

    def clone(self):
        return self.qstate_copy()

    def bloch(self, qid=0):
        return self.qstate_bloch(qid=qid)

    def inpro(self, qstate):
        return self.qstate_inner_product(qstate)
        
    def tenspro(self, qstate):
        return self.qstate_tensor_product(qstate)

    def evolve(self, observable=None, time=0.0, iter=0):
        self.qstate_evolve(observable=observable, time=time, iter=iter)
        return self
    
    def expect(self, observable=None):
        return self.qstate_expect_value(observable=observable)
    
    def apply(self, matrix=None):
        self.qstate_apply_matrix(matrix=matrix)
        return self

    def x(self, q0):
        self.qstate_operate_qgate(kind=PAULI_X, phase=DEF_PHASE, id=[q0])
        return self

    def y(self, q0):
        self.qstate_operate_qgate(kind=PAULI_Y, phase=DEF_PHASE, id=[q0])
        return self

    def z(self, q0):
        self.qstate_operate_qgate(kind=PAULI_Z, phase=DEF_PHASE, id=[q0])
        return self

    def xr(self, q0):
        self.qstate_operate_qgate(kind=ROOT_PAULI_X, phase=DEF_PHASE, id=[q0])
        return self

    def xr_dg(self, q0):
        self.qstate_operate_qgate(kind=ROOT_PAULI_X_, phase=DEF_PHASE, id=[q0])
        return self

    def h(self, q0):
        self.qstate_operate_qgate(kind=HADAMARD, phase=DEF_PHASE, id=[q0])
        return self

    def s(self, q0):
        self.qstate_operate_qgate(kind=PHASE_SHIFT_S, phase=DEF_PHASE, id=[q0])
        return self

    def s_dg(self, q0):
        self.qstate_operate_qgate(kind=PHASE_SHIFT_S_, phase=DEF_PHASE, id=[q0])
        return self

    def t(self, q0):
        self.qstate_operate_qgate(kind=PHASE_SHIFT_T, phase=DEF_PHASE, id=[q0])
        return self

    def t_dg(self, q0):
        self.qstate_operate_qgate(kind=PHASE_SHIFT_T_, phase=DEF_PHASE, id=[q0])
        return self

    def rx(self, q0, phase=DEF_PHASE):
        self.qstate_operate_qgate(kind=ROTATION_Y, phase=phase, id=[q0])
        return self

    def ry(self, q0, phase=DEF_PHASE):
        self.qstate_operate_qgate(kind=ROTATION_Y, phase=phase, id=[q0])
        return self

    def rz(self, q0, phase=DEF_PHASE):
        self.qstate_operate_qgate(kind=ROTATION_Z, phase=phase, id=[q0])
        return self

    def p(self, q0, phase=DEF_PHASE):
        self.qstate_operate_qgate(kind=PHASE_SHIFT, phase=phase, id=[q0])
        return self

    def cx(self, q0, q1):
        self.qstate_operate_qgate(kind=CONTROLLED_X, phase=DEF_PHASE, id=[q0,q1])
        return self

    def cy(self, q0, q1):
        self.qstate_operate_qgate(kind=CONTROLLED_Y, phase=DEF_PHASE, id=[q0,q1])
        return self

    def cz(self, q0, q1):
        self.qstate_operate_qgate(kind=CONTROLLED_Z, phase=DEF_PHASE, id=[q0,q1])
        return self

    def cxr(self, q0, q1):
        self.qstate_operate_qgate(kind=CONTROLLED_XR, phase=DEF_PHASE, id=[q0,q1])
        return self

    def cxr_dg(self, q0, q1):
        self.qstate_operate_qgate(kind=CONTROLLED_XR_, phase=DEF_PHASE, id=[q0,q1])
        return self

    def ch(self, q0, q1):
        self.qstate_operate_qgate(kind=CONTROLLED_H, phase=DEF_PHASE, id=[q0,q1])
        return self

    def cs(self, q0, q1):
        self.qstate_operate_qgate(kind=CONTROLLED_S, phase=DEF_PHASE, id=[q0,q1])
        return self

    def cs_dg(self, q0, q1):
        self.qstate_operate_qgate(kind=CONTROLLED_S_, phase=DEF_PHASE, id=[q0,q1])
        return self

    def ct(self, q0, q1):
        self.qstate_operate_qgate(kind=CONTROLLED_T, phase=DEF_PHASE, id=[q0,q1])
        return self

    def ct_dg(self, q0, q1):
        self.qstate_operate_qgate(kind=CONTROLLED_T_, phase=DEF_PHASE, id=[q0,q1])
        return self

    def cp(self, q0, q1, phase=DEF_PHASE):
        self.qstate_operate_qgate(kind=CONTROLLED_P, phase=phase, id=[q0,q1])
        return self

    def crx(self, q0, q1, phase=DEF_PHASE):
        self.qstate_operate_qgate(kind=CONTROLLED_RX, phase=phase, id=[q0,q1])
        return self

    def cry(self, q0, q1, phase=DEF_PHASE):
        self.qstate_operate_qgate(kind=CONTROLLED_RY, phase=phase, id=[q0,q1])
        return self

    def crz(self, q0, q1, phase=DEF_PHASE):
        self.qstate_operate_qgate(kind=CONTROLLED_RZ, phase=phase, id=[q0,q1])
        return self

    def ccx(self, q0, q1, q2):
        self.qstate_operate_qgate(kind=TOFFOLI, phase=DEF_PHASE, id=[q0,q1,q2])
        return self
    
    def m(self, id=None, shots=DEF_SHOTS, angle=0.0, phase=0.0, tag=None):
        return self.qstate_measure(id=id, shots=shots, angle=angle, phase=phase, tag=tag)
        
    def mx(self, id=None, shots=DEF_SHOTS, tag=None):
        return self.qstate_measure(id=id, shots=shots, angle=0.5, phase=0.0, tag=tag)
        
    def my(self, id=None, shots=DEF_SHOTS, tag=None):
        return self.qstate_measure(id=id, shots=shots, angle=0.5, phase=0.5, tag=tag)
        
    def mz(self, id=None, shots=DEF_SHOTS, tag=None):
        return self.qstate_measure(id=id, shots=shots, angle=0.0, phase=0.0, tag=tag)

    def mb(self, id=None, shots=DEF_SHOTS, tag=None):
        return self.qstate_measure_bell(id=id, shots=shots, tag=tag)
        
    def free(self):
        self.qstate_free()

    #
    # ctypes
    #

    @classmethod
    def qstate_init(cls, qubit_num=None, seed=None):
        
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
    
    def qstate_print(self, id=None):

        if id is None or id == []:
            id = [i for i in range(self.qubit_num)]

        self.__check_args(kind=SHOW, shots=None, angle=None, id=id)
        
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
        
    def qstate_copy(self):

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

    def qstate_bloch(self, qid=0):

        # error check
        self.__check_args(kind=BLOCH, shots=None, angle=None, id=[qid])

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

    def qstate_inner_product(self, qstate):

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

    def qstate_tensor_product(self, qstate):

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

    def qstate_evolve(self, observable=None, time=0.0, iter=0):

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

    def qstate_expect_value(self, observable=None):

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

    def qstate_apply_matrix(self, matrix=None):

        if matrix is None:
            raise QState_FailToApply()
        
        try:
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
            
            lib.qstate_apply_matrix.restype = ctypes.c_int
            lib.qstate_apply_matrix.argtypes = [ctypes.POINTER(QState),
                                                DoubleArray, DoubleArray,
                                                ctypes.c_int, ctypes.c_int]
            ret = lib.qstate_apply_matrix(ctypes.byref(self),
                                          c_mat_real, c_mat_imag,
                                          ctypes.c_int(row), ctypes.c_int(col))

            if ret == FALSE:
                raise QState_FailToApply()

            return self

        except Exception:
            raise QState_FailToApply()

    def qstate_get_camp(self, id=None):

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
        
    def qstate_measure(self, id=None, shots=DEF_SHOTS, angle=0.0, phase=0.0, tag=None):

        if id is None or id == []:
            id = [i for i in range(self.qubit_num)]
            
        # error check
        self.__check_args(kind=MEASURE, id=id, shots=shots, angle=angle, phase=phase)

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

        out = ctypes.cast(c_mdata.value, ctypes.POINTER(MDataC))
        
        state_num = out.contents.state_num
        last_state = out.contents.last
        freq = ctypes.cast(out.contents.freq, ctypes.POINTER(ctypes.c_int*state_num))
        freq_list = [freq.contents[i] for i in range(state_num)]
        md = MData(freq_list=freq_list, last_state=last_state, qubit_num=qubit_num,
                       state_num=state_num, angle=angle, phase=phase)
        out.contents.free()

        return md

    def qstate_measure_bell(self, id=None, shots=DEF_SHOTS, tag=None):

        if id is None or id == []:
            id = [i for i in range(2)]
            
        # error check
        self.__check_args(kind=MEASURE_BELL, id=id, shots=shots, angle=None, phase=None)

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

        out = ctypes.cast(c_mdata.value, ctypes.POINTER(MDataC))
        
        last_state = out.contents.last
        freq = ctypes.cast(out.contents.freq, ctypes.POINTER(ctypes.c_int*state_num))
        freq_list = [freq.contents[i] for i in range(state_num)]
        md = MData(freq_list=freq_list, last_state=last_state, qubit_num=qubit_num,
                   state_num=state_num, angle=0.0, phase=0.0, is_bell=True)
        out.contents.free()

        return md

    def qstate_free(self):

        lib.qstate_free.argtypes = [ctypes.POINTER(QState)]
        lib.qstate_free(ctypes.byref(self))
 
    def qstate_operate_qgate(self, kind=None, id=None, phase=None):

        # error check
        self.__check_args(kind=kind, id=id, shots=None, angle=None, phase=phase)
        
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

    def __check_args(self, kind=None, id=None, shots=None, angle=None, phase=None):

        for q in id:
            if (q >= self.qubit_num) or (q < 0):
                raise QState_OutOfBound()
            
        qnum = self.__get_qgate_qubit_num(kind)

        if qnum == 0:  # any qubit number
            # check qubit number
            if len(id) > self.qubit_num:
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
              kind==ROTATION_X or kind==ROTATION_Y or kind==ROTATION_Z):
            return 1
        elif (kind==CONTROLLED_X or kind==CONTROLLED_Y or kind==CONTROLLED_Z or
              kind==CONTROLLED_XR or kind==CONTROLLED_XR_ or kind==CONTROLLED_H or
              kind==CONTROLLED_S or kind==CONTROLLED_S_ or
              kind==CONTROLLED_T or kind==CONTROLLED_T_ or kind==CONTROLLED_P or
              kind==CONTROLLED_RX or kind==CONTROLLED_RY or kind==CONTROLLED_RZ or
              kind==MEASURE_BELL):
            return 2
        elif (kind==TOFFOLI):
            return 3
        else:
            raise QState_UnknownQgateKind()
