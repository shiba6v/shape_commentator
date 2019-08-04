import ast
import sys
import copy
import os

initialize_code = """
__name__ = "__main__"
__package__ = None
if "{0.filename}" == "":
    if "__file__" in globals():
        del __file__
else:
    __file__ = "{0.filename}"

def SHAPE_COMMENTATOR_tuple_unpacker(tpl_input):
    class SHAPE_COMMENTATOR_TUPLE_UNPACKER_ENDMARK_TUPLE:
        pass
    class SHAPE_COMMENTATOR_TUPLE_UNPACKER_ENDMARK_LIST:
        pass
    result = ""
    length_remaining = 10
    too_long = False
    too_long_dot_yet = False
    tpl_stack = [tpl_input]
    while len(tpl_stack) > 0:
        tpl = tpl_stack.pop()
        if isinstance(tpl,SHAPE_COMMENTATOR_TUPLE_UNPACKER_ENDMARK_TUPLE):
            result += "),"
        elif isinstance(tpl,SHAPE_COMMENTATOR_TUPLE_UNPACKER_ENDMARK_LIST):
            result += "],"
        elif too_long:
            if too_long_dot_yet:
                result += " ... "
                too_long_dot_yet = False
            continue
        elif type(tpl) == tuple or type(tpl) == list:
            if type(tpl) == tuple:
                result += "("
                tpl_stack.append(SHAPE_COMMENTATOR_TUPLE_UNPACKER_ENDMARK_TUPLE())
            elif type(tpl) == list:
                result += "["
                tpl_stack.append(SHAPE_COMMENTATOR_TUPLE_UNPACKER_ENDMARK_LIST())
            tmp = list(tpl)
            tmp.reverse()
            for t in tmp:
                tpl_stack.append(t)
        elif hasattr(tpl, "shape"):
            result += str(tpl.shape) + ","
        else:
            result += type(tpl).__name__ + ","
        length_remaining -= 1
        if not too_long and length_remaining <= 0:
            too_long = True
            too_long_dot_yet = True
    result = result[:-1]
    return result
"""

class SHAPE_COMMENTATOR_ENV():
    def __init__(self):
        self.globals = {}
        self.filename = ""

class ShapeNodeTransformer(ast.NodeTransformer):
    def subsciript_dict(self, lineno, col_offset, s):
        return ast.Subscript(
            lineno=lineno,
            col_offset=col_offset,
            value=ast.Name(
                lineno=lineno,
                col_offset=col_offset,
                id='SHAPE_COMMENTATOR_RESULT',
                ctx=ast.Load()),
            slice=ast.Index(
                    value=ast.Str(
                    lineno=lineno,
                    col_offset=col_offset+25,
                    s=s)
                ),
            ctx=ast.Store()
         )
    def name_store_tmp(self, lineno, col_offset):
        return [ast.Name(
                lineno=lineno,
                col_offset=col_offset,
                id='SHAPE_COMMENTATOR_TMP',
                ctx=ast.Store()
            )]
    def name_load_tmp(self, lineno, col_offset):
        return ast.Name(
                lineno=lineno,
                col_offset=col_offset,
                id='SHAPE_COMMENTATOR_TMP',
                ctx=ast.Load()
            )
    def call_tuple_unpacker(self, lineno, col_offset):
        return ast.Call(
            lineno=lineno,
            col_offset=col_offset,
            func=ast.Name(
                lineno=lineno,
                col_offset=col_offset,
                id='SHAPE_COMMENTATOR_tuple_unpacker',
                ctx=ast.Load()
            ),
            args=[ast.Name(
                lineno=lineno,
                col_offset=col_offset,
                id='SHAPE_COMMENTATOR_TMP',
                ctx=ast.Load()
            )],
            keywords=[]
        )
    def visit_Assign(self, node_orig):
        node_store_tmp = ast.Assign(
            lineno=node_orig.lineno,
            col_offset=node_orig.col_offset,
            value = copy.deepcopy(node_orig.value)
        )
        node_store_tmp.targets = self.name_store_tmp(node_orig.lineno, node_orig.col_offset)
        node_orig.value = self.name_load_tmp(node_orig.lineno, node_orig.col_offset)
        node_record = ast.Assign(
            lineno=node_orig.lineno,
            col_offset=node_orig.col_offset
        )
        node_record.targets = [self.subsciript_dict(node_orig.lineno, node_orig.col_offset, str(node_orig.lineno))]
        node_record.value = self.call_tuple_unpacker(node_orig.lineno, node_orig.col_offset, )
        return [node_store_tmp,node_orig,node_record]

def _code_compile(source, env):
    tree = ast.parse(source)
    ShapeNodeTransformer().visit(tree)
    initializer = initialize_code.format(env)
    tree.body = ast.parse(initializer).body + tree.body
    code = compile(tree,'<string>','exec')
    return code

def _execute(source, env):
    r"""
    >>> SHAPE_COMMENTATOR_RESULT={};env=SHAPE_COMMENTATOR_ENV();env.globals=globals();_execute('import numpy as np\na = np.array([1,2,3,4,5,6])',env);SHAPE_COMMENTATOR_RESULT
    {'2': '(6,)'}
    """
    code = _code_compile(source, env)
    exec(code, env.globals)

# clear comment in Jupyter Notebook / IPython
def clear_comment(source, output_func):
    r"""
    >>> clear_comment('import numpy as np\na = np.array([1,2,3,4,5,6])  #_ (6,)', lambda line:sys.stdout.write(line+"\n"))
    import numpy as np
    a = np.array([1,2,3,4,5,6])
    """
    for idx,line in enumerate(source.split("\n")):
        new_line = line.split("  #_ ")
        output_func(new_line[0])

# output commented source code as filename.py.commented.py
def _write_comment(source, SHAPE_COMMENTATOR_RESULT, output_func):
    r"""
    >>> _write_comment('import numpy as np\na = np.array([1,2,3,4,5,6])', {'2': '(6,)'}, lambda line:sys.stdout.write(line+"\n"))
    import numpy as np
    a = np.array([1,2,3,4,5,6])  #_ (6,)
    """
    for idx,line in enumerate(source.split("\n")):
        key = str(idx+1)
        if key in SHAPE_COMMENTATOR_RESULT:
            new_line = line.split("  #_ ")
            output_func(new_line[0]+"  #_ " + SHAPE_COMMENTATOR_RESULT[key])
        else:
            output_func(line)

# move arguments to fill filename position
def _preprocess_in_module_mode():
    r"""
    >>> import sys;sys.argv=["0","1","2"];_preprocess_in_module_mode();print(sys.argv)
    ['1', '2']
    """
    if len(sys.argv) <= 1:
        print("Please set filename")
        print("example:")
        print("    $ python -m shape_commentator filename arg1 arg2")
        exit()
    for i in range(len(sys.argv)-1):
        sys.argv[i] = sys.argv[i+1]
    del sys.argv[len(sys.argv)-1]

def make_comment(source, env, output_func):
    env.globals['SHAPE_COMMENTATOR_RESULT'] = {}
    try:
        _execute(source,env)
    finally:
        _write_comment(source, env.globals['SHAPE_COMMENTATOR_RESULT'], output_func)

# def make_comment(source, env, output_func):
#     env.globals['SHAPE_COMMENTATOR_RESULT'] = {}
#     _execute(source,env)
#     _write_comment(source, env.globals['SHAPE_COMMENTATOR_RESULT'], output_func)

# comment in Jupyter Notebook / IPython
def comment(source, globals, locals=None):
    r"""
    >>> In=['import numpy as np\na = np.array([1,2,3,4,5,6])','print("delete_this")'];comment(In[len(In)-2],globals(),locals())
    import numpy as np
    a = np.array([1,2,3,4,5,6])  #_ (6,)
    """
    # delete the cell which runs shape_commentator
    exec("In[len(In)-1] = ''", globals)
    env = SHAPE_COMMENTATOR_ENV()
    env.globals = globals
    print_func = lambda line:sys.stdout.write(line+"\n")
    make_comment(source, env, print_func)

# clear comment in Jupyter Notebook / IPython
def clear(source):
    r"""
    >>> In=['import numpy as np\na = np.array([1,2,3,4,5,6])  #_ (6,)',''];clear(In[len(In)-2])
    import numpy as np
    a = np.array([1,2,3,4,5,6])
    """
    print_func = lambda line:sys.stdout.write(line+"\n")
    clear_comment(source, print_func)

def main():
    _preprocess_in_module_mode()
    filename = sys.argv[0]
    with open(filename+".commented.py", "w") as f_w:
        output_func = lambda x: f_w.write(x + "\n")
        with open(filename) as f:
            source = f.read()
            env = SHAPE_COMMENTATOR_ENV()
            env.globals = globals()
            env.filename = filename
            make_comment(source, env, output_func)
