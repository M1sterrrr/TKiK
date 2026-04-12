def skaner(tekst):
    global pozycja

    while pozycja < len(tekst) and tekst[pozycja].isspace():
        pozycja += 1

    if pozycja >= len(tekst):
        return 'END_OF_FILE', None

    aktualny_znak = tekst[pozycja]
    start_kolumna = pozycja + 1

    if aktualny_znak.isdigit():
        liczba = ""
        while pozycja < len(tekst) and tekst[pozycja].isdigit():
            liczba += tekst[pozycja]
            pozycja += 1
        return 'NUMBER', liczba

    if aktualny_znak.isalpha():
        ident = ""
        while pozycja < len(tekst) and tekst[pozycja].isalnum():
            ident += tekst[pozycja]
            pozycja += 1
        return 'ID', ident

    znaki_pojedyncze = {
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'MULTIPLICATION',
        '/': 'DIVISION',
        '(': 'LEFT_PARENTHESIS',
        ')': 'RIGHT_PARENTHESIS',
    }

    if aktualny_znak in znaki_pojedyncze:
        pozycja += 1
        return znaki_pojedyncze[aktualny_znak], aktualny_znak

    pozycja += 1
    return 'ERROR', f"Nierozpoznany znak '{aktualny_znak}' w kolumnie {start_kolumna}"


wyrazenie = "2+3*(76+8/3) + 3*(9-3)"
pozycja = 0

print(f"Analizowany tekst: {wyrazenie}")

while True:
    kod, wartosc = skaner(wyrazenie)

    if kod == 'END_OF_FILE':
        print(f"Koniec skanowania :))")
        break
    elif kod == 'ERROR':
        print(f"BŁĄD SKANERA:\n - {wartosc}")
    else:
        print(f"{kod:20} | {wartosc}")