# -*- coding: utf-8 -*-
""" Obserbavle for quantum many-body spin system. """
import ctypes

from qlazy.ObservableBase import ObservableBase

class Observable(ObservableBase):
    """ Observable for quantum many-body spin system.

    Attributes
    ----------
    string : str
        string of observable description
        ex) "-2.0 + z_0 * z_1 + x_0 + x_1" for 2-qubit system

    """
    def __init__(self, string=None):
        self.string = string

    def __str__(self):
        return self.string
