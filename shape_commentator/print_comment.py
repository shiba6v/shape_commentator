import sys
from .main import _preprocess_in_module_mode, _make_comment

def print_comment_main():
    _preprocess_in_module_mode()
    filename = sys.argv[0]
    print_func = lambda line:sys.stdout.write(line+"\n")
    with open(filename) as f:
        source = f.read()
        _make_comment(source, globals(), print_func)

if __name__ == "__main__":
    print_comment_main()