# -*- coding: utf-8 -*-
from qlazy.config import *
from qlazy.error import *

BACKEND_DEVICES = {'qlazy': ['qstate_simulator','stabilizer_simulator'],
                   'qulacs': ['cpu_simulator','gpu_simulator'],
                   'ibmq': ['qasm_simulator', 'least_busy']}

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
                if name == 'ibmq':
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
    def devices(cls, product=None):

        if product is None:
            return BACKEND_DEVICES
        else:
            return BACKEND_DEVICES[product]

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
