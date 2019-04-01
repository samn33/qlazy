from qlazypy.basic import QState

# initialize
qs = QState(3)

# circuit
qs.h(0).h(1).h(2)
qs.rx(0,phase=0.5).cx(0,2) # angle = phase * PI = 0.5 * PI
qs.ry(0,phase=0.5).cx(1,0)
qs.rz(0,phase=0.5)
qs.h(0).h(1)

print("== final state ==")
qs.show()
print("* amplitude = ", qs.amp)

# measurement
md = qs.m(id=[0,1,2],shots=50)

print("== circuit ==")
qs.show("circ")

print("== measurement ==")
md.show()

print("* freq = ", md.frq)
print("* last = ", md.lst)

md.free()
qs.free()
