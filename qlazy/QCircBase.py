# -*- coding: utf-8 -*-
""" Quantum Circuit (Base) """
import ctypes
from collections import Counter
from fractions import Fraction
import re
import random
import pickle

import qlazy.config as cfg
from qlazy.util import (is_clifford_gate, is_non_clifford_gate, is_measurement_gate,
                        is_reset_gate, get_qgate_qubit_num, get_qgate_param_num)

def string_to_args(s):  # for from_qasm
    """ convert string to args """

    token = s.split(' ')
    if len(token) == 1:
        args = token
    elif len(token) > 1:
        args = [token[0], ' '.join(token[1:])]
    else:
        raise ValueError("can't split string {}.".format(s))

    return args

def init_qc_canvas(qubit_num, cmem_num): # for show method

    qlen = len(str(qubit_num - 1))
    clen = len(str(cmem_num))
    qc_canvas = ["q[{:0{digits}d}] -"
                 .format(i, digits=qlen) + "-" * (clen - 1) for i in range(qubit_num)]
    if cmem_num > 0:
        qc_canvas.append('c' + ' ' * (qlen+1) + '=/=' + '=' * (clen - 1))
        qc_canvas.append(' ' + ' ' * (qlen+1) + ' ' + str(cmem_num) + ' ')

    return qc_canvas
    
def append_qc_canvas(qc_canvas, gates, qubit_num, cmem_num): # for show method

    if len(gates) == 1: # append single gate
        g = gates[0]

        if get_qgate_param_num(g['kind']) == 0:
            g_label = cfg.GATE_LABEL[g['kind']] + '-'
        else:
            g_label = cfg.GATE_LABEL[g['kind']] + '(' + str(g['para'][0]) + ')-'
            
        if get_qgate_qubit_num(g['kind']) == 1 or is_reset_gate(g['kind']):
            qc_canvas[g['qid'][0]] += g_label
            if g['ctrl'] is not None:
                for j in range(g['qid'][0] + 1, qubit_num):
                    qc_canvas[j] += '|'
                qc_canvas[qubit_num] += '^'
                qc_canvas[qubit_num + 1] += (str(g['ctrl']) + ' ')

        elif get_qgate_qubit_num(g['kind']) == 2:
            qc_canvas[g['qid'][0]] += '*'
            qc_canvas[g['qid'][1]] += g_label
            qid_min = min(g['qid'][0], g['qid'][1])
            qid_max = max(g['qid'][0], g['qid'][1])
            for i in range(qid_min + 1, qid_max):
                qc_canvas[i] += '|'
            if g['ctrl'] is not None:
                for j in range(qid_max, qubit_num):
                    qc_canvas[j] += '|'
                qc_canvas[qubit_num] += '^'
                qc_canvas[qubit_num + 1] += (str(g['ctrl']) + ' ')

        elif is_measurement_gate(g['kind']):
            qc_canvas[g['qid'][0]] += g_label
            qc_canvas[qubit_num + 1] += (str(g['c']) + ' ')
            for i in range(g['qid'][0] + 1, qubit_num):
                qc_canvas[i] += '|'
            qc_canvas[qubit_num] += 'v'
            
    else: # append group of 1-qubit gates
        for g in gates:
            if get_qgate_param_num(g['kind']) == 0:
                g_label = cfg.GATE_LABEL[g['kind']] + '-'
            else:
                g_label = cfg.GATE_LABEL[g['kind']] + '(' + str(g['para'][0]) + ')-'
            qc_canvas[g['qid'][0]] += g_label

    # padding
    canvas_len = max(map(len, qc_canvas))
    for i in range(len(qc_canvas)):
        if i < qubit_num:
            qc_canvas[i] += ('-' * (canvas_len - len(qc_canvas[i])))
        elif i == qubit_num:
            qc_canvas[i] += ('=' * (canvas_len - len(qc_canvas[i])))
        else:
            qc_canvas[i] += (' ' * (canvas_len - len(qc_canvas[i])))

class QCircBase(ctypes.Structure):
    """ Quantum Circuit (Base)

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
    _fields_ = [
        ('qubit_num', ctypes.c_int),
        ('cmem_num', ctypes.c_int),
        ('gate_num', ctypes.c_int),
        ('first', ctypes.c_void_p),
        ('last', ctypes.c_void_p),
    ]

    def __new__(cls, **kwargs):
        """
        Parameters
        ----------
        None

        Returns
        -------
        qcirc : instance (QCirc)

        """
        obj = qcirc_base_init()
        qcirc = ctypes.cast(obj.value, ctypes.POINTER(cls)).contents
        return qcirc

    def __str__(self):

        return self.to_string()

    def __add__(self, qc):

        qcirc = self.merge(qc)
        return qcirc

    def __iadd__(self, qc):

        self.merge_mutable(qc)
        return self

    def __mul__(self, other):

        return self.multiple(other)
        
    __rmul__ = __mul__
        
    def __eq__(self, qc):

        ans = self.is_equal(qc)
        return ans

    def __ne__(self, qc):

        ans = not self.is_equal(qc)
        return ans

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

            qcirc_str += ("{0:}{2:} {1:} {3:}{4:}\n"
                          .format(gate_str, qid_str, para_str, c_str, ctrl_str))

        return qcirc_str.strip()

    @classmethod
    def from_qasm(cls, string):
        """
        get QCirc instance from OpenQASM 2.0 string.

        Parameters
        ----------
        None

        Returns
        -------
        qcirc : instance of QCirc

        Notes
        -----
        Non-unitary gates (measure, reset) and user customized
        gates are not supported. Supported gates are
        'x', 'y', 'z', 'h', 's', 'sdg', 't', 'tdg', 'cx', 'cz',
        'ch', 'rx', 'rz', 'crz'.

        """
        line_list = string.split('\n')

        # line #0
        line_count = 0
        args = string_to_args(line_list[line_count])
        if args[0] == 'OPENQASM' and args[1] == '2.0;':
            line_count += 1
        else:
            raise ValueError("line #0 must be 'OPENQASM 2.0;'")

        # line #1
        args = string_to_args(line_list[line_count])
        if args[0] == 'include' and args[1] == '"qelib1.inc";':
            line_count += 1
        else:
            raise ValueError("""line #1 must be 'include "qelib1.inc;"' """)

        # line #2 (#3)
        args = string_to_args(line_list[line_count])
        if args[0] == 'qreg' and re.match('q', args[1]).group() == 'q':
            line_count += 1
        else:
            raise ValueError("""line #2 must be 'qreg q[<int>];"' """)

        # line (#3) #4 ...
        qcirc = cls()
        for i in range(line_count, len(line_list)):
            args = string_to_args(line_list[i])
            if args[0] == '':
                continue

            if args[0] in ('measure', 'reset'):
                raise ValueError("sorry, 'measure', 'reset' is not supported.")

            if args[0] in ('x', 'y', 'z', 'h', 's', 'sdg', 't', 'tdg'):
                res = re.search(r"q\[|\];", args[1])
                if res is not None:
                    q = int(re.sub(r"q\[|\];", "", args[1]))
                else:
                    raise ValueError("argument '{}' is not valid for '{}' gate."
                                     .format(args[1], args[0]))

                if args[0] == 'x':
                    qcirc.x(q)
                elif args[0] == 'z':
                    qcirc.z(q)
                elif args[0] == 'h':
                    qcirc.h(q)
                elif args[0] == 's':
                    qcirc.s(q)
                elif args[0] == 'sdg':
                    qcirc.s_dg(q)
                elif args[0] == 't':
                    qcirc.t(q)
                elif args[0] == 'tdg':
                    qcirc.t_dg(q)

            elif args[0] in ('cx', 'cz', 'ch'):
                res = re.search(r"q\[[0-9]+\],\s*q\[[0-9]+\];", args[1])
                if res is not None:
                    qubits = args[1].split(',')
                    q0 = int(re.sub(r"q\[|\]", "", qubits[0]))
                    q1 = int(re.sub(r"q\[|\];", "", qubits[1]))
                else:
                    raise ValueError("argument '{}' is not valid for '{}' gate."
                                     .format(args[1], args[0]))

                if args[0] == 'cx':
                    qcirc.cx(q0, q1)
                elif args[0] == 'cz':
                    qcirc.cz(q0, q1)
                elif args[0] == 'ch':
                    qcirc.ch(q0, q1)

            elif (re.match('rx', args[0]) is not None or
                  re.match('rz', args[0]) is not None):

                res = re.search(r"q\[|\];", args[1])
                if res is not None:
                    q = int(re.sub(r"q\[|\];", "", args[1]))
                else:
                    raise ValueError(("argument '{}' is not valid for '{}' gate."
                                      .format(args[1], args[0])))

                para_str = [s.strip('*').strip('/') for s in re.sub(r".+\(|\)", "",
                                                                    args[0]).split("pi")]
                if para_str[0] == '0':
                    para = 0.
                else:
                    denominator = 1.
                    if para_str[0] == '':
                        numerator = 1.
                    else:
                        numerator = float(para_str[0])
                    if para_str[1] == '':
                        denominator = 1.
                    else:
                        denominator = float(para_str[1])
                    para = numerator / denominator

                if re.match('rx', args[0]) is not None:
                    qcirc.rx(q, phase=para)
                elif re.match('rz', args[0]) is not None:
                    qcirc.rz(q, phase=para)

            elif re.match('crz', args[0]) is not None:

                res = re.search(r"q\[[0-9]+\],\s*q\[[0-9]+\];", args[1])
                if res is not None:
                    qubits = args[1].split(',')
                    q0 = int(re.sub(r"q\[|\]", "", qubits[0]))
                    q1 = int(re.sub(r"q\[|\];", "", qubits[1]))
                else:
                    raise ValueError(("argument '{}' is not valid for '{}' gate."
                                      .format(args[1], args[0])))

                para_str = [s.strip('*').strip('/') for s in re.sub(r".+\(|\)", "",
                                                                    args[0]).split("pi")]
                if para_str[0] == '0':
                    para = 0.
                else:
                    denominator = 1.
                    if para_str[0] == '':
                        numerator = 1.
                    else:
                        numerator = float(para_str[0])
                    if para_str[1] == '':
                        denominator = 1.
                    else:
                        denominator = float(para_str[1])
                    para = numerator / denominator

                if re.match('crz', args[0]) is not None:
                    qcirc.crz(q0, q1, phase=para)

            else:
                raise ValueError("{} gate is not supported".format(args[0]))

        return qcirc

    @classmethod
    def from_qasm_file(cls, file_path):
        """
        get QCirc instance from OpenQASM 2.0 file.

        Parameters
        ----------
        file_path: str
            file path name of OpenQASM 2.0 file

        Returns
        -------
        qcirc : instance of QCirc

        Notes
        -----
        Non-unitary gates (measure, reset) and user customized
        gates are not supported. Supported gates are
        'x', 'y', 'z', 'h', 's', 'sdg', 't', 'tdg',
        'cx', 'cz', 'ch', 'rx', 'rz', 'crz'.

        """
        with open(file_path, mode='r') as f:
            s = f.read()

        qcirc = cls.from_qasm(s)
        return qcirc

    def to_qasm(self):
        """
        get OpenQASM 2.0 string of the circuit.

        Parameters
        ----------
        None

        Returns
        -------
        qcirc_str : str

        """
        qc = self.clone()

        # header and include file
        qcirc_str = """OPENQASM 2.0;\n"""
        qcirc_str += """include "qelib1.inc";\n"""

        # definition of qreg, creg
        qcirc_str += """qreg q[{}];\n""".format(self.qubit_num)
        for i in range(self.cmem_num):
            qcirc_str += """creg c{}[1];\n""".format(i)

        # description of each gate operation
        while True:
            kind = qc.kind_first()
            if kind is None:
                break

            (kind, qid, para, c, ctrl) = qc.pop_gate()
            term_num = get_qgate_qubit_num(kind)
            if kind in (cfg.MEASURE, cfg.RESET):
                term_num = 1

            para_num = get_qgate_param_num(kind)
            para_frac = [Fraction(str(p)) for p in para]

            gate_str = cfg.GATE_STRING_QASM[kind]
            qid_str = ",".join(["q[" + str(qid[i]) + "]" for i in range(term_num)])
            qid_str.strip()

            if para_num == 0:
                if kind == cfg.CONTROLLED_S:
                    para_str = "(pi/2)"
                elif kind == cfg.CONTROLLED_S_:
                    para_str = "(-pi/2)"
                elif kind == cfg.CONTROLLED_T:
                    para_str = "(pi/4)"
                elif kind == cfg.CONTROLLED_T_:
                    para_str = "(-pi/4)"
                else:
                    para_str = ""
            else:
                para_str_list = []
                for i, p in enumerate(para_frac):
                    if i >= para_num:
                        break
                    if p.numerator == 0:
                        para_str_list.append("0")
                    elif p.numerator == 1:
                        para_str_list.append("pi/"+ str(p.denominator))
                    else:
                        para_str_list.append(str(p.numerator) + "*pi/" + str(p.denominator))

                para_str = ",".join(para_str_list)
                para_str = "(" + para_str+ ")"

            if c is None:
                c_str = ""
            else:
                c_str = " -> c{}[0]".format(c)

            if ctrl is None:
                ctrl_str = ""
            else:
                ctrl_str = "if(c{}==1) ".format(ctrl)

            qcirc_str += ("{4:}{0:}{2:} {1:}{3:};\n"
                          .format(gate_str, qid_str, para_str, c_str, ctrl_str))

        return qcirc_str.strip()

    def to_qasm_file(self, file_path):
        """
        write to OpenQASM 2.0 file.

        Parameters
        ----------
        file_path: str
            file path name of OpenQASM 2.0 file

        Returns
        -------
        None

        """
        s = self.to_qasm()
        with open(file_path, mode='w') as f:
            f.write(s)

    def show(self, width=100):
        """
        show the circuit

        Parameters
        ----------
        width : int, default - 100
            width for line breaks and display long quantum circuit

        Returns
        -------
        None

        """
        qc = self.clone()

        qubit_num = self.qubit_num
        cmem_num = self.cmem_num
        gate_num = self.gate_num

        qc_canvas = init_qc_canvas(qubit_num, cmem_num)
        
        gates = []
        qids = []
        while True:
            kind = qc.kind_first()
            if kind is None:
                break

            (kind, qid, para, c, ctrl) = qc.pop_gate()
            gate = {'kind': kind, 'qid': qid, 'para': para, 'c': c, 'ctrl': ctrl}
            if ((get_qgate_qubit_num(kind) == 1 or is_reset_gate(kind)) and ctrl is None):
                if qid[0] in qids:
                    append_qc_canvas(qc_canvas, gates, qubit_num, cmem_num)
                    gates = [gate]
                    qids = [qid[0]]
                else:
                    gates.append(gate)
                    qids.append(qid[0])

            else:
                if gates != []:
                    append_qc_canvas(qc_canvas, gates, qubit_num, cmem_num)
                    gates = []
                    qids = []
                append_qc_canvas(qc_canvas, [gate], qubit_num, cmem_num)

        if gates != []:
            append_qc_canvas(qc_canvas, gates, qubit_num, cmem_num)
            
        pos_start = 0
        pos_end = width
        while True:
            if pos_start >= len(qc_canvas[0]):
                break
            for line in qc_canvas:
                print(line[pos_start:pos_end])
            print()
            pos_start += width
            pos_end +=width

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
        obj = qcirc_base_copy(self)
        qcirc = ctypes.cast(obj.value, ctypes.POINTER(self.__class__)).contents
        return qcirc

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
        obj = qcirc_base_merge(self, qc)
        qcirc = ctypes.cast(obj.value, ctypes.POINTER(self.__class__)).contents
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
        qcirc_base_merge_mutable(self, qc)

    def multiple(self, other):
        """
        integer multiple for quantum circuit

        Parameters
        ----------
        other : instance of QCirc / int
            quantum circuit / number

        Returns
        -------
        qc : instance of QCirc
            quantum circuit after multiplication

        """
        if isinstance(other, int) and other > 0:
            qc = self.clone()
            qc_out = self.clone()
            for i in range(other-1):
                qc_out = qc_out.merge(qc)
        else:
            raise TypeError("Can't multiple QCirc with {} (type:{})".format(other, type(other)))
        
        return qc_out

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
        ans = qcirc_base_is_equal(self, qc)
        return ans

    def kind_first(self):
        """
        get kind of first gate of the circuit.

        Parameters
        ----------
        None

        Returns
        -------
        kind_list : int
            kind of first quantum gate of quantum circuit

        Note
        ----
        return None if none of gates included

        """
        kind = qcirc_base_kind_first(self)
        return kind

    def kind_list(self):
        """
        get list of kinds from the circuit.

        Parameters
        ----------
        None

        Returns
        -------
        kinds : list of kind
            kinds of the quantum circuit

        Note
        ----
        return None if none of gates included

        """
        qc = self.clone()
        kind_list = []
        while True:
            kind = qc.kind_first()
            if kind is None:
                break
            kind_list.append(kind)
            qc.pop_gate()

        return kind_list

    def get_gates(self):
        """
        get list of gates from the circuit.

        Parameters
        ----------
        None

        Returns
        -------
        gates : list of dict
            gates of the quantum circuit
            gates = [{'kind':kind, 'qid':qid, 'phase':phase, 'cid':cid, 'ctrl':ctrl}, ...]
            - kind: gate name
            - qid: qubit id
            - phase: phase parameter (non-zero only for rotation gates)
            - cid: classical register id (set only for measurement gate)
            - ctrl: classical register id to control gate operation

        """
        qc = self.clone()
        gates = []
        while True:
            kind = qc.kind_first()
            if kind is None:
                break

            (kind, qid, para, c, ctrl) = qc.pop_gate()
            qid = [q for q in qid if q >= 0]
            if c is None:
                cid = None
            else:
                cid = [c]
            gates.append({'kind': cfg.GATE_STRING[kind], 'qid': qid,
                          'phase': para[0], 'cid': cid, 'ctrl': ctrl})

        return gates

    def add_gates(self, gates=None):
        """
        add list of gates to the circuit.

        Parameters
        ----------
        gates : list of dict
            gates of the quantum circuit
            gates = [{'kind':kind, 'qid':qid, 'phase':phase, 'cid':cid, 'ctrl':ctrl}, ...]
            - kind: gate name
            - qid: qubit id
            - phase: phase parameter (non-zero only for rotation gates)
            - cid: classical register id (set only for measurement gate)
            - ctrl: classical register id for controlling gate operation

        Returns
        -------
        self: instance of QCirc
            circuit after adding gates

        """
        if gates is None:
            raise ValueError("gates must be specified.")
        for g in gates:
            kind = cfg.GATE_KIND[g['kind']]
            qid = g['qid']
            para = [g['phase'], 0.0, 0.0]
            if g['cid'] is None:
                c = None
            else:
                c = g['cid'][0]
            ctrl = g['ctrl']
            self.append_gate(kind, qid, para, c, ctrl)
        return self

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
        gates = self.get_gates()
        with open(file_path, mode='wb') as f:
            pickle.dump(gates, f)

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
            gates = pickle.load(f)
        qcirc = cls().add_gates(gates)
        return qcirc

    def get_stats(self):
        """
        get statistics of the circuit.

        Parameters
        ----------
        None

        Returns
        -------
        stats : dict
            {'qubit_num':qubit_num, 'cmem_num':cmem_num, 'gate_num':gate_num, 'gate_freq':gate_freq}
            - qubit_num: number of qubits
            - cmem_num: number of classical bits
            - gate_num: number of gates
            - gate_freq: frequency of gates (Counter)

        """
        gate_list = [cfg.GATE_STRING[kind] for kind in self.kind_list()]
        gate_freq = Counter(gate_list)

        gatetype_list = []
        for kind in self.kind_list():
            if is_clifford_gate(kind) is True or is_non_clifford_gate(kind) is True:
                gatetype_list.append('unitary')
                if is_clifford_gate(kind) is True:
                    gatetype_list.append('clifford')
                elif is_non_clifford_gate(kind) is True:
                    gatetype_list.append('non-clifford')
            elif is_measurement_gate(kind) is True or is_reset_gate(kind) is True:
                gatetype_list.append('non-unitary')
            else:
                raise ValueError("unknown gate kind:{}".format(kind))
        gatetype_freq = Counter(gatetype_list)

        stats = {'qubit_num': self.qubit_num, 'cmem_num':self.cmem_num, 'gate_num': len(gate_list),
                 'gate_freq': gate_freq, 'gatetype_freq': gatetype_freq}
        return stats

    @classmethod
    def generate_random_gates(cls, qubit_num=0, gate_num=0, phase=None, prob=None, **kwargs):
        """
        generate circuit including random gates.

        Parameters
        ----------
        qubit_num: int
            number of qubits
        gate_num: int
            numbner of gates
        phase: tupple of float
            phases selected randomly
        prob: dict
            {'x':prob_x, 'z':prob_z, 'h':prob_h, 's':prob_s, 's_dg':prob_s_dg,
             't':prob_t, 't_dg':prob_t_dg, 'rx':prob_rx, 'rz':prob_rz, 'cx':prob_cx,
             'cz':prob_cz, 'ch':prob_ch, 'crz':prob_crz}
            - prob_x: probability of x
            - prob_z: probability of z
            - prob_h: probability of h
            - prob_s: probability of s
            - prob_s_dg: probability of s_dg
            - prob_t: probability of t
            - prob_t_dg: probability of t_dg
            - prob_rx: probability of rx
            - prob_rz: probability of rz
            - prob_cx: probability of cx
            - prob_cz: probability of cz
            - prob_ch: probability of ch
            - prob_crz: probability of crz

        Returns
        -------
        qcirc: instance of QCirc
            generated circuit

        Examples
        --------
        >>> qc = QCirc.generate_random_gates(qubit_num=5, gate_num=100,
        phase_unit=0.25, prob={'h':3, 'cx':7, 'rz':1})

        Notes
        -----
        * each probability values are normalized so that the sum of the probabilities is 1.0.
        * Phase parameters of rotation gates are selected randomly in the element of 'phase'.

        """
        if ((isinstance(qubit_num, int) is not True or
             isinstance(gate_num, int) is not True or qubit_num < 1 or gate_num < 1)):
            raise ValueError("qubit_num and/or gate_num must be positive integer.")
        if phase is not None:
            if ((isinstance(phase, float) is not True and
                 isinstance(phase, int) is not True and
                 isinstance(phase, tuple) is not True)):
                raise ValueError("phase value(s) must be int/float of tuple.")

        total_prob = 0.0
        for p in prob.values():
            total_prob += p
        glist = []
        plist = []
        p = 0.0
        for k, v in prob.items():
            if v < 0.0:
                raise ValueError("probability must be positive value.")
            if k  in ('x', 'z', 'h', 's', 's_dg', 't', 't_dg', 'rx', 'rz', 'cx', 'cz', 'ch', 'crz'):
                glist.append(k)
                p += v / total_prob
                plist.append(p)
            else:
                raise ValueError("gate '{}' is not supported.".format(k))

        if plist[-1] != 1.0:
            plist[-1] = 1.0

        qcirc = cls()

        TRY_MAX = 10  # for random generation
        max_q = -1
        gate_count = 0
        while gate_count < gate_num or max_q < qubit_num - 1:
            r = random.random()
            kind = None
            for i, p in enumerate(plist):
                if r <= p:
                    kind = cfg.GATE_KIND[glist[i]]
                    break
            term_num = get_qgate_qubit_num(kind)
            para_num = get_qgate_param_num(kind)

            if term_num == 1 and para_num == 0:    # 1-qubit gate
                q0 = random.randint(0, qubit_num - 1)
                qcirc.append_gate(kind, [q0])
                max_q = max(max_q, q0)
                gate_count += 1
            elif term_num == 1 and para_num == 1:  # 1-qubit and 1-parameter gate
                q0 = random.randint(0, qubit_num - 1)
                if phase is None:
                    p = 0.0
                elif isinstance(phase, (float, int)):
                    p = phase
                else:
                    p = random.choice(phase)
                qcirc.append_gate(kind, [q0], para=[p, 0., 0.])
                max_q = max(max_q, q0)
                gate_count += 1
            elif term_num == 2 and para_num == 0:  # 2-qubit gate
                q0 = random.randint(0, qubit_num - 1)
                q1 = random.randint(0, qubit_num - 1)
                cnt = 0
                while q0 == q1 and cnt < TRY_MAX:
                    q1 = random.randint(0, qubit_num - 1)
                    cnt += 1
                if cnt >= TRY_MAX:
                    raise ValueError(("can't generate qubit id for '{}' gate."
                                      .format(cfg.GATE_STRING[kind])))
                qcirc.append_gate(kind, [q0, q1])
                max_q = max(max_q, q0, q1)
                gate_count += 1
            elif term_num == 2 and para_num == 1:  # 2-qubit and 1-parameter gate
                q0 = random.randint(0, qubit_num - 1)
                q1 = random.randint(0, qubit_num - 1)
                cnt = 0
                while q0 == q1 and cnt < TRY_MAX:
                    q1 = random.randint(0, qubit_num - 1)
                    cnt += 1
                if cnt >= TRY_MAX:
                    raise ValueError(("can't generate qubit id for '{}' gate."
                                      .format(cfg.GATE_STRING[kind])))
                if phase is None:
                    p = 0.0
                elif isinstance(phase, (float, int)):
                    p = phase
                else:
                    p = random.choice(phase)
                qcirc.append_gate(kind, [q0, q1], para=[p, 0., 0.])
                max_q = max(max_q, q0, q1)
                gate_count += 1
            else:
                raise ValueError(("gate of term_num={}, param_num={} is not supported"
                                  .format(term_num, para_num)))

        # delete extra gates
        for _ in range(gate_count - gate_num):
            qcirc.pop_gate()

        return qcirc

    def to_pyzx(self):
        """
        get pyzx's Circuit instance.

        Parameters
        ----------
        None

        Returns
        -------
        zxqc: instance of pyzx's Circuit
            quantum circuit

        Notes
        -----
        Non-unitary gates: measure, reset are not supported.

        """
        from pyzx import Circuit

        zxqc = Circuit.from_qasm(self.to_qasm())
        return zxqc

    @classmethod
    def from_pyzx(cls, zxqc):
        """
        get pyzx's Circuit instance.

        Parameters
        ----------
        zxqc: instance of pyzx's Circuit
            quantum circuit

        Returns
        -------
        qc: instance of QCirc
            quantum circuit

        Notes
        -----
        Non-unitary gates: measure, reset are not supported.

        """
        qc = cls.from_qasm(zxqc.to_qasm())
        return qc

    def optimize(self, *args, **kwargs):
        """
        optimize the quantum circuit (using pyzx's full_optimize method).

        Parameters
        ----------
        None

        Returns
        -------
        qc: instance of QCirc
            optimized circuit

        Notes
        -----
        Non-unitary gates: measure, reset are not supported.

        """
        import pyzx as zx

        zxqc = self.to_pyzx()
        zxqc_opt = zx.optimize.full_optimize(zxqc)
        qc = self.__class__.from_pyzx(zxqc_opt)

        return qc

    def equivalent(self, qc, *args, **kwargs):
        """
        two quantum circuits are equivalent or not (using pyzx's verify_equality method).

        Parameters
        ----------
        None

        Returns
        -------
        ans: bool

        Notes
        -----
        Non-unitary gates: measure, reset are not supported.

        """
        from pyzx import Circuit

        zxqc_A = Circuit.from_qasm(self.to_qasm())
        zxqc_B = Circuit.from_qasm(qc.to_qasm())
        ans = zxqc_A.verify_equality(zxqc_B)

        return ans

    def pop_gate(self):
        """
        pop first gate of the circuit.

        Parameters
        ----------
        None

        Returns
        -------
        gate : tupple of (int, [int,int], [float,float,float], int, int)
            tupple of (kind, qid, para, c, ctrl)
            - kind ... kind of gate
            - qid ... qubit id list
            - para ... parameters for rotation
            - c ... classical register ID to store measured data (only for measurement gate)
            - ctrl ... classical register id to controll the gate

        """
        (kind, qid, para, c, ctrl) = qcirc_base_pop_gate(self)
        return (kind, qid, para, c, ctrl)

    def append_gate(self, kind=None, qid=None, para=None, c=None, ctrl=None, **kwargs):
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

        Returns
        -------
        None

        """
        # kind must be int
        if isinstance(kind, int) is not True:
            raise TypeError("kind must be int.")

        # qid must be list of int
        if isinstance(qid, list) is not True:
            raise TypeError("qid must be list.")
        for q in qid:
            if isinstance(q, int) is not True:
                raise TypeError("qid must be list of int.")

        # para is None or para must be list of float
        if para is not None:
            if isinstance(para, list) is True:
                for p in para:
                    if isinstance(p, float) is not True:
                        raise TypeError("para must be a list of float.")
            else:
                raise TypeError("para must be a list of float.")

        # c is None or c must be int
        if c is not None and isinstance(c, int) is not True:
            raise TypeError("c must be int.")

        # ctrl is None or ctrl must be int
        if ctrl is not None and isinstance(ctrl, int) is not True:
            raise TypeError("ctrl must be int.")

        qcirc_base_append_gate(self, kind, qid, para, c, ctrl)

    def split_unitary_non_unitary(self):
        """
        split two part of the gate.

        Parameters
        ----------
        None

        Returns
        -------
        qc_pair : tupple of (QCirc, Qcirc)
            former part includes only unitary gates and later part
            includes non-unitary gate (measure or reset) first
        """
        qc_unitary = self.__class__()
        qc_non_unitary = self.clone()
        while True:
            kind_ori = qc_non_unitary.kind_first()
            if kind_ori is None or kind_ori is cfg.MEASURE or kind_ori is cfg.RESET:
                break
            (kind, qid, para, c, ctrl) = qc_non_unitary.pop_gate()
            qc_unitary.append_gate(kind, qid, para, c, ctrl)

        qc_pair = (qc_unitary, qc_non_unitary)
        return qc_pair

    def all_gates_measurement(self):
        """
        gates of the qcirc are all measurement

        Parameters
        ----------
        None

        Returns
        -------
        ans : bool
            True if all gates are measurement, False if otherwise
        """
        if self.kind_first() is None:
            return False
        
        ans = True
        qcirc = self.clone()
        while True:
            kind = qcirc.kind_first()
            if kind is None:
                break
            (kind, qid, para, c, ctrl) = qcirc.pop_gate()
            if kind is not cfg.MEASURE:
                ans = False
                break
        return ans

    def __del__(self):

        qcirc_base_free(self)

    # non-unitary gate

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
        if qid is None:
            raise ValueError("qid must be specified.")
        if cid is None:
            raise ValueError("cid must be specified.")
        if len(qid) != len(cid):
            raise ValueError("length of qid and cid must be same.")
        for q, c in zip(qid, cid):
            qid = [q, -1]
            self.append_gate(kind=cfg.MEASURE, qid=qid, c=c)

        return self

    def reset(self, qid):
        """
        add reset gate.

        Parameters
        ----------
        qid : list of int
            qubit id list to measure.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        Notes
        -----
        'cid' must be 'None' or same length as 'qid'

        """
        for q in qid:
            qid = [q, -1]
            self.append_gate(kind=cfg.RESET, qid=qid)
        return self

    # add 1-qubit gate

    def x(self, q0, ctrl=None):
        """
        add X gate.

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, -1]
        self.append_gate(kind=cfg.PAULI_X, qid=qid, ctrl=ctrl)
        return self

    def y(self, q0, ctrl=None):
        """
        add Y gate.

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, -1]
        self.append_gate(kind=cfg.PAULI_Z, qid=qid, ctrl=ctrl)
        self.append_gate(kind=cfg.PAULI_X, qid=qid, ctrl=ctrl)
        return self

    def z(self, q0, ctrl=None):
        """
        add Z gate.

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, -1]
        self.append_gate(kind=cfg.PAULI_Z, qid=qid, ctrl=ctrl)
        return self

    def h(self, q0, ctrl=None):
        """
        add H gate (hadamard gate).

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, -1]
        self.append_gate(kind=cfg.HADAMARD, qid=qid, ctrl=ctrl)
        return self

    def xr(self, q0, ctrl=None):
        """
        add root X gate.

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, -1]
        para = [0.5, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_X, qid=qid, para=para, ctrl=ctrl)
        return self

    def xr_dg(self, q0, ctrl=None):
        """
        add root X dagger gate
        (hermmitian conjugate of root X gate).

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, -1]
        para = [-0.5, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_X, qid=qid, para=para, ctrl=ctrl)
        return self

    def s(self, q0, ctrl=None):
        """
        add S gate.

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, -1]
        self.append_gate(kind=cfg.PHASE_SHIFT_S, qid=qid, ctrl=ctrl)
        return self

    def s_dg(self, q0, ctrl=None):
        """
        add S dagger gate (hermitian conjugate of S gate).

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, -1]
        self.append_gate(kind=cfg.PHASE_SHIFT_S_, qid=qid, ctrl=ctrl)
        return self

    def t(self, q0, ctrl=None):
        """
        add T gate.

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, -1]
        self.append_gate(kind=cfg.PHASE_SHIFT_T, qid=qid, ctrl=ctrl)
        return self

    def t_dg(self, q0, ctrl=None):
        """
        add T dagger gate (hermitian conjugate of T gate).

        Parameters
        ----------
        q0 : int
            qubit id.
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, -1]
        self.append_gate(kind=cfg.PHASE_SHIFT_T_, qid=qid, ctrl=ctrl)
        return self

    def rx(self, q0, phase=cfg.DEF_PHASE, ctrl=None):
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

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, -1]
        para = [phase, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_X, qid=qid, para=para, ctrl=ctrl)
        return self

    def ry(self, q0, phase=cfg.DEF_PHASE, ctrl=None):
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
        self.append_gate(kind=cfg.ROTATION_X, qid=qid, para=para, ctrl=ctrl)
        self.append_gate(kind=cfg.PHASE_SHIFT_S, qid=qid, ctrl=ctrl)
        return self

    def rz(self, q0, phase=cfg.DEF_PHASE, ctrl=None):
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

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, -1]
        para = [phase, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_Z, qid=qid, para=para, ctrl=ctrl)
        return self

    def p(self, q0, phase=cfg.DEF_PHASE, ctrl=None):
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
        self.append_gate(kind=cfg.ROTATION_Z, qid=qid, para=para, ctrl=ctrl)
        return self

    # add 2-qubit gate

    def cx(self, q0, q1, ctrl=None):
        """
        add CX gate (controlled X gate, controlled NOT gate, CNOT gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, q1]
        self.append_gate(kind=cfg.CONTROLLED_X, qid=qid, ctrl=ctrl)
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
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, q1]
        self.append_gate(kind=cfg.CONTROLLED_Z, qid=qid, ctrl=ctrl)
        self.append_gate(kind=cfg.CONTROLLED_X, qid=qid, ctrl=ctrl)
        self.append_gate(kind=cfg.PHASE_SHIFT_S, qid=qid, ctrl=ctrl)
        return self

    def cz(self, q0, q1, ctrl=None):
        """
        add CZ gate (controlled Z gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, q1]
        self.append_gate(kind=cfg.CONTROLLED_Z, qid=qid, ctrl=ctrl)
        return self

    def cxr(self, q0, q1, ctrl=None):
        """
        add CXR gate (controlled root X gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        para = [0.5, 0.0, 0.0]
        self.append_gate(kind=cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=[q0, q1], para=para, ctrl=ctrl)
        self.append_gate(kind=cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)
        para = [0.25, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_Z, qid=[q0, q1], para=para, ctrl=ctrl)
        return self

    def cxr_dg(self, q0, q1, ctrl=None):
        """
        add CXR dagger gate (controlled XR dagger gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        para = [-0.5, 0.0, 0.0]
        self.append_gate(kind=cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=[q0, q1], para=para, ctrl=ctrl)
        self.append_gate(kind=cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)
        para = [-0.25, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_Z, qid=[q0, q1], para=para, ctrl=ctrl)
        return self

    def ch(self, q0, q1, ctrl=None):
        """
        add CH gate (controlled H gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, q1]
        self.append_gate(kind=cfg.CONTROLLED_H, qid=qid, ctrl=ctrl)
        return self

    def cs(self, q0, q1, ctrl=None):
        """
        add CS gate (controlled S gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, q1]
        para = [0.5, 0.0, 0.0]
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=qid, para=para, ctrl=ctrl)
        para = [0.25, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_Z, qid=qid, para=para, ctrl=ctrl)
        return self

    def cs_dg(self, q0, q1, ctrl=None):
        """
        add CS dagger gate (controlled S dagger gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, q1]
        para = [-0.5, 0.0, 0.0]
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=qid, para=para, ctrl=ctrl)
        para = [-0.25, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_Z, qid=qid, para=para, ctrl=ctrl)
        return self

    def ct(self, q0, q1, ctrl=None):
        """
        add CT gate (controlled T gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, q1]
        para = [0.25, 0.0, 0.0]
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=qid, para=para, ctrl=ctrl)
        para = [0.125, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_Z, qid=qid, para=para, ctrl=ctrl)
        return self

    def ct_dg(self, q0, q1, ctrl=None):
        """
        add CT dagger gate (controlled T dagger gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, q1]
        para = [-0.25, 0.0, 0.0]
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=qid, para=para, ctrl=ctrl)
        para = [-0.125, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_Z, qid=qid, para=para, ctrl=ctrl)
        return self

    def sw(self, q0, q1, ctrl=None):
        """
        add swap gate

        Parameters
        ----------
        q0 : int
            qubit id
        q1 : int
            qubit id
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q1, q0], ctrl=ctrl)
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        return self

    def cp(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None):
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

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, q1]
        para = [phase, 0.0, 0.0]
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=qid, para=para, ctrl=ctrl)
        para = [phase/2, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_Z, qid=qid, para=para, ctrl=ctrl)
        return self

    def crx(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None):
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

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        para = [phase, 0.0, 0.0]
        self.append_gate(kind=cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=[q0, q1], para=para, ctrl=ctrl)
        self.append_gate(kind=cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)
        return self

    def cry(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None):
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
        self.append_gate(cfg.CONTROLLED_RZ, qid=[q0, q1], para=para, ctrl=ctrl)
        self.append_gate(cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)

        # cs gate
        para = [0.5, 0.0, 0.0]
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=[q0, q1], para=para, ctrl=ctrl)
        para = [0.25, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_Z, qid=[q0, q1], para=para, ctrl=ctrl)

        return self

    def crz(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None):
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

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        qid = [q0, q1]
        para = [phase, 0.0, 0.0]
        self.append_gate(kind=cfg.CONTROLLED_RZ, qid=qid, para=para, ctrl=ctrl)
        return self

    def rxx(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None):
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

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        para=[phase, 0.0, 0.0]
        self.append_gate(kind=cfg.HADAMARD, qid=[q0, -1], ctrl=ctrl)
        self.append_gate(kind=cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        self.append_gate(kind=cfg.ROTATION_Z, qid=[q1, -1], para=para, ctrl=ctrl)
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        self.append_gate(kind=cfg.HADAMARD, qid=[q0, -1], ctrl=ctrl)
        self.append_gate(kind=cfg.HADAMARD, qid=[q1, -1], ctrl=ctrl)
        return self

    def ryy(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None):
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

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        para = [phase, 0.0, 0.0]
        self.append_gate(kind=cfg.ROTATION_X, qid=[q0, -1], para=[0.5, 0.0, 0.0], ctrl=ctrl)
        self.append_gate(kind=cfg.ROTATION_X, qid=[q1, -1], para=[0.5, 0.0, 0.0], ctrl=ctrl)
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        self.append_gate(kind=cfg.ROTATION_Z, qid=[q1, -1], para=para, ctrl=ctrl)
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        self.append_gate(kind=cfg.ROTATION_X, qid=[q0, -1], para=[-0.5, 0.0, 0.0], ctrl=ctrl)
        self.append_gate(kind=cfg.ROTATION_X, qid=[q1, -1], para=[-0.5, 0.0, 0.0], ctrl=ctrl)
        return self

    def rzz(self, q0, q1, phase=cfg.DEF_PHASE, ctrl=None):
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

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        para = [phase, 0.0, 0.0]
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        self.append_gate(kind=cfg.ROTATION_Z, qid=[q1, -1], para=para, ctrl=ctrl)
        self.append_gate(kind=cfg.CONTROLLED_X, qid=[q0, q1], ctrl=ctrl)
        return self

    # 3-qubit gate

    def ccx(self, q0, q1, q2, ctrl=None):
        """
        add CCX gate (toffoli gate, controlled controlled X gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (control qubit).
        q2 : int
            qubit id (target qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.cxr(q1, q2, ctrl=ctrl).cx(q0, q1, ctrl=ctrl).cxr_dg(q1, q2, ctrl=ctrl)
        self.cx(q0, q1, ctrl=ctrl).cxr(q0, q2, ctrl=ctrl)
        return self

    def csw(self, q0, q1, q2, ctrl=None):
        """
        add CSW gate (fredkin gate, controlled swap gate).

        Parameters
        ----------
        q0 : int
            qubit id (control qubit).
        q1 : int
            qubit id (swap qubit).
        q2 : int
            qubit id (swap qubit).
        ctrl : int
            address of classical memory to control gate operation.

        Returns
        -------
        self : instance of QCirc
            quantum circuit after adding

        """
        self.cx(q2, q1, ctrl=ctrl).ccx(q0, q1, q2, ctrl=ctrl).cx(q2, q1, ctrl=ctrl)
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

        return self

# c-library for qstate
from qlazy.lib.qcirc_base_c import (qcirc_base_init, qcirc_base_copy, qcirc_base_merge,
                                    qcirc_base_merge_mutable, qcirc_base_is_equal,
                                    qcirc_base_append_gate, qcirc_base_kind_first,
                                    qcirc_base_pop_gate, qcirc_base_free)
