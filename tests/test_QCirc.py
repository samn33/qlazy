import unittest
import math
import numpy as np
import pyzx as zx

from pyzx import Circuit
from qlazy import QState, QCirc, Backend, PauliProduct
from qlazy.config import *

EPS = 1.0e-6

def equal_or_not(qs_A, qs_B):

    fid = qs_A.fidelity(qs_B)
    if abs(fid - 1.0) < EPS:
        return True
    else:
        return False

def valid_or_not(qc):

    bk = Backend(product='ibmq', device='aer_simulator')
    res = bk.run(qcirc=qc)
    qasm_A = res.info['quantum_circuit'].qasm()
    qasm_B = qc.to_qasm()
    circ_A = Circuit.from_qasm(qasm_A)
    circ_B = Circuit.from_qasm(qasm_B)
    ans = circ_A.verify_equality(circ_B)
    return ans

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
        qc = QCirc().h(0).cx(0,1).rx(3, phase=0.1)
        self.assertEqual(qc.qubit_num, 4)
        self.assertEqual(qc.cmem_num, 0)
        self.assertEqual(qc.gate_num, 3)
        
    def test_append_gate_with_cid(self):
        """test 'append_gate' (with cid)
        """
        qc = QCirc().h(0).cx(0,1).rx(3, phase=0.1).measure(qid=[0,5], cid=[1,2]) 
        self.assertEqual(qc.qubit_num, 6)
        self.assertEqual(qc.cmem_num, 3)
        self.assertEqual(qc.gate_num, 5)
       
    def test_append_gate_with_cid(self):
        """test 'append_gate' (with ctrl)
        """
        qc = QCirc().h(0).cx(0,1, ctrl=5).rx(3, phase=0.1)
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
        qc_R = QCirc().crx(0, 1, phase=0.3).measure(qid=[0,1,2], cid=[0,1,2])
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
        qc_R = QCirc().crx(0, 1, phase=0.3).measure(qid=[0,1,2], cid=[0,1,2])
        qc_LR = QCirc().h(0).cx(0,1).rx(1, phase=0.2).crx(0, 1, phase=0.3).measure(qid=[0,1,2], cid=[0,1,2])
        self.assertEqual(qc_L + qc_R == qc_LR, True)
        self.assertEqual(qc_R + qc_L == qc_LR, False)
        
    def test_merge_3terms(self):
        """test 'merge' (2 terms)
        """
        qc_1 = QCirc().h(0).cx(0,1).rx(1, phase=0.2)
        qc_2 = QCirc().cry(0, 1, phase=0.3).measure(qid=[0,1,2], cid=[0,1,2])
        qc_3 = QCirc().x(0).z(5)
        qc_123 = QCirc().h(0).cx(0,1).rx(1, phase=0.2).cry(0, 1, phase=0.3).measure(qid=[0,1,2], cid=[0,1,2]).x(0).z(5)
        self.assertEqual(qc_1 + qc_2 + qc_3 == qc_123, True)
        
    def test_merge_incremental(self):
        """test 'merge' (incremental)
        """
        qc_1 = QCirc().h(0).cx(0,1).rx(1, phase=0.2)
        qc_2 = QCirc().cry(0, 1, phase=0.3).measure(qid=[0,1,2], cid=[0,1,2])
        qc_3 = QCirc().x(0).z(5)
        qc_expect = QCirc().h(0).cx(0,1).rx(1, phase=0.2).cry(0, 1, phase=0.3).measure(qid=[0,1,2], cid=[0,1,2]).x(0).z(5)
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
        qc_R = QCirc().crz(0, 1, phase=0.3).measure(qid=[0,1,2], cid=[0,1,2])
        qc_LR = QCirc().h(0).cx(0,1).rx(1, phase=0.2).cry(0, 1, phase=0.3).measure(qid=[0,1,2], cid=[0,1,2])
        self.assertEqual(qc_L.kind_first(), HADAMARD)
        self.assertEqual(qc_R.kind_first(), CONTROLLED_RZ)
        self.assertEqual(qc_LR.kind_first(), HADAMARD)

class TestQCirc_pop_gate(unittest.TestCase):
    """ test 'QCirc' : 'pop_gate'
    """

    def test_pop_gate_not_update(self):
        """test 'pop_gate' (not update)
        """
        qc = QCirc().h(0).cx(0,1).rx(1, phase=0.2).crz(0, 1, phase=0.3).measure(qid=[0,1,2], cid=[0,1,2])
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
        qc = QCirc().h(5, ctrl=6).cx(0,1).rx(1, phase=0.2).crz(0, 1, phase=0.3).measure(qid=[0,1,2], cid=[0,1,2])
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
# export OpenQASM
#

class TestQCirc_to_qasm(unittest.TestCase):
    """ test 'QCirc' : 'to_qasm'
    """

    def test_x(self):
        """test x
        """
        qc = QCirc().x(0)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).x(0)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
        
    def test_y(self):
        """test y
        """
        qc = QCirc().y(0)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).y(0)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
        
    def test_z(self):
        """test z
        """
        qc = QCirc().z(0)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).z(0)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
        
    def test_xr(self):
        """test xr
        """
        qc = QCirc().xr(0)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).xr(0)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
        
    def test_xr_dg(self):
        """test xr_dg
        """
        qc = QCirc().xr_dg(0)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).xr_dg(0)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
        
    def test_h(self):
        """test h
        """
        qc = QCirc().h(0)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).h(0)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
        
    def test_s(self):
        """test s
        """
        qc = QCirc().s(0)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).s(0)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
        
    def test_s_dg(self):
        """test s_dg
        """
        qc = QCirc().s_dg(0)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).s_dg(0)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
        
    def test_t(self):
        """test t
        """
        qc = QCirc().t(0)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).t(0)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
        
    def test_t_dg(self):
        """test t_dg
        """
        qc = QCirc().t_dg(0)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).t_dg(0)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
        
    def test_p(self):
        """test p
        """
        qc = QCirc().p(0, phase=0.1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).p(0, phase=0.1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
        
    def test_rx(self):
        """test rx
        """
        qc = QCirc().rx(0, phase=0.1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).rx(0, phase=0.1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
        
    def test_ry(self):
        """test ry
        """
        qc = QCirc().ry(0, phase=0.1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).ry(0, phase=0.1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
        
    def test_rz(self):
        """test rz
        """
        qc = QCirc().rz(0, phase=0.1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).rz(0, phase=0.1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_cx(self):
        """test cx
        """
        qc = QCirc().cx(0,1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).cx(0,1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_cy(self):
        """test cy
        """
        qc = QCirc().cy(0,1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).cy(0,1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_cz(self):
        """test cz
        """
        qc = QCirc().cz(0,1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).cz(0,1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_cxr(self):
        """test cxr
        """
        qc = QCirc().cxr(0,1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).cxr(0,1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_cxr_2(self):
        """test cxr (2)
        """
        qc = QCirc().h(0).cxr(0,1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).h(0).cxr(0,1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_cxr_dg(self):
        """test cxr_dg
        """
        qc = QCirc().cxr_dg(0,1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).cxr_dg(0,1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_ch(self):
        """test ch
        """
        qc = QCirc().ch(0,1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).ch(0,1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_cs(self):
        """test cs
        """
        qc = QCirc().cs(0,1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).cs(0,1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_cs_dg(self):
        """test cs_dg
        """
        qc = QCirc().cs_dg(0,1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).cs_dg(0,1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_ct(self):
        """test ct
        """
        qc = QCirc().ct(0,1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).ct(0,1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_ct_dg(self):
        """test ct_dg
        """
        qc = QCirc().ct_dg(0,1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).ct_dg(0,1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_cp(self):
        """test cp
        """
        qc = QCirc().cp(0,1, phase=0.1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).cp(0,1, phase=0.1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_crx(self):
        """test crx
        """
        qc = QCirc().crx(0,1, phase=0.1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).crx(0,1, phase=0.1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_cry(self):
        """test cry
        """
        qc = QCirc().cry(0,1, phase=0.1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).cry(0,1, phase=0.1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_crz(self):
        """test crz
        """
        qc = QCirc().crz(0,1, phase=0.1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).crz(0,1, phase=0.1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_sw(self):
        """test sw
        """
        qc = QCirc().sw(0,1)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).sw(0,1)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_ccx(self):
        """test ccx
        """
        qc = QCirc().ccx(0,1,2)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).ccx(0,1,2)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_csw(self):
        """test csw
        """
        qc = QCirc().csw(0,1,2)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).csw(0,1,2)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_many_unitary_gates(self):
        """test many unitary gates
        """
        qc = QCirc().h(0).cx(0,1).crx(1,0, phase=0.1).csw(0,1,2)
        bk = Backend()
        qs_A = bk.run(qcirc=qc).info['qstate']
        qs_B = QState(qubit_num=qc.qubit_num).h(0).cx(0,1).crx(1,0, phase=0.1).csw(0,1,2)
        self.assertEqual(equal_or_not(qs_A, qs_B), True)
        self.assertEqual(valid_or_not(qc), True)
    
    def test_measure(self):
        """test measure
        """
        qc = QCirc().measure(qid=[0,1], cid=[0,1])
        self.assertEqual(valid_or_not(qc), True)
    
    def test_reset(self):
        """test reset
        """
        qc = QCirc().reset(qid=[0,1])
        actual = qc.to_qasm()
        expect = """OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[2];\nreset q[0];\nreset q[1];"""
        self.assertEqual(actual, expect)

#
# import OpenQASM
#

class TestQCirc_from_qasm(unittest.TestCase):
    """ test 'QCirc' : 'from_qasm'
    """

    def test_x(self):
        """test x
        """
        qc_A = QCirc().x(0)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)

    def test_y(self):
        """test y
        """
        qc_A = QCirc().y(0)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
        
    def test_z(self):
        """test z
        """
        qc_A = QCirc().z(0)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
        
    def test_xr(self):
        """test xr
        """
        qc_A = QCirc().xr(0)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
        
    def test_xr_dg(self):
        """test xr_dg
        """
        qc_A = QCirc().xr_dg(0)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
        
    def test_h(self):
        """test h
        """
        qc_A = QCirc().h(0)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
        
    def test_s(self):
        """test s
        """
        qc_A = QCirc().s(0)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
        
    def test_s_dg(self):
        """test s_dg
        """
        qc_A = QCirc().s_dg(0)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
        
    def test_t(self):
        """test t
        """
        qc_A = QCirc().t(0)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
        
    def test_t_dg(self):
        """test t_dg
        """
        qc_A = QCirc().t_dg(0)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
        
    def test_p(self):
        """test p
        """
        qc_A = QCirc().p(0, phase=0.1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
        
    def test_rx(self):
        """test rx
        """
        qc_A = QCirc().rx(0, phase=0.1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
        
    def test_ry(self):
        """test ry
        """
        qc_A = QCirc().ry(0, phase=0.1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
        
    def test_rz(self):
        """test rz
        """
        qc_A = QCirc().rz(0, phase=0.1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_cx(self):
        """test cx
        """
        qc_A = QCirc().cx(0,1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_cy(self):
        """test cy
        """
        qc_A = QCirc().cy(0,1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_cz(self):
        """test cz
        """
        qc_A = QCirc().cz(0,1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_cxr(self):
        """test cxr
        """
        qc_A = QCirc().cxr(0,1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_cxr_2(self):
        """test cxr (2)
        """
        qc_A = QCirc().h(0).cxr(0,1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_cxr_dg(self):
        """test cxr_dg
        """
        qc_A = QCirc().cxr_dg(0,1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_ch(self):
        """test ch
        """
        qc_A = QCirc().ch(0,1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_cs(self):
        """test cs
        """
        qc_A = QCirc().cs(0,1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_cs_dg(self):
        """test cs_dg
        """
        qc_A = QCirc().cs_dg(0,1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_ct(self):
        """test ct
        """
        qc_A = QCirc().ct(0,1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_ct_dg(self):
        """test ct_dg
        """
        qc_A = QCirc().ct_dg(0,1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_cp(self):
        """test cp
        """
        qc_A = QCirc().cp(0,1, phase=0.1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_crx(self):
        """test crx
        """
        qc_A = QCirc().crx(0,1, phase=0.1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_cry(self):
        """test cry
        """
        qc_A = QCirc().cry(0,1, phase=0.1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_crz(self):
        """test crz
        """
        qc_A = QCirc().crz(0,1, phase=0.1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_sw(self):
        """test sw
        """
        qc_A = QCirc().sw(0,1)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_ccx(self):
        """test ccx
        """
        qc_A = QCirc().ccx(0,1,2)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_csw(self):
        """test csw
        """
        qc_A = QCirc().csw(0,1,2)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)
    
    def test_many_unitary_gates(self):
        """test many unitary gates
        """
        qc_A = QCirc().h(0).cx(0,1).crx(1,0, phase=0.1).csw(0,1,2)
        str_A = qc_A.to_qasm()
        qc_B = QCirc.from_qasm(str_A)
        str_B = qc_B.to_qasm()
        self.assertEqual(str_A, str_B)

class TestQCirc_get_stats(unittest.TestCase):
    """ test 'QCirc' : get_stats
    """

    def test_get_stats(self):
        """test get_stats
        """
        qc = QCirc().x(0).z(2).h(0).h(0).cx(0,1).h(0).h(1).crz(1,0, phase=0.1).rx(1, phase=0.2)
        qc.measure(qid=[0,1], cid=[0,1]).reset(qid=[0])
        stats = qc.get_stats()
        self.assertEqual(stats['qubit_num'], 3)
        self.assertEqual(stats['gate_num'], 12)
        self.assertEqual(stats['gate_freq']['h'], 4)
        self.assertEqual(stats['gate_freq']['x'], 1)
        self.assertEqual(stats['gate_freq']['z'], 1)
        self.assertEqual(stats['gate_freq']['cx'], 1)
        self.assertEqual(stats['gate_freq']['crz'], 1)
        self.assertEqual(stats['gate_freq']['rx'], 1)
        self.assertEqual(stats['gate_freq']['measure'], 2)
        self.assertEqual(stats['gate_freq']['reset'], 1)

class TestQCirc_dump_load(unittest.TestCase):
    """ test 'QCirc' : dump, load
    """

    def test_dump_load(self):
        """test dump, load
        """
        qc_A = QCirc().x(0).z(2).h(0).h(0).cx(0,1).h(0).h(1).crz(1,0, phase=0.1).rx(1, phase=0.2)
        qc_A.dump("tmp/foo.qc")
        qc_B = QCirc.load("tmp/foo.qc")
        self.assertEqual(qc_A, qc_B)

class TestQCirc_get_gates(unittest.TestCase):
    """ test 'QCirc' : get_gates, add_gates
    """

    def test_get_add_gates(self):
        """test get_gates, add_gates
        """
        qc_A = QCirc().x(0).z(2).h(0).h(0).cx(0,1).h(0).h(1).crz(1,0, phase=0.1).rx(1, phase=0.2)
        gates = qc_A.get_gates()
        qc_B = QCirc().add_gates(gates)
        self.assertEqual(qc_A, qc_B)

class TestQCirc_generate_random_gates(unittest.TestCase):
    """ test 'QCirc' : generate_random_gates
    """

    def test_generate_random_gates(self):
        """test get_gates, add_gates
        """
        qc = QCirc.generate_random_gates(qubit_num=3, gate_num=1000,
                                         prob={'h':5, 'cx':3, 't':2})
        stats = qc.get_stats()
        self.assertEqual(round(stats['gate_freq']['h'] / 100.), 5)
        self.assertEqual(round(stats['gate_freq']['cx'] / 100.), 3)
        self.assertEqual(round(stats['gate_freq']['t'] / 100.), 2)
        
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
