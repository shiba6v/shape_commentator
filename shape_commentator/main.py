import ast
import sys
import copy

initialize_code = """
__name__ = "__main__"
def SHAPE_COMMENTATOR_tuple_unpacker(tpl_input):
    class SHAPE_COMMENTATOR_tuple_unpacker_endmark:
        pass
    result = ""
    tpl_stack = [tpl_input]
    while len(tpl_stack) > 0:
        tpl = tpl_stack.pop()
        if type(tpl) == tuple or type(tpl) == list:
            result += "("
            tpl_stack.append(SHAPE_COMMENTATOR_tuple_unpacker_endmark())
            tmp = list(tpl)
            tmp.reverse()
            for t in tmp:
                tpl_stack.append(t)
        elif isinstance(tpl,SHAPE_COMMENTATOR_tuple_unpacker_endmark):
            result += ")"
        elif hasattr(tpl, "shape"):
            result += str(tpl.shape) + ","
        else:
            # change to type(tpl).__name__
            result += str(type(tpl)) + ","
    return result
"""

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

def code_compile(source):
    tree = ast.parse(source)
    ShapeNodeTransformer().visit(tree)
    tree.body = ast.parse(initialize_code).body + tree.body
    code = compile(tree,'<string>','exec')
    return code

def execute(source,globals,locals=None):
    r"""
    >>> SHAPE_COMMENTATOR_RESULT={};execute('import numpy as np\na = np.array([1,2,3,4,5,6])',globals(),locals());SHAPE_COMMENTATOR_RESULT
    {'2': '(6,),'}
    """
    code = code_compile(source)
    exec(code, globals, locals)

# comment in Jupyter Notebook / IPython
def comment(source, globals, locals=None):
    r"""
    >>> In=['import numpy as np\na = np.array([1,2,3,4,5,6])','print("delete_this")'];comment(In[len(In)-2],globals(),locals())
    import numpy as np
    a = np.array([1,2,3,4,5,6])  #_ (6,),
    """
    # delete the cell which runs shape_commentator
    exec("In[len(In)-1] = ''", globals)
    globals['SHAPE_COMMENTATOR_RESULT'] = {}
    try:
        execute(source, globals)
    finally:
        print_func = lambda line:sys.stdout.write(line+"\n")
        write_comment(source, globals['SHAPE_COMMENTATOR_RESULT'], print_func)

# output commented source code as filename.py.commented.py
def write_comment(source, SHAPE_COMMENTATOR_RESULT, output_func):
    r"""
    >>> write_comment('import numpy as np\na = np.array([1,2,3,4,5,6])', {'2': '(6,),'}, lambda line:sys.stdout.write(line+"\n"))
    import numpy as np
    a = np.array([1,2,3,4,5,6])  #_ (6,),
    """
    for idx,line in enumerate(source.split("\n")):
        key = str(idx+1)
        if key in SHAPE_COMMENTATOR_RESULT:
            new_line = line.split("  #_ ")
            output_func(new_line[0]+"  #_ " + SHAPE_COMMENTATOR_RESULT[key])
        else:
            output_func(line)

def main():
    print("=========aaa=========")
    if len(sys.argv) <= 1:
        print("Please set filename")
        print("example:")
        print("    $ python -m shape_commentator filename arg1 arg2")
        exit()
    
    filename = sys.argv[1]
    with open(filename) as f:
        source = f.read()
        for i in range(len(sys.argv)-1):
            sys.argv[i] = sys.argv[i+1]
        del sys.argv[len(sys.argv)-1]
        global SHAPE_COMMENTATOR_RESULT
        SHAPE_COMMENTATOR_RESULT = {}
        try:
            execute(source,globals())
        finally:
            with open(filename+".commented.py", "w") as f_w:
                output_func = lambda x: f_w.write(x + "\n")
                write_comment(source, SHAPE_COMMENTATOR_RESULT, output_func)

if __name__ == '__main__':
    main()