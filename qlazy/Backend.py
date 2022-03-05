# -*- coding: utf-8 -*-
""" Backend device of quantum computing """

import datetime

BACKEND_DEVICES = {'qlazy': ['qstate_simulator', 'stabilizer_simulator'],
                   'qulacs': ['cpu_simulator', 'gpu_simulator'],
                   'ibmq': ['aer_simulator', 'qasm_simulator']}

class Backend:
    """ Backend device of quantum computing

    Attributes
    ----------
    product : str
        product name of the backend
        ('qlazy' or 'qulacs' or 'ibmq')
    device : str
        device name of the product

    Example
    -------
    >>> bk = Backend(product='qlazy', device='stabilizer_simulator')
    >>> bk = Backend(product='qulacs', device='gpu_simulator')
    >>> bk = Backend(product='ibmq', device='least_busy')

    """

    def __init__(self, product=None, device=None):

        #
        # set attributes (procuct, device)
        #

        if product is None:
            self.product = 'qlazy'
            if device is None:
                self.device = 'qstate_simulator'
            elif device in BACKEND_DEVICES[product]:
                self.device = device
            else:
                raise ValueError("device:'{}' is unknown for product:'{}'."
                                 .format(device, self.product))

        elif product in BACKEND_DEVICES.keys():
            self.product = product
            if device in BACKEND_DEVICES[product]:
                self.device = device
            elif device is None:
                self.device = BACKEND_DEVICES[product][0]
            elif product == 'ibmq':
                self.device = device
            else:
                raise ValueError("device:'{}' is unknown for product:'{}'."
                                 .format(device, self.product))

        else:
            raise ValueError("product:{} is unknown.".format(product))

        #
        # set method (__run)
        #

        # qlazy
        if self.product == 'qlazy':

            # qstate simulator
            if self.device == 'qstate_simulator':
                from qlazy.backend.qlazy_qstate_simulator import run
                self.__run = run

            # stabilizer simulator
            elif self.device == 'stabilizer_simulator':
                from qlazy.backend.qlazy_stabilizer_simulator import run
                self.__run = run

            else:
                raise ValueError("device:'{}' is unknown for product:'{}'."
                                 .format(self.device, self.product))

        # qulacs
        elif self.product == 'qulacs':

            # cpu_simulator
            if self.device == 'cpu_simulator':
                from qlazy.backend.qulacs_simulator import run_cpu
                self.__run = run_cpu

            # gpu_simulator
            elif self.device == 'gpu_simulator':
                from qlazy.backend.qulacs_simulator import run_gpu
                self.__run = run_gpu

            else:
                raise ValueError("device:'{}' is unknown for product:'{}'."
                                 .format(self.device, self.product))

        # ibmq
        elif self.product == 'ibmq':
            from qlazy.backend.ibmq import run
            self.__run = run

        else:
            raise ValueError("device:'{}' is unknown for product:'{}'."
                             .format(self.device, self.product))

    @classmethod
    def products(cls):
        """ get products list """
        return list(BACKEND_DEVICES)

    @classmethod
    def qlazy_devices(cls):
        """ get qlazy's devices list """
        return BACKEND_DEVICES['qlazy']

    @classmethod
    def qulacs_devices(cls):
        """ get qulacs's devices list """
        return BACKEND_DEVICES['qulacs']

    @classmethod
    def ibmq_devices(cls):
        """ get ibmq's devices list """
        devices = BACKEND_DEVICES['ibmq']
        try:
            from qiskit import IBMQ
            provider = IBMQ.load_account()
            ibmq_backend_system_names = [b.name() for b in
                                         provider.backends(simulator=False, operational=True)]
        except Exception:
            pass
        else:
            devices += ['least_busy']
            devices += ibmq_backend_system_names

        return devices

    @classmethod
    def devices(cls, product):
        """ get devices list for the product """

        if product == 'qlazy':
            device_list = Backend.qlazy_devices()
        elif product == 'qulacs':
            device_list = Backend.qulacs_devices()
        elif product == 'ibmq':
            device_list = Backend.ibmq_devices()
        else:
            raise ValueError("unknown product: {}".format(product))

        return device_list

    def __str__(self):

        backend_dict = {'product': self.product, 'device': self.device}
        return str(backend_dict)

    def run(self, qcirc=None, shots=1, cid=None):
        """
        run the quantum circuit.

        Parameters
        ----------
        qcirc : instance of QCirc, default None
            quantum circuit.
        shots : int, default 1
            number of measurements.
        cid : list, default []
            classical register id list to count frequency.

        Returns
        -------
        result : incetance of Result
            measurement result.

        Examples
        --------
        >>> # simple example
        >>> from qlazy import QCirc, Backend
        >>> bk = Backend(product='qlazy', device='qstate_simulator')
        >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
        >>> result = bk.run(qcirc=qc, shots=100)
        >>> print(result.frequency)
        Counter({'00': 51, '11': 49})
        >>> ...
        >>> # control quantum gate by measured results
        >>> from qlazy import QCirc, Backend
        >>> bk = Backend(product='qlazy', device='qstate_simulator')
        >>> qc = QCirc.h(0)
        >>> qc.cx(0,1).measure(qid=[0],cid=[0])
        >>> qc.x(0, ctrl=0).x(1, ctrl=0).measure(qid=[0,1], cid=[0,1])
        >>> result = bk.run(qcirc=qc, shots=100)
	>>> print(result.frequency)
        Counter({'00': 100})

        """
        start_time = datetime.datetime.now()
        result = self.__run(qcirc=qcirc, shots=shots, cid=cid, backend=self)
        end_time = datetime.datetime.now()

        result.start_time = start_time
        result.end_time = end_time
        result.elapsed_time = (end_time - start_time).total_seconds()

        return result
