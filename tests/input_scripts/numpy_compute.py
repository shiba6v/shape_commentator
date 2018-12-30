import numpy as np

a = np.array([1,2,3,4,5,6])
b = np.array([0,1,2,3,4,5])

ab_h = np.hstack((a,b))
ab_v = np.vstack((a,b))
ab = np.dot(a,b)
AA, BB = np.meshgrid(a,b)
a_b = (a,b)
