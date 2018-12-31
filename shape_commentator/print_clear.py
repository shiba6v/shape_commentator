import sys
from .main import preprocess_in_module_mode, clear

def print_clear_main():
    preprocess_in_module_mode()
    filename = sys.argv[0]
    with open(filename) as f:
        source = f.read()
        print_func = lambda line:sys.stdout.write(line+"\n")
        clear(source)

if __name__ == "__main__":
    print_clear_main()