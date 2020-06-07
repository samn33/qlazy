# -*- coding: utf-8 -*-
import ctypes
from ctypes.util import find_library

from qlazypy.Observable import Observable
from qlazypy.error import *
from qlazypy.config import *
from qlazypy.util import *

lib = ctypes.CDLL('libqlz.'+get_lib_ext(),mode=ctypes.RTLD_GLOBAL)
libc = ctypes.CDLL(find_library("c"),mode=ctypes.RTLD_GLOBAL)

def observable_init(str=None):
    
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

def observable_free(ob):

    lib.observable_free.argtypes = [ctypes.POINTER(Observable)]
    lib.observable_free(ctypes.byref(ob))
