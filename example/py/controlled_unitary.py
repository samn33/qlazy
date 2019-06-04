from qlazypy import QState

def main():
    qs = QState(2)
    qs.h(0).cp(0,1)
    qs.show()
    qs.free()

if __name__ == '__main__':
    main()
