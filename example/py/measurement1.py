from qlazypy import QState

# initialize
qs = QState(2)

print("== initial state ==")
qs.show()
print("* amplitude = ", qs.amp)
print("* amplitude = ", qs.get_amp(id=[0]))

# measurement
qs.m(angle=0.5,phase=0.0).show() # measurement of X-axis

print("== state 1 ==")
qs.show()

# measurement
qs.m(angle=0.5,phase=0.0).show()

print("== state 2 ==")
qs.show()

qs.free()
