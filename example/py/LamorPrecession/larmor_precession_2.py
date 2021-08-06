from qlazy import QState,Observable

def main():

    hm = Observable("x_0")

    for i in range(21):
        t = i*0.05
        qs = QState(1)

        # time evolution
        qs.evolve(observable=hm, time=t, iter=100)

        # quantum stat in bloch spere
        theta, phi = qs.bloch(0)

        print("time = {0:.2f}, theta = {1:.2f}*PI, phi = {2:.2f}*PI"
              .format(t,theta,phi))

        # qs.free()
    
    # hm.free()
    
if __name__ == '__main__':
    main()
