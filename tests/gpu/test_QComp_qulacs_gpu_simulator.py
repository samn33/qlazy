# -*- coding: utf-8 -*-
import unittest
import math
import numpy as np
import sys

from qlazy import QComp, Backend, PauliProduct
from qlazy.util import *

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

#===================
# qulacs_simulator
#===================

#
# 1-qubit gate
#

class TestQComp_1_qubit_qulacs_gpu_simulator(unittest.TestCase):
    """ test 'QComp' : 1-qubit gate (qulacs_simulator)
    """

    def test_x(self):
        """test 'x' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.x(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([0.0, 1.0]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_x(self):
        """test 'x' gate (following 'h' gate)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).x(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0/SQRT_2, 1.0/SQRT_2]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_y(self):
        """test 'y' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.y(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([0.0, 1.0j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_y(self):
        """test 'y' gate (following 'h' gate)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).y(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([-1.0j/SQRT_2, 1.0j/SQRT_2]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_z(self):
        """test 'z' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.z(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0, 0.0]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_z(self):
        """test 'z' gate (following 'h' gate)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).z(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0/SQRT_2, -1.0/SQRT_2]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_xr(self):
        """test 'xr' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.xr(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([0.5+0.5j, 0.5-0.5j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_xr(self):
        """test 'xr' gate (following 'h' gate)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).xr(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0/SQRT_2, 1.0/SQRT_2]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_xr_dg(self):
        """test 'xr_dg' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.xr_dg(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([0.5-0.5j, 0.5+0.5j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_xr_dg(self):
        """test 'xr_dg' gate (following 'h' gate)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).xr_dg(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0/SQRT_2, 1.0/SQRT_2]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h(self):
        """test 'h' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0/SQRT_2, 1.0/SQRT_2]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_h(self):
        """test 'h' gate (following 'h')
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0, 0.0]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_s(self):
        """test 's' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.s(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0, 0.0]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_s(self):
        """test 's' gate (following 'h' gate)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).s(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0/SQRT_2, 1.0j/SQRT_2]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_s_dg(self):
        """test 's_dg' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.s_dg(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0, 0.0]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_s_dg(self):
        """test 's_dg' gate (following 'h' gate)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).s_dg(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0/SQRT_2, -1.0j/SQRT_2]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_t(self):
        """test 't' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.t(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0, 0.0]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_t(self):
        """test 't' gate (following 'h' gate)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).t(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0/SQRT_2, 0.5+0.5j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_t_dg(self):
        """test 't_dg' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.t_dg(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0, 0.0]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_t_dg(self):
        """test 't_dg' gate (following 'h' gate)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).t_dg(0).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0/SQRT_2, 0.5-0.5j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_rx(self):
        """test 'rx' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.rx(0, phase=0.25).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([COS_PI_8, -SIN_PI_8*1.0j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_rx(self):
        """test 'rx' gate (following 'h' gate)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).rx(0, phase=0.25).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([0.65328148-0.27059805j, 0.65328148-0.27059805j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_ry(self):
        """test 'ry' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.ry(0, phase=0.25).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([COS_PI_8, SIN_PI_8]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_ry(self):
        """test 'ry' gate (following 'h' gate)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).ry(0, phase=0.25).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([0.38268343+0.j, 0.92387953+0.j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_rz(self):
        """test 'rz' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.rz(0, phase=0.25).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0, 0.0]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_rz(self):
        """test 'rz' gate (following 'h' gate)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).rz(0, phase=0.25).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([0.65328148-0.27059805j, 0.65328148+0.27059805j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_p(self):
        """test 'p' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.p(0, phase=0.25).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0, 0.0]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_p(self):
        """test 'p' gate (following 'h' gate)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).p(0, phase=0.25).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([0.70710678, 0.5+0.5j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_u1(self):
        """test 'u1' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.u1(0, alpha=0.1).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([1.0, 0.0]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_u1(self):
        """test 'u1' gate (following 'h' gate)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).u1(0, alpha=0.1).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([0.70710678+0.j, 0.67249851+0.21850801j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_u2(self):
        """test 'u2' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.u2(0, alpha=0.1, beta=0.2).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([0.70710678+0.j, 0.5720614 +0.41562694j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_u2(self):
        """test 'u2' gate (following 'h' gate)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).u2(0, alpha=0.1, beta=0.2).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([0.02447174-0.1545085j,0.69840112+0.69840112j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_u3(self):
        """test 'u3' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.u3(0, alpha=0.1, beta=0.2, gamma=0.3).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([0.89100652+0.j, 0.36728603+0.26684892j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_u3(self):
        """test 'u3' gate (following 'h' gate)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).u3(0, alpha=0.1, beta=0.2, gamma=0.3).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([0.32472882-0.09920056j, 0.63003676+0.69840112j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

#
# 2-qubit gate
#

class TestQComp_2_qubit_qulacs_gpu_simulator(unittest.TestCase):
    """ test 'QComp' : 2-qubit gate
    """

    def test_cx(self):
        """test 'cx' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).cx(0,1).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cy(self):
        """test 'cy' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).cy(0,1).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), -0.5j, 0.5j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cz(self):
        """test 'cz' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).cz(0,1).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), (0.5+0j), (-0.5+0j)]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cxr(self):
        """test 'cxr' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).cxr(0,1).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cxr_dg(self):
        """test 'cxr_dg' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).cxr_dg(0,1).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_ch(self):
        """test 'ch' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).ch(0,1).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), (0.7071067811865475+0j), 0j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cs(self):
        """test 'cs' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).cs(0,1).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), (0.5+0j), 0.5j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cs_dg(self):
        """test 'cs_dg' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).cs_dg(0,1).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), (0.5+0j), -0.5j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_ct(self):
        """test 'ct' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).ct(0,1).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.35355339059327373+0.35355339059327373j)]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_ct_dg(self):
        """test 'ct_dg' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).ct_dg(0,1).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.35355339059327373-0.35355339059327373j)]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_sw(self):
        """test 'sw' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).sw(0,1).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_x_sw(self):
        """test 'sw' gate (following 'x' gate, not 'h' gates)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.x(0).sw(0,1).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([0j, (1+0j), 0j, 0j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cp(self):
        """test 'cp'gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).cp(0,1, phase=0.25).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                                             (0.3535533905932738+0.35355339059327373j)]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_crx(self):
        """test 'crx' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).crx(0,1, phase=0.25).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), (0.4619397662556434-0.1913417161825449j),
                                             (0.4619397662556434-0.1913417161825449j)]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cry(self):
        """test 'cry' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).cry(0,1, phase=0.25).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), (0.2705980500730985+0j),
                                             (0.6532814824381882+0j)]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_crz(self):
        """test 'crz' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).crz(0,1, phase=0.25).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j),(0.4619397662556434-0.1913417161825449j),
                           (0.4619397662556434+0.1913417161825449j)]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cu1(self):
        """test 'cu1' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).cu1(0,1, alpha=0.1).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.47552825814757677+0.1545084971874737j)]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cu2(self):
        """test 'cu2' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).cu2(0,1, alpha=0.1, beta=0.2).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), (0.0173041346112951-0.10925400611220525j),
                                             (0.49384417029756883+0.49384417029756883j)]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cu3(self):
        """test 'cu3' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).h(1).cu3(0,1, alpha=0.1, beta=0.2, gamma=0.3).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([(0.5+0j), (0.5+0j), (0.22961795053748937-0.07014538985214754j),
                                             (0.44550326209418395+0.4938441702975689j)]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

#
# 3-qubit gate
#

class TestQComp_3_qubit_qulacs_gpu_simulator(unittest.TestCase):
    """ test 'QComp' : 3-qubit gate
    """

    def test_ccx(self):
        """test 'ccx' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.x(0).x(1).ccx(0,1,2).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([0j, 0j, 0j, 0j, 0j, 0j, 0j, (1+0j)]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_x_x_csw(self):
        """test 'csw' gate
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.x(0).x(1).csw(0,1,2).run()
        actual = res.info['quantumstate'].get_vector()
        expect = reverse_bit_order(np.array([0j, 0j, 0j, 0j, 0j, (1+0j), 0j, 0j]))
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

#
# operate
#

class TestQComp_operate_qulacs_gpu_simulator(unittest.TestCase):
    """ test 'QComp' : operate
    """

    def test_operate_x(self):
        """test 'operate' (x)
        """
        qc_expect = QComp(product='qulacs', device='gpu_simulator').x(0)
        res = qc_expect.run()
        expect = res.info['quantumstate'].get_vector()
        pp = PauliProduct(pauli_str="X")
        qc_actual = QComp(product='qulacs', device='gpu_simulator').operate(pp=pp)
        res = qc_actual.run()
        actual = res.info['quantumstate'].get_vector()
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_operate_h_x(self):
        """test 'operate' (x followed by h)
        """
        qc_expect = QComp(product='qulacs', device='gpu_simulator').h(0).x(0)
        res = qc_expect.run()
        expect = res.info['quantumstate'].get_vector()
        pp = PauliProduct(pauli_str="X")
        qc_actual = QComp(product='qulacs', device='gpu_simulator').h(0).operate(pp=pp)
        res = qc_actual.run()
        actual = res.info['quantumstate'].get_vector()
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_operate_h_y(self):
        """test 'operate' (Y followed by h)
        """
        qc_expect = QComp(product='qulacs', device='gpu_simulator').h(0).y(0)
        res = qc_expect.run()
        expect = res.info['quantumstate'].get_vector()
        pp = PauliProduct(pauli_str="Y")
        qc_actual = QComp(product='qulacs', device='gpu_simulator').h(0).operate(pp=pp)
        res = qc_actual.run()
        actual = res.info['quantumstate'].get_vector()
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_operate_h_z(self):
        """test 'operate' (Z followed by h)
        """
        qc_expect = QComp(product='qulacs', device='gpu_simulator').h(0).z(0)
        res = qc_expect.run()
        expect = res.info['quantumstate'].get_vector()
        pp = PauliProduct(pauli_str="Z")
        qc_actual = QComp(product='qulacs', device='gpu_simulator').h(0).operate(pp=pp)
        res = qc_actual.run()
        actual = res.info['quantumstate'].get_vector()
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_operate_xyz(self):
        """test 'operate' (xyz)
        """
        qc_expect = QComp(product='qulacs', device='gpu_simulator').x(2).y(0).z(1)
        res = qc_expect.run()
        expect = res.info['quantumstate'].get_vector()
        pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
        qc_actual = QComp(product='qulacs', device='gpu_simulator').operate(pp=pp)
        res = qc_actual.run()
        actual = res.info['quantumstate'].get_vector()
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_operate_controlled_xyz(self):
        """test 'operate' (controlled_xyz)
        """
        qc_expect = QComp(product='qulacs', device='gpu_simulator').cx(3,2).cy(3,0).cz(3,1)
        res = qc_expect.run()
        expect = res.info['quantumstate'].get_vector()
        pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
        qc_actual = QComp(product='qulacs', device='gpu_simulator').operate(pp=pp, ctrl=3)
        res = qc_actual.run()
        actual = res.info['quantumstate'].get_vector()
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)
        
#
# measurement
#

class TestQComp_measure_qulacs_gpu_simulator(unittest.TestCase):
    """ test 'QComp' : various kind of measurements
    """

    def test_measure_mesurement_only_1(self):
        """test 'measure' (measurement only (1))
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.measure(qid=[0,1], cid=[0,1]).run(shots=10)
        freq = res.frequency
        cid = res.cid
        self.assertEqual(freq['00'], 10)
        self.assertEqual(cid, [0,1])
    
    def test_measure_mesurement_only_2(self):
        """test 'measure' (measurement only (2))
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.measure(qid=[0,1], cid=[1,2]).run(shots=10, cid=[1,2])
        freq = res.frequency
        cid = res.cid
        self.assertEqual(freq['00'], 10)
        self.assertEqual(cid, [1,2])
    
    def test_measure_mesurement_only_3(self):
        """test 'measure' (measurement only (3))
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.measure(qid=[0,1], cid=[0,1]).run(shots=10)
        freq = res.frequency
        cid = res.cid
        self.assertEqual(freq['00'], 10)
        self.assertEqual(cid, [0,1])
    
    def test_measure_mesurement_only_4(self):
        """test 'measure' (measurement only (4))
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.measure(qid=[0,1]).run(shots=10)
        self.assertEqual(res.frequency, None)

    def test_measure_mesurement_unitary(self):
        """test 'measure' (measurement-unitary)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.measure(qid=[0,1], cid=[1,2]).h(0).cx(0,1).run(shots=10, cid=[1,2])
        freq = res.frequency
        cid = res.cid
        expect = np.array([(0.7071067811865476+0j), 0j, 0j, (0.7071067811865476+0j)])
        actual = res.info['quantumstate'].get_vector()
        ans = equal_vectors(actual, expect)
        self.assertEqual(freq['00'], 10)
        self.assertEqual(ans, True)
        self.assertEqual(cid, [1,2])
    
    def test_measure_unitary_measurement_with_no_cmem(self):
        """test 'measure' (unitary-meausrement with no cmem)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).cx(0,1).measure(qid=[0,1]).run(shots=10)
        expect_1 = np.array([1+0j, 0j, 0j, 0j])
        expect_2 = np.array([0j, 0j, 0j, 1+0j])
        actual = res.info['quantumstate'].get_vector()
        ans_1 = equal_vectors(actual, expect_1)
        ans_2 = equal_vectors(actual, expect_2)
        self.assertEqual(ans_1 or ans_2, True)
    
    def test_measure_unitary_measurement_with_cmem(self):
        """test 'measure' (unitary-measurement with cmem)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).cx(0,1).measure(qid=[0,1], cid=[0,1]).run(shots=10, cid=[0,1])
        freq = res.frequency
        cid = res.cid
        ans = (freq['00']+freq['11'] == 10) and (freq['00'] != 0) and (freq['11'] != 0)
        self.assertEqual(ans, True)
        self.assertEqual(cid, [0,1])
    
    def test_measure_unitary_measurement_with_cmem_norecord(self):
        """test 'measure' (unitary-measurement with cmem norecord)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).cx(0,1).measure(qid=[0,1]).run(shots=10)
        freq = res.frequency
        cid = res.cid
        self.assertEqual(freq, None)
        self.assertEqual(cid, [])

    def test_measure_mesurement_unitary_measurement(self):
        """test 'measure' (meaurement-unitary-measrement)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.measure(qid=[0,1], cid=[1,2]).x(0).measure(qid=[0,1], cid=[2,0]).run(shots=10, cid=[0,1,2])
        freq = res.frequency
        cid = res.cid
        self.assertEqual(freq['001'], 10)
        self.assertEqual(cid, [0,1,2])
    
    def test_measure_unitary_measuremen_cunitary_measurement(self):
        """test 'measure' (unitary-measurement-cunitary-measurement)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.h(0).cx(0,1).measure(qid=[0], cid=[0]).x(0, ctrl=0).x(1, ctrl=0).measure(qid=[0,1], cid=[0,1]).run(shots=10)
        freq = res.frequency
        cid = res.cid
        self.assertEqual(freq['00'], 10)
        self.assertEqual(cid, [0,1])

#
# reset
#

class TestQComp_reset_qulacs_gpu_simulator(unittest.TestCase):
    """ test 'QComp' : various kind of resets
    """

    def test_reset_simple_all(self):
        """test 'reset' (simple_all)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.x(0).x(1).reset(qid=[0,1,2]).measure(qid=[0,1,2], cid=[0,1,2]).run(shots=10)
        freq = res.frequency
        self.assertEqual(freq['000'], 10)

    def test_reset_simple_partial(self):
        """test 'reset' (simple_partial)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.x(0).x(1).reset(qid=[1]).measure(qid=[0,1], cid=[0,1]).run(shots=10)
        freq = res.frequency
        self.assertEqual(freq['10'], 10)

    def test_reset_unitary_measure_reset(self):
        """test 'reset' (unitary-measure-reset)
        """
        qc = QComp(product='qulacs', device='gpu_simulator')
        res = qc.x(0).x(1).measure(qid=[0,1,2]).reset(qid=[1]).measure(qid=[0,1], cid=[0,1]).run(shots=10, cid=[0,1])
        freq = res.frequency
        self.assertEqual(freq['10'], 10)

#
# inheritance
#

class TestQComp_inheritance_qulacs_gpu_simulator(unittest.TestCase):
    """ test 'QComp' : inheritance (qulacs_gpu_simulator)
    """

    def test_inheritance(self):
        """test 'inheritance'
        """
        qc = MyQComp(product='qulacs', device='gpu_simulator')
        res = qc.bell(0,1).measure(qid=[0,1], cid=[0,1]).run(shots=10)
        freq = res.frequency
        ans = (freq['00']+freq['11'] == 10) and (freq['00'] != 0) and (freq['11'] != 0)
        self.assertEqual(ans, True)

if __name__ == '__main__':
    unittest.main()
