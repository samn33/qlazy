# -*- coding: utf-8 -*-
""" gpu related functions """

from qlazy.lib.gpu_c import (wrap_is_gpu_available, wrap_is_gpu_supported_lib,
                             wrap_gpu_preparation)

def is_gpu_available():
    """ cuda is available or not """

    return wrap_is_gpu_available()

def is_gpu_supported_lib():
    """ this qlazy library supports cuda executoin or not """

    return wrap_is_gpu_supported_lib()

def gpu_preparation():
    """ memory allocation and free (dummy) """

    return wrap_gpu_preparation()
