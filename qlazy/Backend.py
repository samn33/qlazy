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
        name of the backend
        ('qlazy' or 'qulacs' or 'ibmq')
    device : str
        name of the quantum computing device
        ('qstate_simulator' or 'stabilizer_simulator' for 'qlazy', 
        'cpu_simulator' or 'gpu_simulator' for 'qulacs', 
        'qasm_simulator' or 'least_busy' or other quantum system name for 'ibmq')

    Example
    -------
    >>> bk = Backend(product='qlazy', device='stabilizer_simulator')
    >>> bk = Backend(product='qulacs', device='gpu_simulator')
    >>> bk = Backend(product='ibmq', device='least_busy')

    """

    def __init__(self, product=None, device=None):

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

    @classmethod
    def print(cls):

        for k,v in BACKEND_DEVICES.items():
            print("product: {}".format(k))
            print("- devices: {}".format(v))
