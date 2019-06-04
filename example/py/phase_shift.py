from qlazypy import QState

theta = 0.3

qs = QState(1)
qs.h(0)

print("== phase shift (phase={}) ==".format(theta))
qs.p(0,phase=theta)
qs.show()
qs.p(0,phase=-theta)

print("== rotation Z (phase={}) ==".format(theta))
qs.rz(0,phase=theta)
qs.show()

qs.free()
