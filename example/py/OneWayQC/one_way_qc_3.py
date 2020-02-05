import random
from qlazypy import QState

def main():

    print("== CNOT gate ==")

    print("** one-way quantum computing")

    # graph state
    qs_oneway = QState(15)
    qs_oneway.h(0)
    qs_oneway.h(1).h(2).h(3).h(4).h(5).h(6).h(7)
    qs_oneway.h(9).h(10).h(11).h(12).h(13).h(14)
    qs_oneway.cz(0,1).cz(1,2).cz(2,3).cz(3,4).cz(4,5).cz(5,6)
    qs_oneway.cz(3,7).cz(7,11)
    qs_oneway.cz(8,9).cz(9,10).cz(10,11).cz(11,12).cz(12,13).cz(13,14)

    # measurement
    qs_oneway.mx([0], shots=1)
    qs_oneway.my([1], shots=1)
    qs_oneway.my([2], shots=1)
    qs_oneway.my([3], shots=1)
    qs_oneway.my([4], shots=1)
    qs_oneway.my([5], shots=1)
    qs_oneway.my([7], shots=1)
    qs_oneway.mx([8], shots=1)
    qs_oneway.mx([9], shots=1)
    qs_oneway.mx([10], shots=1)
    qs_oneway.my([11], shots=1)
    qs_oneway.mx([12], shots=1)
    qs_oneway.mx([13], shots=1)

    qs_oneway.show([6,14])

    print("** conventianal quantum gate")

    qs_gate = QState(2)
    qs_gate.h(0)
    qs_gate.cx(0,1)
    qs_gate.show()

    qs_oneway.free()
    qs_gate.free()
    
if __name__ == '__main__':
    main()
