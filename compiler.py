

from lexer        import LexicalAnalyser
from parser       import SyntaxAnalyser
from symbol_table import SymbolTable
from ir_generator import IRCodeGenerator


class MiniCompiler:
    """Orchestrates all four phases for a multi-line source program."""

    DIVIDER = '─' * 55

    def __init__(self):
        # each phase gets its own object — they talk through the shared symbol table
        self._lexer    = LexicalAnalyser()
        self._parser   = SyntaxAnalyser()
        self._symtable = SymbolTable()
        self._ir_gen   = IRCodeGenerator(self._symtable)
        self._errors   = []   # all errors across all lines go here

    def compile(self, source_code: str, source_label: str = ""):
        # print the header first so output is readable even if errors happen
        print(self.DIVIDER)
        print("  CO4205 Mini Compiler  –  Assignment 1")
        if source_label:
            print(f"  Source : {source_label}")
        print(self.DIVIDER)

        lines = source_code.strip().splitlines()

        for line_no, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()
            if not line or line.startswith('#'):
                continue   # skip blank lines and comments

            try:
                tokens = self._lexer.tokenise(line, line_no)   # phase 1
                ast    = self._parser.parse(tokens, line_no)    # phase 2
                self._ir_gen.generate(ast)                      # phase 3 + 4

            except (
                LexicalAnalyser.LexicalError,
                SyntaxAnalyser.SyntaxError,
                NameError,
            ) as err:
                # collect errors and keep going — don't stop at first failure
                self._errors.append(str(err))

        self._print_symbol_table()
        self._print_ir_code()
        self._print_errors()

        print(self.DIVIDER)
        status = "FAILED" if self._errors else "SUCCESS"
        print(f"  Compilation {status}")
        print(self.DIVIDER)

    def _print_symbol_table(self):
        # shows every variable that was successfully declared
        print("\nSymbol Table:")
        entries = self._symtable.all_entries()
        if entries:
            for name, info in entries.items():
                print(f"  {name} : {info['status']}")
        else:
            print("  (empty)")

    def _print_ir_code(self):
        # prints the three-address code lines in the order they were generated
        print("\nIntermediate Code:")
        instructions = self._ir_gen.all_instructions()
        if instructions:
            for instr in instructions:
                print(f"  {instr}")
        else:
            print("  (no instructions generated)")

    def _print_errors(self):
        # only prints the errors section if something actually went wrong
        if self._errors:
            print("\nErrors:")
            for err in self._errors:
                print(f"  {err}")
