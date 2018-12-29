import numpy as np

a = np.array([1,2,3,4,5,6])  #_ (6,),
b = np.array([0,1,2,3,4,5])  #_ (6,),

ab_h = np.hstack((a,b))  #_ (12,),
ab_v = np.vstack((a,b))  #_ (2, 6),
ab = np.dot(a,b)  #_ (),
AA, BB = np.meshgrid(a,b)  #_ ((6, 6),(6, 6),)

