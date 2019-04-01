from qlazypy.basic import QState

qs = QState(2)

qs.h(0)
qs.cx(0,1)
qs.show()

md = qs.m(shots=50)
md.show()

md.free()
qs.free()
