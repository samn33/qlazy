import random
import numpy as np
import matplotlib.pyplot as plt
import logging
from qlazy import QState
from qlazy.tools.Register import CreateRegister, InitRegister

EPS = 1.e-8
QS_A = QState(qubit_num=1).h(0).t(0)

def init_qs_list(N, prob):

    return [QState(qubit_num=1).h(0).t(0).z(0) if random.uniform(0, 1) <= prob else QState(qubit_num=1).h(0).t(0) for i in range(N)]

def measure_X_stab(mval_list):

    s0 = sum([mval_list[q-1] for q in [1,6,7,10,11,12,13,15]]) % 2
    s1 = sum([mval_list[q-1] for q in [2,5,7,9,11,12,14,15]]) % 2
    s2 = sum([mval_list[q-1] for q in [3,4,7,9,10,13,14,15]]) % 2
    s3 = sum([mval_list[q-1] for q in [3,5,6,8,11,13,14,15]]) % 2
    if s0 == 0 and s1 == 0 and s2  == 0 and s3 == 0: return True
    else: return False

def measure_logical_X(mval_list):

    if sum(mval_list) % 2 == 0: return True
    else: return False

def distillation_A(qs_list):

    data = CreateRegister(1)   # data qubit
    code = CreateRegister(15)  # logical qubit for Steane code
    anci = CreateRegister(1)   # ancilla qubit for S gate
    qubit_num = InitRegister(data, code, anci)
    qs = QState(qubit_num=qubit_num-len(anci))

    # bell state
    qs.h(data[0]).cx(data[0], code[14])

    # Reed-Muler code
    [qs.h(code[q-1]) for q in [1,2,4,8]]
    [qs.cx(code[8-1], code[q-1]) for q in [9,10,11,12,13,14,15]]
    [qs.cx(code[4-1], code[q-1]) for q in [5,6,7,12,13,14,15]]
    [qs.cx(code[2-1], code[q-1]) for q in [3,6,7,10,11,14,15]]
    [qs.cx(code[1-1], code[q-1]) for q in [3,5,7,9,11,13,15]]
    [qs.cx(code[15-1], code[q-1]) for q in [3,5,6,9,10,12]]

    # T_dag gates and measurements
    mval_list = []
    for i in range(15):
        qs_total = qs.tenspro(qs_list[i])
        m = qs_total.cx(anci[0], code[i]).m(qid=[code[i]]).last
        if m == '1': qs_total.x(anci[0])
        else: qs_total.s_dg(anci[0])
        mval = int(qs_total.mx(qid=[anci[0]]).last)
        mval_list.append(mval)
        qs = qs_total.partial(qid=data+code)

    if measure_X_stab(mval_list) == False: return None

    qs_pat = qs_total.partial(qid=data)
    if measure_logical_X(mval_list) == False: qs_pat.z(0)

    return qs_pat

def prob_simulation(prob, trial):

    fail = 0
    for i in range(trial):
        while True:
            qs_list = init_qs_list(15, prob)
            qs = distillation_A(qs_list)
            if qs is not None: break
        if abs(qs.fidelity(QS_A) - 1.0) > EPS: fail += 1
        print("[{}] fail/trial = {}/{}".format(i, fail, trial))
    return fail / trial

def prob_theoretical(p):

    u, v = 2 * p - 1, 1 - 2 * p
    return (1 + 15 * u**8 + 15 * u**7 + u**15) / (2 * (1 + 15 * v**8))

if __name__ == '__main__':

    # logging
    logger = logging.getLogger('ErrorSimulation')
    logger.setLevel(20)
    sh = logging.StreamHandler()
    fh = logging.FileHandler('error_simulation_A.log', mode='w')
    logger.addHandler(sh)
    logger.addHandler(fh)
    
    # error probability (theoretical)
    prob_in = np.linspace(0.0, 0.3, 50)
    prob_out_linear = np.array([p for p in prob_in])
    prob_out_theoretical = np.array([prob_theoretical(p) for p in prob_in])
    
    # error probability (simulation)
    trial = 500
    prob_in_simulation = np.linspace(0.0, 0.3, 7)
    logger.info("{0:}, {1:}, {2:}".format("in", "out(simulation)", "out(theoretical)"))
    prob_out_simulation = []
    for p_in in prob_in_simulation:
        p_out = prob_simulation(p_in, trial)
        logger.info("{0:.6f}, {1:.6f} {2:.6f}".format(p_in, p_out, prob_theoretical(p_in)))
        prob_out_simulation.append(p_out)

    # plot
    fig, ax = plt.subplots()
    ax.set_xlabel("error probability (in)")
    ax.set_ylabel("error probability (out)")
    ax.set_title("magic state distillation: |A>")
    ax.grid()
    ax.plot(prob_in, prob_out_theoretical, color='orange', label='theoretical')
    ax.plot(prob_in, prob_out_linear, color='gray', linestyle='dashed')
    ax.plot(prob_in_simulation, prob_out_simulation, color='green', label='simultion', marker='s')
    ax.legend(loc=0)
    fig.tight_layout()
    plt.savefig('error_simulation_A.png')
    plt.show()
