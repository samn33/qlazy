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

class Observable(ctypes.Structure):

    _fields_ = [
        ('spin_num', ctypes.c_int),
        ('array_num', ctypes.c_int),
        ('spro_array', ctypes.c_void_p),
    ]

    def __new__(self, str=None):

        self.spin_num = 0
        self.array_num = 0
        self.spro_array = None
    
        c_str = ctypes.create_string_buffer(str.encode('utf-8'))

        observ = None
        c_observ = ctypes.c_void_p(observ)
        
        lib.observable_init.restype = ctypes.c_int
        lib.observable_init.argtypes = [ctypes.POINTER(ctypes.c_char),
                                        ctypes.POINTER(ctypes.c_void_p)]
        ret = lib.observable_init(c_str, c_observ)

        if ret == FALSE:
            raise Observable_FailToInitialize()
        
        out = ctypes.cast(c_observ.value, ctypes.POINTER(Observable))

        return out.contents

    def free(self):

        lib.observable_free.argtypes = [ctypes.POINTER(Observable)]
        lib.observable_free(ctypes.byref(self))
