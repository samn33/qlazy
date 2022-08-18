# -*- coding: utf-8 -*-
import unittest
import random
import math
import numpy as np
from qlazy import MPState, PauliProduct, QState

EPS = 1.0e-6

SQRT_2 = np.sqrt(2.0)
COS_PI_8 = math.cos(math.pi/8)
COS_PI_4 = math.cos(math.pi/4)
SIN_PI_8 = math.sin(math.pi/8)
SIN_PI_4 = math.sin(math.pi/4)

class MyMPState(MPState):

    def __init__(self, qubit_num=0, tensors=None, name=None):
        super().__init__(qubit_num=qubit_num, tensors=tensors)
        self.name = name

    def get_name(self):
        return self.name
     
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

def is_norm_one(vec):

    norm = abs(np.vdot(vec, vec))
    if abs(norm - 1.0) < EPS:
        return True
    else:
        return False

def equal_mpstates(mps_0, mps_1):

    fid = mps_0.fidelity(mps_1)
    if abs(fid - 1.0) < EPS:
        return True
    else:
        return False

class TestMPState_init(unittest.TestCase):
    """ test 'MPState' : '__init__'
    """

    def test_init(self):
        """test '__init__'
        """
        mps = MPState(qubit_num=3)
        actual = mps.amp
        expect = np.array([1.+0.j, 0.j, 0j, 0j, 0j, 0j, 0j, 0j])
        self.assertEqual(is_norm_one(actual),True)
        self.assertEqual(equal_vectors(actual, expect), True)

class TestMPState_del_all(unittest.TestCase):
    """ test 'MPState' : 'del_all'
    """

    def test_del_all(self):
        """test 'free_all'
        """
        mps_0 = MPState(1)
        mps_1 = MPState(1).x(0)
        mps_2 = MPState(1).h(0)
        MPState.del_all(mps_0, mps_1, mps_2)

        mps_0 = MPState(1)
        mps_1 = MPState(1).x(0)
        mps_2 = MPState(1).h(0)
        mps_A = [mps_1, mps_2]
        MPState.del_all(mps_0,mps_A)

        mps_0 = MPState(1)
        mps_1 = MPState(1).x(0)
        mps_2 = MPState(1).h(0)
        mps_B = [mps_0,[mps_1, mps_2]]
        MPState.del_all(mps_B)

class TestMPState_reset(unittest.TestCase):
    """ test 'MPState' : 'reset'
    """

    def test_reset_all(self):
        """test 'reset_all'
        """
        mps = MPState(qubit_num=3).h(0).h(1).h(2)
        mps.reset()
        actual = mps.amp
        expect = np.array([1.+0.j, 0j, 0j, 0j, 0j, 0j, 0j, 0j])
        self.assertEqual(is_norm_one(actual),True)
        self.assertEqual(equal_vectors(actual, expect), True)

    def test_reset_partial(self):
        """test 'reset_partial'
        """
        mps = MPState(qubit_num=3).h(0).cx(0,1).cx(1,2)
        mps.reset(qid=[0])
        actual = mps.amp
        expect_0 = np.array([1.+0.j, 0.j, 0.j, 0.j, 0.j, 0.j, 0.j, 0.j])
        expect_1 = np.array([0.j, 0.j, 0.j, 1.+0.j, 0.j, 0.j, 0.j, 0.j])
        ans = (equal_vectors(actual, expect_0) or equal_vectors(actual, expect_1))
        self.assertEqual(is_norm_one(actual),True)
        self.assertEqual(ans, True)

class TestMPState_1_qubit(unittest.TestCase):
    """ test 'MPState' : 1-qubit gate
    """

    def test_x(self):
        """test 'x' gate
        """
        mps = MPState(qubit_num=1).x(0)
        actual = mps.amp
        expect = np.array([0.0, 1.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans, True)

    def test_h_x(self):
        """test 'x' gate (following 'h' gate)
        """
        mps = MPState(qubit_num=1).h(0).x(0)
        actual = mps.amp
        expect = np.array([1.0/SQRT_2, 1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_y(self):
        """test 'y' gate
        """
        mps = MPState(qubit_num=1).y(0)
        actual = mps.amp
        expect = np.array([0.0, 1.0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_y(self):
        """test 'y' gate (following 'h' gate)
        """
        mps = MPState(qubit_num=1).h(0).y(0)
        actual = mps.amp
        expect = np.array([-1.0j/SQRT_2, 1.0j/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_z(self):
        """test 'z' gate
        """
        mps = MPState(qubit_num=1).z(0)
        actual = mps.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_z(self):
        """test 'z' gate (following 'h' gate)
        """
        mps = MPState(qubit_num=1).h(0).z(0)
        actual = mps.amp
        expect = np.array([1.0/SQRT_2, -1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_xr(self):
        """test 'xr' gate
        """
        mps = MPState(qubit_num=1).xr(0)
        actual = mps.amp
        expect = np.array([0.5+0.5j, 0.5-0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_xr(self):
        """test 'xr' gate (following 'h' gate)
        """
        mps = MPState(qubit_num=1).h(0).xr(0)
        actual = mps.amp
        expect = np.array([1.0/SQRT_2, 1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_xr_dg(self):
        """test 'xr_dg' gate
        """
        mps = MPState(qubit_num=1).xr_dg(0)
        actual = mps.amp
        expect = np.array([0.5-0.5j, 0.5+0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_xr_dg(self):
        """test 'xr_dg' gate (following 'h' gate)
        """
        mps = MPState(qubit_num=1).h(0).xr_dg(0)
        actual = mps.amp
        expect = np.array([1.0/SQRT_2, 1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h(self):
        """test 'h' gate
        """
        mps = MPState(qubit_num=1).h(0)
        actual = mps.amp
        expect = np.array([1.0/SQRT_2, 1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_h(self):
        """test 'h' gate (following 'h')
        """
        mps = MPState(qubit_num=1).h(0).h(0)
        actual = mps.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_s(self):
        """test 's' gate
        """
        mps = MPState(qubit_num=1).s(0)
        actual = mps.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_s(self):
        """test 's' gate (following 'h' gate)
        """
        mps = MPState(qubit_num=1).h(0).s(0)
        actual = mps.amp
        expect = np.array([1.0/SQRT_2, 1.0j/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_s_dg(self):
        """test 's_dg' gate
        """
        mps = MPState(qubit_num=1).s_dg(0)
        actual = mps.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_s_dg(self):
        """test 's_dg' gate (following 'h' gate)
        """
        mps = MPState(qubit_num=1).h(0).s_dg(0)
        actual = mps.amp
        expect = np.array([1.0/SQRT_2, -1.0j/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_t(self):
        """test 't' gate
        """
        mps = MPState(qubit_num=1).t(0)
        actual = mps.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_t(self):
        """test 't' gate (following 'h' gate)
        """
        mps = MPState(qubit_num=1).h(0).t(0)
        actual = mps.amp
        expect = np.array([1.0/SQRT_2, 0.5+0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_t_dg(self):
        """test 't_dg' gate
        """
        mps = MPState(qubit_num=1).t_dg(0)
        actual = mps.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_t_dg(self):
        """test 't_dg' gate (following 'h' gate)
        """
        mps = MPState(qubit_num=1).h(0).t_dg(0)
        actual = mps.amp
        expect = np.array([1.0/SQRT_2, 0.5-0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_rx(self):
        """test 'rx' gate
        """
        mps = MPState(qubit_num=1).rx(0, phase=0.25)
        actual = mps.amp
        expect = np.array([COS_PI_8, -SIN_PI_8*1.0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_rx(self):
        """test 'rx' gate (following 'h' gate)
        """
        mps = MPState(qubit_num=1).h(0).rx(0, phase=0.25)
        actual = mps.amp
        expect = np.array([0.65328148-0.27059805j, 0.65328148-0.27059805j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_ry(self):
        """test 'ry' gate
        """
        mps = MPState(qubit_num=1).ry(0, phase=0.25)
        actual = mps.amp
        expect = np.array([COS_PI_8, SIN_PI_8])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_ry(self):
        """test 'ry' gate (following 'h' gate)
        """
        mps = MPState(qubit_num=1).h(0).ry(0, phase=0.25)
        actual = mps.amp
        expect = np.array([0.38268343+0.j, 0.92387953+0.j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_rz(self):
        """test 'rz' gate
        """
        mps = MPState(qubit_num=1).rz(0, phase=0.25)
        actual = mps.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_rz(self):
        """test 'rz' gate (following 'h' gate)
        """
        mps = MPState(qubit_num=1).h(0).rz(0, phase=0.25)
        actual = mps.amp
        expect = np.array([0.65328148-0.27059805j, 0.65328148+0.27059805j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_p(self):
        """test 'p' gate
        """
        mps = MPState(qubit_num=1).p(0, phase=0.25)
        actual = mps.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_p(self):
        """test 'p' gate (following 'h' gate)
        """
        mps = MPState(qubit_num=1).h(0).p(0, phase=0.25)
        actual = mps.amp
        expect = np.array([0.70710678, 0.5+0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

class TestMPState_1_qubit_in_3_reg(unittest.TestCase):
    """ test 'MPState' : 1-qubit gate in 3-register circuit
    """

    def test_rx_0(self):
        """ test 1-qubit gate in 3-register circuit (reg. #0)
        """
        mps = MPState(qubit_num=3).rx(0, phase=0.25)
        actual = mps.amp
        expect = np.array([0.92387953, 0.0, 0.0, 0.0, -0.38268343j, 0.0, 0.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_rx_1(self):
        """ test 1-qubit gate in 3-register circuit (reg. #1)
        """
        mps = MPState(qubit_num=3).rx(1, phase=0.25)
        actual = mps.amp
        expect = np.array([0.92387953, 0.0, -0.38268343j, 0.0, 0.0, 0.0, 0.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_rx_2(self):
        """ test 1-qubit gate in 3-register circuit (reg. #2)
        """
        mps = MPState(qubit_num=3).rx(2, phase=0.25)
        actual = mps.amp
        expect = np.array([0.92387953, -0.38268343j, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

class TestMPState_2_qubit(unittest.TestCase):
    """ test 'MPState' : 2-qubit gate
    """

    def test_cx(self):
        """test 'cx' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).cx(0,1)
        actual = mps.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cy(self):
        """test 'cy' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).cy(0,1)
        actual = mps.amp
        expect = np.array([(0.5+0j), (0.5+0j), -0.5j, 0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cz(self):
        """test 'cz' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).cz(0,1)
        actual = mps.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (-0.5+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cxr(self):
        """test 'cxr' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).cxr(0,1)
        actual = mps.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cxr_dg(self):
        """test 'cxr_dg' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).cxr_dg(0,1)
        actual = mps.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_ch(self):
        """test 'ch' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).ch(0,1)
        actual = mps.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.7071067811865475+0j), 0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cs(self):
        """test 'cs' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).cs(0,1)
        actual = mps.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), 0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cs_dg(self):
        """test 'cs_dg' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).cs_dg(0,1)
        actual = mps.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), -0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_ct(self):
        """test 'ct' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).ct(0,1)
        actual = mps.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.35355339059327373+0.35355339059327373j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_ct_dg(self):
        """test 'ct_dg' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).ct_dg(0,1)
        actual = mps.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.35355339059327373-0.35355339059327373j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_sw(self):
        """test 'sw' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).sw(0,1)
        actual = mps.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_x_sw(self):
        """test 'sw' gate (following 'x' gate, not 'h' gates)
        """
        mps = MPState(qubit_num=2).x(0).sw(0,1)
        actual = mps.amp
        expect = np.array([0j, (1+0j), 0j, 0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cp(self):
        """test 'cp'gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).cp(0,1, phase=0.25)
        actual = mps.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.3535533905932738+0.35355339059327373j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_crx(self):
        """test 'crx' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).crx(0,1, phase=0.25)
        actual = mps.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.4619397662556434-0.1913417161825449j),
                           (0.4619397662556434-0.1913417161825449j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cry(self):
        """test 'cry' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).cry(0,1, phase=0.25)
        actual = mps.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.2705980500730985+0j),
                           (0.6532814824381882+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_crz(self):
        """test 'crz' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).crz(0,1, phase=0.25)
        actual = mps.amp
        expect = np.array([(0.5+0j), (0.5+0j),(0.4619397662556434-0.1913417161825449j),
                           (0.4619397662556434+0.1913417161825449j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_rxx(self):
        """test 'rxx' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).rxx(0, 1, phase=0.25)
        actual = mps.amp
        expect = np.array([(0.46193977-0.19134172j), (0.46193977-0.19134172j),
                           (0.46193977-0.19134172j), (0.46193977-0.19134172j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)
        
    def test_ryy(self):
        """test 'ryy' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).ryy(0, 1, phase=0.25)
        actual = mps.amp
        expect = np.array([(0.46193977+0.19134172j), (0.46193977-0.19134172j),
                           (0.46193977-0.19134172j), (0.46193977+0.19134172j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_rzz(self):
        """test 'rzz' gate
        """
        mps = MPState(qubit_num=2).h(0).h(1).rzz(0, 1, phase=0.25)
        actual = mps.amp
        expect = np.array([(0.46193977-0.19134172j), (0.46193977+0.19134172j),
                           (0.46193977+0.19134172j), (0.46193977-0.19134172j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)
        
class TestMPState_2_qubit_in_3_reg(unittest.TestCase):
    """ test 'MPState' : 2-qubit gate in 3-register circuit
    """

    def test_crx_0_1(self):
        """ test 2-qubit gate in 3-register circuit (reg. #0,#1)
        """
        mps = MPState(qubit_num=3).h(0).h(1).h(2).crx(0,1, phase=0.25)
        actual = mps.amp
        expect = np.array([(0.35355339059327373+0j), (0.35355339059327373+0j),
                           (0.35355339059327373+0j), (0.35355339059327373+0j),
                           (0.3266407412190941-0.13529902503654925j),
                           (0.3266407412190941-0.13529902503654925j),
                           (0.3266407412190941-0.13529902503654925j),
                           (0.3266407412190941-0.13529902503654925j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_crx_1_2(self):
        """ test 2-qubit gate in 3-register circuit (reg. #1,#2)
        """
        mps = MPState(qubit_num=3).h(0).h(1).h(2).crx(1,2, phase=0.25)
        actual = mps.amp
        expect = np.array([(0.35355339059327373+0j), (0.35355339059327373+0j),
                           (0.3266407412190941-0.13529902503654925j),
                           (0.3266407412190941-0.13529902503654925j),
                           (0.35355339059327373+0j), (0.35355339059327373+0j),
                           (0.3266407412190941-0.13529902503654925j),
                           (0.3266407412190941-0.13529902503654925j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_crx_2_0(self):
        """ test 2-qubit gate in 3-register circuit (reg. #2,#0)
        """
        mps = MPState(qubit_num=3).h(0).h(1).h(2).crx(2,0, phase=0.25)
        actual = mps.amp
        expect = np.array([(0.35355339059327373+0j),
                           (0.3266407412190941-0.13529902503654925j),
                           (0.35355339059327373+0j),
                           (0.3266407412190941-0.13529902503654925j),
                           (0.35355339059327373+0j),
                           (0.3266407412190941-0.13529902503654925j),
                           (0.35355339059327373+0j),
                           (0.3266407412190941-0.13529902503654925j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

class TestMPState_3_qubit(unittest.TestCase):
    """ test 'MPState' : 3-qubit gate
    """

    def test_ccx(self):
        """test 'ccx' gate
        """
        mps = MPState(qubit_num=3).x(0).x(1).ccx(0,1,2)
        actual = mps.amp
        expect = np.array([0j, 0j, 0j, 0j, 0j, 0j, 0j, (1+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_x_x_csw(self):
        """test 'csw' gate
        """
        mps = MPState(qubit_num=3).x(0).x(1).csw(0,1,2)
        actual = mps.amp
        expect = np.array([0j, 0j, 0j, 0j, 0j, (1+0j), 0j, 0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)


class TestMPState_clone(unittest.TestCase):
    """ test 'MPState' : 'clone'
    """

    def test_clone(self):
        """test 'clone'
        """
        mps_src = MPState(qubit_num=3).h(0).h(1).h(2)
        mps_dst = mps_src.clone()
        actual_src = mps_src.amp
        actual_dst = mps_dst.amp
        ans = equal_vectors(actual_src, actual_dst)
        self.assertEqual(ans,True)

class TestMPState_inpro(unittest.TestCase):
    """ test 'MPState' : 'inpro' and 'fidelity'
    """

    def test_inpro(self):
        """test 'inpro'
        """
        mps_0 = MPState(qubit_num=3).h(0).h(1).h(2)
        mps_1 = MPState(qubit_num=3).h(0).h(1).h(2)
        inpro = mps_0.inpro(mps_1)
        ans = (round(inpro.real, 4) == 1.0 and inpro.imag == 0.0)
        self.assertEqual(ans, True)

    def test_inpro_partial(self):
        """test 'inpro' (for partial system)
        """
        mps_0 = MPState(qubit_num=3).h(0).h(1).h(2)
        mps_1 = MPState(qubit_num=3).h(0).h(1).h(2)
        inpro = mps_0.inpro(mps_1, qid=[0,1])
        ans = (round(inpro.real, 4) == 1.0 and inpro.imag == 0.0)
        self.assertEqual(ans, True)

    def test_fidelity(self):
        """test 'fidelity'
        """
        mps_0 = MPState(qubit_num=3).h(0).h(1).h(2)
        mps_1 = MPState(qubit_num=3).h(0).h(1).h(2)
        fid = mps_0.fidelity(mps_1)
        ans = (round(fid, 4) == 1.0)
        self.assertEqual(ans, True)

    def test_fidelity_partial(self):
        """test 'fidelity' (for partial system)
        """
        mps_0 = MPState(qubit_num=3).h(0).h(1).h(2)
        mps_1 = MPState(qubit_num=3).h(0).h(1).h(2)
        fid = mps_0.fidelity(mps_1, qid=[0,1])
        ans = (round(fid, 4) == 1.0)
        self.assertEqual(ans, True)

# class TestMPState_evolve(unittest.TestCase):
#     """ test 'MPState' : 'evolve'
#     """
# 
#     def test_evolve(self):
#         """test 'evolve'
#         """
#         hm = Observable("x_0")
#         mps = MPState(qubit_num=1)
#         mps.evolve(observable=hm, time=0.2, iteration=100)
#         actual = mps.amp
#         expect = np.array([(0.8090169943749473+0j), 0.5877852522924732j])
#         ans = equal_vectors(actual, expect)
#         self.assertEqual(ans,True)
# 
# class TestMPState_expect(unittest.TestCase):
#     """ test 'MPState' : 'expect'
#     """
# 
#     def test_evolve_1_qubit(self):
#         """test 'evolve' (1-qubit)
#         """
#         ob = Observable("y_0")
#         hm = Observable("x_0")
#         mps = MPState(qubit_num=1)
#         mps.evolve(observable=hm, time=0.2, iteration=100)
#         actual = mps.expect(observable=ob)
#         expect = 0.9510565162951199
#         ans = equal_values(actual, expect)
#         self.assertEqual(ans,True)
# 
#     def test_evolve_2_qubit(self):
#         """test 'evolve' (2-qubit)
#         """
#         qs = QState(qubit_num=2).x(0)
#         hm = Observable("z_0*z_1+x_0+x_1")
#         ob = Observable("2.0+z_0+z_1")
#         mps.evolve(observable=hm,time=0.1,iteration=10)
#         actual = mps.expect(observable=ob)
#         expect = 1.9999999999999898+0j
#         ans = equal_values(actual, expect)
#         self.assertEqual(ans,True)

class TestMPState_measure(unittest.TestCase):
    """ test 'MPState' : various kind of measurements
    """

    def test_measure(self):
        """test 'measure'
        """
        mps = MPState(qubit_num=4).x(1).x(2)
        mval = mps.measure(qid=[0,1,2,3])
        self.assertEqual(mval, '0110')

    def test_m(self):
        """test 'm' (for bell state)
        """
        mps = MPState(qubit_num=2).h(0).cx(0,1)
        md = mps.m(shots=10)
        self.assertEqual(md.frequency['00']+md.frequency['11'], 10)
        self.assertEqual(md.frequency['01'], 0)
        self.assertEqual(md.frequency['10'], 0)

class TestMPState_operate(unittest.TestCase):
    """ test 'MPState' : 'operate'
    """

    def test_operate_x(self):
        """test 'operate' (x)
        """
        mps_expect = MPState(qubit_num=1)
        mps_actual = MPState(qubit_num=1)
        pp = PauliProduct(pauli_str="X")
        mps_expect.x(0)
        mps_actual.operate(pp=pp)
        ans = equal_mpstates(mps_expect, mps_actual)
        self.assertEqual(ans,True)
        
    def test_operate_h_x(self):
        """test 'operate' (x followed by h)
        """
        mps_expect = MPState(qubit_num=1).h(0)
        mps_actual = MPState(qubit_num=1).h(0)
        pp = PauliProduct(pauli_str="X")
        mps_expect.x(0)
        mps_actual.operate(pp=pp)
        ans = equal_mpstates(mps_expect, mps_actual)
        self.assertEqual(ans,True)
        
    def test_operate_h_y(self):
        """test 'operate' (y followed by h)
        """
        mps_expect = MPState(qubit_num=1).h(0)
        mps_actual = MPState(qubit_num=1).h(0)
        pp = PauliProduct(pauli_str="Y")
        mps_expect.y(0)
        mps_actual.operate(pp=pp)
        ans = equal_mpstates(mps_expect, mps_actual)
        self.assertEqual(ans,True)
        
    def test_operate_h_z(self):
        """test 'operate' (z followed by h)
        """
        mps_expect = MPState(qubit_num=1).h(0)
        mps_actual = MPState(qubit_num=1).h(0)
        pp = PauliProduct(pauli_str="Z")
        mps_expect.z(0)
        mps_actual.operate(pp=pp)
        ans = equal_mpstates(mps_expect, mps_actual)
        self.assertEqual(ans,True)
        
    def test_operate_xyz(self):
        """test 'operate' (xyz)
        """
        mps_expect = MPState(qubit_num=3)
        mps_actual = MPState(qubit_num=3)
        pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
        mps_expect.x(2).y(0).z(1)
        mps_actual.operate(pp=pp)
        ans = equal_mpstates(mps_expect, mps_actual)
        self.assertEqual(ans,True)
        
    def test_operate_controlled_xyz(self):
        """test 'operate' (controlled_xyz)
        """
        mps_expect = MPState(qubit_num=4)
        mps_actual = MPState(qubit_num=4)
        pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
        mps_expect.cx(3,2).cy(3,0).cz(3,1)
        mps_actual.operate(pp=pp, ctrl=3)
        ans = equal_mpstates(mps_expect, mps_actual)
        self.assertEqual(ans,True)

class TestMPState_inheritance(unittest.TestCase):
    """ test 'MPState' : inheritance
    """

    def test_inheritance_1(self):
        """test 'inheritance_1'
        """
        mps_expect = MPState(qubit_num=2).h(0).cx(0,1).x(0)
        mps_actual = MyMPState(qubit_num=2).bell(0,1).x(0)
        fid = mps_expect.fidelity(mps_actual)
        self.assertEqual(abs(fid-1.0) < EPS, True)

    def test_inheritance_2(self):
        """test 'inheritance_2'
        """
        mps_expect = MPState(qubit_num=2).h(0).cx(0,1).x(0)
        mps_actual = MyMPState(qubit_num=2).clone()
        mps_actual = mps_actual.bell(0,1).x(0)
        fid = mps_expect.fidelity(mps_actual)
        self.assertEqual(abs(fid-1.0) < EPS, True)

    def test_inheritance_4(self):
        """test 'inheritance_4'
        """
        mps = MyMPState(qubit_num=1, name='hoge')
        self.assertEqual(mps.get_name(), 'hoge')

class TestMPState_random(unittest.TestCase):
    """ test 'MPState' : random
    """
    def test_random(self):
        """test 'random'
        """
        qubit_num = 20
        operation_num = 3
        rnd_list = [random.random() for _ in range(operation_num * 3)]

        mps = MPState(qubit_num=qubit_num)
        for j in range(operation_num):
            for i in range(qubit_num):
                mps.rx(i, phase=rnd_list[3*j])
                mps.ry(i, phase=rnd_list[3*j+1])
                mps.rz(i, phase=rnd_list[3*j+2])
            for k in range(1, qubit_num):
                mps.cx(k-1,k)
        mps_vec = mps.get_amp()

        qs = QState(qubit_num=qubit_num)
        for j in range(operation_num):
            for i in range(qubit_num):
                qs.rx(i, phase=rnd_list[3*j])
                qs.ry(i, phase=rnd_list[3*j+1])
                qs.rz(i, phase=rnd_list[3*j+2])
            for k in range(1, qubit_num):
                qs.cx(k-1,k)
        qs_vec = qs.get_amp()

        ans = equal_vectors(mps_vec, qs_vec)
        self.assertEqual(ans, True)
        
if __name__ == '__main__':
    unittest.main()
