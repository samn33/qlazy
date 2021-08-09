# -*- coding: utf-8 -*-

from qlazy.UnitaryOperator import UnitaryOperator
        
class PauliProduct(UnitaryOperator):

    """ Pauli Product

    Attributes
    ----------
    qid : list of int
        list of qubit id.
    pauli_list : list of str
        list of pauli operators.

    """
    def __init__(self, pauli_str=None, qid=None):
        """
        Parameters
        ----------
        pauli_str : str
            string representation of Pauli Product.
            ex) "XZZY"
        qid : list of int, default - [0,1,..,len(pauli_str)-1]
            list of qubit id.
            ex) [1, 0, 3, 6]

        Notes
        -----
        'pauli_str' must consist of 'X','Y','Z', and length of 'pauli_str' must be equal to length of 'qid'

        Examples
        --------
        >>> pp = PauliProduct(pauli_str ="XZZY", qid=[1, 0, 3, 6])
        represent Pauli Product : X1*Z0*Z3*Y6.
        >>> pp = PauliProduct(pauli_str ="I")
        represent identity.

        """
        if pauli_str is None:
            raise ValueError("pauli_str or qid is not specified")
        if qid is None:
            qid = [i for i in range(len(pauli_str))]
    
        if len(pauli_str) != len(qid):
            raise ValueError("length of 'pauli_str' is not equal to length of 'qid'")
        elif len(qid) != len(set(qid)):
            raise ValueError("some elements of 'qid' are duplicated")
        elif sum([0 if p in ['X','Y','Z','I'] else 1 for p in list(pauli_str)]) > 0:
            raise ValueError("'pauli_str' must consist of 'X','Y','Z'")

        qid_sorted = []
        pauli_list_sorted = []

        if list(set(pauli_str)) == ['I']:
            qid_sorted = [0]
            pauli_list_sorted = ['I']
        else:
            for q, p in sorted(zip(qid, list(pauli_str))):
                if p == 'I': continue
                qid_sorted.append(q)
                pauli_list_sorted.append(p)

        super().__init__(qid=qid_sorted)
        self.pauli_list = pauli_list_sorted

    def __str__(self):

        pauli_product = ""
        for i,p in sorted(zip(self.qid, self.pauli_list)):
            pauli_product += "{0:}({1:}) ".format(p, str(i))

        pauli_product = pauli_product.rstrip()
        return pauli_product

    def get_binary_rep(self, qubit_num=None):
        """
        get binary representation of pauli product.

        Parameters
        ----------
        qubit_num : int, default - max(self.qid)+1
            qubit number of binary representation.

        Returns
        -------
        binary_rep : list of int
            output binary representation of the pauli product.

        Examples
        --------
        >>> pp = PauliProduct(pauli_str="XYZ", qid=[0,1,2])
        >>> print(pp.get_binary_rep())
        [1,1,0,0,1,1]

        """
        if qubit_num is None:
            qubit_num = self.qubit_num

        if qubit_num < max(self.qid) + 1:
            raise Valueerror("qubit_num is smaller than the size required by pauli product")
            
        binary_rep = [0] * qubit_num * 2
        for q in range(qubit_num):
            if q in self.qid:
                i = self.qid.index(q)
                if self.pauli_list[i] == 'X':
                    binary_rep[q] = 1
                elif self.pauli_list[i] == 'Z':
                    binary_rep[qubit_num + q] = 1
                elif self.pauli_list[i] == 'Y':
                    binary_rep[q] = 1
                    binary_rep[qubit_num + q] = 1

        return binary_rep

    def is_commute(self, pp):
        """
        is pauli product commute to other pauli product or not.

        Parameters
        ----------
        pp : instance of PauliProduct
            pauli product

        Returns
        -------
        ans : bool
            commute (True) or anti-commute (False)

        """
        qubit_num = max(max(self.qid), max(pp.qid)) + 1

        binary_rep_self = self.get_binary_rep(qubit_num)
        binary_rep_pp = pp.get_binary_rep(qubit_num)

        inner_prod = 0
        for i in range(qubit_num):
            inner_prod += (binary_rep_self[i] * binary_rep_pp[qubit_num + i])
            inner_prod += (binary_rep_self[qubit_num + i] * binary_rep_pp[i])
        inner_prod = inner_prod % 2

        if inner_prod == 0:
            ans = True
        else:
            ans = False
        
        return ans

    def tenspro(self, pp):
        """
        get tensor product with other pauli product.

        Parameters
        ----------
        pp : instance of PauliProduct
            pauli product

        Returns
        -------
        pp_out : instance of PauliProduct
            output pauli product

        """
        qubit_num = max(max(self.qid), max(pp.qid)) + 1
        
        binary_rep_self = self.get_binary_rep(qubit_num)
        binary_rep_pp = pp.get_binary_rep(qubit_num)

        binary_rep = [(bs + bp) % 2 for bs, bp in zip(binary_rep_self, binary_rep_pp)]

        pauli_list = []
        qid = []
        for i in range(qubit_num):
            if binary_rep[i] == 1 and binary_rep[qubit_num + i] == 1:
                pauli_list.append('Y')
                qid.append(i)
            elif binary_rep[i] == 1:
                pauli_list.append('X')
                qid.append(i)
            elif binary_rep[qubit_num + i] == 1:
                pauli_list.append('Z')
                qid.append(i)

        pauli_str = ''.join(pauli_list)

        pp_out = PauliProduct(pauli_str=pauli_str, qid=qid)

        return pp_out
