from qlazypy import QState

def main():

    print("== hadamard gate ==")

    print("** one-way quantum computing")

    # graph state
    qs_oneway = QState(5)
    qs_oneway.h(1).h(2).h(3).h(4)
    qs_oneway.cz(0,1).cz(1,2).cz(2,3).cz(3,4)

    # measurement
    qs_oneway.mx(id=[0], shots=1)
    qs_oneway.my(id=[1], shots=1)
    qs_oneway.my(id=[2], shots=1)
    qs_oneway.my(id=[3], shots=1)

#    qs_oneway.m(id=[0], shots=1, angle=0.5, phase=0.0)
#    qs_oneway.m(id=[1], shots=1, angle=0.5, phase=0.5)
#    qs_oneway.m(id=[2], shots=1, angle=0.5, phase=0.5)
#    qs_oneway.m(id=[3], shots=1, angle=0.5, phase=0.5)

    # result state
    qs_oneway.show(id=[4])

    print("** conventianal quantum gate")

    qs_gate = QState(1)
    qs_gate.h(0)
    qs_gate.show()

    del qs_oneway
    del qs_gate
    
if __name__ == '__main__':
    main()
