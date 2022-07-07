# -*- coding: utf-8 -*-
""" wrapper functions for Observable """
import ctypes
from ctypes.util import find_library
import pathlib

from qlazy.util import get_lib_ext
from qlazy.Observable import Observable

lib = ctypes.CDLL(str(pathlib.Path(__file__).with_name('libqlz.'+get_lib_ext())))
libc = ctypes.CDLL(find_library("c"), mode=ctypes.RTLD_GLOBAL)

def observable_init(ostr):
    """ initialize Observable object """

    c_str = ctypes.create_string_buffer(ostr.encode('utf-8'))

    observ = None
    c_observ = ctypes.c_void_p(observ)

    lib.observable_init.restype = ctypes.c_bool
    lib.observable_init.argtypes = [ctypes.POINTER(ctypes.c_char),
                                    ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.observable_init(c_str, c_observ)

    if ret is False:
        raise ValueError("can't initialize Observable object.")

    return c_observ

def observable_free(ob):
    """ free memory of Observable object """

    lib.observable_free.argtypes = [ctypes.POINTER(Observable)]
    lib.observable_free(ctypes.byref(ob))
