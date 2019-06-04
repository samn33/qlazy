import math
from qlazypy import QState,Observable

def main():

    hm = Observable("x_0")
    ob_y = Observable("y_0")
    ob_z = Observable("z_0")

    for i in range(6):
        t = i*0.05
        qs = QState(1)

        # time evolution
        qs.evolve(observable=hm, time=t, iter=100)

        # expectation values of Observable Y,Z
        exp_y = qs.expect(observable=ob_y).real
        exp_z = qs.expect(observable=ob_z).real

        # argument
        if abs(exp_z)<0.00001: # exp_theta = 0.5*PI, if exp_z = 0.0 
            exp_theta = 0.5
        else:
            exp_theta = math.atan(exp_y/exp_z) / math.pi

        print("time = {0:.2f}, <y> = {1:.2f}, <z> = {2:.2f}, <theta> = {3:.2f}*PI"
              .format(t, exp_y, exp_z, exp_theta))

        qs.free()
    
    hm.free()
    
if __name__ == '__main__':
    main()
