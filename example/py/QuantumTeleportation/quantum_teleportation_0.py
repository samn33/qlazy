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
    
# Alice execute Bell-measurement to her qubits 0,1
qs.cx(0,1).h(0)
b0 = qs.m([0],shots=1).lst
b1 = qs.m([1],shots=1).lst
print("== Bell measurement ==")
print("b0,b1 = ", b0,b1)

# Bob operate his qubit (id=2) according to the result
if b0 == 0 and b1 == 0:  # phi+
    pass
elif b0 == 0 and b1 == 1:  # psi+
    qs.x(2)
elif b0 == 1 and b1 == 0:  # psi-
    qs.z(2)
elif b0 == 1 and b1 == 1:  # phi-
    qs.x(2).z(2)

# final state (before teleportation)
print("== Alice (final) ==")
qs.show([0])
print("== Bob (final) ==")
qs.show([2])
