# -*- coding: utf-8 -*-
import ctypes
from ctypes.util import find_library
import numpy as np
import pathlib

from qlazy.config import *
from qlazy.error import *
from qlazy.util import *
from qlazy.CMem import CMem

lib= ctypes.CDLL(str(pathlib.Path(__file__).with_name('libqlz.'+get_lib_ext())))
libc = ctypes.CDLL(find_library("c"),mode=ctypes.RTLD_GLOBAL)

def cmem_init(cmem_num):

    cmem = None
    c_cmem = ctypes.c_void_p(cmem)

    lib.cmem_init.restype = ctypes.c_int
    lib.cmem_init.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.cmem_init(ctypes.c_int(cmem_num), c_cmem)

    if ret == FALSE:
        raise CMem_Error_Initialize()

    out = ctypes.cast(c_cmem.value, ctypes.POINTER(CMem))
        
    return out.contents
    
def cmem_free(cmem):

    lib.cmem_free.argtypes = [ctypes.POINTER(CMem)]
    lib.cmem_free(ctypes.byref(cmem))
