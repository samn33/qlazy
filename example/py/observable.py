from qlazypy import QState,Observable

def main():

    qs = QState(2)
    qs.x(0)
    
    hm = Observable("z_0*z_1+x_0+x_1")
    ob = Observable("2.0+z_0+z_1")
    
    qs.evolve(observable=hm,time=0.1,iter=10)
    print("** time evolution")
    qs.show()

    e = qs.expect(observable=ob)
    print("** expectation value = ",e)

    qs_ini = QState(2)
    v = qs.inpro(qs_ini)
    print("** inner product = ", v)
    
    del qs
    del qs_ini
    del hm
    del ob
    
if __name__ == '__main__':
    main()
