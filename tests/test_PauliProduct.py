import unittest

from qlazy import PauliProduct

def equal_list(list_0, list_1):

    return list_0 == list_1

class TestPauliProduct_init(unittest.TestCase):
    """ test 'PauliProduct' : '__init__'
    """

    def test_init_I(self):
        """test '__init__' (pauli_str="I")
        """
        pp = PauliProduct(pauli_str="I")
        ans = equal_list(pp.pauli_list, ['I']) and equal_list(pp.qid, [0])
        self.assertEqual(ans, True)

    def test_init_X(self):
        """test '__init__' (pauli_str="X")
        """
        pp = PauliProduct(pauli_str="X")
        ans = equal_list(pp.pauli_list, ['X']) and equal_list(pp.qid, [0])
        self.assertEqual(ans, True)

    def test_init_X_qid(self):
        """test '__init__' (pauli_str="X", qid=[1])
        """
        pp = PauliProduct(pauli_str="X", qid=[1])
        ans = equal_list(pp.pauli_list, ['X']) and equal_list(pp.qid, [1])
        self.assertEqual(ans, True)

    def test_init_XZ(self):
        """test '__init__' (pauli_str="XZ")
        """
        pp = PauliProduct(pauli_str="XZ")
        ans = equal_list(pp.pauli_list, ['X','Z']) and equal_list(pp.qid, [0,1])
        self.assertEqual(ans, True)

    def test_init_XZ_qid(self):
        """test '__init__' (pauli_str="XZ", qid=[3,1])
        """
        pp = PauliProduct(pauli_str="XZ", qid=[3,1])
        ans = equal_list(pp.pauli_list, ['Z','X']) and equal_list(pp.qid, [1,3])
        self.assertEqual(ans, True)

    def test_init_XZZIX_qid(self):
        """test '__init__' (pauli_str="XZZIX", qid=[3,1,4,10,5])
        """
        pp = PauliProduct(pauli_str="XZZIX", qid=[3,1,4,10,5])
        ans = equal_list(pp.pauli_list, ['Z','X','Z','X']) and equal_list(pp.qid, [1,3,4,5])
        self.assertEqual(ans, True)

class TestPauliProduct_init(unittest.TestCase):
    """ test 'PauliProduct' : '__init__'
    """

    def test_print(self):
        """test '__str__' (pauli_str="XZZIX", qid=[3,1,4,10,5])
        """
        pp = PauliProduct(pauli_str="XZZIX", qid=[3,1,4,10,5])
        self.assertEqual(pp.__str__(), "Z(1) X(3) Z(4) X(5)")

class TestPauliProduct_is_commute(unittest.TestCase):
    """ test 'PauliProduct' : 'is_commute'
    """

    def test_is_commute_0(self):
        """test 'is_commute' ("I", "XYZ") => commute
        """
        pp_0 = PauliProduct(pauli_str="I")
        pp_1 = PauliProduct(pauli_str="XYZ", qid=[3,2,1])
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans, True)
        
    def test_is_commute_1(self):
        """test 'is_commute' ("XYZ", "XYZ") => commute
        """
        pp_0 = PauliProduct(pauli_str="XYZ")
        pp_1 = PauliProduct(pauli_str="XYZ")
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans, True)
        
    def test_is_commute_2(self):
        """test 'is_commute' ("XYZ", "Z") => anti-commute
        """
        pp_0 = PauliProduct(pauli_str="XYZ", qid=[2,1,0])
        pp_1 = PauliProduct(pauli_str="Z", qid=[1])
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans, False)
        
    def test_is_commute_3(self):
        """test 'is_commute' ("XYZ", "Z") => anti-commute
        """
        pp_0 = PauliProduct(pauli_str="XYZ", qid=[2,1,0])
        pp_1 = PauliProduct(pauli_str="ZX", qid=[7,0])
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans, False)
        
    def test_is_commute_4(self):
        """test 'is_commute' ("XYZ", "Z") => commute
        """
        pp_0 = PauliProduct(pauli_str="XYZ", qid=[2,1,0])
        pp_1 = PauliProduct(pauli_str="ZX", qid=[7,10])
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans, True)
        
class TestPauliProduct_tenspro(unittest.TestCase):
    """ test 'PauliProduct' : 'tenspro'
    """

    def test_tenspro_0(self):
        """test 'is_commute' ("I", "XYZ") => commute
        """
        pp_0 = PauliProduct(pauli_str="I")
        pp_1 = PauliProduct(pauli_str="XYZ", qid=[3,2,1])
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans, True)
        
    def test_is_commute_1(self):
        """test 'is_commute' ("XYZ", "XYZ") => commute
        """
        pp_0 = PauliProduct(pauli_str="XYZ")
        pp_1 = PauliProduct(pauli_str="XYZ")
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans, True)
        
    def test_is_commute_2(self):
        """test 'is_commute' ("XYZ", "Z") => anti-commute
        """
        pp_0 = PauliProduct(pauli_str="XYZ", qid=[2,1,0])
        pp_1 = PauliProduct(pauli_str="Z", qid=[1])
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans, False)
        
    def test_is_commute_3(self):
        """test 'is_commute' ("XYZ", "Z") => anti-commute
        """
        pp_0 = PauliProduct(pauli_str="XYZ", qid=[2,1,0])
        pp_1 = PauliProduct(pauli_str="ZX", qid=[7,0])
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans, False)
        
    def test_is_commute_4(self):
        """test 'is_commute' ("XYZ", "Z") => commute
        """
        pp_0 = PauliProduct(pauli_str="XYZ", qid=[2,1,0])
        pp_1 = PauliProduct(pauli_str="ZX", qid=[7,10])
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans, True)
        
class TestPauliProduct_mul(unittest.TestCase):
    """ test 'PauliProduct' : '__mul__'
    """

    def test_mul_1(self):
        """test 'mul_1'
        """
        pp_1 = PauliProduct(pauli_str='XYZ', qid=[0,1,2])
        pp_2 = PauliProduct(pauli_str='XYZ', qid=[0,1,2])
        actual = pp_1 * pp_2
        expect = PauliProduct(pauli_str='I', qid=[0])
        self.assertEqual(actual, expect)
        
    def test_mul_2(self):
        """test 'mul_2'
        """
        pp_1 = PauliProduct(pauli_str='XXZ', qid=[0,1,2])
        pp_2 = PauliProduct(pauli_str='XYZ', qid=[0,1,2])
        actual = pp_1 * pp_2
        expect = PauliProduct(pauli_str='Z', qid=[1], factor=1.j)
        self.assertEqual(actual, expect)
        
    def test_mul_3(self):
        """test 'mul_3'
        """
        pp_1 = PauliProduct(pauli_str='XXZ', qid=[0,1,2])
        pp_2 = PauliProduct(pauli_str='XZZ', qid=[0,1,2])
        actual = pp_1 * pp_2
        expect = PauliProduct(pauli_str='Y', qid=[1], factor=-1.j)
        self.assertEqual(actual, expect)
        
    def test_mul_4(self):
        """test 'mul_4'
        """
        pp_1 = PauliProduct(pauli_str='XYZ', qid=[0,1,2])
        pp_2 = PauliProduct(pauli_str='XXZ', qid=[0,1,2])
        actual = pp_1 * pp_2
        expect = PauliProduct(pauli_str='Z', qid=[1], factor=-1.j)
        self.assertEqual(actual, expect)
        
    def test_mul_5(self):
        """test 'mul_5'
        """
        pp_1 = PauliProduct(pauli_str='XYZ', qid=[0,1,2])
        pp_2 = PauliProduct(pauli_str='XZZ', qid=[0,1,2])
        actual = pp_1 * pp_2
        expect = PauliProduct(pauli_str='X', qid=[1], factor=1.j)
        self.assertEqual(actual, expect)
        
    def test_mul_6(self):
        """test 'mul_6'
        """
        pp_1 = PauliProduct(pauli_str='XZZ', qid=[0,1,2])
        pp_2 = PauliProduct(pauli_str='XXZ', qid=[0,1,2])
        actual = pp_1 * pp_2
        expect = PauliProduct(pauli_str='Y', qid=[1], factor=1.j)
        self.assertEqual(actual, expect)
        
    def test_mul_7(self):
        """test 'mul_7'
        """
        pp_1 = PauliProduct(pauli_str='XZZ', qid=[0,1,2])
        pp_2 = PauliProduct(pauli_str='XYZ', qid=[0,1,2])
        actual = pp_1 * pp_2
        expect = PauliProduct(pauli_str='X', qid=[1], factor=-1.j)
        self.assertEqual(actual, expect)
        
    def test_mul_8(self):
        """test 'mul_8'
        """
        pp_1 = PauliProduct(pauli_str='XYZ', qid=[0,1,2])
        pp_2 = PauliProduct(pauli_str='ZYX', qid=[2,1,0])
        actual = pp_1 * pp_2
        expect = PauliProduct(pauli_str='I', qid=[0])
        self.assertEqual(actual, expect)
        
    def test_mul_9(self):
        """test 'mul_9'
        """
        pp_1 = PauliProduct(pauli_str='XZ', qid=[0,1], factor=-1)
        pp_2 = PauliProduct(pauli_str='XZYZ', qid=[2,1,3,4], factor=-1.j)
        actual = pp_1 * pp_2
        expect = PauliProduct(pauli_str='XXYZ', qid=[0,2,3,4], factor=1.j)
        self.assertEqual(actual, expect)
        
    def test_mul_10(self):
        """test 'mul_10'
        """
        pp_1 = PauliProduct(pauli_str='XZ', qid=[0,1], factor=-1)
        pp_2 = PauliProduct(pauli_str='XZ', qid=[1,2], factor=-1.j)
        actual = pp_1 * pp_2
        expect = PauliProduct(pauli_str='XYZ', qid=[0,1,2], factor=-1)
        self.assertEqual(actual, expect)

    def test_mul_11(self):
        """test 'mul_11'
        """
        pp_1 = PauliProduct(pauli_str='XZY', qid=[0,1,2], factor=-1)
        pp_2 = PauliProduct(pauli_str='XZ', qid=[1,2], factor=-1.j)
        actual = pp_1 * pp_2
        expect = PauliProduct(pauli_str='XYX', qid=[0,1,2], factor=-1.j)
        self.assertEqual(actual, expect)

if __name__ == '__main__':

    unittest.main()
