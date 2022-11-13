# -*- coding: utf-8 -*-
""" Quantum Circuit """
import pickle

import qlazy.config as cfg
from qlazy.QCircBase import QCircBase
from qlazy.util import get_qgate_qubit_num, get_qgate_param_num

class QCirc(QCircBase):
    """ Quantum Circuit

    Attributes
    ----------
    qubit_num : int
        qubit number of the quantum state (= log(state_num)).
    cmem_num : int
        number of the classical register.
    gate_num : int
        number of gates in the quantum circuit.
    first: object
        first gate of the quantum circuit.
    last: object
        last gate of the quantum circuit.

    """
    def __init__(self):

        super().__init__()
        self.tag_list = []
        self.fac_list = []
        self.phase_list = []
        self.gphase_list = []
        self.params = {}

    def clone(self):
        """
        clone quantum circuit.

        Parameters
        ----------
        None

        Returns
        -------
        qcirc : instance of QCirc
            quantum circuit

        """
        qcirc = super().clone()
        qcirc.tag_list = self.tag_list[:]
        qcirc.fac_list = self.fac_list[:]
        qcirc.phase_list = self.phase_list[:]
        qcirc.gphase_list = self.gphase_list[:]
        qcirc.params = dict(self.params)
        return qcirc

    def to_string(self):
        """
        get string of the circuit (qlazy format).

        Parameters
        ----------
        None

        Returns
        -------
        qcirc_str : str

        """
        qc = self.clone()
        qcirc_str = ""
        gate_cnt = 0
        while True:
            kind = qc.kind_first()
            if kind is None:
                break

            (kind, qid, para, c, ctrl) = qc.pop_gate()
            term_num = get_qgate_qubit_num(kind)
            if kind in (cfg.MEASURE, cfg.RESET):
                term_num = 1
            para_num = get_qgate_param_num(kind)

            gate_str = cfg.GATE_STRING[kind]
            qid_str = " ".join(map(str, [qid[i] for i in range(term_num)]))
            qid_str.strip()

            if para_num == 0:
                para_str = ""
            else:
                para_str = ",".join(map(str, [para[i] for i in range(para_num)]))
                para_str = "(" + para_str+ ")"

            if c is None:
                c_str = ""
            else:
                c_str = "-> {}".format(c)

            if ctrl is None:
                ctrl_str = ""
            else:
                ctrl_str = ", ctrl = {}".format(ctrl)

            if self.tag_list[gate_cnt] is not None:
                tag_str = "    #" + self.tag_list[gate_cnt]
            else:
                tag_str = ""
                
            qcirc_str += ("{0:}{2:} {1:} {3:}{4:}{5:}\n"
                          .format(gate_str, qid_str, para_str, c_str, ctrl_str, tag_str))

            gate_cnt += 1

        return qcirc_str.strip()

    def merge(self, qc):
        """
        merge two quantum circuits.

        Parameters
        ----------
        qc : instance of QCirc
            quantum circuit (merged)

        Returns
        -------
        qcirc : instance of QCirc
            new quantum circuit (merge result)

        """
        if not isinstance(qc, self.__class__):
            raise TypeError("quantum circuit is not {}.".format(self.__class__))

        qcirc = super().merge(qc)
        qcirc.tag_list = self.tag_list[:] + qc.tag_list[:]
        qcirc.fac_list = self.fac_list[:] + qc.fac_list[:]
        qcirc.phase_list = self.phase_list[:] + qc.phase_list[:]
        qcirc.gphase_list = self.gphase_list[:] + qc.gphase_list[:]
        qcirc.params = dict(self.params, **qc.params)
        return qcirc

    def merge_mutable(self, qc):
        """
        merge a quantum circuit with another one.

        Parameters
        ----------
        qc : instance of QCirc
            quantum circuit (merged)

        Returns
        -------
        None

        Notes
        -----
        This method changes original quantum circuit.

        """
        if not isinstance(qc, self.__class__):
            raise TypeError("quantum circuit is not {}.".format(self.__class__))

        super().merge_mutable(qc)
        self.tag_list.extend(qc.tag_list)
        self.fac_list.extend(qc.fac_list)
        self.phase_list.extend(qc.phase_list)
        self.gphase_list.extend(qc.gphase_list)
        self.params.update(**qc.params)

    def is_equal(self, qc):
        """
        eaual or not.

        Parameters
        ----------
        qc : instance of QCirc
            quantum circuit (merged)

        Returns
        -------
        qcirc : instance of QCirc
            quantum circuit (result)

        """
        if not isinstance(qc, self.__class__):
            raise TypeError("quantum circuit is not {}.".format(self.__class__))

        ans = False
        if super().is_equal(qc) is True:
            ans = True
        return ans

    def remap(self, qid=None, cid=None):
        """
        remap qubit id and cmem id of quantum circuit

        Parameters
        ----------
        qid : list (int)
            list of qubit id (quantum register)
        cid : list (int)
            list of cmem id (classical memory or classical register)

        Returns
        -------
        qcirc : instance of QCirc
            new quantum circuit after remapping

        Examples
        --------
        >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
        >>> qc.show()
        q[0] -H-*-M---
        q[1] ---X-|-M-
        c  =/=====v=v=
        2         0 1
        >>> qc_new1 = qc.remap(qid=[1,0], cid=[1,0])
        >>> qc_new1.show()
        q[0] ---X---M-
        q[1] -H-*-M-|-
        c  =/=====v=v=
        2         1 0
        >>> qc_new2 = qc.remap(qid=[2,1], cid=[1,0])
        >>> qc_new2.show()
        q[0] ---------
        q[1] ---X---M-
        q[2] -H-*-M-|-
        c  =/=====v=v=
        2         1 0

        Notes
        -----
        Length of the qid must be equal to qubit_num of the original quantum circut.
        Length of cid must be equal to cmem_num of the original quantum circut.
        Elements of the qid and the cid must not be duplicated. 

        """
        if qid is None and cid is None:
            return self.clone()
        elif qid is None:
            qid = list(range(self.qubit_num))
        elif cid is None:
            cid = list(range(self.cmem_num))

        # check qid

        if all([isinstance(q, int) and q>=0 for q in qid]):
            pass
        else:
            raise TypeError("qid must be a list of zero or more integer.")

        if len(qid) != self.qubit_num:
            raise ValueError("length of qid must be equal to the qubit number of the quantum circuit:{}.".format(self.qubit_num))

        if len(set(qid)) != len(qid):
            raise ValueError("elements of qid must not be duplicated.")

        # check cid

        if all([isinstance(c, int) and c>=0 for c in cid]):
            pass
        else:
            raise TypeError("cid must be a list of zero or more integer.")

        if len(cid) != self.cmem_num:
            raise ValueError("length of cid must be equal to the cmem number of the quantum circuit:{}.".fomat(self.cmem_num))

        if len(set(cid)) != len(cid):
            raise ValueError("elements of cid must not be duplicated.")

        qcirc = QCirc()

        gates = self.get_gates()
        for g in gates:
            if g['qid'] is not None:
                g['qid'] = [qid[q] for i,q in enumerate(g['qid'])]
            if g['cid'] is not None:
                g['cid'] = [cid[c] for i,c in enumerate(g['cid'])]
            if g['ctrl'] is not None:
                g['ctrl'] = cid[g['ctrl']]

        qcirc.add_gates(gates)
        qcirc.tag_list = self.tag_list[:]
        qcirc.phase_list = self.phase_list[:]
        qcirc.gphase_list = self.gphase_list[:]
        qcirc.fac_list = self.fac_list[:]
        qcirc.params = dict(self.params)
        
        return qcirc

    def dump(self, file_path):
        """
        dump the circuit

        Parameters
        ----------
        file_path: str
            file path of dump file

        Returns
        -------
        None

        """
        obj = (self.get_gates(), self.tag_list, self.phase_list, self.gphase_list, self.fac_list, self.params)
        with open(file_path, mode='wb') as f:
            pickle.dump(obj, f)

    def save(self, file_path):
        """
        save the circuit

        Parameters
        ----------
        file_path: str
            file path of dump file

        Returns
        -------
        None

        """
        self.dump(file_path)

    @classmethod
    def load(cls, file_path):
        """
        load the circuit

        Parameters
        ----------
        file_path: str
            file path of dump file

        Returns
        -------
        qcirc: instance of QCirc
            loaded circuit

        """
        with open(file_path, mode='rb') as f:
            gates, tag_list, phase_list, gphase_list, fac_list, params = pickle.load(f)
        qcirc = cls().add_gates(gates)
        qcirc.tag_list = tag_list
        qcirc.phase_list = phase_list
        qcirc.gphase_list = gphase_list
        qcirc.fac_list = fac_list
        qcirc.params = params
        return qcirc

    def append_gate(self, kind, qid, para=None, c=None, ctrl=None, tag=None, fac=1.0):
        """
        append gate to the end of the circuit.
    
        Parameters
        ----------
        kind : int
            kind of gate
        qid : list (int)
            list of qubit id
        para : list (float), default None
            list of parameters
        c : int, default None
            classical register id to store measured data
        ctrl : int, default None
            classical register id to controll the gate
        tag : str
            tag of phase parameter for parametric quantum circuit.
        fac : float
            factor of phase
    
        Returns
        -------
        None
    
        """
        super().append_gate(kind=kind, qid=qid, c=c, para=para, ctrl=ctrl)

        # phase_list
        if para is not None:
            phase = para[0]
            gphase = para[1]
        else:
            phase = 0.0
            gphase = 0.0
        self.phase_list.append(phase)
        self.gphase_list.append(gphase)
        
        # tag_lsit
        if tag is None or isinstance(tag, str):
            self.tag_list.append(tag)
        else:
            raise TypeError("tag must be str.")

        # fac_list
        if fac is None or isinstance(fac, float):
            self.fac_list.append(fac)
        else:
            raise TypeError("fac must be float.")

        # params
        if tag is not None:
            self.params[tag] = phase

    def set_params(self, params):
        """
        set parameters for each tag
    
        Parameters
        ----------
        params : dict
            tag and phase dictionary
            ex) {'tag1': phase1, 'tag2': phase2, ...}
    
        Returns
        -------
        None
    
        Examples
        --------
        >>> qc = QCirc().h(0).rz(0, tag='foo').rx(0, tag='bar')
        >>> qc.set_params(params={'foo': 0.2, 'bar': 0.4})
        >>> print(qc)
        h 0
        rz(0.2) 0
        rx(0.4) 0
        >>> qc.set_params(params={'foo': 0.3, 'bar': 0.5})
        >>> print(qc)
        h 0
        rz(0.3) 0
        rx(0.5) 0

        """
        if not isinstance(params, dict):
            raise TypeError("params must be dict.")

        if set(params.keys()) > set(self.params.keys()):
            raise ValueError("unknown tags are specified.")

        for i, tag in enumerate(self.tag_list):
            if tag in params.keys():
                self.params[tag] = params[tag]
                self.phase_list[i] = self.fac_list[i] * self.params[tag]
                if self.gphase_list[i] != 0.0: # for the p gate
                    self.gphase_list[i] = self.phase_list[i] / 2.0

        if len(self.phase_list) != self.gate_num:
            raise ValueError("phase_list length is not same as gate_num")
        
        qcirc_base_set_phase_list(self, self.phase_list)

    # add 1-qubit gate

    def rx(self, q0, phase=cfg.DEF_PHASE, ctrl=None, tag=None, fac=1.0):
        """
        add RX gate (rotation around X-axis).

        Parameters
        ----------
        q0 : int
            qubit id.
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.
        tag : str
            tag of phase parameter for parametric quantum circuit.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, -1]
        para = [phase, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_X, qid=qid, para=para, ctrl=ctrl, tag=tag, fac=fac)
        return self

    def ry(self, q0, phase=cfg.DEF_PHASE, ctrl=None, tag=None, fac=1.0):
        """
        add RY gate (rotation around Y-axis).

        Parameters
        ----------
        q0 : int
            qubit id.
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, -1]
        para = [phase, 0.0, 0.0]
        self.append_gate(kind=cfg.PHASE_SHIFT_S_, qid=qid, ctrl=ctrl)
        self.append_gate(kind=cfg.ROTATION_X, qid=qid, para=para, ctrl=ctrl, tag=tag, fac=fac)
        self.append_gate(kind=cfg.PHASE_SHIFT_S, qid=qid, ctrl=ctrl)
        return self

    def rz(self, q0, phase=cfg.DEF_PHASE, ctrl=None, tag=None, fac=1.0):
        """
        add RZ gate (rotation around Z-axis).

        Parameters
        ----------
        q0 : int
            qubit id.
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.
        tag : str
            tag of phase parameter for parametric quantum circuit.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, -1]
        para = [phase, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_Z, qid=qid, para=para, ctrl=ctrl, tag=tag, fac=fac)
        return self

    def p(self, q0, phase=cfg.DEF_PHASE, ctrl=None, tag=None, fac=1.0):
        """
        add P gate (phase shift gate).

        Parameters
        ----------
        q0 : int
            qubit id.
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.
        tag : str
            tag of phase parameter for parametric quantum circuit.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        Notes
        -----
        matrix expression is following...
        | 1.0 0.0             |
        | 0.0 exp(i*phase*PI) |

        """
        qid = [q0, -1]
        para = [phase, phase/2.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_Z, qid=qid, para=para, ctrl=ctrl, tag=tag, fac=fac)
        return self

    # add 2-qubit gate

    def cp(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None, tag=None, fac=1.0):
        """
        add CP gate (controlled P gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.
        tag : str
            tag of phase parameter for parametric quantum circuit.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, q1]
        para = [phase, 0.0, 0.0]
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=qid, para=para, ctrl=ctrl, tag=tag, fac=fac)
        para = [phase/2, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_Z, qid=qid, para=para, ctrl=ctrl, tag=tag, fac=0.5*fac)
        return self

    def crx(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None, tag=None, fac=1.0):
        """
        add CRX gate (controlled RX gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.
        tag : str
            tag of phase parameter for parametric quantum circuit.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        para = [phase, 0.0, 0.0]
        self.append_gate(kind=cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=[q0, q1], para=para, ctrl=ctrl, tag=tag, fac=fac)
        self.append_gate(kind=cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)
        return self

    def cry(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None, tag=None, fac=1.0):
        """
        add CRY gate (controlled RY gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.
        tag : str
            tag of phase parameter for parametric quantum circuit.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        # cs_dg gate
        para = [-0.5, 0.0, 0.0]
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=[q0, q1], para=para, ctrl=ctrl)
        para = [-0.25, 0.0, 0.0]
        self.append_gate(cfg.ROTATION_Z, qid=[q0, q1], para=para, ctrl=ctrl)
        para = [phase, 0.0, 0.0]
        self.append_gate(cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)
        self.append_gate(cfg.CONTROLLED_RZ, qid=[q0, q1], para=para, ctrl=ctrl, tag=tag, fac=fac)
        self.append_gate(cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)

        # cs gate
        para = [0.5, 0.0, 0.0]
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=[q0, q1], para=para, ctrl=ctrl)
        para = [0.25, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_Z, qid=[q0, q1], para=para, ctrl=ctrl)

        return self

    def crz(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None, tag=None, fac=1.0):
        """
        add CRZ gate (controlled RZ gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.
        tag : str
            tag of phase parameter for parametric quantum circuit.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, q1]
        para = [phase, 0.0, 0.0]
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=qid, para=para, ctrl=ctrl, tag=tag, fac=fac)
        return self

    def rxx(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None, tag=None, fac=1.0):
        """
        add Rxx gate (controlled RZ gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.
        tag : str
            tag of phase parameter for parametric quantum circuit.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        para=[phase, 0.0, 0.0]
        self.append_gate(kind=cfg.HADAMARD, qid=[q0, -1], ctrl=ctrl)
        self.append_gate(kind=cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        self.append_gate(kind=cfg.ROTATION_Z, qid=[q1, -1], para=para, ctrl=ctrl, tag=tag, fac=fac)
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        self.append_gate(kind=cfg.HADAMARD, qid=[q0, -1], ctrl=ctrl)
        self.append_gate(kind=cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)
        return self

    def ryy(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None, tag=None, fac=1.0):
        """
        add Ryy gate (controlled RZ gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.
        tag : str
            tag of phase parameter for parametric quantum circuit.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        para = [phase, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_X, qid=[q0, -1], para=[0.5, 0.0, 0.0], ctrl=ctrl)
        self.append_gate(kind=cfg.ROTATION_X, qid=[q1, -1], para=[0.5, 0.0, 0.0], ctrl=ctrl)
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        self.append_gate(kind=cfg.ROTATION_Z, qid=[q1, -1], para=para, ctrl=ctrl, tag=tag, fac=fac)
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        self.append_gate(kind=cfg.ROTATION_X, qid=[q0, -1], para=[-0.5, 0.0, 0.0], ctrl=ctrl)
        self.append_gate(kind=cfg.ROTATION_X, qid=[q1, -1], para=[-0.5, 0.0, 0.0], ctrl=ctrl)
        return self

    def rzz(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None, tag=None, fac=1.0):
        """
        add Rzz gate (controlled RZ gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        phase : float
            rotation angle (unit of angle is PI radian).
        ctrl : int
            address of classical memory to control gate operation.
        tag : str
            tag of phase parameter for parametric quantum circuit.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        para = [phase, 0.0, 0.0]
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        self.append_gate(kind=cfg.ROTATION_Z, qid=[q1, -1], para=para, ctrl=ctrl, tag=tag, fac=fac)
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        return self

    def add_control(self, qctrl=None):
        """
        add control qubit to quantum circuit

        Parameters
        ----------
        qctrl : int
            control qubit id

        Returns
        -------
        qc_out : instance of QCirc
            quantum circuit after adding control qubit

        """
        gates = self.get_gates()
        for g in gates:
            if qctrl in g['qid']:
                raise ValueError("qctrl={} is not allowed because it is already used.".format(qctrl))

        qc = self.clone()
        qc_out = QCirc()
        gid = 0
        while True:
            kind = qc.kind_first()
            if kind is None:
                break

            (kind, qid, para, c, ctrl) = qc.pop_gate()

            self.__add_controlled_gate(qc_out, kind, qid, para, c, ctrl, gid, qctrl)
            gid += 1
            
        return qc_out

    def __add_controlled_gate(self, qc, kind, qid, para, c, ctrl, gid, qctrl):

        # 1-qubit gate
        if kind == cfg.PAULI_X:
            qc.cx(qctrl, qid[0], ctrl=ctrl)
        elif kind == cfg.PAULI_Z:
            qc.cz(qctrl, qid[0], ctrl=ctrl)
        elif kind == cfg.HADAMARD:
            qc.ch(qctrl, qid[0], ctrl=ctrl)
        elif kind == cfg.PHASE_SHIFT_S:
            qc.cs(qctrl, qid[0], ctrl=ctrl)
        elif kind == cfg.PHASE_SHIFT_S_:
            qc.cs_dg(qctrl, qid[0], ctrl=ctrl)
        elif kind == cfg.PHASE_SHIFT_T:
            qc.ct(qctrl, qid[0], ctrl=ctrl)
        elif kind == cfg.PHASE_SHIFT_T_:
            qc.ct_dg(qctrl, qid[0], ctrl=ctrl)
        elif kind == cfg.ROTATION_X:
            qc.crx(qctrl, qid[0], phase=para[0], ctrl=ctrl, tag=self.tag_list[gid], fac=1.0)
        elif kind == cfg.ROTATION_Z:
            qc.crz(qctrl, qid[0], phase=para[0], ctrl=ctrl, tag=self.tag_list[gid], fac=1.0)
            if self.gphase_list[gid] != 0.0: # for the p gate
                qc.rz(qctrl, phase=self.gphase_list[gid])

        # 2-qubit gate
        elif kind == cfg.CONTROLLED_X:
            qc.ccx(qctrl, qid[0], qid[1], ctrl=ctrl)
        elif kind == cfg.CONTROLLED_Z:
            qc.h(qid[1], ctrl=ctrl)
            qc.ccx(qctrl, qid[0], qid[1], ctrl=ctrl)
            qc.h(qid[1], ctrl=ctrl)
        elif kind == cfg.CONTROLLED_H:
            q0, q1 = qid[0], qid[1]
            qc.cry(qctrl, q1, phase=-0.25, ctrl=ctrl).ccx(qctrl, q0, q1, ctrl=ctrl).crz(qctrl, q1, phase=-0.5, ctrl=ctrl)
            qc.ccx(qctrl, q0, q1, ctrl=ctrl).crz(qctrl, q1, phase=0.5, ctrl=ctrl).cry(qctrl, q1, phase=0.25, ctrl=ctrl)
            qc.crz(qctrl, q0, phase=0.5, ctrl=ctrl)
        elif kind == cfg.CONTROLLED_RZ:
            qc.crz(qctrl, qid[1], phase=para[0]/2.0, ctrl=ctrl, tag=self.tag_list[gid], fac=0.5)
            qc.ccx(qctrl, qid[0], qid[1], ctrl=ctrl)
            qc.crz(qctrl, qid[1], phase=-para[0]/2.0, ctrl=ctrl, tag=self.tag_list[gid], fac=-0.5)
            qc.ccx(qctrl, qid[0], qid[1], ctrl=ctrl)

        # non-unitary gate
        elif kind == cfg.MEASURE:
            qc.measure(qid=[qid[0]], cid=[c])
        elif kind == cfg.RESET:
            qc.reset(qid=[qid[0]])
        else:
            raise ValueError("not supported quantum gate.")


# c-library for qstate
from qlazy.lib.qcirc_base_c import qcirc_base_set_phase_list
