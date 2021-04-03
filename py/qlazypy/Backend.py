# -*- coding: utf-8 -*-

class Backend:
    """ Backend device of quantum computing

    Attributes
    ----------
    name : str, default 'qlazy_qstate_simulator'
        name of the quantum computing device
        ('qlazy_qstate_simulator', 'qlazy_stabilizer_simulator','qulacs_simulator', 'qulacs_gpu_simulator')

    """

    def __init__(self, name='qlazy_qstate_simulator'):

        if name in ('qlazy_qstate_simulator', 'qlazy_stabilizer_simulator',
                    'qulacs_simulator', 'qulacs_gpu_simulator'):
            self.name = name
        else:
            raise Backend_Error_NameNotSupported()

