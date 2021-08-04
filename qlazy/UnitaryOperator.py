# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, ABC

class UnitaryOperator(metaclass=ABCMeta):

    """ Unitary Operator

    Attributes
    ----------
    qid : list of int
        list of qubit id.

    """
    @abstractmethod
    def __init__(self, qid=None):

        if qid is None:
            raise ValueError("'qid' is not specified")
        
        self.qid = qid
        self.qubit_num = max(qid) + 1

    @abstractmethod
    def __str__(self):
        raise NotImplemented()

    @abstractmethod
    def tenspro(self, unitary_operator):
        raise NotImplemented()
