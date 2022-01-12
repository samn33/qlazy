import unittest

from qlazy import QCirc
from qlazy.config import *

class MyQCirc(QCirc):

    def __init__(self, name=None):
        self.name = name

    def get_name(self):
        return self.name
    
    def bell(self, q0, q1):
        self.h(q0).cx(q0,q1)
        return self

class TestQCirc_new(unittest.TestCase):
    """ test 'QCirc' : '__new__'
    """

    def test_init(self):
        """test '__new__'
        """
        qc = QCirc()
        self.assertEqual(qc.qubit_num, 0)
        self.assertEqual(qc.cmem_num, 0)
        self.assertEqual(qc.gate_num, 0)

class TestQCirc_append_gate(unittest.TestCase):
    """ test 'QCirc' : 'append_gate'
    """

    def test_append_gate_simple(self):
        """test 'append_gate' (simple)
        """
        qc = QCirc().h(0).cx(0,1).u3(3, alpha=0.1, beta=0.2, gamma=0.3)
        self.assertEqual(qc.qubit_num, 4)
        self.assertEqual(qc.cmem_num, 0)
        self.assertEqual(qc.gate_num, 3)
        
    def test_append_gate_with_cid(self):
        """test 'append_gate' (with cid)
        """
        qc = QCirc().h(0).cx(0,1).u3(3, alpha=0.1, beta=0.2, gamma=0.3).measure(qid=[0,5], cid=[1,2]) 
        self.assertEqual(qc.qubit_num, 6)
        self.assertEqual(qc.cmem_num, 3)
        self.assertEqual(qc.gate_num, 5)
       
    def test_append_gate_with_cid(self):
        """test 'append_gate' (with ctrl)
        """
        qc = QCirc().h(0).cx(0,1, ctrl=5).u3(3, alpha=0.1, beta=0.2, gamma=0.3)
        self.assertEqual(qc.qubit_num, 4)
        self.assertEqual(qc.cmem_num, 6)
        self.assertEqual(qc.gate_num, 3)
        

class TestQCirc_is_equal(unittest.TestCase):
    """ test 'QCirc' : 'is_equal'
    """

    def test_is_equal(self):
        """test 'is_equal'
        """
        qc_L = QCirc().h(0).cx(0,1).rx(1, phase=0.2)
        qc_R = QCirc().cu3(0, 1, alpha=0.3, beta=0.4, gamma=0.5).measure(qid=[0,1,2], cid=[0,1,2])
        qc_L_clone = qc_L.clone()
        ans = (qc_L == qc_R)
        self.assertEqual(qc_L == qc_R, False)
        self.assertEqual(qc_R != qc_L, True)
        self.assertEqual(qc_L == qc_L_clone, True)
        self.assertEqual(qc_L != qc_L_clone, False)

class TestQCirc_merge(unittest.TestCase):
    """ test 'QCirc' : 'merge'
    """

    def test_merge_2terms(self):
        """test 'merge' (2 terms)
        """
        qc_L = QCirc().h(0).cx(0,1).rx(1, phase=0.2)
        qc_R = QCirc().cu3(0, 1, alpha=0.3, beta=0.4, gamma=0.5).measure(qid=[0,1,2], cid=[0,1,2])
        qc_LR = QCirc().h(0).cx(0,1).rx(1, phase=0.2).cu3(0, 1, alpha=0.3, beta=0.4, gamma=0.5).measure(qid=[0,1,2], cid=[0,1,2])
        self.assertEqual(qc_L + qc_R == qc_LR, True)
        self.assertEqual(qc_R + qc_L == qc_LR, False)
        
    def test_merge_3terms(self):
        """test 'merge' (2 terms)
        """
        qc_1 = QCirc().h(0).cx(0,1).rx(1, phase=0.2)
        qc_2 = QCirc().cu2(0, 1, alpha=0.3, beta=0.4).measure(qid=[0,1,2], cid=[0,1,2])
        qc_3 = QCirc().x(0).z(5)
        qc_123 = QCirc().h(0).cx(0,1).rx(1, phase=0.2).cu2(0, 1, alpha=0.3, beta=0.4).measure(qid=[0,1,2], cid=[0,1,2]).x(0).z(5)
        self.assertEqual(qc_1 + qc_2 + qc_3 == qc_123, True)
        
    def test_merge_incremental(self):
        """test 'merge' (incremental)
        """
        qc_1 = QCirc().h(0).cx(0,1).rx(1, phase=0.2)
        qc_2 = QCirc().cu2(0, 1, alpha=0.3, beta=0.4).measure(qid=[0,1,2], cid=[0,1,2])
        qc_3 = QCirc().x(0).z(5)
        qc_expect = QCirc().h(0).cx(0,1).rx(1, phase=0.2).cu2(0, 1, alpha=0.3, beta=0.4).measure(qid=[0,1,2], cid=[0,1,2]).x(0).z(5)
        qc_actual = qc_1.clone()
        qc_actual += qc_2
        qc_actual += qc_3
        self.assertEqual(qc_actual == qc_expect, True)
        
class TestQCirc_kind_first(unittest.TestCase):
    """ test 'QCirc' : 'kind_first'
    """

    def test_kind_first(self):
        """test 'kind_first'
        """
        qc_L = QCirc().h(0).cx(0,1).rx(1, phase=0.2)
        qc_R = QCirc().cu2(0, 1, alpha=0.3, beta=0.4).measure(qid=[0,1,2], cid=[0,1,2])
        qc_LR = QCirc().h(0).cx(0,1).rx(1, phase=0.2).cu3(0, 1, alpha=0.3, beta=0.4, gamma=0.5).measure(qid=[0,1,2], cid=[0,1,2])
        self.assertEqual(qc_L.kind_first(), HADAMARD)
        self.assertEqual(qc_R.kind_first(), CONTROLLED_U2)
        self.assertEqual(qc_LR.kind_first(), HADAMARD)

class TestQCirc_pop_gate(unittest.TestCase):
    """ test 'QCirc' : 'pop_gate'
    """

    def test_pop_gate_not_update(self):
        """test 'pop_gate' (not update)
        """
        qc = QCirc().h(0).cx(0,1).rx(1, phase=0.2).cu3(0, 1, alpha=0.3, beta=0.4, gamma=0.5).measure(qid=[0,1,2], cid=[0,1,2])
        self.assertEqual(qc.qubit_num, 3)
        self.assertEqual(qc.cmem_num, 3)
        self.assertEqual(qc.gate_num, 7)
        (kind, qid, para, c, ctrl) = qc.pop_gate()
        self.assertEqual(kind, HADAMARD)
        self.assertEqual(qid, [0,-1])
        self.assertEqual(para, [0.0,0.0,0.0])
        self.assertEqual(c, None)
        self.assertEqual(ctrl, None)
        self.assertEqual(qc.qubit_num, 3)
        self.assertEqual(qc.cmem_num, 3)
        self.assertEqual(qc.gate_num, 6)

    def test_pop_gate_updte(self):
        """test 'pop_gate' (update)
        """
        qc = QCirc().h(5, ctrl=6).cx(0,1).rx(1, phase=0.2).cu3(0, 1, alpha=0.3, beta=0.4, gamma=0.5).measure(qid=[0,1,2], cid=[0,1,2])
        self.assertEqual(qc.qubit_num, 6)
        self.assertEqual(qc.cmem_num, 7)
        self.assertEqual(qc.gate_num, 7)
        (kind, qid, para, c, ctrl) = qc.pop_gate()
        self.assertEqual(kind, HADAMARD)
        self.assertEqual(qid, [5,-1])
        self.assertEqual(para, [0.0,0.0,0.0])
        self.assertEqual(c, None)
        self.assertEqual(ctrl, 6)
        self.assertEqual(qc.qubit_num, 3)
        self.assertEqual(qc.cmem_num, 3)
        self.assertEqual(qc.gate_num, 6)

#
# inheritance
#

class TestQCirc_inheritance(unittest.TestCase):
    """ test 'QCirc' : inheritance
    """

    def test_inheritance(self):
        """test 'inheritance'
        """
        qc_expect = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
        qc_actual = MyQCirc().bell(0,1).measure(qid=[0,1], cid=[0,1])
        self.assertEqual(qc_actual, qc_expect)

    def test_inheritance_init(self):
        """test 'inheritance_init'
        """
        qc = MyQCirc(name='hoge').h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
        s = qc.get_name()
        self.assertEqual(s, 'hoge')

if __name__ == '__main__':

    unittest.main()
