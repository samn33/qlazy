# -*- coding: utf-8 -*-
""" Result of quantum circuit execution """

from collections import Counter
from datetime import datetime
from dataclasses import dataclass, field
import pickle

from qlazy.Backend import Backend
from qlazy.QState import QState
from qlazy.Stabilizer import Stabilizer
from qlazy.CMem import CMem

@dataclass
class Result:
    """ Result of quantum circuit execution

    Attributes
    ----------
    backend : instance of Backend
        backend device of quantum computing
    qubit_num : int
        number of qubits
    cmem_num : int
        number of classical bits
    cid : list
        classical register id list to get frequencys.
    shots : int
        number of measurements
    freqency : instance of Counter
        frequencies of measured value.
    start_time : instance of datetime
        start time to ececute the quantum circuit.
    end_time : instance of datetime
        end time to ececute the quantum circuit.
    elapsed_time : float
        elapsed time to ececute the quantum circuit.
    qstate : instance of QState
        quantum state after executing circuit.
    stabilizer : instance of Stabilizer
        stabilizer state after executing circuit.
    cmem : instance of CMem
        classical memory after executing circuit.
    info : dict
        result informations relating to the backend device

    """
    backend: Backend       = field(default=None, init=False)
    qubit_num: int         = field(default=None, init=False)
    cmem_num: int          = field(default=None, init=False)
    cid: list              = field(default=None, init=False)
    shots: int             = field(default=None, init=False)
    frequency: Counter     = field(default=None, init=False)
    start_time: datetime   = field(default=None, init=False)
    end_time: datetime     = field(default=None, init=False)
    elapsed_time: float    = field(default=None, init=False)
    qstate: QState         = field(default=None, init=False)
    stabilizer: Stabilizer = field(default=None, init=False)
    cmem: CMem             = field(default=None, init=False)
    info: dict             = field(default=None, init=False)

    def __str__(self):

        s = "backend: {}\n".format(self.backend)
        s += "qubit_num: {}\n".format(self.qubit_num)
        s += "cmem_num: {}\n".format(self.cmem_num)
        s += "cid: {}\n".format(self.cid)
        s += "shots: {}\n".format(self.shots)
        s += "frequency: {}\n".format(self.frequency)
        s += "start_time: {}\n".format(self.start_time)
        s += "end_time: {}\n".format(self.end_time)
        s += "elapsed_time: {}\n".format(self.elapsed_time)
        s += "info: {}\n".format(self.info)

        return s

    def show(self, verbose=False):
        """
        show the result.

        Parameters
        ----------
        verbose: bool
            verbose output or not
        None

        Returns
        -------
        None

        """
        s = ""
        if verbose is True:
            s += "[backend]\n"
            s += "- product      = {}\n".format(self.backend.product)
            s += "- device       = {}\n".format(self.backend.device)
            s += "[qubit & cmem]\n"
            s += "- qubit_num    = {}\n".format(self.qubit_num)
            s += "- cmem_num     = {}\n".format(self.cmem_num)
            s += "[measurement]\n"
            s += "- cid          = {}\n".format(self.cid)
            s += "- shots        = {}\n".format(self.shots)
            s += "[time]\n"
            s += "- start_time   = {}\n".format(self.start_time)
            s += "- end_time     = {}\n".format(self.end_time)
            s += "- elapsed_time = {:.6f} [sec]\n".format(self.elapsed_time)
            s += "[histogram]\n"

        if self.frequency is None:
            s += "None\n"
        else:
            digits = len(str(max(self.frequency.values())))

            for k, v in self.frequency.items():
                prob = v / self.shots
                if v > 0:
                    bar_graph = '+'
                bar_graph += '+' * int(prob * 30)
                if verbose is True:
                    bp = "- "
                else:
                    bp = ""
                s += (bp + "freq[{0:}] = {1:{digits}d} ({2:1.4f}) |{3:}\n"
                      .format(k, v, prob, bar_graph, digits=digits))

        print(s.rstrip())

    def save(self, file_path):
        """
        save the result

        Parameters
        ----------
        file_path: str
            file path of dump file

        Returns
        -------
        None

        """
        result_dict = {'backend': self.backend,
                       'qubit_num': self.qubit_num, 'cmem_num': self.cmem_num,
                       'cid': self.cid, 'shots': self.shots,
                       'frequency': self.frequency, 'start_time': self.start_time,
                       'end_time': self.end_time, 'elapsed_time': self.elapsed_time}

        with open(file_path, mode='wb') as f:
            pickle.dump(result_dict, f)

    @classmethod
    def load(cls, file_path):
        """
        load the result

        Parameters
        ----------
        file_path: str
            file path of dump file

        Returns
        -------
        result: instance of Result
            loaded circuit

        """
        with open(file_path, mode='rb') as f:
            result_dict = pickle.load(f)

        result = Result()
        result.backend = result_dict['backend']
        result.qubit_num = result_dict['qubit_num']
        result.cmem_num = result_dict['cmem_num']
        result.cid = result_dict['cid']
        result.shots = result_dict['shots']
        result.frequency = result_dict['frequency']
        result.start_time = result_dict['start_time']
        result.end_time = result_dict['end_time']
        result.elapsed_time = result_dict['elapsed_time']

        return result
