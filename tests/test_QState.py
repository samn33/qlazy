# -*- coding: utf-8 -*-
import unittest
import math
import numpy as np
from qlazy import QState, Observable, PauliProduct

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

class MyQState(QState):

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

class TestQState_init(unittest.TestCase):
    """ test 'QState' : '__new__'
    """

    def test_init(self):
        """test '__new__' (qubit_num)
        """
        qs = QState(qubit_num=3)
        actual = qs.amp
        expect = np.array([1j, 0j, 0j, 0j, 0j, 0j, 0j, 0j])
        ans = equal_vectors(actual, expect)
        # qs.free()
        self.assertEqual(ans,True)

    def test_init_with_vector(self):
        """test '__new__' (vector)
        """
        vec = np.array([2j, 0j, 0j, 0j, 0j, 0j, 0j, 0j])
        qs = QState(vector=vec)
        actual = qs.amp
        expect = np.array([1j, 0j, 0j, 0j, 0j, 0j, 0j, 0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

class TestQState_del_all(unittest.TestCase):
    """ test 'QState' : 'del_all'
    """

    def test_del_all(self):
        """test 'free_all'
        """
        qs_0 = QState(1)
        qs_1 = QState(1).x(0)
        qs_2 = QState(1).h(0)
        QState.del_all(qs_0,qs_1,qs_2)

        qs_0 = QState(1)
        qs_1 = QState(1).x(0)
        qs_2 = QState(1).h(0)
        qs_A = [qs_1,qs_2]
        QState.del_all(qs_0,qs_A)

        qs_0 = QState(1)
        qs_1 = QState(1).x(0)
        qs_2 = QState(1).h(0)
        qs_B = [qs_0,[qs_1,qs_2]]
        QState.del_all(qs_B)
        
class TestQState_reset(unittest.TestCase):
    """ test 'QState' : 'reset'
    """

    def test_reset(self):
        """test 'reset'
        """
        qs = QState(qubit_num=3).h(0).h(1).h(2)
        qs.reset()
        actual = qs.amp
        expect = np.array([1j, 0j, 0j, 0j, 0j, 0j, 0j, 0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

class TestQState_1_qubit(unittest.TestCase):
    """ test 'QState' : 1-qubit gate
    """

    def test_x(self):
        """test 'x' gate
        """
        qs = QState(qubit_num=1).x(0)
        actual = qs.amp
        expect = np.array([0.0, 1.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_x(self):
        """test 'x' gate (following 'h' gate)
        """
        qs = QState(qubit_num=1).h(0).x(0)
        actual = qs.amp
        expect = np.array([1.0/SQRT_2, 1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_y(self):
        """test 'y' gate
        """
        qs = QState(qubit_num=1).y(0)
        actual = qs.amp
        expect = np.array([0.0, 1.0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_y(self):
        """test 'y' gate (following 'h' gate)
        """
        qs = QState(qubit_num=1).h(0).y(0)
        actual = qs.amp
        expect = np.array([-1.0j/SQRT_2, 1.0j/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_z(self):
        """test 'z' gate
        """
        qs = QState(qubit_num=1).z(0)
        actual = qs.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_z(self):
        """test 'z' gate (following 'h' gate)
        """
        qs = QState(qubit_num=1).h(0).z(0)
        actual = qs.amp
        expect = np.array([1.0/SQRT_2, -1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_xr(self):
        """test 'xr' gate
        """
        qs = QState(qubit_num=1).xr(0)
        actual = qs.amp
        expect = np.array([0.5+0.5j, 0.5-0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_xr(self):
        """test 'xr' gate (following 'h' gate)
        """
        qs = QState(qubit_num=1).h(0).xr(0)
        actual = qs.amp
        expect = np.array([1.0/SQRT_2, 1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_xr_dg(self):
        """test 'xr_dg' gate
        """
        qs = QState(qubit_num=1).xr_dg(0)
        actual = qs.amp
        expect = np.array([0.5-0.5j, 0.5+0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_xr_dg(self):
        """test 'xr_dg' gate (following 'h' gate)
        """
        qs = QState(qubit_num=1).h(0).xr_dg(0)
        actual = qs.amp
        expect = np.array([1.0/SQRT_2, 1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h(self):
        """test 'h' gate
        """
        qs = QState(qubit_num=1).h(0)
        actual = qs.amp
        expect = np.array([1.0/SQRT_2, 1.0/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_h(self):
        """test 'h' gate (following 'h')
        """
        qs = QState(qubit_num=1).h(0).h(0)
        actual = qs.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_s(self):
        """test 's' gate
        """
        qs = QState(qubit_num=1).s(0)
        actual = qs.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_s(self):
        """test 's' gate (following 'h' gate)
        """
        qs = QState(qubit_num=1).h(0).s(0)
        actual = qs.amp
        expect = np.array([1.0/SQRT_2, 1.0j/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_s_dg(self):
        """test 's_dg' gate
        """
        qs = QState(qubit_num=1).s_dg(0)
        actual = qs.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_s_dg(self):
        """test 's_dg' gate (following 'h' gate)
        """
        qs = QState(qubit_num=1).h(0).s_dg(0)
        actual = qs.amp
        expect = np.array([1.0/SQRT_2, -1.0j/SQRT_2])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_t(self):
        """test 't' gate
        """
        qs = QState(qubit_num=1).t(0)
        actual = qs.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_t(self):
        """test 't' gate (following 'h' gate)
        """
        qs = QState(qubit_num=1).h(0).t(0)
        actual = qs.amp
        expect = np.array([1.0/SQRT_2, 0.5+0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_t_dg(self):
        """test 't_dg' gate
        """
        qs = QState(qubit_num=1).t_dg(0)
        actual = qs.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_t_dg(self):
        """test 't_dg' gate (following 'h' gate)
        """
        qs = QState(qubit_num=1).h(0).t_dg(0)
        actual = qs.amp
        expect = np.array([1.0/SQRT_2, 0.5-0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_rx(self):
        """test 'rx' gate
        """
        qs = QState(qubit_num=1).rx(0, phase=0.25)
        actual = qs.amp
        expect = np.array([COS_PI_8, -SIN_PI_8*1.0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_rx(self):
        """test 'rx' gate (following 'h' gate)
        """
        qs = QState(qubit_num=1).h(0).rx(0, phase=0.25)
        actual = qs.amp
        expect = np.array([0.65328148-0.27059805j, 0.65328148-0.27059805j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_ry(self):
        """test 'ry' gate
        """
        qs = QState(qubit_num=1).ry(0, phase=0.25)
        actual = qs.amp
        expect = np.array([COS_PI_8, SIN_PI_8])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_ry(self):
        """test 'ry' gate (following 'h' gate)
        """
        qs = QState(qubit_num=1).h(0).ry(0, phase=0.25)
        actual = qs.amp
        expect = np.array([0.38268343+0.j, 0.92387953+0.j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_rz(self):
        """test 'rz' gate
        """
        qs = QState(qubit_num=1).rz(0, phase=0.25)
        actual = qs.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_rz(self):
        """test 'rz' gate (following 'h' gate)
        """
        qs = QState(qubit_num=1).h(0).rz(0, phase=0.25)
        actual = qs.amp
        expect = np.array([0.65328148-0.27059805j, 0.65328148+0.27059805j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_p(self):
        """test 'p' gate
        """
        qs = QState(qubit_num=1).p(0, phase=0.25)
        actual = qs.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_p(self):
        """test 'p' gate (following 'h' gate)
        """
        qs = QState(qubit_num=1).h(0).p(0, phase=0.25)
        actual = qs.amp
        expect = np.array([0.70710678, 0.5+0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_u1(self):
        """test 'u1' gate
        """
        qs = QState(qubit_num=1).u1(0, alpha=0.1)
        actual = qs.amp
        expect = np.array([1.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_u1(self):
        """test 'u1' gate (following 'h' gate)
        """
        qs = QState(qubit_num=1).h(0).u1(0, alpha=0.1)
        actual = qs.amp
        expect = np.array([0.70710678+0.j, 0.67249851+0.21850801j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_u2(self):
        """test 'u2' gate
        """
        qs = QState(qubit_num=1).u2(0, alpha=0.1, beta=0.2)
        actual = qs.amp
        expect = np.array([0.70710678+0.j, 0.5720614 +0.41562694j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_u2(self):
        """test 'u2' gate (following 'h' gate)
        """
        qs = QState(qubit_num=1).h(0).u2(0, alpha=0.1, beta=0.2)
        actual = qs.amp
        expect = np.array([0.02447174-0.1545085j,0.69840112+0.69840112j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_u3(self):
        """test 'u3' gate
        """
        qs = QState(qubit_num=1).u3(0, alpha=0.1, beta=0.2, gamma=0.3)
        actual = qs.amp
        expect = np.array([0.89100652+0.j, 0.36728603+0.26684892j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_h_u3(self):
        """test 'u3' gate (following 'h' gate)
        """
        qs = QState(qubit_num=1).h(0).u3(0, alpha=0.1, beta=0.2, gamma=0.3)
        actual = qs.amp
        expect = np.array([0.32472882-0.09920056j, 0.63003676+0.69840112j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

class TestQState_1_qubit_in_3_reg(unittest.TestCase):
    """ test 'QState' : 1-qubit gate in 3-register circuit
    """

    def test_rx_0(self):
        """ test 1-qubit gate in 3-register circuit (reg. #0)
        """
        qs = QState(qubit_num=3).rx(0, phase=0.25)
        actual = qs.amp
        expect = np.array([0.92387953, 0.0, 0.0, 0.0, -0.38268343j, 0.0, 0.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_rx_1(self):
        """ test 1-qubit gate in 3-register circuit (reg. #1)
        """
        qs = QState(qubit_num=3).rx(1, phase=0.25)
        actual = qs.amp
        expect = np.array([0.92387953, 0.0, -0.38268343j, 0.0, 0.0, 0.0, 0.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_rx_2(self):
        """ test 1-qubit gate in 3-register circuit (reg. #2)
        """
        qs = QState(qubit_num=3).rx(2, phase=0.25)
        actual = qs.amp
        expect = np.array([0.92387953, -0.38268343j, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

class TestQState_2_qubit(unittest.TestCase):
    """ test 'QState' : 2-qubit gate
    """

    def test_cx(self):
        """test 'cx' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).cx(0,1)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cy(self):
        """test 'cy' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).cy(0,1)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), -0.5j, 0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cz(self):
        """test 'cz' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).cz(0,1)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (-0.5+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cxr(self):
        """test 'cxr' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).cxr(0,1)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cxr_dg(self):
        """test 'cxr_dg' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).cxr_dg(0,1)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_ch(self):
        """test 'ch' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).ch(0,1)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.7071067811865475+0j), 0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cs(self):
        """test 'cs' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).cs(0,1)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), 0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cs_dg(self):
        """test 'cs_dg' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).cs_dg(0,1)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), -0.5j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_ct(self):
        """test 'ct' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).ct(0,1)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.35355339059327373+0.35355339059327373j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_ct_dg(self):
        """test 'ct_dg' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).ct_dg(0,1)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.35355339059327373-0.35355339059327373j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_sw(self):
        """test 'sw' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).sw(0,1)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j), (0.5+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_x_sw(self):
        """test 'sw' gate (following 'x' gate, not 'h' gates)
        """
        qs = QState(qubit_num=2).x(0).sw(0,1)
        actual = qs.amp
        expect = np.array([0j, (1+0j), 0j, 0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cp(self):
        """test 'cp'gate
        """
        qs = QState(qubit_num=2).h(0).h(1).cp(0,1, phase=0.25)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.3535533905932738+0.35355339059327373j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_crx(self):
        """test 'crx' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).crx(0,1, phase=0.25)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.4619397662556434-0.1913417161825449j),
                           (0.4619397662556434-0.1913417161825449j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cry(self):
        """test 'cry' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).cry(0,1, phase=0.25)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.2705980500730985+0j),
                           (0.6532814824381882+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_crz(self):
        """test 'crz' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).crz(0,1, phase=0.25)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j),(0.4619397662556434-0.1913417161825449j),
                           (0.4619397662556434+0.1913417161825449j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cu1(self):
        """test 'cu1' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).cu1(0,1, alpha=0.1)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.5+0j),
                           (0.47552825814757677+0.1545084971874737j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cu2(self):
        """test 'cu2' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).cu2(0,1, alpha=0.1, beta=0.2)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.0173041346112951-0.10925400611220525j),
                           (0.49384417029756883+0.49384417029756883j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_cu3(self):
        """test 'cu3' gate
        """
        qs = QState(qubit_num=2).h(0).h(1).cu3(0,1, alpha=0.1, beta=0.2, gamma=0.3)
        actual = qs.amp
        expect = np.array([(0.5+0j), (0.5+0j), (0.22961795053748937-0.07014538985214754j),
                           (0.44550326209418395+0.4938441702975689j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

class TestQState_2_qubit_in_3_reg(unittest.TestCase):
    """ test 'QState' : 2-qubit gate in 3-register circuit
    """

    def test_crx_0_1(self):
        """ test 2-qubit gate in 3-register circuit (reg. #0,#1)
        """
        qs = QState(qubit_num=3).h(0).h(1).h(2).crx(0,1, phase=0.25)
        actual = qs.amp
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
        qs = QState(qubit_num=3).h(0).h(1).h(2).crx(1,2, phase=0.25)
        actual = qs.amp
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
        qs = QState(qubit_num=3).h(0).h(1).h(2).crx(2,0, phase=0.25)
        actual = qs.amp
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

class TestQState_3_qubit(unittest.TestCase):
    """ test 'QState' : 3-qubit gate
    """

    def test_ccx(self):
        """test 'ccx' gate
        """
        qs = QState(qubit_num=3).x(0).x(1).ccx(0,1,2)
        actual = qs.amp
        expect = np.array([0j, 0j, 0j, 0j, 0j, 0j, 0j, (1+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_x_x_csw(self):
        """test 'csw' gate
        """
        qs = QState(qubit_num=3).x(0).x(1).csw(0,1,2)
        actual = qs.amp
        expect = np.array([0j, 0j, 0j, 0j, 0j, (1+0j), 0j, 0j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

class TestQState_n_qubit(unittest.TestCase):
    """ test 'QState' : n-qubit gate
    """

    def test_mcx_3(self):
        """test 'mcx' gate (for 3-qubit)
        """
        qs = QState(qubit_num=3).x(0).x(1).mcx([0,1,2])
        actual = qs.amp
        expect = np.array([0j, 0j, 0j, 0j, 0j, 0j, 0j, (1+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_mcx_4(self):
        """test 'mcx' gate (for 4-qubit)
        """
        qs = QState(qubit_num=4).x(0).x(1).x(2).mcx([0,1,2,3])
        actual = qs.amp
        expect = np.array([0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j,
                           0j, 0j, 0j, 0j, 0j, 0j, 0j, (1+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_mcx_5(self):
        """test 'mcx' gate (for 5-qubit)
        """
        qs = QState(qubit_num=5).x(0).x(1).x(2).x(3).mcx([0,1,2,3,4])
        actual = qs.amp
        expect = np.array([0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j,
                           0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j,
                           0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j,
                           0j, 0j, 0j, 0j, 0j, 0j, 0j, (1+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

class TestQState_partial(unittest.TestCase):
    """ test 'QState' : 'partial'
    """

    def test_partial_2_from_3(self):
        """test 'partial' (2-qubit state from 3-qubit)
        """
        qs_ini = QState(qubit_num=3).h(0).h(1).cx(1,2)
        qs = qs_ini.partial([1,2])
        actual = qs.amp
        expect = np.array([(0.7071067811865476+0j), 0j, 0j, (0.7071067811865476+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

    def test_partial_3_permutation(self):
        """test 'partial' (3-qubit permutation)
        """
        qs_ini = QState(qubit_num=3).h(0).h(1).cx(1,2)
        qs = qs_ini.partial([2,0,1])
        actual = qs.amp
        expect = np.array([(0.5+0j), 0j, (0.5+0j), 0j, 0j, (0.5+0j), 0j, (0.5+0j)])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

class TestQState_clone(unittest.TestCase):
    """ test 'QState' : 'clone'
    """

    def test_clone(self):
        """test 'clone'
        """
        qs_src = QState(qubit_num=3).h(0).h(1).h(2)
        qs_dst = qs_src.clone()
        actual_src = qs_src.amp
        actual_dst = qs_dst.amp
        ans = equal_vectors(actual_src, actual_dst)
        self.assertEqual(ans,True)

class TestQState_bloch(unittest.TestCase):
    """ test 'QState' : 'bloch'
    """

    def test_bloch(self):
        """test 'bloch'
        """
        qs = QState(qubit_num=3).ry(0, phase=0.25).rz(0, phase=0.25)
        theta, phi = qs.bloch()
        ans = (round(theta,4) == 0.25 and round(phi,4) == 0.25)
        self.assertEqual(ans, True)

class TestQState_inpro(unittest.TestCase):
    """ test 'QState' : 'inpro' and 'fidelity'
    """

    def test_inpro(self):
        """test 'inpro'
        """
        qs_0 = QState(qubit_num=3).h(0).h(1).h(2)
        qs_1 = QState(qubit_num=3).h(0).h(1).h(2)
        inpro = qs_0.inpro(qs_1)
        ans = (round(inpro.real, 4) == 1.0 and inpro.imag == 0.0)
        self.assertEqual(ans, True)

    def test_inpro_partial(self):
        """test 'inpro' (for partial system)
        """
        qs_0 = QState(qubit_num=3).h(0).h(1).h(2)
        qs_1 = QState(qubit_num=3).h(0).h(1).h(2)
        inpro = qs_0.inpro(qs_1, qid=[0,1])
        ans = (round(inpro.real, 4) == 1.0 and inpro.imag == 0.0)
        self.assertEqual(ans, True)

    def test_fidelity(self):
        """test 'fidelity'
        """
        qs_0 = QState(qubit_num=3).h(0).h(1).h(2)
        qs_1 = QState(qubit_num=3).h(0).h(1).h(2)
        fid = qs_0.fidelity(qs_1)
        ans = (round(fid, 4) == 1.0)
        self.assertEqual(ans, True)

    def test_fidelity_partial(self):
        """test 'fidelity' (for partial system)
        """
        qs_0 = QState(qubit_num=3).h(0).h(1).h(2)
        qs_1 = QState(qubit_num=3).h(0).h(1).h(2)
        fid = qs_0.fidelity(qs_1, qid=[0,1])
        ans = (round(fid, 4) == 1.0)
        self.assertEqual(ans, True)

class TestQState_tenspro(unittest.TestCase):
    """ test 'QState' : 'tenspro'
    """

    def test_tenspro(self):
        """test 'tenspro'
        """
        qs_A = QState(qubit_num=1).h(0)
        qs_B = QState(qubit_num=2).h(0).cx(0,1)
        actual = qs_A.tenspro(qs_B)
        expect = QState(qubit_num=3).h(0).h(1).cx(1,2)
        ans = equal_qstates(actual, expect)
        self.assertEqual(ans,True)

class TestQState_composite(unittest.TestCase):
    """ test 'QState' : 'composite'
    """

    def test_tenspro(self):
        """test 'composite'
        """
        qs = QState(qubit_num=1).h(0)
        actual = qs.composite(num=3)
        expect = QState(qubit_num=3).h(0).h(1).h(2)
        ans = equal_qstates(actual, expect)
        self.assertEqual(ans,True)

class TestQState_join(unittest.TestCase):
    """ test 'QState' : 'join'
    """

    def test_join(self):
        """test 'join'
        """
        expect = QState(qubit_num=6).h(0).cx(0,1)
        expect.h(2).rz(2, phase=0.2)
        expect.rx(3, phase=0.3)
        expect.h(4).cx(4,5)

        qs_tmp = QState(qubit_num=2).h(0).cx(0,1)
        qs_list = [QState(qubit_num=1).h(0).rz(0, phase=0.2),
                   QState(qubit_num=1).rx(0, phase=0.3),
                   QState(qubit_num=2).h(0).cx(0,1)]
        actual = qs_tmp.join(qs_list)
        
        ans = equal_qstates(actual, expect)
        self.assertEqual(ans,True)
        
class TestQState_evolve(unittest.TestCase):
    """ test 'QState' : 'evolve'
    """

    def test_evolve(self):
        """test 'evolve'
        """
        hm = Observable("x_0")
        qs = QState(qubit_num=1)
        qs.evolve(observable=hm, time=0.2, iter=100)
        actual = qs.amp
        expect = np.array([(0.8090169943749473+0j), 0.5877852522924732j])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans,True)

class TestQState_expect(unittest.TestCase):
    """ test 'QState' : 'expect'
    """

    def test_evolve_1_qubit(self):
        """test 'evolve' (1-qubit)
        """
        ob = Observable("y_0")
        hm = Observable("x_0")
        qs = QState(qubit_num=1)
        qs.evolve(observable=hm, time=0.2, iter=100)
        actual = qs.expect(observable=ob)
        expect = 0.9510565162951199
        ans = equal_values(actual, expect)
        self.assertEqual(ans,True)

    def test_evolve_2_qubit(self):
        """test 'evolve' (2-qubit)
        """
        qs = QState(qubit_num=2).x(0)
        hm = Observable("z_0*z_1+x_0+x_1")
        ob = Observable("2.0+z_0+z_1")
        qs.evolve(observable=hm,time=0.1,iter=10)
        actual = qs.expect(observable=ob)
        expect = 1.9999999999999898+0j
        ans = equal_values(actual, expect)
        self.assertEqual(ans,True)

class TestQState_apply(unittest.TestCase):
    """ test 'QState' : 'apply'
    """

    def test_apply(self):
        """test 'apply'
        """
        mat = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
        qs_0 = QState(qubit_num=2).h(0).apply(matrix=mat)
        qs_1 = QState(qubit_num=2).h(0).cx(0,1)
        ans = equal_qstates(qs_0, qs_1)
        self.assertEqual(ans,True)

class TestQState_measure(unittest.TestCase):
    """ test 'QState' : various kind of measurements
    """

    def test_m(self):
        """test 'm' (for bell state)
        """
        qs = QState(qubit_num=2).h(0).cx(0,1)
        md = qs.m(shots=10)
        self.assertEqual(md.frq[0]+md.frq[3], 10)
        self.assertEqual(md.frq[1], 0)
        self.assertEqual(md.frq[2], 0)

    def test_mx(self):
        """test 'mx' (for bell state)
        """
        qs = QState(qubit_num=2).h(0).cx(0,1)
        md = qs.mx(shots=10)
        self.assertEqual(md.frq[0]+md.frq[3], 10)
        self.assertEqual(md.frq[1], 0)
        self.assertEqual(md.frq[2], 0)

    def test_my(self):
        """test 'my' (for bell state)
        """
        qs = QState(qubit_num=2).h(0).cx(0,1)
        md = qs.my(shots=10)
        self.assertEqual(md.frq[1]+md.frq[2], 10)
        self.assertEqual(md.frq[0], 0)
        self.assertEqual(md.frq[3], 0)

    def test_mz(self):
        """test 'mz' (for bell state)
        """
        qs = QState(qubit_num=2).h(0).cx(0,1)
        md = qs.mz(shots=10)
        self.assertEqual(md.frq[0]+md.frq[3], 10)
        self.assertEqual(md.frq[1], 0)
        self.assertEqual(md.frq[2], 0)

    def test_mb(self):
        """test 'mb' (for bell state)
        """
        qs = QState(qubit_num=2).h(0).cx(0,1)
        md = qs.mb(shots=10)
        self.assertEqual(md.frq[0], 10)
        self.assertEqual(md.frq[1], 0)
        self.assertEqual(md.frq[2], 0)
        self.assertEqual(md.frq[3], 0)

    def test_m(self):
        """test 'm' (some angle and phase)
        """
        qs = QState(qubit_num=2).ry(1, phase=0.2).rz(1, phase=0.2)
        md = qs.m([1], shots=10, angle=0.2, phase=0.2)
        self.assertEqual(md.frq[0], 10)
        self.assertEqual(md.frq[1], 0)

    def test_m_value(self):
        """test 'm_value'
        """
        qs = QState(qubit_num=2).h(0).cx(0,1)
        qs.m(shots=10)
        qs.m([0], shots=10, tag='foo')
        qs.m([1], shots=10, tag='bar', angle=0.25, phase=0.25)
        actual = (qs.m_value() == 0 or qs.m_value() == 3)
        self.assertEqual(actual, True)
        actual = (qs.m_value(binary=True) == '00' or qs.m_value(binary=True) == '11')
        self.assertEqual(actual, True)
        actual = (qs.m_value(tag='foo') == 0 or qs.m_value(tag='foo') == 1)
        self.assertEqual(actual, True)
        actual = (qs.m_value(tag='bar', angle=0.25, phase=0.25) == 0
                  or qs.m_value(tag='bar', angle=0.25, phase=0.25) == 1)
        self.assertEqual(actual, True)
        
    def test_m_bit(self):
        """test 'm_bit'
        """
        qs = QState(qubit_num=4)
        [qs.h(i) for i in range(4)]
        qs.m(shots=10, angle=0.25, phase=0.25)
        qs.m(shots=10, tag='foo')
        actual = (qs.m_bit(1, angle=0.25, phase=0.25) == 0
                  or qs.m_bit(1, angle=0.25, phase=0.25) == 1)
        self.assertEqual(actual, True)
        actual = (qs.m_bit(3, tag='foo') == 0 or qs.m_bit(3, tag='foo') == 1)
        self.assertEqual(actual, True)
        actual = ((qs.m_bit(3, tag='foo', boolean=True) == False
                   or qs.m_bit(3, tag='foo', boolean=True) == True))
        self.assertEqual(actual, True)
        
    def test_m_freq(self):
        """test 'm_freq'
        """
        qs = QState(2)
        qs.h(0).cx(0,1).m(shots=100)
        freq = qs.m_freq()
        actual = sum(freq.values())
        self.assertEqual(actual, 100)

class TestQState_schmidt_decocmp(unittest.TestCase):
    """ test 'QState' : 'schmidt_decomp'
    """

    def test_schmidt_decomp(self):
        """test 'schmidt_decomp'
        """
        qs_ori = QState(vector=VECTOR_16)
        coef, qs_0, qs_1 = qs_ori.schmidt_decomp(qid_0=[0,1], qid_1=[2,3])
        rank = len(coef)
        qs_list = [qs_0[i].tenspro(qs_1[i]) for i in range(rank)]
        vec_comp = np.zeros(qs_ori.state_num, dtype=np.complex)
        for i in range(rank):
            vec_comp = vec_comp + coef[i] * qs_list[i].get_amp()
        qs_comp = QState(vector=vec_comp)
        ans = equal_qstates(qs_ori, qs_comp)
        self.assertEqual(ans,True)

    def test_schmidt_coef(self):
        """test 'schmidt_coef'
        """
        qs_ori = QState(vector=VECTOR_16)
        actual = qs_ori.schmidt_coef(qid_0=[0,1], qid_1=[2,3])
        expect = np.array([0.7617283446607606, 0.5858869297203181,
                           0.266279733863013, 0.0748434222702293])
        ans = equal_vectors(actual, expect)
        self.assertEqual(ans, True)

class TestQState_operate(unittest.TestCase):
    """ test 'QState' : 'operate'
    """

    def test_operate_x(self):
        """test 'operate' (x)
        """
        qs_expect = QState(qubit_num=1)
        qs_actual = QState(qubit_num=1)
        pp = PauliProduct(pauli_str="X")
        qs_expect.x(0)
        qs_actual.operate(pp=pp)
        ans = equal_qstates(qs_expect, qs_actual)
        self.assertEqual(ans,True)
        
    def test_operate_h_x(self):
        """test 'operate' (x followed by h)
        """
        qs_expect = QState(qubit_num=1).h(0)
        qs_actual = QState(qubit_num=1).h(0)
        pp = PauliProduct(pauli_str="X")
        qs_expect.x(0)
        qs_actual.operate(pp=pp)
        ans = equal_qstates(qs_expect, qs_actual)
        self.assertEqual(ans,True)
        
    def test_operate_h_y(self):
        """test 'operate' (y followed by h)
        """
        qs_expect = QState(qubit_num=1).h(0)
        qs_actual = QState(qubit_num=1).h(0)
        pp = PauliProduct(pauli_str="Y")
        qs_expect.y(0)
        qs_actual.operate(pp=pp)
        ans = equal_qstates(qs_expect, qs_actual)
        self.assertEqual(ans,True)
        
    def test_operate_h_z(self):
        """test 'operate' (z followed by h)
        """
        qs_expect = QState(qubit_num=1).h(0)
        qs_actual = QState(qubit_num=1).h(0)
        pp = PauliProduct(pauli_str="Z")
        qs_expect.z(0)
        qs_actual.operate(pp=pp)
        ans = equal_qstates(qs_expect, qs_actual)
        self.assertEqual(ans,True)
        
    def test_operate_xyz(self):
        """test 'operate' (xyz)
        """
        qs_expect = QState(qubit_num=3)
        qs_actual = QState(qubit_num=3)
        pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
        qs_expect.x(2).y(0).z(1)
        qs_actual.operate(pp=pp)
        ans = equal_qstates(qs_expect, qs_actual)
        self.assertEqual(ans,True)
        
    def test_operate_controlled_xyz(self):
        """test 'operate' (controlled_xyz)
        """
        qs_expect = QState(qubit_num=4)
        qs_actual = QState(qubit_num=4)
        pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
        qs_expect.cx(3,2).cy(3,0).cz(3,1)
        qs_actual.operate(pp=pp, ctrl=3)
        ans = equal_qstates(qs_expect, qs_actual)
        self.assertEqual(ans,True)
        
class TestQState_inheritance(unittest.TestCase):
    """ test 'QState' : inheritance
    """

    def test_inheritance_1(self):
        """test 'inheritance_1'
        """
        qs_expect = QState(qubit_num=2).h(0).cx(0,1).x(0)
        qs_actual = MyQState(qubit_num=2).bell(0,1).x(0)
        fid = qs_expect.fidelity(qs_actual)
        self.assertEqual(abs(fid-1.0) < EPS, True)

    def test_inheritance_2(self):
        """test 'inheritance_2'
        """
        qs_expect = QState(qubit_num=2).h(0).cx(0,1).x(0)
        qs_actual = MyQState(qubit_num=2).clone()
        qs_actual = qs_actual.bell(0,1).x(0)
        fid = qs_expect.fidelity(qs_actual)
        self.assertEqual(abs(fid-1.0) < EPS, True)

    def test_inheritance_3(self):
        """test 'inheritance_3'
        """
        qs_A = QState(qubit_num=1)
        qs_B = QState(qubit_num=1)
        qs_expect = qs_A.tenspro(qs_B).h(0).cx(0,1).x(0)
        qs_C = MyQState(qubit_num=1)
        qs_D = MyQState(qubit_num=1)
        qs_actual = qs_C.tenspro(qs_D)
        qs_actual.bell(0,1).x(0)
        fid = qs_expect.fidelity(qs_actual)
        self.assertEqual(abs(fid-1.0) < EPS, True)

if __name__ == '__main__':
    unittest.main()
