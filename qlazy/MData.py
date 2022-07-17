# -*- coding: utf-8 -*-
""" Mesured data """
import ctypes
from collections import Counter

class MData(ctypes.Structure):
    """ Measured data

    Attributes
    ----------
    qubit_num : int
        number of qubits
    shot_num : int
        number of measureings
    angle : float
        angle
    phase : float
        phase
    qubit_id : list of int
        list of qubit ids
    freq : list of float
        list of frequencies
    last_val : int
        last measurement value

    """
    _fields_ = [
        ('qubit_num', ctypes.c_int),
        ('shot_num', ctypes.c_int),
        ('angle', ctypes.c_double),
        ('phase', ctypes.c_double),
        ('qubit_id', ctypes.POINTER(ctypes.c_int)),
        ('freq', ctypes.POINTER(ctypes.c_int)),
        ('last_val', ctypes.c_int),
    ]

    def __new__(cls, qubit_num=None, shots=1, angle=0.0, phase=0.0, qid=None, **kwargs):
        """
        Parameters
        ----------
        None

        Returns
        -------
        md : instance (QCirc)

        """
        obj = mdata_init(qubit_num, shots, angle, phase, qid)
        md = ctypes.cast(obj.value, ctypes.POINTER(cls)).contents
        return md

    def __str__(self):

        s = ""
        s += "measured direction (theta, phi): {0:}*PI, {1:}*PI\n".format(self.angle, self.phase)
        s += "measured qubit id: {}\n".format([self.qubit_id[i] for i in range(self.qubit_num)])
        s += "frequency: {}\n".format(self.frequency)
        s += "last state: {}".format(self.last)
        return s

    def show(self):
        """ show the measured data"""
        # mdata_print(self)

        if self.angle == 0.0 and self.phase == 0.0:
            mdir = 'z-axis'
        elif self.angle == 0.5 and self.phase == 0.0:
            mdir = 'x-axis'
        elif self.angle == 0.5 and self.phase == 0.5:
            mdir = 'y-axis'
        else:
            mdir = "theta={:.3f}*PI, phi={:.3f}*PI".format(self.angle, self.phase)

        print("direction of measurement: {}".format(mdir))

        if mdir == 'z-axis':
            for k, v in self.frequency.items():
                print("frq[{}] = {}".format(k, v))
            print("last state => {}".format(self.last))
        else:
            for k, v in self.frequency.items():
                print("frq[{}] = {}".format(k.replace('0', 'u').replace('1', 'd'), v))
            print("last state => {}".format(self.last.replace('0', 'u').replace('1', 'd')))

    @property
    def last(self):
        """ last measured value (binary string) """
        mval = self.last_val
        digits = self.qubit_num
        return '{:0{digits}b}'.format(mval, digits=digits)

    @property
    def lst(self):
        """ last measured value (integer) """
        return self.last_val

    @property
    def frequency(self):
        """ frequencies of measured value (Counter) """
        state_num = 2**self.qubit_num
        frq = [self.freq[i] for i in range(state_num)]
        digits = self.qubit_num
        res = {"{:0{digits}b}".format(k, digits=digits):v
               for k, v in enumerate(frq) if v > 0}
        return Counter(res)

    @property
    def frq(self):
        """ frequencies of measured value (list) """
        state_num = 2**self.qubit_num
        freq_list = [0] * state_num
        for k, v in self.frequency.items():
            i = int(k, 2)
            freq_list[i] = v
        return freq_list

    @property
    def state_num(self):
        """ number of states """
        return 2**self.qubit_num

    def __del__(self):

        mdata_free(self)

# c-library for qstate
from qlazy.lib.mdata_c import mdata_init, mdata_print, mdata_free
