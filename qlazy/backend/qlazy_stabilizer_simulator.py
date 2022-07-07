# -*- coding: utf-8 -*-
""" run function for qlazy's stabilizer simulator """

from qlazy.Stabilizer import Stabilizer
from qlazy.CMem import CMem
from qlazy.Result import Result
from qlazy.lib.stabilizer_c import stabilizer_operate_qcirc

def run(qcirc=None, shots=1, cid=None, backend=None, out_state=False):
    """ run the quantum circuit """

    if qcirc is None:
        raise ValueError("quantum circuit must be specified.")

    qubit_num = qcirc.qubit_num
    cmem_num = qcirc.cmem_num
    stab = Stabilizer(qubit_num)
    stab.set_all('Z')
    if cmem_num > 0:
        cmem = CMem(cmem_num)
    else:
        cmem = None

    if cid is None:
        cid = list(range(cmem_num))

    if cmem_num < len(cid):
        raise ValueError("length of cid must be less than classical resister size of qcirc")

    qcirc_unitary, qcirc_non_unitary = qcirc.split_unitary_non_unitary()

    frequency = stabilizer_operate_qcirc(stab, cmem, qcirc_unitary, 1, cid)
    frequency = stabilizer_operate_qcirc(stab, cmem, qcirc_non_unitary, shots, cid)

    result = Result()
    result.qubit_num = qubit_num
    result.cmem_num = cmem_num
    result.cid = cid
    result.shots = shots
    result.frequency = frequency
    result.backend = backend
    if out_state is True:
        result.stabilizer = stab
        result.cmem = cmem
    else:
        result.stabilizer = None
        result.cmem = None
    result.info = None

    return result
