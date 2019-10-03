from qlazypy import QState

qs = QState(2)
qs.x(0)

print("== initial ===")
qs.show()

qs.sw(0,1)

print("== final ===")
qs.show()

qs.free()
