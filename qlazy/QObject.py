# -*- coding: utf-8 -*-
""" Quantum Object """

import qlazy.config as cfg

def gray_code(n):
    """ gray code generator """

    for k in range(2**n):
        yield k^(k>>1)

class QObject:

    # 1-qubit gate

    def x(self, q0, ctrl=None):
        """
        operate X gate.

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.PAULI_X, qid=[q0], ctrl=ctrl)
        return self

    def y(self, q0, ctrl=None):
        """
        operate Y gate.

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.PAULI_Y, qid=[q0], ctrl=ctrl)
        return self

    def z(self, q0, ctrl=None):
        """
        operate Z gate.

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.PAULI_Z, qid=[q0], ctrl=ctrl)
        return self

    def xr(self, q0, ctrl=None):
        """
        operate root X gate.

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.ROOT_PAULI_X, qid=[q0], ctrl=ctrl)
        return self

    def xr_dg(self, q0, ctrl=None):
        """
        operate root X dagger gate
        (hermmitian conjugate of root X gate).

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.ROOT_PAULI_X_, qid=[q0], ctrl=ctrl)
        return self

    def h(self, q0, ctrl=None):
        """
        operate H gate (hadamard gate).

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.HADAMARD, qid=[q0], ctrl=ctrl)
        return self

    def s(self, q0, ctrl=None):
        """
        operate S gate.

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.PHASE_SHIFT_S, qid=[q0], ctrl=ctrl)
        return self

    def s_dg(self, q0, ctrl=None):
        """
        operate S dagger gate (hermitian conjugate of S gate).

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.PHASE_SHIFT_S_, qid=[q0], ctrl=ctrl)
        return self

    def t(self, q0, ctrl=None):
        """
        operate T gate.

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.PHASE_SHIFT_T, qid=[q0], ctrl=ctrl)
        return self

    def t_dg(self, q0, ctrl=None):
        """
        operate T dagger gate (hermitian conjugate of T gate).

        Parameters
        ----------
        q0 : int
            qubit id.

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.PHASE_SHIFT_T_, qid=[q0], ctrl=ctrl)
        return self

    def rx(self, q0, phase=0.0, gphase=0.0, fac=1.0, tag=None, ctrl=None):
        """
        operate RX gate (rotation around X-axis).

        Parameters
        ----------
        q0 : int
            qubit id.
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.ROTATION_X, qid=[q0], phase=phase, gphase=gphase, fac=fac, tag=tag, ctrl=ctrl)
        return self

    def ry(self, q0, phase=0.0, gphase=0.0, fac=1.0, tag=None, ctrl=None):
        """
        operate RY gate (rotation around Y-axis).

        Parameters
        ----------
        q0 : int
            qubit id.
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.ROTATION_Y, qid=[q0], phase=phase, gphase=gphase, fac=fac, tag=tag, ctrl=ctrl)
        return self

    def rz(self, q0, phase=0.0, gphase=0.0, fac=1.0, tag=None, ctrl=None):
        """
        operate RZ gate (rotation around Z-axis).

        Parameters
        ----------
        q0 : int
            qubit id.
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.ROTATION_Z, qid=[q0], phase=phase, gphase=gphase, fac=fac, tag=tag, ctrl=ctrl)
        return self

    def p(self, q0, phase=0.0, gphase=0.0, fac=1.0, tag=None, ctrl=None):
        """
        operate P gate (phase shift gate).

        Parameters
        ----------
        q0 : int
            qubit id.
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QObject

        Notes
        -----
        matrix expression is following...
        | 1.0 0.0             |
        | 0.0 exp(i*phase*PI) |

        """
        self.operate_gate(kind=cfg.PHASE_SHIFT, qid=[q0], phase=phase, gphase=gphase, fac=fac, tag=tag, ctrl=ctrl)
        return self

    # 2-qubit gate

    def cx(self, q0, q1, ctrl=None):
        """
        operate CX gate (controlled X gate, controlled NOT gate, CNOT gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        return self

    def cy(self, q0, q1, ctrl=None):
        """
        operate CY gate (controlled X gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.CONTROLLED_Y, qid=[q0, q1], ctrl=ctrl)
        return self

    def cz(self, q0, q1, ctrl=None):
        """
        operate CZ gate (controlled Z gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.CONTROLLED_Z, qid=[q0, q1], ctrl=ctrl)
        return self

    def cxr(self, q0, q1, ctrl=None):
        """
        operate CXR gate (controlled root X gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.CONTROLLED_XR, qid=[q0, q1], ctrl=ctrl)
        return self

    def cxr_dg(self, q0, q1, ctrl=None):
        """
        operate CXR dagger gate (controlled XR dagger gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.CONTROLLED_XR_, qid=[q0, q1], ctrl=ctrl)
        return self

    def ch(self, q0, q1, ctrl=None):
        """
        operate CH gate (controlled H gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.CONTROLLED_H, qid=[q0, q1], ctrl=ctrl)
        return self

    def cs(self, q0, q1, ctrl=None):
        """
        operate CS gate (controlled S gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.CONTROLLED_S, qid=[q0, q1], ctrl=ctrl)
        return self

    def cs_dg(self, q0, q1, ctrl=None):
        """
        operate CS dagger gate (controlled S dagger gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.CONTROLLED_S_, qid=[q0, q1], ctrl=ctrl)
        return self

    def ct(self, q0, q1, ctrl=None):
        """
        operate CT gate (controlled T gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.CONTROLLED_T, qid=[q0, q1], ctrl=ctrl)
        return self

    def ct_dg(self, q0, q1, ctrl=None):
        """
        operate CT dagger gate (controlled T dagger gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.CONTROLLED_T_, qid=[q0, q1], ctrl=ctrl)
        return self

    def sw(self, q0, q1, ctrl=None):
        """
        swap gate

        Parameters
        ----------
        q0 : int
            qubit id
        q1 : int
            qubit id

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.SWAP_QUBITS, qid=[q0, q1], ctrl=ctrl)
        return self

    def cp(self, q0, q1, phase=0.0, gphase=0.0, fac=1.0, tag=None, ctrl=None):
        """
        operate CP gate (controlled P gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.CONTROLLED_P, qid=[q0, q1], phase=phase, gphase=gphase, fac=fac, tag=tag, ctrl=ctrl)
        return self

    def crx(self, q0, q1, phase=0.0, gphase=0.0, fac=1.0, tag=None, ctrl=None):
        """
        operate CRX gate (controlled RX gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.CONTROLLED_RX, qid=[q0, q1], phase=phase, gphase=gphase, fac=fac, tag=tag, ctrl=ctrl)
        return self

    def cry(self, q0, q1, phase=0.0, gphase=0.0, fac=1.0, tag=None, ctrl=None):
        """
        operate CRY gate (controlled RY gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.CONTROLLED_RY, qid=[q0, q1], phase=phase, gphase=gphase, fac=fac, tag=tag, ctrl=ctrl)
        return self

    def crz(self, q0, q1, phase=0.0, gphase=0.0, fac=1.0, tag=None, ctrl=None):
        """
        operate CRZ gate (controlled RZ gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.CONTROLLED_RZ, qid=[q0, q1], phase=phase, gphase=gphase, fac=fac, tag=tag, ctrl=ctrl)
        return self

    def rxx(self, q0, q1, phase=0.0, gphase=0.0, fac=1.0, tag=None, ctrl=None):
        """
        operate Rxx gate.

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.ROTATION_XX, qid=[q0, q1], phase=phase, gphase=gphase, fac=fac, tag=tag, ctrl=ctrl)
        return self

    def ryy(self, q0, q1, phase=0.0, gphase=0.0, fac=1.0, tag=None, ctrl=None):
        """
        operate Ryy gate.

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.ROTATION_YY, qid=[q0, q1], phase=phase, gphase=gphase, fac=fac, tag=tag, ctrl=ctrl)
        return self

    def rzz(self, q0, q1, phase=0.0, gphase=0.0, fac=1.0, tag=None, ctrl=None):
        """
        operate Rxx gate.

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).

        Returns
        -------
        self : instance of QObject

        """
        self.operate_gate(kind=cfg.ROTATION_ZZ, qid=[q0, q1], phase=phase, gphase=gphase, fac=fac, tag=tag, ctrl=ctrl)
        return self

    # 3-qubit gate

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
        self : instance of QObject

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
        self : instance of QObject

        """
        self.cx(q2, q1, ctrl=ctrl).ccx(q0, q1, q2, ctrl=ctrl).cx(q2, q1, ctrl=ctrl)
        return self

    # n-qubit gate

    def mcx(self, qid=None, ctrl=None):
        """
        operate MCX gate (multi-controlled X gate).
    
        Parameters
        ----------
        qid : list of int
            qubit id list [control, control, ... , control, target]
    
        Returns
        -------
        self : instance of QObject
    
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

    def qft(self, qid):
        """
        Quantum Fourier Transform
    
        Parameters
        ----------
        qid : list of int
            qubit id list
    
        Returns
        -------
        self : instance of QObject
    
        """
        qubit_num = len(qid)
        for i in range(qubit_num):
            self.h(qid[qubit_num-i-1])
            phase = 1.0
            for j in range(qubit_num-i-1):
                phase /= 2.0
                self.cp(qid[qubit_num-i-j-2], qid[qubit_num-i-1], phase=phase)

        return self

    def iqft(self, qid):
        """
        Inverse Quantum Fourier Transform
    
        Parameters
        ----------
        qid : list of int
            qubit id list
    
        Returns
        -------
        self : instance of QObject
    
        """
        qubit_num = len(qid)
        for i in range(qubit_num):
            phase = -1.0/2**i
            for j in range(i):
                self.cp(qid[j], qid[i], phase=phase)
                phase *= 2.0
            self.h(qid[i])

        return self

    # operate pauli product

    def operate_pp(self, pp=None, ctrl=None, qctrl=None):
        """
        operate pauli product.

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

    def operate(self, pp=None, ctrl=None, qctrl=None):
        """ operate pauli product. """

        return self.operate_pp(pp=pp, ctrl=ctrl, qctrl=qctrl)

    # reset

    def reset(self, qid=None):
        """
        reset to |00..0> state.

        Parameters
        ----------
        qid : list, default - qubit id's list for all of the qubits
            qubit id's list to reset.

        Returns
        -------
        self : instance of QObject
            quantum state.

        Notes
        -----
        If 'qid' is set, specified qubits are reset after
        measurement. So if the specified qubits are entangled with the
        remaining qubits, output quantum state is probabilistic. If no
        qubits are set, all qubits are zero reset.

        """
        self.operate_gate(kind=cfg.RESET, qid=qid)
        return self

    # measure

    def measure(self, qid, cid):
        """
        add measurement gate (Z-basis).

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.
        cid : list of int
            classical register id list to store measured result.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.operate_gate(kind=cfg.MEASURE, qid=qid, cid=cid)
        return self

