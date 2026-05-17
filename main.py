# ============================================================
#  Usage of this main.py:
#    python main.py              → uses built-in example
#    python main.py input.txt    → reads from a .txt file
# ============================================================

import sys
from compiler import MiniCompiler


if __name__ == '__main__':

    # If a filename was passed on the command line 
    if len(sys.argv) == 2:
        filepath = sys.argv[1]

        # only .txt files — anything else is probably a mistake
        if not filepath.endswith('.txt'):
            print(f"Error: Expected a .txt file, got '{filepath}'")
            sys.exit(1)

        # read the file
        try:
            with open(filepath, 'r') as f:
                source_code = f.read()
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found.")
            sys.exit(1)
        except IOError as e:
            print(f"Error: Could not read file '{filepath}': {e}")
            sys.exit(1)

        MiniCompiler().compile(source_code, source_label=filepath)

    # No argument → run the built-in assignment example
    elif len(sys.argv) == 1:
        SOURCE = """
a = 5
b = 10
c = a + b * 2
"""
        MiniCompiler().compile(SOURCE, source_label="built-in example")

    # Too many arguments
    else:
        print("Usage:")
        print("  python main.py             # run built-in example")
        print("  python main.py input.txt   # compile a .txt file")
        sys.exit(1)
