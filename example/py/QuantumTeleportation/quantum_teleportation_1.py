from qlazypy import QState

BELL_PHI_PLUS  = 0
BELL_PHI_MINUS = 3
BELL_PSI_PLUS  = 1
BELL_PSI_MINUS = 2

qs = QState(3)

# prepare qubit (id=0) that Alice want to send to Bob by rotating around X,Z
qs.ry(0,phase=0.3).rz(0,phase=0.4)

# make entangled 2 qubits (id=1 for Alice, id=2 for Bob)
qs.h(1).cx(1,2)

# initial state (before teleportation)
print("== Alice (initial) ==")
qs.show(id=[0])
print("== Bob (initial) ==")
qs.show(id=[2])
    
# Alice execute Bell-measurement to her qubits 0,1
print("== Bell measurement ==")
result = qs.mb(id=[0,1],shots=1).lst

# Bob operate his qubit (id=2) according to the result
if result == BELL_PHI_PLUS:
    print("result: phi+")
elif result == BELL_PSI_PLUS:
    print("result: psi+")
    qs.x(2)
elif result == BELL_PSI_MINUS:
    print("result: psi-")
    qs.x(2).z(2)
elif result == BELL_PHI_MINUS:
    print("result: phi-")
    qs.z(2)

# final state (before teleportation)
print("== Alice (final) ==")
qs.show(id=[0])
print("== Bob (final) ==")
qs.show(id=[2])

qs.free()
