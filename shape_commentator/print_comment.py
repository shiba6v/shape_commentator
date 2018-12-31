import sys
from .main import _preprocess_in_module_mode, _execute, _write_comment

def print_comment_main():
    _preprocess_in_module_mode()
    filename = sys.argv[0]
    global SHAPE_COMMENTATOR_RESULT
    SHAPE_COMMENTATOR_RESULT = {}
    with open(filename) as f:
        source = f.read()
        try:
            _execute(source,globals())
        finally:
            print_func = lambda line:sys.stdout.write(line+"\n")
            _write_comment(source, SHAPE_COMMENTATOR_RESULT, print_func)

if __name__ == "__main__":
    print_comment_main()