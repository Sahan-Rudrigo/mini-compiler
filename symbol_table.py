# ============================================================
#  PHASE 3 – SYMBOL TABLE
#  Keeps track of every declared variable and its value.
# ============================================================


class SymbolTable:
    """Maps variable names to their declaration status and value."""

    def __init__(self):
        self._table = {}   # name → { status, value }

    def declare(self, name: str):
        # don't overwrite if it's already there
        if name not in self._table:
            self._table[name] = {'status': 'declared', 'value': None}

    def set_value(self, name: str, value):
        # only update if the variable exists — silently ignore unknown names
        if name in self._table:
            self._table[name]['value'] = value

    def lookup(self, name: str):
        # returns None if name isn't in the table — callers check for that
        return self._table.get(name, None)

    def is_declared(self, name: str) -> bool:
        # quick check used by IR generator before using a variable
        return name in self._table

    def all_entries(self) -> dict:
        # return a copy so callers can't accidentally mutate the table
        return dict(self._table)
