from qlazypy import QState,DensOp

qs_pure = QState(1).h(0)     # (|0> + |1>) / sqrt(2.0)
de_pure = DensOp(qstate=[qs_pure], prob=[1.0])

qs_mixed_1 = QState(1)       # |0>
qs_mixed_2 = QState(1).x(0)  # |1>
de_mixed = DensOp(qstate=[qs_mixed_1,qs_mixed_2], prob=[0.5,0.5])

print("== pure state ==")
de_pure.show()
print("* trace =", de_pure.trace())
print("* square trace =", de_pure.sqtrace())
print("")
print("== mixed state ==")
de_mixed.show()
print("* trace =", de_mixed.trace())
print("* square trace =", de_mixed.sqtrace())
    
qs_pure.free()
qs_mixed_1.free()
qs_mixed_2.free()
    
de_pure.free()
de_mixed.free()
