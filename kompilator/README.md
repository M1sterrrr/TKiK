## Kompilator Pascal → C

Edukacyjny kompilator tłumaczący **podzbiór Pascala** do **języka C**.
Projekt służy jako demonstracja: `lexer → parser → AST → codegen → C → gcc`.

### Co robi projekt

- **Wejście**: plik `.pas` w obsługiwanym podzbiorze Pascala
- **Wyjście**: plik `.c` z równoważnym programem w C (prosty, czytelny kod)
- **Uruchomienie**: wygenerowany kod C można skompilować `gcc` i uruchomić

### Obsługiwany podzbiór Pascala

#### Program i bloki

- **program główny**: `program Nazwa; ... begin ... end.`
- **sekcja zmiennych**: `var ...;`
- **bloki złożone**: `begin ... end` (również pusty `begin end`)

#### Typy i deklaracje

- **`integer`**
- **`boolean`** + literały `true` / `false`

#### Instrukcje

- **przypisanie**: `x := expr`
- **warunek**: `if expr then stmt else stmt`
- **pętle**:
  - `while expr do stmt`
  - `for i := a to b do stmt`
  - `for i := a downto b do stmt`
  - `repeat ... until expr`
- **I/O**:
  - `readln(x)` (dla `integer`)
  - `writeln(a, b, ...)` (drukuje wartości jako liczby + spacje + `\n`)

#### Wyrażenia (expr)

- **liczby**, **zmienne**, **nawiasy**
- arytmetyka: `+ - * / div mod` (gdzie `div` to dzielenie całkowite)
- porównania: `< <= > >= = <>`
- logika: `not`, `and`, `or`

### Przykład (test)

W repo jest plik `test.pas`, który stara się użyć możliwie dużo wspieranej składni.

### Uruchamianie

#### Będąc w katalogu `kompilator/`

```bash
python3 main.py test.pas test.c
gcc test.c -o test
./test
```

#### Będąc w root repo (`TKiK/`)

```bash
python3 kompilator/main.py kompilator/test.pas kompilator/test.c
gcc kompilator/test.c -o kompilator/test
./kompilator/test
```

### Ograniczenia / uwagi

- To jest **projekt edukacyjny**, nie pełny Pascal.
- `readln` jest aktualnie tylko dla `integer`.
- `writeln` drukuje wartości jako liczby (`%d`) — bool też będzie wypisany jako `0/1` (zgodnie z C), jeśli go przekażesz do `writeln`.

