import unittest
import os
from contextlib import redirect_stdout
import datetime
from collections import Counter

from qlazy import QCirc, Backend, Result
from qlazy.config import *

class TestResult_init(unittest.TestCase):
    """ test 'Result' : '__init__'
    """

    def test_init(self):
        """test '__init__'
        """
        try:
            result = Result()
            self.assertEqual(result.backend, None)
            self.assertEqual(result.qubit_num, None)
            self.assertEqual(result.cmem_num, None)
            self.assertEqual(result.cid, None)
            self.assertEqual(result.shots, None)
            self.assertEqual(result.frequency, None)
            self.assertEqual(result.start_time, None)
            self.assertEqual(result.end_time, None)
            self.assertEqual(result.elapsed_time, None)
            self.assertEqual(result.info, None)
        except Exception:
            ans = False
        else:
            ans = True
        self.assertEqual(ans, True)

class TestResult_setter_getter(unittest.TestCase):
    """ test 'Result' : 'setter, getter'
    """

    def test_setter(self):
        """test 'setter'
        """
        try:
            result = Result()
            result.backend = Backend()
            result.qubit_num = 5
            result.cmem_num = 6
            result.cid = [0,1]
            result.shots = 100
            result.frequency = Counter()
            result.start_time = datetime.datetime.now()
            result.end_time = datetime.datetime.now()
            result.elapsed_time = 0.01
            result.info = {}
        except Exception:
            ans = False
        else:
            ans = True
        self.assertEqual(ans, True)
        
    def test_setter_getter(self):
        """test 'setter, getter' (1)
        """
        backend = Backend()
        frequency = Counter()
        frequency['00'] = 49
        frequency['11'] = 51
        start_time = datetime.datetime.now()
        end_time = datetime.datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        info = {'a': 10, 'b': 20}

        result = Result()
        result.backend = backend
        result.qubit_num = 5
        result.cmem_num = 6
        result.cid = [0,1]
        result.shots = 100
        result.frequency = frequency
        result.start_time = start_time
        result.end_time = end_time
        result.elapsed_time = elapsed_time
        result.info = info
        
        self.assertEqual(result.backend, backend)
        self.assertEqual(result.qubit_num, 5)
        self.assertEqual(result.cmem_num, 6)
        self.assertEqual(result.cid, [0,1])
        self.assertEqual(result.shots, 100)
        self.assertEqual(result.frequency, frequency)
        self.assertEqual(result.start_time, start_time)
        self.assertEqual(result.end_time, end_time)
        self.assertEqual(result.elapsed_time, elapsed_time)
        self.assertEqual(result.info, info)
        
    def test_getter(self):
        """test 'getter'
        """
        bk = Backend()
        qc = QCirc().h(0).cx(0,1).rx(1, phase=0.2).cry(0, 1, phase=0.3).measure(qid=[0,1,2], cid=[0,1,2]).x(0).z(5)
        result = bk.run(qcirc=qc, shots=100, cid=[0,1,2])
        self.assertEqual(result.backend, bk)
        self.assertEqual(result.qubit_num, 6)
        self.assertEqual(result.cmem_num, 3)
        self.assertEqual(result.cid, [0,1,2])
        self.assertEqual(result.shots, 100)
        self.assertEqual(type(result.frequency), Counter)
        self.assertEqual(type(result.start_time), datetime.datetime)
        self.assertEqual(type(result.end_time), datetime.datetime)
        self.assertEqual(type(result.elapsed_time), float)
        self.assertEqual(type(result.info), dict)
            
if __name__ == '__main__':

    unittest.main()
