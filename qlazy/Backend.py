# -*- coding: utf-8 -*-
from qlazy.config import *
from qlazy.error import *

BACKEND_DEVICES = {'qlazy': ['qstate_simulator','stabilizer_simulator'],
                   'qulacs': ['cpu_simulator','gpu_simulator'],
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
        
        if product == None:
            if device == None:
                product = 'qlazy'
                device = 'qstate_simulator'
            else:
                raise Backend_Error_NameNotSpecified()            
        
        if product in BACKEND_DEVICES.keys():
            self.product = product

            if device in BACKEND_DEVICES[product]:
                self.device = device
            elif device == None:
                self.device = BACKEND_DEVICES[product][0]
            else:
                if product == 'ibmq':
                    self.device = device
                else:
                    raise Backend_Error_DeviceNotSupported()

        else:
            raise Backend_Error_NameNotSupported()

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
                raise Backend_Error_DeviceNotSupported()
            
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
                raise Backend_Error_DeviceNotSupported()
        
        # ibmq
        elif self.product == 'ibmq':
            from qlazy.backend.ibmq import run
            self.__run = run
    
        else:
            raise Backend_Error_NameNotSupported()

    @classmethod
    def products(cls):

        return list(BACKEND_DEVICES)

    @classmethod
    def qlazy_devices(cls):
        return BACKEND_DEVICES['qlazy']
    
    @classmethod
    def qulacs_devices(cls):
        return BACKEND_DEVICES['qulacs']
    
    @classmethod
    def ibmq_devices(cls):
        devices = BACKEND_DEVICES['ibmq']
        try:
            from qiskit import IBMQ
            provider = IBMQ.load_account()
            ibmq_backend_system_names = [b.name() for b in
                                         provider.backends(simulator=False, operational=True)]
        except Exception as e:
            print(e)
        else:
            devices += ['least_busy']
            devices += ibmq_backend_system_names
        
        return devices

    @classmethod
    def devices(cls, product):

        if product == 'qlazy':
            return Backend.qlazy_devices()
        elif product == 'qulacs':
            return Backend.qulacs_devices()
        elif product == 'ibmq':
            return Backend.ibmq_devices()
        else:
            raise ValueError("unknown product: {}".format(product))

    def run(self, qcirc=None, shots=1, cid=[]):
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
        >>> qc = QCirc.h(0).cx(0,1).measure(qid=[0],cid=[0]).x(0, ctrl=0).x(1, ctrl=0).measure(qid=[0,1], cid=[0,1])
        >>> result = bk.run(qcirc=qc, shots=100)
	>>> print(result.frequency)
        Counter({'00': 100})

        """
        result = self.__run(qcirc=qcirc, shots=shots, cid=cid, backend=self)
        return result
