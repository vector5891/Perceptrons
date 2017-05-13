import numpy as np

M = [[2,1,2,3],
     [3,4,1,2]]

N = [[3,4,2],
     [3,3,3],
     [5,1,6],
     [7,1,8]]

P = np.matmul(M,N)
print P

print "SIMULATING A SINGLE_LAYER NETWORK"
numInputs = 8
numOutputs = 4
inputs = np.random.rand(1,8)

weights = np.random.rand(8,4)
outputs = np.matmul(inputs, weights)
print outputs
