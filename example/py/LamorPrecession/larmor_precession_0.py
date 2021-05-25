import math
import cmath
from qlazy import QState,Observable

def bloch(alpha,beta):

    # eliminate phase factor
    beta = beta / alpha
    alpha = 1.0

    # normalize
    norm = math.sqrt(1.0 + abs(beta)**2)
    alpha /= norm
    beta /= norm

    # (alpha,beta) => (theta,phi)
    theta = (2.0 * math.acos(alpha))
    if abs(alpha)<0.00001 or abs(beta)<0.00001: # north pole or south pole
        phi = 0.0
    else:
        phi = -cmath.phase(math.sin(theta/2.0) / beta)

    # unit => pi*radian
    theta /= math.pi
    phi /= math.pi
    
    return theta, phi
    
def main():

    hm = Observable("x_0")

    for i in range(21):
        t = i*0.05
        qs = QState(1)

        # time evolution
        qs.evolve(observable=hm, time=t, iter=100)

        # quantum stat in bloch spere
        theta, phi = bloch(qs.amp[0],qs.amp[1])

        print("time = {0:.2f}, theta = {1:.2f}*PI, phi = {2:.2f}*PI"
              .format(t,theta,phi))

        qs.free()
    
    hm.free()
    
if __name__ == '__main__':
    main()
