from qlazy import QCirc, Backend
from qlazy.Observable import X,Y,Z

def real_qc_run():

    shots = 100
    qc = QCirc()
    qc.h(0).x(0).z(0).s(0).t(0).s_dg(0).t_dg(0).rx(0, phase=0.1).rz(0, phase=0.2)
    qc.cx(0,1).cz(0,1).ch(0,1).crz(0,1, phase=0.3)
    qc.measure(qid=[0,1], cid=[0,1]) # {'00': 50, '10': 25, '11': 25}
    # qc.measure(qid=[0], cid=[0]) # {'0': 50, '1': 59}
    # qc.measure(qid=[1], cid=[1]) # {'00': 75, '01': 25}
    # qc.measure(qid=[0,1], cid=[1,0]) # {'00': 50, '01': 25, '11': 25}
    # qc.measure(qid=[0,1], cid=[1,3]) # {'0000': 50, '0100': 25, '0101': 25}
    # qc.measure(qid=[0,1], cid=[3,1]) # {'0000': 50, '0001': 25, '0101': 25}
    
    # bk = Backend()  # OK

    # bk = Backend(product='ibmq', device='aer_simulator') # OK
    # bk = Backend(product='ibmq', device='least_busy') # OK
    # bk = Backend(product='qulacs', device='cpu_simulator') # OK

    # bk = Backend(product='braket_local', device='braket_sv') # OK
    # bk = Backend(product='braket_aws', device='sv1') # OK
    # bk = Backend(product='braket_aws', device='tn1') # OK
    # bk = Backend(product='braket_aws', device='dm1') # OK

    # bk = Backend(product='braket_ionq', device='ionq') # OK
    # bk = Backend(product='braket_rigetti', device='aspen_11')
    # bk = Backend(product='braket_rigetti', device='aspen_m_1') # OK
    # bk = Backend(product='braket_oqc', device='lucy') # OK

    result = bk.run(qcirc=qc, shots=shots)
    result.show(verbose=True)

def real_qc_expect():

    ob = 0.5*X(0)*X(1)
    qc = QCirc().h(0).h(1).h(2).h(3)

    bk = Backend()  # OK

    # bk = Backend(product='ibmq', device='aer_simulator') # OK
    # bk = Backend(product='ibmq', device='least_busy') # OK
    # bk = Backend(product='qulacs', device='cpu_simulator') # OK

    # bk = Backend(product='braket_local', device='braket_sv') # OK
    # bk = Backend(product='braket_aws', device='sv1') # OK
    # bk = Backend(product='braket_aws', device='tn1') # OK
    # bk = Backend(product='braket_aws', device='dm1') # OK

    # bk = Backend(product='braket_ionq', device='ionq') # OK
    # bk = Backend(product='braket_rigetti', device='aspen_11')
    # bk = Backend(product='braket_rigetti', device='aspen_m_1') # OK
    # bk = Backend(product='braket_oqc', device='lucy') # OK

    print("* exp (theoretical) = 0.5+0.j")
    expval = bk.expect(qcirc=qc, observable=ob, shots=1000)
    print("* exp (real qc)     = {}".format(expval))

if __name__ == '__main__':

    # real_qc_run()
    real_qc_expect()
