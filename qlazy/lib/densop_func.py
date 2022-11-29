# -*- coding: utf-8 -*-
""" functions for DensOp """

from qlazy.util import get_qgate_qubit_num

def densop_operate_qcirc(densop, qcirc):

    qcirc_unitary = qcirc.clone()  # suppose qcirc is unitary
        
    while True:
        kind = qcirc_unitary.kind_first()
        if kind is None:
            break
        (kind, qid, para, c, ctrl, tag) = qcirc_unitary.pop_gate()
        if ctrl is None or (ctrl is not None and cmem.bits[ctrl] == 1):
            phase = para[0] * para[2]
            if get_qgate_qubit_num(kind) == 1:
                densop.operate_gate(kind, qid[:1], phase)
            elif get_qgate_qubit_num(kind) == 2:
                densop.operate_gate(kind, qid, phase)
            else:
                raise ValueError("qubit number must be 1 or 2.")
