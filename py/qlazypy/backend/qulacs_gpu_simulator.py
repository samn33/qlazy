# -*- coding: utf-8 -*-
from qulacs import QuantumStateGpu
from qlazypy.backend.qulacs_simulator import run, reset, free

def init(qubit_num=0, backend=None):

    qstate = QuantumStateGpu(qubit_num)
    return qstate
