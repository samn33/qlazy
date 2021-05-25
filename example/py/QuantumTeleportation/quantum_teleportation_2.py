from qlazy import QState

qs = QState(3)

# prepare qubit (id=0) that Alice want to send to Bob by rotating around X,Z
qs.ry(0,phase=0.3).rz(0,phase=0.4)

# make entangled 2 qubits (id=1 for Alice, id=2 for Bob)
qs.h(1).cx(1,2)

# initial state (before teleportation)
print("== Alice (initial) ==")
qs.show([0])
print("== Bob (initial) ==")
qs.show([2])
    
# equivalent to quantum teleportation
qs.cx(0,1).h(0)
qs.cx(1,2)
qs.cz(0,2)

# final state (before teleportation)
print("== Alice (final) ==")
qs.show([0])
print("== Bob (final) ==")
qs.show([2])

qs.free()
