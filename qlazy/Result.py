# -*- coding: utf-8 -*-
""" Result of quantum circuit execution """

from collections import Counter
import datetime
import pickle

from qlazy.Backend import Backend

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
    start_time : instance of datetime.datetime
        start time to ececute the quantum circuit.
    end_time : instance of datetime.datetime
        end time to ececute the quantum circuit.
    elapsed_time : float
        elapsed time to ececute the quantum circuit.
    info : dict
        result informations relating to the backend device

    """
    def __init__(self):

        self.__backend = None
        self.__qubit_num = None
        self.__cmem_num = None
        self.__cid = None
        self.__shots = None
        self.__frequency = None
        self.__start_time = None
        self.__end_time = None
        self.__elapsed_time = None
        self.__info = None

    # backend

    @property
    def backend(self):
        """ getter of backend """
        return self.__backend

    @backend.setter
    def backend(self, backend):
        """ setter of backend """
        if isinstance(backend, Backend) is False:
            raise TypeError("type of backend must be Backend.")
        self.__backend = backend

    # qubit_num

    @property
    def qubit_num(self):
        """ getter of qubit_num """
        return self.__qubit_num

    @qubit_num.setter
    def qubit_num(self, qubit_num):
        """ setter of qubit_num """
        if isinstance(qubit_num, int) is False:
            raise TypeError("type of qubit_num must be int.")
        self.__qubit_num = qubit_num

    # cmem_num

    @property
    def cmem_num(self):
        """ getter of cmem_num """
        return self.__cmem_num

    @cmem_num.setter
    def cmem_num(self, cmem_num):
        """ getter of cmem_nem """
        if isinstance(cmem_num, int) is False:
            raise TypeError("type of cmem_num must be int.")
        self.__cmem_num = cmem_num

    # cid

    @property
    def cid(self):
        """ getter of cid """
        return self.__cid

    @cid.setter
    def cid(self, cid):
        """ setter of cid """
        if isinstance(cid, list) is False:
            raise TypeError("type of cid must be list.")
        self.__cid = cid

    # shots

    @property
    def shots(self):
        """ getter of shots """
        return self.__shots

    @shots.setter
    def shots(self, shots):
        """ setter of shots """
        if isinstance(shots, int) is False:
            raise TypeError("type of shots must be int.")
        self.__shots = shots

    # frequency

    @property
    def frequency(self):
        """ getter of frequency """
        return self.__frequency

    @frequency.setter
    def frequency(self, frequency):
        """ setter of frequency """
        if isinstance(frequency, Counter) is False and frequency is not None:
            raise TypeError("type of frequency must be Counter.")
        self.__frequency = frequency

    # start_time

    @property
    def start_time(self):
        """ getter of start_time """
        return self.__start_time

    @start_time.setter
    def start_time(self, start_time):
        """ setter of start_time """
        if isinstance(start_time, datetime.datetime) is False:
            raise TypeError("type of sart_time must be datetime.datetime.")
        self.__start_time = start_time

    # end_time

    @property
    def end_time(self):
        """ getter of end_time """
        return self.__end_time

    @end_time.setter
    def end_time(self, end_time):
        """ setter of end_time """
        if isinstance(end_time, datetime.datetime) is False:
            raise TypeError("type of end_time must be datetime.datetime.")
        self.__end_time = end_time

    # elapsed_time

    @property
    def elapsed_time(self):
        """ getter of elapsed_time """
        return self.__elapsed_time

    @elapsed_time.setter
    def elapsed_time(self, elapsed_time):
        """ setter of elapsed_time """
        if isinstance(elapsed_time, float) is False:
            raise TypeError("type of elaased_time must be float.")
        self.__elapsed_time = elapsed_time

    # info

    @property
    def info(self):
        """ getter of info
            (for device dependent informattion)
        """
        return self.__info

    @info.setter
    def info(self, info):
        """ setter of info """
        if isinstance(info, dict) is False and info is not None:
            raise TypeError("type of info must be dict.")
        self.__info = info

    def __str__(self):

        s = "backend: {}\n".format(self.__backend)
        s += "qubit_num: {}\n".format(self.__qubit_num)
        s += "cmem_num: {}\n".format(self.__cmem_num)
        s += "cid: {}\n".format(self.__cid)
        s += "shots: {}\n".format(self.__shots)
        s += "frequency: {}\n".format(self.__frequency)
        s += "start_time: {}\n".format(self.__start_time)
        s += "end_time: {}\n".format(self.__end_time)
        s += "elapsed_time: {}\n".format(self.__elapsed_time)
        s += "info: {}\n".format(self.__info)

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
            s += "- product      = {}\n".format(self.__backend.product)
            s += "- device       = {}\n".format(self.__backend.device)
            s += "[qubit & cmem]\n"
            s += "- qubit_num    = {}\n".format(self.__qubit_num)
            s += "- cmem_num     = {}\n".format(self.__cmem_num)
            s += "[measurement]\n"
            s += "- cid          = {}\n".format(self.__cid)
            s += "- shots        = {}\n".format(self.__shots)
            s += "[time]\n"
            s += "- start_time   = {}\n".format(self.__start_time)
            s += "- end_time     = {}\n".format(self.__end_time)
            s += "- elapsed_time = {:.6f} [sec]\n".format(self.__elapsed_time)
            s += "[histogram]\n"

        if self.__frequency is None:
            s += "None\n"
        else:
            digits = len(str(max(self.__frequency.values())))

            for k, v in self.__frequency.items():
                prob = v / self.__shots
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
        result_dict = {'backend': self.__backend,
                       'qubit_num': self.__qubit_num, 'cmem_num': self.__cmem_num,
                       'cid': self.__cid, 'shots': self.__shots,
                       'frequency': self.__frequency, 'start_time': self.__start_time,
                       'end_time': self.__end_time, 'elapsed_time': self.__elapsed_time}

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
