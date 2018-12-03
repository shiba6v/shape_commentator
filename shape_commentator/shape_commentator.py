import ast
import sys
import copy

initialize_code = """
SHAPE_COMMENTATOR_RESULT = {}
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

# TODO 一度検査した行は通らないようにしたい
def execute(source,globals={},locals={}):
    tree = ast.parse(source)
    ShapeNodeTransformer().visit(tree)
    tree.body = ast.parse(initialize_code).body + tree.body
    code = compile(tree,'<string>','exec')
    exec(code,globals,locals)

# ソース名.commented.pyにコメント付きソースコードを出力．
def write_comment(source,SHAPE_COMMENTATOR_RESULT,filename="src.py"):
    with open(filename+".commented.py", "w") as f_w:
        for idx,line in enumerate(source.split("\n")):
            key = str(idx+1)
            if key in SHAPE_COMMENTATOR_RESULT:
                new_line = line.split("  #_ ")
                f_w.write(new_line[0]+"  #_ " + SHAPE_COMMENTATOR_RESULT[key] + "\n")
            else:
                f_w.write(line+"\n")

# Jupyter Notebook上で前のセルを簡単にコメントする
def comment(source, globals, locals):
    # commentを呼んだセルに対してcommentを呼ばれると厄介なので消す
    exec("In[len(In)-1] = ' '",globals,locals)
    try:
        execute(source, globals, locals)
    finally:
        for idx,line in enumerate(source.split("\n")):
            key = str(idx+1)
            if key in SHAPE_COMMENTATOR_RESULT:
                new_line = line.split("  #_ ")
                print(new_line[0]+"  #_ " + SHAPE_COMMENTATOR_RESULT[key])
            else:
                print(line)

if __name__ == '__main__':
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
        try:
            execute(source,globals(),locals())
        finally:
            print(SHAPE_COMMENTATOR_RESULT)
            write_comment(source, SHAPE_COMMENTATOR_RESULT, filename)
