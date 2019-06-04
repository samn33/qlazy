from qlazypy import QState

qs = QState(2)

qs.h(0)
qs.cx(0,1)
qs.show()

md = qs.m(id=[0],shots=50)
md.show()

qs.free()
