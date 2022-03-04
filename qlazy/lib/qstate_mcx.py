# -*- coding: utf-8 -*-
""" multi-controlled cnot for quantum state vector """

def __gray_code(n):
    """ gray code generator """

    for k in range(2**n):
        yield k^(k>>1)

def qstate_mcx(qs, qid=None):
    """ multi-controlled cnot """

    if qid is None:
        raise ValueError("qid must be set.")

    # controled and target register
    qid_ctr = qid[:-1]
    qid_tar = qid[-1]

    # hadamard
    qs.h(qid_tar)

    # controlled-RZ(psi), psi=pi/(2**(bitnum-1))
    bitnum = len(qid_ctr)
    psi = 1.0/(2**(bitnum-1)) # unit=pi(radian)
    gray_pre = 0
    for gray in __gray_code(bitnum):
        if gray == 0:
            continue
        msb = len(str(bin(gray)))-3
        chb = len(str(bin(gray^gray_pre)))-3
        if gray != 1:
            if chb == msb:
                chb -= 1
            qs.cx(qid_ctr[chb], qid_ctr[msb])
        qs.cp(qid_ctr[msb], qid_tar, phase=psi)
        psi = -psi
        gray_pre = gray

    # hadamard
    qs.h(qid_tar)
