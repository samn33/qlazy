# -*- coding: utf-8 -*-
from collections import Counter

from qlazy.config import *
from qlazy.error import *

class MData:
    """ Measured Data

    Attributes
    ----------
    frq : list of int
        frequencies of measured value.
    frequency : Counter
        frequencies of measured value.
    lst : int
        last measured value.
    last : str
        last measured value.
    qid : list of int
        qubit id's list.
    qubit_num : int
        qubit number of the quantum state (= log(state_num)).
    state_num : int
        dimension of the quantum state vector (= 2**qubit_num).
    angle : float
        measured direction with Z-axis.
    phase : float
        measured direction with X-axis.

    """

    def __init__(self, freq_list=None, last_state=0, qid=None, qubit_num=0, state_num=0,
                 angle=0.0, phase=0.0, is_bell=False):
        self.frq = freq_list
        self.lst = last_state
        self.qid = qid
        self.qubit_num = qubit_num
        self.state_num = state_num
        self.angle = angle
        self.phase = phase
        self.is_bell = is_bell

    @property
    def last(self):
        """ last measured value (binary string) """
        mval = self.measured_value(angle=self.angle, phase=self.phase)
        digits = len(self.qid)
        return '{:0{digits}b}'.format(mval, digits=digits)

    @property
    def frequency(self):
        """ frequencies of measured value (Counter) """
        return self.measured_freq(angle=self.angle, phase=self.phase)

    def __str__(self):

        s = ""
        s += "qid: {}\n".format(self.qid)
        s += "qubit num: {}\n".format(self.qubit_num)
        s += "state num: {}\n".format(self.state_num)
        s += "angle, phase: {0:}, {1:}\n".format(self.angle, self.phase)
        s += "frequency: {}\n".format(self.frq)
        s += "last state: {}".format(self.lst)
        return s

    def measured_value(self, angle=0.0, phase=0.0):

        if (self.angle == angle and self.phase == phase):
            mval = self.lst
            return mval
        else:
            raise MData_Error_GetMeasuredData()

    def measured_bit(self, q, angle=0.0, phase=0.0):

        if (q in self.qid and self.angle == angle and self.phase == phase):
            bits = len(self.qid)  # total number of qubits measured
            pos = bits - 1- self.qid.index(q)  # position of 'qid' in the 'last_state'
            mbit = (self.lst >> pos) % 2  # measured value '0' or '1'
            return mbit
        else:
            raise MData_Error_GetMeasuredData()

    def measured_freq(self, angle=0.0, phase=0.0):

        if (self.angle == angle and self.phase == phase):
            digits = len(self.qid)
            res = {"{:0{digits}b}".format(k, digits=digits):v
                   for k,v in enumerate(self.frq) if v > 0}
            return Counter(res)
        else:
            raise MData_Error_GetMeasuredData()
            
    def show(self):
        """
        show the measured data.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Examples
        --------
        >>> qs = QState(2).h(0).cx(0,1)
        >>> md = qs.m(shots=100)
        >>> md.show()
        direction of measurement: z-axis
        frq[00] = 51
        frq[11] = 49
        last state => 11

        """
        if self.is_bell == True:
            print("bell-measurement")
            self.__show_bell()
        elif self.angle == 0.5 and self.phase == 0.0:
            print("direction of measurent: x-axis")
            self.__show_any()
        elif self.angle == 0.5 and self.phase == 0.5:
            print("direction of measurement: y-axis")
            self.__show_any()
        elif self.angle == 0.0 and self.phase == 0.0:
            print("direction of measurement: z-axis")
            self.__show_z()
        else:
            print("direction of measurement: theta={0:f}*PI, phi={1:f}*PI".
                  format(self.angle, self.phase))
            self.__show_any()

    def __show_z(self):
        
        for i in range(self.state_num):
            if self.frq[i] != 0:
                state_string = format(i,'b').zfill(self.qubit_num)
                print("frq[{0:}] = {1:d}".
                      format(state_string, self.frq[i]))
                
        state_string = format(self.lst,'b').zfill(self.qubit_num)
        print("last state =>", state_string)

    def __show_bell(self):
        
        for i in range(self.state_num):
            if self.frq[i] != 0:
                if i == BELL_PHI_PLUS:
                    state_string = 'phi+'
                elif i == BELL_PHI_MINUS:
                    state_string = 'phi-'
                elif i == BELL_PSI_PLUS:
                    state_string = 'psi+'
                elif i == BELL_PSI_MINUS:
                    state_string = 'psi-'
                print("frq[{0:}] = {1:d}".
                      format(state_string, self.frq[i]))

        if self.lst == BELL_PHI_PLUS:
            state_string = 'phi+'
        elif self.lst == BELL_PHI_MINUS:
            state_string = 'phi-'
        elif self.lst == BELL_PSI_PLUS:
            state_string = 'psi+'
        elif self.lst == BELL_PSI_MINUS:
            state_string = 'psi-'
        print("last state =>", state_string)

    def __show_any(self):
        
        for i in range(self.state_num):
            if self.frq[i] != 0:
                state_string = format(i,'b').zfill(self.qubit_num)\
                                            .replace('0','u').replace('1','d')
                print("frq[{0:}] = {1:d}".
                      format(state_string, self.frq[i]))
                
        state_string = format(self.lst,'b').zfill(self.qubit_num)\
                                                  .replace('0','u').replace('1','d')
        print("last state =>", state_string)
