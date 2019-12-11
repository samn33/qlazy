# -*- coding: utf-8 -*-
import ctypes
from ctypes.util import find_library
from qlazypy.error import *
from qlazypy.config import *

lib = ctypes.CDLL('libQlazy.so',mode=ctypes.RTLD_GLOBAL)
libc = ctypes.CDLL(find_library("c"),mode=ctypes.RTLD_GLOBAL)

class MDataC(ctypes.Structure):

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
        lib.mdata_print.argtypes = [ctypes.POINTER(MDataC)]
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

        lib.mdata_free.argtypes = [ctypes.POINTER(MDataC)]
        lib.mdata_free(ctypes.byref(self))

class MData:

    def __init__(self, freq_list=None, last_state=0, id=None, qubit_num=0, state_num=0,
                 angle=0.0, phase=0.0, is_bell=False, tag=None):
        self.freq_list = freq_list
        self.last_state = last_state
        self.id = id
        self.qubit_num = qubit_num
        self.state_num = state_num
        self.angle = angle
        self.phase = phase
        self.is_bell = is_bell

    @property
    def frq(self):
        return self.freq_list

    @property
    def lst(self):
        return self.last_state

    def show(self):
        if self.is_bell == True:
            print("bell-measurement")
            self.__show_bell()
        elif self.angle == 0.5 and self.phase == 0.0:
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

    def __show_bell(self):
        
        for i in range(self.state_num):
            if self.freq_list[i] != 0:
                if i == BELL_PHI_PLUS:
                    state_string = 'phi+'
                elif i == BELL_PHI_MINUS:
                    state_string = 'phi-'
                elif i == BELL_PSI_PLUS:
                    state_string = 'psi+'
                elif i == BELL_PSI_MINUS:
                    state_string = 'psi-'
                print("frq[{0:}] = {1:d}".
                      format(state_string, self.freq_list[i]))

        if self.last_state == BELL_PHI_PLUS:
            state_string = 'phi+'
        elif self.last_state == BELL_PHI_MINUS:
            state_string = 'phi-'
        elif self.last_state == BELL_PSI_PLUS:
            state_string = 'psi+'
        elif self.last_state == BELL_PSI_MINUS:
            state_string = 'psi-'
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
