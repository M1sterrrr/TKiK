# Syntax Highlighter

Prosty skaner konwertujący kod źródłowy na format HTML. Narzędzie koloruje składnię, zachowując przy tym identyczny układ tekstu (spacje, tabulacje, nowe linie).

## Specyfikacja Tokenów  ✏️
Program rozpoznaje i koloruje następujące elementy języka:

| Typ Tokena | Opis | Przykład | Kolor |
| :--- | :--- | :--- | :--- |
| **KEYWORD** | Słowa kluczowe | `let`, `if`, `fun` | Różowy |
| **ID** | Identyfikatory | `zmienna`, `x` | Błękit |
| **NUMBER** | Liczby (INT/FLOAT) | `42`, `3.14` | Żółty |
| **OP** | Operatory | `+`, `-`, `*`, `/` | Zielony |
| **COMMENT** | Komentarze | `# to jest komentarz` | Pomarańczowy |
| **WS** | Białe znaki | spacja, `\n`, `\t` | (brak) |
| **ERROR** | Znaki nierozpoznane | `$`, `@`, `^` | Czerwone tło |

## Logika Skanera 🧠
Skaner został zaimplementowany jako **automat skończony** (DFA):
- **Grupowanie znaków:** Łączy sąsiadujące cyfry w jedną liczbę oraz litery w identyfikatory.
- **Zachowanie struktury:** Każdy biały znak jest traktowany jako token `WS`, co pozwala na odtworzenie układu pliku wejściowego w przeglądarce.

## Instrukcja obsługi 📝
Program uruchamia się z poziomu terminala, podając plik źródłowy oraz nazwę pliku wynikowego:

```bash
python koloruj.py kod.txt wynik.html
```

## Zawartość projektu
- `skaner.py` – logika analizy leksykalnej.
- `koloruj.py` – generator HTML i obsługa plików wejścia/wyjścia.
- `test.txt` – przykładowy plik do przetestowania skanera.