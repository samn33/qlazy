# -*- coding: utf-8 -*-
import ctypes
import random
import numpy as np
from qlazypy.error import *
from qlazypy.config import *

lib = ctypes.CDLL('libQlazy.so',mode=ctypes.RTLD_GLOBAL)
try:
    libc = ctypes.CDLL('libc.so.6',mode=ctypes.RTLD_GLOBAL)
except:
    libc = ctypes.CDLL('libc.so',mode=ctypes.RTLD_GLOBAL)

class QState(ctypes.Structure):

    _fields_ = [
        ('qubit_num', ctypes.c_int),
        ('state_num', ctypes.c_int),
        ('camp', ctypes.POINTER(ctypes.c_int)),
        ('measured', ctypes.POINTER(ctypes.c_int)),
    ]
    
    def __new__(self, qubit_num, seed=None):

        self.qubit_num = qubit_num
        self.camp = None
        self.measured = None

        if qubit_num > MAX_QUBIT_NUM:
            print("qubit number must be {0:d} or less.".format(MAX_QUBIT_NUM))
            raise QState_FailToInitialize()

        self._circ = ["q{0:02d} -".format(i) for i in range(qubit_num)]

        if seed is None:
            seed = random.randint(0,1000000)

        lib.init_qlazy(ctypes.c_int(seed))
        
        lib.qstate_init.restype = ctypes.POINTER(QState)
        lib.qstate_init.argtypes = [ctypes.c_int]
        out = lib.qstate_init(ctypes.c_int(self.qubit_num))

        if not out:
            raise QState_FailToInitialize()
        
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

    def circ(self):

        try:
            for i in range(self.qubit_num):
                print(self._circ[i])

        except Exception:
            raise QState_FailToCirc()
    
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
            
            lib.qstate_get_camp.restype = ctypes.POINTER(ctypes.c_double)
            lib.qstate_get_camp.argtypes = [ctypes.POINTER(QState),ctypes.c_int, IntArray]
            ret = lib.qstate_get_camp(ctypes.byref(self),ctypes.c_int(qubit_num), id_array)

            state_num = (1 << len(id))
            out = [0] * state_num
            for i in range(state_num):
                out[i] = complex(ret[2*i],ret[2*i+1])

            libc.free.argtypes = [ctypes.POINTER(ctypes.c_double)]
            libc.free(ret)

        except Exception:
            raise QState_FailToGetCmp()

        return np.array(out)
        
    def x(self, q0):
        return self.X(q0)
        
    def X(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # join circ
        for i in range(self.qubit_num):
            if i == q0:
                self._circ[i] += "X-"
            else:
                self._circ[i] += "--"
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=PAULI_X, phase=DEF_PHASE, id=id)
        return self

    def y(self, q0):
        return self.Y(q0)
    
    def Y(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # join circ
        for i in range(self.qubit_num):
            if i == q0:
                self._circ[i] += "Y-"
            else:
                self._circ[i] += "--"
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=PAULI_Y, phase=DEF_PHASE, id=id)
        return self

    def z(self, q0):
        return self.Z(q0)
    
    def Z(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # join circ
        for i in range(self.qubit_num):
            if i == q0:
                self._circ[i] += "Z-"
            else:
                self._circ[i] += "--"
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=PAULI_Z, phase=DEF_PHASE, id=id)
        return self

    def xr(self, q0):
        return self.XR(q0)
    
    def XR(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # join circ
        for i in range(self.qubit_num):
            if i == q0:
                self._circ[i] += "XR-"
            else:
                self._circ[i] += "---"
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=ROOT_PAULI_X, phase=DEF_PHASE, id=id)
        return self

    def xr_dg(self, q0):
        return self.XR_DG(q0)
    
    def XR_DG(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()

        # join circ
        for i in range(self.qubit_num):
            if i == q0:
                self._circ[i] += "XR+-"
            else:
                self._circ[i] += "----"
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=ROOT_PAULI_X_, phase=DEF_PHASE, id=id)
        return self

    def h(self, q0):
        return self.H(q0)
    
    def H(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()

        # join circ
        for i in range(self.qubit_num):
            if i == q0:
                self._circ[i] += "H-"
            else:
                self._circ[i] += "--"
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=HADAMARD, phase=DEF_PHASE, id=id)
        return self

    def s(self, q0):
        return self.S(q0)
    
    def S(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # join circ
        for i in range(self.qubit_num):
            if i == q0:
                self._circ[i] += "S-"
            else:
                self._circ[i] += "--"
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=PHASE_SHIFT_S, phase=DEF_PHASE, id=id)
        return self

    def s_dg(self, q0):
        return self.S_DG(q0)
    
    def S_DG(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # join circ
        for i in range(self.qubit_num):
            if i == q0:
                self._circ[i] += "S+-"
            else:
                self._circ[i] += "---"
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=PHASE_SHIFT_S_, phase=DEF_PHASE, id=id)
        return self

    def t(self, q0):
        return self.T(q0)
    
    def T(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # join circ
        for i in range(self.qubit_num):
            if i == q0:
                self._circ[i] += "T-"
            else:
                self._circ[i] += "--"
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=PHASE_SHIFT_T, phase=DEF_PHASE, id=id)
        return self

    def t_dg(self, q0):
        return self.T_DG(q0)
    
    def T_DG(self, q0):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # join circ
        for i in range(self.qubit_num):
            if i == q0:
                self._circ[i] += "T+-"
            else:
                self._circ[i] += "---"
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=PHASE_SHIFT_T_, phase=DEF_PHASE, id=id)
        return self

    def rx(self, q0, phase=DEF_PHASE):
        return self.RX(q0,phase=phase)
    
    def RX(self, q0, phase=DEF_PHASE):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # join circ
        for i in range(self.qubit_num):
            if i == q0:
                self._circ[i] += "RX({0:1.3f})-".format(phase)
            else:
                self._circ[i] += "----------"
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=ROTATION_Y, phase=phase, id=id)
        return self

    def ry(self, q0, phase=DEF_PHASE):
        return self.RY(q0,phase=phase)
    
    def RY(self, q0, phase=DEF_PHASE):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # join circ
        for i in range(self.qubit_num):
            if i == q0:
                self._circ[i] += "RY({0:1.3f})-".format(phase)
            else:
                self._circ[i] += "----------"
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=ROTATION_Y, phase=phase, id=id)
        return self

    def rz(self, q0, phase=DEF_PHASE):
        return self.RZ(q0,phase=phase)
    
    def RZ(self, q0, phase=DEF_PHASE):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
            
        # join circ
        for i in range(self.qubit_num):
            if i == q0:
                self._circ[i] += "RZ({0:1.3f})-".format(phase)
            else:
                self._circ[i] += "----------"
            
        # operate
        id = [q0]
        self.__operate_qgate(kind=ROTATION_Z, phase=phase, id=id)
        return self

    def cx(self, q0, q1):
        return self.CX(q0, q1)
    
    def CX(self, q0, q1):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()
            
        # join circ
        for i in range(self.qubit_num):
            if i == q0:
                self._circ[i] += "*--"
            elif i == q1:
                self._circ[i] += "CX-"
            else:
                self._circ[i] += "---"
            
        # operate
        id = [q0,q1]
        self.__operate_qgate(kind=CONTROLLED_X, phase=DEF_PHASE, id=id)
        return self

    def cz(self, q0, q1):
        return self.CZ(q0, q1)
    
    def CZ(self, q0, q1):
        # error check
        if q0 >= self.qubit_num:
            raise QState_OutOfBound()
        if q1 >= self.qubit_num:
            raise QState_OutOfBound()
        if q0 == q1:
            raise QState_SameQubitID()

        # join circ
        for i in range(self.qubit_num):
            if i == q0:
                self._circ[i] += "*--"
            elif i == q1:
                self._circ[i] += "CZ-"
            else:
                self._circ[i] += "---"
            
        # operate
        id = [q0,q1]
        self.__operate_qgate(kind=CONTROLLED_Z, phase=DEF_PHASE, id=id)
        return self

    def ccx(self, q0, q1, q2):
        return self.CCX(q0, q1, q2)
    
    def CCX(self, q0, q1, q2):
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

        # join circ
        for i in range(self.qubit_num):
            if i == q0:
                self._circ[i] += "*---"
            elif i == q1:
                self._circ[i] += "*---"
            elif i == q2:
                self._circ[i] += "CCX-"
            else:
                self._circ[i] += "----"
                
        # operate
        id = [q0,q1,q2]
        self.__operate_qgate(kind=TOFFOLI, phase=DEF_PHASE, id=id)
        return self

    def m(self, id=None, shots=DEF_SHOTS, angle=0.0, phase=0.0):
        return self.M(id=id, shots=shots, angle=angle, phase=phase)
        
    def M(self, id=None, shots=DEF_SHOTS, angle=0.0, phase=0.0):
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

        # join circ
        # for i in range(self.qubit_num):
        for i in range(len(id)):
            for j in range(self.qubit_num):
                if id[i] == j:
                    self._circ[j] += "M-"
                else:
                    self._circ[j] += "--"
            
        # operate
        qubit_num = len(id)
        qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
        for i in range(len(id)):
            qubit_id[i] = id[i]
        IntArray = ctypes.c_int * MAX_QUBIT_NUM
        id_array = IntArray(*qubit_id)
        
        lib.qstate_measure.restype = ctypes.POINTER(MData)
        lib.qstate_measure.argtypes = [ctypes.POINTER(QState), ctypes.c_int,
                                       ctypes.c_double, ctypes.c_double,
                                       ctypes.c_int, IntArray]
        out = lib.qstate_measure(ctypes.byref(self), ctypes.c_int(shots),
                                 ctypes.c_double(angle), ctypes.c_double(phase),
                                 ctypes.c_int(qubit_num), id_array)

        if not out:
            raise QState_FailToMeasure()

        state_num = out.contents.state_num
        last_state = out.contents.last
        freq = ctypes.cast(out.contents.freq, ctypes.POINTER(ctypes.c_int*state_num))
        freq_list = [freq.contents[i] for i in range(state_num)]
        mdpy = MDataPy(freq_list=freq_list, last_state=last_state, qubit_num=qubit_num,
                       state_num=state_num, angle=angle, phase=phase)
        out.contents.free()

        return mdpy

    def mx(self, id=None, shots=DEF_SHOTS):
        return self.M(id=id, shots=shots, angle=0.5, phase=0.0)
        
    def MX(self, id=None, shots=DEF_SHOTS):
        return self.M(id=id, shots=shots, angle=0.5, phase=0.0)
        
    def my(self, id=None, shots=DEF_SHOTS):
        return self.M(id=id, shots=shots, angle=0.5, phase=0.5)
        
    def MY(self, id=None, shots=DEF_SHOTS):
        return self.M(id=id, shots=shots, angle=0.5, phase=0.5)
        
    def mz(self, id=None, shots=DEF_SHOTS):
        return self.M(id=id, shots=shots, angle=0.0, phase=0.0)
        
    def MZ(self, id=None, shots=DEF_SHOTS):
        return self.M(id=id, shots=shots, angle=0.0, phase=0.0)
        
    def mb(self, id=None, shots=DEF_SHOTS):
        return self.MB(id=id, shots=shots)
    
    def MB(self, id=None, shots=DEF_SHOTS):
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

        # join circ
        # for i in range(self.qubit_num):
        for i in range(len(id)):
            for j in range(self.qubit_num):
                if id[i] == j:
                    self._circ[j] += "MB-"
                else:
                    self._circ[j] += "---"
            
        # operate
        state_num = 4
        qubit_num = 2
        qubit_id = [0 for _ in range(MAX_QUBIT_NUM)]
        for i in range(qubit_num):
            qubit_id[i] = id[i]
        IntArray = ctypes.c_int * MAX_QUBIT_NUM
        id_array = IntArray(*qubit_id)
        
        lib.qstate_measure_bell.restype = ctypes.POINTER(MData)
        lib.qstate_measure_bell.argtypes = [ctypes.POINTER(QState), ctypes.c_int,
                                       ctypes.c_int, IntArray]
        out = lib.qstate_measure_bell(ctypes.byref(self), ctypes.c_int(shots),
                                      ctypes.c_int(qubit_num), id_array)

        if not out:
            raise QState_FailToMeasure()

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
        elif self.angle == 0.5 and self.phase == 0.5:
            print("direction of measurement: y-axis")
        elif self.angle == 0.0 and self.phase == 0.0:
            print("direction of measurement: z-axis")
        else:
            print("direction of measurement: theta={0:f}*PI, phi={1:f}*PI".
                  format(self.angle, self.phase))
            
        for i in range(self.state_num):
            if self.freq_list[i] != 0:
                print("frq[{0:}] = {1:d}".
                      format(format(i,'b').zfill(self.qubit_num),self.freq_list[i]))

        print("last state =>", format(self.last_state,'b').zfill(self.qubit_num))
