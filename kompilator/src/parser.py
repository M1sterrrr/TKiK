from __future__ import annotations

import ply.yacc as yacc

from .lexer import tokens, build_lexer


def _token_column(lexer, tok) -> int | None:
    if tok is None:
        return None
    if lexer is None or not hasattr(lexer, "lexdata"):
        return None
    try:
        last_nl = lexer.lexdata.rfind("\n", 0, tok.lexpos)
        return tok.lexpos - last_nl
    except Exception:
        return None


def _format_source_context(lexer, tok) -> tuple[str | None, str | None]:
    if tok is None or lexer is None or not hasattr(lexer, "lexdata"):
        return None, None
    data = lexer.lexdata
    try:
        line_start = data.rfind("\n", 0, tok.lexpos) + 1
        line_end = data.find("\n", tok.lexpos)
        if line_end == -1:
            line_end = len(data)
        line = data[line_start:line_end].rstrip("\n")
        col = _token_column(lexer, tok)
        if col is None:
            return line, None
        caret = " " * (max(col, 1) - 1) + "^"
        return line, caret
    except Exception:
        return None, None


class Node:
    pass


class Program(Node):
    def __init__(self, name, declarations, body):
        self.name = name
        self.declarations = declarations
        self.body = body


class VarDecl(Node):
    def __init__(self, names, vartype: str):
        self.names = names
        self.vartype = vartype


class Compound(Node):
    def __init__(self, statements):
        self.statements = statements


class Assign(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class If(Node):
    def __init__(self, cond, then_stmt, else_stmt=None):
        self.cond = cond
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt


class While(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body


class For(Node):
    def __init__(self, var_name, start_expr, end_expr, direction, body):
        self.var_name = var_name
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.direction = direction  # "to" | "downto"
        self.body = body


class RepeatUntil(Node):
    def __init__(self, body_statements, cond):
        self.body_statements = body_statements
        self.cond = cond


class BinOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Num(Node):
    def __init__(self, value):
        self.value = value


class Bool(Node):
    def __init__(self, value: bool):
        self.value = value


class Var(Node):
    def __init__(self, name):
        self.name = name


class UnaryOp(Node):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class Writeln(Node):
    def __init__(self, exprs):
        self.exprs = exprs


class Readln(Node):
    def __init__(self, name):
        self.name = name


precedence = (
    # rozwiązuje klasyczne "dangling else"
    ("nonassoc", "IFX"),
    ("nonassoc", "ELSE"),
    ("nonassoc", "LT", "LE", "GT", "GE", "EQ", "NE"),
    ("left", "OR"),
    ("left", "PLUS", "MINUS"),
    ("left", "AND"),
    ("left", "TIMES", "DIVIDE", "IDIV", "MOD"),
    ("right", "NOT"),
    ("right", "UMINUS"),
)


def p_program(p):
    "program : PROGRAM ID SEMI var_section compound DOT"
    p[0] = Program(p[2], p[4], p[5])


def p_var_section_empty(p):
    "var_section :"
    p[0] = []


def p_var_section_some(p):
    "var_section : VAR var_declarations"
    p[0] = p[2]


def p_var_declarations_single(p):
    "var_declarations : var_declaration"
    p[0] = [p[1]]


def p_var_declarations_many(p):
    "var_declarations : var_declarations var_declaration"
    p[0] = p[1] + [p[2]]


def p_var_declaration(p):
    "var_declaration : id_list COLON type_spec SEMI"
    p[0] = VarDecl(p[1], p[3])


def p_type_spec_integer(p):
    "type_spec : INTEGER"
    p[0] = "integer"


def p_type_spec_boolean(p):
    "type_spec : BOOLEAN"
    p[0] = "boolean"


def p_id_list_single(p):
    "id_list : ID"
    p[0] = [p[1]]


def p_id_list_many(p):
    "id_list : id_list COMMA ID"
    p[0] = p[1] + [p[3]]


def p_compound(p):
    """compound : BEGIN END
                | BEGIN stmt_seq END
                | BEGIN stmt_seq SEMI END"""
    if len(p) == 3:
        p[0] = Compound([])
    elif len(p) == 5:
        p[0] = Compound(p[2])
    else:
        p[0] = Compound(p[2])


def p_stmt_seq_single(p):
    "stmt_seq : statement"
    p[0] = [p[1]]


def p_stmt_seq_many(p):
    "stmt_seq : stmt_seq SEMI statement"
    p[0] = p[1] + [p[3]]


def p_statement_simple(p):
    "statement : simple_statement"
    p[0] = p[1]


def p_statement_structured(p):
    "statement : structured_statement"
    p[0] = p[1]


def p_simple_statement_assign(p):
    "simple_statement : ID ASSIGN expr"
    p[0] = Assign(p[1], p[3])


def p_simple_statement_writeln_args(p):
    "simple_statement : WRITELN LPAREN expr_list RPAREN"
    p[0] = Writeln(p[3])


def p_simple_statement_writeln_empty(p):
    "simple_statement : WRITELN LPAREN RPAREN"
    p[0] = Writeln([])


def p_simple_statement_readln(p):
    "simple_statement : READLN LPAREN ID RPAREN"
    p[0] = Readln(p[3])


def p_structured_statement_if(p):
    "structured_statement : IF expr THEN statement %prec IFX"
    p[0] = If(p[2], p[4])


def p_structured_statement_if_else(p):
    "structured_statement : IF expr THEN statement ELSE statement"
    p[0] = If(p[2], p[4], p[6])


def p_structured_statement_while(p):
    "structured_statement : WHILE expr DO statement"
    p[0] = While(p[2], p[4])


def p_structured_statement_for_to(p):
    "structured_statement : FOR ID ASSIGN expr TO expr DO statement"
    p[0] = For(p[2], p[4], p[6], "to", p[8])


def p_structured_statement_for_downto(p):
    "structured_statement : FOR ID ASSIGN expr DOWNTO expr DO statement"
    p[0] = For(p[2], p[4], p[6], "downto", p[8])


def p_structured_statement_repeat_until(p):
    """structured_statement : REPEAT stmt_seq UNTIL expr
                            | REPEAT stmt_seq SEMI UNTIL expr"""
    if len(p) == 5:
        p[0] = RepeatUntil(p[2], p[4])
    else:
        p[0] = RepeatUntil(p[2], p[5])


def p_structured_statement_compound(p):
    "structured_statement : compound"
    p[0] = p[1]


def p_expr_list_single(p):
    "expr_list : expr"
    p[0] = [p[1]]


def p_expr_list_many(p):
    "expr_list : expr_list COMMA expr"
    p[0] = p[1] + [p[3]]


def p_expr_binop(p):
    """expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr IDIV expr
            | expr MOD expr
            | expr AND expr
            | expr OR expr
            | expr LT expr
            | expr LE expr
            | expr GT expr
            | expr GE expr
            | expr EQ expr
            | expr NE expr"""
    p[0] = BinOp(p[2], p[1], p[3])


def p_expr_group(p):
    "expr : LPAREN expr RPAREN"
    p[0] = p[2]


def p_expr_uminus(p):
    "expr : MINUS expr %prec UMINUS"
    p[0] = UnaryOp("-", p[2])


def p_expr_not(p):
    "expr : NOT expr"
    p[0] = UnaryOp("not", p[2])


def p_expr_number(p):
    "expr : NUMBER"
    p[0] = Num(p[1])


def p_expr_true(p):
    "expr : TRUE"
    p[0] = Bool(True)


def p_expr_false(p):
    "expr : FALSE"
    p[0] = Bool(False)


def p_expr_var(p):
    "expr : ID"
    p[0] = Var(p[1])


def p_error(p):
    if p:
        lexer = getattr(p, "lexer", None)
        col = _token_column(lexer, p)
        where = f"line {p.lineno}" + (f", col {col}" if col is not None else "")
        token_desc = f"{p.type}({p.value!r})"

        prev = getattr(lexer, "last_token", None) if lexer is not None else None
        prev_desc = None
        if prev is not None:
            prev_col = _token_column(lexer, prev)
            prev_where = f"line {prev.lineno}" + (f", col {prev_col}" if prev_col is not None else "")
            prev_desc = f"last token: {prev.type}({prev.value!r}) at {prev_where}"

        line, caret = _format_source_context(lexer, p)
        parts = [f"Syntax error at {token_desc} ({where})."]
        if prev_desc:
            parts.append(prev_desc)
        if line:
            parts.append(line)
        if caret:
            parts.append(caret)
        raise SyntaxError("\n".join(parts))

    raise SyntaxError("Syntax error at EOF (unexpected end of input; missing 'end' or '.'?)")


def build_parser():
    lexer = build_lexer()
    lexer.last_token = None
    _orig_token = lexer.token

    def _token_wrapper():
        tok = _orig_token()
        if tok is not None:
            lexer.last_token = tok
        return tok

    lexer.token = _token_wrapper
    return yacc.yacc(start="program"), lexer

