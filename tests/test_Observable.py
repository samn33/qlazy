# -*- coding: utf-8 -*-
import unittest

from qlazy import PauliProduct, Observable
from qlazy.Observable import X, Y, Z

class Observable_string(unittest.TestCase):
    """ test 'Observable' : 'string'
    """

    def test_string_1(self):
        """test 'string_1'
        """
        ob = Observable(string="X_0 * X_1 * X_2 + Z_1 * Z_0")
        s = "X_0*X_1*X_2+Z_0*Z_1"
        self.assertEqual(ob.string, s)
        
    def test_string_2(self):
        """test 'string_2'
        """
        ob = Observable(string="-4.0 - 2.0 * X_0 * X_1 * X_2 + 3 * Z_1 * Z_0")
        s = "-4.0-2.0*X_0*X_1*X_2+3.0*Z_0*Z_1"
        self.assertEqual(ob.string, s)
        
    def test_string_3(self):
        """test 'string_3'
        """
        ob = Observable()
        ob.add_wpp(weight=1.0, pp=PauliProduct('XXX', [0,1,2]))
        ob.add_wpp(weight=1.0, pp=PauliProduct('ZZ', [1,0]))
        s = "X_0*X_1*X_2+Z_0*Z_1"
        self.assertEqual(ob.string, s)
        
    def test_string_4(self):
        """test 'string_4'
        """
        ob = Observable()
        ob.add_wpp(weight=-4.0)
        ob.add_wpp(weight=-2.0, pp=PauliProduct('XXX', [0,1,2]))
        ob.add_wpp(weight=3.0, pp=PauliProduct('ZZ', [1,0]))
        s = "-4.0-2.0*X_0*X_1*X_2+3.0*Z_0*Z_1"
        self.assertEqual(ob.string, s)
        
class Observable_clone(unittest.TestCase):
    """ test 'Observable' : 'clone'
    """

    def test_clone_1(self):
        """test 'string_1'
        """
        ob_1 = Observable(string="X_0 * X_1 * X_2 + Z_1 * Z_0")
        ob_2 = ob_1.clone()
        self.assertEqual(ob_1, ob_2)

    def test_clone_2(self):
        """test 'string_1'
        """
        ob_1 = Observable(string="X_0 * X_1 * X_2 + Z_1 * Z_0")
        ob_1.add_wpp(weight=2.3, pp=PauliProduct('Y', [2]))
        ob_2 = ob_1.clone()
        self.assertEqual(ob_1, ob_2)
        
class Observable_eq(unittest.TestCase):
    """ test 'Observable' : '__eq__', '__neq__'
    """

    def test_eq_1(self):
        """test 'eq_1'
        """
        ob_1 = Observable(string=" 2.0 * Z_2 * Z_3 * Z_1 - X_0 * Y_1")
        ob_2 = Observable()
        ob_2.add_wpp(weight=-1.0, pp=PauliProduct('XY', [0,1]))
        ob_2.add_wpp(weight=2.0, pp=PauliProduct('ZZZ', [2,3,1]))
        self.assertEqual(ob_1 == ob_2, True)
        self.assertEqual(ob_1 != ob_2, False)
        
class Observable_pos(unittest.TestCase):
    """ test 'Observable' : '__pos__'
    """

    def test_pos_1(self):
        """test 'pos_1'
        """
        ob_1 = Observable()
        ob_1.add_wpp(weight=1.0, pp=PauliProduct('X', [0]))
        ob_1.add_wpp(weight=1.0, pp=PauliProduct('ZZ', [0,1]))
        ob_2 = +X(0) + Z(0) * Z(1)
        self.assertEqual(ob_1, ob_2)
        
class Observable_neg(unittest.TestCase):
    """ test 'Observable' : '__neg__'
    """

    def test_neg_1(self):
        """test 'neg_1'
        """
        ob_1 = Observable()
        ob_1.add_wpp(weight=-1.0, pp=PauliProduct('X', [0]))
        ob_1.add_wpp(weight=-1.0, pp=PauliProduct('ZZ', [0,1]))
        ob_2 = -X(0) - Z(0) * Z(1)
        self.assertEqual(ob_1, ob_2)
        
class Observable_add(unittest.TestCase):
    """ test 'Observable' : '__add__', '__iadd__'
    """

    def test_add_1(self):
        """test 'add_1'
        """
        ob_1 = Observable(string=" 1.0 * Z_2 * Z_3 + 2.0 * X_0 * Y_1 - 3.0 * Z_0 * Z_1")
        ob_2 = Observable()
        ob_2.add_wpp(weight=-3.0, pp=PauliProduct('XY', [0,1]))
        ob_2.add_wpp(weight=-4.0, pp=PauliProduct('ZZ', [0,1]))
        ob_2.add_wpp(weight=-1.0, pp=PauliProduct('ZZ', [2,3]))
        ob_2.add_wpp(weight=5.0, pp=PauliProduct('ZZZ', [0,1,2]))
        ob_3 = Observable().add_wpp(-1.0, PauliProduct('XY',[0,1])).add_wpp(-7.0, PauliProduct('ZZ',[0,1]))
        ob_3.add_wpp(5.0, PauliProduct('ZZZ',[0,1,2]))
        self.assertEqual(ob_1 + ob_2, ob_3)
        
    def test_add_2(self):
        """test 'add_2'
        """
        ob_1 = Observable(string=" 1.0 * Z_2 * Z_3 + 2.0 * X_0 * Y_1 - 3.0 * Z_0 * Z_1")
        ob_2 = Observable(string=" 1.0 * Z_2 * Z_3 + 2.0 * X_0 * Y_1 - 3.0 * Z_0 * Z_1 + 333.3")
        ob_3 = ob_1 + 333.3
        self.assertEqual(ob_2, ob_3)
        
    def test_add_3(self):
        """test 'add_3'
        """
        ob_1 = Observable(string="X_0 + 0.0")
        ob_2 = Observable(string="X_0").add_wpp(weight=0.0)
        ob_3 = X(0) + 0.0
        self.assertEqual(ob_1, ob_2)
        self.assertEqual(ob_2, ob_3)

    def test_iadd_1(self):
        """test 'iadd_1'
        """
        ob_1 = Observable(string=" 1.0 * Z_2 * Z_3 + 2.0 * X_0 * Y_1 - 3.0 * Z_0 * Z_1")
        ob_2 = Observable()
        ob_2.add_wpp(weight=-3.0, pp=PauliProduct('XY', [0,1]))
        ob_2.add_wpp(weight=-4.0, pp=PauliProduct('ZZ', [0,1]))
        ob_2.add_wpp(weight=-1.0, pp=PauliProduct('ZZ', [2,3]))
        ob_2.add_wpp(weight=5.0, pp=PauliProduct('ZZZ', [0,1,2]))
        ob_3 = Observable().add_wpp(-1.0, PauliProduct('XY',[0,1])).add_wpp(-7.0, PauliProduct('ZZ',[0,1]))
        ob_3.add_wpp(5.0, PauliProduct('ZZZ',[0,1,2]))
        ob_2 += ob_1
        self.assertEqual(ob_2, ob_3)
        
    def test_iadd_2(self):
        """test 'iadd_2'
        """
        ob_1 = Observable(string=" 1.0 * Z_2 * Z_3 + 2.0 * X_0 * Y_1 - 3.0 * Z_0 * Z_1")
        ob_2 = Observable(string=" 1.0 * Z_2 * Z_3 + 2.0 * X_0 * Y_1 - 3.0 * Z_0 * Z_1 + 333.3")
        ob_1 += 333.3
        self.assertEqual(ob_1, ob_2)
        
class Observable_sub(unittest.TestCase):
    """ test 'Observable' : '__sub__', '__isub__'
    """

    def test_sub_1(self):
        """test 'sub_1'
        """
        ob_1 = Observable(string=" 1.0 * Z_2 * Z_3 + 2.0 * X_0 * Y_1 - 3.0 * Z_0 * Z_1")
        ob_2 = Observable()
        ob_2.add_wpp(weight=3.0, pp=PauliProduct('XY', [0,1]))
        ob_2.add_wpp(weight=4.0, pp=PauliProduct('ZZ', [0,1]))
        ob_2.add_wpp(weight=1.0, pp=PauliProduct('ZZ', [2,3]))
        ob_2.add_wpp(weight=-5.0, pp=PauliProduct('ZZZ', [0,1,2]))
        ob_3 = Observable().add_wpp(-1.0, PauliProduct('XY',[0,1])).add_wpp(-7.0, PauliProduct('ZZ',[0,1]))
        ob_3.add_wpp(5.0, PauliProduct('ZZZ',[0,1,2]))
        self.assertEqual(ob_1 - ob_2, ob_3)
        
    def test_sub_2(self):
        """test 'sub_2'
        """
        ob_1 = Observable(string=" 1.0 * Z_2 * Z_3 + 2.0 * X_0 * Y_1 - 3.0 * Z_0 * Z_1")
        ob_2 = Observable(string=" 1.0 * Z_2 * Z_3 + 2.0 * X_0 * Y_1 - 3.0 * Z_0 * Z_1 - 333.3")
        ob_3 = ob_1 - 333.3
        self.assertEqual(ob_2, ob_3)
        
    def test_sub_3(self):
        """test 'sub_3'
        """
        ob_1 = Observable(string=" 1.0 * Z_2 * Z_3 + 2.0 * X_0 * Y_1 - 3.0 * Z_0 * Z_1")
        ob_2 = Observable(string=" -1.0 * Z_2 * Z_3 - 2.0 * X_0 * Y_1 + 3.0 * Z_0 * Z_1 + 333.3")
        ob_3 = 333.3 - ob_1
        self.assertEqual(ob_2, ob_3)
        
    def test_sub_4(self):
        """test 'sub_4'
        """
        ob_1 = Observable(string="X_0 - 0.0")
        ob_2 = Observable(string="X_0").add_wpp(weight=-0.0)
        ob_3 = X(0) - 0.0
        self.assertEqual(ob_1, ob_2)
        self.assertEqual(ob_2, ob_3)

    def test_isub_1(self):
        """test 'isub_1'
        """
        ob_1 = Observable(string=" -1.0 * Z_2 * Z_3 - 2.0 * X_0 * Y_1 + 3.0 * Z_0 * Z_1")
        ob_2 = Observable()
        ob_2.add_wpp(weight=-3.0, pp=PauliProduct('XY', [0,1]))
        ob_2.add_wpp(weight=-4.0, pp=PauliProduct('ZZ', [0,1]))
        ob_2.add_wpp(weight=-1.0, pp=PauliProduct('ZZ', [2,3]))
        ob_2.add_wpp(weight=5.0, pp=PauliProduct('ZZZ', [0,1,2]))
        ob_3 = Observable().add_wpp(-1.0, PauliProduct('XY',[0,1])).add_wpp(-7.0, PauliProduct('ZZ',[0,1]))
        ob_3.add_wpp(5.0, PauliProduct('ZZZ',[0,1,2]))
        ob_2 -= ob_1
        self.assertEqual(ob_2, ob_3)
        
    def test_isub_2(self):
        """test 'isub_2'
        """
        ob_1 = Observable(string=" 1.0 * Z_2 * Z_3 + 2.0 * X_0 * Y_1 - 3.0 * Z_0 * Z_1")
        ob_2 = Observable(string=" 1.0 * Z_2 * Z_3 + 2.0 * X_0 * Y_1 - 3.0 * Z_0 * Z_1 - 333.3")
        ob_1 -= 333.3
        self.assertEqual(ob_1, ob_2)
        
class Observable_mul(unittest.TestCase):
    """ test 'Observable' : '__mul__', '__imul__'
    """

    def test_mul_1(self):
        """test 'mul_1'
        """
        actual = (-2.0 * X(0) + 3.0 * Z(1) * X(2)) * 2.0
        expect = Observable(string="-4.0 * X_0 + 6.0 * Z_1 * X_2")
        self.assertEqual(actual, expect)

    def test_mul_2(self):
        """test 'mul_2'
        """
        actual = 2.0 * (-2.0 * X(0) + 3.0 * Z(1) * X(2))
        expect = Observable(string="-4.0 * X_0 + 6.0 * Z_1 * X_2")
        self.assertEqual(actual, expect)

    def test_mul_3(self):
        """test 'mul_3'
        """
        actual = (-2.0 * X(0) + 3.0 * Z(1) * X(2)) * (X(0) + Z(1) * X(2))
        expect = Observable(string="X_0 * Z_1 * X_2 + 1.0")
        self.assertEqual(actual, expect)

    def test_mul_4(self):
        """test 'mul_4'
        """
        actual = X(0) * Z(0) * Z(0) * X(0)
        expect = Observable().add_wpp(weight=1.0, pp=PauliProduct('I', [0]))
        self.assertEqual(actual, expect)

    def test_mul_5(self):
        """test 'mul_5'
        """
        actual = X(0) * Z(0) * (X(0) + X(0) * Z(0)) + Y(0)
        expect = Observable("-Z_0 - 1.0 + Y_0")
        self.assertEqual(actual, expect)

    def test_imul_1(self):
        """test 'imul_1'
        """
        actual = -2.0 * X(0) + 3.0 * Z(1) * X(2)
        actual *= 2
        expect = Observable(string="-4.0 * X_0 + 6.0 * Z_1 * X_2")
        self.assertEqual(actual, expect)
        
    def test_imul_2(self):
        """test 'imul_2'
        """
        actual = Observable("2.0")
        actual *= (-2.0 * X(0) + 3.0 * Z(1) * X(2))
        expect = Observable(string="-4.0 * X_0 + 6.0 * Z_1 * X_2")
        self.assertEqual(actual, expect)
        
    def test_imul_3(self):
        """test 'imul_3'
        """
        actual = (-2.0 * X(0) + 3.0 * Z(1) * X(2))
        actual *= (X(0) + Z(1) * X(2))
        expect = Observable(string="X_0 * Z_1 * X_2 + 1.0")
        self.assertEqual(actual, expect)

class Observable_truediv(unittest.TestCase):
    """ test 'Observable' : '__truediv__', '__itruediv__'
    """

    def test_truediv_1(self):
        """test 'truediv_1'
        """
        actual = (-2.0 * X(0) + 3.0 * Z(1) * X(2)) / 2.0
        expect = Observable(string="-1.0 * X_0 + 1.5 * Z_1 * X_2")
        self.assertEqual(actual, expect)

    def test_itruediv_1(self):
        """test 'itruediv_1'
        """
        actual = (-2.0 * X(0) + 3.0 * Z(1) * X(2))
        actual /= 2.0
        expect = Observable(string="-1.0 * X_0 + 1.5 * Z_1 * X_2")
        self.assertEqual(actual, expect)

if __name__ == '__main__':
    unittest.main()
