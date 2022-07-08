# -*- coding: utf-8 -*-
""" wrapper functions for CMem """
import ctypes
from ctypes.util import find_library
import pathlib
import numpy as np

from qlazy.util import get_lib_ext
from qlazy.CMem import CMem

lib = ctypes.CDLL(str(pathlib.Path(__file__).with_name('libqlz.'+get_lib_ext())))
libc = ctypes.CDLL(find_library("c"), mode=ctypes.RTLD_GLOBAL)

def cmem_init(cmem_num):
    """ initialize classical memory """

    if cmem_num < 1:
        raise ValueError("cmem size must be positive integer.")

    cmem = None
    c_cmem = ctypes.c_void_p(cmem)

    lib.cmem_init.restype = ctypes.c_bool
    lib.cmem_init.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.cmem_init(ctypes.c_int(cmem_num), c_cmem)

    if ret is False:
        raise ValueError("can't initialize cmem.")

    return c_cmem

def cmem_copy(cm):
    """ copy classical memory """

    cmem = None
    c_cmem = ctypes.c_void_p(cmem)

    lib.cmem_copy.restype = ctypes.c_bool
    lib.cmem_copy.argtypes = [ctypes.POINTER(CMem),
                              ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.cmem_copy(ctypes.byref(cm), c_cmem)

    if ret is False:
        raise ValueError("can't copy cmem.")

    return c_cmem

def cmem_get_bits(cmem):
    """ get bits of the classical memory """

    if cmem is None:
        raise Valueerror("cmem must be set.")

    cmem_num = cmem.cmem_num
    bits = None
    c_bits = ctypes.c_void_p(bits)

    lib.cmem_get_bits.restype = ctypes.c_bool
    lib.cmem_get_bits.argtypes = [ctypes.POINTER(CMem), ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.cmem_get_bits(ctypes.byref(cmem), c_bits)

    if ret is False:
        raise ValueError("can't get element of the classical memory.")

    o = ctypes.cast(c_bits.value, ctypes.POINTER(ctypes.c_ubyte))

    out = [o[i] for i in range(cmem_num)]
    
    libc.free.argtypes = [ctypes.POINTER(ctypes.c_ubyte)]
    libc.free(o)

    return np.array(out)

def cmem_set_bits(cmem, bits):
    """ get bits of the classical memory """

    # bool cmem_set_bits(CMem* cmem, BYTE* bits, int num)
    if cmem is None:
        raise Valueerror("cmem must be set.")

    cmem_num = cmem.cmem_num
    num = len(bits)

    ByteArray = ctypes.c_char * cmem_num
    c_bits = ByteArray(*bits)

    lib.cmem_set_bits.restype = ctypes.c_bool
    lib.cmem_set_bits.argtypes = [ctypes.POINTER(CMem), ByteArray, ctypes.c_int]
    ret = lib.cmem_set_bits(ctypes.byref(cmem), c_bits, ctypes.c_int(num))

    if ret is False:
        raise ValueError("can't set element of the classical memory.")

def cmem_free(cmem):
    """ free classical memory """

    lib.cmem_free.argtypes = [ctypes.POINTER(CMem)]
    lib.cmem_free(ctypes.byref(cmem))
