from qlazypy import QState

def swap(self,q0,q1):

    self.cx(q0,q1)
    self.cx(q1,q0)
    self.cx(q0,q1)
    return self

def main():

    QState.swap = swap
    
    qs = QState(2).x(0)

    print("== initial ==")
    qs.show()
    qs.swap(0,1)
    print("== after operating swap gate ==")
    qs.show()

    qs.free()

if __name__ == '__main__':
    main()
