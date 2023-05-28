from IPython.core import page
from IPython.core.magic import Magics, magics_class, cell_magic
from .main import make_comment, clear_comment, SHAPE_COMMENTATOR_ENV
import sys

def find_frame():
    for i in range(20):
        f = sys._getframe(i)
        if "In" in f.f_globals:
            return f

@magics_class
class ShapeMagics(Magics):
    @cell_magic
    def shape(self, parameter_s='', cell=None):
        opts,argsl = self.parse_options(parameter_s,"d",mode="string")
        if "d" in opts:
            # erase
            output = []
            output_func = lambda x: output.append(x)
            clear_comment(cell, output_func)
            output = "\n".join(output)
            page.page(output)
        else:
            # comment
            output = []
            output_func = lambda x: output.append(x)
            env = SHAPE_COMMENTATOR_ENV()
            env.globals = find_frame().f_globals
            try:
                make_comment(cell, env, output_func)
            finally:
                output = "\n".join(output)
                page.page(output)
