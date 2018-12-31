import sys
from .main import preprocess_in_module_mode, execute, write_comment

def print_comment_main():
    preprocess_in_module_mode()
    filename = sys.argv[0]
    global SHAPE_COMMENTATOR_RESULT
    SHAPE_COMMENTATOR_RESULT = {}
    with open(filename) as f:
        source = f.read()
        try:
            execute(source,globals())
        finally:
            print_func = lambda line:sys.stdout.write(line+"\n")
            write_comment(source, SHAPE_COMMENTATOR_RESULT, print_func)

if __name__ == "__main__":
    print_comment_main()