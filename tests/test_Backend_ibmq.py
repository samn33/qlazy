# -*- coding: utf-8 -*-
""" unittest of aws backend """
import unittest
import random

from qlazy import QCirc, Backend, QState, PauliProduct
from qlazy.tools.Probability import freq2prob, kl_divergence

EPS = 0.01

class MyQCirc(QCirc):
    """ for inheritance """

    def bell(self, q0, q1):
        """ bell circuit """
        self.h(q0).cx(q0, q1)
        return self

#=======
# ibmq
#=======

def evaluate(qc, qs, verbose=False):
    """ evaluate """

    # backend
    shots = 1000
    bk = Backend(product='ibmq', device='aer_simulator')
    res = bk.run(qcirc=qc, shots=shots)
    prob_aws = freq2prob(res.frequency)

    # qlazy
    prob_qlz = qs.get_prob()

    if verbose is True:
        print("prob_qlz =", prob_qlz)
        print("prob_aws =", prob_aws)

    value = kl_divergence(prob_qlz, prob_aws)

    if verbose is True:
        print("value =", value)

    if value >= EPS:
        print("value =", value)

    return value

#
# 1-qubit gate
#

class TestBackend_1_qubit(unittest.TestCase):
    """ test 'Backend' : 1-qubit gate
    """

    def test_x(self):
        """test 'x' gate
        """
        qc = QCirc().x(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).x(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_h_x(self):
        """test 'x-h' gate
        """
        qc = QCirc().h(0).x(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).h(0).x(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_y(self):
        """test 'y' gate
        """
        qc = QCirc().y(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).y(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_h_y(self):
        """test 'h-y' gate
        """
        qc = QCirc().h(0).y(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).h(0).y(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_z(self):
        """test 'z' gate
        """
        qc = QCirc().z(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).z(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_h_z(self):
        """test 'h-z' gate
        """
        qc = QCirc().h(0).z(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).h(0).z(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_xr(self):
        """test 'xr' gate
        """
        qc = QCirc().xr(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).xr(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_h_xr(self):
        """test 'h-xr' gate
        """
        qc = QCirc().h(0).xr(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).h(0).xr(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_xr_dg(self):
        """test 'xr_dg' gate
        """
        qc = QCirc().xr_dg(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).xr_dg(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_h_xr_dg(self):
        """test 'h-xr_dg' gate
        """
        qc = QCirc().h(0).xr_dg(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).h(0).xr_dg(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_h(self):
        """test 'h' gate
        """
        qc = QCirc().h(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).h(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_s(self):
        """test 's' gate
        """
        qc = QCirc().s(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).s(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_h_s(self):
        """test 'h-s' gate
        """
        qc = QCirc().h(0).s(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).h(0).s(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_s_dg(self):
        """test 's_dg' gate
        """
        qc = QCirc().s_dg(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).s_dg(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_h_s_dg(self):
        """test 'h-s_dg' gate
        """
        qc = QCirc().h(0).s_dg(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).h(0).s_dg(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_t(self):
        """test 't' gate
        """
        qc = QCirc().t(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).t(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_h_t(self):
        """test 'h-t-h' gate
        """
        qc = QCirc().h(0).t(0).h(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).h(0).t(0).h(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_t_dg(self):
        """test 't_dg' gate
        """
        qc = QCirc().t_dg(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).t_dg(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_h_t_dg(self):
        """test 'h-t_dg-h' gate
        """
        qc = QCirc().h(0).t_dg(0).h(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).h(0).t_dg(0).h(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_rx(self):
        """test 'rx' gate
        """
        qc = QCirc().rx(0, phase=0.1).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).rx(0, phase=0.1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_h_rx(self):
        """test 'h-rx-h' gate
        """
        qc = QCirc().h(0).rx(0, phase=0.1).h(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).h(0).rx(0, phase=0.1).h(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_ry(self):
        """test 'ry' gate
        """
        qc = QCirc().ry(0, phase=0.1).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).ry(0, phase=0.1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_h_ry(self):
        """test 'h-ry-h' gate
        """
        qc = QCirc().h(0).ry(0, phase=0.1).h(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).h(0).ry(0, phase=0.1).h(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_rz(self):
        """test 'rz' gate
        """
        qc = QCirc().rz(0, phase=0.1).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).rz(0, phase=0.1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_h_rz(self):
        """test 'h-rz-h' gate
        """
        qc = QCirc().h(0).rz(0, phase=0.1).h(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).h(0).rz(0, phase=0.1).h(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_p(self):
        """test 'p' gate
        """
        qc = QCirc().p(0, phase=0.1).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).p(0, phase=0.1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_h_p_h(self):
        """test 'h-p-h' gate
        """
        qc = QCirc().h(0).p(0, phase=0.1).h(0).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).h(0).p(0, phase=0.1).h(0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

#
# 2-qubit gate
#

class TestBackend_2_qubit(unittest.TestCase):
    """ test 'Backend' : 2-qubit gate
    """

    def test_cx(self):
        """test 'cx' gate
        """
        qc = QCirc().h(0).h(1).cx(0, 1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).cx(0, 1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_cy(self):
        """test 'cy' gate
        """
        qc = QCirc().h(0).h(1).cy(0, 1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).cy(0, 1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_cz(self):
        """test 'cz' gate
        """
        qc = QCirc().h(0).h(1).cz(0, 1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).cz(0, 1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_cxr(self):
        """test 'cxr' gate
        """
        qc = QCirc().h(0).h(1).cxr(0, 1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).cxr(0, 1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_cxr_dg(self):
        """test 'cxr_dg' gate
        """
        qc = QCirc().h(0).h(1).cxr_dg(0, 1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).cxr_dg(0, 1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_ch(self):
        """test 'ch' gate
        """
        qc = QCirc().h(0).h(1).ch(0, 1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).ch(0, 1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_cs(self):
        """test 'cs' gate
        """
        qc = QCirc().h(0).h(1).cs(0, 1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).cs(0, 1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_cs_dg(self):
        """test 'cs_dg' gate
        """
        qc = QCirc().h(0).h(1).cs_dg(0, 1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).cs_dg(0, 1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_ct(self):
        """test 'ct' gate
        """
        qc = QCirc().h(0).h(1).ct(0, 1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).ct(0, 1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_ct_dg(self):
        """test 'ct_dg' gate
        """
        qc = QCirc().h(0).h(1).ct_dg(0, 1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).ct_dg(0, 1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_sw(self):
        """test 'sw' gate
        """
        qc = QCirc().sw(0, 1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).sw(0, 1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_h_sw(self):
        """test 'h-sw' gate
        """
        qc = QCirc().h(0).sw(0, 1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).sw(0, 1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_x_sw(self):
        """test 'x-sw' gate
        """
        qc = QCirc().x(0).sw(0, 1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).x(0).sw(0, 1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_cp(self):
        """test 'cp' gate
        """
        qc = QCirc().h(0).h(1).cp(0, 1, phase=0.1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).cp(0, 1, phase=0.1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_crx(self):
        """test 'crx' gate
        """
        qc = QCirc().h(0).h(1).crx(0, 1, phase=0.1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).crx(0, 1, phase=0.1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_cry(self):
        """test 'cry' gate
        """
        qc = QCirc().h(0).h(1).cry(0, 1, phase=0.1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).cry(0, 1, phase=0.1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_crz(self):
        """test 'crz' gate
        """
        qc = QCirc().h(0).h(1).crz(0, 1, phase=0.1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).crz(0, 1, phase=0.1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_rxx(self):
        """test 'rxx' gate
        """
        qc = QCirc().h(0).h(1).rxx(0, 1, phase=0.1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).rxx(0, 1, phase=0.1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_ryy(self):
        """test 'ryy' gate
        """
        qc = QCirc().h(0).h(1).ryy(0, 1, phase=0.1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).ryy(0, 1, phase=0.1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_rzz(self):
        """test 'rzz' gate
        """
        qc = QCirc().h(0).h(1).rzz(0, 1, phase=0.1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).h(1).rzz(0, 1, phase=0.1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

#
# 3-qubit gate
#

class TestBackend_3_qubit(unittest.TestCase):
    """ test 'Backend' : 3-qubit gate
    """

    def test_ccx(self):
        """test 'ccx' gate
        """
        qc = QCirc().x(0).x(1).ccx(0, 1, 2).measure(qid=[0, 1, 2], cid=[0, 1, 2])
        qs = QState(qubit_num=3).x(0).x(1).ccx(0, 1, 2)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_csw(self):
        """test 'csw' gate
        """
        qc = QCirc().x(0).x(1).csw(0, 1, 2).measure(qid=[0, 1, 2], cid=[0, 1, 2])
        qs = QState(qubit_num=3).x(0).x(1).csw(0, 1, 2)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

#
# operate
#

class TestBackend_operate(unittest.TestCase):
    """ test 'Backend' : operate
    """

    def test_operate_x(self):
        """test 'operate' (x)
        """
        pp = PauliProduct(pauli_str="X")
        qc = QCirc().operate(pp=pp).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).operate(pp=pp)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_operate_h_y(self):
        """test 'operate' (h-y)
        """
        pp = PauliProduct(pauli_str="Y")
        qc = QCirc().h(0).operate(pp=pp).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).h(0).operate(pp=pp)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_operate_h_z(self):
        """test 'operate' (h-z)
        """
        pp = PauliProduct(pauli_str="Z")
        qc = QCirc().h(0).operate(pp=pp).measure(qid=[0], cid=[0])
        qs = QState(qubit_num=1).h(0).operate(pp=pp)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_operate_xyz(self):
        """test 'operate' (xyz)
        """
        pp = PauliProduct(pauli_str="XYZ")
        qc = QCirc().operate(pp=pp).measure(qid=[0, 1, 2], cid=[0, 1, 2])
        qs = QState(qubit_num=3).operate(pp=pp)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

    def test_operate_controlled_xyz(self):
        """test 'operate' (xyz)
        """
        pp = PauliProduct(pauli_str="XYZ", qid=[1, 2, 3])
        qc = QCirc().operate(pp=pp, qctrl=0).measure(qid=[0, 1, 2, 3], cid=[0, 1, 2, 3])
        qs = QState(qubit_num=4).operate(pp=pp, qctrl=0)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

#
# random
#

class TestBackend_random(unittest.TestCase):
    """ test 'Backend' : random
    """

    def test_measure_random(self):
        """test 'random'
        """

        a, b, c = random.random(), random.random(), random.random()
        d, e, f = random.random(), random.random(), random.random()

        qc = QCirc()
        qc.rz(0, phase=a).rx(0, phase=b).rz(0, phase=c).h(0).cx(0, 1)
        qc.rz(1, phase=d).rx(1, phase=e).rz(1, phase=f).h(0).cx(0, 1)
        qc.measure(qid=[0, 1], cid=[0, 1])

        qs = QState(qubit_num=2)
        qs.rz(0, phase=a).rx(0, phase=b).rz(0, phase=c).h(0).cx(0, 1)
        qs.rz(1, phase=d).rx(1, phase=e).rz(1, phase=f).h(0).cx(0, 1)

        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

#
# inheritance
#

class TestBackend_inheritance(unittest.TestCase):
    """ test 'Backend' : inheritance
    """

    def test_inheritance(self):
        """test 'inheritance'
        """
        qc = MyQCirc().bell(0, 1).measure(qid=[0, 1], cid=[0, 1])
        qs = QState(qubit_num=2).h(0).cx(0, 1)
        value = evaluate(qc, qs)
        self.assertEqual(value < EPS, True)

if __name__ == '__main__':
    unittest.main()
