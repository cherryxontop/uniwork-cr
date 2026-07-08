import numpy as np
import matplotlib.pyplot as plt

#this is just a simple simulation to check the expected number of rolls to reach the 10th square

# constructing the transition matrix
P = np.zeros((10, 10))     #10x10 zero matrix

for i in range(9):
    for die in range(1, 7):
        target_square = i + die

        #if we overshoot the 10th square, stop on the 10th square
        if target_square > 9:
            P[i, 9] += 1

        else:
            P[i, target_square] += 1

P[9, 9] = 6

print(P.astype(int))
plt.matshow(P.astype(int), cmap="viridis")
plt.show()

# PART 2&3
P_prob = P / 6.0

P_tilde = P_prob[0:9, 0:9]
s = np.ones((9, 1))
I = np.eye(9)

h = np.round(np.linalg.solve(I - P_tilde, s), 2)
print("h =\n", h)

print("h flattened =\n", h.flatten())