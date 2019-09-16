import numpy as np
from qlazypy import QState

qs = QState(4)
id = [3,2]

qs.show(id=id)

qs.h(id[0])
matrix = np.array([[1,0,0,0],
                   [0,1,0,0],
                   [0,0,0,1],
                   [0,0,1,0]])
print(matrix)
qs.apply(matrix=matrix, id=id)
qs.show(id=id)

qs.free()
