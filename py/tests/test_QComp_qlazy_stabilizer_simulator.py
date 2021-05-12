# -*- coding: utf-8 -*-
import unittest
import math
import numpy as np
import sys

from qlazypy import QState, QComp, Backend

EPS = 1.0e-6

SQRT_2 = np.sqrt(2.0)
COS_PI_8 = math.cos(math.pi/8)
COS_PI_4 = math.cos(math.pi/4)
SIN_PI_8 = math.sin(math.pi/8)
SIN_PI_4 = math.sin(math.pi/4)

class MyQComp(QComp):

    def bell(self, q0, q1):
        self.h(q0).cx(q0,q1)
        return self

def equal_values(val_0, val_1):

    dif = abs(val_0 - val_1)
    if dif < EPS:
        return True
    else:
        return False

def equal_vectors(vec_0, vec_1):

    inpro = abs(np.dot(np.conjugate(vec_0), vec_1))
    if abs(inpro - 1.0) < EPS:
        return True
    else:
        return False

def equal_qstates(qs_0, qs_1):

    fid = qs_0.fidelity(qs_1)
    if abs(fid - 1.0) < EPS:
        return True
    else:
        return False

#============================
# qlazy_stabilizer_simulator
#============================

#
# __init__
#

class TestQComp_init(unittest.TestCase):
    """ test 'QComp' : '__init__'
    """

    def test_init_qlazy_stabilizer_simulator(self):
        """test '__init__' (qlazy_stabilizer_simulator)
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=3, cmem_num=2, backend=bk)
        actual = qc.qstate.get_str()
        expect = "  ZII\n  IZI\n  IIZ\n"
        qc.free()
        self.assertEqual(actual, expect)

#
# reset
#

class TestQComp_reset(unittest.TestCase):
    """ test 'QState' : 'reset'
    """

    def test_reset_qlazy_stabilizer_simulator(self):
        """test 'reset' (qlazy_stabilizer_simulator)
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=3, cmem_num=2, backend=bk)
        qc.h(0).h(1).h(2).run()
        qc.reset()
        actual = qc.qstate.get_str()
        expect = "  ZII\n  IZI\n  IIZ\n"
        qc.free()
        self.assertEqual(actual, expect)

#
# 1-qubit gate
#

class TestQComp_1_qubit_qlazy_stabilizer_simulator(unittest.TestCase):
    """ test 'QComp' : 1-qubit gate (qlazy_stabilizer_simulator)
    """

    def test_x(self):
        """test 'x' gate
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.x(0).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = " -Z\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_h_x(self):
        """test 'x' gate (following 'h' gate)
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).x(0).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = "  X\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_y(self):
        """test 'y' gate
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.y(0).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = " -Z\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_h_y(self):
        """test 'y' gate (following 'h' gate)
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).y(0).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = " -X\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_z(self):
        """test 'z' gate
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.z(0).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = "  Z\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_h_z(self):
        """test 'z' gate (following 'h' gate)
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).z(0).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = " -X\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_h(self):
        """test 'h' gate
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = "  X\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_h_h(self):
        """test 'h' gate (following 'h' gate)
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).h(0).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = "  Z\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_s(self):
        """test 's' gate
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.s(0).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = "  Z\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_h_s(self):
        """test 's' gate (following 'h' gate)
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).s(0).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = "  Y\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_s_dg(self):
        """test 's+' gate
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.s(0).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = "  Z\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_h_s_dg(self):
        """test 's+' gate (following 'h' gate)
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).s_dg(0).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = " -Y\n"
        self.assertEqual(actual, expect)
        qc.free()
        
#
# 2-qubit gate
#

class TestQComp_2_qubit_qlazy_stabilizer_simulator(unittest.TestCase):
    """ test 'QComp' : 2-qubit gate (qlazy_stabilizer_simulator)
    """
    
    def test_cx(self):
        """test 'CX'
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.cx(0,1).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = "  ZI\n  ZZ\n"
        qc.free()
        self.assertEqual(actual, expect)

    def test_hh_cx(self):
        """test 'CX' (following 'h' gate)
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cx(0,1).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = "  XX\n  IX\n"
        qc.free()
        self.assertEqual(actual, expect)

    def test_cy(self):
        """test 'CY'
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.cy(0,1).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = "  ZI\n  ZZ\n"
        qc.free()
        self.assertEqual(actual, expect)

    def test_hh_cy(self):
        """test 'CY' (following 'h' gate)
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cy(0,1).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = "-iXY\n  ZX\n"
        qc.free()
        self.assertEqual(actual, expect)

    def test_cz(self):
        """test 'CZ'
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.cz(0,1).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = "  ZI\n  IZ\n"
        qc.free()
        self.assertEqual(actual, expect)

    def test_hh_cz(self):
        """test 'CZ' (folowint 'h' gate)
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cz(0,1).run(reset_qubits=False)
        actual = qc.qstate.get_str()
        expect = "  XZ\n  ZX\n"
        qc.free()
        self.assertEqual(actual, expect)

#
# measurement
#

class TestQComp_measure_stabilizer_simulator(unittest.TestCase):
    """ test 'QComp' : various kind of measurements
    """

    def test_measure_mesurement_only(self):
        """test 'm' (measurement only)
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.measure([0,1]).run(shots=10)
        qc.free()
        self.assertEqual(res['measured_qid'], [0,1])
        self.assertEqual(res['frequency']['00'], 10)

    def test_measure_simple(self):
        """test 'm' (simple case)
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).cx(0,1).measure([0,1]).run(shots=10)
        qc.free()
        self.assertEqual(res['measured_qid'], [0,1])
        self.assertEqual(res['frequency']['00']+res['frequency']['11'], 10)

    def test_measure_use_cmem(self):
        """test 'm' (use classical memory)
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=2, cmem_num=3, backend=bk)
        res = qc.h(0).cx(0,1).measure([0,1],[0,1]).run(shots=10, reset_cmem=False)
        self.assertEqual(res['measured_qid'], [0,1])
        self.assertEqual(res['frequency']['00']+res['frequency']['11'], 10)
        self.assertEqual(qc.cmem==[0,0,0] or qc.cmem==[1,1,0], True)
        qc.free()

    def test_measure_control_qubit(self):
        """test 'm' (control qubit using classical memory)
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = QComp(qubit_num=2, cmem_num=3, backend=bk)
        res = qc.h(0).cx(0,1).measure([0],[0]).x(0, ctrl=0).x(1, ctrl=0).measure([0,1]).run(shots=10)
        qc.free()
        self.assertEqual(res['measured_qid'], [0,1])
        self.assertEqual(res['frequency']['00'], 10)

#
# inheritance
#

class TestQComp_inheritance_stabilizer_simulator(unittest.TestCase):
    """ test 'QComp' : inheritance (qlazy_stabilizer_simulator)
    """

    def test_inheritance(self):
        """test 'inheritance'
        """
        bk = Backend(name='qlazy', device='stabilizer_simulator')
        qc = MyQComp(backend=bk, qubit_num=2, cmem_num=3)
        res = qc.bell(0,1).measure(qid=[0,1]).run(shots=10)
        qc.free()
        self.assertEqual(res['measured_qid'], [0,1])
        self.assertEqual(res['frequency']['00']+res['frequency']['11'], 10)

if __name__ == '__main__':
    unittest.main()
