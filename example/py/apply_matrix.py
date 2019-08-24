import numpy as np
from qlazypy import QState

qs = QState(2)
qs.show()
matrix = np.array([[1,0,0,0],
                   [0,1,0,0],
                   [0,0,0,1],
                   [0,0,1,0]])
print(matrix)

qs.h(0)
qs.apply(matrix).x(0)
qs.show()
qs.free()
