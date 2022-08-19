# -*- coding: utf-8 -*-
""" Obserbavle for quantum many-body spin system. """
import ctypes

class ObservableBase(ctypes.Structure):
    """ Observable for quantum many-body spin system. """

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
        obj = observable_base_init(string)
        ob = ctypes.cast(obj.value, ctypes.POINTER(cls)).contents
        return ob

    def __del__(self):

        observable_base_free(self)

# c-library for observable
from qlazy.lib.observable_base_c import observable_base_init, observable_base_free
