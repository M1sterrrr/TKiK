import sys
from skaner import skaner

def koloruj_skladnie(wejscie_sciezka, wyjscie_sciezka):
    with open(wejscie_sciezka, 'r') as f:
        tekst = f.read()

    kolory = {
        'NUMBER': '#f1fa8c',
        'ID': '#8be9fd',
        'KEYWORD': '#ff79c6',
        'OP': '#50fa7b',
        'COMMENT': "#ef9a45",
        'ERROR': 'white; background-color: #ff5555; font-weight: bold;'
    }

    wynik_html = ""
    aktualna_poz = 0

    while aktualna_poz < len(tekst):
        kod, wartosc, aktualna_poz = skaner(tekst, aktualna_poz)
        
        safe_val = wartosc.replace('<', '&lt;').replace('>', '&gt;')

        if kod in kolory:
            wynik_html += f'<span style="color: {kolory[kod]}">{safe_val}</span>'
        else:
            wynik_html += safe_val

    
    szablon = f"<html><body style='background:#282c34; color:#abb2bf; font-family:monospace;'><pre>{wynik_html}</pre></body></html>"
    
    with open(wyjscie_sciezka, 'w') as f:
        f.write(szablon)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        koloruj_skladnie(sys.argv[1], sys.argv[2])
    else:
        koloruj_skladnie('test.txt', 'wynik.html')#brak pliku = uruchomienie testu