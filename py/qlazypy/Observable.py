# -*- coding: utf-8 -*-
import ctypes
import random
import numpy as np
from ctypes.util import find_library
from qlazypy.error import *
from qlazypy.config import *
from qlazypy.util import get_lib_ext

lib = ctypes.CDLL('libqlz.'+get_lib_ext(),mode=ctypes.RTLD_GLOBAL)
libc = ctypes.CDLL(find_library("c"),mode=ctypes.RTLD_GLOBAL)

class Observable(ctypes.Structure):

    _fields_ = [
        ('spin_num', ctypes.c_int),
        ('array_num', ctypes.c_int),
        ('spro_array', ctypes.c_void_p),
    ]

    def __new__(cls, str=None):

        cls.spin_num = 0
        cls.array_num = 0
        cls.spro_array = None
    
        c_str = ctypes.create_string_buffer(str.encode('utf-8'))

        observ = None
        c_observ = ctypes.c_void_p(observ)
        
        lib.observable_init.restype = ctypes.c_int
        lib.observable_init.argtypes = [ctypes.POINTER(ctypes.c_char),
                                        ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.observable_init(c_str, c_observ)

        if ret == FALSE:
            raise Observable_Error_Initialize()
        
        out = ctypes.cast(c_observ.value, ctypes.POINTER(Observable))

        return out.contents

    def free(self):

        lib.observable_free.argtypes = [ctypes.POINTER(Observable)]
        lib.observable_free(ctypes.byref(self))
