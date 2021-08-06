# -*- coding: utf-8 -*-
import unittest

from qlazy.tools.Register import CreateRegister, InitRegister
from qlazy import QState, QComp, Backend

class TestRegister(unittest.TestCase):
    """ test 'Register' : CreateRegister, InitRegister
    """

    def test_0(self):
        
        reg_0 = CreateRegister(3)
        reg_1 = CreateRegister(2)
        reg_num = InitRegister(reg_0, reg_1)
        self.assertEqual((reg_num, reg_0, reg_1), (5, [0,1,2], [3,4]))

    def test_1(self):
    
        reg_0 = CreateRegister(5)
        reg_1 = CreateRegister(3,4)
        reg_2 = CreateRegister(2,3,4)
        reg_num = InitRegister(reg_0, reg_1, reg_2)
        self.assertEqual((reg_num, reg_0, reg_1, reg_2),
                         (41, [0,1,2,3,4], [[5,6,7,8],[9,10,11,12],[13,14,15,16]],
                          [[[17,18,19,20],[21,22,23,24],[25,26,27,28]],
                           [[29,30,31,32],[33,34,35,36],[37,38,39,40]]]))
        
    def test_2(self):

        # first
        reg_0 = CreateRegister(5)
        reg_1 = CreateRegister(3,4)
        reg_2 = CreateRegister(2,3,4)
        reg_num = InitRegister(reg_0, reg_1, reg_2)
    
        # second (overwrite)
        reg_0 = CreateRegister(5)
        reg_1 = CreateRegister(3,4)
        reg_2 = CreateRegister(2,3,4)
        reg_num = InitRegister(reg_0, reg_1, reg_2)
        self.assertEqual((reg_num, reg_0, reg_1, reg_2),
                         (41, [0,1,2,3,4], [[5,6,7,8],[9,10,11,12],[13,14,15,16]],
                          [[[17,18,19,20],[21,22,23,24],[25,26,27,28]],
                           [[29,30,31,32],[33,34,35,36],[37,38,39,40]]]))
    
class TestRegisterQComp(unittest.TestCase):
    """ test 'Register' : CreateRegister, InitRegister, QComp
    """

    def test_0(self):

        qid_0 = CreateRegister(1)
        qid_1 = CreateRegister(2,2)
        qubit_num = InitRegister(qid_0, qid_1)

        cid_0 = CreateRegister(1)
        cmem_num = InitRegister(cid_0)

        bk = Backend(name='qlazy', device='qstate_simulator')
        qc = QComp(qubit_num=qubit_num, cmem_num=cmem_num, backend=bk)
        qc.h(qid_0[0])
        qc.cx(qid_0[0], qid_1[0][0]).cx(qid_0[0], qid_1[0][1]).cx(qid_0[0], qid_1[1][0]).cx(qid_0[0], qid_1[1][1])
        qc.h(qid_0[0])
        qc.measure(qid=[qid_0[0]], cid=[cid_0[0]])
        res = qc.run(shots=10)
        self.assertEqual(res['measured_qid'], [0])
        self.assertEqual(res['frequency']['0']+res['frequency']['1'], 10)
        
    def test_1(self):

        qid_0 = CreateRegister(2)
        qid_1 = CreateRegister(3,4)
        qubit_num = InitRegister(qid_0, qid_1)
        
        cid_0 = CreateRegister(4)
        cid_1 = CreateRegister(2,3)
        cmem_num = InitRegister(cid_0, cid_1)
        
        bk = Backend(name='qlazy', device='qstate_simulator')
        qc = QComp(qubit_num=qubit_num, cmem_num=cmem_num, backend=bk)
        qc.h(qid_0[1]).cx(qid_0[1], qid_1[0][2]).measure(qid=[qid_0[1], qid_1[0][2]], cid=[cid_1[0][0],cid_1[1][1]])
        res = qc.run(shots=10)
        self.assertEqual(res['measured_qid'], [1,4])
        self.assertEqual(res['frequency']['00']+res['frequency']['11'], 10)
        # qc.free()

if __name__ == '__main__':
    unittest.main()
