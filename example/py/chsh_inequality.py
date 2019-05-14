import random
from qlazypy import QState

def classical_strategy(trials=1000):

    win_cnt = 0
    for _ in range(trials):

        # random bits by Charlie (x,y)
        x = random.randint(0,1)
        y = random.randint(0,1)

        # response by Alice (a)
        a = 0

        # response by Bob (b)
        b = 0

        # count up if win
        if (x and y) == (a+b)%2:
            win_cnt += 1

    print("== result of classical strategy (trials:{0:d}) ==".format(trials))
    print("* win prob. = ", win_cnt/trials)

def quantum_strategy(trials=1000):

    win_cnt = 0
    for _ in range(trials):

        # random bits by Charlie (x,y)
        x = random.randint(0,1)
        y = random.randint(0,1)

        # make entangled 2 qubits (one for Alice and another for Bob)
        qs = QState(2).h(0).cx(0,1)
        
        # response by Alice (a)
        if x == 0:
            # measurement of Z-basis (= Ry(0.0)-basis)
            sa = qs.m(id=[0], shots=1, angle=0.0, phase=0.0).lst
            if sa == 0:
                a = 0
            else:
                a = 1
        else:
            # measurement of X-basis (or Ry(0.5*PI)-basis)
            sa = qs.mx(id=[0], shots=1).lst
            # sa = qs.m(id=[0], shots=1, angle=0.5, phase=0.0).lst
            if sa == 0:
                a = 0
            else:
                a = 1

        # response by Bob (b)
        if y == 0:
            # measurement of Ry(0.25*PI)-basis
            sb = qs.m(id=[1], shots=1, angle=0.25, phase=0.0).lst
            if sb == 0:
                b = 0
            else:
                b = 1
        else:
            # measurement of Ry(-0.25*PI)-basis
            sb = qs.m(id=[1], shots=1, angle=-0.25, phase=0.0).lst
            if sb == 0:
                b = 0
            else:
                b = 1

        # count up if win
        if (x and y) == (a+b)%2:
            win_cnt += 1

        del qs
            
    print("== result of quantum strategy (trials:{0:d}) ==".format(trials))
    print("* win prob. = ", win_cnt/trials)

if __name__ == '__main__':
    
    classical_strategy()
    quantum_strategy()
