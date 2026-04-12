def skaner(tekst, poz):
    if poz >= len(tekst):
        return 'END', None, poz

    start_poz = poz
    znak = tekst[poz]

    if znak.isspace():
        bufor = ""
        while poz < len(tekst) and tekst[poz].isspace():
            bufor += tekst[poz]
            poz += 1
        return 'WS', bufor, poz

    if znak == '#':
        bufor = ""
        while poz < len(tekst) and tekst[poz] != '\n':
            bufor += tekst[poz]
            poz += 1
        return 'COMMENT', bufor, poz

    if znak.isdigit():
        bufor = ""
        while poz < len(tekst) and tekst[poz].isdigit():
            bufor += tekst[poz]
            poz += 1
        return 'NUMBER', bufor, poz

    if znak.isalpha():
        bufor = ""
        while poz < len(tekst) and tekst[poz].isalnum():
            bufor += tekst[poz]
            poz += 1
        typ = 'KEYWORD' if bufor in ['if', 'let', 'fun'] else 'ID'
        return typ, bufor, poz

    znaki_pojedyncze = {'+': 'OP', '-': 'OP', '*': 'OP', '/': 'OP', '(': 'DELIM', ')': 'DELIM'}
    if znak in znaki_pojedyncze:
        return znaki_pojedyncze[znak], znak, poz + 1

    return 'ERROR', znak, poz + 1