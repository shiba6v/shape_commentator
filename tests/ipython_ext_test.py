from IPython.testing.globalipapp import get_ipython
ip = get_ipython()
out = ip.run_cell("""
import shape_commentator
import numpy as np
""", store_history=True)

# test module import in a different cell
globals().update(ip.user_global_ns)

ip.run_cell_magic("shape",None,"""
a = np.array([1,2,3])
b = a
""")
