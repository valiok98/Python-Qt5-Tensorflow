import sys
import numpy as np
import random
w_desired = 0.1
b_desired = 1.3

w1 = random.uniform(2, 10)
b1 = random.uniform(2 , 10)


learning_rate = 0.3
#sigma = 0.2

x_set = np.linspace(1.0, 200.0, num=10)
y_set = [w_desired*x_set[i] + b_desired for i in range(10)]
w_final = (y_set[1]-y_set[0])/(x_set[1]-x_set[0])
b_final = y_set[0] - w_final*x_set[0]


print(w_final, b_final)
print("Compared to: ")
print(w_desired, b_desired)

