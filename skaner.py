from termcolor import colored

def skaner(tekst):
    global pozycja

    while pozycja < len(tekst) and tekst[pozycja].isspace():
        pozycja += 1

    if pozycja >= len(tekst):
        return 'magenta', 'END_OF_FILE', None

    aktualny_znak = tekst[pozycja]
    start_kolumna = pozycja + 1

    if aktualny_znak.isdigit():
        liczba = ""
        while pozycja < len(tekst) and tekst[pozycja].isdigit():
            liczba += tekst[pozycja]
            pozycja += 1
        return 'blue', 'NUMBER', liczba

    if aktualny_znak.isalpha():
        ident = ""
        while pozycja < len(tekst) and tekst[pozycja].isalnum():
            ident += tekst[pozycja]
            pozycja += 1
        return 'yellow', 'ID', ident

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
        return 'cyan', znaki_pojedyncze[aktualny_znak], aktualny_znak

    pozycja += 1
    return 'red', 'ERROR', f"Nierozpoznany znak '{aktualny_znak}' w kolumnie {start_kolumna}"


wyrazenie = "2+3*(76+8/3) + 3*(9-3)"
pozycja = 0

with open("tekst.txt","r") as plik:
    readFile = plik.readline().strip()

print(f"Analizowany tekst: {readFile}")

while True:
    kolor, kod, wartosc = skaner(readFile)

    if kod == 'END_OF_FILE':
        print(f"{colored("Koniec skanowania :))", kolor)}")
        break
    elif kod == 'ERROR':
        print(f"{colored("BŁĄD SKANERA:\n - ", kolor)} {colored(wartosc, kolor)}")
    else:
        print(f"{colored(kod, kolor):27} | {wartosc}")