import numpy as np

a = np.array([1,2,3,4,5,6])  #_ rewrite it!
b = np.array([0,1,2,3,4,5])  #_ rewrite it!

ab_h = np.hstack((a,b))  #_ rewrite it!
ab_v = np.vstack((a,b))  #_ rewrite it!
ab = np.dot(a,b)  #_ rewrite it!
AA, BB = np.meshgrid(a,b)  #_ rewrite it!
