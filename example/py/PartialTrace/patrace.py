from qlazypy import QState, DensOp

qs = QState(4)

qs.h(0).h(1)  # unitary operation for 0,1-system
qs.x(2).z(3)  # unitary operation for 2,3-system

de1 = DensOp(qstate=[qs], prob=[1.0]) # product state
de1_reduced = de1.patrace([0,1])   # trace-out 0,1-system

print("== partial trace of product state ==")
print(" * trace = ", de1_reduced.trace())
print(" * square trace = ", de1_reduced.sqtrace())
    
qs.cx(1,3).cx(0,2)  # entangle between 0,1-system and 2,3-system

de2 = DensOp(qstate=[qs], prob=[1.0])  # entangled state
de2_reduced = de2.patrace([0,1])    # trace-out 0,1-system

print("== partial trace of entangled state ==")
print(" * trace = ", de2_reduced.trace())
print(" * square trace = ", de2_reduced.sqtrace())

print("== partial state of entangled state ==")
qs.show([2,3])

qs.free()
de1.free()
de2.free()
de1_reduced.free()
de2_reduced.free()
