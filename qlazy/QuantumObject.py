# -*- coding: utf-8 -*-
""" Quantum Object """

def gray_code(n):
    """ gray code generator """

    for k in range(2**n):
        yield k^(k>>1)

class QuantumObject:

    def ccx(self, q0, q1, q2, ctrl=None):
        """
        operate CCX gate (toffoli gate, controlled controlled X gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (control qubit).
        q2 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QuantumObject

        """
        self.cxr(q1, q2, ctrl=ctrl).cx(q0, q1, ctrl=ctrl).cxr_dg(q1, q2, ctrl=ctrl).cx(q0, q1, ctrl=ctrl).cxr(q0, q2, ctrl=ctrl)
        return self

    def csw(self, q0, q1, q2, ctrl=None):
        """
        operate CSW gate (fredkin gate, controlled swap gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (swap qubit).
        q2 : int
            qubit id (swap qubit).

        Returns
        -------
        self : instance of QuantumObject

        """
        self.cx(q2, q1, ctrl=ctrl).ccx(q0, q1, q2, ctrl=ctrl).cx(q2, q1, ctrl=ctrl)
        return self

    def mcx(self, qid=None, ctrl=None):
        """
        operate MCX gate (multi-controlled X gate).
    
        Parameters
        ----------
        qid : list of int
            qubit id list [control, control, ... , control, target]
    
        Returns
        -------
        self : instance of QuantumObject
    
        """
        if qid is None:
            raise ValueError("qid must be set.")

        # controled and target register
        qid_ctr = qid[:-1]
        qid_tar = qid[-1]

        # hadamard
        self.h(qid_tar, ctrl=ctrl)

        # controlled-RZ(psi), psi=pi/(2**(bitnum-1))
        bitnum = len(qid_ctr)
        psi = 1.0/(2**(bitnum-1)) # unit=pi(radian)
        gray_pre = 0
        for gray in gray_code(bitnum):
            if gray == 0:
                continue
            msb = len(str(bin(gray)))-3
            chb = len(str(bin(gray^gray_pre)))-3
            if gray != 1:
                if chb == msb:
                    chb -= 1
                self.cx(qid_ctr[chb], qid_ctr[msb], ctrl=ctrl)
            self.cp(qid_ctr[msb], qid_tar, phase=psi, ctrl=ctrl)
            psi = -psi
            gray_pre = gray

        # hadamard
        self.h(qid_tar, ctrl=ctrl)

        return self

    def operate(self, pp=None, ctrl=None, qctrl=None):
        """
        add unitary operator.

        Parameters
        ----------
        pp : instance of PauliProduct
            pauli product to operate
        ctrl : int
            contoroll qubit id for controlled pauli product
            (this option will be removed near future)
        qctrl : int
            contoroll qubit id for controlled pauli product

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        pauli_list = pp.pauli_list
        qid = pp.qid
        factor = pp.factor

        if ctrl is None:
            ctrl = qctrl

        if ctrl is None:
            for q, pauli in zip(qid, pauli_list):
                if pauli == 'X':
                    self.x(q)
                elif pauli == 'Y':
                    self.y(q)
                elif pauli == 'Z':
                    self.z(q)
                else:
                    continue
        else:
            if ctrl in qid:
                raise ValueError("controll and target qubit id conflict")

            for q, pauli in zip(qid, pauli_list):
                if pauli == 'X':
                    self.cx(ctrl, q)
                elif pauli == 'Y':
                    self.cy(ctrl, q)
                elif pauli == 'Z':
                    self.cz(ctrl, q)
                else:
                    continue

            if factor == -1.+0.j:
                self.z(ctrl)
            elif factor == 0.+1.j:
                self.s(ctrl)
            elif factor == 0.-1.j:
                self.s_dg(ctrl)

        return self
