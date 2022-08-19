# -*- coding: utf-8 -*-
""" wrapper functions for ObservableBase """
import ctypes
from ctypes.util import find_library
import pathlib

from qlazy.util import get_lib_ext
from qlazy.ObservableBase import ObservableBase

lib = ctypes.CDLL(str(pathlib.Path(__file__).with_name('libqlz.'+get_lib_ext())))
libc = ctypes.CDLL(find_library("c"), mode=ctypes.RTLD_GLOBAL)

def observable_base_init(ostr):
    """ initialize ObservableBase object """

    c_str = ctypes.create_string_buffer(ostr.encode('utf-8'))

    observ = None
    c_observ = ctypes.c_void_p(observ)

    lib.observable_base_init.restype = ctypes.c_bool
    lib.observable_base_init.argtypes = [ctypes.POINTER(ctypes.c_char),
                                    ctypes.POINTER(ctypes.c_void_p)]
    ret = lib.observable_base_init(c_str, c_observ)

    if ret is False:
        raise ValueError("can't initialize ObservableBase object.")

    return c_observ

def observable_base_free(ob):
    """ free memory of ObservableBase object """

    lib.observable_base_free.argtypes = [ctypes.POINTER(ObservableBase)]
    lib.observable_base_free(ctypes.byref(ob))
