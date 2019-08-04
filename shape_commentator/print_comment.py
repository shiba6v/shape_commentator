import sys
from .main import _preprocess_in_module_mode, make_comment, SHAPE_COMMENTATOR_ENV

def print_comment_main():
    _preprocess_in_module_mode()
    filename = sys.argv[0]
    env = SHAPE_COMMENTATOR_ENV()
    env.globals = globals()
    env.filename = filename
    print_func = lambda line:sys.stdout.write(line+"\n")
    with open(filename) as f:
        source = f.read()
        make_comment(source, env, print_func)

if __name__ == "__main__":
    print_comment_main()