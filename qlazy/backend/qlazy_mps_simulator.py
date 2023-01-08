# -*- coding: utf-8 -*-
""" run function for qlazy's matrix product state simulator """

import numpy as np
from collections import Counter

from qlazy.MPState import MPState
from qlazy.CMem import CMem
from qlazy.Result import Result
from qlazy.util import get_qgate_qubit_num, get_qgate_param_num, is_measurement_gate, is_reset_gate
import qlazy.config as cfg
from qlazy.lib.mpstate_func import mps_operate_qcirc

def run(qcirc=None, shots=1, cid=None, backend=None, out_state=False, max_truncation_err=cfg.EPS,
        init=None):
    """ run the quantum circuit """

    if qcirc is None:
        raise ValueError("quantum circuit must be specified.")

    qubit_num = qcirc.qubit_num
    cmem_num = qcirc.cmem_num

    if init is None:
        mps = MPState(qubit_num=qubit_num)
    else:
        if init.qubit_num < qcirc.qubit_num:
            raise ValueError("qubit number of the quantum state must be equal or larger than the quantum circuit size.")
        mps = init.clone()

    if cmem_num > 0:
        cmem = CMem(cmem_num)
    else:
        cmem = None

    if cid is None:
        cid = list(range(cmem_num))

    if cmem_num < len(cid):
        raise ValueError("length of cid must be less than classical resister size of qcirc")

    frequency = mps_operate_qcirc(mps, cmem, qcirc, shots, cid)

    result = Result()
    result.qubit_num = qubit_num
    result.cmem_num = cmem_num
    result.cid = cid
    result.shots = shots
    result.frequency = frequency
    result.backend = backend
    if out_state is True:
        result.mpstate = mps
        result.cmem = cmem
    else:
        result.mpstate = None
        result.cmem = None
    result.info = None

    return result
