from qlazypy import QState

qs = QState(3)

print("* initial")
qs.x(0).x(1)
qs.show()

print("* final ")
qs.csw(0,1,2)

qs.show()

qs.free()
