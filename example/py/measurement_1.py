from qlazypy import QState

qs = QState(1)

print("== initial state ==")
qs.show()

qs.mx().show()
qs.mx().show()
qs.mz().show()

print("== state ==")
qs.show()

del qs
