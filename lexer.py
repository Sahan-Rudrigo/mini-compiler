# ============================================================
#
#  PHASE 1 – LEXICAL ANALYSER
#  Breaks source code lines into a list of tokens.
# ============================================================

import re

# ─────────────────────────────────────────────────────────────
# TOKEN DEFINITIONS
# ─────────────────────────────────────────────────────────────
# Each token is a (TYPE, VALUE) pair.
# Order matters: longer / more specific patterns must come first.

TOKEN_SPEC = [
    ('NUMBER',     r'\d+(\.\d+)?'),   # integer or float literal
    ('IDENTIFIER', r'[A-Za-z_]\w*'),  # variable name
    ('ASSIGN',     r'='),             # assignment operator  =
    ('PLUS',       r'\+'),            # addition             +
    ('MINUS',      r'-'),             # subtraction          -
    ('MULTIPLY',   r'\*'),            # multiplication       *
    ('DIVIDE',     r'/'),             # division             /
    ('LPAREN',     r'\('),            # left parenthesis     (
    ('RPAREN',     r'\)'),            # right parenthesis    )
    ('SKIP',       r'[ \t]+'),        # whitespace (ignored)
    ('MISMATCH',   r'.'),             # any unexpected char
]

# one big regex built from all the patterns above — faster than checking one by one
MASTER_PATTERN = re.compile(
    '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)
)


class LexicalAnalyser:
    """
    Scans a single source line and converts it into a flat list
    of tokens, filtering out whitespace.

    Raises a LexicalError when an unknown character is found.
    """

    class LexicalError(Exception):
        pass

    def tokenise(self, line: str, line_number: int) -> list:
        # scan one line and return a list of (type, value) token pairs
        tokens = []

        for match in MASTER_PATTERN.finditer(line):
            token_type  = match.lastgroup
            token_value = match.group()

            if token_type == 'SKIP':
                continue                      # spaces don't mean anything here
            elif token_type == 'MISMATCH':
                raise self.LexicalError(
                    f"[Line {line_number}] Lexical Error: "
                    f"Unexpected character '{token_value}'"
                )
            elif token_type == 'NUMBER':
                # store 5.0 as 5, keep 3.14 as 3.14
                token_value = (
                    int(float(token_value))
                    if float(token_value).is_integer()
                    else float(token_value)
                )
            tokens.append((token_type, token_value))

        return tokens
