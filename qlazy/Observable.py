# -*- coding: utf-8 -*-
import ctypes
import warnings
import ctypes

from qlazy.config import *
from qlazy.error import *

class Observable(ctypes.Structure):
    """ Obserbavle for quantum many-body spin system. """
    
    _fields_ = [
        ('spin_num', ctypes.c_int),
        ('array_num', ctypes.c_int),
        ('spro_array', ctypes.c_void_p),
    ]

    def __new__(cls, string=None, **kwargs):
        """
        Parameters
        ----------
        string : str
            expression for the observable.

        Returns
        -------
        ob : instance of Observable
            observable corresponding to the string expression.

        Examles
        -------
        Hamiltonian for 2-body spin system : -2.0 + Z0 X1 + X0 X1
        >>> ob = Observable("-2.0+z_0*z_1+x_0+x_1")

        """
        cls.spin_num = 0
        cls.array_num = 0
        cls.spro_array = None
        obj = observable_init(string)
        ob = ctypes.cast(obj.value, ctypes.POINTER(cls)).contents
        # ob = observable_init(string)
        return ob

    def free(ob):
        """
        free memory of observable.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        # observable_free(ob)
        warnings.warn("No need to call 'free' method because free automatically, or you can use 'del' to free memory explicitly.")

    def __del__(self):
        
        observable_free(self)

# c-library for observable
from qlazy.lib.observable_c import *
