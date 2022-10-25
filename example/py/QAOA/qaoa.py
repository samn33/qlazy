from scipy.optimize import minimize
from qlazy import Observable, Backend, ParametricQCirc
from qlazy.Observable import X, Y, Z

def make_ob(graph):
    """ make observable for QAOA """

    ob = Observable()
    for i,j in graph:
        ob += 0.5*Z(i)*Z(j)

    return ob

def make_pqc(graph, p=1):
    """ make parametric quantum circuit for QAOA """

    node_num = max([max(i,j) for i,j in graph]) + 1
    pqc = ParametricQCirc()

    for i in range(node_num):
        pqc.h(i)

    for k in range(p):
        for i, j in graph:
            pqc.cx(i,j)
            pqc.rz(j, tag='g[{}]'.format(k))
            pqc.cx(i,j)
        for i in range(node_num):
            pqc.rx(i, tag='b[{}]'.format(k))

    return pqc

def main():    

    # graph for max-cut
    #
    # ex)  0---1
    #      |   |
    #      3---2
    #
    graph = ((0,1), (1,2), (2,3), (3,0))

    # observable
    ob = make_ob(graph)
    
    # parametric quantum circuit
    pqc = make_pqc(graph, p=2)

    # backend
    bk = Backend(product='qlazy', device='qstate_simulator')

    def callback(x):
        print("energy = ", get_expval(x))

    def get_params(x):
        params = {}
        for i, v in enumerate(x):
            if i%2 == 0: s = 'g'
            else: s = 'b'
            params['{}[{}]'.format(s, str(i//2))] = v
        return params
        
    def get_expval(x):
        params = get_params(x)
        pqc.set_params(params)
        result = bk.run(qcirc=pqc, out_state=True)
        qs = result.qstate
        expval = qs.expect(observable=ob).real
        return expval

    # execute QAOA
    init = [0.05, 0.05, 0.1, 0.1]
    callback(init)
    res = minimize(get_expval, init, method='Powell', callback=callback)

    # final state
    params = get_params(res.x)
    pqc.set_params(params)
    result = bk.run(qcirc=pqc, out_state=True)
    result.qstate.show()

if __name__ == '__main__':
    main()
