from qlazypy import QState, DensOp

if __name__ == '__main__':

    qs = QState(4)
    [qs.h(i) for i in range(3)]
    #qs.mcx([0,1,2],3)
    qs.show()

    de = DensOp(qstate=[qs])
    de.mcx([0,1,2],3)
    de.show()

    (qs_list, prb_list) = de.spectrum()
    [qs_list[i].show() for i in range(len(qs_list))]
