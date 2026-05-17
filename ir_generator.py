# ============================================================
#  PHASE 4 – INTERMEDIATE CODE GENERATOR
#  Walks the AST and produces Three-Address Code (TAC).
#
#  TAC format:
#    t1 = b * 2
#    t2 = a + t1
#    c  = t2
# ============================================================

from symbol_table import SymbolTable


class IRCodeGenerator:
    """
    Walks the AST and emits Three-Address Code (TAC).
    Creates a new temporary (t1, t2, …) for each sub-expression.
    """

    def __init__(self, symbol_table: SymbolTable):
        # share the same symbol table built during earlier phases
        self._symbol_table = symbol_table
        self._temp_count   = 0    # increments with every new temporary variable
        self._instructions = []   # final TAC output accumulates here

    def generate(self, ast: dict) -> list:
        # snapshot length before so we can return only the new instructions added
        before = len(self._instructions)
        self._emit_statement(ast)
        return self._instructions[before:]

    def all_instructions(self) -> list:
        # called at the end to print the full TAC output
        return list(self._instructions)

    def _new_temp(self) -> str:
        # t1, t2, t3 ... each sub-expression gets its own slot
        self._temp_count += 1
        return f't{self._temp_count}'

    def _emit(self, instruction: str):
        # just appends one TAC line — keeps the rest of the code cleaner
        self._instructions.append(instruction)

    def _emit_statement(self, node: dict):
        target = node['target']
        result = self._emit_expression(node['value'])

        # declare only after expression succeeds — failed lines won't pollute the table
        self._symbol_table.declare(target)

        self._emit(f'{target} = {result}')
        self._symbol_table.set_value(target, result)

    def _emit_expression(self, node: dict) -> str:
        ntype = node['type']

        if ntype == 'number':
            return str(node['value'])

        if ntype == 'identifier':
            name = node['name']
            # catch usage of variables that were never assigned
            if not self._symbol_table.is_declared(name):
                raise NameError(
                    f"IR Generation Error: "
                    f"Variable '{name}' used before declaration."
                )
            return name

        if ntype == 'binop':
            left_result  = self._emit_expression(node['left'])
            right_result = self._emit_expression(node['right'])

            # if both sides are plain numbers, just compute it now (constant folding)
            try:
                left_val  = float(left_result)
                right_val = float(right_result)
                folded    = eval(f'{left_val} {node["op"]} {right_val}')
                folded_str = (
                    str(int(folded))
                    if float(folded).is_integer()
                    else str(folded)
                )
                return folded_str
            except (ValueError, ZeroDivisionError):
                pass   # at least one side is a variable, so we need a temp

            temp = self._new_temp()
            self._emit(f'{temp} = {left_result} {node["op"]} {right_result}')
            return temp

        raise ValueError(f"Unknown AST node type: '{ntype}'")
