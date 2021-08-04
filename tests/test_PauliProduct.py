import unittest

from qlazy import PauliProduct

# def operate(self, pauli_product=None, ctrl=None):
#     """
#     operate pauli product to quantum state.
# 
#     Parameters
#     ----------
#     pauli_product : instance of PauliProduct
#         pauli product to operate
#     ctrl : int
#         contoroll qubit id for controlled pauli product
# 
#     Returns
#     -------
#     self : instance of QState
#         quantum state after operation
# 
#     """
#     pauli_list = pauli_product.pauli_list
#     qid = pauli_product.qid
#     
#     if ctrl is None:
#         for q, pauli in zip(qid, pauli_list):
#             if pauli == 'X':
#                 self.x(q)
#             elif pauli == 'Y':
#                 self.y(q)
#             elif pauli == 'Z':
#                 self.z(q)
#             else:
#                 continue
#     else:
#         if ctrl in qid:
#             raise ValueError("controll and target qubit id conflict")
#         
#         for q, pauli in zip(qid, pauli_list):
#             if pauli == 'X':
#                 self.cx(ctrl, q)
#             elif pauli == 'Y':
#                 self.cy(ctrl, q)
#             elif pauli == 'Z':
#                 self.cz(ctrl, q)
#             else:
#                 continue
#     
#     return self
# 
# QState.add_method(operate)

def equal_list(list_0, list_1):

    if len(list_0) != len(list_1):
        return False
    else:
        for l_0, l_1 in zip(list_0, list_1):
            if l_0 != l_1:
                return False
    return True



class TestPauliProduct_init(unittest.TestCase):
    """ test 'PauliProduct' : '__init__'
    """

    def test_init_I(self):
        """test '__init__' (pauli_str="I")
        """
        pp = PauliProduct(pauli_str="I")
        ans = equal_list(pp.pauli_list, ['I']) and equal_list(pp.qid, [0])
        self.assertEqual(ans,True)

    def test_init_X(self):
        """test '__init__' (pauli_str="X")
        """
        pp = PauliProduct(pauli_str="X")
        ans = equal_list(pp.pauli_list, ['X']) and equal_list(pp.qid, [0])
        self.assertEqual(ans,True)

    def test_init_X_qid(self):
        """test '__init__' (pauli_str="X", qid=[1])
        """
        pp = PauliProduct(pauli_str="X", qid=[1])
        ans = equal_list(pp.pauli_list, ['X']) and equal_list(pp.qid, [1])
        self.assertEqual(ans,True)

    def test_init_XZ(self):
        """test '__init__' (pauli_str="XZ")
        """
        pp = PauliProduct(pauli_str="XZ")
        ans = equal_list(pp.pauli_list, ['X','Z']) and equal_list(pp.qid, [0,1])
        self.assertEqual(ans,True)

    def test_init_XZ_qid(self):
        """test '__init__' (pauli_str="XZ", qid=[3,1])
        """
        pp = PauliProduct(pauli_str="XZ", qid=[3,1])
        ans = equal_list(pp.pauli_list, ['Z','X']) and equal_list(pp.qid, [1,3])
        self.assertEqual(ans,True)

    def test_init_XZZIX_qid(self):
        """test '__init__' (pauli_str="XZZIX", qid=[3,1,4,10,5])
        """
        pp = PauliProduct(pauli_str="XZZIX", qid=[3,1,4,10,5])
        ans = equal_list(pp.pauli_list, ['Z','X','Z','X']) and equal_list(pp.qid, [1,3,4,5])
        self.assertEqual(ans,True)

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
        self.assertEqual(ans,True)
        
    def test_is_commute_1(self):
        """test 'is_commute' ("XYZ", "XYZ") => commute
        """
        pp_0 = PauliProduct(pauli_str="XYZ")
        pp_1 = PauliProduct(pauli_str="XYZ")
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans,True)
        
    def test_is_commute_2(self):
        """test 'is_commute' ("XYZ", "Z") => anti-commute
        """
        pp_0 = PauliProduct(pauli_str="XYZ", qid=[2,1,0])
        pp_1 = PauliProduct(pauli_str="Z", qid=[1])
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans,False)
        
    def test_is_commute_3(self):
        """test 'is_commute' ("XYZ", "Z") => anti-commute
        """
        pp_0 = PauliProduct(pauli_str="XYZ", qid=[2,1,0])
        pp_1 = PauliProduct(pauli_str="ZX", qid=[7,0])
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans,False)
        
    def test_is_commute_4(self):
        """test 'is_commute' ("XYZ", "Z") => commute
        """
        pp_0 = PauliProduct(pauli_str="XYZ", qid=[2,1,0])
        pp_1 = PauliProduct(pauli_str="ZX", qid=[7,10])
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans,True)
        
class TestPauliProduct_tenspro(unittest.TestCase):
    """ test 'PauliProduct' : 'tenspro'
    """

    def test_tenspro_0(self):
        """test 'is_commute' ("I", "XYZ") => commute
        """
        pp_0 = PauliProduct(pauli_str="I")
        pp_1 = PauliProduct(pauli_str="XYZ", qid=[3,2,1])
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans,True)
        
    def test_is_commute_1(self):
        """test 'is_commute' ("XYZ", "XYZ") => commute
        """
        pp_0 = PauliProduct(pauli_str="XYZ")
        pp_1 = PauliProduct(pauli_str="XYZ")
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans,True)
        
    def test_is_commute_2(self):
        """test 'is_commute' ("XYZ", "Z") => anti-commute
        """
        pp_0 = PauliProduct(pauli_str="XYZ", qid=[2,1,0])
        pp_1 = PauliProduct(pauli_str="Z", qid=[1])
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans,False)
        
    def test_is_commute_3(self):
        """test 'is_commute' ("XYZ", "Z") => anti-commute
        """
        pp_0 = PauliProduct(pauli_str="XYZ", qid=[2,1,0])
        pp_1 = PauliProduct(pauli_str="ZX", qid=[7,0])
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans,False)
        
    def test_is_commute_4(self):
        """test 'is_commute' ("XYZ", "Z") => commute
        """
        pp_0 = PauliProduct(pauli_str="XYZ", qid=[2,1,0])
        pp_1 = PauliProduct(pauli_str="ZX", qid=[7,10])
        ans = pp_0.is_commute(pp_1)
        self.assertEqual(ans,True)

# class TestQState_operate(unittest.TestCase):
#     """ test 'QState' : 'operate'
#     """
# 
#     def test_operate_x(self):
#         """test 'operate' (x)
#         """
#         qs_expect = QState(qubit_num=1)
#         qs_actual = QState(qubit_num=1)
#         pp = PauliProduct(pauli_str="X")
#         qs_expect.x(0)
#         qs_actual.operate(pauli_product=pp)
#         ans = equal_qstates(qs_expect, qs_actual)
#         self.assertEqual(ans,True)
# 
#         QState.free_all(qs_expect, qs_actual)
#         
#     def test_operate_h_x(self):
#         """test 'operate' (x followed by h)
#         """
#         qs_expect = QState(qubit_num=1).h(0)
#         qs_actual = QState(qubit_num=1).h(0)
#         pp = PauliProduct(pauli_str="X")
#         qs_expect.x(0)
#         qs_actual.operate(pauli_product=pp)
#         ans = equal_qstates(qs_expect, qs_actual)
#         self.assertEqual(ans,True)
# 
#         QState.free_all(qs_expect, qs_actual)
#         
#     def test_operate_h_y(self):
#         """test 'operate' (y followed by h)
#         """
#         qs_expect = QState(qubit_num=1).h(0)
#         qs_actual = QState(qubit_num=1).h(0)
#         pp = PauliProduct(pauli_str="Y")
#         qs_expect.y(0)
#         qs_actual.operate(pauli_product=pp)
#         ans = equal_qstates(qs_expect, qs_actual)
#         self.assertEqual(ans,True)
# 
#         QState.free_all(qs_expect, qs_actual)
#         
#     def test_operate_h_z(self):
#         """test 'operate' (z followed by h)
#         """
#         qs_expect = QState(qubit_num=1).h(0)
#         qs_actual = QState(qubit_num=1).h(0)
#         pp = PauliProduct(pauli_str="Z")
#         qs_expect.z(0)
#         qs_actual.operate(pauli_product=pp)
#         ans = equal_qstates(qs_expect, qs_actual)
#         self.assertEqual(ans,True)
# 
#         QState.free_all(qs_expect, qs_actual)
#         
#     def test_operate_xyz(self):
#         """test 'operate' (xyz)
#         """
#         qs_expect = QState(qubit_num=3)
#         qs_actual = QState(qubit_num=3)
#         pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
#         qs_expect.x(2).y(0).z(1)
#         qs_actual.operate(pauli_product=pp)
#         ans = equal_qstates(qs_expect, qs_actual)
#         self.assertEqual(ans,True)
# 
#         QState.free_all(qs_expect, qs_actual)
#         
#     def test_operate_controlled_xyz(self):
#         """test 'operate' (controlled_xyz)
#         """
#         qs_expect = QState(qubit_num=4)
#         qs_actual = QState(qubit_num=4)
#         pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
#         qs_expect.cx(3,2).cy(3,0).cz(3,1)
#         qs_actual.operate(pauli_product=pp, ctrl=3)
#         ans = equal_qstates(qs_expect, qs_actual)
#         self.assertEqual(ans,True)
# 
#         QState.free_all(qs_expect, qs_actual)
        
if __name__ == '__main__':

    unittest.main()
