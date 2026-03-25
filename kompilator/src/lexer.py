import ply.lex as lex


reserved = {
    "program": "PROGRAM",
    "var": "VAR",
    "integer": "INTEGER",
    "boolean": "BOOLEAN",
    "begin": "BEGIN",
    "end": "END",
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "while": "WHILE",
    "do": "DO",
    "for": "FOR",
    "to": "TO",
    "downto": "DOWNTO",
    "repeat": "REPEAT",
    "until": "UNTIL",
    "div": "IDIV",
    "mod": "MOD",
    "and": "AND",
    "or": "OR",
    "not": "NOT",
    "true": "TRUE",
    "false": "FALSE",
    "writeln": "WRITELN",
    "readln": "READLN",
}

tokens = [
    "ID",
    "NUMBER",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "ASSIGN",
    "SEMI",
    "COLON",
    "COMMA",
    "LPAREN",
    "RPAREN",
    "LT",
    "LE",
    "GT",
    "GE",
    "EQ",
    "NE",
    "DOT",
] + list(reserved.values())

t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_ASSIGN = r":="
t_SEMI = r";"
t_COLON = r":"
t_COMMA = r","
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LT = r"<"
t_LE = r"<="
t_GT = r">"
t_GE = r">="
t_EQ = r"="
t_NE = r"<>"
t_DOT = r"\."

t_ignore = " \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_COMMENT(t):
    r"\{[^}]*\}"
    pass


def t_ID(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    t.type = reserved.get(t.value.lower(), "ID")
    return t


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_error(t):
    raise SyntaxError(f"Illegal character {t.value[0]!r} at line {t.lexer.lineno}")


def build_lexer():
    return lex.lex()

