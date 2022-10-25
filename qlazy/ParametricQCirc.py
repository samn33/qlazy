# -*- coding: utf-8 -*-
""" Quantum Circuit """

import qlazy.config as cfg
from qlazy.QCirc import QCirc
from qlazy.util import get_qgate_qubit_num, get_qgate_param_num

class ParametricQCirc(QCirc):
    """ Parametric Quantum Circuit

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
        merge quantum circuit.

        Parameters
        ----------
        qc : instance of QCirc
            quantum circuit (merged)

        Returns
        -------
        qcirc : instance of QCirc
            quantum circuit (result)

        """
        # if not isinstance(qc, ParametricQCirc):
        if not isinstance(qc, self.__class__):
            raise TypeError("quantum circuit is not {}.".format(self.__class__))

        qcirc = super().merge(qc)
        qcirc.tag_list = self.tag_list[:] + qc.tag_list[:]
        qcirc.fac_list = self.fac_list[:] + qc.fac_list[:]
        qcirc.phase_list = self.phase_list[:] + qc.phase_list[:]
        qcirc.params = dict(self.params, **qc.params)
        return qcirc

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
        # if not isinstance(qc, ParametricQCirc):
        if not isinstance(qc, self.__class__):
            raise TypeError("quantum circuit is not {}.".format(self.__class__))

        ans = False
        if super().is_equal(qc) is True:
            if self.tag_list == qc.tag_list and self.fac_list == qc.fac_list:
                ans = True
        return ans

    def append_gate(self, kind, qid, para=None, c=None, ctrl=None, tag=None, fac=None):
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
        else:
            phase = 0.0
        self.phase_list.append(phase)
        
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
        >>> qc = ParametricQCirc().h(0).rz(0, tag='foo').rx(0, tag='bar')
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

        # print("* phase num =", len(self.phase_list))
        # print("* gate num  =", self.gate_num)
        if len(self.phase_list) != self.gate_num:
            raise ValueError("phase_list length is not same as gate_num")
        
        qcirc_set_phase_list(self, self.phase_list)

    # add 1-qubit gate

    def rx(self, q0, phase=cfg.DEF_PHASE, ctrl=None, tag=None):
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
        self.append_gate(kind=cfg.ROTATION_X, qid=qid, para=para, ctrl=ctrl, tag=tag, fac=1.0)
        return self

    def ry(self, q0, phase=cfg.DEF_PHASE, ctrl=None, tag=None):
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
        self.append_gate(kind=cfg.ROTATION_X, qid=qid, para=para, ctrl=ctrl, tag=tag, fac=1.0)
        self.append_gate(kind=cfg.PHASE_SHIFT_S, qid=qid, ctrl=ctrl)
        return self

    def rz(self, q0, phase=cfg.DEF_PHASE, ctrl=None, tag=None):
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
        self.append_gate(kind=cfg.ROTATION_Z, qid=qid, para=para, ctrl=ctrl, tag=tag, fac=1.0)
        return self

    def p(self, q0, phase=cfg.DEF_PHASE, ctrl=None, tag=None):
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
        para = [phase, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_Z, qid=qid, para=para, ctrl=ctrl, tag=tag, fac=1.0)
        return self

    # add 2-qubit gate

    def cp(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None, tag=None):
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
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=qid, para=para, ctrl=ctrl, tag=tag, fac=1.0)
        para = [phase/2, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_Z, qid=qid, para=para, ctrl=ctrl, tag=tag, fac=0.5)
        return self

    def crx(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None, tag=None):
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
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=[q0, q1], para=para, ctrl=ctrl, tag=tag, fac=1.0)
        self.append_gate(kind=cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)
        return self

    def cry(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None, tag=None):
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
        self.append_gate(cfg.CONTROLLED_RZ, qid=[q0, q1], para=para, ctrl=ctrl, tag=tag, fac=1.0)
        self.append_gate(cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)

        # cs gate
        para = [0.5, 0.0, 0.0]
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=[q0, q1], para=para, ctrl=ctrl)
        para = [0.25, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_Z, qid=[q0, q1], para=para, ctrl=ctrl)

        return self

    def crz(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None, tag=None):
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
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=qid, para=para, ctrl=ctrl, tag=tag, fac=1.0)
        return self

    def rxx(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None, tag=None):
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
        self.append_gate(kind=cfg.ROTATION_Z, qid=[q1, -1], para=para, ctrl=ctrl, tag=tag, fac=1.0)
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        self.append_gate(kind=cfg.HADAMARD, qid=[q0, -1], ctrl=ctrl)
        self.append_gate(kind=cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)
        return self

    def ryy(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None, tag=None):
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
        self.append_gate(kind=cfg.ROTATION_Z, qid=[q1, -1], para=para, ctrl=ctrl, tag=tag, fac=1.0)
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        self.append_gate(kind=cfg.ROTATION_X, qid=[q0, -1], para=[-0.5, 0.0, 0.0], ctrl=ctrl)
        self.append_gate(kind=cfg.ROTATION_X, qid=[q1, -1], para=[-0.5, 0.0, 0.0], ctrl=ctrl)
        return self

    def rzz(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None, tag=None):
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
        self.append_gate(kind=cfg.ROTATION_Z, qid=[q1, -1], para=para, ctrl=ctrl, tag=tag, fac=1.0)
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        return self

# c-library for qstate
from qlazy.lib.qcirc_c import qcirc_set_phase_list
