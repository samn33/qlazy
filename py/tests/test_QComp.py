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

VECTOR_16 = [-0.20483596+0.23441366j, -0.169582+0.27101216j,
             -0.164284  +0.22521276j, -0.14760841-0.02810872j,
             -0.14938938+0.10050371j, -0.13766646+0.19531029j,
             -0.16514988-0.06170589j, 0.03489414+0.18582622j,
             0.08001864+0.19883844j, 0.11670812-0.05657322j,
             0.41775044+0.14179641j, -0.19339021+0.09413556j,
             -0.08368439+0.1502309j, 0.25751741-0.20723416j,
             -0.00226682+0.0068861j, 0.06875241-0.31143861j]

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


#========================
# qlazy_qstate_simulator
#========================

#
# __init__
#

class TestQComp_init(unittest.TestCase):
    """ test 'QComp' : '__init__'
    """

    def test_init_default(self):
        """test '__init__' (default: qlazy_qstate_simulator)
        """
        qc = QComp(qubit_num=3, cmem_num=2)
        actual = qc.qstate.amp
        expect = np.array([1j, 0j, 0j, 0j, 0j, 0j, 0j, 0j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_init_qlazy_qstate_simulator(self):
        """test '__init__' (qlazy_qstate_simulator)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=3, cmem_num=2, backend=bk)
        actual = qc.qstate.amp
        expect = np.array([1j, 0j, 0j, 0j, 0j, 0j, 0j, 0j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

#
# reset
#

class TestQComp_reset(unittest.TestCase):
    """ test 'QState' : 'reset'
    """

    def test_reset_qlazy_qstate_simulator(self):
        """test 'reset' (qlazy_qstate_simulator)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=3, cmem_num=2, backend=bk)
        qc.h(0).h(1).h(2).run()
        qc.reset()
        actual = qc.qstate.amp
        expect = np.array([1j, 0j, 0j, 0j, 0j, 0j, 0j, 0j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

#
# 1-qubit gate
#

class TestQComp_1_qubit_qlazy_qstate_simulator(unittest.TestCase):
    """ test 'QComp' : 1-qubit gate (qlazy_qstate_simulator)
    """

    def test_x(self):
        """test 'x' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.x(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([0.0, 1.0])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_x(self):
        """test 'x' gate (following 'h' gate)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).x(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0/SQRT_2, 1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_y(self):
        """test 'y' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.y(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([0.0, 1.0j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_y(self):
        """test 'y' gate (following 'h' gate)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).y(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([-1.0j/SQRT_2, 1.0j/SQRT_2])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_z(self):
        """test 'z' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.z(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_z(self):
        """test 'z' gate (following 'h' gate)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).z(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0/SQRT_2, -1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_xr(self):
        """test 'xr' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.xr(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([0.5+0.5j, 0.5-0.5j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_xr(self):
        """test 'xr' gate (following 'h' gate)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).xr(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0/SQRT_2, 1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_xr_dg(self):
        """test 'xr_dg' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.xr_dg(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([0.5-0.5j, 0.5+0.5j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_xr_dg(self):
        """test 'xr_dg' gate (following 'h' gate)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).xr_dg(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0/SQRT_2, 1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h(self):
        """test 'h' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0/SQRT_2, 1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_h(self):
        """test 'h' gate (following 'h')
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).h(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_s(self):
        """test 's' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.s(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_s(self):
        """test 's' gate (following 'h' gate)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).s(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0/SQRT_2, 1.0j/SQRT_2])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_s_dg(self):
        """test 's_dg' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.s_dg(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_s_dg(self):
        """test 's_dg' gate (following 'h' gate)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).s_dg(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0/SQRT_2, -1.0j/SQRT_2])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_t(self):
        """test 't' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.t(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_t(self):
        """test 't' gate (following 'h' gate)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).t(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0/SQRT_2, 0.5+0.5j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_t_dg(self):
        """test 't_dg' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.t_dg(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_t_dg(self):
        """test 't_dg' gate (following 'h' gate)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).t_dg(0).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0/SQRT_2, 0.5-0.5j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_rx(self):
        """test 'rx' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.rx(0, phase=0.25).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([COS_PI_8, -SIN_PI_8*1.0j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_rx(self):
        """test 'rx' gate (following 'h' gate)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).rx(0, phase=0.25).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([0.65328148-0.27059805j, 0.65328148-0.27059805j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_ry(self):
        """test 'ry' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.ry(0, phase=0.25).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([COS_PI_8, SIN_PI_8])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_ry(self):
        """test 'ry' gate (following 'h' gate)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).ry(0, phase=0.25).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([0.38268343+0.j, 0.92387953+0.j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_rz(self):
        """test 'rz' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.rz(0, phase=0.25).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_rz(self):
        """test 'rz' gate (following 'h' gate)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).rz(0, phase=0.25).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([0.65328148-0.27059805j, 0.65328148+0.27059805j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_p(self):
        """test 'p' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.p(0, phase=0.25).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_p(self):
        """test 'p' gate (following 'h' gate)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).p(0, phase=0.25).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([0.70710678, 0.5+0.5j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_u1(self):
        """test 'u1' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.u1(0, alpha=0.1).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_u1(self):
        """test 'u1' gate (following 'h' gate)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).u1(0, alpha=0.1).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([0.70710678+0.j, 0.67249851+0.21850801j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_u2(self):
        """test 'u2' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.u2(0, alpha=0.1, beta=0.2).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([0.70710678+0.j, 0.5720614 +0.41562694j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_u2(self):
        """test 'u2' gate (following 'h' gate)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).u2(0, alpha=0.1, beta=0.2).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([0.02447174-0.1545085j,0.69840112+0.69840112j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_u3(self):
        """test 'u3' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.u3(0, alpha=0.1, beta=0.2, gamma=0.3).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([0.89100652+0.j, 0.36728603+0.26684892j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_h_u3(self):
        """test 'u3' gate (following 'h' gate)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).u3(0, alpha=0.1, beta=0.2, gamma=0.3).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([0.32472882-0.09920056j, 0.63003676+0.69840112j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

#
# 2-qubit gate
#

class TestQComp_2_qubit_qlazy_qstate_simulator(unittest.TestCase):
    """ test 'QComp' : 2-qubit gate
    """

    def test_cx(self):
        """test 'cx' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cx(0,1).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_cy(self):
        """test 'cy' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cy(0,1).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), -0.5j, 0.5j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_cz(self):
        """test 'cz' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cz(0,1).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (-0.5+0j)])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_cxr(self):
        """test 'cxr' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cxr(0,1).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_cxr_dg(self):
        """test 'cxr_dg' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cxr_dg(0,1).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_ch(self):
        """test 'ch' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).ch(0,1).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.7071067811865475+0j), 0j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_cs(self):
        """test 'cs' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cs(0,1).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), 0.5j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_cs_dg(self):
        """test 'cs_dg' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cs_dg(0,1).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), -0.5j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_ct(self):
        """test 'ct' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).ct(0,1).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.35355339059327373+0.35355339059327373j)])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_ct_dg(self):
        """test 'ct_dg' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).ct_dg(0,1).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.35355339059327373-0.35355339059327373j)])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_sw(self):
        """test 'sw' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).sw(0,1).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_sw(self):
        """test 'sw' gate (following 'x' gate, not 'h' gates)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.x(0).sw(0,1).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([0j, (1+0j), 0j, 0j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_cp(self):
        """test 'cp'gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cp(0,1, phase=0.25).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.3535533905932738+0.35355339059327373j)])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_crx(self):
        """test 'crx' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).crx(0,1, phase=0.25).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.4619397662556434-0.1913417161825449j),
                           (0.4619397662556434-0.1913417161825449j)])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_cry(self):
        """test 'cry' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cry(0,1, phase=0.25).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.2705980500730985+0j),
                           (0.6532814824381882+0j)])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_crz(self):
        """test 'crz' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).crz(0,1, phase=0.25).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j),(0.4619397662556434-0.1913417161825449j),
                           (0.4619397662556434+0.1913417161825449j)])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_cu1(self):
        """test 'cu1' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cu1(0,1, alpha=0.1).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.47552825814757677+0.1545084971874737j)])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_cu2(self):
        """test 'cu2' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cu2(0,1, alpha=0.1, beta=0.2).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.0173041346112951-0.10925400611220525j),
                           (0.49384417029756883+0.49384417029756883j)])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_cu3(self):
        """test 'cu3' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cu3(0,1, alpha=0.1, beta=0.2, gamma=0.3).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.22961795053748937-0.07014538985214754j),
                           (0.44550326209418395+0.4938441702975689j)])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

#
# 3-qubit gate
#

class TestQComp_3_qubit_qlazy_qstate_simulator(unittest.TestCase):
    """ test 'QComp' : 3-qubit gate
    """

    def test_ccx(self):
        """test 'ccx' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=3, backend=bk)
        res = qc.x(0).x(1).ccx(0,1,2).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([0j, 0j, 0j, 0j, 0j, 0j, 0j, (1+0j)])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

    def test_x_x_csw(self):
        """test 'csw' gate
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=3, backend=bk)
        res = qc.x(0).x(1).csw(0,1,2).run(reset_qubits=False)
        actual = qc.qstate.amp
        expect = np.array([0j, 0j, 0j, 0j, 0j, (1+0j), 0j, 0j])
        ans = equal_vectors(actual, expect)
        qc.free()
        self.assertEqual(ans,True)

#
# measurement
#

class TestQComp_measure_qstate_simulator(unittest.TestCase):
    """ test 'QComp' : various kind of measurements
    """

    def test_measure_mesurement_only(self):
        """test 'm' (measurement only)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.measure([0,1]).run(shots=10)
        qc.free()
        self.assertEqual(res['measured_qid'], [0,1])
        self.assertEqual(res['frequency']['00'], 10)

    def test_measure_simple(self):
        """test 'm' (simple case)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).cx(0,1).measure([0,1]).run(shots=10)
        qc.free()
        self.assertEqual(res['measured_qid'], [0,1])
        self.assertEqual(res['frequency']['00']+res['frequency']['11'], 10)

    def test_measure_use_cmem(self):
        """test 'm' (use classical memory)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, cmem_num=3, backend=bk)
        res = qc.h(0).cx(0,1).measure([0,1],[0,1]).run(shots=10, reset_cmem=False)
        self.assertEqual(res['measured_qid'], [0,1])
        self.assertEqual(res['frequency']['00']+res['frequency']['11'], 10)
        self.assertEqual(qc.cmem==[0,0,0] or qc.cmem==[1,1,0], True)
        qc.free()

    def test_measure_control_qubit(self):
        """test 'm' (control qubit using classical memory)
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = QComp(qubit_num=2, cmem_num=3, backend=bk)
        res = qc.h(0).cx(0,1).measure([0],[0]).x(0, ctrl=0).x(1, ctrl=0).measure([0,1]).run(shots=10)
        qc.free()
        self.assertEqual(res['measured_qid'], [0,1])
        self.assertEqual(res['frequency']['00'], 10)

#
# inheritance
#

class TestQComp_inheritance_qstate_simulator(unittest.TestCase):
    """ test 'QComp' : inheritance (qlazy_qstate_simulator)
    """

    def test_inheritance(self):
        """test 'inheritance'
        """
        bk = Backend('qlazy_qstate_simulator')
        qc = MyQComp(backend=bk, qubit_num=2, cmem_num=3)
        res = qc.bell(0,1).measure(qid=[0,1]).run(shots=10)
        qc.free()
        self.assertEqual(res['measured_qid'], [0,1])
        self.assertEqual(res['frequency']['00']+res['frequency']['11'], 10)

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
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=3, cmem_num=2, backend=bk)
        actual = qc.stab.get_str()
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
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=3, cmem_num=2, backend=bk)
        qc.h(0).h(1).h(2).run()
        qc.reset()
        actual = qc.stab.get_str()
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
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.x(0).run(reset_qubits=False)
        actual = qc.stab.get_str()
        expect = " -Z\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_h_x(self):
        """test 'x' gate (following 'h' gate)
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).x(0).run(reset_qubits=False)
        actual = qc.stab.get_str()
        expect = "  X\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_y(self):
        """test 'y' gate
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.y(0).run(reset_qubits=False)
        actual = qc.stab.get_str()
        expect = " -Z\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_h_y(self):
        """test 'y' gate (following 'h' gate)
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).y(0).run(reset_qubits=False)
        actual = qc.stab.get_str()
        expect = " -X\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_z(self):
        """test 'z' gate
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.z(0).run(reset_qubits=False)
        actual = qc.stab.get_str()
        expect = "  Z\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_h_z(self):
        """test 'z' gate (following 'h' gate)
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).z(0).run(reset_qubits=False)
        actual = qc.stab.get_str()
        expect = " -X\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_h(self):
        """test 'h' gate
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).run(reset_qubits=False)
        actual = qc.stab.get_str()
        expect = "  X\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_h_h(self):
        """test 'h' gate (following 'h' gate)
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).h(0).run(reset_qubits=False)
        actual = qc.stab.get_str()
        expect = "  Z\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_s(self):
        """test 's' gate
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.s(0).run(reset_qubits=False)
        actual = qc.stab.get_str()
        expect = "  Z\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_h_s(self):
        """test 's' gate (following 'h' gate)
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).s(0).run(reset_qubits=False)
        actual = qc.stab.get_str()
        expect = "  Y\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_s_dg(self):
        """test 's+' gate
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.s(0).run(reset_qubits=False)
        actual = qc.stab.get_str()
        expect = "  Z\n"
        self.assertEqual(actual, expect)
        qc.free()
        
    def test_h_s_dg(self):
        """test 's+' gate (following 'h' gate)
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=1, backend=bk)
        res = qc.h(0).s_dg(0).run(reset_qubits=False)
        actual = qc.stab.get_str()
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
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.cx(0,1).run(reset_qubits=False)
        actual = qc.stab.get_str()
        expect = "  ZI\n  ZZ\n"
        qc.free()
        self.assertEqual(actual, expect)

    def test_hh_cx(self):
        """test 'CX' (following 'h' gate)
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cx(0,1).run(reset_qubits=False)
        actual = qc.stab.get_str()
        expect = "  XX\n  IX\n"
        qc.free()
        self.assertEqual(actual, expect)

    def test_cy(self):
        """test 'CY'
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.cy(0,1).run(reset_qubits=False)
        actual = qc.stab.get_str()
        expect = "  ZI\n  ZZ\n"
        qc.free()
        self.assertEqual(actual, expect)

    def test_hh_cy(self):
        """test 'CY' (following 'h' gate)
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cy(0,1).run(reset_qubits=False)
        actual = qc.stab.get_str()
        expect = "-iXY\n  ZX\n"
        qc.free()
        self.assertEqual(actual, expect)

    def test_cz(self):
        """test 'CZ'
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.cz(0,1).run(reset_qubits=False)
        actual = qc.stab.get_str()
        expect = "  ZI\n  IZ\n"
        qc.free()
        self.assertEqual(actual, expect)

    def test_hh_cz(self):
        """test 'CZ' (folowint 'h' gate)
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).h(1).cz(0,1).run(reset_qubits=False)
        actual = qc.stab.get_str()
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
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.measure([0,1]).run(shots=10)
        qc.free()
        self.assertEqual(res['measured_qid'], [0,1])
        self.assertEqual(res['frequency']['00'], 10)

    def test_measure_simple(self):
        """test 'm' (simple case)
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=2, backend=bk)
        res = qc.h(0).cx(0,1).measure([0,1]).run(shots=10)
        qc.free()
        self.assertEqual(res['measured_qid'], [0,1])
        self.assertEqual(res['frequency']['00']+res['frequency']['11'], 10)

    def test_measure_use_cmem(self):
        """test 'm' (use classical memory)
        """
        bk = Backend('qlazy_stabilizer_simulator')
        qc = QComp(qubit_num=2, cmem_num=3, backend=bk)
        res = qc.h(0).cx(0,1).measure([0,1],[0,1]).run(shots=10, reset_cmem=False)
        self.assertEqual(res['measured_qid'], [0,1])
        self.assertEqual(res['frequency']['00']+res['frequency']['11'], 10)
        self.assertEqual(qc.cmem==[0,0,0] or qc.cmem==[1,1,0], True)
        qc.free()

    def test_measure_control_qubit(self):
        """test 'm' (control qubit using classical memory)
        """
        bk = Backend('qlazy_stabilizer_simulator')
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
        bk = Backend('qlazy_stabilizer_simulator')
        qc = MyQComp(backend=bk, qubit_num=2, cmem_num=3)
        res = qc.bell(0,1).measure(qid=[0,1]).run(shots=10)
        qc.free()
        self.assertEqual(res['measured_qid'], [0,1])
        self.assertEqual(res['frequency']['00']+res['frequency']['11'], 10)

if __name__ == '__main__':
    unittest.main()
