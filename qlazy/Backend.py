# -*- coding: utf-8 -*-
""" Backend device of quantum computing """

import datetime

from qlazy.util import read_config_ini
from qlazy.gpu import is_gpu_available, is_gpu_supported_lib, gpu_preparation

BACKEND_DEVICES = {'qlazy': ['qstate_simulator',
                             'stabilizer_simulator',
                             'mps_simulator'],
                   'qulacs': ['cpu_simulator'],
                   'ibmq': ['aer_simulator',
                            'aer_simulator_statevector',
                            'aer_simulator_matrix_product_state'],
                   'braket_local': ['braket_sv'],
                   'braket_aws': ['sv1',
                                  'tn1',
                                  'dm1'],
                   'braket_ionq': ['ionq'],
                   'braket_rigetti': ['aspen_11',
                                      'aspen_m_1'],
                   'braket_oqc': ['lucy']}

BACKEND_DEVICES_GPU = {'qlazy': ['qstate_gpu_simulator'],
                       'qulacs': ['gpu_simulator']}

if is_gpu_available() is True and is_gpu_supported_lib() is True:
    gpu_preparation()
    USE_GPU = True
else:
    USE_GPU = False


class Backend:
    """ Backend device of quantum computing

    Attributes
    ----------
    product : str
        product name of the backend
        ('qlazy' or 'qulacs' or 'ibmq')
    device : str
        device name of the product
    config_braket : dict
        config for amazon braket backend
        {'backet_name': str, 'poll_timeout_seconds': int}

    Notes
    -----
    If you use amazon braket backend (braket_local, braket_aws,
    braket_ionq, braket_rigetti, braket_oqc), you must have
    config.ini file in your '~/.qlazy/' directory,
    and discribe like following example ...

    Example
    -------
    >>> bk = Backend(product='qlazy', device='stabilizer_simulator')
    >>> bk = Backend(product='qulacs', device='gpu_simulator')
    >>> bk = Backend(product='ibmq', device='least_busy')
    >>> bk = Backend(product='braket_rigetti', device='aspen_11') # read ~/.qlazy/config.ini
    ...
    $ cat ~/.qlazy/config.ini
    [backend_braket]
    backet_name = amazon-braket-xxxx # set your s3 backet name
    ...
    $ cat ~/.qlazy/config.ini
    [backend_braket]
    backet_name = amazon-braket-xxxx # set your s3 backet name
    poll_timeout_seconds = 86400  # set 1-day (default: 5-days)

    """
    def __init__(self, product=None, device=None):

        #
        # set attributes (product, device)
        #

        if product is None:
            self.product = 'qlazy'
            if device is None:
                self.device = 'qstate_simulator'
            else:
                self.device = device

        elif product in BACKEND_DEVICES.keys():
            self.product = product
            self.device = device

        else:
            raise ValueError("product:{} is unknown.".format(product))

        self.config_braket = None

        #
        # set method (__run)
        #

        # qlazy
        if self.product == 'qlazy':

            # qstate simulator
            if self.device == 'qstate_simulator':
                from qlazy.backend.qlazy_qstate_simulator import run_cpu
                self.__run = run_cpu

            # qstate simulator (GPU)
            elif self.device == 'qstate_gpu_simulator':
                from qlazy.backend.qlazy_qstate_simulator import run_gpu
                if USE_GPU is False:
                    raise ValueError("Your environment not support GPU.")
                self.__run = run_gpu

            # stabilizer simulator
            elif self.device == 'stabilizer_simulator':
                from qlazy.backend.qlazy_stabilizer_simulator import run
                self.__run = run

            # mps simulator
            elif self.device == 'mps_simulator':
                from qlazy.backend.qlazy_mps_simulator import run
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
                if USE_GPU is False:
                    raise ValueError("Your environment not support GPU.")
                self.__run = run_gpu

            else:
                raise ValueError("device:'{}' is unknown for product:'{}'."
                                 .format(self.device, self.product))

        # ibmq
        elif self.product == 'ibmq':
            from qlazy.backend.ibmq import run
            self.__run = run

        # braket
        elif self.product in ('braket_local', 'braket_aws',
                              'braket_ionq', 'braket_rigetti', 'braket_oqc'):
            from qlazy.backend.amazon_braket import run

            if self.product != 'braket_local' and self.config_braket is None:
                config_ini = read_config_ini()
                backet_name = config_ini['backend_braket'].get('backet_name')
                poll_timeout_seconds = config_ini['backend_braket'].get('poll_timeout_seconds')
                if poll_timeout_seconds is not None:
                    poll_timeout_seconds = int(poll_timeout_seconds)

                self.config_braket = {'backet_name': backet_name,
                                      'poll_timeout_seconds': poll_timeout_seconds}

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
        devices = BACKEND_DEVICES['qlazy']
        if is_gpu_supported_lib() is True and is_gpu_available() is True:
            devices += BACKEND_DEVICES_GPU['qlazy']
        return devices
        
    @classmethod
    def qulacs_devices(cls):
        """ get qulacs's devices list """
        devices = BACKEND_DEVICES['qulacs']
        if is_gpu_available() is True:
            devices += BACKEND_DEVICES_GPU['qulacs']
        return devices
        
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

        if product in ('qlazy', 'qulacs', 'braket_local', 'braket_aws',
                       'braket_ionq', 'braket_rigetti', 'braket_oqc'):
            device_list = BACKEND_DEVICES[product]
        elif product == 'qlazy':
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

    def run(self, qcirc=None, shots=1, cid=None, out_state=False, **kwargs):
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
        out_state : bool, default False
            output classical and quantum information after execting circuit.
            (only for qlazy's qstate and stabilizer simulator)

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
        result = self.__run(qcirc=qcirc, shots=shots, cid=cid, backend=self,
                            out_state=out_state, **kwargs)
        end_time = datetime.datetime.now()

        result.start_time = start_time
        result.end_time = end_time
        result.elapsed_time = (end_time - start_time).total_seconds()

        return result
