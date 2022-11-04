# -*- coding: utf-8 -*-
import sys
import unittest
import math
import numpy as np
from qlazy import Stabilizer, PauliProduct

class MyStabilizer(Stabilizer):

    def __init__(self, qubit_num=0, name=None):
        super().__init__(qubit_num=qubit_num)
        self.name = name

    def get_name(self):
        return self.name
     
    def bell(self, q0, q1):
        self.h(q0).cx(q0,q1)
        return self

class TestStabilizer_init(unittest.TestCase):
    """ test 'Stabilizer' : '__new__'
    """

    def test_init_1(self):
        """test '__new__' (gene_num = qubit_num)
        """
        sb = Stabilizer(qubit_num=3)
        actual = sb.get_str()
        expect = "  III\n  III\n  III\n"
        self.assertEqual(actual, expect)

    def test_init_2(self):
        """test '__new__' (gene_num < qubit_num)
        """
        sb = Stabilizer(gene_num=2, qubit_num=3)
        actual = sb.get_str()
        expect = "  III\n  III\n"
        self.assertEqual(actual, expect)

    def test_init_3(self):
        """test '__new__' (gene_num > qubit_num)
        """
        sb = Stabilizer(gene_num=3, qubit_num=2)
        actual = sb.get_str()
        expect = "  II\n  II\n  II\n"
        self.assertEqual(actual, expect)

    def test_init_4(self):
        """test '__new__' (seed)
        """
        sb = Stabilizer(gene_num=3, qubit_num=3, seed=123)
        actual = sb.get_str()
        expect = "  III\n  III\n  III\n"
        self.assertEqual(actual, expect)

    def test_init_pp(self):
        """test '__new__' (seed)
        """
        gene_str_list = ["IIIXXXX", "IXXIIXX", "XIXIXIX", "IIIZZZZ", "IZZIIZZ", "ZIZIZIZ"]
        gene_list = [PauliProduct(pauli_str=gene_str, qid=[0,2,4,6,8,7,5]) for gene_str in gene_str_list]
        sb = Stabilizer(pp_list=gene_list)
        actual = sb.get_str()
        expect = "  IIIIIXXXX\n  IIXIXXIXI\n  XIIIXXIIX\n  IIIIIZZZZ\n  IIZIZZIZI\n  ZIIIZZIIZ\n"
        self.assertEqual(actual, expect)
        
class TestStabilizer_set_all(unittest.TestCase):
    """ test 'Stabilizer' : 'set_all'
    """

    def test_set_all_1(self):
        """test 'set_all' (gene_num = qubit_num, 'X')
        """
        sb = Stabilizer(qubit_num=3)
        sb.set_all('X')
        actual = sb.get_str()
        expect = "  XII\n  IXI\n  IIX\n"
        self.assertEqual(actual, expect)
        
    def test_set_all_2(self):
        """test 'set_all' (gene_num < qubit_num, 'X')
        """
        sb = Stabilizer(gene_num=2, qubit_num=3)
        sb.set_all('X')
        actual = sb.get_str()
        expect = "  XII\n  IXI\n"
        self.assertEqual(actual, expect)
        
    def test_set_all_3(self):
        """test 'set_all' (gene_num > qubit_num, 'X')
        """
        sb = Stabilizer(gene_num=3, qubit_num=2)
        sb.set_all('X')
        actual = sb.get_str()
        expect = "  XI\n  IX\n  II\n"
        self.assertEqual(actual, expect)
        
    def test_set_all_4(self):
        """test 'set_all' (gene_num = qubit_num, 'Y')
        """
        sb = Stabilizer(qubit_num=3)
        sb.set_all('Y')
        actual = sb.get_str()
        expect = "  YII\n  IYI\n  IIY\n"
        self.assertEqual(actual, expect)

    def test_set_all_5(self):
        """test 'set_all' (gene_num = qubit_num, 'Z')
        """
        sb = Stabilizer(qubit_num=3)
        sb.set_all('Z')
        actual = sb.get_str()
        expect = "  ZII\n  IZI\n  IIZ\n"
        self.assertEqual(actual, expect)

    def test_set_all_6(self):
        """test 'set_all' (gene_num = qubit_num, 'I')
        """
        sb = Stabilizer(qubit_num=3)
        sb.set_all('I')
        actual = sb.get_str()
        expect = "  III\n  III\n  III\n"
        self.assertEqual(actual, expect)

class TestStabilizer_reset(unittest.TestCase):
    """ test 'Stabilizer' : 'reset'
    """

    def test_reset_1(self):
        """test 'reset'
        """
        sb = Stabilizer(gene_num=4, qubit_num=3)
        sb.set_all('Y').reset()
        actual = sb.get_str()
        expect = "  III\n  III\n  III\n  III\n"
        self.assertEqual(actual, expect)
        
class TestStabilizer_clone(unittest.TestCase):
    """ test 'Stabilizer' : 'clone'
    """

    def test_reset_1(self):
        """test 'clone'
        """
        sb = Stabilizer(gene_num=4, qubit_num=3)
        sb.set_all('Y')
        sb_clone = sb.clone()
        actual = sb_clone.get_str()
        expect = sb.get_str()
        self.assertEqual(actual, expect)
        
class TestStabilizer_set_pauli_fac(unittest.TestCase):
    """ test 'Stabilizer' : 'set_pauli_fac'
    """

    def test_set_pauli_fac_1(self):
        """test 'set_pauli_fac'
        """
        sb = Stabilizer(gene_num=3, qubit_num=4)
        sb.set_all('Z')
        actual = sb.set_pauli_fac(1,'-i').get_str()
        expect = "  ZIII\n-iIZII\n  IIZI\n"
        self.assertEqual(actual, expect)

    def test_set_pauli_fac_2(self):
        """test 'set_pauli_fac'
        """
        sb = Stabilizer(gene_num=3, qubit_num=4)
        sb.set_all('Z').set_pauli_op(1,0,'Y').set_pauli_op(1,2,'Y')
        actual = sb.set_pauli_fac(1,'-i').get_str()
        expect = "  ZIII\n-iYZYI\n  IIZI\n"
        self.assertEqual(actual, expect)

class TestStabilizer_get_pauli_fac(unittest.TestCase):
    """ test 'Stabilizer' : 'get_pauli_fac'
    """

    def test_get_pauli_fac_1(self):
        """test 'get_pauli_fac'
        """
        sb = Stabilizer(gene_num=3, qubit_num=4)
        sb.set_all('Z')
        sb.set_pauli_fac(1,'-i')
        actual = sb.get_pauli_fac(1)
        expect = -1j
        self.assertEqual(actual, expect)

    def test_get_pauli_fac_2(self):
        """test 'get_pauli_fac'
        """
        sb = Stabilizer(gene_num=3, qubit_num=4)
        sb.set_all('Y').set_pauli_op(1,2,'Y')
        sb.set_pauli_fac(1,'-i')
        actual = sb.get_pauli_fac(1)
        expect = -1j
        self.assertEqual(actual, expect)

class TestStabilizer_set_pauli_op(unittest.TestCase):
    """ test 'Stabilizer' : 'set_pauli_op'
    """

    def test_set_pauli_op_1(self):
        """test 'set_pauli_op'
        """
        sb = Stabilizer(gene_num=4, qubit_num=3)
        sb.set_pauli_op(0,0,'X').set_pauli_op(0,1,'Y').set_pauli_op(0,2,'Z')
        sb.set_pauli_op(1,0,'Y').set_pauli_op(1,1,'Z').set_pauli_op(1,2,'X')
        sb.set_pauli_op(2,0,'Z').set_pauli_op(2,1,'X').set_pauli_op(2,2,'Y')
        sb.set_pauli_op(3,0,'I').set_pauli_op(3,1,'I').set_pauli_op(3,2,'I')
        actual = sb.get_str()
        expect = "  XYZ\n  YZX\n  ZXY\n  III\n"
        self.assertEqual(actual, expect)
        
    def test_set_pauli_op_2(self):
        """test 'set_pauli_op'
        """
        sb = Stabilizer(gene_num=4, qubit_num=3)
        sb.set_pauli_op(0,0,'X').set_pauli_op(0,1,'Y').set_pauli_op(0,2,'Z')
        sb.set_pauli_op(1,0,'Y').set_pauli_op(1,1,'Z').set_pauli_op(1,2,'X')
        sb.set_pauli_op(2,0,'Z').set_pauli_op(2,1,'X').set_pauli_op(2,2,'Y')
        sb.set_pauli_op(3,0,'I').set_pauli_op(3,1,'I').set_pauli_op(3,2,'I')
        sb.set_pauli_fac(0,'+1').set_pauli_fac(1,'-1')
        sb.set_pauli_fac(2,'+i').set_pauli_fac(3,'-i')
        
        actual = sb.get_str()
        expect = "  XYZ\n -YZX\n iZXY\n-iIII\n"
        self.assertEqual(actual, expect)
        
class TestStabilizer_get_pauli_op(unittest.TestCase):
    """ test 'Stabilizer' : 'get_pauli_op'
    """

    def test_get_pauli_op_1(self):
        """test 'get_pauli_op'
        """
        sb = Stabilizer(gene_num=4, qubit_num=3)
        sb.set_pauli_op(0,0,'X').set_pauli_op(0,1,'Y').set_pauli_op(0,2,'Z')
        sb.set_pauli_op(1,0,'Y').set_pauli_op(1,1,'Z').set_pauli_op(1,2,'X')
        sb.set_pauli_op(2,0,'Z').set_pauli_op(2,1,'X').set_pauli_op(2,2,'Y')
        sb.set_pauli_op(3,0,'I').set_pauli_op(3,1,'I').set_pauli_op(3,2,'I')
        actual = sb.get_pauli_op(3,2)
        expect = "I"
        self.assertEqual(actual, expect)
        
    def test_get_pauli_op_2(self):
        """test 'get_pauli_op'
        """
        sb = Stabilizer(gene_num=4, qubit_num=3)
        sb.set_pauli_op(0,0,'X').set_pauli_op(0,1,'Y').set_pauli_op(0,2,'Z')
        sb.set_pauli_op(1,0,'Y').set_pauli_op(1,1,'Z').set_pauli_op(1,2,'X')
        sb.set_pauli_op(2,0,'Z').set_pauli_op(2,1,'X').set_pauli_op(2,2,'Y')
        sb.set_pauli_op(3,0,'I').set_pauli_op(3,1,'I').set_pauli_op(3,2,'I')
        sb.set_pauli_fac(0,'+1').set_pauli_fac(1,'-1')
        sb.set_pauli_fac(2,'+i').set_pauli_fac(3,'-i')
        actual = sb.get_pauli_op(3,2)
        expect = "I"
        self.assertEqual(actual, expect)
        
class TestStabilizer_x(unittest.TestCase):
    """ test 'Stabilizer' : 'X'
    """

    def test_x_1(self):
        """test 'X' (input:X)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'X')
        sb.x(0)
        actual = sb.get_str()
        expect = "  X\n"
        self.assertEqual(actual, expect)
        
    def test_x_2(self):
        """test 'X' (input:Y)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'Y')
        sb.x(0)
        actual = sb.get_str()
        expect = " -Y\n"
        self.assertEqual(actual, expect)
        
    def test_x_3(self):
        """test 'X' (input:Z)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'Z')
        sb.x(0)
        actual = sb.get_str()
        expect = " -Z\n"
        self.assertEqual(actual, expect)
        
    def test_x_4(self):
        """test 'X' (input:I)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'I')
        sb.x(0)
        actual = sb.get_str()
        expect = "  I\n"
        self.assertEqual(actual, expect)
        
class TestStabilizer_y(unittest.TestCase):
    """ test 'Stabilizer' : 'Y'
    """

    def test_y_1(self):
        """test 'Y' (input:X)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'X')
        sb.y(0)
        actual = sb.get_str()
        expect = " -X\n"
        self.assertEqual(actual, expect)
        
    def test_y_2(self):
        """test 'Y' (input:Y)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'Y')
        sb.y(0)
        actual = sb.get_str()
        expect = "  Y\n"
        self.assertEqual(actual, expect)
        
    def test_y_3(self):
        """test 'Y' (input:Z)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'Z')
        sb.y(0)
        actual = sb.get_str()
        expect = " -Z\n"
        self.assertEqual(actual, expect)
        
    def test_y_4(self):
        """test 'Y' (input:I)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'I')
        sb.y(0)
        actual = sb.get_str()
        expect = "  I\n"
        self.assertEqual(actual, expect)
        
class TestStabilizer_z(unittest.TestCase):
    """ test 'Stabilizer' : 'Z'
    """

    def test_z_1(self):
        """test 'Z' (input:X)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'X')
        sb.z(0)
        actual = sb.get_str()
        expect = " -X\n"
        self.assertEqual(actual, expect)
        
    def test_z_2(self):
        """test 'Z' (input:Y)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'Y')
        sb.z(0)
        actual = sb.get_str()
        expect = " -Y\n"
        self.assertEqual(actual, expect)
        
    def test_z_3(self):
        """test 'Z' (input:Z)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'Z')
        sb.z(0)
        actual = sb.get_str()
        expect = "  Z\n"
        self.assertEqual(actual, expect)
        
    def test_z_4(self):
        """test 'Z' (input:I)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'I')
        sb.z(0)
        actual = sb.get_str()
        expect = "  I\n"
        self.assertEqual(actual, expect)
        
class TestStabilizer_h(unittest.TestCase):
    """ test 'Stabilizer' : 'H'
    """

    def test_h_1(self):
        """test 'H' (input:X)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'X')
        sb.h(0)
        actual = sb.get_str()
        expect = "  Z\n"
        self.assertEqual(actual, expect)
        
    def test_h_2(self):
        """test 'H' (input:Y)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'Y')
        sb.h(0)
        actual = sb.get_str()
        expect = " -Y\n"
        self.assertEqual(actual, expect)
        
    def test_h_3(self):
        """test 'H' (input:Z)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'Z')
        sb.h(0)
        actual = sb.get_str()
        expect = "  X\n"
        self.assertEqual(actual, expect)
        
    def test_h_4(self):
        """test 'H' (input:I)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'I')
        sb.h(0)
        actual = sb.get_str()
        expect = "  I\n"
        self.assertEqual(actual, expect)
        
class TestStabilizer_s(unittest.TestCase):
    """ test 'Stabilizer' : 'S'
    """

    def test_s_1(self):
        """test 'S' (input:X)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'X')
        sb.s(0)
        actual = sb.get_str()
        expect = "  Y\n"
        self.assertEqual(actual, expect)
        
    def test_s_2(self):
        """test 'S' (input:Y)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'Y')
        sb.s(0)
        actual = sb.get_str()
        expect = " iX\n"
        self.assertEqual(actual, expect)
        
    def test_s_3(self):
        """test 'S' (input:Z)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'Z')
        sb.s(0)
        actual = sb.get_str()
        expect = "  Z\n"
        self.assertEqual(actual, expect)
        
    def test_s_4(self):
        """test 'S' (input:I)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'I')
        sb.s(0)
        actual = sb.get_str()
        expect = "  I\n"
        self.assertEqual(actual, expect)
        
class TestStabilizer_s_dg(unittest.TestCase):
    """ test 'Stabilizer' : 'S+'
    """

    def test_s_dg_1(self):
        """test 'S+' (input:X)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'X')
        sb.s_dg(0)
        actual = sb.get_str()
        expect = " -Y\n"
        self.assertEqual(actual, expect)
        
    def test_s_dg_2(self):
        """test 'S+' (input:Y)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'Y')
        sb.s_dg(0)
        actual = sb.get_str()
        expect = "-iX\n"
        self.assertEqual(actual, expect)
        
    def test_s_dg_3(self):
        """test 'S+' (input:Z)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'Z')
        sb.s_dg(0)
        actual = sb.get_str()
        expect = "  Z\n"
        self.assertEqual(actual, expect)
        
    def test_s_dg_4(self):
        """test 'S+' (input:I)
        """
        sb = Stabilizer(gene_num=1, qubit_num=1)
        sb.set_pauli_op(0,0,'I')
        sb.s_dg(0)
        actual = sb.get_str()
        expect = "  I\n"
        self.assertEqual(actual, expect)
        
class TestStabilizer_cx(unittest.TestCase):
    """ test 'Stabilizer' : 'CX'
    """

    def test_cx_1(self):
        """test 'CX' (input:II)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'I').set_pauli_op(0,1,'I')
        sb.cx(0,1)
        actual = sb.get_str()
        expect = "  II\n"
        self.assertEqual(actual, expect)
        
    def test_cx_2(self):
        """test 'CX' (input:XI)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'X').set_pauli_op(0,1,'I')
        sb.cx(0,1)
        actual = sb.get_str()
        expect = "  XX\n"
        self.assertEqual(actual, expect)
        
    def test_cx_3(self):
        """test 'CX' (input:IX)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'I').set_pauli_op(0,1,'X')
        sb.cx(0,1)
        actual = sb.get_str()
        expect = "  IX\n"
        self.assertEqual(actual, expect)
        
    def test_cx_4(self):
        """test 'CX' (input:YI)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Y').set_pauli_op(0,1,'I')
        sb.cx(0,1)
        actual = sb.get_str()
        expect = "  YX\n"
        self.assertEqual(actual, expect)
        
    def test_cx_5(self):
        """test 'CX' (input:IY)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'I').set_pauli_op(0,1,'Y')
        sb.cx(0,1)
        actual = sb.get_str()
        expect = "  ZY\n"
        self.assertEqual(actual, expect)
        
    def test_cx_6(self):
        """test 'CX' (input:ZI)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Z').set_pauli_op(0,1,'I')
        sb.cx(0,1)
        actual = sb.get_str()
        expect = "  ZI\n"
        self.assertEqual(actual, expect)
        
    def test_cx_7(self):
        """test 'CX' (input:IZ)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'I').set_pauli_op(0,1,'Z')
        sb.cx(0,1)
        actual = sb.get_str()
        expect = "  ZZ\n"
        self.assertEqual(actual, expect)
        
    def test_cx_8(self):
        """test 'CX' (input:XX)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'X').set_pauli_op(0,1,'X')
        sb.cx(0,1)
        actual = sb.get_str()
        expect = "  XI\n"
        self.assertEqual(actual, expect)
        
    def test_cx_9(self):
        """test 'CX' (input:XY)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'X').set_pauli_op(0,1,'Y')
        sb.cx(0,1)
        actual = sb.get_str()
        expect = "  YZ\n"
        self.assertEqual(actual, expect)
        
    def test_cx_10(self):
        """test 'CX' (input:XZ)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'X').set_pauli_op(0,1,'Z')
        sb.cx(0,1)
        actual = sb.get_str()
        expect = " -YY\n"
        self.assertEqual(actual, expect)
        
    def test_cx_11(self):
        """test 'CX' (input:YX)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Y').set_pauli_op(0,1,'X')
        sb.cx(0,1)
        actual = sb.get_str()
        expect = "  YI\n"
        self.assertEqual(actual, expect)
        
    def test_cx_12(self):
        """test 'CX' (input:YY)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Y').set_pauli_op(0,1,'Y')
        sb.cx(0,1)
        actual = sb.get_str()
        expect = " -XZ\n"
        self.assertEqual(actual, expect)
        
    def test_cx_13(self):
        """test 'CX' (input:YZ)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Y').set_pauli_op(0,1,'Z')
        sb.cx(0,1)
        actual = sb.get_str()
        expect = "  XY\n"
        self.assertEqual(actual, expect)
        
    def test_cx_14(self):
        """test 'CX' (input:ZX)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Z').set_pauli_op(0,1,'X')
        sb.cx(0,1)
        actual = sb.get_str()
        expect = "  ZX\n"
        self.assertEqual(actual, expect)
        
    def test_cx_15(self):
        """test 'CX' (input:ZY)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Z').set_pauli_op(0,1,'Y')
        sb.cx(0,1)
        actual = sb.get_str()
        expect = "  IY\n"
        self.assertEqual(actual, expect)
        
    def test_cx_16(self):
        """test 'CX' (input:ZZ)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Z').set_pauli_op(0,1,'Z')
        sb.cx(0,1)
        actual = sb.get_str()
        expect = "  IZ\n"
        self.assertEqual(actual, expect)
        
class TestStabilizer_cy(unittest.TestCase):
    """ test 'Stabilizer' : 'CY'
    """

    def test_cy_1(self):
        """test 'CY' (input:II)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'I').set_pauli_op(0,1,'I')
        sb.cy(0,1)
        actual = sb.get_str()
        expect = "  II\n"
        self.assertEqual(actual, expect)
        
    def test_cy_2(self):
        """test 'CY' (input:XI)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'X').set_pauli_op(0,1,'I')
        sb.cy(0,1)
        actual = sb.get_str()
        expect = "-iXY\n"
        self.assertEqual(actual, expect)

    def test_cy_3(self):
        """test 'CY' (input:IX)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'I').set_pauli_op(0,1,'X')
        sb.cy(0,1)
        actual = sb.get_str()
        expect = "  ZX\n"
        self.assertEqual(actual, expect)

    def test_cy_4(self):
        """test 'CY' (input:YI)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Y').set_pauli_op(0,1,'I')
        sb.cy(0,1)
        actual = sb.get_str()
        expect = "  YY\n"
        self.assertEqual(actual, expect)

    def test_cy_5(self):
        """test 'CY' (input:IY)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'I').set_pauli_op(0,1,'Y')
        sb.cy(0,1)
        actual = sb.get_str()
        expect = "  IY\n"
        self.assertEqual(actual, expect)

    def test_cy_6(self):
        """test 'CY' (input:ZI)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Z').set_pauli_op(0,1,'I')
        sb.cy(0,1)
        actual = sb.get_str()
        expect = "  ZI\n"
        self.assertEqual(actual, expect)

    def test_cy_7(self):
        """test 'CY' (input:IZ)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'I').set_pauli_op(0,1,'Z')
        sb.cy(0,1)
        actual = sb.get_str()
        expect = "  ZZ\n"
        self.assertEqual(actual, expect)

    def test_cy_8(self):
        """test 'CY' (input:XX)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'X').set_pauli_op(0,1,'X')
        sb.cy(0,1)
        actual = sb.get_str()
        expect = " -YZ\n"
        self.assertEqual(actual, expect)

    def test_cy_9(self):
        """test 'CY' (input:XY)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'X').set_pauli_op(0,1,'Y')
        sb.cy(0,1)
        actual = sb.get_str()
        expect = "-iXI\n"
        self.assertEqual(actual, expect)

    def test_cy_10(self):
        """test 'CY' (input:XZ)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'X').set_pauli_op(0,1,'Z')
        sb.cy(0,1)
        actual = sb.get_str()
        expect = "  YX\n"
        self.assertEqual(actual, expect)

    def test_cy_11(self):
        """test 'CY' (input:YX)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Y').set_pauli_op(0,1,'X')
        sb.cy(0,1)
        actual = sb.get_str()
        expect = "-iXZ\n"
        self.assertEqual(actual, expect)
        
    def test_cy_12(self):
        """test 'CY' (input:YY)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Y').set_pauli_op(0,1,'Y')
        sb.cy(0,1)
        actual = sb.get_str()
        expect = "  YI\n"
        self.assertEqual(actual, expect)
        
    def test_cy_13(self):
        """test 'CY' (input:YZ)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Y').set_pauli_op(0,1,'Z')
        sb.cy(0,1)
        actual = sb.get_str()
        expect = " iXX\n"
        self.assertEqual(actual, expect)

    def test_cy_14(self):
        """test 'CY' (input:ZX)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Z').set_pauli_op(0,1,'X')
        sb.cy(0,1)
        actual = sb.get_str()
        expect = "  IX\n"
        self.assertEqual(actual, expect)
        
    def test_cy_15(self):
        """test 'CY' (input:ZY)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Z').set_pauli_op(0,1,'Y')
        sb.cy(0,1)
        actual = sb.get_str()
        expect = "  ZY\n"
        self.assertEqual(actual, expect)
        
    def test_cy_16(self):
        """test 'CY' (input:ZZ)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Z').set_pauli_op(0,1,'Z')
        sb.cy(0,1)
        actual = sb.get_str()
        expect = "  IZ\n"
        self.assertEqual(actual, expect)
        
class TestStabilizer_cz(unittest.TestCase):
    """ test 'Stabilizer' : 'CZ'
    """

    def test_cz_1(self):
        """test 'CZ' (input:II)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'I').set_pauli_op(0,1,'I')
        sb.cz(0,1)
        actual = sb.get_str()
        expect = "  II\n"
        self.assertEqual(actual, expect)
        
    def test_cz_2(self):
        """test 'CZ' (input:XI)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'X').set_pauli_op(0,1,'I')
        sb.cz(0,1)
        actual = sb.get_str()
        expect = "  XZ\n"
        self.assertEqual(actual, expect)
        
    def test_cz_3(self):
        """test 'CZ' (input:IX)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'I').set_pauli_op(0,1,'X')
        sb.cz(0,1)
        actual = sb.get_str()
        expect = "  ZX\n"
        self.assertEqual(actual, expect)
        
    def test_cz_4(self):
        """test 'CZ' (input:YI)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Y').set_pauli_op(0,1,'I')
        sb.cz(0,1)
        actual = sb.get_str()
        expect = "  YZ\n"
        self.assertEqual(actual, expect)
        
    def test_cz_5(self):
        """test 'CZ' (input:IY)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'I').set_pauli_op(0,1,'Y')
        sb.cz(0,1)
        actual = sb.get_str()
        expect = "  ZY\n"
        self.assertEqual(actual, expect)
        
    def test_cz_6(self):
        """test 'CZ' (input:ZI)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Z').set_pauli_op(0,1,'I')
        sb.cz(0,1)
        actual = sb.get_str()
        expect = "  ZI\n"
        self.assertEqual(actual, expect)
        
    def test_cz_7(self):
        """test 'CZ' (input:IZ)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'I').set_pauli_op(0,1,'Z')
        sb.cz(0,1)
        actual = sb.get_str()
        expect = "  IZ\n"
        self.assertEqual(actual, expect)
        
    def test_cz_8(self):
        """test 'CZ' (input:XX)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'X').set_pauli_op(0,1,'X')
        sb.cz(0,1)
        actual = sb.get_str()
        expect = "  YY\n"
        self.assertEqual(actual, expect)
        
    def test_cz_9(self):
        """test 'CZ' (input:XY)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'X').set_pauli_op(0,1,'Y')
        sb.cz(0,1)
        actual = sb.get_str()
        expect = " -YX\n"
        self.assertEqual(actual, expect)
        
    def test_cz_10(self):
        """test 'CZ' (input:XZ)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'X').set_pauli_op(0,1,'Z')
        sb.cz(0,1)
        actual = sb.get_str()
        expect = "  XI\n"
        self.assertEqual(actual, expect)
        
    def test_cz_11(self):
        """test 'CZ' (input:YX)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Y').set_pauli_op(0,1,'X')
        sb.cz(0,1)
        actual = sb.get_str()
        expect = " -XY\n"
        self.assertEqual(actual, expect)
        
    def test_cz_12(self):
        """test 'CZ' (input:YY)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Y').set_pauli_op(0,1,'Y')
        sb.cz(0,1)
        actual = sb.get_str()
        expect = "  XX\n"
        self.assertEqual(actual, expect)
        
    def test_cz_13(self):
        """test 'CZ' (input:YZ)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Y').set_pauli_op(0,1,'Z')
        sb.cz(0,1)
        actual = sb.get_str()
        expect = "  YI\n"
        self.assertEqual(actual, expect)
        
    def test_cz_14(self):
        """test 'CZ' (input:ZX)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Z').set_pauli_op(0,1,'X')
        sb.cz(0,1)
        actual = sb.get_str()
        expect = "  IX\n"
        self.assertEqual(actual, expect)
        
    def test_cz_15(self):
        """test 'CZ' (input:ZY)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Z').set_pauli_op(0,1,'Y')
        sb.cz(0,1)
        actual = sb.get_str()
        expect = "  IY\n"
        self.assertEqual(actual, expect)
        
    def test_cz_16(self):
        """test 'CZ' (input:ZZ)
        """
        sb = Stabilizer(gene_num=1, qubit_num=2)
        sb.set_pauli_op(0,0,'Z').set_pauli_op(0,1,'Z')
        sb.cz(0,1)
        actual = sb.get_str()
        expect = "  ZZ\n"
        self.assertEqual(actual, expect)
        
class TestStabilizer_measure(unittest.TestCase):
    """ test 'Stabilizer' : 'measure'
    """

    def test_measure(self):
        """test 'measure'
        """
        sb = Stabilizer(qubit_num=4).set_all('Z').x(1).x(2)
        mval = sb.measure(qid=[0,1,2,3])
        self.assertEqual(mval, '0110')

class TestStabilizer_m(unittest.TestCase):
    """ test 'Stabilizer' : 'm'
    """

    def test_m_1(self):
        """test 'm'
        """
        sb = Stabilizer(gene_num=2, qubit_num=2)
        sb.set_all('Z')
        sb.h(0).cx(0,1)
        md = sb.m(qid=[0,1], shots=10)
        frq = md.frequency
        lst = md.last
        ans = ((lst == '00' or lst == '11') and (frq['00'] + frq['11'] == 10))
        self.assertEqual(ans, True)

    def test_m_2(self):
        """test 'm'
        """
        sb = Stabilizer(gene_num=3, qubit_num=3)
        sb.set_all('Z')
        sb.h(0).cx(0,1).cx(0,2)
        md = sb.m(qid=[0,1,2], shots=10)
        frq = md.frequency
        lst = md.last
        ans = ((lst == '000' or lst == '111') and (frq['000'] + frq['111'] == 10))
        self.assertEqual(ans, True)

class TestStabilizer_mz(unittest.TestCase):
    """ test 'Stabilizer' : 'mz'
    """

    def test_mz_1(self):
        """test 'mz'
        """
        sb = Stabilizer(gene_num=2, qubit_num=2)
        sb.set_all('Z')
        sb.h(0).cx(0,1)
        md = sb.mz(qid=[0,1], shots=10)
        frq = md.frequency
        lst = md.last
        ans = ((lst == '00' or lst == '11') and (frq['00'] + frq['11'] == 10))
        self.assertEqual(ans, True)

    def test_mz_2(self):
        """test 'mz'
        """
        sb = Stabilizer(gene_num=3, qubit_num=3)
        sb.set_all('Z')
        sb.h(0).cx(0,1).cx(0,2)
        md = sb.mz(qid=[0,1,2], shots=10)
        frq = md.frequency
        lst = md.last
        ans = ((lst == '000' or lst == '111') and (frq['000'] + frq['111'] == 10))
        self.assertEqual(ans, True)

class TestStabilizer_mx(unittest.TestCase):
    """ test 'Stabilizer' : 'mx'
    """

    def test_mx_1(self):
        """test 'mx'
        """
        sb = Stabilizer(gene_num=2, qubit_num=2)
        sb.set_all('Z')
        sb.h(0).cx(0,1)
        md = sb.mx(qid=[0,1], shots=10)
        frq = md.frequency
        lst = md.last
        ans = ((lst == '00' or lst == '11') and (frq['00'] + frq['11'] == 10))
        self.assertEqual(ans, True)

    def test_mx_2(self):
        """test 'mx'
        """
        sb = Stabilizer(gene_num=3, qubit_num=3)
        sb.set_all('Z')
        sb.h(0).cx(0,1).cx(0,2)
        md = sb.mx(qid=[0,1,2], shots=10)
        frq = md.frequency
        lst = md.last
        ans = ((lst == '000' or lst == '011' or lst == '101' or lst == '110') and
               (frq['000'] + frq['011'] + frq['101'] + frq['110'] == 10))
        self.assertEqual(ans, True)

class TestStabilizer_my(unittest.TestCase):
    """ test 'Stabilizer' : 'my'
    """

    def test_my_1(self):
        """test 'my'
        """
        sb = Stabilizer(gene_num=2, qubit_num=2)
        sb.set_all('Z')
        sb.h(0).cx(0,1)
        md = sb.my(qid=[0,1], shots=10)
        frq = md.frequency
        lst = md.last
        ans = ((lst == '01' or lst == '10') and (frq['01'] + frq['10'] == 10))
        self.assertEqual(ans, True)

    def test_my_2(self):
        """test 'my'
        """
        sb = Stabilizer(gene_num=3, qubit_num=3)
        sb.set_all('Z')
        sb.h(0).cx(0,1).cx(0,2)
        md = sb.my(qid=[0,1,2], shots=10)
        frq = md.frequency
        lst = md.last
        ans = ((lst == '000' or lst == '001' or lst == '010' or lst == '011' or
                lst == '100' or lst == '101' or lst == '110' or lst == '111') and
               (frq['000'] + frq['001'] + frq['010'] + frq['011'] +
                frq['100'] + frq['101'] + frq['110'] + frq['111'] == 10))
        self.assertEqual(ans, True)

class TestStabilizer_operate(unittest.TestCase):
    """ test 'Stabilizer' : 'operate'
    """

    def test_operate_x(self):
        """test 'operate' (x)
        """
        sb_expect = Stabilizer(gene_num=1, qubit_num=1).set_pauli_op(0,0,'Z').x(0)
        expect = sb_expect.get_str()
        pp = PauliProduct(pauli_str="X")
        sb_actual = Stabilizer(gene_num=1, qubit_num=1).set_pauli_op(0,0,'Z').operate(pp=pp)
        actual = sb_actual.get_str()
        self.assertEqual(actual, expect)
        
    def test_operate_h_x(self):
        """test 'operate' (x followed by h)
        """
        sb_expect = Stabilizer(gene_num=1, qubit_num=1).set_pauli_op(0,0,'Z').h(0).x(0)
        expect = sb_expect.get_str()
        pp = PauliProduct(pauli_str="X")
        sb_actual = Stabilizer(gene_num=1, qubit_num=1).set_pauli_op(0,0,'Z').h(0).operate(pp=pp)
        actual = sb_actual.get_str()
        self.assertEqual(actual, expect)
        
    def test_operate_h_y(self):
        """test 'operate' (Y followed by h)
        """
        sb_expect = Stabilizer(gene_num=1, qubit_num=1).set_pauli_op(0,0,'Z').h(0).y(0)
        expect = sb_expect.get_str()
        pp = PauliProduct(pauli_str="Y")
        sb_actual = Stabilizer(gene_num=1, qubit_num=1).set_pauli_op(0,0,'Z').h(0).operate(pp=pp)
        actual = sb_actual.get_str()
        self.assertEqual(actual, expect)
        
    def test_operate_h_z(self):
        """test 'operate' (Z followed by h)
        """
        sb_expect = Stabilizer(gene_num=1, qubit_num=1).set_pauli_op(0,0,'Z').h(0).z(0)
        expect = sb_expect.get_str()
        pp = PauliProduct(pauli_str="Z")
        sb_actual = Stabilizer(gene_num=1, qubit_num=1).set_pauli_op(0,0,'Z').h(0).operate(pp=pp)
        actual = sb_actual.get_str()
        self.assertEqual(actual, expect)
        
    def test_operate_xyz(self):
        """test 'operate' (xyz)
        """
        sb_expect = Stabilizer(gene_num=3, qubit_num=3).set_all('Z').x(2).y(0).z(1)
        expect = sb_expect.get_str()
        pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
        sb_actual = Stabilizer(gene_num=3, qubit_num=3).set_all('Z').operate(pp=pp)
        actual = sb_actual.get_str()
        self.assertEqual(actual, expect)
        
    def test_operate_controlled_xyz(self):
        """test 'operate' (controlled_xyz)
        """
        sb_expect = Stabilizer(gene_num=4, qubit_num=4).set_all('Z').cx(3,2).cy(3,0).cz(3,1)
        expect = sb_expect.get_str()
        pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
        sb_actual = Stabilizer(gene_num=4, qubit_num=4).set_all('Z').operate(pp=pp, qctrl=3)
        actual = sb_actual.get_str()
        self.assertEqual(actual, expect)
        
class TestStabilizer_inheritance(unittest.TestCase):
    """ test 'Stabilizer' : inheritance
    """

    def test_inheritance_1(self):
        """test 'inheritance_1'
        """
        sb_expect = Stabilizer(qubit_num=2).set_all('Z')
        sb_expect.h(0).cx(0,1).x(0)
        sb_actual = MyStabilizer(qubit_num=2).set_all('Z')
        sb_actual.bell(0,1).x(0)
        str_expect = sb_expect.get_str()
        str_actual = sb_actual.get_str()
        self.assertEqual(str_expect, str_actual)

    def test_inheritance_2(self):
        """test 'inheritance_2'
        """
        sb_expect = Stabilizer(qubit_num=2).set_all('Z')
        sb_expect.h(0).cx(0,1).x(0)
        sb_actual = MyStabilizer(qubit_num=2).set_all('Z').clone()
        sb_actual.bell(0,1).x(0)
        str_expect = sb_expect.get_str()
        str_actual = sb_actual.get_str()
        self.assertEqual(str_expect, str_actual)

    def test_inheritance_2(self):
        """test 'inheritance_2'
        """
        sb = MyStabilizer(qubit_num=2, name='hoge').set_all('Z')
        self.assertEqual(sb.get_name(), 'hoge')

if __name__ == '__main__':
    unittest.main()
