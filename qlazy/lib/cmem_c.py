# -*- coding: utf-8 -*-
""" wrapper functions for CMem """
import ctypes
from ctypes.util import find_library
import pathlib

import qlazy.config as cfg
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

    lib.cmem_init.restype = ctypes.c_int
    lib.cmem_init.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.cmem_init(ctypes.c_int(cmem_num), c_cmem)

    if ret == cfg.FALSE:
        raise ValueError("can't initialize cmem.")

    return c_cmem

def cmem_copy(cm):
    """ copy classical memory """

    cmem = None
    c_cmem = ctypes.c_void_p(cmem)

    lib.cmem_copy.restype = ctypes.c_int
    lib.cmem_copy.argtypes = [ctypes.POINTER(CMem),
                              ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.cmem_copy(ctypes.byref(cm), c_cmem)

    if ret == cfg.FALSE:
        raise ValueError("can't copy cmem.")

    return c_cmem

def cmem_free(cmem):
    """ free classical memory """

    lib.cmem_free.argtypes = [ctypes.POINTER(CMem)]
    lib.cmem_free(ctypes.byref(cmem))
