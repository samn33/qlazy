# -*- coding: utf-8 -*-
import unittest
import math
import numpy as np
import sys

from qlazy import QState, QComp, Backend, PauliProduct

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
# 1-qubit gate
#

class TestQComp_1_qubit_qlazy_stabilizer_simulator(unittest.TestCase):
    """ test 'QComp' : 1-qubit gate (qlazy_stabilizer_simulator)
    """

    def test_x(self):
        """test 'x' gate
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.x(0).run()
        actual = res.info['stabilizer'].get_str()
        expect = " -Z\n"
        self.assertEqual(actual, expect)
        
    def test_h_x(self):
        """test 'x' gate (following 'h' gate)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.h(0).x(0).run()
        actual = res.info['stabilizer'].get_str()
        expect = "  X\n"
        self.assertEqual(actual, expect)
        
    def test_y(self):
        """test 'y' gate
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.y(0).run()
        actual = res.info['stabilizer'].get_str()
        expect = " -Z\n"
        self.assertEqual(actual, expect)
        
    def test_h_y(self):
        """test 'y' gate (following 'h' gate)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.h(0).y(0).run()
        actual = res.info['stabilizer'].get_str()
        expect = " -X\n"
        self.assertEqual(actual, expect)
        
    def test_z(self):
        """test 'z' gate
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.z(0).run()
        actual = res.info['stabilizer'].get_str()
        expect = "  Z\n"
        self.assertEqual(actual, expect)
        
    def test_h_z(self):
        """test 'z' gate (following 'h' gate)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.h(0).z(0).run()
        actual = res.info['stabilizer'].get_str()
        expect = " -X\n"
        self.assertEqual(actual, expect)
        
    def test_h(self):
        """test 'h' gate
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.h(0).run()
        actual = res.info['stabilizer'].get_str()
        expect = "  X\n"
        self.assertEqual(actual, expect)
        
    def test_h_h(self):
        """test 'h' gate (following 'h' gate)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.h(0).h(0).run()
        actual = res.info['stabilizer'].get_str()
        expect = "  Z\n"
        self.assertEqual(actual, expect)
        
    def test_s(self):
        """test 's' gate
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.s(0).run()
        actual = res.info['stabilizer'].get_str()
        expect = "  Z\n"
        self.assertEqual(actual, expect)
        
    def test_h_s(self):
        """test 's' gate (following 'h' gate)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.h(0).s(0).run()
        actual = res.info['stabilizer'].get_str()
        expect = "  Y\n"
        self.assertEqual(actual, expect)
        
    def test_s_dg(self):
        """test 's+' gate
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.s(0).run()
        actual = res.info['stabilizer'].get_str()
        expect = "  Z\n"
        self.assertEqual(actual, expect)
        
    def test_h_s_dg(self):
        """test 's+' gate (following 'h' gate)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.h(0).s_dg(0).run()
        actual = res.info['stabilizer'].get_str()
        expect = " -Y\n"
        self.assertEqual(actual, expect)
        
#
# 2-qubit gate
#

class TestQComp_2_qubit_qlazy_stabilizer_simulator(unittest.TestCase):
    """ test 'QComp' : 2-qubit gate (qlazy_stabilizer_simulator)
    """
    
    def test_cx(self):
        """test 'CX'
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.cx(0,1).run()
        actual = res.info['stabilizer'].get_str()
        expect = "  ZI\n  ZZ\n"
        self.assertEqual(actual, expect)

    def test_hh_cx(self):
        """test 'CX' (following 'h' gate)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.h(0).h(1).cx(0,1).run()
        actual = res.info['stabilizer'].get_str()
        expect = "  XX\n  IX\n"
        self.assertEqual(actual, expect)

    def test_cy(self):
        """test 'CY'
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.cy(0,1).run()
        actual = res.info['stabilizer'].get_str()
        expect = "  ZI\n  ZZ\n"
        self.assertEqual(actual, expect)

    def test_hh_cy(self):
        """test 'CY' (following 'h' gate)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.h(0).h(1).cy(0,1).run()
        actual = res.info['stabilizer'].get_str()
        expect = "-iXY\n  ZX\n"
        self.assertEqual(actual, expect)

    def test_cz(self):
        """test 'CZ'
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.cz(0,1).run()
        actual = res.info['stabilizer'].get_str()
        expect = "  ZI\n  IZ\n"
        self.assertEqual(actual, expect)

    def test_hh_cz(self):
        """test 'CZ' (folowint 'h' gate)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.h(0).h(1).cz(0,1).run()
        actual = res.info['stabilizer'].get_str()
        expect = "  XZ\n  ZX\n"
        self.assertEqual(actual, expect)

#
# operate
#

class TestQComp_operate_qlazy_stabilizer_simulator(unittest.TestCase):
    """ test 'QComp' : operate
    """

    def test_operate_x(self):
        """test 'operate' (x)
        """
        qc_expect = QComp(product='qlazy', device='stabilizer_simulator').x(0)
        res = qc_expect.run()
        expect = res.info['stabilizer'].get_str()
        pp = PauliProduct(pauli_str="X")
        qc_actual = QComp(product='qlazy', device='stabilizer_simulator').operate(pp=pp)
        res = qc_actual.run()
        actual = res.info['stabilizer'].get_str()
        self.assertEqual(expect, actual)

    def test_operate_h_x(self):
        """test 'operate' (x followed by h)
        """
        qc_expect = QComp(product='qlazy', device='stabilizer_simulator').h(0).x(0)
        res = qc_expect.run()
        expect = res.info['stabilizer'].get_str()
        pp = PauliProduct(pauli_str="X")
        qc_actual = QComp(product='qlazy', device='stabilizer_simulator').h(0).operate(pp=pp)
        res = qc_actual.run()
        actual = res.info['stabilizer'].get_str()
        self.assertEqual(expect, actual)

    def test_operate_h_y(self):
        """test 'operate' (Y followed by h)
        """
        qc_expect = QComp(product='qlazy', device='stabilizer_simulator').h(0).y(0)
        res = qc_expect.run()
        expect = res.info['stabilizer'].get_str()
        pp = PauliProduct(pauli_str="Y")
        qc_actual = QComp(product='qlazy', device='stabilizer_simulator').h(0).operate(pp=pp)
        res = qc_actual.run()
        actual = res.info['stabilizer'].get_str()
        self.assertEqual(expect, actual)

    def test_operate_h_z(self):
        """test 'operate' (Z followed by h)
        """
        qc_expect = QComp(product='qlazy', device='stabilizer_simulator').h(0).z(0)
        res = qc_expect.run()
        expect = res.info['stabilizer'].get_str()
        pp = PauliProduct(pauli_str="Z")
        qc_actual = QComp(product='qlazy', device='stabilizer_simulator').h(0).operate(pp=pp)
        res = qc_actual.run()
        actual = res.info['stabilizer'].get_str()
        self.assertEqual(expect, actual)

    def test_operate_xyz(self):
        """test 'operate' (xyz)
        """
        qc_expect = QComp(product='qlazy', device='stabilizer_simulator').x(2).y(0).z(1)
        res = qc_expect.run()
        expect = res.info['stabilizer'].get_str()
        pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
        qc_actual = QComp(product='qlazy', device='stabilizer_simulator').operate(pp=pp)
        res = qc_actual.run()
        actual = res.info['stabilizer'].get_str()
        self.assertEqual(expect, actual)

    def test_operate_controlled_xyz(self):
        """test 'operate' (controlled_xyz)
        """
        qc_expect = QComp(product='qlazy', device='stabilizer_simulator').cx(3,2).cy(3,0).cz(3,1)
        res = qc_expect.run()
        expect = res.info['stabilizer'].get_str()
        pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
        qc_actual = QComp(product='qlazy', device='stabilizer_simulator').operate(pp=pp, ctrl=3)
        res = qc_actual.run()
        actual = res.info['stabilizer'].get_str()
        self.assertEqual(expect, actual)
        
#
# measurement
#

class TestQComp_measure_qlazy_stabilizer_simulator(unittest.TestCase):
    """ test 'QComp' : various kind of measurements
    """

    def test_measure_mesurement_only_1(self):
        """test 'measure' (measurement only (1))
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.measure(qid=[0,1], cid=[0,1]).run(shots=10)
        freq = res.frequency
        cid = res.cid
        self.assertEqual(freq['00'], 10)
        self.assertEqual(cid, [0,1])
    
    def test_measure_mesurement_only_2(self):
        """test 'measure' (measurement only (2))
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.measure(qid=[0,1], cid=[1,2]).run(shots=10, cid=[1,2])
        freq = res.frequency
        cid = res.cid
        self.assertEqual(freq['00'], 10)
        self.assertEqual(cid, [1,2])
    
    def test_measure_mesurement_only_3(self):
        """test 'measure' (measurement only (3))
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.measure(qid=[0,1], cid=[0,1]).run(shots=10)
        freq = res.frequency
        cid = res.cid
        self.assertEqual(freq['00'], 10)
        self.assertEqual(cid, [0,1])
    
    def test_measure_mesurement_only_4(self):
        """test 'measure' (measurement only (4))
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.measure(qid=[0,1]).run(shots=10)
        self.assertEqual(res.frequency, None)
    
    def test_measure_mesurement_unitary(self):
        """test 'measure' (measurement-unitary)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.measure(qid=[0,1], cid=[1,2]).h(0).cx(0,1).run(shots=10, cid=[1,2])
        freq = res.frequency
        cid = res.cid
        expect = "  XX\n  ZZ\n"
        actual = res.info['stabilizer'].get_str()
        self.assertEqual(actual, expect)
        self.assertEqual(cid, [1,2])

    def test_measure_unitary_measurement_with_no_cmem(self):
        """test 'measure' (unitary-meausrement with no cmem)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.h(0).cx(0,1).measure(qid=[0,1]).run(shots=10)
        expect_1 = "  ZI\n  ZZ\n"
        expect_2 = " -ZI\n  ZZ\n"
        actual = res.info['stabilizer'].get_str()
        ans_1 = (actual == expect_1)
        ans_2 = (actual == expect_2)
        self.assertEqual(ans_1 or ans_2, True)
    
    def test_measure_unitary_measurement_with_cmem(self):
        """test 'measure' (unitary-measurement with cmem)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.h(0).cx(0,1).measure(qid=[0,1], cid=[0,1]).run(shots=10, cid=[0,1])
        freq = res.frequency
        cid = res.cid
        ans = (freq['00']+freq['11'] == 10) and (freq['00'] != 0) and (freq['11'] != 0)
        self.assertEqual(ans, True)
        self.assertEqual(cid, [0,1])
    
    def test_measure_unitary_measurement_with_cmem_norecord(self):
        """test 'measure' (unitary-measurement with cmem norecord)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.h(0).cx(0,1).measure(qid=[0,1]).run(shots=10)
        freq = res.frequency
        cid = res.cid
        self.assertEqual(freq, None)
        self.assertEqual(cid, [])
    
    def test_measure_mesurement_unitary_measurement(self):
        """test 'measure' (meaurement-unitary-measrement)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.measure(qid=[0,1], cid=[1,2]).x(0).measure(qid=[0,1], cid=[2,0]).run(shots=10, cid=[0,1,2])
        freq = res.frequency
        cid = res.cid
        self.assertEqual(freq['001'], 10)
        self.assertEqual(cid, [0,1,2])
    
    def test_measure_unitary_measuremen_cunitary_measurement(self):
        """test 'measure' (unitary-measurement-cunitary-measurement)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.h(0).cx(0,1).measure(qid=[0], cid=[0]).x(0, ctrl=0).x(1, ctrl=0).measure(qid=[0,1], cid=[0,1]).run(shots=10)
        freq = res.frequency
        cid = res.cid
        self.assertEqual(freq['00'], 10)
        self.assertEqual(cid, [0,1])

#
# reset
#

class TestQComp_reset_qlazy_stabilizer_simulator(unittest.TestCase):
    """ test 'QComp' : various kind of resets
    """

    def test_reset_simple_all(self):
        """test 'reset' (simple_all)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.x(0).x(1).reset(qid=[0,1,2]).measure(qid=[0,1,2], cid=[0,1,2]).run(shots=10)
        freq = res.frequency
        self.assertEqual(freq['000'], 10)

    def test_reset_simple_partial(self):
        """test 'reset' (simple_partial)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.x(0).x(1).reset(qid=[1]).measure(qid=[0,1], cid=[0,1]).run(shots=10)
        freq = res.frequency
        self.assertEqual(freq['10'], 10)

    def test_reset_unitary_measure_reset(self):
        """test 'reset' (unitary-measure-reset)
        """
        qc = QComp(product='qlazy', device='stabilizer_simulator')
        res = qc.x(0).x(1).measure(qid=[0,1,2]).reset(qid=[1]).measure(qid=[0,1], cid=[0,1]).run(shots=10, cid=[0,1])
        freq = res.frequency
        self.assertEqual(freq['10'], 10)

#
# inheritance
#

class TestQComp_inheritance_stabilizer_simulator(unittest.TestCase):
    """ test 'QComp' : inheritance (qlazy_stabilizer_simulator)
    """

    def test_inheritance(self):
        """test 'inheritance'
        """
        qc = MyQComp(product='qlazy', device='stabilizer_simulator')
        res = qc.bell(0,1).measure(qid=[0,1], cid=[0,1]).run(shots=10)
        freq = res.frequency
        ans = (freq['00']+freq['11'] == 10) and (freq['00'] != 0) and (freq['11'] != 0)
        self.assertEqual(ans, True)

if __name__ == '__main__':
    unittest.main()
