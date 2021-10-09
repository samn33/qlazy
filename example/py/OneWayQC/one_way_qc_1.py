from qlazy import QState

def main():

    print("== hadamard gate ==")

    print("** one-way quantum computing")

    # graph state
    qs_oneway = QState(5)
    qs_oneway.h(1).h(2).h(3).h(4)
    qs_oneway.cz(0,1).cz(1,2).cz(2,3).cz(3,4)

    # measurement
    qs_oneway.mx([0], shots=1)
    qs_oneway.my([1], shots=1)
    qs_oneway.my([2], shots=1)
    qs_oneway.my([3], shots=1)

    # result state
    qs_oneway.show([4])

    print("** conventianal quantum gate")

    qs_gate = QState(1)
    qs_gate.h(0)
    qs_gate.show()

if __name__ == '__main__':
    main()
