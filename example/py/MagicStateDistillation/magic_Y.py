import random
import numpy as np
import matplotlib.pyplot as plt
import logging
from qlazy import QState
from qlazy.tools.Register import CreateRegister, InitRegister

EPS = 1.e-8
QS_Y = QState(qubit_num=1).h(0).s(0)

def init_qs_list(N, prob):

    return [QState(qubit_num=1).h(0).s(0).z(0) if random.uniform(0, 1) <= prob else QState(qubit_num=1).h(0).s(0) for i in range(N)]

def measure_X_stab(mval_list):

    p0 = (mval_list[3-1] + mval_list[4-1] + mval_list[5-1] + mval_list[6-1]) % 2
    p1 = (mval_list[2-1] + mval_list[5-1] + mval_list[6-1] + mval_list[7-1]) % 2
    p2 = (mval_list[1-1] + mval_list[4-1] + mval_list[6-1] + mval_list[7-1]) % 2
    if p0 == 0 and p1 == 0 and p2 == 0: return True
    else: return False

def measure_logical_X(mval_list):

    if sum(mval_list) % 2 == 0: return True
    else: return False

def distillation_Y(qs_list):

    data = CreateRegister(1)  # data qubit
    code = CreateRegister(7)  # logical qubit for Steane code
    anci = CreateRegister(1)  # ancilla qubit for S gate
    qubit_num = InitRegister(data, code, anci)
    qs = QState(qubit_num=qubit_num-len(anci))

    # bell state
    qs.h(data[0]).cx(data[0], code[6])

    # steane code
    qs.h(code[0]).h(code[1]).h(code[2])
    qs.cx(code[6], code[3]).cx(code[6], code[4])
    qs.cx(code[2], code[3]).cx(code[2], code[4]).cx(code[2], code[5])
    qs.cx(code[1], code[4]).cx(code[1], code[5]).cx(code[1], code[6])
    qs.cx(code[0], code[3]).cx(code[0], code[5]).cx(code[0], code[6])

    # S gates and measurements
    mval_list = []
    for i in range(7):
        qs_total = qs.tenspro(qs_list[i])
        qs_total.cx(code[i], anci[0]).h(anci[0]).cx(code[i], anci[0]).h(anci[0])
        mval = int(qs_total.mx(qid=[code[i]]).last)
        mval_list.append(mval)
        qs = qs_total.partial(qid=data+code)

    if measure_X_stab(mval_list) == False:
        return None

    qs_pat = qs_total.partial(qid=data)
    if measure_logical_X(mval_list) == True: qs_pat.z(0)
    
    return qs_pat

def prob_simulation(prob, trial):

    fail = 0
    for _ in range(trial):
        while True:
            qs_list = init_qs_list(7, prob)
            qs = distillation_Y(qs_list)
            if qs is not None: break
        if abs(qs.fidelity(QS_Y) - 1.0) > EPS: fail += 1
    return fail / trial

def prob_theoretical(p):

    u, v = 2 * p - 1, 1 - 2 * p
    return (1 + 7 * u**3 + 7 * u**4 + u**7) / (2 * (1 + 7 * v**4))

if __name__ == '__main__':

    # logging
    logger = logging.getLogger('ErrorSimulation')
    logger.setLevel(20)
    sh = logging.StreamHandler()
    fh = logging.FileHandler('error_simulation_Y.log', mode='w')
    logger.addHandler(sh)
    logger.addHandler(fh)
    
    # error probability (theoretical)
    prob_in = np.linspace(0.0, 0.4, 50)
    prob_out_linear = np.array([p for p in prob_in])
    prob_out_theoretical = np.array([prob_theoretical(p) for p in prob_in])

    # error probability (simulation)
    trial = 500
    prob_in_simulation = np.linspace(0.0, 0.4, 9)
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
    ax.set_title("magic state distillation: |Y>")
    ax.grid()
    ax.plot(prob_in, prob_out_theoretical, color='orange', label='theoretical')
    ax.plot(prob_in, prob_out_linear, color='gray', linestyle='dashed')
    ax.plot(prob_in_simulation, prob_out_simulation, color='green', label='simultion', marker='s')
    ax.legend(loc=0)
    fig.tight_layout()
    plt.savefig('error_simulation_Y.png')
    plt.show()
