# -*- coding: utf-8 -*-
""" wrapper functions related to gpu """
import ctypes
import pathlib

from qlazy.util import get_lib_ext

lib = ctypes.CDLL(str(pathlib.Path(__file__).with_name('libqlz.'+get_lib_ext())))

def wrap_is_gpu_available():
    """ cuda is available or not """

    lib.is_gpu_available.restype = ctypes.c_bool
    ret = lib.is_gpu_available()
    return ret

def wrap_is_gpu_supported_lib():
    """ this qlazy library supports cuda executoin or not """

    lib.is_gpu_supported_lib.restype = ctypes.c_bool
    ret = lib.is_gpu_supported_lib()
    return ret

def wrap_gpu_preparation():
    """ memory allocation and free (dummy) """

    lib.gpu_preparation.restype = ctypes.c_bool
    ret = lib.gpu_preparation()
    return ret
