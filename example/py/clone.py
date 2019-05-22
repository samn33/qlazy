from qlazypy import QState

print("[source]")
qs_src = QState(1)
qs_src.h(0)
qs_src.show()

print("[destination]")
qs_dst = qs_src.clone()
qs_dst.show()

del qs_src
del qs_dst
