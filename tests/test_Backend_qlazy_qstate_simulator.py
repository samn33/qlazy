# -*- coding: utf-8 -*-
import unittest
import math
import numpy as np
import sys

from qlazy import QCirc, Backend, PauliProduct
from qlazy.Observable import X,Y,Z

EPS = 1.0e-6

SQRT_2 = np.sqrt(2.0)
COS_PI_8 = math.cos(math.pi/8)
COS_PI_4 = math.cos(math.pi/4)
SIN_PI_8 = math.sin(math.pi/8)
SIN_PI_4 = math.sin(math.pi/4)

class MyQCirc(QCirc):

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
# 1-qubit gate
#

class TestBackend_1_qubit_qlazy_qstate_simulator(unittest.TestCase):
    """ test 'Backend' : 1-qubit gate (qlazy_qstate_simulator)
    """

    def test_x(self):
        """test 'x' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().x(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([0.0, 1.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_x(self):
        """test 'x' gate (following 'h' gate)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).x(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0/SQRT_2, 1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_y(self):
        """test 'y' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().y(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([0.0, 1.0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_y(self):
        """test 'y' gate (following 'h' gate)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).y(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([-1.0j/SQRT_2, 1.0j/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_z(self):
        """test 'z' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().z(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_z(self):
        """test 'z' gate (following 'h' gate)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).z(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0/SQRT_2, -1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_xr(self):
        """test 'xr' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().xr(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([0.5+0.5j, 0.5-0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_xr(self):
        """test 'xr' gate (following 'h' gate)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).xr(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0/SQRT_2, 1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_xr_dg(self):
        """test 'xr_dg' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().xr_dg(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([0.5-0.5j, 0.5+0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_xr_dg(self):
        """test 'xr_dg' gate (following 'h' gate)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).xr_dg(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0/SQRT_2, 1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h(self):
        """test 'h' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0/SQRT_2, 1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_h(self):
        """test 'h' gate (following 'h')
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_s(self):
        """test 's' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().s(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_s(self):
        """test 's' gate (following 'h' gate)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).s(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0/SQRT_2, 1.0j/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_s_dg(self):
        """test 's_dg' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().s_dg(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_s_dg(self):
        """test 's_dg' gate (following 'h' gate)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).s_dg(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0/SQRT_2, -1.0j/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_t(self):
        """test 't' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().t(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_t(self):
        """test 't' gate (following 'h' gate)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).t(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0/SQRT_2, 0.5+0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_t_dg(self):
        """test 't_dg' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().t_dg(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_t_dg(self):
        """test 't_dg' gate (following 'h' gate)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).t_dg(0)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0/SQRT_2, 0.5-0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_rx(self):
        """test 'rx' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().rx(0, phase=0.25)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([COS_PI_8, -SIN_PI_8*1.0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_rx(self):
        """test 'rx' gate (following 'h' gate)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).rx(0, phase=0.25)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([0.65328148-0.27059805j, 0.65328148-0.27059805j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_ry(self):
        """test 'ry' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().ry(0, phase=0.25)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([COS_PI_8, SIN_PI_8])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_ry(self):
        """test 'ry' gate (following 'h' gate)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).ry(0, phase=0.25)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([0.38268343+0.j, 0.92387953+0.j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_rz(self):
        """test 'rz' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().rz(0, phase=0.25)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_rz(self):
        """test 'rz' gate (following 'h' gate)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).rz(0, phase=0.25)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([0.65328148-0.27059805j, 0.65328148+0.27059805j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_p(self):
        """test 'p' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().p(0, phase=0.25)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_p(self):
        """test 'p' gate (following 'h' gate)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).p(0, phase=0.25)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([0.70710678, 0.5+0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

#
# 2-qubit gate
#

class TestBackend_2_qubit_qlazy_qstate_simulator(unittest.TestCase):
    """ test 'Backend' : 2-qubit gate
    """

    def test_cx(self):
        """test 'cx' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).cx(0,1)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cy(self):
        """test 'cy' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).cy(0,1)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), -0.5j, 0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cz(self):
        """test 'cz' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).cz(0,1)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (-0.5+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cxr(self):
        """test 'cxr' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).cxr(0,1)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cxr_dg(self):
        """test 'cxr_dg' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).cxr_dg(0,1)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_ch(self):
        """test 'ch' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).ch(0,1)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.7071067811865475+0j), 0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cs(self):
        """test 'cs' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).cs(0,1)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), 0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cs_dg(self):
        """test 'cs_dg' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).cs_dg(0,1)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), -0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_ct(self):
        """test 'ct' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).ct(0,1)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.35355339059327373+0.35355339059327373j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_ct_dg(self):
        """test 'ct_dg' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).ct_dg(0,1)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.35355339059327373-0.35355339059327373j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_sw(self):
        """test 'sw' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).sw(0,1)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_x_sw(self):
        """test 'sw' gate (following 'x' gate, not 'h' gates)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().x(0).sw(0,1)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([0j, (1+0j), 0j, 0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cp(self):
        """test 'cp'gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).cp(0,1, phase=0.25)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.3535533905932738+0.35355339059327373j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_crx(self):
        """test 'crx' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).crx(0,1, phase=0.25)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.4619397662556434-0.1913417161825449j),
                           (0.4619397662556434-0.1913417161825449j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cry(self):
        """test 'cry' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).cry(0,1, phase=0.25)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.2705980500730985+0j),
                           (0.6532814824381882+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_crz(self):
        """test 'crz' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).crz(0,1, phase=0.25)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.5+0j), (0.5+0j),(0.4619397662556434-0.1913417161825449j),
                           (0.4619397662556434+0.1913417161825449j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_rxx(self):
        """test 'rxx' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).rxx(0, 1, phase=0.25)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.46193977-0.19134172j), (0.46193977-0.19134172j),
                           (0.46193977-0.19134172j), (0.46193977-0.19134172j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)
        
    def test_ryy(self):
        """test 'ryy' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).ryy(0, 1, phase=0.25)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.46193977+0.19134172j), (0.46193977-0.19134172j),
                           (0.46193977-0.19134172j), (0.46193977+0.19134172j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)
        
    def test_rzz(self):
        """test 'rzz' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).rzz(0, 1, phase=0.25)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([(0.46193977-0.19134172j), (0.46193977+0.19134172j),
                           (0.46193977+0.19134172j), (0.46193977-0.19134172j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

#
# 3-qubit gate
#

class TestBackend_3_qubit_qlazy_qstate_simulator(unittest.TestCase):
    """ test 'Backend' : 3-qubit gate
    """

    def test_ccx(self):
        """test 'ccx' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().x(0).x(1).ccx(0,1,2)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([0j, 0j, 0j, 0j, 0j, 0j, 0j, (1+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_x_x_csw(self):
        """test 'csw' gate
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().x(0).x(1).csw(0,1,2)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        expect = np.array([0j, 0j, 0j, 0j, 0j, (1+0j), 0j, 0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

#
# operate
#

class TestBackend_operate_qlazy_qstate_simulator(unittest.TestCase):
    """ test 'Backend' : operate
    """

    def test_operate_x(self):
        """test 'operate' (x)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().x(0)
        res = bk.run(qcirc=qc, out_state=True)
        expect = res.qstate.amp
        pp = PauliProduct(pauli_str="X")
        qc = QCirc().operate(pp=pp)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_operate_h_x(self):
        """test 'operate' (x followed by h)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).x(0)
        res = bk.run(qcirc=qc, out_state=True)
        expect = res.qstate.amp
        pp = PauliProduct(pauli_str="X")
        qc = QCirc().h(0).operate(pp=pp)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_operate_h_y(self):
        """test 'operate' (Y followed by h)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).y(0)
        res = bk.run(qcirc=qc, out_state=True)
        expect = res.qstate.amp

        pp = PauliProduct(pauli_str="Y")
        qc = QCirc().h(0).operate(pp=pp)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp

        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_operate_h_z(self):
        """test 'operate' (Z followed by h)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).z(0)
        res = bk.run(qcirc=qc, out_state=True)
        expect = res.qstate.amp
        pp = PauliProduct(pauli_str="Z")
        qc = QCirc().h(0).operate(pp=pp)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_operate_xyz(self):
        """test 'operate' (xyz)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().x(2).y(0).z(1)
        res = bk.run(qcirc=qc, out_state=True)
        expect = res.qstate.amp
        pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
        qc = QCirc().operate(pp=pp)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_operate_controlled_xyz(self):
        """test 'operate' (controlled_xyz)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().cx(3,2).cy(3,0).cz(3,1)
        res = bk.run(qcirc=qc, out_state=True)
        expect = res.qstate.amp
        pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
        qc = QCirc().operate(pp=pp, ctrl=3)
        res = bk.run(qcirc=qc, out_state=True)
        actual = res.qstate.amp
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

#
# measurement
#

class TestBackend_measure_qstate_simulator(unittest.TestCase):
    """ test 'Backend' : various kind of measurements
    """

    def test_measure_mesurement_only_1(self):
        """test 'measure' (measurement only (1))
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().measure(qid=[0,1], cid=[0,1])
        res = bk.run(qcirc=qc, shots=10)
        freq = res.frequency
        cid = res.cid
        self.assertEqual(freq['00'], 10)
        self.assertEqual(cid, [0,1])
    
    def test_measure_mesurement_only_2(self):
        """test 'measure' (measurement only (2))
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().measure(qid=[0,1], cid=[1,2])
        res = bk.run(qcirc=qc, shots=10, cid=[1,2])
        freq = res.frequency
        cid = res.cid
        self.assertEqual(freq['00'], 10)
        self.assertEqual(cid, [1,2])
    
    def test_measure_mesurement_only_3(self):
        """test 'measure' (measurement only (3))
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().measure(qid=[0,1], cid=[0,1])
        res = bk.run(qcirc=qc, shots=10)
        freq = res.frequency
        cid = res.cid
        self.assertEqual(freq['00'], 10)
        self.assertEqual(cid, [0,1])
    
    def test_measure_mesurement_unitary(self):
        """test 'measure' (measurement-unitary)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().measure(qid=[0,1], cid=[1,2]).h(0).cx(0,1)
        res = bk.run(qcirc=qc, shots=10, cid=[1,2], out_state=True)
        freq = res.frequency
        cid = res.cid
        actual = res.qstate.amp
        expect = np.array([(0.7071067811865476+0j), 0j, 0j, (0.7071067811865476+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(freq['00'], 10)
        self.assertEqual(ans, True)
        self.assertEqual(cid, [1,2])
    
    def test_measure_unitary_measurement_with_cmem(self):
        """test 'measure' (unitary-measurement with cmem)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
        res = bk.run(qcirc=qc, shots=10, cid=[0,1])
        freq = res.frequency
        cid = res.cid
        ans = (freq['00']+freq['11'] == 10) and (freq['00'] != 0) and (freq['11'] != 0)
        self.assertEqual(ans, True)
        self.assertEqual(cid, [0,1])
    
    def test_measure_mesurement_unitary_measurement(self):
        """test 'measure' (meaurement-unitary-measrement)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().measure(qid=[0,1], cid=[1,2]).x(0).measure(qid=[0,1], cid=[2,0])
        res = bk.run(qcirc=qc, shots=10, cid=[0,1,2], out_state=True)
        freq = res.frequency
        cid = res.cid
        qstate = res.qstate
        cmem = res.cmem
        self.assertEqual(freq['001'], 10)
        self.assertEqual(cid, [0,1,2])
        self.assertEqual(list(qstate.amp), [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j])
        self.assertEqual(list(cmem.bits), [0,0,1])

    def test_measure_unitary_measuremen_cunitary_measurement(self):
        """test 'measure' (unitary-measurement-cunitary-measurement)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).cx(0,1).measure(qid=[0], cid=[0]).x(0, ctrl=0).x(1, ctrl=0).measure(qid=[0,1], cid=[0,1])
        res = bk.run(qcirc=qc, shots=10)
        freq = res.frequency
        cid = res.cid
        self.assertEqual(freq['00'], 10)
        self.assertEqual(cid, [0,1])

#
# reset
#

class TestBackend_reset_qstate_simulator(unittest.TestCase):
    """ test 'Backend' : various kind of resets
    """

    def test_reset_simple_all(self):
        """test 'reset' (simple_all)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().x(0).x(1).reset(qid=[0,1,2]).measure(qid=[0,1,2], cid=[0,1,2])
        res = bk.run(qcirc=qc, shots=10)
        freq = res.frequency
        self.assertEqual(freq['000'], 10)

    def test_reset_simple_partial(self):
        """test 'reset' (simple_partial)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().x(0).x(1).reset(qid=[1]).measure(qid=[0,1], cid=[0,1])
        res = bk.run(qcirc=qc, shots=10)
        freq = res.frequency
        self.assertEqual(freq['10'], 10)

    def test_reset_unitary_measure_reset(self):
        """test 'reset' (unitary-measure-reset)
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().x(0).x(1).measure(qid=[0,1,2], cid=[0,1,2]).reset(qid=[1]).measure(qid=[0,1], cid=[0,1])
        res = bk.run(qcirc=qc, shots=10, cid=[0,1])
        freq = res.frequency
        self.assertEqual(freq['10'], 10)

#
# expect
#

class TestBackend_expect_qstate_simulator(unittest.TestCase):
    """ test 'Backend' : expectation value
    """

    def test_1(self):
        """test 'X(0)X(1)+X(1)X(2)/2'
        """
        ob = X(0)*X(1) + 0.5*X(1)*X(2)
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).h(2).h(3)
        expval_1 = bk.expect(qcirc=qc, observable=ob, precise=True)
        expval_2 = bk.expect(qcirc=qc, observable=ob, shots=10000)
        self.assertEqual(expval_1.imag == 0.0, True)
        self.assertEqual(expval_2.imag == 0.0, True)
        self.assertEqual(abs(expval_1.real - expval_2.real) < 0.05, True)
        
    def test_2(self):
        """test 'Y(0)Y(1)+Y(1)Y(2)/2'
        """
        ob = Y(0)*Y(1) + 0.5*Y(1)*Y(2)
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).h(2).h(3)
        expval_1 = bk.expect(qcirc=qc, observable=ob, precise=True)
        expval_2 = bk.expect(qcirc=qc, observable=ob, shots=10000)
        self.assertEqual(expval_1.imag == 0.0, True)
        self.assertEqual(expval_2.imag == 0.0, True)
        self.assertEqual(abs(expval_1.real - expval_2.real) < 0.05, True)
        
    def test_3(self):
        """test 'Z(0)Z(1)+Z(1)Z(2)/2'
        """
        ob = Z(0)*Z(1) + 0.5*Z(1)*Z(2)
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = QCirc().h(0).h(1).h(2).h(3)
        expval_1 = bk.expect(qcirc=qc, observable=ob, precise=True)
        expval_2 = bk.expect(qcirc=qc, observable=ob, shots=10000)
        self.assertEqual(expval_1.imag == 0.0, True)
        self.assertEqual(expval_2.imag == 0.0, True)
        self.assertEqual(abs(expval_1.real - expval_2.real) < 0.05, True)

#
# inheritance
#

class TestBackend_inheritance_qstate_simulator(unittest.TestCase):
    """ test 'Backend' : inheritance (qlazy_qstate_simulator)
    """

    def test_inheritance(self):
        """test 'inheritance'
        """
        bk = Backend(product='qlazy', device='qstate_simulator')
        qc = MyQCirc().bell(0,1).measure(qid=[0,1], cid=[0,1])
        res = bk.run(qcirc=qc, shots=10)
        freq = res.frequency
        ans = (freq['00']+freq['11'] == 10) and (freq['00'] != 0) and (freq['11'] != 0)
        self.assertEqual(ans, True)

if __name__ == '__main__':
    unittest.main()
