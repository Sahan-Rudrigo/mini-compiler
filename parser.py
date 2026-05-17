# ============================================================
#  PHASE 2 – SYNTAX ANALYSER
#  Parses the token list and builds an Abstract Syntax Tree (AST).
# ============================================================


class SyntaxAnalyser:
    """
    Recursive-descent parser for the grammar:

        Statement  →  IDENTIFIER ASSIGN Expression
        Expression →  Term   { (PLUS | MINUS) Term   }
        Term       →  Factor { (MULTIPLY | DIVIDE) Factor }
        Factor     →  NUMBER | IDENTIFIER | LPAREN Expression RPAREN
    """

    class SyntaxError(Exception):
        pass

    def __init__(self):
        # _pos tracks where we are in the token list as we parse
        self._tokens  = []
        self._pos     = 0
        self._line_no = 0

    def _current(self):
        # peek at the current token without consuming it
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]
        return None

    def _consume(self, expected_type: str):
        # grab the token we expect — blow up clearly if it's wrong
        token = self._current()
        if token is None:
            raise self.SyntaxError(
                f"[Line {self._line_no}] Syntax Error: "
                f"Expected '{expected_type}' but reached end of line."
            )
        if token[0] != expected_type:
            raise self.SyntaxError(
                f"[Line {self._line_no}] Syntax Error: "
                f"Expected '{expected_type}' but found '{token[1]}'."
            )
        self._pos += 1
        return token

    def parse(self, tokens: list, line_number: int) -> dict:
        # reset state for each new line — parser is reused across lines
        self._tokens  = tokens
        self._pos     = 0
        self._line_no = line_number

        if not tokens:
            raise self.SyntaxError(
                f"[Line {line_number}] Syntax Error: Empty statement."
            )

        ast = self._parse_statement()

        # if there's still something left after a full statement, that's wrong
        if self._current() is not None:
            raise self.SyntaxError(
                f"[Line {self._line_no}] Syntax Error: "
                f"Unexpected token '{self._current()[1]}' after statement."
            )
        return ast

    def _parse_statement(self) -> dict:
        # every valid line looks like:  identifier = expression
        target_token = self._consume('IDENTIFIER')
        self._consume('ASSIGN')
        expr_node = self._parse_expression()
        return {'type': 'assign', 'target': target_token[1], 'value': expr_node}

    def _parse_expression(self) -> dict:
        # handles + and - (lowest precedence)
        node = self._parse_term()
        while self._current() and self._current()[0] in ('PLUS', 'MINUS'):
            op_token = self._current()
            self._pos += 1           # move past the operator
            right = self._parse_term()
            # wrap left and right into a binary operation node
            node  = {'type': 'binop', 'op': op_token[1], 'left': node, 'right': right}
        return node

    def _parse_term(self) -> dict:
        # handles * and / (higher precedence than + and -)
        node = self._parse_factor()
        while self._current() and self._current()[0] in ('MULTIPLY', 'DIVIDE'):
            op_token = self._current()
            self._pos += 1           # move past the operator
            right = self._parse_factor()
            # same structure as expression — just different operators
            node  = {'type': 'binop', 'op': op_token[1], 'left': node, 'right': right}
        return node

    def _parse_factor(self) -> dict:
        # a factor is the smallest unit — a number, a variable, or (expression)
        token = self._current()

        if token is None:
            raise self.SyntaxError(
                f"[Line {self._line_no}] Syntax Error: Unexpected end of expression."
            )
        if token[0] == 'NUMBER':
            self._pos += 1
            return {'type': 'number', 'value': token[1]}
        if token[0] == 'IDENTIFIER':
            self._pos += 1
            return {'type': 'identifier', 'name': token[1]}
        if token[0] == 'LPAREN':
            self._pos += 1
            expr = self._parse_expression()
            self._consume('RPAREN')   # must close what we opened
            return expr

        raise self.SyntaxError(
            f"[Line {self._line_no}] Syntax Error: "
            f"Unexpected token '{token[1]}' in expression."
        )
