from qlazypy import QState

qs = QState(3)

print("* initial")
qs.x(0).x(1)
qs.show()

print("* toffoli")
#qs.ccx(0,1,2)

qs.cxr(1,2).cx(0,1).cxr_dg(1,2).cx(0,1).cxr(0,2)
qs.show()

qs.free()
