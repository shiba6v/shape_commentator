from .main import *

try:
    ip = get_ipython()
    from .ipython_ext import ShapeMagics
    ip.register_magics(ShapeMagics)
except:
    pass