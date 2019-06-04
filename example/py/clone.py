from qlazypy import QState

print("[source]")
qs_src = QState(3)
qs_src.h(0)
qs_src.h(1)
qs_src.h(2)
print(qs_src)
qs_src.show()

print("[destination]")
qs_dst = qs_src.clone()
print(qs_dst)
qs_dst.show()

qs_src.free()
qs_dst.free()
