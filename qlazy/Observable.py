# -*- coding: utf-8 -*-
""" Obserbavle for quantum many-body spin system. """
import ctypes

from qlazy.util import is_num
from qlazy.ObservableBase import ObservableBase
from qlazy.PauliProduct import PauliProduct

class Observable(ObservableBase):
    """ Observable for quantum many-body spin system.

    Attributes
    ----------
    string : str
        string of observable description
        ex) "-2.0 + z_0 * z_1 + x_0 + x_1" for 2-qubit system
    weighted_pp_list : list of dict (weight:pauli_product)
        weighted pauli product list

    """
    def __init__(self, string=None):
        self.string = string

    def __str__(self):

        s = ""
        for weighted_pp in self.weighted_pp_list:
            if weighted_pp['weight'] > 0.0:
                sign = '+'
            else:
                sign = '-'
            if abs(weighted_pp['weight']) == 1.0:
                weight_str = ' '
            else:
                weight_str = ' ' + str(abs(weighted_pp['weight'])) + ' '
            pp_str = weighted_pp['pp'].__str__()
            s += (sign + weight_str + pp_str + ' ')
        
        s = s.strip()
        if list(s)[0] == '+':
            s = s.lstrip('+').lstrip()
        return s

    @property
    def weighted_pp_list(self):
        return self.get_weighted_pp_list()

    def get_weighted_pp_list(self):
        """
        get weighted pauli product list.

        Parameters
        ----------
        None

        Returns
        -------
        weighted_pp_list : list of dict (weight:pauli_product)
            weighted pauli product list

        """
        weighted_pp_list = []

        terms_list = self.string.replace('+', '+ 1.0 *').replace('-', '+ - 1.0 *').split('+')
        for term in terms_list:
            if term == '':
                continue
            items_list = term.split('*')
            weight = 1.0
            spin_product = []
            for x in items_list:
                item = x.replace(' ', '')
                if is_num(item) is True:
                    weight = weight * float(item)
                    continue
                kind_idx = [x.strip() for x in item.split('_')]  # ex) kind_idx = ['x', '1']
                if (len(kind_idx) != 2 or kind_idx[0] not in ('x', 'y', 'z') or
                    kind_idx[1].isdecimal() is False):
                    raise ValueError("invalid string of observable")
                spin_product.append(kind_idx)

            # spin_product to pauli_product
            # ex) spin_product = [['x', '1'], ['z', 0], ..]
            pauli_str = ""
            qid = []
            for spin in spin_product:
                pauli_str += spin[0].upper()
                qid.append(int(spin[1]))
            pp = PauliProduct(pauli_str=pauli_str, qid=qid)

            weighted_pp_list.append({'weight': weight, 'pp': pp})

        return weighted_pp_list
