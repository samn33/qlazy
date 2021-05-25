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
    name : str
        name of the backend
        ('qlazy' or 'qulacs' or 'ibmq')
    device : str
        name of the quantum computing device
        ('qstate_simulator' or 'stabilizer_simulator' for 'qlazy', 
        'cpu_simulator' or 'gpu_simulator' for 'qulacs', 
        'qasm_simulator' or 'least_busy' or other quantum system name for 'ibmq')

    Example
    -------
    >>> bk = Backend(name='qlazy', device='stabilizer_simulator')
    >>> bk = Backend(name='qulacs', device='gpu_simulator')
    >>> bk = Backend(name='ibmq', device='least_busy')

    """

    def __init__(self, name=None, device=None):

        if name == None:
            if device == None:
                name = 'qlazy'
                device = 'qstate_simulator'
            else:
                raise Backend_Error_NameNotSpecified()            
        
        if name in BACKEND_DEVICES.keys():
            self.name = name

            if device in BACKEND_DEVICES[name]:
                self.device = device
            elif device == None:
                self.device = BACKEND_DEVICES[name][0]
            else:
                if name == 'ibmq':
                    self.device = device
                else:
                    raise Backend_Error_DeviceNotSupported()

        # not supported in the near future
        elif name in ('qlazy_qstate_simulator', 'qlazy_stabilizer_simulator',
                      'qulacs_simulator', 'qulacs_gpu_simulator', 'ibmq'):
            self.name = name
            
        else:
            raise Backend_Error_NameNotSupported()

