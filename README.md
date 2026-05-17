1. Project Overview
--------------------
This is a mini compiler that reads simple arithmetic assignment
statements, performs lexical and syntax analysis, manages a
symbol table, and generates intermediate three-address code.

Example input:
    a = 5
    b = 10
    c = a + b * 2

Example output:
    Symbol Table:
      a : declared
      b : declared
      c : declared

    Intermediate Code:
      a = 5
      b = 10
      t1 = b * 2
      t2 = a + t1
      c = t2


2. Compiler Pipeline
---------------------
    Source Code
        |
        v
    Phase 1 – Lexical Analyser    (lexer.py)
        |
        v
    Phase 2 – Syntax Analyser     (parser.py)
        |
        v
    Phase 3 – Symbol Table        (symbol_table.py)
        |
        v
    Phase 4 – IR Code Generator   (ir_generator.py)


3. Files Included
------------------

    main.py           Entry point. Run this file to start the compiler.
    compiler.py       Compiler driver. Connects all four phases.
    lexer.py          Phase 1 – Lexical Analyser.
    parser.py         Phase 2 – Syntax Analyser.
    symbol_table.py   Phase 3 – Symbol Table.
    ir_generator.py   Phase 4 – Intermediate Code Generator.
    input.txt         Sample input file with arithmetic statements.
    README.txt        This file.
    output_screenshot.png   Screenshot of the program output.


4. How to Run the Program
--------------------------
All files must be in the same folder before running.

Method 1: Run the built-in example
    Open terminal or command prompt in the project folder and run:

        python main.py

Method 2: Run using input.txt
    Place input.txt in the same folder and run:

        python main.py input.txt


5. Sample input.txt
--------------------
    a = 5
    b = 10
    c = a + b * 2


6. Requirements
----------------
    Python 3.6 or higher
    No external libraries required (uses only built-in re and sys)
