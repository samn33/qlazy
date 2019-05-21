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
        
        lib.observable_init.restype = ctypes.POINTER(Observable)
        lib.observable_init.argtypes = [ctypes.POINTER(ctypes.c_char)]
        out = lib.observable_init(c_str)

        if not out:
            raise Observable_FailToInitialize()
        
        return out.contents

    def __del__(self):

        lib.observable_free.argtypes = [ctypes.POINTER(Observable)]
        lib.observable_free(ctypes.byref(self))

