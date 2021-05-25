# -*- coding: utf-8 -*-
from qlazy.error import *
from qlazy.config import *
from qlazy.util import *

# multi-controlled X gate

def __gray_code(de, n):

    for k in range(2**n):
        yield k^(k>>1)

def densop_mcx(de,qid=[]):

    # controled and target register
    qid_ctr = qid[:-1]
    qid_tar = qid[-1]
        
    # hadamard
    de.h(qid_tar)

    # controlled-RZ(psi), psi=pi/(2**(bitnum-1))
    bitnum = len(qid_ctr)
    psi = 1.0/(2**(bitnum-1)) # unit=pi(radian)
    gray_pre = 0
    for gray in __gray_code(de, bitnum):
        if gray == 0:
            continue
        msb = len(str(bin(gray)))-3
        chb = len(str(bin(gray^gray_pre)))-3
        if gray != 1:
            if chb == msb:
                chb -= 1
            de.cx(qid_ctr[chb], qid_ctr[msb])
        de.cp(qid_ctr[msb], qid_tar, phase=psi)
        psi = -psi
        gray_pre = gray
    
    # hadamard
    de.h(qid_tar)
