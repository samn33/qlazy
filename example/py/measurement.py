from qlazypy.basic import QState

# initialize
qs = QState(2)

print("== initial state ==")
qs.show()
print("* amplitude = ", qs.amp)

# measurement
md = qs.m(angle=0.5,phase=0.0) # measurement of X-axis
md.show()

print("== state 1 ==")
qs.show()
print("* amplitude = ", qs.amp)

# measurement
md = qs.m(angle=0.5,phase=0.0)
md.show()

print("== state 2 ==")
qs.show()
print("* amplitude = ", qs.amp)

md.free()
qs.free()
