# -*- coding: utf-8 -*-
""" Obserbavle for quantum many-body spin system. """

from qlazy.util import is_num
from qlazy.ObservableBase import ObservableBase
from qlazy.PauliProduct import PauliProduct

def X(q):
    """
    Parameters
    ----------
    q : int
        qubit id

    Returns
    -------
    ob : instance of Observable
        obserbable X(q)

    """
    ob = Observable().add_wpp(weight=1.0, pp=PauliProduct(pauli_str='X', qid=[q]))
    return ob

def Y(q):
    """
    Parameters
    ----------
    q : int
        qubit id

    Returns
    -------
    ob : instance of Observable
        obserbable Y(q)

    """
    ob = Observable().add_wpp(weight=1.0, pp=PauliProduct(pauli_str='Y', qid=[q]))
    return ob

def Z(q):
    """
    Parameters
    ----------
    q : int
        qubit id

    Returns
    -------
    ob : instance of Observable
        obserbable X(q)

    """
    ob = Observable().add_wpp(weight=1.0, pp=PauliProduct(pauli_str='Z', qid=[q]))
    return ob

class Observable:
    """ Observable for quantum many-body spin system.

    Attributes
    ----------
    base : instance of ObservableBase
        observable
    string : str
        string of observable description
        ex) "-2.0+Z_0*Z_1+X_0+X_1" for 2-qubit system
    weighted_pp_list : list of dict ({'weight':weight, 'pp':pauli_product})
        weighted pauli product list

    """
    def __init__(self, string=None):
        """
        Parameters
        ----------
        string : str
            string of observable description
            ex) "-2.0+Z_0*Z_1+X_0+X_1" for 2-qubit system

        """
        if string is not None:
            self.weighted_pp_list = self.get_weighted_pp_list(string)
        else:
            self.weighted_pp_list = []

    def __str__(self):

        ob = self.clone()
        if ob.recalc_weight() is False:
            raise ValueError("Observable is not hermitian.")
            
        term_str_list = []
        for weighted_pp in ob.weighted_pp_list:
            if weighted_pp['weight'] > 0.0:
                sign = '+ '
            else:
                sign = '- '

            p_str_list = []
            for i, p_str in enumerate(weighted_pp['pp'].pauli_list):
                if p_str == 'I':
                    continue
                q = weighted_pp['pp'].qid[i]
                p_str_list.append("{}({})".format(p_str.upper(), str(q)))

            if abs(weighted_pp['weight']) == 1.0:
                if p_str_list == []:
                    weight_str = str(abs(weighted_pp['weight']))
                else:
                    weight_str = ''
            else:
                weight_str = str(abs(weighted_pp['weight']))

            if p_str_list == []:
                pp_str = sign + weight_str
            elif weight_str != '':
                pp_str = sign + weight_str + ' ' + ' '.join(p_str_list)
            else:
                pp_str = sign + weight_str + ' '.join(p_str_list)

            term_str_list.append(pp_str)

        s = " ".join(term_str_list)
        
        s = s.strip()
        if s != '' and list(s)[0] == '+':
            s = s.lstrip('+').lstrip(' ')
        return s

    def __eq__(self, ob):
        """
        Parameters
        ----------
        ob : instance of Observable
            obervable

        Returns
        -------
        ans : bool
            True if equal

        """
        ob_1 = self.clone()
        ob_2 = ob.clone()
        
        if ob_1.recalc_weight() is False:
            raise ValueError("Observable is not hermitian.")
            
        if ob_2.recalc_weight() is False:
            raise ValueError("Observable is not hermitian.")
            
        if len(ob_1.weighted_pp_list) != len(ob_2.weighted_pp_list):
            ans = False
            return ans

        for wpp in ob_1.weighted_pp_list:
            pp = wpp['pp']
            i, w = ob_2.get_idx_weight(pp)
            if w == wpp['weight']:
                ans = True
            else:
                ans = False
                break

        return ans

    def __neq__(self, ob):
        """
        Parameters
        ----------
        ob : instance of Observable
            obervable

        Returns
        -------
        ans : bool
            True if not equal

        """
        ans = not self.__eq__(ob)
        return ans

    def __pos__(self):
        """
        Parameters
        ----------
        None

        Returns
        -------
        out : instance of Observable
            observable (result)

        """
        return self

    def __neg__(self):
        """
        Parameters
        ----------
        None

        Returns
        -------
        out : instance of Observable
            observable (result)

        """
        self *= -1.0
        return self

    def __add__(self, other):
        """
        Parameters
        ----------
        other : instance of Observable
            observable

        Returns
        -------
        out : instance of Observable
            observable (result)

        """
        out = Observable()
        for wpp in self.weighted_pp_list:
            if wpp['weight'] != 0.0:
                out.add_wpp(weight=wpp['weight'], pp=wpp['pp'])

        if isinstance(other, Observable):
            for wpp in other.weighted_pp_list:
                if wpp['weight'] != 0.0:
                    out.add_wpp(weight=wpp['weight'], pp=wpp['pp'])
        elif isinstance(other, int) or isinstance(other, float):
            if other != 0.0:
                out.add_wpp(weight=other, pp=PauliProduct('I', [0]))
        else:
            raise TypeError("Can't add a Observable with {}".format(type(other)))
                
        return out

    __radd__ = __add__

    def __iadd__(self, other):
        """
        Parameters
        ----------
        other : instance of Observable
            observable

        Returns
        -------
        self : instance of Observable
            observable (result)

        """
        out = self.__add__(other)
        self.weighted_pp_list = out.weighted_pp_list[:]
        return self

    def __sub__(self, other):
        """
        Parameters
        ----------
        other : instance of Observable
            observable

        Returns
        -------
        out : instance of Observable
            observable (result)

        """
        out = Observable()
        for wpp in self.weighted_pp_list:
            if wpp['weight'] != 0.0:
                out.add_wpp(weight=wpp['weight'], pp=wpp['pp'])

        if isinstance(other, Observable):
            for wpp in other.weighted_pp_list:
                if wpp['weight'] != 0.0:
                    out.add_wpp(weight=-wpp['weight'], pp=wpp['pp'])
        elif isinstance(other, int) or isinstance(other, float):
            if other != 0.0:
                out.add_wpp(weight=-other, pp=PauliProduct('I', [0]))
        else:
            raise TypeError("Can't sub a Observable with {}".format(type(other)))
                
        return out

    def __rsub__(self, other):

        out = -1.0 * self.__sub__(other)
        return out

    def __isub__(self, other):
        """
        Parameters
        ----------
        other : instance of Observable
            observable

        Returns
        -------
        self : instance of Observable
            observable (result)

        """
        out = self.__sub__(other)
        self.weighted_pp_list = out.weighted_pp_list[:]
        return self

    def __mul__(self, other):
        """
        Parameters
        ----------
        other : instance of Observable / int / float
            observable / number

        Returns
        -------
        self : instance of Observable
            observable (result)

        """
        if isinstance(other, Observable):
            out = Observable()
            for wpp_1 in self.weighted_pp_list:
                for wpp_2 in other.weighted_pp_list:
                    pp = wpp_1['pp'] * wpp_2['pp']
                    weight = wpp_1['weight'] * wpp_2['weight']
                    if weight != 0.0:
                        out.add_wpp(weight=weight, pp=pp)
        elif isinstance(other, int) or isinstance(other, float):
            out = Observable()
            for wpp in self.weighted_pp_list:
                if wpp['weight']*other != 0.0:
                    out.add_wpp(weight=wpp['weight']*other, pp=wpp['pp'])
        else:
            raise TypeError("Can't mul a Observable with {}".format(type(other)))
        
        return out

    __rmul__ = __mul__
        
    def __imul__(self, other):
        """
        Parameters
        ----------
        other : instance of Observable / int / float
            observable / number

        Returns
        -------
        self : instance of Observable
            observable (result)

        """
        out = self.__mul__(other)
        self.weighted_pp_list = out.weighted_pp_list[:]
        return self

    def __pow__(self, other):
        """
        Parameters
        ----------
        other : instance of Observable / int / float
            observable / number

        Returns
        -------
        out : instance of Observable
            observable (result)

        """
        if isinstance(other, int):
            if other < 1:
                raise ValueError("Can't execute {}-th power".format(other))
            out = self.clone()
            for _ in range(other - 1):
                out = out * self
        else:
            raise TypeError("Can't pow a Observable with {}".format(type(other)))

        return out

    def __truediv__(self, other):
        """
        Parameters
        ----------
        other : int / float
            number

        Returns
        -------
        out : instance of Observable
            observable (result)

        """
        if isinstance(other, int) or isinstance(other, float):
            out = Observable()
            for wpp in self.weighted_pp_list:
                out.add_wpp(weight=wpp['weight']/other, pp=wpp['pp'])
        else:
            raise TypeError("Can't div a Observable with {}".format(type(other)))
                
        return out

    def __itruediv__(self, other):
        """
        Parameters
        ----------
        other : int / float
            number

        Returns
        -------
        out : instance of Observable
            observable (result)

        """
        out = self.__truediv__(other)
        self.weighted_pp_list = out.weighted_pp_list[:]
        return self

    def is_hermitian(self):
        """ hermitian or not

        Parameters
        ----------
        None

        Returns
        -------
        ans : bool
            is the observable hermitian or not

        """
        ans = True
        for wpp in self.weighted_pp_list:
            weight = wpp['weight'] * wpp['pp'].factor
            if weight.imag != 0.0:
                ans = False
                break
        return ans

    def recalc_weight(self):
        """ recalculate the weights of weighted_pp_list
            (weight <= weight * pp.factor, pp.factor <= 1.0)

        Parameters
        ----------
        None

        Returns
        -------
        ans : bool
            is the observable hermitian or not

        """
        ans = True
        for wpp in self.weighted_pp_list:
            weight = wpp['weight'] * wpp['pp'].factor
            if weight.imag != 0.0:
                ans = False
                break
            wpp['weight'] = weight.real
            wpp['pp'].factor = 1.+0.j
        return ans
    
    @property
    def base(self):
        return self.get_observable_base()
    
    def get_observable_base(self):
        """ get ObservableBase instance.

        Parameters
        ----------
        None

        Returns
        -------
        ob_base : instance of ObservableBase
            observable

        """
        ob_base = ObservableBase(self.string)
        return ob_base
        
    @property
    def string(self):
        return self.get_string()

    def get_string(self):
        """ get string of observable.

        Parameters
        ----------
        None

        Returns
        -------
        s : str
            string of observable

        """
        ob = self.clone()
        if ob.recalc_weight() is False:
            raise ValueError("Observable is not hermitian.")

        term_str_list = []
        for weighted_pp in ob.weighted_pp_list:
            if weighted_pp['weight'] > 0.0:
                sign = '+'
            else:
                sign = '-'

            p_str_list = []
            for i, p_str in enumerate(weighted_pp['pp'].pauli_list):
                if p_str == 'I':
                    continue
                q = weighted_pp['pp'].qid[i]
                p_str_list.append("{}_{}".format(p_str.upper(), str(q)))

            if abs(weighted_pp['weight']) == 1.0:
                if p_str_list == []:
                    weight_str = str(abs(weighted_pp['weight']))
                else:
                    weight_str = ''
            else:
                weight_str = str(abs(weighted_pp['weight'])) + '*'

            if p_str_list == []:
                pp_str = (sign + weight_str).rstrip('*')
            else:
                pp_str = sign + weight_str + "*".join(p_str_list)

            term_str_list.append(pp_str)

        s = "".join(term_str_list)
        
        s = s.strip()
        if s != '' and list(s)[0] == '+':
            s = s.lstrip('+')
        return s

    def get_weighted_pp_list(self, string):
        """
        get weighted pauli product list.

        Parameters
        ----------
        string : str
            string of observable

        Returns
        -------
        weighted_pp_list : list of dict (weight:pauli_product)
            weighted pauli product list

        """
        weighted_pp_list = []

        terms_list = string.replace(' ', '').replace('+', '+1.0*').replace('-', '+-1.0*').split('+')
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
                kind_idx = [x.strip() for x in item.split('_')]  # ex) kind_idx = ['X', '1']
                if (len(kind_idx) != 2 or kind_idx[0] not in ('x', 'y', 'z', 'X', 'Y', 'Z') or
                    kind_idx[1].isdecimal() is False):
                    raise ValueError("invalid string of observable")
                spin_product.append(kind_idx)

            # spin_product to pauli_product
            # ex) spin_product = [['X', '1'], ['Z', 0], ..]
            pauli_str = ""
            qid = []
            for spin in spin_product:
                pauli_str += spin[0].upper()
                qid.append(int(spin[1]))
            if spin_product == []:
                pauli_str = 'I'
                qid = [0]
            pp = PauliProduct(pauli_str=pauli_str, qid=qid)

            if weight != 0.0:
                weighted_pp_list.append({'weight': weight, 'pp': pp})

        return weighted_pp_list

    def get_idx_weight(self, pp):
        """
        get index and weight value correspond to the pauli product.

        Parameters
        ----------
        pp : instance of PauliProduct
            pauli product

        Returns
        -------
        idx : int
           index number of the list (self.weighted_pp_list) correspond to the pauli product
        weight : float
           weight value correspond to the pauli product

        """
        pp_list = [self.weighted_pp_list[i]['pp'] for i in range(len(self.weighted_pp_list))]
        weight_list = [self.weighted_pp_list[i]['weight'] for i in range(len(self.weighted_pp_list))]
        if pp in pp_list:
            idx = pp_list.index(pp)
            weight = self.weighted_pp_list[idx]['weight']
        else:
            idx = None
            weight = 0.0

        return idx, weight

    def clone(self):
        """
        clone observable.

        Parameters
        ----------
        None

        Returns
        -------
        ob : instance of Observable
            observable

        """
        ob = Observable()
        ob.weighted_pp_list = self.weighted_pp_list[:]
        return ob

    def add_wpp(self, weight=1.0, pp=None):
        """
        add the weighted pauli product to the list (self.weighted_pp_list).

        Parameters
        ----------
        weight : float
           weight value correspond to the pauli product
        pp : instance of PauliProduct
            pauli product

        Returns
        -------
        self : instance of Ovservable
            observable after adding weighted pauli product

        """
        if weight == 0.0:
            return self

        if pp is None: # constant term, not include pauli product
            pp = PauliProduct(pauli_str='I', qid=[0])

        i, w = self.get_idx_weight(pp)
        if w == 0.0:
            w = weight
            self.weighted_pp_list.append({'weight': w, 'pp': pp})
        else:
            w += weight
            if w == 0.0:
                self.weighted_pp_list.pop(i)
            else:
                self.weighted_pp_list[i]['weight'] = w

        return self
