def skaner(tekst):
    global pozycja

    while pozycja < len(tekst) and tekst[pozycja] == " ":
        pozycja += 1

    if pozycja >= len(tekst):
        return 'EOF', None

    aktualny_znak = tekst[pozycja]

    if '9' >= aktualny_znak >= '0':
        return 'NUMBER', aktualny_znak

    if 'z' >= aktualny_znak >= 'a' or 'Z' >= aktualny_znak >= 'A':
        return 'ID', aktualny_znak

    znaki_pojedyncze = {
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'MUL',
        '/': 'DIV',
        '(': 'LEFTPAREN',
        ')': 'RIGHTPAREN'
    }

    if aktualny_znak in znaki_pojedyncze:
        return znaki_pojedyncze[aktualny_znak], aktualny_znak

    return 'ERROR', f"Nierozpoznany znak '{aktualny_znak}' w kolumnie {pozycja + 1}"


wyrazenie = "2+3*(76+8/3) + 3*(9-3)"
pozycja = 0

print(f"Analizowany tekst: {wyrazenie}")

while True:
    kod, wartosc = skaner(wyrazenie)
    pozycja += 1

    if kod == 'EOF':
        print(f"Koniec skanowania :))")
        break
    elif kod == 'ERROR':
        print(f"BŁĄD SKANERA:\n - {wartosc}")
    else:
        print(f"{kod:11} | {wartosc}")