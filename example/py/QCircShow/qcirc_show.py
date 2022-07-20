from qlazy import QCirc

def main():

    qc = QCirc.generate_random_gates(qubit_num=5, gate_num=10, phase=(0.0, 0.25, 0.5),
                                     prob={'h':7, 'cx':5, 'rx':3, 'crz':3})
    qc += QCirc().measure(qid=list(range(5)), cid=list(range(5)))
    qc += QCirc().h(0).x(0, ctrl=3).h(1).measure(qid=[2,1], cid=[10,4])
    print(qc)
    print()
    
    qc.show()

if __name__ == '__main__':

    main()
