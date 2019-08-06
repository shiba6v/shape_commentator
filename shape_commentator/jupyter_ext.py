from IPython.core.magic import register_cell_magic
from .main import make_comment, clear_comment, SHAPE_COMMENTATOR_ENV
from IPython.display import Javascript, display
import json

ENV_GLOBALS = None

class SHAPE_COMMENTATOR_ENV():
    def __init__(self):
        self.globals = {}
        self.filename = ""

@register_cell_magic
def shape_comment(line, cell):
    output = []
    output_func = lambda x: output.append(x)
    env = SHAPE_COMMENTATOR_ENV()
    env.globals = ENV_GLOBALS if ENV_GLOBALS is not None else globals()
    try:
        make_comment(cell, env, output_func)
    finally:
        output = "\n".join(output)
        return output

@register_cell_magic
def shape_erase(line, cell):
    output = []
    output_func = lambda x: output.append(x)
    clear_comment(cell, output_func)
    output = "\n".join(output)
    return output
