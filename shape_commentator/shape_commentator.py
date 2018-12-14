import ast
import sys
import copy

initialize_code = """
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
        elif type(tpl) == SHAPE_COMMENTATOR_tuple_unpacker_endmark:
            result += ")"
        elif hasattr(tpl, "shape"):
            result += str(tpl.shape) + ","
        else:
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
    r"""
    >>> SHAPE_COMMENTATOR_RESULT={};code_compile('import numpy as np\na = np.array([1,2,3,4,5,6])').co_code
    b'd\x00d\x01\x84\x00Z\x00d\x02d\x03l\x01Z\x02e\x02j\x03d\x04d\x05d\x06d\x07d\x08d\tg\x06\x83\x01Z\x04e\x04Z\x05e\x00e\x04\x83\x01e\x06d\n<\x00d\x03S\x00'
    """
    tree = ast.parse(source)
    ShapeNodeTransformer().visit(tree)
    tree.body = ast.parse(initialize_code).body + tree.body
    code = compile(tree,'<string>','exec')
    return code

# TODO 一度検査した行は通らないようにしたい
def execute(source,globals,locals=None):
    r"""
    >>> SHAPE_COMMENTATOR_RESULT={};execute('import numpy as np\na = np.array([1,2,3,4,5,6])',globals(),locals());SHAPE_COMMENTATOR_RESULT
    {'2': '(6,),'}
    """
    code = code_compile(source)
    exec(code, globals, locals)

# Jupyter Notebook上で前のセルを簡単にコメントする
def comment(source, globals, locals=None):
    r"""
    >>> In=['import numpy as np\na = np.array([1,2,3,4,5,6])','print("delete_this")'];comment(In[len(In)-2],globals(),locals())
    import numpy as np
    a = np.array([1,2,3,4,5,6])  #_ (6,),
    """
    # commentを呼んだセルに対してcommentを呼ばれると厄介なので消す
    exec("In[len(In)-1] = ''", globals)
    # globalsを乗っ取っているので，このライブラリ内で宣言された変数は引き継がれない．
    globals['SHAPE_COMMENTATOR_RESULT'] = {}
    try:
        execute(source, globals)
    finally:
        write_comment(source, globals['SHAPE_COMMENTATOR_RESULT'], print)

# ソース名.commented.pyにコメント付きソースコードを出力．
def write_comment(source, SHAPE_COMMENTATOR_RESULT, output_func):
    r"""
    >>> write_comment('import numpy as np\na = np.array([1,2,3,4,5,6])', {'2': '(6,),'}, print)
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
    if len(sys.argv) <= 1:
        print("Please set filename")
        print("example:")
        print("    $ python shape_commentator.py filename")
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