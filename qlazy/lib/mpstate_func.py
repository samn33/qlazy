# -*- coding: utf-8 -*-
""" functions for MPState """

import numpy as np
from collections import Counter

from qlazy.util import get_qgate_qubit_num, is_measurement_gate, is_reset_gate
import qlazy.config as cfg

def mps_operate_qcirc(mps, cmem, qcirc, shots, cid):

    qcirc_unitary, qcirc_non_unitary = qcirc.split_unitary_non_unitary()

    # unitary part
    while True:
        kind = qcirc_unitary.kind_first()
        if kind is None:
            break
        (kind, qid, para, c, ctrl, tag) = qcirc_unitary.pop_gate()
        if ctrl is None or (ctrl is not None and cmem.bits[ctrl] == 1):
            phase = para[0] * para[2]
            if get_qgate_qubit_num(kind) == 1:
                mps.operate_1qubit_gate(cfg.GATE_STRING[kind], qid[0], phase)
            elif get_qgate_qubit_num(kind) == 2:
                mps.operate_2qubit_gate(cfg.GATE_STRING[kind], qid[0], qid[1], phase)
            else:
                raise ValueError("invalid gate description: {}".format(kind, qid, para, c, ctrl))
    
    # non-unitary part
    if qcirc_non_unitary.kind_first() is None: # non-unitary part includes no gates
        frequency = None
    
    elif qcirc_non_unitary.all_gates_measurement() is True: # non-unitary part includes measurements only
        q_list = []
        c_list = []
        bits_array = np.array([0] * cmem.cmem_num)
        while True:
            kind = qcirc_non_unitary.kind_first()
            if kind is None:
                break
            (kind, qid, para, c, ctrl, tag) = qcirc_non_unitary.pop_gate()
            if ctrl is None or (ctrl is not None and cmem.bits[ctrl] == 1):
                q_list.append(qid[0])
                c_list.append(c)

        md = mps.m(qid=q_list, shots=shots)
        frequency = Counter()
        for k, v in md.frequency.items():
            m_list = list(map(int, list(k)))
            b_list = [0] * cmem.cmem_num
            for i, q in enumerate(q_list):
                b_list[c_list[i]] = m_list[i]
            b_list = [b_list[c] for c in cid]
            bits = "".join(map(str, b_list))
            frequency[bits] = v

    else:
        frequency = Counter()
        for n in range(shots):
            qc_tmp = qcirc_non_unitary.clone()
            if n == shots - 1:
                mps_tmp = mps
            else:
                mps_tmp = mps.clone()
            b_list = [0] * cmem.cmem_num
            while True:
                kind = qc_tmp.kind_first()
                if kind is None:
                    break
                (kind, qid, para, c, ctrl, tag) = qc_tmp.pop_gate()
                if ctrl is None or (ctrl is not None and cmem.bits[ctrl] == 1):
                    phase = para[0]
                    if is_measurement_gate(kind) is True:
                        mval = int(mps_tmp.measure(qid=[qid[0]]))
                        b_list[c] = mval
                        cmem.set_bits(b_list)
                    elif is_reset_gate(kind) is True:
                        mps_tmp.reset(qid=[qid[0]])
                    elif get_qgate_qubit_num(kind) == 1:
                        mps_tmp.operate_1qubit_gate(cfg.GATE_STRING[kind], qid[0], phase)
                    elif get_qgate_qubit_num(kind) == 2:
                        mps_tmp.operate_2qubit_gate(cfg.GATE_STRING[kind], qid[0], qid[1], phase)
                    else:
                        raise ValueError("invalid gate description: {}".format(kind, qid, para, c, ctrl))

            b_list = [b_list[c] for c in cid]
            bits = "".join(map(str, b_list))
            frequency[bits] += 1
        
    return frequency
