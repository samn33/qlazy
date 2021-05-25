import math
from qlazy import QState

def measure(phase):

    qs = QState(1)
    qs.h(0)
    freq_list = qs.m([0], shots=100, angle=0.5, phase=phase).frq
    prob = freq_list[0] / 100

    print("===")
    print("phase = {0:.4f} PI".format(phase))
    print("[measured] prob. of up-spin = {0:.4f}".format(prob))
    print("[theoretical] cos(phase/2)^2 = {0:.4f}".format((math.cos(phase*math.pi/2))**2))

    qs.free()

def main():

    measure(0.0)
    measure(0.25)
    measure(0.5)
    measure(0.75)
    measure(1.0)

if __name__ == '__main__':
    main()
